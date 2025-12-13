from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    id: int = 0


class Configuration(BaseModel):
    key: str = ""
    value: str = ""


class TopicIdOnly(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int


class TagIdOnly(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int


class CatalogueIdOnly(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int


class RequirementIdOnly(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int


class ExtraEntry(Base):
    content: str = Field(min_length=1)
    extraTypeId: int
    requirementId: int


class ExtraType(Base):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    extraType: int = Field(ge=1, le=3)
    children: list[ExtraEntry] = []


class Requirement(Base):
    key: str = Field(max_length=20)
    title: str = Field(max_length=200)
    description: str
    visible: bool = True
    parentId: int
    tags: list["TagIdOnly"] = []

    def toIdOnly(self) -> RequirementIdOnly:
        return RequirementIdOnly.model_validate(self.model_dump())


class Tag(Base):
    name: str = Field(min_length=1, max_length=50)
    requirements: list["RequirementIdOnly"] = []
    catalogues: list["CatalogueIdOnly"] = []

    def toIdOnly(self) -> TagIdOnly:
        return TagIdOnly.model_validate(self.model_dump())


class Topic(Base):
    key: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    parentId: int | None = None

    def toIdOnly(self) -> TopicIdOnly:
        return TopicIdOnly.model_validate(self.model_dump())


class Catalogue(Base):
    key: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    topics: list["TopicIdOnly"] = []
    tags: list["TagIdOnly"] = []

    def toIdOnly(self) -> CatalogueIdOnly:
        return CatalogueIdOnly.model_validate(self.model_dump())


class Comment(Base):
    comment: str = Field(min_length=1)
    completed: bool = False
    requirementId: int
    parentId: int


class User(BaseModel):
    id: str = ""
    email: str = ""
    created: float = 0
    active: bool = True
    notificationMailOnCommentChain: bool = False
    notificationMailOnRequirementComment: bool = False


class ServiceUser(BaseModel):
    id: str = ""
    email: str | None = None
