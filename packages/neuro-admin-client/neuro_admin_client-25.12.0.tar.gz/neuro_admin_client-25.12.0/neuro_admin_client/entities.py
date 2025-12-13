from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import Any, cast

from typing_extensions import Self
from yarl import URL


__all__ = [
    "Action",
    "Balance",
    "Cluster",
    "ClusterUser",
    "ClusterUserRoleType",
    "ClusterUserWithInfo",
    "FullNameMixin",
    "OrderedEnum",
    "Org",
    "OrgCluster",
    "OrgNotificationIntervals",
    "OrgUser",
    "OrgUserRoleType",
    "OrgUserWithInfo",
    "Permission",
    "Project",
    "ProjectUser",
    "ProjectUserRoleType",
    "ProjectUserWithInfo",
    "Quota",
    "User",
    "UserInfo",
]


class FullNameMixin:
    first_name: str | None
    last_name: str | None

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        return ""


@dataclass(frozen=True)
class UserInfo(FullNameMixin):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class User(FullNameMixin):
    name: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = None


@dataclass(frozen=True)
class Balance:
    credits: Decimal | None = None
    spent_credits: Decimal = Decimal(0)

    @property
    def is_non_positive(self) -> bool:
        return self.credits is not None and self.credits <= 0


@dataclass(frozen=True)
class Quota:
    total_running_jobs: int | None = None


@unique
class ClusterUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    USER = "user"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class Cluster:
    name: str
    default_credits: Decimal | None
    default_quota: Quota
    default_role: ClusterUserRoleType
    maintenance: bool = False


@dataclass(frozen=True)
class OrgNotificationIntervals:
    balance_projection_seconds: list[int] | None
    """How many seconds left till the balance reaches zero?
    A list of integers, where each number represents a seconds-based interval,
    at which the organization management team will receive a notification,
    if the projected usage will lead to a reaching of a zero-balance in that
    amount of seconds.
    """
    balance_amount: list[int] | None
    """What exact balance amounts should trigger a notification?
    """
    balance_depletion_seconds: list[int] | None
    """If a balance is negative, when we should send a notification?
    e.g. 86_400 means 1 day after org reaches a zero balance.
    """


@dataclass(frozen=True)
class Org:
    name: str
    balance: Balance = Balance()
    user_default_credits: Decimal | None = None
    notification_intervals: OrgNotificationIntervals | None = None


@unique
class OrgUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class OrgUser:
    org_name: str
    user_name: str
    role: OrgUserRoleType
    balance: Balance

    def add_info(self, user_info: UserInfo) -> "OrgUserWithInfo":
        return OrgUserWithInfo(
            user_name=self.user_name,
            role=self.role,
            org_name=self.org_name,
            balance=self.balance,
            user_info=user_info,
        )


@dataclass(frozen=True)
class OrgUserWithInfo(OrgUser):
    user_info: UserInfo


@dataclass(frozen=True)
class OrgCluster:
    org_name: str
    cluster_name: str
    balance: Balance
    quota: Quota
    default_credits: Decimal | None = None
    default_quota: Quota = Quota()
    default_role: ClusterUserRoleType = ClusterUserRoleType.USER
    storage_size: int | None = None
    maintenance: bool = False


@dataclass(frozen=True)
class ClusterUser:
    cluster_name: str
    user_name: str
    role: ClusterUserRoleType | None
    quota: Quota
    balance: Balance
    org_name: str | None

    def add_info(self, user_info: UserInfo) -> "ClusterUserWithInfo":
        return ClusterUserWithInfo(
            cluster_name=self.cluster_name,
            user_name=self.user_name,
            role=self.role,
            quota=self.quota,
            balance=self.balance,
            org_name=self.org_name,
            user_info=user_info,
        )


@dataclass(frozen=True)
class ClusterUserWithInfo(ClusterUser):
    user_info: UserInfo


@unique
class ProjectUserRoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WRITER = "writer"
    READER = "reader"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__().__repr__()


@dataclass(frozen=True)
class Project:
    name: str
    cluster_name: str
    org_name: str | None
    is_default: bool = False  # Enables auto add new tenant users to thi project
    default_role: ProjectUserRoleType = ProjectUserRoleType.WRITER
    has_virtual_kube: bool = False


@dataclass(frozen=True)
class ProjectUser:
    user_name: str
    cluster_name: str
    org_name: str | None
    project_name: str
    role: ProjectUserRoleType

    def add_info(self, user_info: UserInfo) -> "ProjectUserWithInfo":
        return ProjectUserWithInfo(
            project_name=self.project_name,
            cluster_name=self.cluster_name,
            user_name=self.user_name,
            org_name=self.org_name,
            user_info=user_info,
            role=self.role,
        )


@dataclass(frozen=True)
class ProjectUserWithInfo(ProjectUser):
    user_info: UserInfo


class OrderedEnum(str, Enum):
    _order: int

    def __new__(cls, value: str) -> "OrderedEnum":
        order = len(cls.__members__)
        obj = cast("OrderedEnum", str.__new__(cls, value))  # type: ignore[redundant-cast]
        obj._value_ = value
        obj._order = order
        return obj

    def __ge__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._order >= other._order
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._order > other._order
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._order <= other._order
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._order < other._order
        return NotImplemented


@unique
class Action(OrderedEnum):
    DENY = "deny"
    LIST = "list"
    READ = "read"
    WRITE = "write"
    MANAGE = "manage"

    @classmethod
    def public(cls) -> list["Action"]:
        return [cls.READ, cls.WRITE, cls.MANAGE]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__().__repr__()


def check_action_allowed(actual: Action, requested: Action | str) -> bool:
    if isinstance(requested, str):
        requested = Action(requested)
    return actual >= requested


@dataclass(frozen=True)
class Permission:
    uri: URL
    action: Action

    def __init__(self, uri: Any, action: Action | str):
        object.__setattr__(self, "uri", uri if isinstance(uri, URL) else URL(uri))
        if isinstance(action, str):
            action = Action(action)
        object.__setattr__(self, "action", action)

    def with_manage_action(self) -> "Permission":
        return replace(self, action=Action.MANAGE)

    def check_action_allowed(self, requested: Action | str) -> bool:
        return check_action_allowed(self.action, requested)

    def can_list(self) -> bool:
        return self.check_action_allowed(Action.LIST)

    def can_read(self) -> bool:
        return self.check_action_allowed(Action.READ)

    def can_write(self) -> bool:
        return self.check_action_allowed(Action.WRITE)

    def to_payload(self) -> dict[str, str]:
        return {"uri": str(self.uri), "action": self.action.value}

    @classmethod
    def from_payload(cls, perm: dict[str, str]) -> Self:
        return cls(uri=perm["uri"], action=perm["action"])

    def __str__(self) -> str:
        return f"Permission(uri={self.uri!s}, action={self.action.value})"
