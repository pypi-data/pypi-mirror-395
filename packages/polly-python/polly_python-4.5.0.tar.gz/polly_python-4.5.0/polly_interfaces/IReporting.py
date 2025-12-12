from abc import ABC, abstractmethod


class IReporting(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def link_report(
        self,
        polly_session,
        repo_key: str,
        dataset_id: str,
        workspace_id: int,
        workspace_path: str,
        access_key: str,
    ):
        pass

    @abstractmethod
    def link_report_url(
        self, polly_session, repo_key: str, dataset_id: str, url_to_be_linked: str
    ):
        pass

    @abstractmethod
    def fetch_linked_reports(self, polly_session, repo_key: str, dataset_id: str):
        pass

    @abstractmethod
    def delete_linked_report(
        self, polly_session, repo_key: str, dataset_id: str, report_id: str
    ):
        pass
