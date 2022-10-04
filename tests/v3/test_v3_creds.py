def test_creds_syntax():
    """
    a sanity test that Creds can correctly accept credentials. does not test
    whether Creds correctly handles credentials
    """
    import simplematrixbotlib as botlib
    
    botlib.Creds("https://home.server", "echo_bot").from_password("pass")
    botlib.Creds("https://home.server", "echo_bot").from_login_token("pass")
    botlib.Creds("https://home.server", "echo_bot").from_access_token("pass")

    assert True