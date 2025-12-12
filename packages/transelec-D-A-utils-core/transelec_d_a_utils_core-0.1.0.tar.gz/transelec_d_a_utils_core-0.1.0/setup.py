from setuptools import setup, find_packages

setup(
    name='transelec-D_A-utils-core',
    version='0.1.0',
    packages=find_packages(),
    description='Core utilities for data transformation and structured logging.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Luis Fuenzalida', # Reemplazar con tu información
    author_email='bi-lfuenzalida@transelec.cl', # Reemplazar con tu información
    url='https://github.com/Transelec-repository/mv_utils', # Reemplazar con tu repositorio
    license='MIT',
    install_requires=[], 
    extras_require={
        'bq': [ 
            'google-cloud-bigquery>=2.0.0',
            'google-api-core>=1.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)