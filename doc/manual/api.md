The Api class is a class that is used to simplify interaction with the matrix-nio library that Simple-Matrix-Bot-Lib is built upon. The source is located at simplematrixbotlib/api.py

### Accessing an Api instance
An instance of the Api class is automatically created when an instance of the Bot class is created. An example is shown in the following python code.
```python
bot = botlib.Bot(creds)
bot.api #Instance of the Api class
```

### Using the send_text_message method
The send_text_message method of the Api class can be used to send text messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_message = "Hello World"
    if match.is_not_from_this_bot():
        await bot.api.send_text_message(
            room_id=room.room_id, 
            message=example_message,
            msgtype="m.notice")
```
The first two arguments are required. The room_id argument is the id of the destination room. The message argument is the string that is to be sent as a message. The msgtype argument can be "m.text" (default) or "m.notice".

### Using the `send_reaction` method

The `send_reaction` method of the Api class can be used to send reactions to messages in Matrix rooms.
An example is shown in the following python code.

```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_reaction = "✅"
    if match.is_not_from_this_bot():
        await bot.api.send_reaction(
            room_id=room.room_id,
            event=message,
            key=example_reaction)
```

All arguments are required.
The `room_id` argument is the id of the destination room.
The `event` argument is the event object that will get annotated with your reaction.
The `key` argument is the content of the reaction. This is usually an emoji, but may technically be any text.

### Using the send_image_message method
The send_image_message method of the Api class can be used to send image messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_image="./img/example.png"
    if match.is_not_from_this_bot():
        await bot.api.send_image_message(
            room_id=room.room_id, 
            image_filepath=example_image)
```
Both arguments are required. The room_id argument is the id of the destination room. The image_filepath argument is a string that is the path to the image file that is to be sent as a message.

### Using the send_video_message method
The send_video_message method of the Api class can be used to send video messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_video="./videos/example.mp4"
    if match.is_not_from_this_bot():
        await bot.api.send_video_message(
            room_id=room.room_id, 
            video_filepath=example_video)
```
Both arguments are required. The room_id argument is the id of the destination room. The video_filepath argument is a string that is the path to the video file that is to be sent as a message.


### Using the send_markdown_message method
The send_markdown_message method of the Api class can be used to send markdown messages in Matrix rooms. An example is shown in the following python code.
```python
async def example(room, message):
    match = botlib.MessageMatch(room, message, bot)
    example_markdown = "# Hello World from [simplematrixbotlib](https://github.com/KrazyKirby99999/simple-matrix-bot-lib)!"
    if match.is_not_from_this_bot():
        await bot.api.send_markdown_message(
            room_id=room.room_id, 
            message=example_markdown,
            msgtype="m.notice")
```
The first two arguments are required. The room_id argument is the id of the destination room. The message argument is the string with markdown syntax that is to be sent as a message. The msgtype argument can be "m.text" (default) or "m.notice".
