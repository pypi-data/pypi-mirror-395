from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name= "rdbmpy",
    packages=find_packages(),
    version="1.0.12",
    license="Apache License",
    description="A Python package for managing database migrations with PostgreSQL, MySQL, and SQL Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Guilherme Makoto Sacoman Dakuzaku",
    author_email="makoto@rocketti.com.br",
    url="https://github.com/gdakuzak/rdbmpy",
    keywords=["database", "migration", "postgresql", "mysql", "sqlserver", "orm", "sqlalchemy"],
    install_requires=[
        "greenlet>=1.1.0",
        "psycopg[binary]>=3.1",
        "python-dotenv>=0.10.2",
        "SQLAlchemy>=1.3.17",
        "pymysql>=1.0.0",
    ],
    extras_require={
        'sqlserver': ['pyodbc>=4.0.39'],
    },
    entry_points={
        'console_scripts': [
            'rdbmpy = src.migrate:main'
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
