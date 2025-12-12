from pathlib import Path


class SecretFactory:
    def __init__(self, secrets_dir: str):
        self.__secrets_cache = self.__load_secrets(secrets_dir)

    def get(self, name: str) -> str:
        secret: str | None = self.__secrets_cache.get(name)
        if secret:
            return secret
        raise ValueError(f"Secret {name} not found")

    def __load_secrets(self, secrets_dir: str) -> dict[str, str]:
        path = Path(secrets_dir)
        if not path.is_dir():
            return {}

        secrets: dict[str, str] = {}
        for secret_file in path.iterdir():
            if secret_file.is_file():
                secrets[secret_file.name] = secret_file.read_text(encoding="utf-8").strip()
        return secrets
