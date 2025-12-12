from util import assert_sensitivity_response


def test_sensitivity(
    set_insecure_transport,
    api_models,
    steels_model,
):
    model_id = steels_model
    column_headers = api_models.models_id_get(model_id)[
        "training_column_headers"
    ]

    # build the sensitivity request (we use mean of each col as an example)
    sensitivity_request = {
        "dataPoint": [
            {"name": "C (carbon)", "value": 0.57},
            {"name": "Cr (chromium)", "value": 0.43},
            {"name": "Mn (manganese)", "value": 0.63},
            {"name": "Mo (molybdenum)", "value": 0.08},
            {"name": "Ni (nickel)", "value": 0.45},
            {"name": "Si (silicon)", "value": 0.11},
            {"name": "Young's modulus", "value": 208.57},
            {"name": "Yield strength (elastic limit)", "value": 368.61},
            {"name": "Tensile strength", "value": 494.52},
            {"name": "Elongation", "value": 28.9},
            {"name": "Fracture toughness", "value": 75.42},
            {"name": "Thermal conductivity", "value": 48.86},
            {"name": "Specific heat capacity", "value": 480.72},
            {"name": "Thermal expansion coefficient", "value": 11.89},
            {"name": "Electrical resistivity", "value": 19.21},
        ]
    }

    # Get the sensitivity matrix of each column based on our input data point
    sensitivity_response = api_models.models_id_sensitivity_put(
        model_id,
        sensitivity_request=sensitivity_request,
        _preload_content=False,
    )
    assert_sensitivity_response(sensitivity_response, set(column_headers))
