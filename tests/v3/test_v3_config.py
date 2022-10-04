def test_config_dict():
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

def test_config_env_vars():
    import os
    import simplematrixbotlib as botlib

    os.environ["BOT_CREDS"] = "bar"
    os.environ["BOT_PREFIX"] = "!"

    config = botlib.Config(defaults={'creds':'foo'}).from_env({
           'prefix':'BOT_PREFIX'
         })
    assert config.to_dict() == {'creds':'foo', 'prefix':'!'}

    config = botlib.Config(defaults={}).from_env({
           'prefix':'BOT_PREFIX'
         })
    assert config.to_dict() == {'prefix':'!'}

    config = botlib.Config(defaults={'creds':'foo'}).from_env({
           'creds':'BOT_CREDS',
           'prefix':'BOT_PREFIX'
         })
    assert config.to_dict() == {'creds':'bar', 'prefix':'!'}

    config = botlib.Config(defaults={}).from_env({
         })
    assert config.to_dict() == {}