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

import numpy

################################################################################

def vec_col_to_mat_sym(
        vec,
        mat=None,
        with_sqrt=False):

    if (numpy.size(vec,0) == 3):
        if (mat is None):
            return vec_col3_to_mat_sym22(
                vec=vec,
                with_sqrt=with_sqrt)
        else:
            assert(numpy.size(mat,0) == 2), "Wrong matrix dimension in vec_col_to_mat_sym (mat="+str(mat)+", numpy.size(mat,0)="+str(numpy.size(mat,0))+"). Aborting."
            assert(numpy.size(mat,1) == 2), "Wrong matrix dimension in vec_col_to_mat_sym (mat="+str(mat)+", numpy.size(mat,1)="+str(numpy.size(mat,1))+"). Aborting."
            vec_col3_to_mat_sym22(
                vec=vec,
                mat=mat,
                with_sqrt=with_sqrt)
    elif (numpy.size(vec,0) == 6):
        if (mat is None):
            return vec_col6_to_mat_sym33(
                vec=vec,
                with_sqrt=with_sqrt)
        else:
            assert(numpy.size(mat,0) == 3), "Wrong matrix dimension in vec_col_to_mat_sym (mat="+str(mat)+", numpy.size(mat,0)="+str(numpy.size(mat,0))+"). Aborting."
            assert(numpy.size(mat,1) == 3), "Wrong matrix dimension in vec_col_to_mat_sym (mat="+str(mat)+", numpy.size(mat,1)="+str(numpy.size(mat,1))+"). Aborting."
            vec_col6_to_mat_sym33(
                vec=vec,
                mat=mat,
                with_sqrt=with_sqrt)
    else:
        assert (0), "Wrong vector dimension in vec_col_to_mat_sym (vec="+str(vec)+", numpy.size(vec,0)="+str(numpy.size(vec,0))+"). Aborting."

def vec_col3_to_mat_sym22(
        vec,
        mat=None,
        with_sqrt=False):

    #assert (numpy.size(vec,0) == 3), "Wrong vector dimension in vec_col3_to_mat_sym22 (vec="+str(vec)+", numpy.size(vec,0)="+str(numpy.size(vec,0))+"). Aborting."
    if (mat is None):
        if (with_sqrt):
            return numpy.array([[vec[0]       , vec[2]/2**0.5],
                                [vec[2]/2**0.5, vec[1]       ]])
        else:
            return numpy.array([[vec[0], vec[2]],
                                [vec[2], vec[1]]])
    else:
        #assert(numpy.size(mat,0) == 2), "Wrong matrix dimension in vec_col3_to_mat_sym22 (mat="+str(mat)+", numpy.size(mat,0)="+str(numpy.size(mat,0))+"). Aborting."
        #assert(numpy.size(mat,1) == 2), "Wrong matrix dimension in vec_col3_to_mat_sym22 (mat="+str(mat)+", numpy.size(mat,1)="+str(numpy.size(mat,1))+"). Aborting."
        if (with_sqrt):
            mat[0,0] = vec[0]
            mat[0,1] = vec[2]/2**0.5
            mat[1,0] = vec[2]/2**0.5
            mat[1,1] = vec[1]
        else:
            mat[0,0] = vec[0]
            mat[0,1] = vec[2]
            mat[1,0] = vec[2]
            mat[1,1] = vec[1]

def cvec4_to_mat22(
        vec,
        mat):

    mat[0,0] = vec[0]
    mat[0,1] = vec[1]
    mat[1,0] = vec[2]
    mat[1,1] = vec[3]

def fvec4_to_mat22(
        vec,
        mat):

    mat[0,0] = vec[0]
    mat[1,0] = vec[1]
    mat[0,1] = vec[2]
    mat[1,1] = vec[3]

def vec_col6_to_mat_sym33(
        vec,
        mat=None,
        with_sqrt=False):

    #assert (numpy.size(vec,0) == 6), "Wrong vector dimension in vec_col3_to_mat_sym22 (vec="+str(vec)+", numpy.size(vec,0)="+str(numpy.size(vec,0))+"). Aborting."
    if (mat is None):
        if (with_sqrt):
            return numpy.array([[vec[0]       , vec[3]/2**0.5, vec[4]/2**0.5],
                                [vec[3]/2**0.5, vec[1]       , vec[5]/2**0.5],
                                [vec[4]/2**0.5, vec[5]/2**0.5, vec[2]       ]])
        else:
            return numpy.array([[vec[0], vec[3], vec[4]],
                                [vec[3], vec[1], vec[5]],
                                [vec[4], vec[5], vec[2]]])
    else:
        #assert(numpy.size(mat,0) == 3), "Wrong matrix dimension in vec_col3_to_mat_sym22 (mat="+str(mat)+", numpy.size(mat,0)="+str(numpy.size(mat,0))+"). Aborting."
        #assert(numpy.size(mat,1) == 3), "Wrong matrix dimension in vec_col3_to_mat_sym22 (mat="+str(mat)+", numpy.size(mat,1)="+str(numpy.size(mat,1))+"). Aborting."
        if (with_sqrt):
            mat[0,0] = vec[0]
            mat[0,1] = vec[3]/2**0.5
            mat[0,2] = vec[4]/2**0.5
            mat[1,0] = vec[3]/2**0.5
            mat[1,1] = vec[1]
            mat[1,2] = vec[5]/2**0.5
            mat[2,0] = vec[4]/2**0.5
            mat[2,1] = vec[5]/2**0.5
            mat[2,2] = vec[2]
        else:
            mat[0,0] = vec[0]
            mat[0,1] = vec[3]
            mat[0,2] = vec[4]
            mat[1,0] = vec[3]
            mat[1,1] = vec[1]
            mat[1,2] = vec[5]
            mat[2,0] = vec[4]
            mat[2,1] = vec[5]
            mat[2,2] = vec[2]

