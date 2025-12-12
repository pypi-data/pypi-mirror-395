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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002C7E728AAE0>), ('PMI2', <function <lambda> at 0x000002C7E728B060>), ('PMI3', <function <lambda> at 0x000002C7E728B110>), ('NPR1', <function <lambda> at 0x000002C7E728B1C0>), ('NPR2', <function <lambda> at 0x000002C7E728B270>), ('RadiusOfGyration', <function <lambda> at 0x000002C7E728B320>), ('InertialShapeFactor', <function <lambda> at 0x000002C7E728B3D0>), ('Eccentricity', <function <lambda> at 0x000002C7E728B480>), ('Asphericity', <function <lambda> at 0x000002C7E728B530>), ('SpherocityIndex', <function <lambda> at 0x000002C7E728B5E0>), ('PBF', <function <lambda> at 0x000002C7E728B690>)]
