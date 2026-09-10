import numpy as np
from sidt.core import gf2_rank, affine_sid, locality_lower_bound, domain_collapse_lower_bound, sid_from_count

def test_rank():
    A=np.array([[1,0,1],[0,1,1],[1,1,0]],dtype=np.uint8)
    assert gf2_rank(A)==2
    assert affine_sid(A)==1

def test_full_rank():
    assert affine_sid(np.eye(8,dtype=np.uint8))==0

def test_zero_rank():
    assert affine_sid(np.zeros((3,5),dtype=np.uint8))==5

def test_locality():
    assert locality_lower_bound(10,[{0,1},{1,2},{7}])==6

def test_domain_budget():
    assert domain_collapse_lower_bound(12,[1,1,2,1])==7

def test_sid_count():
    assert sid_from_count(8)==3.0

def test_additivity():
    A=np.array([[1,1,0],[0,1,1]],dtype=np.uint8); B=np.eye(2,dtype=np.uint8)
    C=np.block([[A,np.zeros((2,2),dtype=np.uint8)],[np.zeros((2,3),dtype=np.uint8),B]])
    assert affine_sid(C)==affine_sid(A)+affine_sid(B)
