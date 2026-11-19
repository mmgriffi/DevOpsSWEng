import os
import pytest

@pytest.fixture(scope="session")
def base_url():
    target_env = os.getenv("TARGET_ENV")

    if target_env == "dev":
        return "http://devops-dev.cluen.com"
    elif target_env == "prod":
        return "http://devops-prod.cluen.com"
    else:
        return "http://127.0.0.1:8000"
