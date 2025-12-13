from pydantic import BaseModel, BaseSettings


class RpcConfig(BaseModel):
    comms_url: str = "localhost:50051"


# class SelfConfig(BaseModel):
#     name: str


class AppConfig(BaseSettings):
    rpc: RpcConfig = RpcConfig()
    # app: SelfConfig

    class Config:
        env_nested_delimiter = "__"
        env_file = ".env"
        env_file_encoding = "utf-8"


CONFIG: AppConfig = AppConfig()
