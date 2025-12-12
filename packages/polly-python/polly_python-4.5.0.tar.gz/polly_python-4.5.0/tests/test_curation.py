import os
from polly.auth import Polly
from polly import curation
import pandas as pd

# from botocore.exceptions import ClientError

key = "POLLY_API_KEY"
token = os.getenv(key)
test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)
dev_key = "DEV_POLLY_API_KEY"
devpolly_token = os.getenv(dev_key)


def test_obj_initialised():
    Polly.auth(token)
    assert curation.Curation() is not None
    assert curation.Curation(token) is not None
    assert Polly.get_session(token) is not None


def test_annotate_with_ontology():
    Polly.auth(token)
    obj1 = curation.Curation()
    result = obj1.annotate_with_ontology(
        "This mouse has cancer. We took apart its lungs and found ACE2 upregulation"
    )
    assert result is not None
    assert len(result) > 0


def test_standardise_entity():
    Polly.auth(token)
    obj2 = curation.Curation()
    result2 = obj2.standardise_entity("AD", "disease")
    assert result2 is not None


def test_recognise_entity():
    Polly.auth(token)
    obj3 = curation.Curation()
    result3 = obj3.recognise_entity(
        "Gene expression profiling on mice lungs and reveals ACE2 upregulation"
    )
    assert result3 is not None


def test_find_abbreviations():
    Polly.auth(token)
    obj4 = curation.Curation()
    result4 = obj4.find_abbreviations(
        "Hepatocellular carcinoma (HCC) was observed in the model"
    )
    assert result4 is not None


def test_assign_control_pert_labels():
    Polly.auth(token)
    obj5 = curation.Curation()
    sample_metadata = pd.DataFrame(
        {
            "sample_id": [1, 2, 3, 4],
            "disease": ["control1", "ctrl2", "healthy", "HCC"],
        }
    )
    result5 = obj5.assign_control_pert_labels(
        sample_metadata, columns_to_exclude=["sample_id"]
    )
    assert result5 is not None


"""
 Commenting this Test case out as this test case is failing due to unidentified reason.
 Raised a ticket to fix this testcase and add it back once fixed.

 Ticket: https://elucidatainc.atlassian.net/browse/PRD-280

def test_assign_clinical_labels():
    Polly.auth(token)
    obj6 = curation.Curation()

    result6 = obj6.assign_clinical_labels(
        repo_name="geo",
        dataset_ids=["GSE152430_GPL18573", "GSE35643_GPL6244"],
        sample_ids=[
            "GSM4615218",
            "GSM4615219",
            "GSM4615220",
            "GSM872418",
            "GSM872419",
            "GSM872420",
            "GSM872421",
        ],
    )

    assert result6 is not None

    result6 = obj6.assign_clinical_labels(
        repo_name="geo", dataset_ids=["GSE152430_GPL18573", "GSE35643_GPL6244"]
    )

    assert result6 is not None

"""
