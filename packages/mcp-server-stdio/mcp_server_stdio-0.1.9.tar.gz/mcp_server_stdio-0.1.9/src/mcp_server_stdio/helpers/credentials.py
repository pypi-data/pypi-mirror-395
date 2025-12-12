# helpers/credentials.py

import os
from dataclasses import dataclass
from fastmcp import Context

@dataclass
class Credentials:
    api_key: str
    secret_key: str
    base_url: str
    zone_uuid: str

    def to_headers(self) -> dict[str, str]:
        return {
            "apikey": self.api_key,
            "secretkey": self.secret_key,
        }

class CredentialsService:

    @staticmethod
    def from_env() -> Credentials:
        return Credentials(
            api_key=os.getenv("API_KEY", ""),
            secret_key=os.getenv("SECRET_KEY", ""),
            base_url=os.getenv("BASE_URL", ""),
            zone_uuid=os.getenv("ZONE_UUID", "")
        )

    @staticmethod
    def from_context(context: Context) -> Credentials:
        return getattr(context, "credentials", CredentialsService.from_env())

