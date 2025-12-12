from abc import ABC, abstractmethod


class ISchema(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def insert_schema(self, polly_session, repo_key, body: dict):
        pass

    @abstractmethod
    def update_schema(self, polly_session, repo_key, body: dict):
        pass

    @abstractmethod
    def replace_schema(self, polly_session, repo_key, body: dict):
        pass

    @abstractmethod
    def validate_schema(self, polly_session, body: dict):
        pass

    @abstractmethod
    def get_schema(
        self,
        polly_session,
        repo_key,
        schema_level=[],
        source="",
        data_type="",
        return_type="dataframe",
    ):
        pass
