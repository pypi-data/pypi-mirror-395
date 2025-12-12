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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f2880ec1260>), ('PMI2', <function <lambda> at 0x7f286f5f8d60>), ('PMI3', <function <lambda> at 0x7f286f5f8ea0>), ('NPR1', <function <lambda> at 0x7f286f5f8f40>), ('NPR2', <function <lambda> at 0x7f286f5f8fe0>), ('RadiusOfGyration', <function <lambda> at 0x7f286f5f9080>), ('InertialShapeFactor', <function <lambda> at 0x7f286f5f9120>), ('Eccentricity', <function <lambda> at 0x7f286f5f91c0>), ('Asphericity', <function <lambda> at 0x7f286f5f9260>), ('SpherocityIndex', <function <lambda> at 0x7f286f5f9300>), ('PBF', <function <lambda> at 0x7f286f5f93a0>)]
