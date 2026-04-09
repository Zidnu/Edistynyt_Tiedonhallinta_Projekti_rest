import os
import subprocess

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

_path = './models.py'
if os.path.exists(_path):
    os.remove(_path)


src_user = input("Anna lähdetietokannan (MySQL) käyttäjän nimi (oletuksena root): ")
src_pwd = input("Anna lähdetietokannan (MySQL) käyttäjän salasana (oletuksena tyhjä):")
src_db = input("Anna lähdetietokannan (MySQL) nimi: ")
src_db_port = input("Anna lähdetietokannan (MySQL) portti (oletuksena 3306): ")

if src_user == "":
    src_user = "root"

if src_db_port == "":
    src_db_port = "3306"

dst_user = input("Anna tietokannan (Postgres) käyttäjän nimi (oletuksena postgres): ")
dst_pwd = input("Anna tietokannan (Postgres) käyttäjän salasana:")
dst_db = input(f"Anna tietokannan (Postgres) nimi (oletuksena {src_db}): ")
dst_db_port = input("Anna tietokannan (Postgres) portti (oletuksena 5432): ")

if dst_db_port == "":
    dst_db_port = "5432"

if dst_db == "":
    dst_db = src_db

if dst_user == "":
    dst_user = "postgres"


src_conn_str = f"mysql+mysqlconnector://{src_user}:{src_pwd}@localhost:{src_db_port}/{src_db}"
dst_conn_str = f"postgresql+psycopg2://{dst_user}:{dst_pwd}@localhost/{dst_db}"

try:
    args_str = f"sqlacodegen_v2 {src_conn_str} --outfile models.py"
    print(args_str)
    prc = subprocess.Popen(args_str, shell=True)
    prc.communicate()
    import models

    if database_exists(dst_conn_str):
        drop_database(dst_conn_str)
    create_database(dst_conn_str)

    engine = create_engine(dst_conn_str)
    if hasattr(models, 'Base'):
        _metadata = models.Base.metadata
    elif hasattr(models, 'metadata'):
        _metadata = models.metadata
    else:
        raise Exception('metadata missing')

    _metadata.create_all(engine)


except Exception as e:
    print(e)
