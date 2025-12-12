# -*- coding: utf-8 -*-
"""
logx.py
- Consola y archivo JSONL por ambiente.
- Control de verbosidad con LOG_LEVEL (DEBUG|INFO|WARN|ERROR). Default: INFO.
- emit_once(event, ...) imprime una sola vez por corrida para ese 'event'.

Extensión autónoma:
- VM EXECUTION LOG a BigQuery (fwk_ingest.vm_execution_log)
  * start_vm_event(project_name, transaction_type, endpoint_alias) -> VMEvent
  * finish_vm_event_with_logger(event, status, logger, error_detail=None) -> inserta fila en BQ
  * La lógica BQ es inyectada mediante la clase BigQueryVMEventLogger.
"""
import time
import os, sys, json, socket, uuid, threading
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any, Dict, List

# --- CONSTANTES DE BIGQUERY (FIJAS PARA LOGS CENTRALIZADOS) ---
_VMLOG_DATASET = "FWK_INGEST"
_VMLOG_TABLE   = "VM_EXECUTION_LOGS" 
# --- FIN CONSTANTES DE BIGQUERY ---


# ------------------------
# Logger básico (Console/File)
# ------------------------
_LEVEL_ORDER = {"DEBUG":10, "INFO":20, "WARN":30, "WARNING":30, "ERROR":40}
_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
_MIN_LEVEL = _LEVEL_ORDER.get(_LOG_LEVEL, 20)

_ENV = (os.getenv("ENV", "DES") or "DES").upper()
_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = _LOG_DIR / (f"{_ENV.lower()}.log")

_PRETTY = sys.stdout.isatty()

_CONTEXT = {
    "component": None,
    "env": _ENV,
    "gcp_project": None,
    "gcs_bucket": None,
    "bq_dataset": None,
}
_EMITTED_ONCE = set()

_ICONS = {"DEBUG":"∙", "INFO":"✓", "WARN":"⚠", "WARNING":"⚠", "ERROR":"✖"}
_COLORS = {
    "DEBUG":"\033[90m", "INFO":"\033[92m", "WARN":"\033[93m",
    "WARNING":"\033[93m", "ERROR":"\033[91m", "RESET":"\033[0m",
}

def _color(level: str, text: str) -> str:
    if not _PRETTY: return text
    c = _COLORS.get(level.upper(), "")
    r = _COLORS["RESET"]
    return f"{c}{text}{r}" if c else text

def _now_iso():
    return datetime.now(timezone.utc).isoformat()

def _should_print(level: str) -> bool:
    return _LEVEL_ORDER.get(level.upper(), 20) >= _MIN_LEVEL

def set_component(name: str):
    _CONTEXT["component"] = name

def set_context(**kwargs):
    for k, v in kwargs.items():
        if k in ("gcp_project","gcs_bucket","bq_dataset"):
            _CONTEXT[k] = v

def get_trace_id() -> str:
    tid = os.environ.get("TRACE_ID")
    if not tid:
        tid = str(uuid.uuid4()); os.environ["TRACE_ID"] = tid
    return tid

def _write_file(line: str):
    with _LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def _to_console(event: str, level: str, rec: dict):
    if not _PRETTY:
        print(json.dumps(rec, ensure_ascii=False, separators=(",",":")))
        sys.stdout.flush()
        return
    ts_local = datetime.fromisoformat(rec["ts"]).astimezone().strftime("%H:%M:%S")
    icon = _ICONS.get(level, "•")
    comp = rec.get("component") or "-"
    skip = {"ts","level","event","trace_id","host","component","env","gcp_project","gcs_bucket","bq_dataset"}
    kvs = []
    for k, v in rec.items():
        if k in skip: 
            continue
        if isinstance(v, (list, dict)) and len(json.dumps(v)) > 120:
            kvs.append(f"{k}=…")
        else:
            kvs.append(f"{k}={v}")
    msg = f"[{_ENV}][{ts_local}] {comp} ▶ {event}"
    if kvs:
        msg += " " + "  ".join(kvs)
    print(_color(level, f"{icon} {msg}"))
    sys.stdout.flush()

def emit(event: str, level: str = "INFO", **fields):
    level = level.upper()
    if not _should_print(level):
        return
    rec = {
        "ts": _now_iso(),
        "level": "WARNING" if level == "WARN" else level,
        "event": event,
        "trace_id": get_trace_id(),
        "host": socket.gethostname(),
    }
    for k, v in _CONTEXT.items():
        if v is not None:
            rec[k] = v
    for k, v in fields.items():
        try:
            json.dumps(v); rec[k] = v
        except Exception:
            rec[k] = str(v)
    line = json.dumps(rec, ensure_ascii=False, separators=(",",":"))
    _write_file(line)
    _to_console(event, rec["level"], rec)

def emit_once(event: str, level: str = "INFO", **fields):
    key = (event, level.upper())
    if key in _EMITTED_ONCE:
        return
    _EMITTED_ONCE.add(key)
    emit(event, level=level, **fields)

