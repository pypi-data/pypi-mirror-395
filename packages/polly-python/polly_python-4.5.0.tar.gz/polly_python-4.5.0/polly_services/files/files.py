from polly_interfaces.IFiles import IFiles
from polly import helpers
from polly_services.files import files_hlpr
import pandas as pd
import warnings
from polly import constants as const
from polly_services import polly_services_hlpr
from polly.errors import error_handler, paramException
import polly.http_response_codes as http_codes
import time


class Files(IFiles):
    def __init__(self):
        pass

    def add_datasets(
        self,
        polly_session,
        repo_id: int,
        source_folder_path: dict,
        priority="low",
        validation=False,
    ):
        """Function to ingest the dataset and metadata in omixatlas

        Args:
            polly_session (_type_): _description_
            repo_id (int): _description_
            source_folder_path (dict): _description_
            priority (str, optional): _description_. Defaults to "low".
            validation (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        try:
            files_hlpr.parameter_check_for_add_dataset(
                repo_id, source_folder_path, priority
            )

            data_file_list, metadata_file_list = files_hlpr.create_file_list(
                source_folder_path
            )

            # data metadata file mapping
            # initial data metadata mapping dict containing all the files
            data_metadata_mapping = files_hlpr.map_data_metadata_files(
                data_file_list, metadata_file_list, source_folder_path
            )

            validation_dataset_lvl = {}
            if validation:
                validation_dataset_lvl = files_hlpr.check_status_file(
                    source_folder_path
                )
                (
                    data_file_list,
                    metadata_file_list,
                ) = files_hlpr.filter_files_after_dataset_lvl_validation(
                    data_file_list,
                    metadata_file_list,
                    validation_dataset_lvl,
                    source_folder_path,
                    data_metadata_mapping,
                )
                # create data_metadata_mapping again with filtered files after validation
                data_metadata_mapping = (
                    files_hlpr.map_data_metadata_files_after_validation(
                        data_file_list, metadata_file_list
                    )
                )

            # sai has confirmed -> every file will have same tokens
            # does not depend on the destination folder -> so empty destination
            # folder also ok
            (
                session_tokens,
                bucket_name,
                package_name,
                metadata_directory,
            ) = files_hlpr.get_session_tokens(polly_session, repo_id)

            # folder paths
            data_source_folder_path = source_folder_path["data"]
            metadata_source_folder_path = source_folder_path["metadata"]

            # Upload details
            metadata_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "metadata_directory": metadata_directory,
            }
            data_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "package_name": package_name,
            }

            # list of list which will store all the results
            # at last assign it to a dataframe
            file_status_dict = {}

            file_status_dict, data_file_list = files_hlpr.upload_metadata_in_add(
                polly_session,
                repo_id,
                priority,
                metadata_file_list,
                metadata_upload_details,
                metadata_source_folder_path,
                file_status_dict,
                data_metadata_mapping,
                data_file_list,
            )

            file_status_dict = files_hlpr.upload_data_in_add(
                repo_id,
                data_file_list,
                data_upload_details,
                data_source_folder_path,
                file_status_dict,
                polly_session,
            )

            return self.ingestion_and_updation_print_commons(
                file_status_dict, validation, polly_session, repo_id
            )
        except Exception as err:
            raise err

    def update_datasets(
        self,
        polly_session,
        repo_id: int,
        source_folder_path: dict,
        priority="low",
        file_mapping={},
        validation=False,
    ):
        """_summary_

        Args:
            polly_session (_type_): _description_
            repo_id (int): _description_
            source_folder_path (dict): _description_
            priority (str, optional): _description_. Defaults to "low".
            file_mapping (list, optional): _description_. Defaults to list with dummy entry.
            validation (bool, optional): _description_. Defaults to False.
        """
        try:
            files_hlpr.parameter_check_for_update_dataset(
                repo_id, source_folder_path, priority, file_mapping
            )

            data_file_list, metadata_file_list = files_hlpr.create_file_list(
                source_folder_path
            )

            # mapping dict
            (
                data_metadata_mapping,
                unmapped_data_file_names,
                unmapped_metadata_file_names,
            ) = files_hlpr.map_metadata_files_for_update(
                data_file_list, metadata_file_list, source_folder_path
            )

            # check if unmapped files -> pair file exists in OA -> raise warning
            # if pair file does not exist
            # based on that update the data_metadata_mapping_dict, data_file_list, metadata_file_list

            # go through this function once to check if everything seems right ??
            (
                data_metadata_mapping,
                data_file_list,
                metadata_file_list,
                unmapped_metadata_file_names,
                unmapped_data_file_names,
            ) = files_hlpr.check_for_unmapped_files_in_oa(
                data_metadata_mapping,
                data_file_list,
                metadata_file_list,
                unmapped_data_file_names,
                unmapped_metadata_file_names,
                file_mapping,
                polly_session,
                source_folder_path,
                repo_id,
            )

            # only metadata file names -> no ext as ext is common
            if unmapped_metadata_file_names:
                files_hlpr.raise_warning_for_unmapped_metadata_file_update(
                    unmapped_metadata_file_names
                )

            # full data file names with ext
            if unmapped_data_file_names:
                files_hlpr.raise_warning_for_unmapped_data_file_update(
                    unmapped_data_file_names
                )

            validation_dataset_lvl = {}
            # dataset level validation is on the metadata files -> so that must not be empty
            if validation and metadata_file_list:
                validation_dataset_lvl = files_hlpr.check_status_file(
                    source_folder_path
                )
                (
                    data_file_list,
                    metadata_file_list,
                ) = files_hlpr.filter_files_after_dataset_lvl_validation(
                    data_file_list,
                    metadata_file_list,
                    validation_dataset_lvl,
                    source_folder_path,
                    data_metadata_mapping,
                )
                # create data_metadata_mapping again with filtered files after validation
                data_metadata_mapping = (
                    files_hlpr.map_data_metadata_files_after_validation(
                        data_file_list, metadata_file_list
                    )
                )

            # sai has confirmed -> every file will have same tokens
            # does not depend on the destination folder -> so empty destination
            # folder also ok
            (
                session_tokens,
                bucket_name,
                package_name,
                metadata_directory,
            ) = files_hlpr.get_session_tokens(polly_session, repo_id)

            # folder paths
            data_source_folder_path = source_folder_path.get("data", "")
            metadata_source_folder_path = source_folder_path.get("metadata", "")

            # Upload details
            metadata_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "metadata_directory": metadata_directory,
            }
            data_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "package_name": package_name,
            }

            # list of list which will store all the results
            # at last assign it to a dataframe
            file_status_dict = {}

            if metadata_file_list:
                file_status_dict, data_file_list = files_hlpr.upload_metadata_in_update(
                    polly_session,
                    repo_id,
                    priority,
                    metadata_file_list,
                    metadata_upload_details,
                    metadata_source_folder_path,
                    file_status_dict,
                    data_metadata_mapping,
                    data_file_list,
                )

            if data_file_list:
                file_status_dict = files_hlpr.upload_data_in_add(
                    repo_id,
                    data_file_list,
                    data_upload_details,
                    data_source_folder_path,
                    file_status_dict,
                    polly_session,
                )

            return self.ingestion_and_updation_print_commons(
                file_status_dict, validation, polly_session, repo_id
            )
        except Exception as err:
            raise err

    def ingestion_and_updation_print_commons(
        self, file_status_dict: dict, validation: str, polly_session, repo_id: str
    ):
        """_summary_

        Args:
            file_status (dict): _description_
        """
        # iterating the status dict
        # generating appropriate messages
        data_upload_results_df = pd.DataFrame()
        result_list = []
        if file_status_dict:
            result_list = files_hlpr.generating_response_from_status_dict(
                file_status_dict, result_list
            )

            # generating DF
            data_upload_results_df = pd.DataFrame(
                result_list, columns=["File Name", "Message"]
            )
            # print message before delay
            print(const.WAIT_FOR_COMMIT)
            # delay added after the files are uploaded
            # before commit API is hit
            time.sleep(30)
            files_hlpr.commit_data_to_repo(polly_session, repo_id)
            files_hlpr.print_dataframe(800, 800, 1200, data_upload_results_df)

        if validation:
            print("\n")
            print("-----Files which are Not Validated-------")
            helpers.display_df_from_list(
                files_hlpr.dataset_level_metadata_files_not_uploaded,
                "Invalid Metadata Files",
            )
            print("\n")
            helpers.display_df_from_list(
                files_hlpr.data_files_whose_metadata_failed_validation,
                "Invalid Data Files",
            )

        # reset global variables storing validation results
        # flushes out the previous state of variables and creates
        # new state
        files_hlpr.reset_global_variables_with_validation_results()
        return data_upload_results_df

    def delete_datasets(
        self, polly_session, repo_id: int, dataset_ids: list, dataset_file_path_dict={}
    ):
        """Delete Datasets

        Args:
            polly_session (_type_): _description_
            repo_id (int): _description_
            dataset_ids (list): _description_
            dataset_file_path_dict (dict, optional): _description_. Defaults to {}.

        Raises:
            err: _description_
        """
        try:
            files_hlpr.parameter_check_for_delete_dataset(
                repo_id, dataset_ids, dataset_file_path_dict
            )

            repo_id = polly_services_hlpr.make_repo_id_string(repo_id)

            # check if dataset_file_path_dict keys subset of dataset_ids
            files_hlpr.dataset_file_path_is_subset_dataset_id(
                dataset_ids, dataset_file_path_dict
            )

            # normalise the file path which user has given
            dataset_file_path_dict = files_hlpr.normalize_file_paths(
                dataset_file_path_dict
            )
            # {"<dataset_id>": ["<file_paths>"]}
            # single file_path => Means single element in the list
            # if multiple file paths => Means multiple elements in the list
            dataset_s3_keys_dict = self._s3_key_dataset(
                polly_session, repo_id, dataset_ids
            )

            # convert the dict to df at last
            result_dict = {}

            # result dict format
            # {'GSE101942_GPL11154': [{'Message': 'Dataset not deleted because file_path for
            #  the dataset_id is incorrect', 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'},
            # {'Message': 'Dataset not deleted because file_path for the dataset_id is incorrect',
            # 'Folder Path': 'transcriptomics_907s/GSE76311_GPL17586.gct'}]}
            result_dict = self._delete_datasets_helper(
                polly_session, repo_id, dataset_s3_keys_dict, dataset_file_path_dict
            )

            valid_deletion_entry = files_hlpr.check_res_dict_has_file_deleted_entries(
                result_dict
            )

            if result_dict and valid_deletion_entry:
                # if result dict is generated and there is at least
                # 1 deletion entry in the df -> then commit API will be hit
                # to log the deletion status of the valid entry
                # print message before delay
                print(const.WAIT_FOR_COMMIT_DELETE)
                # delay added after the files are uploaded
                # before commit API is hit
                time.sleep(30)

                # informing infra to commit the delete data in the repository
                files_hlpr.commit_data_to_repo(polly_session, repo_id)

                files_hlpr.convert_delete_datasets_res_dict_to_df(result_dict)
            elif result_dict:
                # result dict is generated but there is no valid entry of deletion
                # for any of the dataset_ids in the dict
                # commit API not hit
                files_hlpr.convert_delete_datasets_res_dict_to_df(result_dict)
            else:
                print(const.DELETION_OPERATION_UNSUCCESSFUL_FOR_ALL_DATASET_IDS)

        except Exception as err:
            raise err

    def _s3_key_dataset(self, polly_session, repo_id: int, dataset_ids: list) -> dict:
        """
        S3 keys for dataset ids
        """
        # key -> `dataset_id`, value -> single or multiple file keys
        # {<dataset_id>:["list of file ids"] or str}
        # if for a dataset_id there is error message from API
        # str will represent that error message
        s3_keys_dict = {}
        for dataset_id in dataset_ids:
            list_files_resp = self.get_all_file_paths(
                polly_session, repo_id, dataset_id, internal_call=True
            )
            s3_keys_dict[dataset_id] = list_files_resp

        # clearing the cache of list files after getting file paths
        # for all the dataset_ids
        # no need for this now
        # files_hlpr.list_files.cache_clear()
        return s3_keys_dict

    # this function needs to be refactored as per the new API
    # there needs to be a different implementation of this function
    # def get_all_file_paths(
    #     self, polly_session, repo_id: int, dataset_id: str, internal_call=False
    # ):
    #     """Get all file paths where the file is stored corresponding to the
    #     repo_id and dataset_id

    #     Args:
    #         repo_id (int): repo_id of the omixatlas
    #         dataset_ids (str): dataset_id present in the omixatlas

    #     Raises:
    #         paramError: If Params are not passed in the desired format or value not valid.

    #     Returns:
    #         list: all the file paths corresponding to repo_id and dataset_id
    #         Error: If repo_id or dataset id does not exist in the system
    #     """
    #     files_hlpr.get_all_file_paths_param_check(repo_id, dataset_id)
    #     # list of the all the file paths in the system
    #     # corresponding to the passed repo_id and dataset id
    #     file_paths = []

    #     # check if omixatlas exists
    #     # if omixatlas does not exist then it will raise an error
    #     polly_services_hlpr.get_omixatlas(polly_session, repo_id)

    #     # cache it once and clear the cache once the function execution ends
    #     list_files_resp_list = files_hlpr.list_files(polly_session, repo_id)

    #     # internal_call argument is only for system use
    #     # It will not be exposed to the users
    #     # If internal_call is True -> this method called from inside delete datasets
    #     # in that Only raise exception if Forbidden or Unauthorized
    #     # In all other cases -> return the error message so that
    #     # file deletion process does not get halted. Error Message gets logged
    #     # For these files deletion will be skipped
    #     # This is to ease out the process of Bulk Delete

    #     # iterating over list_files_resp_list to get all the list of files
    #     for list_files_resp in list_files_resp_list:
    #         if list_files_resp.status_code != const.OK and internal_call:
    #             if list_files_resp.status_code == http_codes.NOT_FOUND:
    #                 error_msg_dict = polly_services_hlpr.extract_error_message(
    #                     list_files_resp.text
    #                 )
    #                 return error_msg_dict.get("detail", "")
    #         elif list_files_resp.status_code != const.OK:
    #             error_handler(list_files_resp)
    #         else:
    #             list_files_resp = list_files_resp.json()
    #             list_files_resp_data = list_files_resp.get("data", [])
    #             for file_data in list_files_resp_data:
    #                 file_metadata = file_data.get("attributes", {}).get("metadata", {})
    #                 file_dataset_id = file_metadata.get("dataset_id", "")
    #                 if file_dataset_id == dataset_id:
    #                     # id in the response corresponds to file path
    #                     # where the file is present
    #                     file_id = file_data.get("id")
    #                     file_paths.append(file_id)

    #             if not file_paths:
    #                 warnings.formatwarning = (
    #                     lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    #                 )
    #                 warnings.warn(
    #                     f"{dataset_id} does not exist in the Omixatlas {repo_id} "
    #                 )

    #     return file_paths

    def get_all_file_paths(
        self, polly_session, repo_id: int, dataset_id: str, internal_call=False
    ):
        """_summary_

        Args:
            polly_session (_type_): _description_
            repo_id (int): _description_
            dataset_id (str): _description_
            internal_call (bool, optional): _description_. Defaults to False.
        """
        try:
            files_hlpr.get_all_file_paths_param_check(repo_id, dataset_id)
            # list of the all the file paths in the system
            # corresponding to the passed repo_id and dataset id
            file_paths = []

            # check if omixatlas exists
            # if omixatlas does not exist then it will raise an error
            polly_services_hlpr.get_omixatlas(polly_session, repo_id)

            file_paths = files_hlpr.check_destination_folder_for_dataset_id(
                polly_session, dataset_id, repo_id
            )
            # if file_paths is empty it is an internal call -> then return a message
            # that message will be put in the res df
            if not file_paths and internal_call:
                message = f"{dataset_id} files not found in this {repo_id}"
                print(message)
                return message
            return file_paths
        except Exception as err:
            raise err

    def _delete_datasets_helper(
        self,
        polly_session,
        repo_id: str,
        dataset_s3_keys_dict: dict,
        dataset_file_path_dict: dict,
    ):
        """Calls the API to delete the datasets and deletes the dataset

        Args:
            repo_id (str): repo_id of the OmixAtlas
            dataset_s3_keys_dict(dict): Dictionary contaning datasetid and corresponding file paths
            dataset_file_path_dict(dict): In case multiple files are present for the dataset_id \
            The file_paths from where users needs to delete the file can be passed in this. \
            Format -> {<dataset_id>:["<List of file paths from where user wants to delete file>"]}
        """

        result_dict = {}
        for datasetid_key, file_path in dataset_s3_keys_dict.items():
            if isinstance(file_path, str):
                # if only string type value is present corresponding to
                # dataset id means that it is an error message
                # Put the error message for corresponding dataset id directly
                # in the result dict
                res = [{"Message": file_path, "Folder Path": ""}]
                result_dict[datasetid_key] = res
            elif isinstance(file_path, list):
                if len(file_path) == 1:
                    # this means only single file present in the system for
                    # the dataset id -> so case of single file deletion for
                    # dataset id
                    # passing the file_path present at the 0th index as that is the
                    # only file_path in the list
                    dataset_id_single_res_dict = self._delete_file_with_single_path(
                        polly_session,
                        repo_id,
                        datasetid_key,
                        file_path[0],
                        dataset_file_path_dict,
                    )
                    # append dataset_id_res_dict to main dict
                    # working of update dict
                    """
                    Original Dictionary:
                    {'A': 'Geeks'}
                    Dictionary after updation:
                    {'A': 'Geeks', 'B': 'For', 'C': 'Geeks'}
                    """
                    # here updating the existing dict with key value pair of delete msg
                    # for the current dataset id
                    if dataset_id_single_res_dict:
                        result_dict.update(dataset_id_single_res_dict)
                elif len(file_path) > 1:
                    dataset_id_mulitple_res_dict = (
                        self._delete_file_with_multiple_paths(
                            polly_session,
                            repo_id,
                            datasetid_key,
                            dataset_file_path_dict,
                            file_path,
                        )
                    )
                    if dataset_id_mulitple_res_dict:
                        # if dataset_id_mulitple_res_dict is not empty
                        # means the API request for deletion of dataset id is processed
                        # then df will have entry, update it into resultant df
                        # else skip for this dataset id
                        result_dict.update(dataset_id_mulitple_res_dict)

        return result_dict

    def _delete_file_with_single_path(
        self,
        polly_session,
        repo_id: int,
        datasetid_key: str,
        file_path: str,
        dataset_file_path_dict: dict,
    ):
        """Delete File with single path

        Args:
            repo_id (int): repo_id of the OmixAtlas
            datasetid_key (str): dataset_id to be deleted
            file_path (str): file path of the dataset_id with single location in system
            dataset_file_path_dict (dict): dataset_id, file_path dict
        """

        dataset_id_single_res_dict = {}
        # intialising value corresponding to datasetid_key as list
        # corresponding to multiple paths passed by the user
        # there can be multiple entries for a single dataset_id
        dataset_id_single_res_dict[datasetid_key] = []
        # checking if datasetid_key is present in dataset_file_path_dict
        # Ideally if datasetid_key has single path where file is present
        # Passing the path is not required, because the system will find out the
        # path from the list file API and delete the file
        # Giving the path is necessary when the dataset_id is present in multiple
        # files in the Omixatlas, in that system on its own can't decide which file
        # to delete, in that case -> users need to pass the file path from where
        # they want the file to be deleted.
        if datasetid_key in dataset_file_path_dict:
            # dataset_file_path_dict[datasetid_key] -> file_path passed by the user
            # dataset_file_path_dict[datasetid_key] -> list format
            # paths passed by the user already normalised before hand
            # already normalised beforehand
            for user_file_path in dataset_file_path_dict[datasetid_key]:
                # file_path -> file_path of the dataset_id file in the system
                # user_file_path -> file_path of the dataset_id file passed by the user

                if user_file_path != file_path:
                    delete_res_val = files_hlpr.user_file_path_incorrect(
                        user_file_path, datasetid_key
                    )
                    dataset_id_single_res_dict[datasetid_key].append(delete_res_val)
                else:
                    delete_res_val = self._delete_file_with_single_path_helper(
                        polly_session, repo_id, user_file_path
                    )
                    dataset_id_single_res_dict[datasetid_key].append(delete_res_val)
        else:
            # file path not passed delete the dataset id from the file path
            # obtained from the system
            delete_res_val = self._delete_file_with_single_path_helper(
                polly_session, repo_id, file_path
            )
            dataset_id_single_res_dict[datasetid_key].append(delete_res_val)
        return dataset_id_single_res_dict

    def _delete_file_with_single_path_helper(
        self, polly_session, repo_id: str, file_path: str
    ) -> dict:
        """helper function for single path delete datasets
        Args:
            repo_id(str): repo_id of the Omixatlas
            file_path(str): file_path from where file needs to be deleted
        """
        delete_url = (
            f"{polly_session.discover_url}/repositories/{repo_id}/files/{file_path}"
        )
        resp = polly_session.session.delete(delete_url)
        if resp.status_code == http_codes.ACCEPTED:
            res = {
                "Message": "Request Accepted. Dataset will be deleted in the next version of OmixAtlas",
                "Folder Path": f"{file_path}",
            }
            return res
        elif resp.status_code == http_codes.FORBIDDEN:
            # raising error in the case when the user is forbidden
            # to delete the file which may occur from repository lock
            # or invalid permissions for the user
            # rest in all the cases, no need to raise error
            # just store the error message in the result dict
            # and skip the file
            error_handler(resp)
        else:
            res = {
                "Message": f"Deletion failed because {resp.text}. Please contact polly.support@elucidata.io",
                "Folder Path": f"{file_path}",
            }
            return res

    def _delete_file_with_multiple_paths(
        self,
        polly_session,
        repo_id: int,
        datasetid_key: str,
        dataset_file_path_dict: dict,
        file_paths: list,
    ):
        """Delete the files for the datasetid having multiple paths

        Args:
            repo_id (int): repo_id of the OmixAtlas
            datasetid_key (str): dataset_id to be deleted
            file_path (list):
            dataset_file_path_dict (_type_): _description_
        """
        dataset_id_res_dict = {}
        # intialising value corresponding to datasetid_key as list
        # corresponding to multiple paths passed by the user
        # there can be multiple entries for a single dataset_id
        dataset_id_res_dict[datasetid_key] = []
        # dataset id file is not unique in the Omixatlas
        # there are multiple files with same dataset id
        if datasetid_key not in dataset_file_path_dict:
            warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
            warnings.warn(
                f"Unable to delete file with dataset_id: {datasetid_key} "
                + "present in mutiple files/folders. "
                + "Please pass the path of the file which needs to be deleted. "
                + "For getting the list of paths/folders where the dataset_id files are "
                + "can be fetching using <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                + "For any questions, please reach out to polly.support@elucidata.io. "
            )
            # break line added -> for better UX
            print("\n")
            res = {
                "Message": "Dataset not deleted because no file_path passed.",
                "Folder Path": f"{file_paths}",
            }
            dataset_id_res_dict[datasetid_key].append(res)
        else:
            passed_file_paths = dataset_file_path_dict[datasetid_key]
            if not passed_file_paths:
                raise paramException(
                    title="paramException",
                    detail=(
                        "No file_path passed for this dataset_id. "
                        + "Multiple files are present for the dataset id. "
                        + "Please pass list of paths from which file needs to be deleted. "
                        + f"Please pass paths from this list {file_paths} "
                        + "Alternatively for getting the list of file_paths for the dataset_id "
                        + "call <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                    ),
                )

            # Intersection of file paths for the dataset_id which are present in the system
            # and what users have passed
            # file_paths -> file paths for the dataset id present in the system
            # passed_file_paths -> file paths passed by the user for the dataset id
            file_paths_to_delete = list(set(file_paths) & set(passed_file_paths))

            # if there are no file paths passed which corresponds to file paths
            # present in the system for the given dataset_id
            if not file_paths_to_delete:
                raise Exception(
                    f"file paths incorrect, it does not belong to dataset_id -> {datasetid_key}"
                    + f". Please pass file path from these {file_paths}. "
                    + "Alternatively for getting the list of file_paths for the dataset_id "
                    + "call <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                )

            # if from the file paths passed not all the file paths have the
            # file with the given dataset id
            invalid_paths = list(set(passed_file_paths) - set(file_paths_to_delete))

            # raise warning for those invalid file paths
            if invalid_paths:
                # loop over invalid paths, raise warning and log the entry in the df
                for invalid_path in invalid_paths:
                    delete_msg_val = (
                        files_hlpr.warning_invalid_path_delete_dataset_multiple_paths(
                            invalid_path, datasetid_key
                        )
                    )
                    dataset_id_res_dict[datasetid_key].append(delete_msg_val)

            for valid_file_path in file_paths_to_delete:
                delete_msg_val = self._delete_file_with_single_path_helper(
                    polly_session, repo_id, valid_file_path
                )
                dataset_id_res_dict[datasetid_key].append(delete_msg_val)

            return dataset_id_res_dict
