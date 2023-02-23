from __future__ import annotations
import asyncio
import json
import sys
import typing
from typing import Optional, List

import aiohttp
import nio

import simplematrixbotlib as botlib
from nio import SyncResponse, AsyncClient

if typing.TYPE_CHECKING:
    from simplematrixbotlib import Config


def run(config: Config, bots: List[Bot]):
    loop = asyncio.get_event_loop()
    bot_group = asyncio.gather(*[bot().run(config) for bot in bots])
    loop.run_until_complete(bot_group)

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

        #self.creds = creds
        #if config:
        #    self.config = config
        #    self._need_allow_homeserver_users = False
        #else:
        #    self._need_allow_homeserver_users = True
        #    self.config = botlib.Config()
        #self.api = botlib.Api(self.creds, self.config)
        #self.listener = botlib.Listener(self)
        #self.async_client: AsyncClient = None
        #self.callbacks: botlib.Callbacks = None

    async def main(self):
        self.creds.session_read_file()

        if not (await botlib.api.check_valid_homeserver(self.creds.homeserver
                                                        )):
            raise ValueError("Invalid Homeserver")

        await self.api.login()

        self.async_client = self.api.async_client

        resp = await self.async_client.sync(timeout=65536, full_state=False
                                            )  #Ignore prior messages

        if isinstance(resp, SyncResponse):
            print(
                f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})"
            )
            if self.config.encryption_enabled:
                key = self.async_client.olm.account.identity_keys['ed25519']
                print(
                    f"This bot's public fingerprint (\"Session key\") for one-sided verification is: "
                    f"{' '.join([key[i:i+4] for i in range(0, len(key), 4)])}")

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
                        #f"or reset your session by deleting {self.creds._session_stored_file}"
                        #f"{' and ' + self.config.store_path if self.config.encryption_enabled else ''}."
                    )

        if client.should_upload_keys:
            await client.keys_upload()

        print(f"Connected ({self.__class__.__name__}) to {creds['homeserver']} as {client.user_id} ({creds['device_id']})")


    async def run(self, config: Config):
        """
        Runs the bot.

        """
        await self.login(config=config)
