#
# Imandra Inc.
#
# endpts_search.py
# 

import logging
from fastapi import HTTPException

from .cl_server import CLServer
from .search import SearchResult
from ..tools.cl_caller import calc_search_embeddings

log = logging.getLogger(__name__)

def register_search_endpoints(app : CLServer):
    """
    Attach search functions to the server.
    """

    @app.get("/search", operation_id="get_server_status")
    async def search (
        query : str
        ) -> list[SearchResult]:
        """ 
        Returns the results of searching the across all the strategies.
        """

        try:
            query_emb = await calc_search_embeddings(query)
        except Exception as e:
            errMsg = f"Failed to calculate query embeddings: {e}"
            log.error(errMsg)
            raise HTTPException(status_code=404, detail=errMsg)

        if query_emb is None:
            log.warning(f"calc_search_embeddings was returned as None")
            return []

        # let's first get the embeddings vector and then we'll do something special...

        res = app.search(query_emb)

        log.info(f"Search result is {res}")

        return res