# -------------------------------------------------------------
# VM EXECUTION LOG → BigQuery (Inyección de Dependencia)
# -------------------------------------------------------------

class VMEvent:
    def __init__(self, project_name: str, transaction_type: str, endpoint_alias: str):
        self.execution_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{uuid.uuid4().hex[:4]}"
        self.vm_id = f"vm_{project_name}_{transaction_type}_{endpoint_alias}"
        self.thread_id = threading.get_ident()
        self.start_dt = datetime.now(timezone.utc)

class BigQueryVMEventLogger:
    """
    Clase para manejar la inserción de eventos VM en BigQuery.
    Dataset y Tabla son fijos para la centralización de logs.
    """
    def __init__(self, bq_client: Any, project_id: str):
        self._client = bq_client
        self._project_id = project_id 
        self._dataset_id = _VMLOG_DATASET
        self._table_id = _VMLOG_TABLE
        self._full_table_id = f"{project_id}.{_VMLOG_DATASET}.{_VMLOG_TABLE}"
        self._table_ensured = False

    def ensure_table(self):
        """
        Asegura que el Dataset y la Tabla existan en BigQuery usando el project_id inyectado.
        """
        if self._table_ensured:
            return

        try:
            from google.cloud import bigquery
            from google.api_core.exceptions import NotFound, Conflict

            ds_ref = bigquery.DatasetReference(self._project_id, self._dataset_id)
            try:
                self._client.get_dataset(ds_ref)
            except NotFound:
                ds = bigquery.Dataset(ds_ref)
                ds.location = "southamerica-west1"
                self._client.create_dataset(ds)
                emit("VMLOG_DATASET_CREATED", level="INFO", dataset=str(ds_ref), bq_project=self._project_id)

            table_ref = ds_ref.table(self._table_id)
            try:
                self._client.get_table(table_ref)
            except NotFound:
                schema = [
                    bigquery.SchemaField("EXECUTION_ID", "STRING"),
                    bigquery.SchemaField("VM_ID",        "STRING"),
                    bigquery.SchemaField("THREAD_ID",    "INT64"),
                    bigquery.SchemaField("ERROR_DETAIL", "STRING"),
                    bigquery.SchemaField("STATUS",       "STRING"),
                    bigquery.SchemaField("START_DT",     "TIMESTAMP"),
                    bigquery.SchemaField("END_DT",       "TIMESTAMP"),
                    bigquery.SchemaField("DURATION",     "FLOAT64"),
                ]
                self._client.create_table(bigquery.Table(table_ref, schema=schema))
                emit("VMLOG_TABLE_CREATED", level="INFO", table=str(table_ref), bq_project=self._project_id)
            
            self._table_ensured = True
            
        except Conflict:
            time.sleep(1)
            self._table_ensured = True
        except Exception as e:
            emit("VMLOG_INIT_FATAL_ERROR", level="ERROR", error=str(e), note="No se pudo asegurar la tabla de logs BQ.")
            self._table_ensured = False

    def insert_vm_event(self, row: Dict[str, Any]) -> None:
        """Inserta una fila de log en BigQuery."""
        if not self._client or not self._table_ensured:
            emit("VM_EXECUTION_LOG_SKIP", level="WARN", note="Cliente BQ no inicializado o tabla no asegurada.")
            return

        try:
            from google.api_core.exceptions import BadRequest
            
            errors = self._client.insert_rows_json(self._full_table_id, [row])
            if errors:
                emit("VM_EXECUTION_LOG_WRITE_ERR", level="ERROR", errors=str(errors))
            else:
                emit("VM_EXECUTION_LOG_WRITE_OK", level="DEBUG", table=self._full_table_id)
                
        except BadRequest as e:
            emit("VM_EXECUTION_LOG_BAD_REQUEST", level="ERROR", error=str(e))
        except Exception as e:
            emit("VM_EXECUTION_LOG_FATAL", level="ERROR", error=str(e))

def start_vm_event(project_name: str, transaction_type: str, endpoint_alias: str) -> VMEvent:
    """Crea y retorna un nuevo VMEvent."""
    return VMEvent(project_name, transaction_type, endpoint_alias)

def finish_vm_event_with_logger(
    ev: VMEvent, 
    status: str, 
    logger: BigQueryVMEventLogger, 
    error_detail: Optional[str] = None
) -> None:
    """Finaliza el evento y lo inserta en BigQuery usando el logger inyectado."""
    end_dt = datetime.now(timezone.utc)
    duration = (end_dt - ev.start_dt).total_seconds()
    row = {
        "EXECUTION_ID": ev.execution_id,
        "VM_ID": ev.vm_id,
        "THREAD_ID": int(ev.thread_id),
        "ERROR_DETAIL": (error_detail if error_detail else None),
        "STATUS": status,
        "START_DT": ev.start_dt.isoformat(),
        "END_DT": end_dt.isoformat(),
        "DURATION": float(duration),
    }
    logger.insert_vm_event(row)