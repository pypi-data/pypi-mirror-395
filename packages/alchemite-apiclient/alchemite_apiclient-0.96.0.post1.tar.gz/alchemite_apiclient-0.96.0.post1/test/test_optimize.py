import json
import os

from alchemite_apiclient.extensions import await_job


def test_optimize(
    set_insecure_transport, api_models, steels_model, example_dir
):
    model_id = steels_model
    optimize_args = os.path.join(example_dir, "optimize_args_steel.json")

    # Get optimize input arguments
    with open(optimize_args, encoding="UTF-8") as f:
        optimize_args = json.load(f)

    # Send optimize request
    optimize_job_id = api_models.models_id_optimize_post(
        model_id, **optimize_args
    )

    # Wait until the optimize job has finished
    def get_optimize_job_metadata():
        return api_models.models_id_optimize_job_id_get(
            model_id, job_id=optimize_job_id
        )

    optimize_response = await_job(get_optimize_job_metadata)
    assert "status" in optimize_response
    assert optimize_response["status"] == "done"