def cvec9_to_mat33(
        vec,
        mat):

    mat[0,0] = vec[0]
    mat[0,1] = vec[1]
    mat[0,2] = vec[2]
    mat[1,0] = vec[3]
    mat[1,1] = vec[4]
    mat[1,2] = vec[5]
    mat[2,0] = vec[6]
    mat[2,1] = vec[7]
    mat[2,2] = vec[8]

def fvec9_to_mat33(
        vec,
        mat):

    mat[0,0] = vec[0]
    mat[1,0] = vec[1]
    mat[2,0] = vec[2]
    mat[0,1] = vec[3]
    mat[1,1] = vec[4]
    mat[2,1] = vec[5]
    mat[0,2] = vec[6]
    mat[1,2] = vec[7]
    mat[2,2] = vec[8]

def mat_sym_to_vec_col(
        mat,
        vec=None,
        with_sqrt=False):

    if (numpy.size(mat,0) == 2) and (numpy.size(mat,1) == 2):
        if (vec is None):
            return mat_sym22_to_vec_col3(
                mat=mat,
                with_sqrt=with_sqrt)
        else:
            assert(numpy.size(vec,0) == 3), "Wrong vector dimension in mat_sym_to_vec_col (vec="+str(vec)+", numpy.size(vec,0)="+str(numpy.size(vec,0))+"). Aborting."
            mat_sym22_to_vec_col3(
                mat=mat,
                vec=vec,
                with_sqrt=with_sqrt)
    elif (numpy.size(mat,0) == 3) and (numpy.size(mat,1) == 3):
        if (vec is None):
            return mat_sym33_to_vec_col6(
                mat=mat,
                with_sqrt=with_sqrt)
        else:
            assert(numpy.size(vec,0) == 6), "Wrong vector dimension in mat_sym_to_vec_col (vec="+str(vec)+", numpy.size(vec,0)="+str(numpy.size(vec,0))+"). Aborting."
            mat_sym33_to_vec_col6(
                mat=mat,
                vec=vec,
                with_sqrt=with_sqrt)
    else:
        assert (0), "Wrong matrix dimension in mat_sym_to_vec_col (mat="+str(mat)+", numpy.size(mat,0)="+str(numpy.size(mat,0))+", numpy.size(mat,1)="+str(numpy.size(mat,1))+"). Aborting."

def mat_sym22_to_vec_col3(
        mat,
        vec=None,
        with_sqrt=False):

    if (vec is None):
        if (with_sqrt):
            return numpy.array([mat[0,0], mat[1,1], 2**0.5*mat[0,1]])
        else:
            return numpy.array([mat[0,0], mat[1,1], mat[0,1]])
    else:
        if (with_sqrt):
            vec[0] =        mat[0,0]
            vec[1] =        mat[1,1]
            vec[2] = 2**0.5*mat[0,1]
        else:
            vec[0] = mat[0,0]
            vec[1] = mat[1,1]
            vec[2] = mat[0,1]

def mat22_to_cvec4(
        mat,
        vec):

    vec[0] = mat[0,0]
    vec[1] = mat[0,1]
    vec[2] = mat[1,0]
    vec[3] = mat[1,1]

def fvec4_to_mat22(
        mat,
        vec):

    vec[0] = mat[0,0]
    vec[1] = mat[1,0]
    vec[2] = mat[0,1]
    vec[3] = mat[1,1]

def mat_sym33_to_vec_col6(
        mat,
        vec=None,
        with_sqrt=False):

    if (vec is None):
        if (with_sqrt):
            return numpy.array([mat[0,0], mat[1,1], mat[2,2], 2**0.5*mat[0,1], 2**0.5*mat[0,2], 2**0.5*mat[1,2]])
        else:
            return numpy.array([mat[0,0], mat[1,1], mat[2,2], mat[0,1], mat[0,2], mat[1,2]])
    else:
        if (with_sqrt):
            vec[0] =        mat[0,0]
            vec[1] =        mat[1,1]
            vec[2] =        mat[2,2]
            vec[3] = 2**0.5*mat[0,1]
            vec[4] = 2**0.5*mat[0,2]
            vec[5] = 2**0.5*mat[1,2]
        else:
            vec[0] = mat[0,0]
            vec[1] = mat[1,1]
            vec[2] = mat[2,2]
            vec[3] = mat[0,1]
            vec[4] = mat[0,2]
            vec[5] = mat[1,2]

def mat33_to_cvec9(
        mat,
        vec):

    vec[0] = mat[0,0]
    vec[1] = mat[0,1]
    vec[2] = mat[0,2]
    vec[3] = mat[1,0]
    vec[4] = mat[1,1]
    vec[5] = mat[1,2]
    vec[6] = mat[2,0]
    vec[7] = mat[2,1]
    vec[8] = mat[2,2]

def mat33_to_fvec9(
        mat,
        vec):

    vec[0] = mat[0,0]
    vec[1] = mat[1,0]
    vec[2] = mat[2,0]
    vec[3] = mat[0,1]
    vec[4] = mat[1,1]
    vec[5] = mat[2,1]
    vec[6] = mat[0,2]
    vec[7] = mat[1,2]
    vec[8] = mat[2,2]
