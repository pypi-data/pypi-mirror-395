from datetime import datetime, timezone
import jwt
from time import time


def generate_jwt(private_key: bytes, app_id: str) -> str:
    """Generate a JWT to authenticate requests to GitHub's API
    :param private_key: the contents of the private key generated from GitHub
    :param app_id: the GitHub App ID
    :return: the JWT
    """

    now = int(time())
    payload = {
        # issued at time, 60 seconds in the past to allow for clock drift
        "iat": now - 60,
        # JWT expiration time (10 minute maximum)
        "exp": now + (9 * 60),
        # GitHub App's identifier
        "iss": app_id,
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def read_file(file_path: str) -> str:
    with open(f"{file_path}", "r") as file:
        return file.read()


def is_blank(string) -> bool:
    # returns True if the string is None, empty, or only whitespace
    return not string or not string.strip()


def is_not_blank(string: str) -> bool:
    # returns False if the string is None, empty, or only whitespace
    return not is_blank(string)


def to_datetime_utc(datetime_value: str, datetime_format: str = "%Y-%m-%dT%H:%M:%SZ") -> datetime | None:
    if is_blank(datetime_value):
        return None
    return datetime.strptime(datetime_value, datetime_format).replace(tzinfo=timezone.utc)
