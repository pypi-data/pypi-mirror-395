#
#   Imandra Inc.
#
#   model.py
#

import re

from imandra.u.agents.code_logician.base import (
    FormalizationDependency,
    FormalizationStatus,
    ModuleInfo,
    VG,
    RegionDecomp,
    OpaqueData
)

from collections import deque

from typing import Optional, Dict
from pathlib import Path
import datetime, logging

from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from rich import box

from pydantic import BaseModel, field_serializer
import numpy as np

log = logging.getLogger(__name__)

from .model_status import ModelStatus, SrcCodeStatus
from .model_task import (
    ModelTask, UserManualIMLEditTask, FormalizationNeed
)

from .cl_agent_state import (
    CLAgentState, 
    Embedding, 
    frm_status_to_rich
)


class UserIMLEdit(BaseModel):
    """
    We'll just use this to keep track of user edits
    """
    user_iml_entry : str
    src_code_at_the_time : str
    time_of_edit : datetime.datetime

class Model(BaseModel):
    """
        Container for a model - representing a single model along with its dependendencies, 
        formalization state, user-overriden IML code, etc...

        These are the primary events that the model handles:
        - 1. Update to the source code (will trigger CL agent state)
        - 2. Update to the IML code (by the user)
        - 3. Applying the result of running CL agent
        - 4. User freezes/unfreezes their IML code (to prevent it from 
            being overriden by CL results)
        - 5. User resets the changes that he made to the model (to the last CL model available)

        The metamodel updates the model when those events occur (listed above). It then 
        uses the Model status function to figure out wether a new event should be written
        or an update to IML code on disk

        Three ways that a status is accessed:
        - formalization_reasons(user_wait_time : int) -- returns a list of formalization reasons
          (why a CL task should be generated). The list may be comprised of the following:
            - FormalizationNeed.NO_AGENT_STATE - no formalization state exists
            - FormalizationNeed.SRC_CODE_CHANGED - underlying source code changed
            - FormalizationNeed.CONTEXT_ADDED - human has provided context for the model
            - FormalizationNeed.DEPS_CHANGED - formalization state of one or more of the dependencies changed
        
            -- if the returned list is empty, then no further action is required
                
        - iml_on_fs_update_ready() - should we update the iml model that's written to disk
            - Description: this can be set when we have an update to the model

    """

    rel_path : str
    src_code : Optional[str] = None
    src_code_last_changed : Optional[datetime.datetime] = None
    src_language : str = "Python"

    # This contains the formalization state - 
    # note it is updated by both - running CL on the source code changes (e.g. python)
    # and on user-manual edits to IML (we call a separate step for that)
    agent_state : Optional[CLAgentState] = None

    # Here we account for user's changes to the model IML code 
    # and keep track of how long it's been since they edited it
    # if it's been long enough and it's different that what we have
    # then we'll kick off a command to make it part of the Graph State
    user_iml_edit : Optional[UserIMLEdit] = None # This is human provided IML code and timestamp

    # If the user IML code is frozen, then even if the 
    # CL comes up with an update to the model, then it would still not 
    # override the file on disk
    iml_code_frozen : bool = False

    # Here we keep a record of what should be on disk
    # Because we have two sources of IML models on disk (agent and user)
    # we keep this here to check for differences if there's an update (i.e.
    # if we write the model to disk after CL results come in, then we update this
    # and when the FS event comes in for IML change, we disregard it)
    expected_iml_on_disk : Optional[str] = None

    src_code_embeddings : list[Embedding] = [] # Embeddings for the original source code
    iml_code_embeddings : list[Embedding] = [] # IML code embeddings

    # This is human-provided context that is sent to the CL agent
    context : Optional[str] = None

    # This is used to keep track of the latest TaskID that was generated
    # We can only apply changes to the CL agent state if the taskID of the
    # result andf what we're waiting for matches - otherwise we discard the results
    outstanding_task_ID : Optional[str] = None

    # This will be typically inserted after creation of the object because
    # this requires actual object references (to other models)
    dependencies : list['Model']|list[str] = [] # list of models that this model depends on
    rev_dependencies : list['Model']|list[str] = [] # list of models that this model affects (the inverse of dependencies)

    @field_serializer('dependencies','rev_dependencies')
    def serialize_tags(self, deps: list['Model']) -> list[str]:
        return list (map (lambda x: x.rel_path, deps))

    # This gets updated along with each agent state - here we maintain
    # IML code for the dependencies that were used. If they differ
    # then we may need to re-run CodeLogician.
    formalized_deps : list[FormalizationDependency] = []

    # We do the same with the human-provided context
    formalized_context : Optional[str] = None

    # Static formalization reasons - note if the model is "live"
    # (i.e. not post deserialization (so we have actual dependencies present)
    # then this is not used - this is only to store those for serialization
    # when we have to present the model
    static_frm_reasons : list[FormalizationNeed] = []
    @field_serializer('static_frm_reasons')
    def serialize_frm_reasons(self, _):
        return self.formalization_reasons()

    def add_dependency(self, d:'Model') -> None:
        """
        "Safe" add of a dependency - if it's already there, it would not add it twice
        """
        if d in self.dependencies: return
        self.dependencies.append(d)

    def status(self) -> ModelStatus:
        """ 
        Return a status object that contains various bits of the current state of the model
        """

        return ModelStatus(
            src_code_status=self.src_code_status(),
            instructions_added=self.context_provided(),
            deps_changed=self.deps_changed(),
            deps_need_formalization=self.deps_need_formalization(),
            outstanding_task_ID=self.outstanding_task_ID,
            formalization_status=self.formalization_status()
        )

    @staticmethod
    def calc_distance (vec1:list[float], vec2:list[float]):
        """
        Calculate cosine distance between two vectors
        """

        dot_product = np.dot(vec1, vec2)

        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)

        if norm_vec1 == 0 or norm_vec2 == 0:
            return 1.0  # Handle cases where one or both vectors are zero vectors
        
        cosine_similarity = dot_product / (norm_vec1 * norm_vec2)
        cosine_distance = 1 - cosine_similarity
        return cosine_distance

    def calc_embedding_distance (self, query_vector : list[float]) -> tuple[float|None, str|None]:
        """
        Calculate distance between the specified query vector and its own embeddings. 
        Return the one with smallest distance. 
        """

        qv = np.array(query_vector)

        def do_search(embeddings):
            min_distance = None

            for embedding in embeddings:
                curr_vec = np.array(embedding.vector)

                try:
                    distance = self.calc_distance(qv, curr_vec)
                except Exception as e:
                    raise Exception(f"Failed to calculate distance: {e}")

                if min_distance is None:
                    min_distance = distance
                else:
                    if distance < min_distance:
                        min_distance = distance
            return min_distance

        min_dist_iml = do_search(self.iml_code_embeddings)
        min_dist_src = do_search(self.src_code_embeddings)

        if min_dist_iml is None and min_dist_src is None:
            return None, None
        elif min_dist_iml is None and min_dist_src is not None:
            return float(min_dist_src), 'SRC'
        elif min_dist_iml is not None and min_dist_src is not None:
            return float(min_dist_iml), 'IML'
        else:
            if min_dist_iml < min_dist_src:
                return float(min_dist_iml), 'IML'
            else:
                return float(min_dist_src), 'SRC'

    def needs_embedding_update(self) -> bool:
        """
        Does this model need to update embedding info?
        """
        # TODO check to see if the source code/etc changed since last embedding...
        return False

    def gen_iml_user_update_task (self) -> ModelTask|None:
        """
        Generate a model task for updating the IML code within the graph state.
        What happens is that during the update, extract the VGs/Decomps, etc and place them 
        in the right format within the graph state.
        """

        if self.user_iml_edit is None:
            return None

        def remove_import_directives(text: str) -> str:
            """
            Removes lines of the form [@@@import ...] from the given text.
            """
            return re.sub(r'^\s*\[@@@import.*?\]\s*\n?', '', text, flags=re.MULTILINE)

        task = UserManualIMLEditTask (
            rel_path=self.rel_path,
            graph_state = self.agent_state.graph_state if self.agent_state else None,
            iml_code=remove_import_directives(self.user_iml_edit.user_iml_entry),
            dependencies=self.dependencies_iml_models()
        )

        self.outstanding_task_ID = task.task_id

        return task

    def gen_embedding_task (self) -> ModelTask:
        """
        Create an embedding task - TODO: we should streamline this 
        """
        task = ModelTask(
            rel_path=self.rel_path,
            src_code=self.src_code if self.src_code else "",
            context=self.context,
            gen_embeddings=True
        )

        # Let's now save this task so we know that we should expect 
        # the result 
        self.outstanding_task_ID = task.task_id

        return task

    def gen_formalization_task(self) -> ModelTask:
        """
        Generate a formalization task (ModelTask) object if we need to
        """

        task = ModelTask (
            rel_path=self.rel_path,
            src_code=self.src_code if self.src_code else "",
            context=self.context,
            graph_state=self.agent_state.graph_state if self.agent_state else None,
            dependencies=self.dependencies_iml_models()
        )

        self.outstanding_task_ID = task.task_id

        return task
    
    def set_iml_code_frozen(self) -> None:
        """
        Set IML code frozen - this will prevent any 
        """
        self.user_iml_code_frozen = True

    def set_iml_code_unfrozen(self) -> None:
        """
        Here we set the IML code unfrozen
        """
        self.user_iml_code_frozen = False

    def cl_result_available(self) -> bool:
        """
        Is there a CL result that has been available, but not set
        b/c of the frozen client model?
        """

        return False

    def context_provided(self) -> bool:
        """ 
        Return True if there's human-provided context
        """

        return bool(self.context)

    def iml_on_fs_update_ready(self) -> bool:
        """
        Returns True/False if there's an update to the IML model that should be written to disk...
        """

        return False

    def apply_agent_state (self,
        agent_state : CLAgentState,
        dependencies : list[FormalizationDependency] = [],
        result_of_user_edit : bool = False) -> None:
        """
        Apply the agent state and store the dependencies that were used in the call to CL agent

        Parameters:
        - agent_state - CLAgentState that we'll apply
        - dependencies - the dependencies that were used during formalization - we'll use them later to compare if 
            we need to redo autoformalization.
        - result_of_user_edit : bool

        """

        # Let's make sure we have an actual CLAgentState
        if not isinstance(agent_state, CLAgentState):
            raise Exception (f"Expected a value of CLAgentState, but got something else: {str(agentState)}!")

        # Let's also now reset the task ID
        self.outstanding_task_ID = None

        # Agent state
        self.agent_state = agent_state

        # Remove instructions that were used from the current list of outstanding ones
        self.formalized_context = agent_state.context

        # Let's now set the dependencies' models that were used
        self.formalized_deps = dependencies

        # We can also update the embeddings
        self.src_code_embeddings = agent_state.src_code_embeddings
        self.iml_code_embeddings = agent_state.iml_code_embeddings

    def user_iml_change_ready (self, user_wait_time : int | None) -> bool:
        """
        Is the user's IML change ready to be turned into a task. Here, we consider whether 
        the change done by the user is "old enough". We do this to ensure we're only formalizing
        changes that have become 'stable'.
        """

        if self.user_iml_edit is None:
            return False

        if user_wait_time is None:
            long_enough = True
        else:
            long_enough = \
                (datetime.datetime.now() - self.user_iml_edit.time_of_edit) \
                > \
                datetime.timedelta(seconds=user_wait_time)

        return long_enough

    def formalization_reasons(self, user_wait_time : Optional[int] = None) -> list[FormalizationNeed]:
        """
        Unlike the function `user_iml_change_ready`, here we only look at the source code changes.
        Returns a list of reasons for the need to perform formalization on this model.
        If the list is empty - then there's no need to do it.
        """

        if self.src_code is None: return [] # if we have no source code (i.e. file was deleted), then there's nothing to do
        if self.agent_state is None: return [FormalizationNeed.NO_AGENT_STATE]

        reasons:list[FormalizationNeed] = []
        if self.has_src_code_changed(user_wait_time): reasons.append(FormalizationNeed.SRC_CODE_CHANGED)
        if self.context_provided(): reasons.append(FormalizationNeed.CONTEXT_ADDED)
        if self.deps_changed(): reasons.append(FormalizationNeed.DEPS_CHANGED)

        return reasons

    def deps_need_formalization(self, user_wait_time : int = 0):
        """ 
        Return True if there're dependencies (may be indirect) that are due for formalization and
        False otherwise. We use this function when constructing the list of Tasks for the metamodel. 
        """

        for d in self.dependencies:
            if d.formalization_reasons(user_wait_time) or d.deps_need_formalization(user_wait_time):
                return True
        
        return False

    def full_deep_dependencies(self) -> list['Model']:
        """ 
        Get a full deep list of dependencies
        """

        result = []

        def helper (m : 'Model'):
            """
            Traverse the dependencies graph
            """

            for m in m.dependencies:
                if m not in result:
                    result.append(m)
                
                helper(m)

        helper(self)

        return result

    def shallow_dep_iml_models (self) -> list[FormalizationDependency]:
        """
        Return the list of only the top-level 
        """

        if len(self.dependencies) == 0: return []
        if isinstance(self.dependencies[0], str): return []
        
        ds : list[FormalizationDependency] = []

        for model in self.dependencies:
            src_mod_info = model.to_CL_src_module_info()
            iml_mod_info = model.to_CL_iml_module_info()

            # We only care about the models that have IML code available
            if iml_mod_info is None: continue

            ds.append(
                FormalizationDependency (
                    src_module=src_mod_info,
                    iml_module=iml_mod_info,
                )
            )
        
        return ds

    def dependencies_iml_models(self) -> list[FormalizationDependency]:
        """
        This is used in two places -> to print out the full model and to 
        generate formalizaiton task context
        """

        log.debug(f"Will now get the list of dependencies for {self.rel_path}")

        if len(self.dependencies) == 0: return []
        if isinstance(self.dependencies[0], str): return []

        ds : list[FormalizationDependency] = []

        full_list = self.full_deep_dependencies()

        sorted_list = Model.do_topological_sort(full_list)

        for model in sorted_list:
            src_mod_info = model.to_CL_src_module_info()
            iml_mod_info = model.to_CL_iml_module_info()

            # We only care about the models that have IML code available
            if iml_mod_info is None: continue

            ds.append(
                FormalizationDependency(
                src_module=src_mod_info,
                iml_module=iml_mod_info,
                )
            )

        log.debug(f"Done")

        return ds

    def make_dep_name_from_path (self, rel_path : str) -> str:
        """
        Create a name for a dependency 
        """
        p = Path(rel_path).parent / Path(rel_path).stem

        return ('_'.join(Path(p).parts)).capitalize()

    def to_CL_src_module_info(self) -> ModuleInfo:
        """
        Create ModuleInfo
        """

        return ModuleInfo (
            name = self.make_dep_name_from_path(self.rel_path),
            relative_path = Path(self.rel_path),
            content = self.src_code if self.src_code else "",
            src_lang = self.src_language
        )

    def to_CL_iml_module_info(self) -> ModuleInfo | None:
        """
        Return ModuleInfo object for the IML code if it's available, None otherwise
        """

        # If we don't have any IML code for this model, let's not return it
        if self.iml_code() is None:
            return None
        
        if self.iml_code() is not None:
            iml_code = str(self.iml_code())
        else:
            iml_code = ""

        return ModuleInfo (
            name = self.make_dep_name_from_path(self.rel_path),
            relative_path = Path(self.rel_path),
            content = iml_code,
            src_lang="IML"
        )

    def src_code_status(self, srcCodeWaitTime : Optional[int] = None) -> SrcCodeStatus:
        """
        Return source code status
        """

        if self.src_code is None:
            return SrcCodeStatus.SRC_CODE_DELETED

        else:
            if srcCodeWaitTime is None or self.src_code_last_changed is None:
                timeLongEnough = True
            else:
                timeLongEnough = (datetime.datetime.now() - self.src_code_last_changed) > datetime.timedelta(seconds=srcCodeWaitTime)

        if timeLongEnough and (hash(self.src_code) == hash(self.iml_code())):
            return SrcCodeStatus.SRC_CODE_CHANGED
        else:
            return SrcCodeStatus.SRC_CODE_CURRENT

    def formalization_status(self) -> FormalizationStatus:
        """
        Return formalization status of the model
        """
        if self.agent_state is None:
            return FormalizationStatus.UNKNOWN
        else:
            return self.agent_state.status

    def has_src_code_changed(self, user_wait_time : Optional[int] = None) -> bool:
        """
        Return True if source code has changed from when it was formalized
        """

        # if we're missing formalization altogether, then source code has changed
        if self.agent_state is None:
            return True

        if user_wait_time is None or self.src_code_last_changed is None:
            timeLongEnough = True
        else:
            timeLongEnough = (datetime.datetime.now() - self.src_code_last_changed) > \
            datetime.timedelta(seconds=user_wait_time)

        return timeLongEnough and (hash(self.src_code) != hash(self.agent_state.src_code))

    def deps_changed(self) -> bool:
        """    
        Return True if dependencies' models (IML code) have changed since we
        ran CL formalization task last time. When we receive CL results, we always
        record dependencies' IML models that were used. 
        """

        currentDeps = self.shallow_dep_iml_models()

        paths_list = list(map(lambda x: Path(x.rel_path), self.dependencies))

        relevant_formalized_deps = \
            list(filter(lambda x: x.src_module.relative_path in paths_list, self.formalized_deps))
    
        if len(relevant_formalized_deps) != len(currentDeps):
            return True

        # This will iterate through the list and pick up any changes
        # to the dependencies (they're Pydantic model objects)
        for d in relevant_formalized_deps:
            if d not in currentDeps:
                return True
            
        return False

    def create_import_iml_statements(self):
        """
        Generate a list of import statements to the relevant IML models.
        """

        text = ""

        for d in self.dependencies_iml_models():
            name = d.iml_module.name
            rel_path = str(Path(d.iml_module.relative_path).with_suffix('.iml'))
            text += f"[@@@import {name}, \"{rel_path}\"]\n"
        
        return text

    def set_iml_model (
            self, 
            new_iml_model : str,
            record_time : bool = False) -> None:
        """
        Set the IML model code and record the time if we need to. This is called
        when the user manually overrides the model. We also need to check if the model
        actually changed... (this event is all also  called when we write out the model
        from CL result - it can't tell the difference, so we need to check it here...)
        """

        # We use hash as it also handles the case when models are None
        if hash(new_iml_model.strip()) == hash(str(self.expected_iml_on_disk).strip()): 
            log.warning(f"Model set by the user doesn't appear to be any different from existing model: [{self.rel_path}]")
            return
        
        log.info(f"User is updating the IML model: [{self.rel_path}]")

        self.user_iml_edit = UserIMLEdit(
            user_iml_entry=new_iml_model,
            src_code_at_the_time = "N\\" if self.src_code is None else self.src_code,
            time_of_edit=datetime.datetime.now()
        )

    def set_src_code(self, new_src_code : str|None, record_time:bool = False) -> None:
        """
        Set the src_code and update the time source code changed
        """

        # This means the code was deleted
        if new_src_code is None:
            self.src_code = None
            self.src_code_last_changed = None
            return 

        #if not isinstance(new_src_code, str):
        #    raise Exception (f"Expected a string value for `new_src_code`, but got {type(new_src_code).__name__}")

        if hash(new_src_code) != hash(self.src_code):
            log.info(f"Updating source code for model [{self.rel_path}]")
      
            if record_time:
                self.src_code_last_changed = datetime.datetime.now()
            else:
                self.src_code_last_changed = None

            self.src_code = new_src_code
        else:
            log.warning(f"Specified model hasn't changed: [{self.rel_path}]")

    def iml_code_to_print(self) -> str:
        """
        Provide IML code (if available) along with relevant import statements
        """

        if self.iml_code() is None: return "N\\A"

        import_statements = self.create_import_iml_statements()

        full_model = f"{import_statements}\n\n{self.iml_code()}"

        return full_model

    def iml_code(self) -> str | None:
        """
        If available, returns IML code with artifacts (e.g. VGs and decomps)
        """
        return self.agent_state.iml_code if self.agent_state else None

    def iml_model(self) -> str | None:
        """
        If available, returns IML model (not artifacts like VGs, decomps). This
        also looks at the available user-overriden code.
        """

        return self.agent_state.iml_model if self.agent_state else None

    def verification_goals(self) -> list[VG]:
        """
        If available, returns the list of dictionaries with verification goals
        """
        return self.agent_state.vgs if self.agent_state else []

    def failed_vgs(self) -> list[VG]:
        """
        Return just the list of failed VGs
        """
        return list(filter(lambda x: x['status'] == False, self.verification_goals()))

    def decomps(self) -> list[RegionDecomp]:
        """
        If available, returns the list of decomposition requests
        """
        return self.agent_state.region_decomps if self.agent_state else []
    
    def opaque_funcs (self) -> list[OpaqueData]:
        """
        If available, return the opaque functions used along with their approximations
        """
        return self.agent_state.opaque_funcs if self.agent_state else []

    def gen_stats(self) -> Dict[str, str|int]:
        """
        Generate some numberical stats for this model
        """

        s:dict[str, str|int] = {}
        s['frm_status'] = str(self.formalization_status())
        s['num_opaques'] = len(self.opaque_funcs())
        s['num_failed_vgs'] = len(self.failed_vgs())

        return s

    def toJSON (self) -> str:
        """
        Return a dictionary we can save to disk
        """
        
        # This will save the reasons which we can only calculate if
        # we have "live" dependency models (not strings as is the case
        # post-deserialization)
        self.static_frm_reasons = self.formalization_reasons(5)

        log.debug(f"Adding static frm reasons: [{self.static_frm_reasons}]")

        return self.model_dump_json()

    @staticmethod
    def fromJSON(j : str | dict[str,str]) -> 'Model':
        """
        Return a Model object from provided JSON. Note that we do not set the lists
        of models for 'dependsOn' here because we don't have access to the
        actual model objects. This is done outside this state methods.
        """

        if isinstance(j, str):
            return Model.model_validate_json(j)
        else:
            return Model.model_validate(j)

    def str_summary(self) -> str:
        """
        Return a one-line string with high-level details
        """

        return f"[status={self.status()}]"

    def __hash__ (self):
        """
        We need this so we can compare models
        """
        return hash(str(self.toJSON()))

    def __repr__(self):
        """
        Return a nice representation
        """

        dependencyPaths = list(map(lambda x: x.rel_path, self.dependencies))
        agentStateStr = "None" if self.agent_state is None else self.agent_state.status

        s  = f"Model: {self.rel_path} \n"
        s += f"{str(self.status())}\n"
        s += f"Formalization state: {agentStateStr}\n"
        s += f"Depends on: {dependencyPaths}\n"
        s += f"Source language: {self.src_language}\n"

        if self.src_code:
            s += f"Source code (condensed): \n {self.src_code[:100]}\n"
        else:
            s += f"Source code (condensed): \n None \n"

        s += f"Opaque funcs: {len(self.opaque_funcs())}\n"
        s += f"Decomps: {len(self.decomps())}\n"
        return s

    def __rich__ (self):
        """ 
        Return a Rich representation 
        """

        table = Table(
            title=Text(f"Model: {self.rel_path}", style="bold italic magenta"),
            box=box.MINIMAL_DOUBLE_HEAD,
            show_lines=True
        )

        table.add_column("Name")
        table.add_column("Attribute")

        src_code_str = "N/A" if self.src_code is None else self.src_code
        user_iml_code_str = "N/A" if self.user_iml_edit is None else self.user_iml_edit.user_iml_entry
        user_iml_code_last_change = "N/A" if self.user_iml_edit is None else str (self.user_iml_edit.time_of_edit)

        needs_frm_str = "Yes" if self.static_frm_reasons == [] else "No"
        frozen_str = "Yes" if self.iml_code_frozen else "No"

        iml_code_str = "N/A" if not self.iml_code() else str(self.iml_code())

        eval_result_str = "N/A" if not self.agent_state else self.agent_state.eval_res

        table.add_row( "Relative path",                 Text(self.rel_path, style="bold")                       )
        table.add_row( "Formalization status",          frm_status_to_rich(self.formalization_status())         )
        table.add_row( "Eval result",                   Text(eval_result_str, style="bold"))
        table.add_row( "Needs formalization?",          Text(needs_frm_str, style="bold")                       )
        table.add_row( "Formalization reasons",         Text(str(self.static_frm_reasons))                      )
        table.add_row( "Frozen?",                       Text(frozen_str)                                        )
        table.add_row( "Src last changed",              Text(f"{self.src_code_last_changed}", style="bold")     )
        table.add_row( "Src code",                      Syntax(src_code_str, "python")                          )
        table.add_row( "IML code",                      Syntax(iml_code_str, "ocaml")                           )
        table.add_row( "User IML code",                 Syntax(user_iml_code_str, "ocaml")                      )
        table.add_row( "User IML code last changed",    Text(f"{user_iml_code_last_change}", style="bold")      )
        table.add_row( "Src Code Embeddings",           Text(f"{bool(self.src_code_embeddings)}", style="bold") )
        table.add_row( "IML Code Ebeddings",            Text(f"{bool(self.iml_code_embeddings)}", style="bold") )
        table.add_row( "Context",                       Text(f"{self.context}", style="bold")                   )
        table.add_row( "Task ID",                       Text(f"{self.outstanding_task_ID}", style="bold")       )
        table.add_row( "Deps",                          Text(f"{self.dependencies}", style="bold")              )
        table.add_row( "Opaques",                       Text(f"{self.opaque_funcs()}", style="bold")            )
        table.add_row( "Verification Goals",            Text(f"{self.verification_goals()}", style="bold")      )
        table.add_row( "Decompositions",                Text(f"{self.decomps()}", style="bold")                 )

        return table

    @staticmethod
    def do_topological_sort(models : list['Model']) -> list['Model']:
        """
        Return list of paths s.t. they're sorted topologically (by dependencies)
        """

        path_to_idx, idx_to_path = {}, {}
        edges = []
        idx = 0

        def add_to_lookup(idx, path):
            path_to_idx[path] = idx
            idx_to_path[idx] = path

        # Get all the edges
        for model in models:
            if model.rel_path not in path_to_idx:
                add_to_lookup(idx, model.rel_path)
                idx += 1

            for d in model.dependencies:
                if d.rel_path not in path_to_idx:
                    add_to_lookup(idx, d.rel_path)
                    idx += 1
                    
                edges.append((path_to_idx[model.rel_path], path_to_idx[d.rel_path]))

        def constructadj(V, edges):
            adj = [[] for _ in range(V)]
            for u, v in edges:
                adj[u].append(v)
            return adj

        def topologicalSort(V, edges):
            adj = constructadj(V, edges)

            indegree = [0] * V

            # Calculate indegree of each vertex
            for u in range(V):
                for v in adj[u]:
                    indegree[v] += 1
            
            # Queue to store vertices with indegree 0
            q = deque ([i for i in range(V) if indegree[i] == 0])

            result = []
            while q:
                node = q.popleft()
                result.append(node)

                for neighbor in adj[node]:
                    indegree[neighbor] -= 1
                    if indegree[neighbor] == 0:
                        q.append(neighbor)
            
            # Check for cycle
            if len(result) != V:
                raise Exception (f"Graph contains cycle!")
            
            return result
        
        sorted_model_idxs = topologicalSort(len(models), edges)

        sorted_models = []

        # Here we just convert indexes into actual Model objects
        for i in sorted_model_idxs:
            matches = list(filter(lambda m: m.rel_path == idx_to_path[i], models))
            if len(matches):
                sorted_models.append(matches[0])
        
        # For our purposes, we need leafs to go first
        sorted_models.reverse()

        return sorted_models

