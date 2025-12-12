from datetime import datetime

from polly import helpers
from polly import constants as const
from polly.auth import Polly
from polly.help import example
from polly.errors import wrongParamException, error_handler
from polly.tracking import Track


def _add_arguments_to_url(
    url: str,
    batch_id: str = None,
    org_id: str = None,
    status: str = None,
    priority: str = None,
    user_id: str = None,
    page_size: int = None,
    page_after: int = None,
    search_term: str = None,
):
    """
    This function is used to add query parameters to a provided URL, if provided.
    These query parameters are: batch_id, org_id, user_id, page_size, page_after

    Args:
        url (str): The URL in which the query parameters are to be added.
        batch_id (str): add batch_id to the query parameter
        org_id (str): add org_id to the query parameter
        user_id (str): add user_id to the query parameter
        page_size (str): add page_size to the query parameter
        page_after (str): add page_after to the query parameter

    Returns:
        Returns a string, which is the URL with added query parameters.

    """
    if (
        batch_id is not None
        or org_id is not None
        or status is not None
        or priority is not None
        or user_id is not None
        or page_size is not None
        or page_after is not None
    ):
        url = f"{url}?"
        if batch_id is not None:
            url = f"{url}filter[batch_id]={batch_id}&"

        if org_id is not None:
            url = f"{url}filter[org_id]={org_id}&"

        if status is not None:
            url = f"{url}filter[status]={status}&"

        if priority is not None:
            url = f"{url}filter[priority]={priority}&"

        if user_id is not None:
            url = f"{url}filter[user_id]={user_id}&"

        if page_size is not None:
            url = f"{url}page[size]={page_size}&"

        if page_after is not None:
            url = f"{url}filter[after]={page_after}&"

        if search_term is not None:
            url = f"{url}filter[search_term]={search_term}"

    return url


def _generate_batch_name():
    return "Batch at {:%B-%d-%Y} - {:%H:%M}".format(
        datetime.now().astimezone(), datetime.now().astimezone()
    )


def _generate_run_name():
    return "Run created on {:%B-%d-%Y} at {:%H:%M}".format(
        datetime.now().astimezone(), datetime.now().astimezone()
    )


def _filter_response(data: dict):
    if type(data) is list:
        return [_filter_response(item) for item in data]

    if "attributes" in data.keys():
        attributes = data.get("attributes")
        if data.get("type") == "pipelines":
            attributes.pop("parameter_schema", None)

        if data.get("type") == "batches":
            attributes.pop("notification_channels")

        if data.get("type") == "runs":
            attributes = data.get("attributes")

        data["attributes"] = attributes

    if "links" in data.keys():
        data.pop("links")

    return data


