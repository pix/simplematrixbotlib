import simplematrixbotlib as botlib
from nio import Event

def test_listener():
    class BotPlaceholder:
        def __init__(self):
            methods = [getattr(self, func) for func in dir(self) if callable(getattr(self, func))]
            self._event_registry = [func for func in methods if hasattr(func, '_on_event')]
            self._reaction_registry = [func for func in methods if hasattr(func, '_on_reaction')]
            self._start_registry = [func for func in methods if hasattr(func, '_on_start')]
            self._end_registry = [func for func in methods if hasattr(func, '_on_end')]
        
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

        @botlib.on_start
        async def start_handler():
            pass
        assert True

        @botlib.on_end
        async def end_handler():
            pass
        assert True

    bot = BotPlaceholder()
    assert bot.message_handler in bot._event_registry
    assert bot.reaction_handler in bot._reaction_registry
    assert bot.event_handler in bot._event_registry
    assert bot.start_handler in bot._start_registry
    assert bot.end_handler in bot._end_registry