class ModelList(BaseModel):
    """
    We use this with terminal CLI tools
    """

    models : list[Model]

    def toJSON(self) -> dict:
        """
        Return a JSON
        """
        return [m.toJSON() for m in self.models]
   
    @staticmethod
    def fromJSON(j : str|dict) -> 'ModelList':
        """
        """
        if isinstance(j, str):
            return Model.model_validate_json(j)
        elif isinstance(j, dict):
            return Model.model_validate(j)
        else:
            raise Exception (f"Input must be either a str or a dict!")

    @staticmethod
    def get_model_summary(m : Model) -> dict[str,str|bool|int|FormalizationStatus]:
        """ 
        Create a dict with various summary stats of the provided model
        """

        d = {}
        d['frm_status'] = m.formalization_status()
        d['needs_frm'] = "No" if m.static_frm_reasons == [] else "Yes"
        d['frm_reasons'] = list(map(str, m.static_frm_reasons))
        d['is_frozen'] = "Yes" if m.iml_code_frozen else "No"
        d['rel_path'] = m.rel_path
        d['src_last_ched'] = m.src_code_last_changed

        d['user_iml_code'] = not(m.user_iml_edit is None)
        d['user_iml_last_ched'] = str(m.user_iml_edit.time_of_edit) if m.user_iml_edit else "N\\A"

        d['src_code_embds'] = bool(m.src_code_embeddings)
        d['iml_code_embds'] = bool(m.iml_code_embeddings)
        d['context'] = m.context
        d['task_id'] = m.outstanding_task_ID
        d['deps'] = m.dependencies
        d['num_opaques'] = len(m.opaque_funcs())
        d['num_vgs'] = len(m.verification_goals())
        d['num_decomps'] = len(m.decomps())

        return d

    def __rich__(self):
        """ 
        We'll used this in the CLI
        """

        table = Table(
            title=Text(f"Models list", style="bold italic magenta"),
            box=box.MINIMAL_DOUBLE_HEAD,
            show_lines=True
        )

        table.add_column("ID"                       , justify="right", no_wrap=True )
        table.add_column("Frm Status"               , justify="right", no_wrap=True )
        table.add_column("Frozen"                   , justify="right", no_wrap=True )
        table.add_column("Needs frm?"               , justify="right", no_wrap=True )
        table.add_column("Frm Needs"                , justify="right", no_wrap=False)
        table.add_column("Rel path"                 , justify="right", no_wrap=True )
        table.add_column("Src Last Changed"         , justify="right", no_wrap=True )
        table.add_column("User IML Code"            , justify="right", no_wrap=True )
        table.add_column("User IML Code Last Chged" , justify="right", no_wrap=True )
        table.add_column("Src Code Embds"           , justify="right", no_wrap=True )
        table.add_column("IML Code Embds"           , justify="right", no_wrap=True )
        table.add_column("Context"                  , justify="right" )
        table.add_column("Task ID"                  , justify="right" )
        table.add_column("Dependencies"             , justify="right", no_wrap=False)
        table.add_column("Num opaques"              , justify="right" )
        table.add_column("Num VGs"                  , justify="right" )
        table.add_column("Num Decomps"              , justify="right" )

        for m_id, m in enumerate(self.models):
            d = ModelList.get_model_summary(m)
            table.add_row (
                Text(f"{m_id}", style="bold"),
                frm_status_to_rich(d['frm_status']),
                Text(f"{d['is_frozen']}", style="bold"),
                Text(f"{d['needs_frm']}", style="bold"),
                Text(f"{d['frm_reasons']}", style="bold"),
                Text(f"{d['rel_path']}", style="bold"),
                Text(f"{d['src_last_ched']}", style="bold"),
                Text(f"{d['user_iml_code']}", style="bold"),
                Text(f"{d['user_iml_last_ched']}", style="bold"),
                Text(f"{d['src_code_embds']}", style="bold"),
                Text(f"{d['iml_code_embds']}", style="bold"),
                Text(f"{d['context']}", style="bold"),
                Text(f"{d['task_id']}", style="bold"),
                Text(f"{d['deps']}", style="bold"),
                Text(f"{d['num_opaques']}", style="bold"),
                Text(f"{d['num_vgs']}", style="bold"),
                Text(f"{d['num_decomps']}", style="bold")
            )
        
        return table