class Pipelines:
    """
    Pipeline class enables users to interact with the functional properties of the Pipelines infrastructure \
    such as create, read or delete pipelines. It can also be used for creating pipeline batches and runs.

    Args:
        token (str): token copy from polly.

    Usage:
        from polly.pipelines import Pipeline

        pipeline = Pipeline(token)
    """

    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly"):
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://apis.{self.session.env}.elucidata.io"
        self.orchestration_url = f"{self.base_url}/pravaah/orchestration"
        self.monitoring_url = f"{self.base_url}/pravaah/monitoring"

    @Track.track_decorator
    def list_pipelines(self, search_term: str = None):
        """
        This function returns all the pipelines that the user have access to
        Please use this function with default values for the paramters.

        Args:
            None

        Returns:
            list: It will return a list of JSON objects. (See Examples)
        """
        all_pipelines = []
        default_page_size = 20
        start_url = f"{self.orchestration_url}/pipelines"
        start_url = _add_arguments_to_url(
            start_url, page_size=default_page_size, search_term=search_term
        )
        response = self.session.get(start_url)
        error_handler(response)
        pipelines = response.json().get("data")
        all_pipelines = all_pipelines + pipelines
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)
            response.raise_for_status()
            response_json = response.json()
            all_pipelines = all_pipelines + response_json.get("data")
            next_link = response_json.get("links").get("next")

        data = [_filter_response(pipeline) for pipeline in all_pipelines]
        return data

    @Track.track_decorator
    def get_pipeline(self, pipeline_id: str):
        """
        This function returns the pipeline data of the provided pipeline_id.

        Args:
            pipeline_id (str): pipeline_id for required pipeline

        Returns:
            object: It will return a JSON object with pipeline data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """

        if pipeline_id is None:
            raise wrongParamException("pipeline_id can not be None")

        if not isinstance(pipeline_id, str):
            raise wrongParamException("pipeline_id should be a string")

        url = f"{self.orchestration_url}/pipelines/{pipeline_id}"
        response = self.session.get(url)
        error_handler(response)
        data = response.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def create_batch(
        self,
        pipeline_id: str,
        name: str = None,
        description: str = None,
        priority: str = "low",
        customer_org: str = None,
        tags: dict = {},
        domain_context: dict = {},
    ):
        """
        This function is used to create a Pipeline batch.\n
        A batch is a collection of runs, this functions creates an empty batch in which the runs can be added.

        Args:
            pipeline_id (str): pipeline_id for which the batch is to be created
            name (str): name of the batch
            description (str): description of the batch
            priority (str): priority of the batch, can be low | medium | high
            customer_org (str) : organization
            tags (dict): a dict of key-value pair with tag_name -> tag_value mapping
            domain_context (dict): domain context for a batch

        Returns:
            object: It will return a JSON object which is the pipeline batch. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        if name is None:
            name = _generate_batch_name()

        if priority not in ["low", "medium", "high"]:
            raise wrongParamException(
                "A batch priority can be only one of these values: low | medium | high"
            )

        batch_object = {
            "data": {
                "type": "batches",
                "attributes": {
                    "name": name,
                    "description": description,
                    "priority": priority,
                    "domain_context": domain_context,
                    "tags": tags,
                    "customer_org": customer_org,
                    "pipeline_id": pipeline_id,
                },
            }
        }

        batch_url = f"{self.orchestration_url}/batches"
        batch = self.session.post(batch_url, json=batch_object)
        error_handler(batch)
        data = batch.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def submit_run(
        self, batch_id: str, parameters: dict, config: dict = {}, run_name: str = None
    ):
        """
        This function is used for creating runs for a particular batch.

        Args:
            batch_id (str): batch_id in which the run is to be created.
            parameters (dict): a key-value object of all the required parameters of pipeline
            config (dict): config definition for the pipeline run. should be of format \
                            {"infra":  {"cpu": int, "memory": int, "storage": int}}
            run_name (str, Optional): name of the run, auto-generated if not assigned

        Returns:
            Object: It will return a JSON object with pipeline data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        if parameters is None or config is None:
            raise wrongParamException("The provided arguments can not be of NoneType")

        if run_name is None:
            run_name = _generate_run_name()

        run = {
            "type": "runs",
            "attributes": {
                "batch_id": batch_id,
                "name": run_name,
                "config": config,
                "parameters": parameters,
            },
        }

        runs_object = {"data": [run]}
        runs_url = f"{self.orchestration_url}/runs"
        response = self.session.post(runs_url, json=runs_object)
        error_handler(response)

        data = response.json().get("data")[0]
        if "error" in data.keys() or "errors" in data.keys():
            raise Exception()

        return _filter_response(data)

    @Track.track_decorator
    def list_batches(
        self,
        status: str = None,
        priority: str = None,
        search_term: str = None,
    ):
        """
        This function returns the list of pipeline batches

        Args:
            status (str, Optional): to filter batches based on the status
            priority (str, Optional): to filter the batches based on priority
            search_term (str, Optional): to filter the batches based on a search term.

        Returns:
            list: It will return a list of JSON object with pipeline batches. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        all_batches = []
        default_page_size = 20
        start_url = _add_arguments_to_url(
            f"{self.orchestration_url}/batches",
            page_size=default_page_size,
            status=status,
            priority=priority,
            search_term=search_term,
        )
        response = self.session.get(start_url)
        error_handler(response)
        batches = response.json().get("data")
        all_batches = all_batches + batches
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)

            response.raise_for_status()
            response_json = response.json()
            all_batches = all_batches + response_json.get("data")

            next_link = response_json.get("links").get("next")

        data = [_filter_response(batch) for batch in all_batches]
        return data

    @Track.track_decorator
    def get_batch(self, batch_id: str):
        """
        This function returns the pipeline batch data \n
        Args:
            batch_id (str): the batch_id for which the data is required

        Returns:
            list: It will return a list of JSON object with pipeline batch data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/batches/{batch_id}"
        batch = self.session.get(url)
        error_handler(batch)
        data = batch.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def list_runs(self, batch_id: str):
        """
        This function returns the list of runs executed for a batch.

        Args:
            batch_id (str): the batch_id for which the runs are required

        Returns:
            list: It will return a list of JSON object with pipeline runs. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        all_runs = []
        default_page_size = 20
        start_url = _add_arguments_to_url(
            f"{self.orchestration_url}/runs",
            page_size=default_page_size,
            batch_id=batch_id,
        )
        response = self.session.get(start_url)
        error_handler(response)
        runs = response.json().get("data")
        all_runs = all_runs + runs
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)
            response.raise_for_status()
            response_json = response.json()
            all_runs = all_runs + response_json.get("data")
            next_link = response_json.get("links").get("next")

        data = [_filter_response(run) for run in all_runs]
        return data

    @Track.track_decorator
    def get_run(self, run_id: str):
        """
        This function returns the run data for the provided run_id \n
        Args:
            run_id (str): the run_id for which the data is required

        Returns:
            object: It will return a JSON object with pipeline run data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/runs/{run_id}"
        run = self.session.get(url)
        error_handler(run)
        data = run.json().get("data", run.json())
        return _filter_response(data)

    @Track.track_decorator
    def cancel_run(self, run_id: str):
        """
        This function cancels a run
        Args:
            run_id (str): the run_id of the run to be cancelled

        Returns:
            object: It will return a JSON object with pipeline run data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/runs/{run_id}/cancel"
        run = self.session.post(url)
        error_handler(run)
        data = run.json().get("data", run.json())
        return _filter_response(data)

    @Track.track_decorator
    def delete_storage(self, run_id: str):
        """
        This function deletes storage for the run
        Args:
            run_id (str): the run_id of the run for which the storage has to be deleted

        Returns:
            object: It will return a JSON object with message. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/runs/{run_id}/storage"
        run = self.session.delete(url)
        error_handler(run)
        data = run.json().get("data", run.json())
        return _filter_response(data)
