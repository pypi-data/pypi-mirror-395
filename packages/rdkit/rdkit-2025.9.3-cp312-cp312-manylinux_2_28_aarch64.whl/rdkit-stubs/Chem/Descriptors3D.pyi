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
descList: list  # value = [('PMI1', <function <lambda> at 0xffffa8190ae0>), ('PMI2', <function <lambda> at 0xffffa8191300>), ('PMI3', <function <lambda> at 0xffffa81913a0>), ('NPR1', <function <lambda> at 0xffffa8191440>), ('NPR2', <function <lambda> at 0xffffa81914e0>), ('RadiusOfGyration', <function <lambda> at 0xffffa8191580>), ('InertialShapeFactor', <function <lambda> at 0xffffa8191620>), ('Eccentricity', <function <lambda> at 0xffffa81916c0>), ('Asphericity', <function <lambda> at 0xffffa8191760>), ('SpherocityIndex', <function <lambda> at 0xffffa8191800>), ('PBF', <function <lambda> at 0xffffa81918a0>)]
