import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class User:
    username: str
    password: str

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, password='***')"


def _user(prefix: str, default_username: str = "", default_password: str = "") -> User:
    return User(
        username=os.getenv(f"{prefix}_USER", default_username),
        password=os.getenv(f"{prefix}_PASSWORD", default_password),
    )


STANDARD_USER = _user("STANDARD", "standard_user", "secret_sauce")
LOCKED_USER = _user("LOCKED", "locked_out_user", "secret_sauce")
PROBLEM_USER = _user("PROBLEM", "problem_user", "secret_sauce")