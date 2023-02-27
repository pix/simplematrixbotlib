from __future__ import annotations

import asyncio
import json
import signal
import typing
from functools import partial
from typing import List

import aiohttp
import nio
from nio import SyncResponse, AsyncClient, UnknownEvent

import simplematrixbotlib as botlib

if typing.TYPE_CHECKING:
    from simplematrixbotlib import Config

_BOT_COUNT = 0


def run(config: Config, bots: List[Bot]):
    loop = asyncio.get_event_loop()
    bot_group = asyncio.gather(*[bot().run(config) for bot in bots], bot_count_check())
    loop.run_until_complete(bot_group)


async def bot_count_check():
    while True:
        if not _BOT_COUNT:
            stop()
        await asyncio.sleep(0)


def stop(*args):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit(0)


class Bot:
    """
    A class for the bot library user to interact with.
    
    ...

    Attributes
    ----------
    api : simplematrixbotlib.Api
        An instance of the simplematrixbotlib.Api class.
    
    """

    def __init__(self):
        """
        Initializes the simplematrixbotlib.Bot class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """

        # self.creds = creds
        # if config:
        #    self.config = config
        #    self._need_allow_homeserver_users = False
        # else:
        #    self._need_allow_homeserver_users = True
        #    self.config = botlib.Config()
        # self.api = botlib.Api(self.creds, self.config)
        # self.listener = botlib.Listener(self)
        # self.async_client: AsyncClient = None
        # self.callbacks: botlib.Callbacks = None

    async def main(self):
        self.creds.session_read_file()

        if not (await botlib.api.check_valid_homeserver(self.creds.homeserver
                                                        )):
            raise ValueError("Invalid Homeserver")

        await self.api.login()

        self.async_client = self.api.async_client

        resp = await self.async_client.sync(timeout=65536, full_state=False
                                            )  # Ignore prior messages

        if isinstance(resp, SyncResponse):
            print(
                f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})"
            )
            if self.config.encryption_enabled:
                key = self.async_client.olm.account.identity_keys['ed25519']
                print(
                    f"This bot's public fingerprint (\"Session key\") for one-sided verification is: "
                    f"{' '.join([key[i:i + 4] for i in range(0, len(key), 4)])}")

        self.creds.session_write_file()

        if self._need_allow_homeserver_users:
            # allow (only) users from our own homeserver by default
            _, hs = botlib.api.split_mxid(self.api.async_client.user_id)
            self.config.allowlist = set([f"(.+):{hs}"])

        self.callbacks = botlib.Callbacks(self.async_client, self)
        await self.callbacks.setup_callbacks()

        for action in self.listener._startup_registry:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    async def login(self, config):
        creds = config.to_dict()['creds']
        client = AsyncClient(homeserver=creds['homeserver'])
        client.access_token = creds['access_token']

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'{creds["homeserver"]}/_matrix/client/r0/account/whoami?access_token={creds["access_token"]}'
            ) as response:
                if isinstance(response, nio.responses.LoginError):
                    raise Exception(response)

                r = json.loads(
                    (await
                     response.text()).replace(":false,", ":\"false\","))

                creds['device_id'] = r['device_id']
                client.user_id = r['user_id']

                if not client.user_id == creds['user_id']:
                    raise ValueError(
                        f"Given Matrix user id \'{creds['user_id']}\' does not match the user id \'{client.user_id}\' associated with the access token. "
                        "This error prevents you from accidentally using the wrong account. "
                        "Resolve this by providing the correct user id with your credentials, "
                        # f"or reset your session by deleting {self.creds._session_stored_file}"
                        # f"{' and ' + self.config.store_path if self.config.encryption_enabled else ''}."
                    )

        if client.should_upload_keys:
            await client.keys_upload()

        print(
            f"Connected ({self.__class__.__name__}) to {creds['homeserver']} as {client.user_id} ({creds['device_id']})")

        return client

    async def startup(self, client: AsyncClient):
        print(f"Syncing {self.__class__.__name__}...")
        resp = await client.sync(timeout=65536, full_state=False)

        if isinstance(resp, SyncResponse):
            print(f"Sync Successful ({self.__class__.__name__}) !")

        for name, value in self.__class__.__dict__.items():
            if hasattr(value, '_on_start'):
                await value(self)

    async def stop(self, client: AsyncClient = None):
        if not client:
            client = self._client
        print(f"Stopping {self.__class__.__name__}...")

        for name, value in self.__class__.__dict__.items():
            if hasattr(value, '_on_end'):
                await value(self)

        global _BOT_COUNT
        _BOT_COUNT -= 1

        await client.close()

    async def setup_callbacks(self, config: Config, client: AsyncClient):
        for name, value in self.__class__.__dict__.items():
            if hasattr(value, '_on_event'):
                event = value._on_event
                value = partial(value, self)
                client.add_event_callback(value, event)

            if hasattr(value, '_on_reaction'):
                value = partial(value, self)
                def check_type(func):
                    async def wrapper(room, event_):
                        if event_.type == 'm.reaction':
                            await func(room, event_, event_.source['content']['m.relates_to']['key'])
                    return wrapper

                client.add_event_callback(check_type(value), UnknownEvent)

    async def run(self, config: Config):
        """
        Runs the bot.

        """
        global _BOT_COUNT
        _BOT_COUNT += 1
        signal.signal(signal.SIGINT, stop)

        client = await self.login(config=config)
        self._client = client

        await self.startup(client=client)
        await self.setup_callbacks(config=config, client=client)
        await client.sync_forever(timeout=3000, full_state=True)
