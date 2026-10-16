import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class User:
    username: str
    password: str


def _user(prefix: str) -> User:
    return User(
        username=os.getenv(f"{prefix}_USER", ""),
        password=os.getenv(f"{prefix}_PASSWORD", ""),
    )


STANDARD_USER = _user("STANDARD")
LOCKED_USER = _user("LOCKED")
PROBLEM_USER = _user("PROBLEM")