#
# Imandra Inc.
#
# endpts_strategy.py
#

from fastapi import HTTPException
from .cl_server import CLServer
from .state import ServerState
from ..strategy.state import StrategyState
from ..strategy.config import StratConfig, StratConfigUpdate
from typing import Dict

# TODO need to implement this vs manually creating an pydantic model
#from pydantic_partial import create_partial_model
#PartialPyIMLConfig = create_partial_model(StratConfig)

import logging
log = logging.getLogger(__name__)

def register_strategy_endpoints (
        app: CLServer
    ):
    """ 
    Functions relate to accessing the state of the strategy or sending it commands
    """

    @app.post("/strategy/setcws/{strat_id}", operation_id="setcws")
    async def set_cws(strat_id : str) -> str:
        """
        Set the current working strategy
        """
        
        try:
            app.set_current_strat_id(strat_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update current working strategy: {e}")
        
        return "OK"

    @app.get("/strategy/cws", operation_id="cws")
    async def get_cws() -> str | None:
        """
        Return ID of the current working strategy
        """
        return app.current_strat_id
    

    @app.get("/strategy/list", operation_id="list_strategies")
    async def list_strategies () -> list[Dict[str, str]]:
        """
        Return the current list of strategies. Each strategy will contain:
        - 'strat_id' - strat_id
        - 'path' - directory path for this strategy
        - 'type' - 'PyIML' will be returned as it's the only strategy currently supported 
        """
        return app.list_strategies()

    @app.get("/strategy/states", operation_id="get_all_strategy_states")
    async def all_strategy_states () -> list[StrategyState]:
        """
        Return all strategy states
        """
        return list(app.strategy_states().values())

    @app.post("/strategy/create", operation_id="create_new_strategy")
    async def create_strategy (
        strat_type : str,
        strat_path : str
        ) -> str:
        """
        Create a new strategy
        """
        try:
            strat_id = app.add_strategy(strat_type, strat_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create strategy: {e}")
    
        return strat_id

    @app.post("/strategy/delete/{strat_id}", operation_id="delete_strategy")
    async def delete_strategy (
        strat_id : str
        ) -> str:
        """
        Remove strategy (will stop the worker and delete it from the container)
        """

        if app.current_strat_id is None:
            raise HTTPException(status_code=400, detail=f"No current strategy") 

        try:
            app.rem_strategy(app.current_strat_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to delete strategy: {str(e)}")
    
        return "OK"

    @app.get("/strategy/state", operation_id="get_strategy_state")
    async def strat_state ( 
        strategy_id : str
        ) -> StrategyState:
        """
        Return the full strategy state 
        """
        log.info(f"Received strategy state request")

        if app.current_strat_id is None:
            raise HTTPException(status_code=400, detail=f"No current strategy") 

        try:
            state = app.strategy_state_by_id(app.current_strat_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        return state

    @app.get("/strategy/summary", operation_id="get_strategy_summary")
    async def strat_summary (
        strategy_id : str
        ) -> dict:
        """
        Return PyIML strategy state summary
        """
        log.info("Received request for strategy summary")    

        if app.current_strat_id is None:
            raise HTTPException(status_code=400, detail=f"No current strategy") 

        try:
            state = app.strategy_state_by_id(app.current_strat_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        return state.summary()

    @app.get("/strategy/config", operation_id="get_strategy_config")
    async def strat_config (
        strategy_id : str
        ) -> StratConfig:
        """ 
        Return the current strategy configuration 
        """
        log.info("Received request for strategy config")

        if app.current_strat_id is None:
            raise HTTPException(status_code=400, detail=f"No current strategy") 

        try:
            strat_config = app.strategy_config_by_id(app.current_strat_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        return strat_config
  
    @app.patch("/strategy/config/set", operation_id="set_config_field")
    async def strat_config_set (
        configUpdate : StratConfigUpdate
        ) -> str:
        """
        Set strategy configuration field to specified value.
        """

        if app.current_strat_id is None:
            raise HTTPException(status_code=400, detail=f"No current strategy") 

        try:
            strat_config = app.strategy_config_by_id(app.current_strat_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy config: {e}")

        log.info(f"Received strategy config update request: {str(configUpdate.model_dump())}")
        try:
            updated_data = configUpdate.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(strat_config, key, value)
        
            app.update_strat_config(app.current_strat_id, strat_config)
        except Exception as e:
            err_msg = f"Error when attempting to update config: {str(e)}"
            log.error(err_msg)
            return HTTPException(status_code=406, detail=err_msg)
        
        return "OK"
