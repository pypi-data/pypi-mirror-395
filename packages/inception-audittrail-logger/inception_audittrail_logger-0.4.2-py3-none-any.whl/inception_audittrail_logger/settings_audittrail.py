import os
import time
import socket
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

# Set up logger
logger = logging.getLogger("audittrail")
logger.setLevel(logging.DEBUG)
logger.propagate = True


class Settings(BaseSettings):
    # AppAuth Settings
    application_name: str = ""
    application_version: str = ""
    # Logging Settings
    aws_region: str = "eu-west-1"
    elasticsearch_service: str = "es"
    elasticsearch_host: str = ""
    elasticsearch_port: int = 443
    elasticsearch_verify_certs: bool = True
    elasticsearch_provider: str = ("self-hosted",)  # aws, azure, gcp, self-hosted
    elasticsearch_aws_access_key: str = ""
    elasticsearch_aws_secret_key: str = ""
    mongodb_url: str = ""
    hostname: str = socket.gethostname()
    ip_address: str = socket.gethostbyname(hostname)
    env_file: str = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_file)
    model_config = SettingsConfigDict(env_file=env_file)


@lru_cache(maxsize=1)
def get_audittrail_setting() -> Settings:
    return Settings()


def init_audittrail(
    application_name: str,
    application_version: str,
    mongodb_url: str,
    aws_region: str = "eu-west-1",
    elasticsearch_service: str = "es",
    elasticsearch_host: str = "",
    elasticsearch_port: int = 443,
    elasticsearch_verify_certs: bool = False,
    elasticsearch_provider: str = "self-hosted",  # aws, azure, gcp, self-hosted
    elasticsearch_aws_access_key: str = "",
    elasticsearch_aws_secret_key: str = "",
):

    env_file = os.path.join(os.path.dirname(__file__), ".env")
    with open(env_file, "w") as f:
        f.write(f'application_name="{application_name}"\n')
        f.write(f'application_version="{application_version}"\n')
        f.write(f'aws_region="{aws_region}"\n')
        f.write(f'elasticsearch_service="{elasticsearch_service}"\n')
        f.write(f'elasticsearch_host="{elasticsearch_host}"\n')
        f.write(f'elasticsearch_port="{elasticsearch_port}"\n')
        f.write(f'elasticsearch_verify_certs="{elasticsearch_verify_certs}"\n')
        f.write(f'elasticsearch_provider="{elasticsearch_provider}"\n')
        f.write(f'elasticsearch_aws_access_key="{elasticsearch_aws_access_key}"\n')
        f.write(f'elasticsearch_aws_secret_key="{elasticsearch_aws_secret_key}"\n')
        f.write(f'mongodb_url="{mongodb_url}"\n')

    time.sleep(3)
    os.chmod(env_file, 0o777)
    # load the settings
    audittrail_settings = get_audittrail_setting().model_dump()
    # print("Audittrail settings: ", audittrail_settings)


if __name__ == "__main__":
    init_audittrail(
        application_name="test_application",
        application_version="1.0.0",
        aws_region="eu-west-1",
        elasticsearch_service="es",
        elasticsearch_host="search-your-domain-name.eu-west-1.es.amazonaws.com",
        elasticsearch_port=443,
        elasticsearch_verify_certs=True,
        elasticsearch_provider="aws",
        mongodb_url="mongodb://localhost:27017",
    )
