import asyncio, json
import aiohttp
from nio import AsyncClient, LoginResponse

class CredsError(Exception): pass

class Creds:
    def __init__(self, homeserver, user_id):
        self._dict = {'homeserver': homeserver, 'user_id':user_id}
    
    async def _get_access_token(self, password=None, login_token=None):
        client = AsyncClient(self._dict['homeserver'], self._dict['user_id'])
        device_name = 'simplematrixbotlib'
        if password:
            resp = (await client.login(password=password, device_name=device_name))
        elif login_token:
            resp = (await client.login(token=login_token, device_name=device_name))
        else:
            raise CredsError(f"Invalid Credentials: Requires password or login_token (SSO token)")
        if not isinstance(resp, LoginResponse):
            raise CredsError(f"Failed to successfully obtain access_token: {LoginResponse}")
        await client.close()
        return resp.access_token
    
    def from_password(self, password):
        self._dict['access_token'] = asyncio.get_event_loop().run_until_complete(
            self._get_access_token(password=password))
        return self._dict
    
    def from_login_token(self, login_token):
        self._dict['access_token'] = asyncio.get_event_loop().run_until_complete(
            self._get_access_token(login_token=login_token))
        return self._dict

    def from_access_token(self, access_token):
        async def confirm_access_token():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self._dict['homeserver']}/_matrix/client/r0/account/whoami?access_token={access_token}"
                    ) as resp:
                        if json.loads((await resp.text()).replace(":false,", ":\"false\",")
                        )['user_id'] == self._dict['user_id']:
                            self._dict['access_token'] = access_token
                            return self._dict
                        else:
                            raise CredsError(f"Failed to confirm access_token: {resp=}")
        return asyncio.get_event_loop().run_until_complete(confirm_access_token())             
