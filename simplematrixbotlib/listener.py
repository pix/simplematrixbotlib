from nio import RoomMessageText, UnknownEvent

def on_message(handler): 
    return on_event(RoomMessageText)(handler)

def on_reaction(handler):
    handler._on_reaction = True
    return handler

def on_event(event):
    def wrapped(handler):
        handler._on_event = event
        return handler
    return wrapped

def on_start(handler):
    handler._on_start = True
    return handler

def on_end(handler):
    handler._on_end = True
    return handler

class LegacyListener:

    def __init__(self, bot):
        self._bot = bot
        self._registry = []
        self._startup_registry = []

    def on_custom_event(self, event):

        def wrapper(func):
            if [func, event] in self._registry:
                func()
            else:
                self._registry.append([func, event])

        return wrapper

    def on_message_event(self, func):
        if [func, RoomMessageText] in self._registry:
            func()
        else:
            self._registry.append([func, RoomMessageText])

    def on_reaction_event(self, func):

        async def new_func(room, event):
            if event.type == "m.reaction":
                await func(room, event,
                           event.source['content']['m.relates_to']['key'])

        self._registry.append([new_func, UnknownEvent])

    def on_startup(self, func):
        if func in self._startup_registry:
            func()
        else:
            self._startup_registry.append(func)
