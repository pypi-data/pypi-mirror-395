#
#   Imandra Inc.
#
#   meta_model.py
#

from functools import cmp_to_key
from pathlib import Path
from collections import defaultdict
from imandra.u.agents.code_logician.base import FormalizationStatus


from ..server.events import FileSystemEvent, FileSystemEventType
from .cl_agent_state import CLAgentState
from .model import Model, ModelList
from .model_task import ModelTask
from .sketch import Sketch
from .worker import CLResult

from ..tools.filesystem import FileSystem
from ..dep_tools.python import build_py_dep_graph

from rich.text import Text
from rich.pretty import Pretty
from rich.panel import Panel
from rich import print as rprint

from pydantic import BaseModel, model_validator
from typing import Dict, Tuple
import json

import logging
log = logging.getLogger(__name__)

class MetaModel(BaseModel):
    """
    Container for the set of models representing the whole directory
    """

    src_dir_abs_path : str
    models : Dict[str, Model]
    language : str = "Python"

    @model_validator(mode='after')
    def link_model_deps(self) -> 'MetaModel':
        """
        When store states to disk, we store relative paths for 
        dependencies/rev_dependencies. Here we substitute them with actual model objects.
        """

        for model in self.models.values():
            model_deps, model_rev_deps = [], []

            for dep in model.dependencies:
                if isinstance(dep, str) and dep in self.models:
                    model_deps.append(self.models[dep])
                else:
                    model_deps.append(dep)

            for dep in model.rev_dependencies:
                if isinstance(dep, str) and dep in self.models:
                    model_rev_deps.append(self.models[dep])
                else:
                    model_rev_deps.append(dep)
        
            model.dependencies = model_deps
            model.rev_dependencies = model_rev_deps
        
        return self
    
    def search (
            self, 
            query_vector : list[float],
            num_top_hits : int = 5
        ) -> list[Tuple[float, str, str]]:
        """
        Return the list of models more whose embedding vectors are closest to the query, along with
        the distance.
        """

        distances = []
        unavailable = 0

        # TODO This right now just gets us the top hit from each model
        # but, we should instead aggregate them across models and get
        # the top hits that way
        for model in self.models.values():
            dist, src_type = model.calc_embedding_distance(query_vector)

            if dist is None:
                unavailable += 1
                continue
            else:
                sresult = {
                    'dist': dist,
                    'rel_path': model.rel_path,
                    'src_type': src_type
                }
                distances.append(sresult)

        # let's now sort the distances and select top_k from there 
        return list(sorted(distances, key=lambda x: x['dist']))[:num_top_hits]

    def get_paths_with_dirs(self):
        """ 
        Return a list of paths with directory information
        """

        FILE_MARKER = '<files>'
        def attach(branch, trunk, model):
            parts = branch.split('/', 1)
            if len(parts) == 1:  # branch is a file
                trunk[FILE_MARKER].append(model)
            else:
                node, others = parts
                if node not in trunk:
                    trunk[node] = defaultdict(dict, ((FILE_MARKER, []),))
                attach(others, trunk[node], model)

        main_dict = defaultdict(dict, ((FILE_MARKER, []),))
        
        for path in sorted(self.models.keys()):
            attach(path, main_dict, self.models[path])

        return main_dict

    def list_models (self) -> ModelList:
        """
        Return the list of all models
        """
        
        return ModelList(models=list(self.models.values()))

    def vgs(self):
        """
        Return all verification goals for all the models
        """
        return { m.rel_path : m.verification_goals() for m in self.models.values() }

    def decomps(self):
        """
        Return decomposition requests for all the models
        """
        return { m.rel_path : m.decomps() for m in self.models.values() }

    def opaques(self):
        """
        Return all the opaque functions for all the models
        """
        return { m.rel_path : m.opaque_funcs() for m in self.models.values() }

    def apply_cl_result (self, cl_result : CLResult) -> None:
        """
        Applies the result of running CodeLogician on a model
        """

        if cl_result.task.rel_path in self.models:
            model = self.models[cl_result.task.rel_path]

            # Rememeber that we may have multiple tasks outstanding simultaneously
            # so, we always keep the last one that we use
            if model.outstanding_task_ID == cl_result.task.task_id:

                dependencies = cl_result.task.dependencies
                model.apply_agent_state(cl_result.agent_state, dependencies)
                model.outstanding_task_ID = None

                log.info(f"CLResult applied to model successfully!")
            else:
                log.warning(f"Model with path={cl_result.task.rel_path} has a newer Task ID, so ignoring this one!")
        else:
            log.error(f"Attempting to apply CL Result to a non-existent model path: {cl_result.task.rel_path}!")

    def update_model(self, rel_path : str, state : CLAgentState) -> None:
        """
        Update the model with a new agent state (formalization state form CL agent)
        """

        if rel_path in self.models:
            self.models[rel_path].apply_agent_state(state)
            log.info(f"AgentState successfully updated for model with path=[{rel_path}]")
        else:
            log.error(f"Attempting to set agent state to a non-existent model path {rel_path}")


    def get_embedding_tasks(self) -> list[ModelTask]:
        """
        Generate list of CL tasks to generate embeddings
        """

        tasks = []
        for model in self.models.values():
            if model.needs_embedding_update():
                tasks.append(model.gen_embedding_task())
        
        return tasks

    def get_next_tasks(self, user_wait_time : int | None = None) -> list[ModelTask]:
        """ 
        Create a list of formalization tasks for the strategy to send to the CL agent.

        We're looking for models that need:
        - Have a
        - Formalization done
        - Have no formalization tasks outstanding (`model.outstanding_task_ID == None`)
        - Have no dependencies that need formalization

        - user_wait_time - how much we should wait since the last src code/iml model update - 
        this is used to determine whether `src_code` and/or 'iml_code' have changed.
        """

        log.debug(f"About to `get_next_tasks`")

        tasks : list[ModelTask] = []

        for model in self.models.values():

            if model.user_iml_change_ready(user_wait_time) and model.outstanding_task_ID is None:
                log.debug(f"Model {model.rel_path} will need a user IML override task")
                model_task = model.gen_iml_user_update_task()
                if model_task:
                    tasks.append(model_task)
                    log.info(f"Added model task for manually setting IML code [{model.rel_path}]")
                else:
                    log.error(f"We should've gotten a ModelTask user IML change for this model, but didnt! [{model.rel_path}]")
                    continue

                log.debug(f"The model [{model.rel_path}] has unprocessed user set IML code.")

            else:
                # Let's now consider the "regular" CL task
                log.debug(f"Will now check if model {model.rel_path} needs formalization")
                needs_formalization = bool(model.formalization_reasons(user_wait_time))
                deps_dont_need_formalization = not(model.deps_need_formalization())

                if needs_formalization and deps_dont_need_formalization and \
                    model.outstanding_task_ID is None:
                    log.info (f"{model.rel_path} needs formalization: [{model.formalization_reasons(user_wait_time)}]")
                    tasks.append(model.gen_formalization_task())
                
                    log.debug(f"Model [{model.rel_path}] has a formalization task!")
                else:
                    log.debug(f"Nope")

        log.debug(f"Returning {len(tasks)} formalization tasks!")

        return tasks

    def calc_upstream_affected(self, rel_path : str) -> int:
        """ 
        Return the number of models affected by the model with specified 'rel_path'
        """

        if rel_path not in self.models:
            raise Exception (f"Specified model [{rel_path}] is not present!")

        def helper(current_path:str, visited: list[str]):
            """ Our helper function to help us traverse the models """

            for path in self.models:
                if path in visited: continue

                found = False

                for d in self.models[path].dependencies:
                    if current_path == d.rel_path:
                        found = True
                        break

                if found:
                    visited.append(path)
                    visited = helper(path, visited)

            return visited

        return len(helper(rel_path, []))

    def gen_listing(self, category:str="frm_status"):
        """
        Return a sorted list of models by a specified category.

        Possible values are:
        - Formalization Status [value='frm_status'] - formalization status
        - Upstream dependencies [value='upstream'] - number of upstream dependencies
        - Number of opaque functions [value='opaques'] - number of opaque functions
        - Number of failed VGs [value='failed_vgs'] - number of failed verification goals
        """

        supported = ['frm_status', 'upstream', 'opaques', 'failed_vgs']

        # Let's make sure the category is supported first
        if category.lower() not in supported:
            raise Exception(f"Supplied category is not supported: {category}. Possible values are: {supported}")

        stats = {}

        # This should get us the number of models that are ultimatey affected by this model
        for rel_path in self.models:
            upstream = self.calc_upstream_affected(rel_path)
            stats[rel_path] = { 'path': rel_path, 'upstream': upstream }

        for rel_path in self.models:
            modelStats = self.models[rel_path].gen_stats()

            # Let's now append the statistics here
            for key in modelStats:
                stats[rel_path][key] = modelStats[key]

        def compare(s1, s2):
            try:
                if category.lower() == "frm_status":
                    return s1['frm_status'] >= s2['frm_status']
                elif category.lower() == "upstream":
                    return s1['upstream'] >= s2['upstream']
                elif category.lower() == "opaques":
                    return s1['num_opaques'] >= s2['num_opaques']
                else:
                    return s1['failed_vgs'] >= s2['failed_vgs']
            except Exception as e:
                raise Exception (f"Failed to compare model statistcs: {str(e)}")

        return list(sorted(stats.values(), key=cmp_to_key(compare)))

    def abs_path_in_models(self, path:str) -> bool:
        """
        Return True if the specified path in the models
        """
        return self.make_path_relative(path) in self.models

    def make_path_relative(self, path: str) -> str:
        """
        Return True/False if the specified path is relative to the base source code directory
        """
        return str(Path(path).relative_to(self.src_dir_abs_path))

    def get_model_by_path(self, rel_path:str) -> Model|None:
        """
        Returns Model object for specified relative path, None if it's missing
        """

        if rel_path in self.models:
            return self.models[rel_path]
        return None


    def gather_deep_dependencies(self, rel_path:str) -> list[Model]:
        """
        Return list of all "deep" dependencies for the specified relative path
        """

        if rel_path not in self.models: return []

        def rec_helper(curr_model:Model):
            res = []
            for d in curr_model.dependencies:
                res.extend(rec_helper(d) + [d])
            return res

        curr_model = self.models[rel_path]
        return list(set(rec_helper(curr_model) + [curr_model]))

    def gen_consolidated_model (self, rel_path:str) -> Tuple[str, Dict[str,Model]]:
        """
        Generate a single consolidated model from the achnor model specified by (rel_path).    
        """

        if rel_path not in self.models:
            raise Exception (f"Specified model {rel_path} is not a model!")

        # we'll gather the relevant models (subgraph) and then sort it 
        relevant_models : list[Model] = self.gather_deep_dependencies(rel_path)        
        sorted_list : list[Model] = Model.do_topological_sort(relevant_models)

        # now we'll consolidate the code
        iml = ""
        for model in sorted_list:
            iml += f"(* Starting {model.rel_path} *)\n" \
                    + (str(model.iml_code()) if model.iml_code() else "") + \
                    f"\n(* Ending {model.rel_path} *)\n"

        return iml, { m.rel_path:m for m in relevant_models }

    def process_filesystem_event(self, event : FileSystemEvent):
        """
        Note that the provided paths are absolute!
        We receive events that concern both - Python and IML files.
        """

        # Let's figure out if we have a source code file or we have 
        # 

        ext = Path(event.abs_path1).suffix
        if ext == '.py':
            self.process_fs_event_src_code (event)
        elif ext == '.iml':
            self.process_fs_event_iml_code (event)
        else:
            log.warning(f"MetaModel asked to process FS event for unknown extension: {ext}")

    def process_fs_event_iml_code (self, event : FileSystemEvent):
        """
        Process FileSystem event when it's for a model
        """

        if event.action_type in [FileSystemEventType.CREATED, FileSystemEventType.MODIFIED]:
            # Let's first figure out what the Model path would be for this guy
            
            rel_path = self.make_path_relative(event.abs_path1)
            model_path = str(Path(rel_path).with_suffix('.py'))

            if model_path in self.models:
                
                try:
                    with open(event.abs_path1) as infile:
                        imlCode = infile.read()
                except Exception as e:
                    log.error(f"Failed to read IML file: {event.abs_path1}: {e}")
                    return
                
                self.models[model_path].set_iml_model(imlCode, record_time=True)
                self.models[model_path].expected_iml_on_disk = imlCode
                
                log.info(f"Updated IML code for {model_path}")
            else:
                log.info(f"Received IML file for unknown model. Implied model path is: {model_path}")
        else:
            log.info(f"We only support CREATED/MODIFIED FS events for IML models. Got: [{event.action_type}]")

    def process_fs_event_src_code (self, event : FileSystemEvent):
        """
        Process FileSystem event when it's for a source code file
        """

        if event.action_type == FileSystemEventType.CREATED:
            if self.make_path_relative(event.abs_path1) in self.models:
                log.warning(f"Attempting to create a model with a path that already exists!")
                return
            else:
                log.info(f"Creating a model for {event.abs_path1}")

                abs_path = event.abs_path1
                rel_path = self.make_path_relative(abs_path)
                try:
                    with open(abs_path) as infile:
                        srcCode = infile.read()
                except Exception as e:
                    log.error(f"Failed to read contents of the created file {abs_path}")
                    return

                self.models[rel_path] = Model(rel_path=rel_path, src_code=srcCode)
                log.info(f"We've now created a new model for path={rel_path}.")

        elif event.action_type == FileSystemEventType.MODIFIED:
            # A source file has been modified, so we will update our model info
            log.info(f"Processing modified source file: {event.abs_path1}")

            abs_path = event.abs_path1
            rel_path = self.make_path_relative(abs_path)

            try:
                with open(abs_path) as infile:
                    srcCode = infile.read()
            except Exception as e:
                log.error(f"Failed to open a modified file: fullpath={abs_path}; error={str(e)}")
                return

            if rel_path in self.models:
                # Let's now update the model's source code and record when we've done it
                self.models[rel_path].set_src_code(srcCode, True)
                log.info(f"We've now updated source code for model with path=[{abs_path}]")
            else:
                log.info("Modified file does not have a corresponding model. Creating it.")
                self.models[rel_path] = Model(rel_path=rel_path, src_code=srcCode)
                log.info(f"We've now created a new model for path={abs_path}.")
    
        elif event.action_type == FileSystemEventType.DELETED:
            # We need to process a deleted file event
            log.info(f"Processing deleted source file: {event.abs_path1}")
            rel_path = self.make_path_relative(event.abs_path1)
            if rel_path in self.models:
                self.models[rel_path].set_src_code(None)
            else:
                log.error(f"Attempting to process delete event for a non-existent model {event.abs_path1}")

        elif event.action_type == FileSystemEventType.MOVED:
            # We need to process a deleted file event
            log.info(f"Processing a moved file: {event.abs_path1} to {event.abs_path2}")
            rel_path1 = self.make_path_relative(event.abs_path1)
            rel_path2 = self.make_path_relative(event.abs_path2)
            
            if rel_path1 in self.models and rel_path2 not in self.models:
                # self._models[rel_path].setSrcCode(None)
                self.models[rel_path2] = self.models[rel_path1]
                self.models[rel_path2].rel_path = rel_path2
                del self.models[rel_path1]
        else:
            log.error("Something went wrong. We've gotten an unknown event type: {event.action_type}")

    def run_file_sync(self):
        """
        Go through the source code directory and update the models.
        """

        log.info (f"Building FS from {self.src_dir_abs_path}")
        fs = FileSystem.from_disk(Path(self.src_dir_abs_path))

        py_dep = build_py_dep_graph(fs)

        # Let's look for deleted nodes
        model_paths = {str(m.relative_path) for m in py_dep.nx_graph}
        for path in self.models:
            log.info(f"Checking path {path}...")
            if path not in model_paths:
                # This should indicate that the model has since been deleted
                self.models[path].set_src_code(None)

        # Now let's look at new nodes update code for the existing ones
        for node in py_dep.nodes:
            rel_path = str(node.relative_path)
            if rel_path not in self.models:
                log.info (f"Adding model for path {rel_path}")
                model = Model(
                    rel_path=rel_path,
                    src_code=node.content,
                    src_language=self.language,
                )
                self.models[rel_path] = model
                log.info(f"Creating new model with path={node.relative_path}.")
            else:
                log.info(f"Setting source code to existing node={node.relative_path}.")
                self.models[rel_path].set_src_code(node.content)

        # Now let's add the dependencies
        for p1, p2 in py_dep.nx_graph.edges:
            path1, path2 = str(p1.relative_path), str(p2.relative_path)
            if path1 in self.models and path2 in self.models:
                model1 = self.models[path1]
                model2 = self.models[path2]
                if model2 not in model1.dependencies:
                    model1.dependencies.append(model2)

            else:
                errorMsg = f"Attempting to add a dependency that doesn't exist!"
                log.error(errorMsg)
                raise Exception (errorMsg)

        # We should now have our dict with models representing all the files in the
        # directory right now and those that have been deleted!
        log.info("FileSync ran successfully!")

    def apply_sketch(self, sketch:Sketch) -> None:
        """
        Apply sketch back to the MetaModel
        """

        raise NotImplementedError(f"Sketch application is not implemented yet!")

    @staticmethod
    def fromJSON(j : str|dict):
        """
        Return an object from JSON file
        """

        if isinstance(j, str):
            return MetaModel.model_validate_json(j)
        elif isinstance(j, dict):
            return MetaModel.model_validate(j)
        else:
            raise Exception (f"Input must be either a str or a dict!")

    def toJSON(self):
        """
        Return a JSON object
        """
        return self.model_dump_json()
  
    def summary(self):
        """ Return summary of the meta model state """
        allFormStatuses = [
            FormalizationStatus.UNKNOWN,
            FormalizationStatus.TRANSPARENT,
            FormalizationStatus.INADMISSIBLE,
            FormalizationStatus.EXECUTABLE_WITH_APPROXIMATION,
            FormalizationStatus.ADMITTED_WITH_OPAQUENESS
        ]

        frmStatuses = {s: 0 for s in allFormStatuses}
        for model in self.models.values():
            frmStatuses[model.formalization_status()] += 1

        def count(f): return sum(len(f(m)) for m in self.models.values())

        return { "frm_statuses":  frmStatuses,
                 **{label: count(f) for label, f in
                    [("num_models",       lambda _: [None]),
                     ("num_vgs",          lambda m: m.verification_goals()),
                     ("num_opaque_funcs", lambda m: m.opaque_funcs()),
                     ("num_decomps",      lambda m: m.decomps())
                    ]}}

    def rich_summary(self):
        """ Return rich summary of the meta model state """
        from rich.console import Group
        from codelogician.util import flat_map, intersperse

        summary = self.summary()
        def frm_status(status_count):
            status, count = status_count
            return Text.assemble(status.__rich__(), " ", (str(count), "bold"))

        def fmt_countable(label_key):
            label, key = label_key
            return Text.assemble(f"Num. {label}: ", (str(summary[key]), "bold"))

        countables = [
            ("Models",             "num_models"),
            ("Verification goals", "num_vgs"),
            ("Opaque functions",   "num_opaque_funcs"),
            ("Decompositions",     "num_decomps")
        ]
        return Group(
            Text.assemble(*intersperse(" | ", map(fmt_countable, countables))),
            Text.assemble(*intersperse(" | ", map(frm_status, summary['frm_statuses'].items())))
        )

    def __repr__(self):
        """ Return a nice representation """

        metaSummary = self.summary()
        statuses = {s.name: n for s, n in metaSummary["frm_statuses"].items()}

        s  = f"Source file directory: {self.src_dir_abs_path}\n"
        s += f"Number of models: {metaSummary['num_models']}\n"
        s += f"Number of VGs: {metaSummary['num_vgs']}\n"
        s += f"Number of decomps: {metaSummary['num_decomps']}\n"
        s += f"Status breakdown: \n{json.dumps(statuses, indent=4)}"
        s += "\n"
        s += "Model details:\n"

        for path in self.models:
            s += f"Model [path={path}; {self.models[path].str_summary()}]\n"

        return s

    def __rich__ (self):
        """ Return RICH values """
        pretty = Pretty(self.toJSON(), indent_size=2)
        return Panel(pretty, title="Current MetaModel", border_style="green")


class MetaModelUtils:
  """ Some helper functions for reasoning about metamodels """

  @staticmethod
  def modelContentsChanged(mmodel1 : MetaModel, mmodel2 : MetaModel):
    
    if set(mmodel1.models.keys()) != set(mmodel2.models.keys()):
      return True
    
    # TODO Add other conditions, like changes to opaque functions, etc...
    return False
