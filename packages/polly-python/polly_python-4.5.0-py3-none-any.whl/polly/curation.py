import json
from collections import namedtuple

from typing import Dict, Optional, List

import pandas as pd
from functools import lru_cache
from polly.errors import (
    InvalidSchemaJsonException,
    InvalidSyntaxForRequestException,
    EmptyPayloadException,
    RequestException,
    UnauthorizedException,
    extract_json_api_error,
)
from polly.auth import Polly

from polly import helpers, constants as const, application_error_info as app_err_info
from polly.help import example
import polly.http_response_codes as http_codes

from polly.constants import SUPPORTED_ENTITY_TYPES

from polly.tracking import Track


class Curation:
    """
    The Curation class contains wrapper functions around the models used for
    semantic annotations of string/text.

    Args:
        token (str): token copy from polly.

    Usage:
            from polly.curation import Curation

            curationObj = Curation(token)
    """

    Tag = namedtuple("Tag", ["name", "ontology_id", "entity_type"])
    example = classmethod(example)

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
    ) -> None:
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"
        self.elastic_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        self.inference_url = f"https://api.discover.{self.session.env}.elucidata.io/curations/inferences/"

    def _handle_errors(self, response):
        detail = response.get("errors")[0].get("detail", [])
        title = response.get("errors")[0].get("title", [])
        return title, detail

    def _handle_perform_inference_api_error(self, response):
        if response.status_code == http_codes.UNAUTHORIZED:
            raise UnauthorizedException("User is unauthorized to access this")
        elif response.status_code == http_codes.BAD_REQUEST:
            title, details = extract_json_api_error(response)
            if title == app_err_info.EMPTY_PAYLOAD_CODE:
                raise EmptyPayloadException()
            elif app_err_info.INVALID_MODEL_NAME_TITLE in title:
                raise InvalidSyntaxForRequestException()
        elif response.status_code == http_codes.INTERNAL_SERVER_ERROR:
            raise InvalidSchemaJsonException()
        elif response.status_code == http_codes.GATEWAY_TIMEOUT:
            error_detail = response.json().get("message", "Request timed out")
            raise Exception(error_detail)
        else:
            title, details = extract_json_api_error(response)
            raise Exception("Exception Occurred :" + str(details))

    def _perform_inference(
        self,
        model_name: str,
        input_data: dict,
    ) -> dict:
        """
        This is a wrapper around model inference APIs
        It serializes input_data, calls the API for the given model_name
        and returns deserialized output.

        Args:
            model_name (str): one of 'normalizer', 'biobert' and 'control-perturbation'
            input_data (dict): model input

        Returns:
            dict
        """
        url = self.inference_url + model_name

        payload = {}
        payload = json.dumps({"data": {"attributes": input_data, "type": "curation"}})
        response = self.session.post(url, data=payload)
        try:
            if response.status_code != 201:
                self._handle_perform_inference_api_error(response)
        except Exception as err:
            raise err
        try:
            response = response.json()
        except json.JSONDecodeError as e:
            raise e
        if "data" in response:
            return response.get("data")
        return response

    @Track.track_decorator
    @lru_cache(maxsize=None)
    def standardise_entity(
        self,
        mention: str,
        entity_type: str,
        context: Optional[str] = None,
        threshold: Optional[float] = None,
    ) -> dict:
        """
        Map a given mention (keyword) to an ontology term.
        Given a text and entity type, users can get the Polly compatible ontology for the text such as the MESH ontology.

        Args:
            mention (str): mention of an entity e.g. "Cadiac arrythmia"
            entity_type (str): Should be one of \
            ['disease', 'drug', 'tissue', 'cell_type', 'cell_line', 'species', 'gene']
            context (str): The text where the mention occurs. \
            This is used to resolve abbreviations.
            Threshold: (float, optional) = Optional Parameter. \
            All entities with a score < threshold are filtered out from the output. \
            Its best not to specify a threshold and just use the default value instead.

        Returns:
            dict : Dictionary containing keys and values of the entity type, \
            ontology (such as NCBI, MeSH), ontology ID (such as the MeSH ID), the score (confidence score), and synonyms if any

        Raises:
            requestException : Invalid Request
        """
        data = {
            "mention": {
                "keyword": mention,
                "entity_type": entity_type,
                "threshold": threshold,
            }
        }

        if context:
            data["context"] = context
        output = self._perform_inference("normalizer", data)
        if output.get("errors", []):
            title, detail = self._handle_errors(output)
            raise RequestException(title, detail)

        if "term" not in output:
            return {
                "ontology": "CUI-less",
                "ontology_id": None,
                "name": None,
                "entity_type": entity_type,
            }

        return output.get("term", [])

    @Track.track_decorator
    def recognise_entity(
        self,
        text: str,
        threshold: Optional[float] = None,
        normalize_output: bool = False,
    ):
        """
        Run an NER model on the given text. The returned value is a list of entities along with span info.
        Users can simply recognise entities in a given text without any ontology standardisation
         (unlike the annotate_with_ontology function which normalises as well).

        Args:
            text (str): input text
            threshold (float, optional): Optional Parameter. \
            All entities with a score < threshold are filtered out from the output. \
            Its best not to specify a threshold and just use the default value instead.
            normalize_output (bool): whether to normalize the keywords

        Returns:
            entities (List[dict]): List of spans containing the keyword, start/end index of the keyword and the entity type

        Raises:
            requestException: Invalid Request
        """
        # TODO: If text is too long, break it up into chunks small enough for biobert

        payload = {"text": text}
        if threshold:
            payload["threshold"] = threshold
        response = self._perform_inference("biobert", payload)
        if response.get("errors", []):
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            entities = response.get("entities", [])
        except KeyError as e:
            raise e

        # TODO: fetch this list from the server maybe?

        if normalize_output:
            for entity in entities:
                # don't call `normalize` for unsupported entity types
                if entity.get("entity_type") not in SUPPORTED_ENTITY_TYPES:
                    entity["name"] = None
                    continue
                norm = self.standardise_entity(
                    entity["keyword"], entity["entity_type"], text
                )
                if norm.get("ontology", []) == "CUI-less":
                    entity["name"] = None
                else:
                    entity["ontology_id"] = norm["ontology"] + ":" + norm["ontology_id"]
                    entity["name"] = norm["name"]
        return entities

    @Track.track_decorator
    def annotate_with_ontology(
        self,
        text: str,
    ) -> List[Tag]:
        """
        Tag a given piece of text. A "tag" is just an ontology term. Annotates with Polly supported ontologies.
        This function calls recognise_entity followed by normalize.
        Given a text, users can identify and tag entities in a text.
        Each entity/tag recognised in the text contains the name(word in the text identified), entity_type and the ontology_id.

        Args:
            text (str): Input text

        Returns:
            set of unique tags
        """

        entities = self.recognise_entity(text, normalize_output=True)
        res = {
            self.Tag(
                e.get("name", []), e.get("ontology_id", []), e.get("entity_type", [])
            )
            for e in entities
            if e.get("name")
        }
        return list(res)

    @Track.track_decorator
    def find_abbreviations(self, text: str) -> Dict[str, str]:
        """
        To run abbreviation detection separately.
        Internally calls a normaliser.

        Args:
            text (str): The string to detect abbreviations in.

        Returns:
            Dictionary with abbreviation as key and full form as value

        Raises:
            requestException: Invalid Request
        """
        data = {
            "mention": {"keyword": "dummykeyword", "entity_type": "gene"},
            "context": text,
        }

        response = self._perform_inference("normalizer", data)
        if "errors" in response:
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            output = response.get("abbreviations", [])
        except KeyError as e:
            raise e

        return output

    def assign_control_pert_labels(
        self, sample_metadata, columns_to_exclude=None
    ) -> pd.DataFrame:
        """Returns the sample metadata dataframe with 2 additional columns.
            is_control - whether the sample is a control sample
            control_prob - the probability that the sample is control

        Args:
            sample_metadata (DataFrame): Metadata table
            columns_to_exclude (Set[str]): Any columns which don't play any role in determining the label, e.g. sample id

        Returns:
            DataFrame: Input data frame with 2 additional columns

        Raises:
            requestException: Invalid Request

        """
        sample_metadata = sample_metadata.copy()

        if columns_to_exclude is None:
            columns_to_exclude = []

        cols = sample_metadata.columns.difference(columns_to_exclude)

        samples = sample_metadata[cols].to_dict("records")
        request_body = {"samples": samples}
        response = self._perform_inference("control-pertubation", request_body)
        response = {
            k: v for k, v in response.items() if k != "version" and k != "testing"
        }
        if "errors" in response:
            title, detail = self._handle_errors(response)
            raise RequestException(title, detail)
        try:
            output = pd.DataFrame(response)
        except KeyError as e:
            raise e
        sample_metadata["is_control"] = output["is_control"].values
        sample_metadata["control_prob"] = output["control_prob"].values
        return sample_metadata
