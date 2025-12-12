from util import assert_column_groups_response


def test_column_groups(
    set_insecure_transport,
    api_datasets,
    steels_dataset,
):
    dataset_id = steels_dataset
    # Create column groups for the dataset

    column_groups_batch_post_request = {
        "columnGroups": [
            {
                "name": "Element Inputs (incomplete)",
                "columns": [
                    "C (carbon)",
                    "Cr (chromium)",
                    "Mn (manganese)",
                    "Mo (molybdenum)",
                ],
            },
            {
                "name": "Strength Targets",
                "columns": [
                    "Yield strength (elastic limit)",
                    "Tensile strength",
                    "Fracture toughness",
                ],
            },
            {
                "name": "Temperature Targets",
                "columns": [
                    "Thermal conductivity",
                    "Specific heat capacity",
                    "Thermal expansion coefficient",
                ],
            },
        ]
    }

    column_group_ids = api_datasets.datasets_id_column_groups_batch_post(
        dataset_id,
        column_groups_batch_post_request,
    )

    column_groups_response = api_datasets.datasets_id_column_groups_get(
        dataset_id,
    )

    for column_group in column_groups_response:
        assert_column_groups_response(
            column_group,
            next(
                (
                    expected_group
                    for expected_group in column_groups_batch_post_request[
                        "columnGroups"
                    ]
                    if expected_group["name"] == column_group["name"]
                ),
                {},
            ),
        )

    # Modify and fetch column group for the dataset

    column_group_id = column_group_ids[0]
    api_datasets.datasets_id_column_groups_column_group_id_patch(
        dataset_id,
        column_group_id,
        column_group_patch_request={
            "name": "Element Inputs",
            "columns": [
                "C (carbon)",
                "Cr (chromium)",
                "Mn (manganese)",
                "Mo (molybdenum)",
                "Ni (nickel)",
                "Si (silicon)",
            ],
        },
    )

    modified_column_group = (
        api_datasets.datasets_id_column_groups_column_group_id_get(
            dataset_id,
            column_group_id,
        )
    )

    assert_column_groups_response(
        modified_column_group,
        {
            "name": "Element Inputs",
            "columns": [
                "C (carbon)",
                "Cr (chromium)",
                "Mn (manganese)",
                "Mo (molybdenum)",
                "Ni (nickel)",
                "Si (silicon)",
            ],
        },
    )
