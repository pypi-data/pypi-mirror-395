import copy
import os

import BlackDynamite as BD
import yaml
from BlackDynamite.bd_transactions import _transaction


class RunList:
    def __init__(self, runs):
        self.runs = runs

    def __await__(self):
        async def inner():
            import asyncio

            import transaction

            transaction.commit()

            for r, j in self.runs:
                while r.state != "FINISHED":
                    await asyncio.sleep(2)
                    transaction.commit()

            return self.runs

        return inner().__await__()


class TaskSelectionEval:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()

    def __and__(self, other_foo):
        if not callable(other_foo):
            raise RuntimeError("cannot combine with a not callable object")

        def _eval():
            res1 = self()
            if not res1:
                return False
            res2 = other_foo()
            if not res2:
                return False
            return res1 + res2

        return TaskSelectionEval(_eval)

    def __await__(self):
        async def inner():
            import asyncio

            is_fired = False
            while not is_fired:
                await asyncio.sleep(2)
                is_fired = self.func()
            return is_fired

        return inner().__await__()


class TaskSelection:
    def __init__(self, constraints, selector, base, study):
        self.constraints = constraints
        self.base = base
        self.selector = selector
        self.study = study

    def exec(self):
        selected_runs = self.selector.selectRuns(self.constraints, quiet=True)
        return selected_runs

    def __call__(self):
        return self.exec()

    def __await__(self):
        async def inner():
            import asyncio

            is_fired = False
            while not is_fired:
                await asyncio.sleep(2)
                is_fired = self.exec()
            return is_fired

        return inner().__await__()

    def all(self, *args):
        def _eval():
            selection = self.exec()
            if not len(selection) > 0:
                return False

            for constraints in args:
                all_flag = True

                from BlackDynamite.constraints_zeo import ZEOconstraints

                self.matching_condition = ZEOconstraints(
                    self.base, constraints
                ).getMatchingCondition()

                for objs in selection:
                    if not self.matching_condition(objs):
                        all_flag = False
                        break
                if all_flag:
                    return selection
            return False

        return TaskSelectionEval(_eval)

    def __iter__(self):
        return iter(self.exec())

    def __bool__(self):
        return bool(self.exec())

    def __len__(self):
        return len(self.exec())

    def __getitem__(self, index):
        return self.exec()[index]


class TaskManager:
    def __init__(self, workflow, study):
        self.workflow = workflow
        self.study = study
        self.config = self.workflow.config["task_managers"][self.study]

        if self.config is None:
            self.config = {}
        if "host" in self.config:
            self.host = self.config["host"]
        else:
            self.host = "zeo://" + self.study_dir

        self._base = None
        self.selector = None

        self._default_job_space = {}
        self._default_run_params = {}
        if "job_space" in self.bd_config:
            self._default_job_space = self.bd_config["job_space"]
        if "run_params" in self.bd_config:
            self._default_run_params = self.bd_config["run_params"]

    def connect(self):
        return self.base

    @property
    def base(self):
        if self._base is not None:
            return self._base

        cwd = os.getcwd()
        os.chdir(self.study_dir)
        params = {"study": self.study, "host": self.host}
        self._base = BD.Base(**params)
        # print(self._base.schema)
        os.chdir(cwd)

        BD.singleton_base = self._base
        print(f"connected: to '{self.study}' => {self._base}")
        return self._base

    @property
    def bd_config(self):
        fname = os.path.join(self.study_dir, "bd.yaml")
        with open(fname) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

    @property
    def study_dir(self):
        return os.path.join(self.workflow.directory, self.study)

    @property
    def bd_dir(self):
        return os.path.join(self.study_dir, ".bd")

    def _createRun(self, job, run_params, commit=False):
        myrun = job.base.Run()
        # set the run parameters from the parsed entries
        job.base.prepare(myrun, "run_desc")
        myrun["machine_name"] = "localhost"
        myrun["nproc"] = 1
        myrun["workflow"] = self.workflow.config_path
        myrun.entries.update(run_params)
        cwd = os.getcwd()
        os.chdir(self.study_dir)

        myrun.setExecFile("launch.sh", commit=commit)

        config_files = ["doIt.py"]
        # print(self.bd_config)
        if "config_files" in self.bd_config:
            for f in self.bd_config["config_files"]:
                config_files.append(f)
        myrun.addConfigFiles(config_files, commit=commit)
        os.chdir(cwd)

        # search if the run was already created
        myrun["job_id"] = job.id
        runs = self.base.select([type(myrun)], myrun)
        if len(runs) > 0:
            return runs[0]

        _id = myrun.attachToJob(job, commit=commit)
        myrun = job.base.runs[_id]
        return myrun

    def _createJob(self, job_input, commit=False):
        new_job = self.base.Job()
        for k, v in job_input.items():
            new_job[k] = v

        from BlackDynamite import jobselector

        jselect = jobselector.JobSelector(new_job.base)
        jobs = jselect.selectJobs(new_job, quiet=True)
        # check if already inserted
        if len(jobs) > 0:
            return jobs[0]

        _id = self.base.insert(new_job, commit=commit)
        new_job = self.base.jobs[_id]
        return new_job

    def createTask(self, run_params=None, commit=False, **kwargs):
        import inspect

        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name

        from BlackDynamite.base_zeo import BaseZEO

        BaseZEO.singleton_base = self.base

        if run_params is None:
            run_params = {}

        run_params_ = copy.deepcopy(self._default_run_params)
        for k, v in run_params.items():
            if isinstance(v, dict) and k in run_params_:
                run_params_[k].update(v)
            else:
                run_params_[k] = v

        if self.workflow.run_name is None:
            raise RuntimeError("Cannot create task if the 'run_name' is not specified")

        run_params_["run_name"] = self.workflow.run_name
        run_params_["event_name"] = caller_name

        job_space = self._expandJobSpace(**kwargs)
        runs = self._create_runs_and_jobs(job_space, run_params_, commit=commit)
        return RunList(runs)

    def _expandJobSpace(self, **kwargs):
        desc_job = self.base.get_descriptor("job_desc")
        job_space = copy.deepcopy(self._default_job_space)
        job_space.update(kwargs)
        job_space = self.base._createParameterSpace(job_space, entries_desc=desc_job)
        return job_space

    @_transaction
    def _create_runs_and_jobs(self, job_space, run_params, commit=False):
        created = []
        for job_inputs in job_space:
            j = self._createJob(job_inputs, commit=commit)
            r = self._createRun(j, run_params, commit=commit)
            created.append((r, j))
        return created

    def select(self, constraints=None):
        if isinstance(constraints, str):
            constraints = [constraints]
        if constraints is None:
            constraints = []
        if self.selector is None:
            self.selector = BD.RunSelector(self.base)
        if self.workflow.run_name is not None:
            constraints += [f"run_name = {self.workflow.run_name}"]

        return TaskSelection(constraints, self.selector, self.base, self.study)
