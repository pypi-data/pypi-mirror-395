from dataclasses import dataclass


@dataclass
class ZitadelConfig:
    authority: str
    client_id: str
    project_id: str

    @classmethod
    def load(cls) -> "ZitadelConfig":
        return cls(
            authority="https://synvex.zitadel.cloud",
            client_id="346204250872807426",
            project_id="346204250872807425"
        )
