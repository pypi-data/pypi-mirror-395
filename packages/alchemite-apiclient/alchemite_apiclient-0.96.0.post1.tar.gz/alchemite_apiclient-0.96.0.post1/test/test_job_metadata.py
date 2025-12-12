import json
import os

import alchemite_apiclient as client
from alchemite_apiclient.extensions import await_job


def test_jobs_metadata_put_suggest_additional(
    set_insecure_transport, api_models, api_jobs, steels_model, example_dir
):
    model_id = steels_model
    suggest_args = os.path.join(example_dir, "suggest_additional_args_steel.json")

    # Get suggest additional input arguments
    with open(suggest_args, encoding="UTF-8") as f:
        suggest_additional_args = json.load(f)

    # Send suggest_additional request
    suggest_additional_job_id = api_models.models_id_suggest_additional_post(
        model_id, **suggest_additional_args
    )

    # Wait until the suggest_additional job has finished
    def get_suggest_additional_job_metadata():
        return api_models.models_id_suggest_additional_job_id_get(
            model_id, job_id=suggest_additional_job_id
        )

    suggest_additional_response = await_job(get_suggest_additional_job_metadata)
    assert "status" in suggest_additional_response
    assert suggest_additional_response["status"] == "done"

    # Create job query to search for suggest-additional jobs for this model
    job_query = client.JobQuery(
        types=["suggest-additional"],
        filters=client.JobsMetadataFilters(job_ids=[suggest_additional_job_id]),
    )

    # Call jobs_metadata_put to get job metadata
    response = api_jobs.jobs_metadata_put(job_query=job_query)

    # Verify the response structure
    assert "total" in response
    assert "result" in response
    assert response["total"] >= 1  # At least our job should be found

    # Verify our job is in the results
    job_found = False
    for job_data in response["result"]:
        if job_data.get("id") == suggest_additional_job_id:
            job_found = True
            # Verify job has expected properties
            assert job_data.get("type") == "suggest-additional"
            assert job_data.get("status") == "done"
            assert job_data.get("modelId") == model_id
            break

    assert job_found, (
        f"Job {suggest_additional_job_id} was not found in jobs_metadata_put results"
    )
