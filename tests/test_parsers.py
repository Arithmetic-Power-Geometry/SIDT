from sidt.parsers import parse_dimacs, parse_fukuoka_gf2

def test_dimacs(tmp_path):
    p=tmp_path/'x.cnf'; p.write_text('c demo\np cnf 3 2\n1 -2 0\n2 3 0\n')
    x=parse_dimacs(p)
    assert x['n']==3 and x['m']==2 and x['supports']==[[0,1],[1,2]]

def test_fukuoka_format(tmp_path):
    p=tmp_path/'x.txt'; p.write_text('Galois Field : GF(2)\nNumber of variables (n) : 2\nNumber of equations (m) : 2\nSeed : 0\n*********************\n1 0 1 0 1 ;\n0 1 0 1 0 ;\n')
    x=parse_fukuoka_gf2(p)
    assert x['n']==2 and x['m']==2 and x['seed']==0
