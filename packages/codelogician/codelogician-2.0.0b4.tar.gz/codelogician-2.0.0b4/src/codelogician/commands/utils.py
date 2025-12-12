#
#   Imandra Inc.
#
#   utils.py
#

import httpx, sys
from rich import print as rprint
from logging import getLogger

log = getLogger(__name__)

class CLServerClient:
    """
    Wrapper around our server so we can 
    """
    def __init__ (self, addr:str=None):
        """ ctor """

        if addr is None: addr = "http://127.0.0.1:8000"
        self._server_addr = addr

    def check_conn (self) -> True:
        """
        Return True if the server is reachable, False otherwise 
        """
        try:
            res = httpx.get(f"{self._server_addr}/server/status")
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
        except Exception as e:
            return False

        return True

    def get(self, cmd : str, data : dict = None) -> httpx.Response:
        """
        Execute GET
        """

        if cmd.startswith('/'): cmd = cmd[1:]

        try:
            res = httpx.get(f"{self._server_addr}/{cmd}", params=data, timeout=60)
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}\n {res.json()['detail']}")
            sys.exit(0)
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
            sys.exit(0)
        except Exception as e:
            rprint(f"[bold][magenta]CodeLogician: [/bold][/magenta][bold][red]Failed to execute HTTP request: {e}. Exiting![/red][/bold]")
            sys.exit(0)

        return res

    def post (self, cmd : str, data: dict = None) -> httpx.Response:
        """
        Execute POST
        """

        if len(cmd) > 1 and cmd.startswith('/'): cmd = cmd[1:]

        try:
            res = httpx.post(f"{self._server_addr}/{cmd}", data=data, timeout=60)
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}\n {res.json()['detail']}")
            sys.exit(0)
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
            sys.exit(0)
        except Exception as e:
            rprint(f"[bold][magenta]CodeLogician: [/bold][/magenta][bold][red]Failed to execute HTTP request: {e}. Exiting.[/red][/bold]")
            sys.exit(0)

        return res
