from util import assert_output_tolerance_response


def test_output_tolerance(
    set_insecure_transport,
    api_models,
    steels_model,
):
    model_id = steels_model
    num_samples = 5

    output_tolerance_request = {
        "sampleDefinition": {
            "Mo (molybdenum)": {"type": "continuous", "range": [0.2, 0.44]},
            "Thermal expansion coefficient": {
                "type": "continuous",
                "range": [0, 3.76],
            },
            "Electrical resistivity": {
                "type": "continuous",
                "range": [4, 4.42],
            },
        },
        "setInputs": {
            "Cr (chromium)": 0.43,
            "Mn (manganese)": 0.63,
            "Ni (nickel)": 0.45,
            "Si (silicon)": 0.11,
            "Specific heat capacity": 480.72,
        },
        "numSamples": num_samples,
    }

    output_tolerance_response = api_models.models_id_output_tolerance_put(
        model_id,
        output_tolerance_request=output_tolerance_request,
    )
    assert_output_tolerance_response(
        output_tolerance_response,
        num_samples,
        len(output_tolerance_request["setInputs"]),
    )

    # Make univariate output tolerance request
    output_tolerance_univariate_response = (
        api_models.models_id_output_tolerance_univariate_put(
            model_id, output_tolerance_request=output_tolerance_request
        )
    )

    for univariate_column in output_tolerance_request["sampleDefinition"]:
        univariate_sample = output_tolerance_univariate_response[
            univariate_column
        ]
        assert_output_tolerance_response(
            univariate_sample,
            num_samples,
            len(output_tolerance_request["setInputs"])
            + len(output_tolerance_request["sampleDefinition"])
            - 1,
        )
