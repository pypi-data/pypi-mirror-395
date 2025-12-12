from multiprocessing import AuthenticationError
import re
import requests
from polly import helpers
from polly.auth import Polly
from polly.errors import (
    InvalidParameterException,
    InvalidPathException,
    UnauthorizedException,
    InvalidJobFunctionParameterException,
    extract_json_api_error,
    has_error_message,
    error_handler,
)
from polly.helpers import parseInt

# from polly.constants import MIN_REQUIRED_KEYS_FOR_JOBS, MACHINES_FOR_JOBS
from polly.constants import COMPUTE_ENV_VARIABLE, DATA_LOG_MODES
import polly.http_response_codes as http_codes
from polly import constants as const
from polly.tracking import Track

import pandas as pd
import os
import json


class jobs:
    """
    The polly_jobs class contains functions which can be used to create, cancel and monitor polly jobs.
    Polly CLI jobs can now be initiated, managed and have a status-checked for from Polly Python.
    This lets users run jobs on the Polly cloud infrastructure by scaling computation resources as per need.
    Users can start and stop tasks and even monitor jobs.

    Note:- User must use TOKEN instead of KEYS to work with the job module of polly-python.

    Args:
        token (str): token copy from polly.

    Usage:
        from polly.jobs import jobs

        jobs = jobs(token)
    """

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
    ) -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"

    # project_id -> workspace_id
    # job_file -> json file
    @Track.track_decorator
    def submit_job(self, project_id: str, job_file=None, job_dict=None) -> pd.DataFrame:
        """
        Submits  a polly cli job in the given workspace.
        A message will be displayed on the status of the operation.
        Job configuration can be provided either as a json file using job_file parameter or
        as a dictionary using job_dict parameter

        Args:
            project_id (str):  workspace id
            job_file (str, optional): job configuration json file path, defaults to None
            job_dict (dict, optional): job configuration dictionary, defaults to None
        """
        parameter_check_dict = {}

        parameter_check_dict["project_id"] = project_id
        # neither both job_file and job_dict should be provided, nor both should not be provided.
        # only one of the two should be provided
        if (job_file is None and job_dict is None) or (job_file and job_dict):
            raise InvalidParameterException(
                "One of json_file or json_dict required for the function."
                + "Either both or none have been provided.Please check"
            )
        if job_file:
            parameter_check_dict["job_file"] = job_file
        if job_dict:
            parameter_check_dict["job_dict"] = job_dict

        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        try:
            if job_file:
                with open(job_file, "r") as jobfile:
                    jobData = json.load(jobfile)
                    # self._validate_job_json(jobData)
            else:
                jobData_json_string = json.dumps(job_dict)
                jobData = json.loads(jobData_json_string)
        except Exception as err:
            raise err

        # TODO: add file validation for json
        jobData = self._add_secret_env_keys_to_jobData(jobData, project_id)
        job_post_data = self._submit_job_to_polly(project_id, jobData)
        submittedProject_df = ""
        if job_post_data:
            submitted_job_id = job_post_data.json().get("data").get("job_id")
            project_id = job_post_data.json().get("data").get("project_id")
            submittedProject = {"Workspace ID": project_id, "Job ID": submitted_job_id}
            submittedProject_df = pd.DataFrame([submittedProject])
        return submittedProject_df

    @Track.track_decorator
    def cancel_job(self, project_id: str, job_id: str):
        """
        cancel a polly job.

        Args:
            project_id (str): workspace id
            job_id (str): job id

        Raises:
            InvalidParameterException: parameter passed are invalid
        """
        parameter_check_dict = {}
        parameter_check_dict["project_id"] = project_id
        parameter_check_dict["job_id"] = job_id
        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs/{job_id}"
        try:
            # successfull -> returns 204
            postData = self.session.delete(self.jobUrl)
            if postData.status_code == 204:
                print("Cancelled job ID " + job_id + " successfully!")
            else:
                # handling this differently because postData.text is a str
                if postData.text:
                    postData_resp_json = json.loads(postData.text)
                else:
                    postData_resp_json = postData.json()
                error = postData_resp_json.get("error")
                if error is None:
                    error = postData_resp_json.get("errors", [])[0]
                if "detail" in error:
                    detail = error.get("detail", "")
                    print("Failed to cancel the job.: " + detail)
                else:
                    print("Failed to cancel the job.")
        except Exception as err:
            print("Failed to cancel the job.")
            raise err

    @Track.track_decorator
    def job_status(self, project_id: str, job_id="", internalCalls=False) -> dict:
        """
        Get the status of a job given the rproject id and job id.
        If no job id given, gives status for all the jobs in the
        provided workspace.

        Args:
            project_id (str): workspace id
            job_id (str): job id

        Returns:
            DataFrame: Contains job id, job name and status sorted as per created timestamp
        """
        parameter_check_dict = {}
        parameter_check_dict["project_id"] = project_id
        if job_id:
            parameter_check_dict["job_id"] = job_id
        self._parameter_check_for_jobs(parameter_check_dict)
        if isinstance(project_id, int):
            project_id = str(project_id)

        sortedJobsTemp = None
        sortedJobs = []
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs/{job_id}"

        # TODO: Yogesh : from a job id if we can get the project id. -> improvement
        # TODO: job id can be a optional parameter -> MVP
        try:
            postDatas = self._get_data_for_job_id(self.jobUrl)
            if postDatas.status_code != const.OK:
                self._handle_response_errors(postDatas)
            # list of data
            else:
                sortedJobsTemp = postDatas.json()
                sortedJobs.extend(sortedJobsTemp.get("data"))
                # TODO: can remove this looping with dev testing
                for i in range(len(sortedJobsTemp.get("data"))):
                    if sortedJobsTemp.get("links", "") and sortedJobsTemp.get(
                        "links", ""
                    ).get("next", ""):
                        jobUrl = (
                            f"{self.base_url}{sortedJobsTemp.get('links').get('next')}"
                        )
                        postDatas = self._get_data_for_job_id(jobUrl)
                        if postDatas.status_code != const.OK:
                            self._handle_response_errors(postDatas)
                        sortedJobsTemp = postDatas.json()
                        sortedJobs.extend(sortedJobsTemp.get("data"))
                    else:
                        continue
        except Exception as err:
            print("Not able to get the status of the Job(s)")
            raise err
        sortedJobs = sorted(sortedJobs, key=lambda d: d["attributes"]["created_ts"])
        if internalCalls:
            return sortedJobs
        status_result_df = self._generate_job_status_df(sortedJobs)
        # with pd.option_context(
        #     "display.max_rows", 800, "display.max_columns", 800, "display.width", 1200
        # ):
        #     print(status_result_df)
        return status_result_df

    @Track.track_decorator
    def job_logs(self, project_id: any, job_id: str, mode="all"):
        """
        get logs of job

        Arguments:
            project_id (str): workspace_id
            job_id (str): job_id

        Keyword Arguments:
            mode (str): either 'latest' or 'all' logs (default: {"all"})

        Raises:
            err: RequestException
        """
        try:
            parameter_check_dict = {}
            parameter_check_dict["project_id"] = project_id
            parameter_check_dict["job_id"] = job_id
            parameter_check_dict["mode"] = mode
            self._parameter_check_for_jobs(parameter_check_dict)
            if isinstance(project_id, int):
                project_id = str(project_id)
            returndata = []
            # get the latest log of the job submitted
            if mode == "latest":
                templog = self._get_job_log(project_id, job_id, None, True)
                if templog:
                    returndata.append(templog)
                    log_signed_url = templog.get("log_signed_url")
                    response = requests.get(log_signed_url)
                    error_handler(response)
                    logData = response.text
                    print(logData)
            # get all the logs of the jobs submitted
            elif mode == "all":
                nextToken = None
                templog = self._get_job_log(project_id, job_id, nextToken)
                if templog:
                    returndata.append(templog)
                    log_signed_url = templog.get("log_signed_url")
                    response = requests.get(log_signed_url)
                    error_handler(response)
                    logData = response.text
                    print(logData)
                    nextToken = templog.get("next_token", None)
                while nextToken:
                    templog = self._get_job_log(project_id, job_id, nextToken)
                    if templog:
                        returndata.append(templog)
                        log_signed_url = templog.get("log_signed_url")
                        response = requests.get(log_signed_url)
                        error_handler(response)
                        logData = response.text
                        print(logData)
                        nextToken = templog.get("next_token", None)
        except Exception as err:
            print("Error: Not able to get the log of the job")
            raise err

    def _get_job_log(self, project_id: str, job_id: str, next_token=None, latest=False):
        """
        get the AWS signed url for the job logs.
        Returns response (str) with signed url and next token for job logs

        args:
            project_id (str/int): workspace id
            job_id (str): job id

        **kwargs:
            next_token (str): token string to fetch data (default: {None})
            latest (bool) : get latest log (default: {False})

        """
        logReturn = ""
        try:
            env = self.session.env
            self.base_url = f"https://v2.api.{env}.elucidata.io"
            self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs/{job_id}"
            if next_token:
                self.log_url = f"{self.jobUrl}/logs?next_token={next_token}"
            else:
                self.log_url = f"{self.jobUrl}/logs/?"
            if latest:
                if "next_token" in self.log_url:
                    self.log_url = f"{self.log_url}&show=latest"
                else:
                    self.log_url = f"{self.log_url}?show=latest"
            log_returned = self._get_data_for_job_id(self.log_url)
            log_returned_data = log_returned.json().get("data")
            if not log_returned_data:
                error = log_returned.json().get("error")
                if error is None:
                    error = log_returned.json().get("errors", [])[0]
                if error.get("code") == "resource_not_found":
                    print("Not able to find the logs. It seems to be not generated yet")
                    return
                else:
                    print("Not able to get the logs.")
                    return
            logReturn = log_returned_data[0].get("attributes")
            return logReturn
        except Exception as err:
            print("Not able to get the logs.")
            raise err

    def _is_valid_job_id(self, project_id: str, job_id: str):
        """
        checks if the job id provided is valid
        checks the jobid in the jobs in the workspace

        Arguments:
            project_id (int or str):  workspace id
            job_id (str): job id

        Returns:
            valid (bool): True if job id is valid
        """
        valid = False
        try:
            jobs_list = self.job_status(project_id, internalCalls=True)
            job_id_list = []
            for jobs in jobs_list:
                job_id_list.append(jobs.get("attributes").get("job_id"))
            if job_id in job_id_list:
                valid = True
        except Exception as err:
            raise err
        return valid

    def _handle_response_errors(self, postDatas):
        """
        api to handle the response errors

        Arguments:
            postDatas (json) : api response json

        """
        if postDatas.status_code == http_codes.FORBIDDEN:
            raise AuthenticationError("User access is denied. Please contact admin")
        elif postDatas.status_code == http_codes.UNAUTHORIZED:
            raise UnauthorizedException("User is unauthorized to access this")
        elif postDatas.status_code == http_codes.NOT_FOUND:
            error_title, error_detail = extract_json_api_error(postDatas.text)
            raise Exception(error_detail)
        elif postDatas.status_code == http_codes.GATEWAY_TIMEOUT:
            error_detail = postDatas.get("message", "Request timed out")
        else:
            error_title, error_detail = extract_json_api_error(postDatas.text)
            raise Exception(error_detail)

    def _generate_job_status_df(self, sortedJobs):
        """
        given a list of jobs related info dict this generates a dataframe of the job id, name and status

        Arguments:
            sortedJobs (list): list of job information

        Returns:
            status_result_df (pd.dataframe): dataframe containing job id, name
        """
        job_info_list = []
        if sortedJobs:
            for jobs in sortedJobs:
                job_info = {}
                job_info["id"] = jobs.get("attributes").get("job_id")
                job_info["name"] = jobs.get("attributes").get("job_name")
                job_info["job_state"] = jobs.get("attributes").get("state")
                job_info_list.append(job_info)
            status_result_df = pd.DataFrame(job_info_list)
            status_result_df.columns = ["Job ID", "Job Name", "Job State"]
        else:
            status_result_df = pd.DataFrame(columns=["Job ID", "Job Name", "Job State"])
        return status_result_df

    def _get_data_for_job_id(self, jobUrl):
        """
        given a url, gets the response for the url.
        """
        try:
            if jobUrl:
                self.jobUrl = jobUrl
                postDatas = self.session.get(self.jobUrl)
            else:
                postDatas = self.session.get(self.jobUrl)
        except Exception as err:
            raise err
        return postDatas

    def _add_secret_env_keys_to_jobData(self, jobData: json, project_id: str) -> json:
        """
        add env variables and values to the job data json needed for job run

        Args:
            jobData (json) :  json containing existing variables
            project_id (str):  workspace id

        Returns:
           appended job data json with the secret env variables
        """
        if "secret_env" not in jobData:
            jobData["secret_env"] = {}
        headers = self.session.headers
        if "x-api-key" in headers:
            jobData["secret_env"]["POLLY_API_KEY"] = headers.get("x-api-key")
        jobData["secret_env"]["POLLY_WORKSPACE_ID"] = project_id
        return jobData

    def _submit_job_to_polly(self, project_id: str, job_data: json):
        """
        given a complete job data and workspace id
        calling the api to start a job

        Args:
            project_id (str) : workspace id
            job_data (jsob) : json containing all required variables

        Raises:
            err

        Returns:
            response from the api call
        """
        submitBody = {"data": {"type": "jobs", "attributes": job_data}}

        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.jobUrl = f"{self.base_url}/projects/{project_id}/jobs"
        try:
            postData = self.session.post(self.jobUrl, data=json.dumps(submitBody))
            if postData.status_code != const.CREATED:
                if postData.status_code == http_codes.GATEWAY_TIMEOUT:
                    error_detail = postData.json().get("message", "Request timed out")
                    raise Exception(error_detail)
                if has_error_message(postData):
                    title, detail = extract_json_api_error(postData)
                    raise Exception(title, detail)
        except Exception as err:
            print("Not able to submit job")
            raise err
        return postData

    def _valid_cpu(self, cpu: str) -> bool:
        matches = False
        cpu_regex = "^([+-]?[0-9.]+)([m]*[-+]?[0-9]*)$"
        match = re.fullmatch(cpu_regex, cpu)
        if match is not None:
            matches = True
        return matches

    def _convert_cpu(self, cpu: str):
        cpuRegex = "^[0-9]+m$"
        if re.fullmatch(cpuRegex, cpu):
            cpu_parsed = parseInt(cpu[0:-1]) * 0.001
            return cpu_parsed
        else:
            return parseInt(cpu)

    def _parameter_check_for_jobs(self, paramter_dict: dict):
        for keys, values in paramter_dict.items():
            if keys == "project_id":
                project_id = values
                if not (
                    project_id
                    and (isinstance(project_id, str) or isinstance(project_id, int))
                ):
                    raise InvalidParameterException("project id/workspace id")
            elif keys in ["job_file", "job_dict"]:
                self._check_job_configuration_parameter(keys, values)
            elif keys == "job_id":
                job_id = values
                self._check_job_id(job_id, project_id)
            elif keys == "mode":
                mode = values
                if mode not in DATA_LOG_MODES:
                    raise InvalidParameterException(
                        f"valid mode values are : {DATA_LOG_MODES}"
                    )

    def _check_job_configuration_parameter(
        self, job_config_param_key, job_config_param_value
    ):
        if job_config_param_key == "job_file":
            job_file = job_config_param_value
            if not os.path.exists(job_file):
                raise InvalidPathException(job_file)
        elif job_config_param_key == "job_dict":
            job_dict = job_config_param_value
            if not (isinstance(job_dict, dict)):
                raise InvalidParameterException(
                    "job_dict should be a dictionary datatype"
                )

    def _check_job_id(self, job_id, project_id):
        if not (job_id and (isinstance(job_id, str))):
            raise InvalidParameterException("Missing/invalid datatype for job id")
        if not self._is_valid_job_id(project_id, job_id):
            raise InvalidJobFunctionParameterException("Job id")
