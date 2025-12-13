"""Common data classes"""

import pydantic
from pydantic import ByteSize, ConfigDict, constr
from pydantic_extra_types.pendulum_dt import DateTime


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(extra="forbid")


class DataStore(BaseModel):
    name: str
    provider: constr(to_lower=True)
    bucket: str
    region: str | None = None
    default: bool = False


class Environment(BaseModel):
    name: str
    provider: constr(to_lower=True)
    image: str
    machinetype: str
    region: str
    default: bool = False
    size: ByteSize = ByteSize(20_000_000_000)


class LogMessage(BaseModel):
    message: str
    timestamp: DateTime


class Run(BaseModel):
    command: list[str]
    commit_sha: str | None = None
    creator: str
    datastore: DataStore
    environment: Environment
    message: str
    project: str
    started: DateTime
    ended: DateTime | None = None
    exit_status: int | None = None
    sha: str | None = None
    tags: list[str]
    inputs: list["Run"] | None = None

    @property
    def short_sha(self):
        return self.sha[:10]
