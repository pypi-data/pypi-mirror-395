"""
Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__: list[str] = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = -1):
    """
    
    Compute all 3D descriptors of a molecule
    
    Arguments:
    - mol: the molecule to work with
    - confId: conformer ID to work with. If not specified the default (-1) is used
    
    Return:
    
    dict
        A dictionary with decriptor names as keys and the descriptor values as values
    
    raises a ValueError 
        If the molecule does not have conformers
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x7f58e0617b00>), ('PMI2', <function <lambda> at 0x7f58e0617ce0>), ('PMI3', <function <lambda> at 0x7f58dc8044a0>), ('NPR1', <function <lambda> at 0x7f58dc804540>), ('NPR2', <function <lambda> at 0x7f58dc8045e0>), ('RadiusOfGyration', <function <lambda> at 0x7f58dc804680>), ('InertialShapeFactor', <function <lambda> at 0x7f58dc804720>), ('Eccentricity', <function <lambda> at 0x7f58dc8047c0>), ('Asphericity', <function <lambda> at 0x7f58dc804860>), ('SpherocityIndex', <function <lambda> at 0x7f58dc804900>), ('PBF', <function <lambda> at 0x7f58dc8049a0>)]
