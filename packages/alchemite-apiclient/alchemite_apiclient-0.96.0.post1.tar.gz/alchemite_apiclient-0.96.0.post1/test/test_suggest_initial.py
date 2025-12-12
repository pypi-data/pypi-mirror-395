import json
import os

from alchemite_apiclient.extensions import await_job


def test_suggest_initial(set_insecure_transport, api_default, example_dir):
    suggest_initial_args_path = os.path.join(example_dir, "suggest_initial_args.json")

    # Make a suggest initial request
    with open(suggest_initial_args_path, encoding="UTF-8") as f:
        suggest_initial_args = json.load(f)

    # Send suggest_initial request
    suggest_initial_job_id = api_default.suggest_initial_post(**suggest_initial_args)

    # Wait until the suggest_initial job has finished
    def get_suggest_initial_job_metadata():
        return api_default.suggest_initial_job_id_get(suggest_initial_job_id)

    suggest_initial_response = await_job(get_suggest_initial_job_metadata)
    assert "status" in suggest_initial_response
    assert suggest_initial_response["status"] == "done"

    # Delete suggest_initial job
    delete_response = api_default.suggest_initial_job_id_delete(suggest_initial_job_id)
    assert delete_response == ""
