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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f1e9cbf0a40>), ('PMI2', <function <lambda> at 0x7f1e9cbf1260>), ('PMI3', <function <lambda> at 0x7f1e9cbf1300>), ('NPR1', <function <lambda> at 0x7f1e9cbf13a0>), ('NPR2', <function <lambda> at 0x7f1e9cbf1440>), ('RadiusOfGyration', <function <lambda> at 0x7f1e9cbf14e0>), ('InertialShapeFactor', <function <lambda> at 0x7f1e9cbf1580>), ('Eccentricity', <function <lambda> at 0x7f1e9cbf1620>), ('Asphericity', <function <lambda> at 0x7f1e9cbf16c0>), ('SpherocityIndex', <function <lambda> at 0x7f1e9cbf1760>), ('PBF', <function <lambda> at 0x7f1e9cbf1800>)]
