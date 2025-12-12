from setuptools import setup, find_packages

setup(
    name="pii-engine",
    version="1.0.0",
    description="Production-grade PII Engine for Employment Exchange",
    author="PII Platform Team",
    packages=find_packages(),
    install_requires=[
        "faker>=19.0.0",
        "cryptography>=41.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "redis>=4.6.0",
        "python-multipart>=0.0.6"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)