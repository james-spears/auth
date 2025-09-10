from enum import IntEnum


class RoleTypes(IntEnum):
    RELEASE_TEAM_MEMBER = 1
    RELEASE_TEAM_LEAD = 2
    DEVELOPER_TEAM_MEMBER = 3
    DEVELOPER_TEAM_LEAD = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
