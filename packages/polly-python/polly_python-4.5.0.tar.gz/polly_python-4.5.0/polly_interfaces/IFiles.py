from abc import ABC, abstractmethod


class IFiles(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_datasets(
        self,
        polly_session,
        repo_id: int,
        source_folder_path: dict,
        destination_folder_path="",
        priority="low",
        validation=False,
    ):
        pass

    @abstractmethod
    def update_datasets(
        self,
        polly_session,
        repo_id: int,
        source_folder_path: dict,
        destination_folder_path="",
        priority="low",
        validation=False,
    ):
        pass

    @abstractmethod
    def delete_datasets(
        self, polly_session, repo_id: int, dataset_ids: list, dataset_file_path_dict={}
    ):
        pass

    @abstractmethod
    def get_all_file_paths(
        self, polly_session, repo_id: int, dataset_id: str, internal_call=False
    ):
        pass
