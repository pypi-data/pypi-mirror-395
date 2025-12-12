import csv
import json
from io import StringIO

import alchemite_apiclient as client
from alchemite_apiclient.extensions import (
    Configuration,
    await_job,
    await_trained,
)

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_projects = client.ProjectsApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Provide path to the dataset to train a model from, and suggest initial arguments
dataset_file = "steels.csv"
suggest_initial_args_path = "suggest_initial_args.json"

# Define names for the project, dataset, model and job (they do not have to be unique)
project_name = "Example Project"
dataset_name = "steels"
model_name = "steels"
suggest_initial_job_name = "new job"
#######################

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(
    f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})"
)
print("------------------------------------------")

# Find or create a project called "Example Project" to house the model and suggest-initial job
existing_projects = api_projects.projects_get()
project_id = None
for project in existing_projects:
    if project.name == project_name:
        project_id = project.id
        print("Found existing project with id:", project_id)
        break
if project_id is None:
    # Couldn't find existing project, so create a new one with POST /projects
    project_id = api_projects.projects_post({"name": project_name})
    print("No existing project found. Created new project with id:", project_id)

# Get suggest initial input arguments
with open(suggest_initial_args_path, encoding="UTF-8") as f:
    suggest_initial_args = json.load(f)
    suggest_initial_args["suggest_initial_request"]["project_id"] = project_id
    suggest_initial_args["suggest_initial_request"]["name"] = suggest_initial_job_name


# Send suggest_initial request
suggest_initial_job_id = api_default.suggest_initial_post(**suggest_initial_args)
print("suggest_initial job ID:", suggest_initial_job_id)


# Wait until the suggest_initial job has finished
def get_suggest_initial_job_metadata():
    return api_default.suggest_initial_job_id_get(suggest_initial_job_id)


suggest_initial_job = await_job(get_suggest_initial_job_metadata)

# Upload a dataset with POST /datasets
with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]

row_count = len(rows) - 1
column_headers = rows[0][1:]
descriptor_columns = [0] * len(column_headers)
dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": descriptor_columns,
    "data": data,
}
dataset_id = api_datasets.datasets_post(dataset=dataset)
print("Uploaded dataset:", dataset_id)

# Create and train a model as part of the project
model = {
    "name": model_name,
    "training_method": "alchemite",
    "training_dataset_id": dataset_id,
    "project_id": project_id,
}
model_id = api_models.models_post(model=model)
print("Created model record ID:", model_id)
response = api_models.models_id_train_put(model_id, train_request={})
await_trained(lambda: api_models.models_id_get(model_id))


# Retrieve all models in a project
models = api_models.models_metadata_put(
    model_query={"filters": {"project_id": project_id}},
)
print(f"Models for Project '{project_name}'")
for model in models["result"]:
    print(f"{model['id']}: {model['name']}")
print()
# Show all suggest-initial jobs in a project
jobs = api_default.suggest_initial_get()
print(f"Suggest-initial jobs for Project '{project_name}'")
for job in jobs:
    if job.get("project_id", None) == project_id:
        print(f"{job['id']}: {job.get('name', '(unnamed)')}")

# Delete model and dataset
# api_models.models_id_delete(model_id)
# api_datasets.datasets_id_delete(dataset_id)
