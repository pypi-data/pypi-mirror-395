def test_connect(
    set_insecure_transport,
    api_default,
):
    api_response = api_default.version_get()

    assert "alchemite_version" in api_response
    assert "api_application_version" in api_response
    assert "api_definition_version" in api_response
