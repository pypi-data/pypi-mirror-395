from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class CommunicationSetting(BaseSettings):
    port: str = Field(default="50051", description="Port as a string")
    timeout: float = Field(default=30.0, description="Timeout in seconds")


    @field_validator("port")
    def validate_port(cls, v):
        if not v.isdigit() or not (0 < int(v) < 65536):
            raise ValueError(f"Port must be a numeric string between 1 and 65535, got '{v}'")
        return v

    @field_validator("timeout")
    def validate_timeout(cls, v):
        if v <= 0.0:
            raise ValueError("Timeout must be positive")
        return v


