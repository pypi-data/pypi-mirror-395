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
descList: list  # value = [('PMI1', <function <lambda> at 0x00000210C8D77AC0>), ('PMI2', <function <lambda> at 0x00000210D0EE05E0>), ('PMI3', <function <lambda> at 0x00000210D0EE0670>), ('NPR1', <function <lambda> at 0x00000210D0EE0700>), ('NPR2', <function <lambda> at 0x00000210D0EE0790>), ('RadiusOfGyration', <function <lambda> at 0x00000210D0EE0820>), ('InertialShapeFactor', <function <lambda> at 0x00000210D0EE08B0>), ('Eccentricity', <function <lambda> at 0x00000210D0EE0940>), ('Asphericity', <function <lambda> at 0x00000210D0EE09D0>), ('SpherocityIndex', <function <lambda> at 0x00000210D0EE0A60>), ('PBF', <function <lambda> at 0x00000210D0EE0AF0>)]
