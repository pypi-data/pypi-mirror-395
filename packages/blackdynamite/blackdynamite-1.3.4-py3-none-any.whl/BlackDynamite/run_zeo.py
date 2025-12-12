#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import os
import socket
import subprocess
from functools import reduce

################################################################
import BTrees
################################################################
from deprecated import deprecated

from . import base, bdlogging, bdparser, conffile_zeo, zeoobject
from .base_zeo import _transaction
from .conffile_zeo import ConfFile

################################################################
__all__ = ["RunZEO", "getRunFromScript"]
print = bdlogging.invalidPrint
logger = bdlogging.getLogger(__name__)
BTree = BTrees.OOBTree.BTree
OOSet = BTrees.OOBTree.OOSet

################################################################


class UnknownQuantity(RuntimeError):
    pass


################################################################


class RunZEO(zeoobject.ZEOObject):
    """ """

    def serialize_dict(v):
        import json

        if isinstance(v, dict):
            return json.dumps(v)
        return v

    def get_params(self):
        params = tuple(
            [
                RunZEO.serialize_dict(v)
                for e, v in self.entries.items()
                if (e != "id" and v is not None)
            ]
        )
        return params

    def get_keys(self):
        keys = tuple(
            [e for e, v in self.entries.items() if e != "id" and v is not None]
        )
        return keys

    def getJob(self):
        return self.base.getJobFromID(self.entries["job_id"])

    @_transaction
    def start(self):
        # logger.error(self.entries['state'])
        self.entries["state"] = "START"
        self.start_time = datetime.datetime.now()
        # logger.error(self['state'])
        logger.debug("starting run")

    @_transaction
    def finish(self):
        self.entries["state"] = "FINISHED"
        logger.debug("finish run")

    @_transaction
    def fail(self, state="FAILURE"):
        self.entries["state"] = state
        logger.debug("failed run")

    @_transaction
    def setLaunchState(self, mydir, params):
        if self["state"] != "CREATED":
            return
        self["state"] = "TOBELAUNCHED"
        self["run_path"] = os.path.join(mydir, "run-" + str(self.id))

        from . import __version__ as BD_version

        self["blackdynamite_version"] = BD_version

    @_transaction
    def setContextRequirements(self):
        import importlib.metadata

        requirements = []
        for dist in importlib.metadata.distributions():
            name = dist.metadata["Name"]
            version = dist.version
            requirements.append(f"{name}=={version}")

        # Join as requirements.txt style string
        requirements_txt = "\n".join(sorted(requirements))
        f = conffile_zeo.addFile("requirements.txt", content=requirements_txt)
        self.base.configfiles[f.id] = f
        self["python_requirements"] = f.id

    @_transaction
    def attachToJob(self, job, commit=True):
        self["job_id"] = job.id
        return self.base.insert(self, commit=commit)

    def getExecFile(self):
        conf_exec = self.base.configfiles[self.exec]
        return self.getUpdatedConfigFile(conf_exec)

    @_transaction
    def setExecFile(self, file_name, commit=True):
        # check if the file is already in the config files
        for _id in self.configfiles:
            f = self.base.configfiles[_id]
            if f.filename == file_name:
                self.entries["exec"] = f.id
                return f.id

        # the file is not in the current config files
        # so it has to be added
        _ids = self.addConfigFiles(file_name, commit=commit)
        self.entries["exec"] = _ids[0]
        return _ids[0]

    def annotateHostName(self, host):
        host = self["machine_name"]
        if hasattr(self.base, "bd_conf_files"):
            if host in self.base.bd_conf_files:
                conf = self.base.bd_conf_files[host]
                if "user" in conf:
                    host = conf["user"] + "@" + host
            logger.debug(self.base.bd_conf_files.keys())
        logger.debug(host)
        return host

    def listFiles(self, subdir="", cache=None):
        """List files in run directory / specified sub-directory"""
        command = "ls {0}".format(os.path.join(self["run_path"], subdir))
        if (
            not self["machine_name"] == socket.gethostname()
            and self["machine_name"] != "localhost"
            and cache is None
        ):
            host = self.annotateHostName(self["machine_name"])
            command = f'ssh {host} "{command}"'
        elif cache is not None:
            dest_path = os.path.join(
                cache, "BD-" + self.base.schema + "-cache", f"run-{self.id}"
            )
            command = f"ls {os.path.join(dest_path, subdir)}"
        logger.debug(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        out = [o.strip().decode() for o in out]
        return out

    def getFile(self, filename, cache=None):
        if cache is None:
            cache = self.base.root_dir
        dest_path = os.path.join(
            cache, "BD-" + self.base.schema + "-cache", "run-{0}".format(self.id)
        )
        dest_file = os.path.join(dest_path, filename)

        full_filename = self.getFullFileName(filename)

        # Check if file is local
        if os.path.isfile(full_filename):
            return full_filename

        # If file is distant, prepare cache directory hierarchy
        dest_path = os.path.dirname(dest_file)

        logger.debug("Directories: " + dest_path)
        logger.debug("File: " + dest_file)

        # Making directories
        try:
            os.makedirs(dest_path, exist_ok=True)
        except Exception as e:
            logger.error(e)
            pass

        if os.path.isfile(dest_file):
            logger.debug("File {} already cached".format(dest_file))
            return dest_file

        host = self.annotateHostName(self["machine_name"])

        cmd = "scp {0}:{1} {2}".format(host, self.getFullFileName(filename), dest_file)
        logger.debug(cmd)
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        errors = bytes(p.stderr.read()).decode().strip()
        if errors:
            logger.warning(errors)
        return dest_file

    def getFullFileName(self, filename):
        return os.path.join(self["run_path"], filename)

    @_transaction
    def addConfigFiles(self, file_list, regex_params=None):
        if not isinstance(file_list, list):
            file_list = [file_list]
        params_list = list(self.types.keys())
        myjob = self.base.Job()
        params_list += list(myjob.types.keys())

        files_to_add = [
            conffile_zeo.addFile(fname, regex_params=regex_params, params=params_list)
            for fname in file_list
        ]

        added_files = []
        for f in files_to_add:
            if f.id not in self.configfiles:
                self.configfiles.add(f.id)
                self.base.configfiles[f.id] = f
                added_files.append(f.id)
        return added_files

    def getConfigFiles(self):
        files = [self.base.configfiles[_id] for _id in self.configfiles]

        conffiles = [self.getUpdatedConfigFile(f) for f in files]

        return conffiles

    def getConfigFile(self, file_id):
        return self.configfiles[file_id]

    def getPythonRequirements(self):
        return self.base.configfiles[self.entries["python_requirements"]]

    def replaceBlackDynamiteVariables(self, text):
        myjob = self.base.Job()
        myjob["id"] = self.entries["job_id"]
        myjob = myjob.getMatchedObjectList()[0]

        for key, val in myjob.entries.items():
            tmp = text.replace("__BLACKDYNAMITE__" + key + "__", str(val))
            if (not tmp == text) and val is None:
                raise Exception("unset job parameter " + key)
            text = tmp

        for key, val in self.entries.items():
            tmp = text.replace("__BLACKDYNAMITE__" + key + "__", str(val))
            if (not tmp == text) and val is None:
                logger.debug(self.entries)
                raise Exception("unset run parameter " + key)
            text = tmp

        text = text.replace("__BLACKDYNAMITE__dbhost__", self.base.host)
        text = text.replace("__BLACKDYNAMITE__study__", self.base.schema)
        text = text.replace("__BLACKDYNAMITE__run_id__", str(self.id))
        return text

    def getUpdatedConfigFile(self, conf):
        conf = ConfFile(conf.filename, content=conf.file)
        conf["file"] = self.replaceBlackDynamiteVariables(conf["file"])
        return conf

    def listQuantities(self):
        return self.base.quantities

    def getLastStep(self):
        if "last_step" in self.entries:
            return self.last_step, self.last_step_time
        else:
            return None, None

    def getQuantity(self, name, step=None):
        if name not in self.quantities:
            raise UnknownQuantity(
                f"for run {self}\n"
                f"unknown quantity '{name}'\n"
                "possible quantities are"
                f" {[e for e in self.quantities.keys()]}"
            )
        array = self.getQuantityArrayFromBlob(name)
        if step is None:
            return array

        return array[array["step[int]"] == step]

    def getQuantities(self, names, step=None):
        res = []
        for q in names:
            res.append(self.getQuantity(q))
        import pandas as pd

        array = reduce(
            lambda left, right: pd.merge(left, right, on="step[int]", how="outer"), res
        )
        if step is None:
            return array

        return array[array["step[int]"] == step]

    @zeoobject._transaction
    def saveStepTimeStamp(self, step):
        self.last_step = step
        self.last_step_time = datetime.datetime.now()

    @zeoobject._transaction
    def pushQuantity(self, vals, steps, name, description=None):
        import numpy as np

        quantities = self.base.quantities
        if name not in quantities and description is not None:
            quantities[name] = description
        array_vals = np.array([vals], dtype=object)
        array_steps = np.array(steps, dtype=int)

        if len(array_steps.shape) == 0:
            array_steps = np.array([steps], dtype=int)

        if len(array_steps.shape) != 1:
            raise RuntimeError(
                f"step array can only be a single dimension array {array_steps}"
            )

        logger.debug(array_vals)
        n_steps = len(array_steps)
        for i, vals in enumerate(array_vals):
            if n_steps == 1:
                step = array_steps[0]
            else:
                step = array_steps[i]
            logger.debug([i, vals, step])

            self.saveQuantityArrayToBlob(name, step, vals)
            self.saveStepTimeStamp(step)

    def create_blob(self, name):
        logger.debug(self["run_path"])
        fname = os.path.join(self["run_path"], name + ".csv")
        logger.info(f"create blob {fname}")

        return fname

    def getQuantityBlob(self, name):
        logger.debug(name)
        if name not in self.quantities:
            logger.info(f"create quantity {name}")
            self.quantities[name] = self.create_blob(name)
        logger.debug(self.quantities[name])
        return self.quantities[name]

    def getQuantityArrayFromBlob(self, name):
        fname = self.getQuantityBlob(name)
        ext = os.path.splitext(fname)[1]
        import pandas as pd

        if ext == ".csv":
            _f = pd.read_csv(fname)
        else:
            raise RuntimeError(f"unknown extension: {fname} => {ext}")
        return _f

    def saveQuantityArrayToBlob(self, name, step, array_val):
        import numpy as np

        array_val = np.array(array_val)
        fname = self.getQuantityBlob(name)
        if not os.path.exists(fname):
            with open(fname, "w") as _f:
                _f.write("step[int]")
                n_qs = len(array_val.flatten())
                for i, v in enumerate(array_val.flatten()):
                    if isinstance(v, str):
                        try:
                            v = float(v)
                        except ValueError:
                            pass
                    if n_qs > 1:
                        _f.write(f",{name}-{i}[{type(v).__name__}]")
                    else:
                        _f.write(f",{name}[{type(v).__name__}]")

                _f.write("\n")

        with open(fname, "a") as _f:
            _f.write(f"{step}")
            for v in array_val.flatten():
                logger.debug([fname, v])
                if isinstance(v, str):
                    try:
                        v = float(v)
                    except ValueError:
                        _f.write(f",{v}")
                else:
                    _f.write(f",{v:.15e}")

            _f.write("\n")
            _f.flush()

    @_transaction
    def delete(self):
        job_id = self["job_id"]
        job = self.base.jobs[job_id]
        del job.runs[self.id]
        del self.base.runs[self.id]

    @_transaction
    def deleteData(self):
        del self.quantities
        self.quantities = BTree()

    def __init__(self):
        super().__init__()
        self.configfiles = OOSet()
        self.quantities = BTree()
        # logger.error(self.quantities)
        self.base.prepare(self, "run_desc")
        self["id"] = None
        self.types["id"] = int
        self.types["machine_name"] = str
        self.types["run_path"] = str
        self.allowNull["run_path"] = True
        self.types["job_id"] = int
        self.types["nproc"] = int
        self.types["run_name"] = str
        self.types["start_time"] = datetime.datetime
        self.allowNull["start_time"] = True
        self.types["state"] = str
        self.allowNull["state"] = True
        self.types["exec"] = str
        self.types["last_step"] = int
        self.types["last_step_time"] = datetime.datetime

        self["last_step"] = None
        self["last_step_time"] = None
        self["start_time"] = None

    # deprecated
    @deprecated("use getQuantity(name, step=None) instead")
    def getScalarQuantity(self, name, step=None):
        return self.getQuantity(name, step)

    @deprecated("use getQuantity(name, step=None) instead")
    def getVectorQuantity(self, name, step=None):
        return self.getQuantity(name, step)

    @deprecated("use getQuantities(names, step=None) instead")
    def getScalarQuantities(self, names, step=None):
        return self.getQuantities(names, step)

    @deprecated("use getQuantity(names, step=None) instead")
    def getVectorQuantities(self, names, step=None):
        return self.getQuantities(names, step)

    @deprecated("use pushQuantity(vals, step, name, description) instead")
    def pushVectorQuantity(self, vals, step, name, description=None):
        self.pushQuantity(vals, step, name, description)

    @deprecated("use pushQuantity(vals, step, name, description) instead")
    def pushScalarQuantity(self, val, step, name, description=None):
        self.pushQuantity(val, step, name, description)

    @deprecated("use pushQuantity(vals, steps, name, description) instead")
    def pushScalarQuantities(self, vals, steps, name, description=None):
        self.pushQuantity(vals, steps, name, description)


################################################################


def getRunFromScript():
    from .base_zeo import BaseZEO

    if BaseZEO.singleton_base is not None:
        mybase = BaseZEO.singleton_base
    else:
        parser = bdparser.BDParser()
        group = parser.register_group("getRunFromScript")
        group.add_argument("--run_id", type=int)
        params = parser.parseBDParameters(argv=[])
        mybase = base.Base(**params)
    myrun = mybase.runs[params["run_id"]]
    myjob = mybase.jobs[myrun.job_id]

    while myrun.state == "CREATED" or myrun.state == "TOBELAUNCHED":
        import time

        time.sleep(0.1)
    return myrun, myjob
