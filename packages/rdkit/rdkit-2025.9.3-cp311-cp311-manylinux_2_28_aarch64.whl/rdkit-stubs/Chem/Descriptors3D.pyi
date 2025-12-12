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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff976391c0>), ('PMI2', <function <lambda> at 0xffff8816cd60>), ('PMI3', <function <lambda> at 0xffff8816cea0>), ('NPR1', <function <lambda> at 0xffff8816cf40>), ('NPR2', <function <lambda> at 0xffff8816cfe0>), ('RadiusOfGyration', <function <lambda> at 0xffff8816d080>), ('InertialShapeFactor', <function <lambda> at 0xffff8816d120>), ('Eccentricity', <function <lambda> at 0xffff8816d1c0>), ('Asphericity', <function <lambda> at 0xffff8816d260>), ('SpherocityIndex', <function <lambda> at 0xffff8816d300>), ('PBF', <function <lambda> at 0xffff8816d3a0>)]
