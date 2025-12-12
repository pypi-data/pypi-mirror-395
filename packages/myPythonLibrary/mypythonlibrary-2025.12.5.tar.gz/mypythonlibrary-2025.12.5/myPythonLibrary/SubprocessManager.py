#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2012-2025                                       ###
###                                                                          ###
### University of California at San Francisco (UCSF), USA                    ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland         ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import os
import socket
import subprocess
import time

import myPythonLibrary as mypy

################################################################################

class SubprocessManager():
    def __init__(self,
            hostname           : str = None,
            n_subprocesses_max : int = None):

        if (hostname is not None):
            self.hostname = hostname
        else:
            self.hostname = socket.gethostname()

        if (n_subprocesses_max is not None):
            self.n_subprocesses_max = n_subprocesses_max
        else:
            self.n_subprocesses_max = os.cpu_count()

        self.processes = []

    def get_n_active_processes(self):
        # for process in self.processes: print (process.poll())
        return sum(process.poll() is None for process in self.processes)

    def wait_for_available_process(self):
        print ("n_slurm_processes_cur:", self.get_n_active_processes())
        while (self.get_n_active_processes() >= self.n_subprocesses_max):
            time.sleep(1)
            print ("n_slurm_processes_cur:", self.get_n_active_processes())

    def wait_for_finished_processes(self):
        print ("n_slurm_processes_cur:", self.get_n_active_processes())
        while (self.get_n_active_processes() > 0):
            time.sleep(1)
            print ("n_slurm_processes_cur:", self.get_n_active_processes())

    def start_new_process(self, command_lst, stdout_filename = None):
        if (stdout_filename is not None):
            stdout = open(stdout_filename, mode="w", buffering=1) # MG20221007: Otherwise buffer is not always emptied…
        else:
            stdout = subprocess.DEVNULL

        process = subprocess.Popen(command_lst, stdout=stdout, stderr=subprocess.STDOUT)
        self.processes.append(process)

    def start_new_process_when_available(self, *args, **kwargs):
        self.wait_for_available_process()
        self.start_new_process(*args, **kwargs)

################################################################################
 
class TasksManager():
    def __init__(self,
            use_subprocesses : bool = False,
            **kwargs):

        self.use_subprocesses = use_subprocesses

        if (self.use_subprocesses):
            self.subprocess_manager = mypy.SubprocessManager(**kwargs)

    def wait_for_available_task(self):
        if (self.use_subprocesses):
            self.subprocess_manager.wait_for_available_process()

    def wait_for_finished_tasks(self):
        if (self.use_subprocesses):
            self.subprocess_manager.wait_for_finished_processes()

    def run_task(self, function_name, arguments_dict, stdout_filename=None):
        if (self.use_subprocesses):
            command_lst  = []
            command_lst += ["python", function_name+".py"]
            command_lst += [item for key, value in arguments_dict.items() for item in ("--"+key, str(value).replace(" ", ""))]
            print (command_lst)

            self.subprocess_manager.start_new_process(
                command_lst     = command_lst,
                stdout_filename = stdout_filename)
        else:
            print (locals())
            print (globals())
            globals()[function_name](**arguments_dict)

    def run_task_when_available(self, *args, **kwargs):
        self.wait_for_available_task()
        self.run_task(*args, **kwargs)
