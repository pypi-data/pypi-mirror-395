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

import filecmp
import numpy
import os
import shutil
import sys

################################################################################

class Test():
    
    def __init__(self,
        res_folder,
        perform_tests=1,
        tester="numpy",
        tester_numpy_tolerance=1e-3,
        stop_at_failure=1,
        clean_after_tests=1,
        ref_suffix="-ref",
        qois_suffix="-qois",
        qois_ext=".dat"):

        self.res_folder    = res_folder
        self.perform_tests = perform_tests
        if (tester == "numpy"):
            self.tester = self.numpy
        elif (tester == "filecmp"):
            self.tester = self.filecmp
        else:
            assert (0),\
                "tester should be numpy or filecmp. Aborting."
        self.tester_numpy_tolerance = tester_numpy_tolerance
        self.stop_at_failure        = stop_at_failure
        self.clean_after_tests      = clean_after_tests
        self.ref_suffix             = ref_suffix
        self.qois_suffix            = qois_suffix
        self.qois_ext               = qois_ext
        self.success                = True

        shutil.rmtree(self.res_folder, ignore_errors=1)
        os.mkdir(self.res_folder)

    def __del__(self):
        if (self.clean_after_tests) and (self.success):
            shutil.rmtree(self.res_folder, ignore_errors=1)

    def test(self, res_basename):
        if (self.perform_tests):
            res_filename = self.res_folder                +"/"+res_basename+self.qois_suffix+self.qois_ext
            ref_filename = self.res_folder+self.ref_suffix+"/"+res_basename+self.qois_suffix+self.qois_ext
            self.success = self.tester(res_filename, ref_filename)
            if not (self.success):
                print ("Result in "+res_filename+" (\n"+open(res_filename).read()+") "+\
                       "does not correspond to "+\
                       "reference in "+ref_filename+" (\n"+open(ref_filename).read()+").")
                if (self.stop_at_failure):
                    print ("Aborting.")
                    sys.exit(1)

    def filecmp(self, res_filename, ref_filename):
        return filecmp.cmp(res_filename, ref_filename)

    def numpy(self, res_filename, ref_filename):
        res_array = numpy.loadtxt(res_filename)[-1,:]
        # print (res_array)
        ref_array = numpy.loadtxt(ref_filename)[-1,:]
        # print (ref_array)
        if (res_array.shape != ref_array.shape):
            return False
        if (numpy.linalg.norm(ref_array) > 1e-6):
            error = numpy.linalg.norm(res_array-ref_array)/numpy.linalg.norm(ref_array)
        else:
            error = numpy.linalg.norm(res_array-ref_array)
        # print (error)
        return (error<self.tester_numpy_tolerance)
