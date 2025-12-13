from reqdb.api import API, Auth
from reqdb.models import (
    Catalogue,
    Comment,
    Configuration,
    ExtraEntry,
    ExtraType,
    Requirement,
    ServiceUser,
    Tag,
    Topic,
    User,
)


class ReqDB:

    api: API

    def __init__(
        self,
        fqdn: str,
        auth: Auth,
        insecure: bool = False,
    ) -> None:
        ReqDB.api = API(fqdn, auth, insecure)

    class Tags:
        endpoint: str = "tags"
        model = Tag

        @classmethod
        def get(cls, id: int) -> Tag:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[Tag]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[Tag]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: Tag) -> Tag:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Tag) -> Tag:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class Topics:
        endpoint: str = "topics"
        model = Topic

        @classmethod
        def get(cls, id: int) -> Topic:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[Topic]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[Topic]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: Topic) -> Topic:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Topic) -> Topic:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class Requirements:
        endpoint: str = "requirements"
        model = Requirement

        @classmethod
        def get(cls, id: int) -> Requirement:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[Requirement]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[Requirement]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: Requirement) -> Requirement:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Requirement) -> Requirement:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class ExtraTypes:
        endpoint: str = "extraTypes"
        model = ExtraType

        @classmethod
        def get(cls, id: int) -> ExtraType:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[ExtraType]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[ExtraType]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: ExtraType) -> ExtraType:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: ExtraType) -> ExtraType:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class ExtraEntries:
        endpoint: str = "extraEntries"
        model = ExtraEntry

        @classmethod
        def get(cls, id: int) -> ExtraEntry:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[ExtraEntry]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[ExtraEntry]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: ExtraEntry) -> ExtraEntry:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: ExtraEntry) -> ExtraEntry:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class Catalogues:
        endpoint: str = "catalogues"
        model = Catalogue

        @classmethod
        def get(cls, id: int) -> Catalogue:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[Catalogue]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[Catalogue]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: Catalogue) -> Catalogue:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Catalogue) -> Catalogue:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class Comment:
        endpoint: str = "comments"
        model = Comment

        @classmethod
        def get(cls, id: int) -> Comment:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}/{id}"))

        @classmethod
        def find(cls, query: str) -> list[Comment]:
            data = ReqDB.api.get(f"{cls.endpoint}/find?query={query}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def all(cls) -> list[Comment]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: Comment) -> Comment:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Comment) -> Comment:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

    class Audit:
        endpoint: str = "audit"

        @classmethod
        def _targetCheck(cls, obj: str):
            target = [
                "extraEntries",
                "extraTypes",
                "requirements",
                "tags",
                "topics",
                "catalogues",
                "comments",
            ]
            if obj not in [
                "extraEntries",
                "extraTypes",
                "requirements",
                "tags",
                "topics",
                "catalogues",
                "comments",
            ]:
                raise KeyError(f"Audit object can only one of: {', '.join(target)}")

        @classmethod
        def get(cls, obj: str, id: int) -> dict:
            cls._targetCheck(obj)
            return ReqDB.api.get(f"{cls.endpoint}/{obj}/{id}")

        @classmethod
        def all(cls, obj: str) -> dict:
            cls._targetCheck(obj)
            return ReqDB.api.get(f"{cls.endpoint}/{obj}")

    class Configuration:
        endpoint: str = "config/system"
        model = Configuration

        @classmethod
        def all(cls) -> list[Configuration]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: str, data: Configuration) -> Configuration:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

    class User:
        endpoint: str = "config/user"
        model = User

        @classmethod
        def get(cls) -> User:
            return cls.model.model_validate(ReqDB.api.get(f"{cls.endpoint}"))

        @classmethod
        def update(cls, data: User) -> User:
            return cls.model.model_validate(ReqDB.api.update(f"{cls.endpoint}", data))

    class ServiceUser:
        endpoint: str = "/config/service/users"
        model = ServiceUser

        @classmethod
        def all(cls) -> list[ServiceUser]:
            data = ReqDB.api.get(f"{cls.endpoint}")
            return [cls.model.model_validate(d) for d in data]

        @classmethod
        def update(cls, id: int, data: ServiceUser) -> ServiceUser:
            return cls.model.model_validate(
                ReqDB.api.update(f"{cls.endpoint}/{id}", data)
            )

        @classmethod
        def add(cls, data: ServiceUser) -> ServiceUser:
            return cls.model.model_validate(ReqDB.api.add(f"{cls.endpoint}", data))

        @classmethod
        def delete(cls, id: int) -> bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}")
