import os
from pathlib import Path
from typing import List, Literal, Dict, Any, ClassVar

from pydantic import AnyHttpUrl, HttpUrl, AfterValidator
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from typing_extensions import Annotated

from .sources import MultiDotEnvSettingsSource, SSMSettingsSource, SecretsManagerSettingsSource

AnyHttpUrlString = Annotated[AnyHttpUrl, AfterValidator(lambda v: str(v))]
HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]

SettingsSourceType = Literal[
    "init",
    "env",
    "dotenv",
    "ssm",
    "secrets",
    "file_secrets"
]

default_source_config: List[Dict[str, Any]] = [
    # 3. INIT settings example
    {
        "type": "init",
    },
    # 2. ENV settings example
    {
        "type": "env",
    },
    # 3. .env file example
    {
        "type": "dotenv",
        "files": ["config/.env", "config/.env.local"]
    },
    # 4. File-based secrets example (usually Docker secrets)
    {
        "type": "filesecrets",
        "files": ["./secrets/config.json"]  # Example for file-based secret sources
    },
    # 5. AWS SSM Parameter Store example
    {
        "type": "ssm",
        "prefixes": ["/myapp/config/", "/common/secrets/"],
        "region": "us-west-2"
    },
    # 6. AWS Secrets Manager example
    {
        "type": "secrets",
        "secret_ids": ["my/secret/id1", "my/secret/id2"],
        "region": "us-west-2"
    },

]


class Settings(BaseSettings):
    """ Common configuration parameters shared between all environments.

    The settings class is designed to be flexible and extensible. You can define your own settings variables
    and use the `source_config` parameter to specify the priority/order to load them.

    This class is used to read configuration parameters from various sources, including:
    - the derived classes
    - this class
    - environment variables
    - .env (dotenv) files
    - secret files
    - AWS SSM Parameter Store (if available)
    - AWS Secrets Manager (if available)

    Read configuration parameters defined in this class, and from
    ENVIRONMENT variables and from the .env file.

    This file extends Pydantic's BaseSettings to provide a flexible settings management system
    that allows multiple .env files and AWS' SSM Parameter Store and Secrets Manager.

    The following source can be used to load settings in the specified priority:
      - init_settings
      - dotenv_settings
      - env_settings
      - file_secret_settings
      - AWS Parameter Store (if available)
      - AWS Secrets Manager (if available)

    The following environment variables should already be defined::
      - HOSTNAME (on Linux servers only - set by OS)
      - COMPUTERNAME (on Windows servers only - set by OS)

    If using AWS Services like Parameter Store or Secrets Manager, this library
    will automatically use boto3's standard credential chain:
      - Environment Variables(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.)
      - ~/.aws/credentials or configured profiles (via aws configure).
      - IAM Role on EC2, Lambda, or ECS (via Instance Metadata Service).
      - AWS CLI SSO or other advanced credential providers.

    Path where your <environment>.env file should be placed::
      - linux: /home/<user>/.local
      - darwin: /home/<user>/.local
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python'

    Path where your secret files should be placed::
      - linux: /home/<user>/.local/secrets
      - darwin: /home/<user>/.local/secrets
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python\\secrets'

    You know you are running in Docker when the "/.dockerenv" file exists.

    This class can be used as a base class for other settings classes, such as `LocalSettings`, `DevSettings` and
    setup multiple settings variables and pick the one based on the environment.

    For example, you can have `DefaultSettings` class for common settings and derive `DevSettings`, `ProdSettings`
    to override the sources_config for each.

             _setup: dict[str, Type[LocalSettings | DevSettings | QASettings | ProdSettings]] = dict(
                    local=LocalSettings or DefaultSettings,
                    dev=DevSettings,
                    qa=QASettings,
                    prod=ProdSettings
            )

            ENVIRONMENT = os.getenv('ENVIRONMENT', MISSING_ENV)
            print(f"Loading Environment: {ENVIRONMENT}")
            settings = _setup[ENVIRONMENT]()

    """
    model_config = SettingsConfigDict(
        extra='ignore',  # Allow/ignore/forbid extra fields here
    )

    source_config: ClassVar[List[Dict[str, Any]]] = default_source_config

    def __init__(self, *,
                 source_config: List[Dict[str, Any]] | None,
                 **kwargs: Any):
        """Initialize settings with explicit sources configuration."""
        self.__class__.source_config = source_config or default_source_config
        super().__init__(**kwargs)

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Custom sources after init and env (which are automatically included)
        sources: List[PydanticBaseSettingsSource] = []
        for src in cls.source_config:
            src_type = src.get("srctype", "init")
            if src_type == "init":
                if "data" in src:
                    sources.append(PydanticBaseSettingsSource(src["data"]))
                else:
                    sources.append(init_settings)
            elif src_type == "env":
                sources.append(env_settings)
            elif src_type == "dotenv":
                env_files = [Path(f) for f in src.get("files", "config/.env")]
                sources.append(MultiDotEnvSettingsSource(settings_cls, env_files))
            elif src_type == "filesecrets":
                env_files = [Path(f) for f in src.get("files", cls._getSecretsDir())]
                sources.append(MultiDotEnvSettingsSource(settings_cls, env_files))
            elif src_type == "ssm":
                sources.append(SSMSettingsSource(
                    cls,
                    prefixes=src["prefixes"],
                    region=src.get("region", "us-west-2"),
                    merge=src.get("merge", True),
                    flatten_root=src.get("flatten_root", False),
                    ttl=src.get("ttl", 3600),
                ))
            elif src_type == "secrets":
                sources.append(SecretsManagerSettingsSource(
                    cls, secret_ids=src["secret_ids"], region=src.get("region", "us-west-2")
                ))
            else:
                raise ValueError(f"Unknown source type: {src_type}")
        return tuple(sources)

    @staticmethod
    def _getSecretsDir() -> str:
        """Determine secrets directory based on Docker/non-Docker context."""
        if os.path.exists('/.dockerenv'):
            return '/run/secrets'
        else:
            secrets_dir = 'config/secrets'
            os.makedirs(secrets_dir, exist_ok=True)
            return secrets_dir
