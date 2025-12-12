from setuptools import setup

setup(
    name="postgresdbmodel",
    version="0.1.1",
    description="Capa de acceso a datos para PostgreSQL integrada con SQLAlchemy",
    author="darth wayne",
    author_email="darrthwayne@gmail.com",
    packages=["postgresdbmodel"],
    install_requires=[
        "SQLAlchemy",
        "psycopg2-binary"
    ],
    python_requires='>=3.7',
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)