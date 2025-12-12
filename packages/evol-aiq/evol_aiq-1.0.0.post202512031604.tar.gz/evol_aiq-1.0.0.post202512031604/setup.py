from datetime import datetime

from setuptools import setup, find_packages
import os
import logging

logger = logging.getLogger(__name__)

timestamp = datetime.now().strftime("%Y%m%d%H%M")

build_version = os.environ.get("EVOL_AIQ_VERSION", "0.1.1")
version = f"{build_version}.post{timestamp}"
print("*****************************************************************")
print("*********    ", version, "     ***************")
print("*****************************************************************")
setup(
        name='evol-aiq',
        version=version,
        description='Evolving AIQ base build',
        author='Evolving AIQ Team (PD,RK)',
        author_email='your.email@example.com',
        packages=find_packages(),
        install_requires=[
            'pandas',  # List any dependencies here, e.g., 'requests>=2.20.0',
            'Flask',
            'gunicorn',
            'pyyaml',
            'scikit-learn',
            'matplotlib',
            'numpy',
            'joblib',
            'fastapi',
            'missingno',
            'seaborn',
            'lightgbm',
            'xgboost',
            'dash',
            'dash_bootstrap_components',
            'pyhive',
            'sqlalchemy',
            'thrift',
            'thrift_sasl',
            'orjson'
        ],
    )
