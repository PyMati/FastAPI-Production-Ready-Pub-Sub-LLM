import secrets


class CSRFService:
    @staticmethod
    def generate_csrf_token() -> str:
        return secrets.token_urlsafe(32)
