def test_config():
    import simplematrixbotlib as botlib

    config = botlib.Config(defaults={'creds':'foo'}).from_dict({
           'prefix':'!'
         })
    
    assert config.to_dict() == {'creds':'foo', 'prefix':'!'}

    config = botlib.Config(defaults={}).from_dict({
           'prefix':'!'
         })
    
    assert config.to_dict() == {'prefix':'!'}

    config = botlib.Config(defaults={'creds':'foo'}).from_dict({
           'creds':'bar',
           'prefix':'!'
         })
    
    assert config.to_dict() == {'creds':'bar', 'prefix':'!'}

    config = botlib.Config(defaults={}).from_dict({
         })
    
    assert config.to_dict() == {}
