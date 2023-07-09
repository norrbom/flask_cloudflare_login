from os import environ
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
import json
import pytest
from flask_cloudflare_login.access import CfUser


@pytest.fixture(autouse=True)
def conf_test():
    environ["TEST_CF_GROUPS"] = "[{}]"
    load_dotenv(dotenv_path=Path(__file__).parent.joinpath(".env"))


def get_user():
    return CfUser(
        email=getenv("TEST_CF_EMAIL"), groups=json.loads(getenv("TEST_CF_GROUPS"))
    )


def test_user_id():
    assert get_user().id == "foo.bar@example.com"
