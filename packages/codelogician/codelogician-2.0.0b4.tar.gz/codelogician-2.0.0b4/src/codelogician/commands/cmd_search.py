#
#   Imandra Inc.
#
#   cmd_search.py
#


from rich import print as rprint
from logging import getLogger
log = getLogger(__name__)

from .utils import CLServerClient

def run_search (
    query : str,
    addr : str 
    ):
    """
    Run search command
    """

    cl_client = CLServerClient(addr)

    response = cl_client.get("search", {'query': query})

    if len(response.json()) == 0:
        print ("No results found!")
    else:
        for res in response.json():
            rprint (res)
