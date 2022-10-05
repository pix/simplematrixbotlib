def test_parser():
    import simplematrixbotlib as botlib

    message = "echo foo something bar something spam eggs"
    rule = "echo <arg1> something <arg2> something <*>"
    parsed = botlib.parse(input_=message, rule=rule)
    assert parsed == {'arg1':'foo', 'arg2':'bar'}

    message = "something echo foo something bar something spam eggs"
    rule = "echo <arg1> something <arg2> something <*>"
    parsed = botlib.parse(input_=message, rule=rule)
    assert parsed == {}

    message = "echo foo something bar something spam eggs"
    rule = "echo <arg1> something <arg2> something <arg3 *>"
    parsed = botlib.parse(input_=message, rule=rule)
    assert parsed == {'arg1':'foo', 'arg2':'bar', 'arg3':'spam eggs'}

    message = "anything"
    rule = "<arg *> <*>"
    try:
        parsed = botlib.parse(input_=message, rule=rule)
        assert False
    except botlib.ParseError:
        assert True
