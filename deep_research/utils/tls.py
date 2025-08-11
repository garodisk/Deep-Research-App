import os, certifi

def apply_certifi_env() -> None:
    """Ensure Python HTTPS clients trust a CA bundle in corp / Windows setups."""
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())