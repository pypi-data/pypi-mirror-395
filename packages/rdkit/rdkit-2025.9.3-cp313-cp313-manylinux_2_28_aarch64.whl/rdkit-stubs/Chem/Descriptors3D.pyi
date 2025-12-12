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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff96f57ba0>), ('PMI2', <function <lambda> at 0xffff96f57d80>), ('PMI3', <function <lambda> at 0xffff92f38540>), ('NPR1', <function <lambda> at 0xffff92f385e0>), ('NPR2', <function <lambda> at 0xffff92f38680>), ('RadiusOfGyration', <function <lambda> at 0xffff92f38720>), ('InertialShapeFactor', <function <lambda> at 0xffff92f387c0>), ('Eccentricity', <function <lambda> at 0xffff92f38860>), ('Asphericity', <function <lambda> at 0xffff92f38900>), ('SpherocityIndex', <function <lambda> at 0xffff92f389a0>), ('PBF', <function <lambda> at 0xffff92f38a40>)]
