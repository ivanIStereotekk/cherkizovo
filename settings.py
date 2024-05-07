from dotenv import dotenv_values
import pathlib

# ROOT DIRECTORY OF THE PROJECT
root_dir = pathlib.Path(__file__).parent.resolve()

# DOTENV FILE
config = dotenv_values(f"{root_dir}/.env")

# When it's building it feeds from .env  docker url
if config['POSTGRES_DOCKER_BUILD'] == 'True':
    PG_HOST = config["POSTGRES_HOST_DOCKER"]
elif config['POSTGRES_DOCKER_BUILD'] == 'False':
    PG_HOST = config["POSTGRES_HOST_LOCAL"]


# PARAMS FOR THE DATABASE
PG_USER = config["POSTGRES_USER"]
PG_PASS = config["POSTGRES_PASSWORD"]
PG_PORT = config["POSTGRES_PORT"]
PG_DB_NAME = config["POSTGRES_DB_NAME"]