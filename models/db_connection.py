import sqlalchemy
import os
from dotenv import load_dotenv
from pathlib import Path
from os import getenv

def load_env(env_file: str=getenv("DOTENV_PATH", "."), fallover=True):
    print(f"Loading environment from {env_file}")
    if Path(env_file).is_file():
        print(f"Loading environment from .env file {env_file}")
        load_dotenv(env_file)
    elif fallover and Path(".env").is_file():
        print(f"Loading environment from .env file {env_file}")
        load_dotenv()

load_env()

def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,  # 30 seconds
        "pool_recycle": 1800,  # 30 minutes
    }
    # if development_env:
    if os.environ.get("DB_LOCAL"):
        print("Connectiong to local db")
        return init_local_connection_engine(db_config)
    elif os.environ.get("DB_HOST"):
        print("Connectiong to google via tcp")
        return init_tcp_connection_engine(db_config)
    else:
        print("Connectiong to google via socket")
        return init_unix_connection_engine(db_config)

def init_local_connection_engine(db_config):
    # pool=sqlalchemy.create_engine('postgresql+psycopg2://ggarcia:@localhost/flin', echo=True)
    pool=sqlalchemy.create_engine(os.environ["DB_URL"], echo=True)
    print("Connected... pool started", os.environ["DB_URL"])
    return pool

def init_tcp_connection_engine(db_config):
    ## FROM DOCS --> For public IP paths, Cloud Functions provides encryption and connects using the Cloud SQL Auth proxy through Unix sockets.
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])
    
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name  # e.g. "my-database-name"
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_tcp]
    pool.dialect.description_encoding = None
    return pool


def init_unix_connection_engine(db_config):
    ## FROM DOCS --> For public IP paths, Cloud Functions provides encryption and connects using the Cloud SQL Auth proxy through Unix sockets.
    # secrets secret.

    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    #db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/tmp/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    # print("{}:{}:{}:{}:{}".format(db_user, db_name, db_pass, db_socket_dir, cloud_sql_connection_name))
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        #"postgresql+pg8000://speechio_dev:4ZxUgr5Z73OM6gUnbCkC@/speechio_dev?unix_sock=/cloudsql/sppech-io:europe-west1:speechio-prod/.s.PGSQL.5432",
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": f"/cloudsql/{cloud_sql_connection_name}/.s.PGSQL.5432"
            }
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_socket]
    pool.dialect.description_encoding = None
    return pool
