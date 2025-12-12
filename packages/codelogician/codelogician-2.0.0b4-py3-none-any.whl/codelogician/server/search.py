#
#   Imandra Inc.
#
#   search.py
#

from pydantic import BaseModel

import rich.repr

@rich.repr.auto
class SearchResult(BaseModel):
    """
    Search result returned from a strategy
    """

    distance : float
    text : str
    rel_path : str
    match_entity_type : str
    strat_name : str
