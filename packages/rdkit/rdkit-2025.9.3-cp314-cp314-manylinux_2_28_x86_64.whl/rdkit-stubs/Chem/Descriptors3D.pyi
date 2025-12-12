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
descList: list  # value = [('PMI1', <function <lambda> at 0x7fdeadfd2090>), ('PMI2', <function <lambda> at 0x7fde9b6d8bf0>), ('PMI3', <function <lambda> at 0x7fde9b6d8ca0>), ('NPR1', <function <lambda> at 0x7fde9b6d8d50>), ('NPR2', <function <lambda> at 0x7fde9b6d8e00>), ('RadiusOfGyration', <function <lambda> at 0x7fde9b6d8eb0>), ('InertialShapeFactor', <function <lambda> at 0x7fde9b6d8f60>), ('Eccentricity', <function <lambda> at 0x7fde9b6d9010>), ('Asphericity', <function <lambda> at 0x7fde9b6d90c0>), ('SpherocityIndex', <function <lambda> at 0x7fde9b6d9170>), ('PBF', <function <lambda> at 0x7fde9b6d9220>)]
