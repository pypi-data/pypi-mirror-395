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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f1c5175d900>), ('PMI2', <function <lambda> at 0x7f1c40e52e60>), ('PMI3', <function <lambda> at 0x7f1c40e52ef0>), ('NPR1', <function <lambda> at 0x7f1c40e52f80>), ('NPR2', <function <lambda> at 0x7f1c40e53010>), ('RadiusOfGyration', <function <lambda> at 0x7f1c40e530a0>), ('InertialShapeFactor', <function <lambda> at 0x7f1c40e53130>), ('Eccentricity', <function <lambda> at 0x7f1c40e531c0>), ('Asphericity', <function <lambda> at 0x7f1c40e53250>), ('SpherocityIndex', <function <lambda> at 0x7f1c40e532e0>), ('PBF', <function <lambda> at 0x7f1c40e53370>)]
