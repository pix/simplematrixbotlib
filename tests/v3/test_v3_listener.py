import simplematrixbotlib as botlib
from nio import Event

def test_listener():
    @botlib.on_message
    async def message_handler(room, message):
        pass
    assert True

    @botlib.on_reaction
    async def reaction_handler(room, event, reaction):
        pass
    assert True

    @botlib.on_event(Event)
    async def event_handler(room, event):
        pass
    assert True

    @botlib.on_startup
    async def startup_handler():
        pass
    assert True

    @botlib.on_end
    async def end_handler():
        pass
    assert True