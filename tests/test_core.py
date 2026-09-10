import numpy as np
from sidt.core import gf2_rank, affine_sid, locality_lower_bound, collapse_budget_lower_bound

def test_rank_identity():
    A=np.array([[1,0,1],[0,1,1],[1,1,0]],dtype=np.uint8)
    assert gf2_rank(A)==2
    assert affine_sid(A)==1

def test_full_rank():
    A=np.eye(6,dtype=np.uint8)
    assert affine_sid(A)==0

def test_locality_bound():
    assert locality_lower_bound(8,[{0,1},{1,2},{5}])==4

def test_collapse_budget():
    assert collapse_budget_lower_bound(10,[1,2,1])==6

def test_additivity():
    A=np.array([[1,1,0],[0,1,1]],dtype=np.uint8)
    B=np.array([[1,0],[0,1]],dtype=np.uint8)
    C=np.block([[A,np.zeros((2,2),dtype=np.uint8)],[np.zeros((2,3),dtype=np.uint8),B]])
    assert affine_sid(C)==affine_sid(A)+affine_sid(B)
