from dotenv import dotenv_values
import pathlib
import os
import time

# ROOT DIRECTORY OF THE PROJECT
root_dir = pathlib.Path(__file__).parent.resolve()

# DOTENV FILE
config = dotenv_values(f"{root_dir}/.env")

# When it's building it feeds from .env  docker url
if config['POSTGRES_DOCKER_BUILD'] == 'True':
    PG_HOST = config["POSTGRES_HOST_DOCKER"]
elif config['POSTGRES_DOCKER_BUILD'] == 'False':
    PG_DOCKER_RUN_DEV_MODE = config['DEV_DOKER_POSTGRES']
    PG_HOST = config["POSTGRES_HOST_LOCAL"]
    os.system(PG_DOCKER_RUN_DEV_MODE) # Run docker container with postgres development usage
    time.sleep(10)
    os.system(f'echo "Service is run on {PG_HOST}"')


# PARAMS FOR THE DATABASE
PG_USER = config["POSTGRES_USER"]
PG_PASS = config["POSTGRES_PASSWORD"]
PG_PORT = config["POSTGRES_PORT"]
PG_DB_NAME = config["POSTGRES_DB_NAME"]