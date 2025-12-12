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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001F0227EA980>), ('PMI2', <function <lambda> at 0x000001F0227EB240>), ('PMI3', <function <lambda> at 0x000001F0227EB2E0>), ('NPR1', <function <lambda> at 0x000001F0227EB380>), ('NPR2', <function <lambda> at 0x000001F0227EB420>), ('RadiusOfGyration', <function <lambda> at 0x000001F0227EB4C0>), ('InertialShapeFactor', <function <lambda> at 0x000001F0227EB560>), ('Eccentricity', <function <lambda> at 0x000001F0227EB600>), ('Asphericity', <function <lambda> at 0x000001F0227EB6A0>), ('SpherocityIndex', <function <lambda> at 0x000001F0227EB740>), ('PBF', <function <lambda> at 0x000001F0227EB7E0>)]
