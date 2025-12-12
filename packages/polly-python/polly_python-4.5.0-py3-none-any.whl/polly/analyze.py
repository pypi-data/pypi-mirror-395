from polly.auth import Polly
from polly import helpers
from polly import constants as const
from polly.omixatlas import OmixAtlas
from polly.jobs import jobs
from polly.workspaces import Workspaces
from polly.errors import paramException
from polly.tracking import Track
from polly import omixatlas_hlpr
from polly.constants import (
    COHORT_SUPPORTED_DATATYPES,
    COHORT_SUPPORTED_DATASOURCES,
    COHORT_LIST_COLS_TO_DROP,
    MA_SUPPORTED_REPO,
)

import pandas as pd
import plotly.express as px
import json
import numpy as np


class Analyze:
    """
    The Analyze class contains functions which can be used to identify cohorts in datasets, \
    perform differential expression and pathway analysis, and execute meta-analysis workflows.

    Args:
        token (str): Authentication token from polly

    Usage:
        from polly.analyze import Analyze

        analysis = Analyze(token)
    """

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.omixatlas_obj = OmixAtlas()
        self.job_obj = jobs()
        self.workspace_obj = Workspaces()
        self.elastic_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )

    @Track.track_decorator
    def identify_cohorts(self, repo_key: str, dataset_id: str) -> pd.DataFrame:
        """
        This function is used to get the cohorts that can be created from samples in a GEO dataset.
        Please note: Currently only Bulk RNASeq datasets from GEO source are supported.
        If results are generated for other datatypes or datasource, they may be inaccurate.
        If you want to use this functionality for any other data type and source,
        please reach out to polly.support@elucidata.io

        Args:
            repo_key (int/str): repo_id or repo_name in str or int format
            dataset_id (str): dataset_id of the GEO dataset. eg. "GSE132270_GPL11154_raw"

        Returns:
            Dataframe showing values of samples across factors/cohorts.
        """
        # param checks
        omixatlas_hlpr.parameter_check_for_dataset_id(dataset_id)
        omixatlas_hlpr.parameter_check_for_repo_id(repo_key)
        repo_key = omixatlas_hlpr.make_repo_id_string(repo_key)

        # TO DO: get_metadata() for dataset level in omixatlas.py and call that here
        # Get dataset level metadata and check if datatype is supported
        response_omixatlas = self.omixatlas_obj.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data", "")
        index_name = data.get("indexes", {}).get("files", "")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{self.elastic_url}/{index_name}/_search"
        query = helpers.elastic_query(index_name, dataset_id)
        metadata = helpers.get_metadata(self, elastic_url, query)
        source_info = metadata.get("_source", "")
        if (source_info["data_type"] not in COHORT_SUPPORTED_DATATYPES) or (
            source_info["dataset_source"] not in COHORT_SUPPORTED_DATASOURCES
        ):
            raise paramException(
                title="Param Error",
                detail="Only Bulk RNA Seq datasets that are from GEO are supported",
            )

        # Get sample level metadata
        col_metadata = self.omixatlas_obj.get_metadata(repo_key, dataset_id, "samples")
        # Index should be sample IDs which are available in geo_accession
        col_metadata = col_metadata.set_index("geo_accession")

        # Remove unnecessary columns
        col_metadata = col_metadata.drop(
            COHORT_LIST_COLS_TO_DROP, axis=1, errors="ignore"
        )

        # Iterate over columns
        for column in col_metadata.columns:
            # Check if column contains lists (curated columns do)
            if col_metadata[column].apply(lambda x: isinstance(x, list)).any():
                # Convert lists to strings
                col_metadata[column] = col_metadata[column].apply(
                    lambda x: "[" + ", ".join(x) + "]" if isinstance(x, list) else x
                )

        # Keeps only columns with more than 1 unique value
        col_metadata = col_metadata.loc[:, col_metadata.nunique() > 1]
        # Remove columns like sample id etc that has all unique values (only if n_samples > 2)
        if len(col_metadata) > 2:
            col_metadata = col_metadata.loc[
                :, col_metadata.nunique() != len(col_metadata)
            ]

        # Print a message if there are no unique columns
        if col_metadata.empty:
            print(
                """There is no variation across the sample(s) in the dataset,
             i.e. all metadata is the same. Hence, no cohorts can be created for this dataset.
             The output sunburst will be blank and the output dataframe will be empty.
             Please use `omixatlas.get_metadata("repo_id","dataset_id","table_name")`
             to view the sample-level metadata of a dataset."""
            )

        # # Initialize empty list for storing sets of columns with the same distribution
        # from scipy.stats import ks_2samp
        # column_sets = []

        # # Iterate over pairs of columns
        # for i, col1 in enumerate(df.columns):
        #     for col2 in df.columns[i+1:]:
        #         # Perform Kolmogorov-Smirnov test to compare the distributions of col1 and col2
        #         p_value = ks_2samp(df[col1], df[col2]).pvalue

        #         # If p-value > threshold (e.g., 0.05), consider the columns to have the same distribution
        #         if p_value > 0.05:
        #             column_sets.append((col1, col2))

        # # Print sets of columns with the same distribution
        # for column_set in column_sets:
        #     print(column_set)

        # Fix for 'None entries cannot have not-None children' error in sunburst
        col_metadata = col_metadata.fillna("notgiven")

        # Get list of columns to plot in sunburst, in ascending order of nunique() values
        df = col_metadata
        df = pd.DataFrame(df.nunique()).reset_index()
        df = df.sort_values(by=[0])
        lst = df["index"].to_list()
        print("Factors based on which cohorts can be created for this dataset:", lst)

        #         # if a column contains 'age', bucket into groups
        #         age_col_name = [col for col in col_metadata.columns if "age" in col]
        #         if age_col_name:
        #             # create age ranges and labels
        #             age_bins = [0, 20, 40, 60, 80, 100]
        #             age_labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]

        #             # bin age values into age ranges
        #             array_of_arrays = col_metadata.loc[:, age_col_name].values
        #             array_of_strings = [x[0] for x in array_of_arrays]
        #             col_metadata["age_range"] = pd.cut(
        #                 array_of_strings, bins=age_bins, labels=age_labels
        #             )

        #         # Create dataframe with distribution of factors and number of samples
        #         distribution_df = {"Factor": [], "Cohorts": [], "Number of Samples": []}
        #         if age_col_name:
        #             lst.remove(age_col_name[0])
        #             lst.append("age_range")
        #         for column_name in lst:
        #             unique_values = col_metadata[column_name].unique()
        #             for cohort in unique_values:
        #                 n_samples = len(col_metadata[col_metadata[column_name] == cohort])
        #                 distribution_df["Factor"].append(column_name)
        #                 distribution_df["Cohorts"].append(cohort)
        #                 distribution_df["Number of Samples"].append(n_samples)
        #         distribution_df = pd.DataFrame(distribution_df)
        #         if age_col_name:
        #             distribution_df["Factor"] = distribution_df["Factor"].replace(
        #                 "age_range", age_col_name[0]
        #             )
        #             lst = df["index"].to_list()
        #         print(distribution_df)

        # Plot sunburst
        fig = px.sunburst(col_metadata, path=lst)
        fig.show()
        return col_metadata[lst]

    def _get_control_perturbation_ids(
        self, col_metadata_df: pd.DataFrame, design_formula: dict
    ) -> list:
        """Given a design formula (control or perturbation), return the list of sample_ids
        from the sample level metadata (col_metadata) that are either control or perturbation,
        depending on design formula.

        Args:
            col_metadata_df (pd.DataFrame): The sample level metadata from identify_cohorts
            design_formula (dict): design_formula_control or design_formula_perturbation

        Returns:
            list: list of sample_ids that are either control or perturbation
        """
        sample_ids = []
        for column, value in design_formula.items():
            # Check if the user-provided column exists in the DataFrame
            if column not in col_metadata_df.columns:
                raise paramException(
                    title="Param Error",
                    detail=f"Column '{column}' does not exist in the DataFrame.",
                )
            # Check if the user-provided value exists in the given column
            if value not in col_metadata_df[column].values:
                raise paramException(
                    title="Param Error",
                    detail=f"Value '{value}' does not exist in column '{column}'",
                )
            # Boolean values list for samples in df if column == value
            sample_filter = col_metadata_df[column] == value
            # Add sublists to list with boolean values for each condition
            sample_ids.append([sample_filter])
        # Logical AND of all bool values in sublist
        sample_ids = np.all(sample_ids, axis=0)
        # Get sample IDs corresponding to logical AND indices
        sample_ids = col_metadata_df[sample_ids.T].sample_id

        return sample_ids

    def _parse_design_formula(
        self, repo_key: str, dataset_id: str, design_formulas: list
    ) -> pd.DataFrame:
        """Creates the cohort df for a dataset that is required for meta analysis.

        Args:
            repo_key (int/str): repo_id or repo_name in str or int format
            dataset_id (str): dataset_id of the GEO dataset. eg. "GSE132270_GPL11154_raw"
            design_formulas (list): design formula dicts for control and perturbation samples

        Returns:
            DataFrame: cohort df with three columns ['dataset_id', 'sample_id', 'kw_condition']\
            'kw_condition' has value 'control' or 'perturbation' based on the design formula.
        """
        col_metadata = self.omixatlas_obj.get_metadata(repo_key, dataset_id, "samples")

        # Convert curated columns to string so that input values can be compared directly
        for column in col_metadata.columns:
            # Check if column contains lists (curated columns do)
            if col_metadata[column].apply(lambda x: isinstance(x, list)).any():
                # Convert lists to strings
                col_metadata[column] = col_metadata[column].apply(
                    lambda x: "[" + ", ".join(x) + "]" if isinstance(x, list) else x
                )

        # Create design formula dataframe for this dataset ID
        cohort_df = pd.DataFrame(columns=["dataset_id", "sample_id", "kw_condition"])
        cohort_df["sample_id"] = col_metadata["geo_accession"]
        cohort_df["dataset_id"] = dataset_id

        # Extract control and perturbation sample IDs
        control_ids = self._get_control_perturbation_ids(
            col_metadata, design_formulas[0]
        )
        perturbation_ids = self._get_control_perturbation_ids(
            col_metadata, design_formulas[1]
        )

        cohort_df["kw_condition"] = "NA"
        cohort_df.loc[cohort_df["sample_id"].isin(control_ids), "kw_condition"] = (
            "control"
        )
        cohort_df.loc[cohort_df["sample_id"].isin(perturbation_ids), "kw_condition"] = (
            "perturbation"
        )

        return cohort_df

    @Track.track_decorator
    def run_meta_analysis(
        self,
        repo_key: str,
        workspace_id: int,
        analysis_name: str,
        design_formulas: dict,
        samples_to_remove=[],
    ):
        """
        Use this function to execute the Polly DIY Meta-Analysis Pipeline.
        Only the 'geo_transcriptomics_omixatlas' omixatlas is supported currently.

        Args:
            repo_key (int/str): repo_id or repo_name in str or int format
            workspace_id (int): the workspace in which the datasets and results should be stored
            analysis_name (str): name of your analysis, eg. "MA_BRCA_run1".\
            The reports, datasets, and results will be stored in a folder with this name.
            design_formulas (dict): key:value pair of atleast 2 dataset ids and a list of design formulas.\
            eg. dataset_id:[design formula control, design formula perturbation]
            samples_to_remove (list, optional): List of samples to omit, if any. Defaults to [].
        """
        dataset_ids = list(design_formulas.keys())

        # param checks
        omixatlas_hlpr.parameter_check_for_list_dataset_ids(dataset_ids)
        if len(dataset_ids) < 2:
            raise paramException(
                title="Param Error",
                detail="Design formula should contain atleast two datasets.",
            )
        omixatlas_hlpr.parameter_check_for_repo_id(repo_key)
        repo_key = omixatlas_hlpr.make_repo_id_string(repo_key)
        if repo_key not in MA_SUPPORTED_REPO:
            raise paramException(
                title="Param Error",
                detail="Only the 'geo_transcriptomics_omixatlas' omixatlas is supported currently.",
            )
        omixatlas_hlpr.str_params_check([analysis_name])

        # parse design formula to get cohort df
        cohort_dfs = []
        for dataset, design_formula in design_formulas.items():
            # Check if user has specified both control and perturbation in the list
            if len(design_formula) != 2:
                raise paramException(
                    title="Param Error",
                    detail=f"""Design formula for dataset_id '{dataset}' should have length
                    two with one dictionary for control and perturbation each.""",
                )
            # Check if user has specified both control and perturbation in the list
            if design_formula[0] == design_formula[1]:
                raise paramException(
                    title="Param Error",
                    detail=f"Control and perturbation dictionaries for dataset_id '{dataset}' cannot be the same.",
                )
            df = self._parse_design_formula(repo_key, dataset, design_formula)
            cohort_dfs.append(df)
        cohort_df = pd.concat(cohort_dfs)

        if samples_to_remove:
            # Check if samples_to_remove is not a list
            if not (samples_to_remove and isinstance(samples_to_remove, list)):
                raise paramException(
                    title="Param Error",
                    detail="'samples_to_remove' should be list of strings",
                )
            # Check if any samples in 'samples_to_remove' are not present in the DataFrame's index
            invalid_samples = [
                sample
                for sample in samples_to_remove
                if sample not in cohort_df["sample_id"].tolist()
            ]
            if invalid_samples:
                raise paramException(
                    title="Param Error",
                    detail=f"The following samples are not present in the DataFrame: {invalid_samples}",
                )
            # remove samples from above df if any
            cohort_df = cohort_df[~cohort_df["sample_id"].isin(samples_to_remove)]

        print("Cohort csv file created from the design formulae.")

        # save cohort df as csv to workspace
        cohort_csv_path = analysis_name + "_cohorts.csv"
        cohort_df.to_csv(cohort_csv_path, sep="\t")
        self.workspace_obj.upload_to_workspaces(
            workspace_id, cohort_csv_path, cohort_csv_path
        )

        # create job.json and submit polly job
        job_dict = {
            "image": "docker.polly.elucidata.io/elucidatarnd/polly-python",
            "tag": "meta_analysis_v1",
            "name": "Polly DIY pipeline: Meta Analysis",
            "machineType": "mi5xlarge",
            "env": {
                "POLLY_WORKSPACE_ID": workspace_id,
                "DATASET_IDS": dataset_ids,
                "SOURCE_OMIXATLAS": repo_key,
                "ANALYSIS_NAME": analysis_name,
                "COHORT_CSV_PATH": cohort_csv_path,
            },
        }

        job_json = json.dumps(job_dict, indent=4)
        job_path = analysis_name + "_job.json"
        with open(job_path, "w") as input:
            input.write(job_json)

        job_df = self.job_obj.submit_job(workspace_id, job_path)
        print(
            job_df,
            "Meta-Analysis Job submitted. You may further use job_status() and job_logs().",
        )
