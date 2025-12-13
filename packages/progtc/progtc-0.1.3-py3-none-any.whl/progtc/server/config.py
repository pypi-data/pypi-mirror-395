from pydantic import BaseModel


class ServerConfig(BaseModel):
    api_key: str = "1234567890"
    tool_call_timeout: float = 10.0
    code_execution_timeout: float = 30.0


server_config = ServerConfig()
