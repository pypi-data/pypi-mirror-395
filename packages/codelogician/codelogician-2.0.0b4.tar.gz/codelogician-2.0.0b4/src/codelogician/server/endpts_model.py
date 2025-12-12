#
# Imandra Inc.
#
# model_cmd_endpoints.py
#

from fastapi import HTTPException
from imandra.u.agents.code_logician.command import Command
from ..strategy.model import Model
from ..strategy.events import ModelCLTaskEvent
from .cl_server import CLServer

import logging

log = logging.getLogger(__name__)

def register_model_endpoints (
        app : CLServer
    ):
    """
    Individual model commands
    """

    @app.post("/model/cmd/freeze/{index}", operation_id="freeze_model")
    async def model_freeze(
        index : int
    ):
        """
        Freeze the model
        """
        
        log.info(f"Submitting model freeze command for model with index={index}")

        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy")

        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        models = list(state.curr_meta_model.models.values())

        if not(0 <= index and index < len(models)):
            raise HTTPException(status_code=400, detail=f"Invalid index (number of models is {len(models)}: {index})")

        model : Model = models[index]

        model.iml_code_frozen = True

        return "OK"

    @app.post("/model/cmd/unfreeze/{index}", operation_id="unfreeze_model")
    async def model_unfreeze(
        index : int
    ):
        """
        Unfreeze the model
        """
        
        log.info(f"Submitting model unfreeze command for model with index={index}")

        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy")

        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        models = list(state.curr_meta_model.models.values())

        if not(0 <= index and index < len(models)):
            raise HTTPException(status_code=400, detail=f"Invalid index (number of models is {len(models)}: {index})")

        model : Model = models[index]

        model.iml_code_frozen = False

        return "OK"

    @app.post("/model/cmd/{index}", operation_id="post_model_command")
    async def model_command (
        index : int,
        cmd : Command
        ):
        """
        Submit model CodeLogician agent command
        """

        log.info(f"Submitting command={cmd} for model with path=[{index}]")

        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy") 

        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        if state.curr_meta_model is None:
            raise HTTPException(status_code=404, detail=f"No MetaModel exists!")

        if index not in state.curr_meta_model.models:
            raise HTTPException(status_code=404, detail=f"Could not locate model with specified index=[{index}]")

        try:
            taskEvent = ModelCLTaskEvent(rel_path=path, cmd=cmd)
            app.strategy_worker_by_id(strategy_id).add_event(taskEvent)
        except Exception as e:
            errMsg = f"Failed to create a task for CodeLogician: {str(e)}"
            log.error(errMsg)
            raise HTTPException(status_code=403, detail=errMsg)
    
        return "OK"
  
    @app.get("/model/paths", operation_id="get_model_paths")
    async def model_paths():
        """
        Get list of all paths for which models exist.
        """
        
        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy") 

        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        log.info("Request for model paths")
        if state.curr_meta_model is None:
            return []
        else:
            return list(state.curr_meta_model.models.keys())

    @app.get("/model/byindex/{index}")
    async def model_by_index(
        index : int
        ):
        """
        Retrieve a JSON represention of a Model for specified index (by model rel paths)
        """

        log.info(f"Request for model by index:{index}")

        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy")
        
        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")
        
        models = list(state.curr_meta_model.models.values())

        if not(0 <= index and index < len(models)):
            raise HTTPException(status_code=400, detail=f"Invalid index (number of models is {len(models)}: {index})")
        
        return models[index].model_dump_json()

    @app.get("/model/bypath/{path}", operation_id="get_model_by_path")
    async def model_by_path(
        path : str
        ):
        """
        Retrieve JSON representation of a model for a specified path (which is relative to the source directory)
        """
    
        log.info(f"Request for model by path: {path}")

        strategy_id = app.current_strat_id
        if strategy_id is None:
            raise HTTPException(status_code=404, detail=f"No current strategy") 

        try:
            state = app.strategy_state_by_id(strategy_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Failed to get strategy state: {e}")

        if path in state.curr_meta_model.models:
            return state.curr_meta_model.models[path].toJSON()
        else:
            raise HTTPException(status_code=404, detail=f"Model with specific path [{path}] not found!")
