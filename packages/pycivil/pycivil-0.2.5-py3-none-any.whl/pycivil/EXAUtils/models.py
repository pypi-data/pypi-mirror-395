from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER = "super"
    NONE = "none"

class User(BaseModel):
    userId: str = ""
    uuid: UUID = UUID("{00000000-0000-0000-0000-000000000000}")
    active: bool = True
    usr: str = ""
    psw: str = ""
    mailLogin: str = ""
    name: str = ""
    surname: str = ""
    role: UserRole = UserRole.NONE
    currentProjectId: str = ""

    def isNull(self) -> bool:
        return self.uuid == UUID("{00000000-0000-0000-0000-000000000000}")

class Project(BaseModel):
    brief: Optional[str] = "Default"
    description: Optional[str] = ""
    id: Optional[int] = 0
    projects_defaults: Optional[int] = 0
    title: Optional[str] = ""
    uuid: Optional[UUID] = UUID("{00000000-0000-0000-0000-000000000000}")


class UserAuth(BaseModel):
    checkAuth: bool = False
    role: UserRole = UserRole.NONE
