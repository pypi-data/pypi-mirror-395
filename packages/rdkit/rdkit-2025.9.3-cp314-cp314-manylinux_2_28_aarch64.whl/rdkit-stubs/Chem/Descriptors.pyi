from __future__ import annotations
from collections import abc
from rdkit import Chem
from rdkit.Chem.ChemUtils import DescriptorUtilities as _du
import rdkit.Chem.ChemUtils.DescriptorUtilities
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_1
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_10
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_100
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_101
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_102
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_103
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_104
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_105
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_106
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_107
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_108
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_109
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_11
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_110
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_111
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_112
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_113
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_114
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_115
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_116
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_117
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_118
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_119
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_12
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_120
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_121
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_122
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_123
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_124
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_125
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_126
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_127
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_128
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_129
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_13
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_130
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_131
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_132
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_133
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_134
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_135
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_136
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_137
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_138
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_139
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_14
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_140
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_141
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_142
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_143
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_144
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_145
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_146
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_147
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_148
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_149
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_15
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_150
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_151
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_152
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_153
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_154
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_155
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_156
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_157
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_158
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_159
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_16
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_160
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_161
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_162
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_163
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_164
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_165
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_166
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_167
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_168
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_169
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_17
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_170
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_171
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_172
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_173
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_174
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_175
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_176
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_177
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_178
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_179
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_18
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_180
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_181
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_182
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_183
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_184
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_185
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_186
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_187
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_188
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_189
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_19
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_190
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_191
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_192
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_2
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_20
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_21
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_22
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_23
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_24
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_25
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_26
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_27
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_28
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_29
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_3
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_30
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_31
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_32
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_33
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_34
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_35
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_36
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_37
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_38
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_39
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_4
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_40
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_41
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_42
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_43
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_44
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_45
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_46
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_47
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_48
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_49
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_5
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_50
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_51
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_52
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_53
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_54
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_55
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_56
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_57
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_58
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_59
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_6
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_60
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_61
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_62
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_63
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_64
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_65
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_66
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_67
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_68
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_69
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_7
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_70
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_71
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_72
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_73
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_74
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_75
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_76
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_77
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_78
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_79
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_8
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_80
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_81
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_82
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_83
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_84
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_85
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_86
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_87
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_88
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_89
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_9
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_90
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_91
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_92
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_93
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_94
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_95
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_96
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_97
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_98
from rdkit.Chem.ChemUtils.DescriptorUtilities import AUTOCORR2D_99
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_CHGHI
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_CHGLO
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_LOGPHI
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_LOGPLOW
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MRHI
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MRLOW
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MWHI
from rdkit.Chem.ChemUtils.DescriptorUtilities import BCUT2D_MWLOW
import rdkit.Chem.EState.EState
from rdkit.Chem.EState.EState import MaxAbsEStateIndex
from rdkit.Chem.EState.EState import MaxEStateIndex
from rdkit.Chem.EState.EState import MinAbsEStateIndex
from rdkit.Chem.EState.EState import MinEStateIndex
import rdkit.Chem.EState.EState_VSA
from rdkit.Chem.EState.EState_VSA import EState_VSA1
from rdkit.Chem.EState.EState_VSA import EState_VSA10
from rdkit.Chem.EState.EState_VSA import EState_VSA11
from rdkit.Chem.EState.EState_VSA import EState_VSA2
from rdkit.Chem.EState.EState_VSA import EState_VSA3
from rdkit.Chem.EState.EState_VSA import EState_VSA4
from rdkit.Chem.EState.EState_VSA import EState_VSA5
from rdkit.Chem.EState.EState_VSA import EState_VSA6
from rdkit.Chem.EState.EState_VSA import EState_VSA7
from rdkit.Chem.EState.EState_VSA import EState_VSA8
from rdkit.Chem.EState.EState_VSA import EState_VSA9
import rdkit.Chem.GraphDescriptors
from rdkit.Chem.GraphDescriptors import AvgIpc
from rdkit.Chem.GraphDescriptors import BalabanJ
from rdkit.Chem.GraphDescriptors import BertzCT
from rdkit.Chem.GraphDescriptors import Chi0
from rdkit.Chem.GraphDescriptors import Chi1
from rdkit.Chem.GraphDescriptors import Ipc
import rdkit.Chem.Lipinski
from rdkit.Chem.Lipinski import HeavyAtomCount
import rdkit.Chem.QED
from rdkit.Chem.QED import qed
import rdkit.Chem.SpacialScore
from rdkit.Chem.SpacialScore import SPS
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem import rdMolDescriptors as _rdMolDescriptors
from rdkit.Chem import rdMolDescriptors
import rdkit.Chem.rdMolDescriptors
from rdkit.Chem import rdPartialCharges
__all__: list[str] = ['AUTOCORR2D_1', 'AUTOCORR2D_10', 'AUTOCORR2D_100', 'AUTOCORR2D_101', 'AUTOCORR2D_102', 'AUTOCORR2D_103', 'AUTOCORR2D_104', 'AUTOCORR2D_105', 'AUTOCORR2D_106', 'AUTOCORR2D_107', 'AUTOCORR2D_108', 'AUTOCORR2D_109', 'AUTOCORR2D_11', 'AUTOCORR2D_110', 'AUTOCORR2D_111', 'AUTOCORR2D_112', 'AUTOCORR2D_113', 'AUTOCORR2D_114', 'AUTOCORR2D_115', 'AUTOCORR2D_116', 'AUTOCORR2D_117', 'AUTOCORR2D_118', 'AUTOCORR2D_119', 'AUTOCORR2D_12', 'AUTOCORR2D_120', 'AUTOCORR2D_121', 'AUTOCORR2D_122', 'AUTOCORR2D_123', 'AUTOCORR2D_124', 'AUTOCORR2D_125', 'AUTOCORR2D_126', 'AUTOCORR2D_127', 'AUTOCORR2D_128', 'AUTOCORR2D_129', 'AUTOCORR2D_13', 'AUTOCORR2D_130', 'AUTOCORR2D_131', 'AUTOCORR2D_132', 'AUTOCORR2D_133', 'AUTOCORR2D_134', 'AUTOCORR2D_135', 'AUTOCORR2D_136', 'AUTOCORR2D_137', 'AUTOCORR2D_138', 'AUTOCORR2D_139', 'AUTOCORR2D_14', 'AUTOCORR2D_140', 'AUTOCORR2D_141', 'AUTOCORR2D_142', 'AUTOCORR2D_143', 'AUTOCORR2D_144', 'AUTOCORR2D_145', 'AUTOCORR2D_146', 'AUTOCORR2D_147', 'AUTOCORR2D_148', 'AUTOCORR2D_149', 'AUTOCORR2D_15', 'AUTOCORR2D_150', 'AUTOCORR2D_151', 'AUTOCORR2D_152', 'AUTOCORR2D_153', 'AUTOCORR2D_154', 'AUTOCORR2D_155', 'AUTOCORR2D_156', 'AUTOCORR2D_157', 'AUTOCORR2D_158', 'AUTOCORR2D_159', 'AUTOCORR2D_16', 'AUTOCORR2D_160', 'AUTOCORR2D_161', 'AUTOCORR2D_162', 'AUTOCORR2D_163', 'AUTOCORR2D_164', 'AUTOCORR2D_165', 'AUTOCORR2D_166', 'AUTOCORR2D_167', 'AUTOCORR2D_168', 'AUTOCORR2D_169', 'AUTOCORR2D_17', 'AUTOCORR2D_170', 'AUTOCORR2D_171', 'AUTOCORR2D_172', 'AUTOCORR2D_173', 'AUTOCORR2D_174', 'AUTOCORR2D_175', 'AUTOCORR2D_176', 'AUTOCORR2D_177', 'AUTOCORR2D_178', 'AUTOCORR2D_179', 'AUTOCORR2D_18', 'AUTOCORR2D_180', 'AUTOCORR2D_181', 'AUTOCORR2D_182', 'AUTOCORR2D_183', 'AUTOCORR2D_184', 'AUTOCORR2D_185', 'AUTOCORR2D_186', 'AUTOCORR2D_187', 'AUTOCORR2D_188', 'AUTOCORR2D_189', 'AUTOCORR2D_19', 'AUTOCORR2D_190', 'AUTOCORR2D_191', 'AUTOCORR2D_192', 'AUTOCORR2D_2', 'AUTOCORR2D_20', 'AUTOCORR2D_21', 'AUTOCORR2D_22', 'AUTOCORR2D_23', 'AUTOCORR2D_24', 'AUTOCORR2D_25', 'AUTOCORR2D_26', 'AUTOCORR2D_27', 'AUTOCORR2D_28', 'AUTOCORR2D_29', 'AUTOCORR2D_3', 'AUTOCORR2D_30', 'AUTOCORR2D_31', 'AUTOCORR2D_32', 'AUTOCORR2D_33', 'AUTOCORR2D_34', 'AUTOCORR2D_35', 'AUTOCORR2D_36', 'AUTOCORR2D_37', 'AUTOCORR2D_38', 'AUTOCORR2D_39', 'AUTOCORR2D_4', 'AUTOCORR2D_40', 'AUTOCORR2D_41', 'AUTOCORR2D_42', 'AUTOCORR2D_43', 'AUTOCORR2D_44', 'AUTOCORR2D_45', 'AUTOCORR2D_46', 'AUTOCORR2D_47', 'AUTOCORR2D_48', 'AUTOCORR2D_49', 'AUTOCORR2D_5', 'AUTOCORR2D_50', 'AUTOCORR2D_51', 'AUTOCORR2D_52', 'AUTOCORR2D_53', 'AUTOCORR2D_54', 'AUTOCORR2D_55', 'AUTOCORR2D_56', 'AUTOCORR2D_57', 'AUTOCORR2D_58', 'AUTOCORR2D_59', 'AUTOCORR2D_6', 'AUTOCORR2D_60', 'AUTOCORR2D_61', 'AUTOCORR2D_62', 'AUTOCORR2D_63', 'AUTOCORR2D_64', 'AUTOCORR2D_65', 'AUTOCORR2D_66', 'AUTOCORR2D_67', 'AUTOCORR2D_68', 'AUTOCORR2D_69', 'AUTOCORR2D_7', 'AUTOCORR2D_70', 'AUTOCORR2D_71', 'AUTOCORR2D_72', 'AUTOCORR2D_73', 'AUTOCORR2D_74', 'AUTOCORR2D_75', 'AUTOCORR2D_76', 'AUTOCORR2D_77', 'AUTOCORR2D_78', 'AUTOCORR2D_79', 'AUTOCORR2D_8', 'AUTOCORR2D_80', 'AUTOCORR2D_81', 'AUTOCORR2D_82', 'AUTOCORR2D_83', 'AUTOCORR2D_84', 'AUTOCORR2D_85', 'AUTOCORR2D_86', 'AUTOCORR2D_87', 'AUTOCORR2D_88', 'AUTOCORR2D_89', 'AUTOCORR2D_9', 'AUTOCORR2D_90', 'AUTOCORR2D_91', 'AUTOCORR2D_92', 'AUTOCORR2D_93', 'AUTOCORR2D_94', 'AUTOCORR2D_95', 'AUTOCORR2D_96', 'AUTOCORR2D_97', 'AUTOCORR2D_98', 'AUTOCORR2D_99', 'AvgIpc', 'BCUT2D_CHGHI', 'BCUT2D_CHGLO', 'BCUT2D_LOGPHI', 'BCUT2D_LOGPLOW', 'BCUT2D_MRHI', 'BCUT2D_MRLOW', 'BCUT2D_MWHI', 'BCUT2D_MWLOW', 'BalabanJ', 'BertzCT', 'CalcMolDescriptors', 'Chem', 'Chi0', 'Chi1', 'EState_VSA1', 'EState_VSA10', 'EState_VSA11', 'EState_VSA2', 'EState_VSA3', 'EState_VSA4', 'EState_VSA5', 'EState_VSA6', 'EState_VSA7', 'EState_VSA8', 'EState_VSA9', 'FpDensityMorgan1', 'FpDensityMorgan2', 'FpDensityMorgan3', 'HeavyAtomCount', 'HeavyAtomMolWt', 'Ipc', 'MaxAbsEStateIndex', 'MaxAbsPartialCharge', 'MaxEStateIndex', 'MaxPartialCharge', 'MinAbsEStateIndex', 'MinAbsPartialCharge', 'MinEStateIndex', 'MinPartialCharge', 'NumRadicalElectrons', 'NumValenceElectrons', 'PropertyFunctor', 'SPS', 'abc', 'autocorr', 'descList', 'names', 'qed', 'rdFingerprintGenerator', 'rdMolDescriptors', 'rdPartialCharges', 'setupAUTOCorrDescriptors']
class PropertyFunctor(rdkit.Chem.rdMolDescriptors.PythonPropertyFunctor):
    """
    Creates a python based property function that can be added to the
    global property list.  To use, subclass this class and override the
    __call__ method.  Then create an instance and add it to the
    registry.  The __call__ method should return a numeric value.
    
    Example:
    
      class NumAtoms(Descriptors.PropertyFunctor):
        def __init__(self):
          Descriptors.PropertyFunctor.__init__(self, "NumAtoms", "1.0.0")
        def __call__(self, mol):
          return mol.GetNumAtoms()
    
      numAtoms = NumAtoms()
      rdMolDescriptors.Properties.RegisterProperty(numAtoms)
    """
    def __call__(self, mol):
        ...
    def __init__(self, name, version):
        ...
def CalcMolDescriptors(mol, missingVal = None, silent = True):
    """
    calculate the full set of descriptors for a molecule
    
    Parameters
    ----------
    mol : RDKit molecule
    missingVal : float, optional
                 This will be used if a particular descriptor cannot be calculated
    silent : bool, optional
             if True then exception messages from descriptors will be displayed
    
    Returns
    -------
    dict 
         A dictionary with decriptor names as keys and the descriptor values as values
    """
def FpDensityMorgan1(x):
    ...
def FpDensityMorgan2(x):
    ...
def FpDensityMorgan3(x):
    ...
def HeavyAtomMolWt(x):
    """
    The average molecular weight of the molecule ignoring hydrogens
    
      >>> HeavyAtomMolWt(Chem.MolFromSmiles('CC'))
      24.02...
      >>> HeavyAtomMolWt(Chem.MolFromSmiles('[NH4+].[Cl-]'))
      49.46
    
    """
def MaxAbsPartialCharge(mol, force = False):
    ...
def MaxPartialCharge(mol, force = False):
    ...
def MinAbsPartialCharge(mol, force = False):
    ...
def MinPartialCharge(mol, force = False):
    ...
def NumRadicalElectrons(mol):
    """
    The number of radical electrons the molecule has
      (says nothing about spin state)
    
    >>> NumRadicalElectrons(Chem.MolFromSmiles('CC'))
    0
    >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH3]'))
    0
    >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH2]'))
    1
    >>> NumRadicalElectrons(Chem.MolFromSmiles('C[CH]'))
    2
    >>> NumRadicalElectrons(Chem.MolFromSmiles('C[C]'))
    3
    
    """
def NumValenceElectrons(mol):
    """
    The number of valence electrons the molecule has
    
    >>> NumValenceElectrons(Chem.MolFromSmiles('CC'))
    14
    >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)O'))
    18
    >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)[O-]'))
    18
    >>> NumValenceElectrons(Chem.MolFromSmiles('C(=O)'))
    12
    
    """
def _ChargeDescriptors(mol, force = False):
    ...
def _FingerprintDensity(mol, func, *args, **kwargs):
    ...
def _getMorganCountFingerprint(mol, radius):
    ...
def _isCallable(thing):
    ...
def _runDoctests(verbose = None):
    ...
def _setupDescriptors(namespace):
    ...
def setupAUTOCorrDescriptors():
    """
    Adds AUTOCORR descriptors to the default descriptor lists
    """
_descList: list  # value = [('MaxAbsEStateIndex', rdkit.Chem.EState.EState.MaxAbsEStateIndex), ('MaxEStateIndex', rdkit.Chem.EState.EState.MaxEStateIndex), ('MinAbsEStateIndex', rdkit.Chem.EState.EState.MinAbsEStateIndex), ('MinEStateIndex', rdkit.Chem.EState.EState.MinEStateIndex), ('qed', rdkit.Chem.QED.qed), ('SPS', rdkit.Chem.SpacialScore.SPS), ('MolWt', <function <lambda> at 0xffff846992d0>), ('HeavyAtomMolWt', HeavyAtomMolWt), ('ExactMolWt', <function <lambda> at 0xffff84699bc0>), ('NumValenceElectrons', NumValenceElectrons), ('NumRadicalElectrons', NumRadicalElectrons), ('MaxPartialCharge', MaxPartialCharge), ('MinPartialCharge', MinPartialCharge), ('MaxAbsPartialCharge', MaxAbsPartialCharge), ('MinAbsPartialCharge', MinAbsPartialCharge), ('FpDensityMorgan1', FpDensityMorgan1), ('FpDensityMorgan2', FpDensityMorgan2), ('FpDensityMorgan3', FpDensityMorgan3), ('BCUT2D_MWHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWHI), ('BCUT2D_MWLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWLOW), ('BCUT2D_CHGHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGHI), ('BCUT2D_CHGLO', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGLO), ('BCUT2D_LOGPHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPHI), ('BCUT2D_LOGPLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPLOW), ('BCUT2D_MRHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRHI), ('BCUT2D_MRLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRLOW), ('AvgIpc', rdkit.Chem.GraphDescriptors.AvgIpc), ('BalabanJ', rdkit.Chem.GraphDescriptors.BalabanJ), ('BertzCT', rdkit.Chem.GraphDescriptors.BertzCT), ('Chi0', rdkit.Chem.GraphDescriptors.Chi0), ('Chi0n', <function <lambda> at 0xffff846bd430>), ('Chi0v', <function <lambda> at 0xffff846bd010>), ('Chi1', rdkit.Chem.GraphDescriptors.Chi1), ('Chi1n', <function <lambda> at 0xffff846bd4e0>), ('Chi1v', <function <lambda> at 0xffff846bd0c0>), ('Chi2n', <function <lambda> at 0xffff846bd590>), ('Chi2v', <function <lambda> at 0xffff846bd170>), ('Chi3n', <function <lambda> at 0xffff846bd640>), ('Chi3v', <function <lambda> at 0xffff846bd220>), ('Chi4n', <function <lambda> at 0xffff846bd6f0>), ('Chi4v', <function <lambda> at 0xffff846bd2d0>), ('HallKierAlpha', <function <lambda> at 0xffff846bc250>), ('Ipc', rdkit.Chem.GraphDescriptors.Ipc), ('Kappa1', <function <lambda> at 0xffff846bc300>), ('Kappa2', <function <lambda> at 0xffff846bc3b0>), ('Kappa3', <function <lambda> at 0xffff846bc460>), ('LabuteASA', <function <lambda> at 0xffff846983b0>), ('PEOE_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb8a0>), ('PEOE_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbed0>), ('PEOE_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0xffff84698040>), ('PEOE_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0xffff846980f0>), ('PEOE_VSA13', <function _InstallDescriptors.<locals>.<lambda> at 0xffff846981a0>), ('PEOE_VSA14', <function _InstallDescriptors.<locals>.<lambda> at 0xffff84698250>), ('PEOE_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb950>), ('PEOE_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cba00>), ('PEOE_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbab0>), ('PEOE_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbb60>), ('PEOE_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbc10>), ('PEOE_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbcc0>), ('PEOE_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbd70>), ('PEOE_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbe20>), ('SMR_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867ca980>), ('SMR_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cafb0>), ('SMR_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caa30>), ('SMR_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caae0>), ('SMR_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cab90>), ('SMR_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cac40>), ('SMR_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cacf0>), ('SMR_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cada0>), ('SMR_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cae50>), ('SMR_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caf00>), ('SlogP_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb060>), ('SlogP_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb690>), ('SlogP_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb740>), ('SlogP_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb7f0>), ('SlogP_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb110>), ('SlogP_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb1c0>), ('SlogP_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb270>), ('SlogP_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb320>), ('SlogP_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb3d0>), ('SlogP_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb480>), ('SlogP_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb530>), ('SlogP_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb5e0>), ('TPSA', <function <lambda> at 0xffff846985c0>), ('EState_VSA1', rdkit.Chem.EState.EState_VSA.EState_VSA1), ('EState_VSA10', rdkit.Chem.EState.EState_VSA.EState_VSA10), ('EState_VSA11', rdkit.Chem.EState.EState_VSA.EState_VSA11), ('EState_VSA2', rdkit.Chem.EState.EState_VSA.EState_VSA2), ('EState_VSA3', rdkit.Chem.EState.EState_VSA.EState_VSA3), ('EState_VSA4', rdkit.Chem.EState.EState_VSA.EState_VSA4), ('EState_VSA5', rdkit.Chem.EState.EState_VSA.EState_VSA5), ('EState_VSA6', rdkit.Chem.EState.EState_VSA.EState_VSA6), ('EState_VSA7', rdkit.Chem.EState.EState_VSA.EState_VSA7), ('EState_VSA8', rdkit.Chem.EState.EState_VSA.EState_VSA8), ('EState_VSA9', rdkit.Chem.EState.EState_VSA.EState_VSA9), ('VSA_EState1', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf5e0>), ('VSA_EState10', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfc10>), ('VSA_EState2', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf690>), ('VSA_EState3', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf740>), ('VSA_EState4', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf7f0>), ('VSA_EState5', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf8a0>), ('VSA_EState6', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf950>), ('VSA_EState7', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfa00>), ('VSA_EState8', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfab0>), ('VSA_EState9', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfb60>), ('FractionCSP3', <function <lambda> at 0xffff846be4b0>), ('HeavyAtomCount', rdkit.Chem.Lipinski.HeavyAtomCount), ('NHOHCount', <function <lambda> at 0xffff846be2a0>), ('NOCount', <function <lambda> at 0xffff846be1f0>), ('NumAliphaticCarbocycles', <function <lambda> at 0xffff846beae0>), ('NumAliphaticHeterocycles', <function <lambda> at 0xffff846bea30>), ('NumAliphaticRings', <function <lambda> at 0xffff846be980>), ('NumAmideBonds', <function <lambda> at 0xffff846becf0>), ('NumAromaticCarbocycles', <function <lambda> at 0xffff846be770>), ('NumAromaticHeterocycles', <function <lambda> at 0xffff846be6c0>), ('NumAromaticRings', <function <lambda> at 0xffff846be560>), ('NumAtomStereoCenters', <function <lambda> at 0xffff846beda0>), ('NumBridgeheadAtoms', <function <lambda> at 0xffff846bec40>), ('NumHAcceptors', <function <lambda> at 0xffff846bddd0>), ('NumHDonors', <function <lambda> at 0xffff846bdc70>), ('NumHeteroatoms', <function <lambda> at 0xffff846bdf30>), ('NumHeterocycles', <function <lambda> at 0xffff846bef00>), ('NumRotatableBonds', <function <lambda> at 0xffff846be090>), ('NumSaturatedCarbocycles', <function <lambda> at 0xffff846be8d0>), ('NumSaturatedHeterocycles', <function <lambda> at 0xffff846be820>), ('NumSaturatedRings', <function <lambda> at 0xffff846be610>), ('NumSpiroAtoms', <function <lambda> at 0xffff846bee50>), ('NumUnspecifiedAtomStereoCenters', <function <lambda> at 0xffff846beb90>), ('Phi', <function <lambda> at 0xffff846befb0>), ('RingCount', <function <lambda> at 0xffff846be350>), ('MolLogP', <function <lambda> at 0xffff867ca350>), ('MolMR', <function <lambda> at 0xffff867ca400>), ('fr_Al_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bcc0>), ('fr_Al_OH', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b950>), ('fr_Al_OH_noTert', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6b90>), ('fr_ArN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a71c0>), ('fr_Ar_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bd70>), ('fr_Ar_N', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a45c0>), ('fr_Ar_NH', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4670>), ('fr_Ar_OH', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469ba00>), ('fr_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469be20>), ('fr_COO2', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bed0>), ('fr_C_O', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b7f0>), ('fr_C_O_noCOO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b8a0>), ('fr_C_S', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a57a0>), ('fr_HOCCN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7270>), ('fr_Imine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a47d0>), ('fr_NH0', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4510>), ('fr_NH1', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4460>), ('fr_NH2', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a43b0>), ('fr_N_O', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4b40>), ('fr_Ndealkylation1', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6f00>), ('fr_Ndealkylation2', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6fb0>), ('fr_Nhpyrrole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5170>), ('fr_SH', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a56f0>), ('fr_aldehyde', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4250>), ('fr_alkyl_carbamate', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7060>), ('fr_alkyl_halide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5590>), ('fr_allylic_oxid', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6da0>), ('fr_amide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4eb0>), ('fr_amidine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5010>), ('fr_aniline', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4720>), ('fr_aryl_methyl', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6e50>), ('fr_azide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4e00>), ('fr_azo', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4ca0>), ('fr_barbitur', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5a60>), ('fr_benzene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a66c0>), ('fr_benzodiazepine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6c40>), ('fr_bicyclic', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6610>), ('fr_diazo', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4d50>), ('fr_dihydropyridine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6a30>), ('fr_epoxide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a64b0>), ('fr_ester', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bc10>), ('fr_ether', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a40f0>), ('fr_furan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5d20>), ('fr_guanido', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a50c0>), ('fr_halogen', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a54e0>), ('fr_hdrzine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4930>), ('fr_hdrzone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a49e0>), ('fr_imidazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5c70>), ('fr_imide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5220>), ('fr_isocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a52d0>), ('fr_isothiocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5380>), ('fr_ketone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4040>), ('fr_ketone_Topliss', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7110>), ('fr_lactam', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a62a0>), ('fr_lactone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6350>), ('fr_methoxy', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bab0>), ('fr_morpholine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a61f0>), ('fr_nitrile', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4880>), ('fr_nitro', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4bf0>), ('fr_nitro_arom', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a68d0>), ('fr_nitro_arom_nonortho', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6980>), ('fr_nitroso', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4a90>), ('fr_oxazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5f30>), ('fr_oxime', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bb60>), ('fr_para_hydroxylation', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6cf0>), ('fr_phenol', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a41a0>), ('fr_phenol_noOrthoHbond', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6ae0>), ('fr_phos_acid', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6770>), ('fr_phos_ester', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6820>), ('fr_piperdine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6090>), ('fr_piperzine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6140>), ('fr_priamide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4f60>), ('fr_prisulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a59b0>), ('fr_pyridine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5fe0>), ('fr_quatN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4300>), ('fr_sulfide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5640>), ('fr_sulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5900>), ('fr_sulfone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5850>), ('fr_term_acetylene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5bc0>), ('fr_tetrazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6400>), ('fr_thiazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5e80>), ('fr_thiocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5430>), ('fr_thiophene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5dd0>), ('fr_unbrch_alkane', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6560>), ('fr_urea', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5b10>)]
autocorr: rdkit.Chem.ChemUtils.DescriptorUtilities.VectorDescriptorWrapper  # value = <rdkit.Chem.ChemUtils.DescriptorUtilities.VectorDescriptorWrapper object>
descList: list  # value = [('MaxAbsEStateIndex', rdkit.Chem.EState.EState.MaxAbsEStateIndex), ('MaxEStateIndex', rdkit.Chem.EState.EState.MaxEStateIndex), ('MinAbsEStateIndex', rdkit.Chem.EState.EState.MinAbsEStateIndex), ('MinEStateIndex', rdkit.Chem.EState.EState.MinEStateIndex), ('qed', rdkit.Chem.QED.qed), ('SPS', rdkit.Chem.SpacialScore.SPS), ('MolWt', <function <lambda> at 0xffff846992d0>), ('HeavyAtomMolWt', HeavyAtomMolWt), ('ExactMolWt', <function <lambda> at 0xffff84699bc0>), ('NumValenceElectrons', NumValenceElectrons), ('NumRadicalElectrons', NumRadicalElectrons), ('MaxPartialCharge', MaxPartialCharge), ('MinPartialCharge', MinPartialCharge), ('MaxAbsPartialCharge', MaxAbsPartialCharge), ('MinAbsPartialCharge', MinAbsPartialCharge), ('FpDensityMorgan1', FpDensityMorgan1), ('FpDensityMorgan2', FpDensityMorgan2), ('FpDensityMorgan3', FpDensityMorgan3), ('BCUT2D_MWHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWHI), ('BCUT2D_MWLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MWLOW), ('BCUT2D_CHGHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGHI), ('BCUT2D_CHGLO', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_CHGLO), ('BCUT2D_LOGPHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPHI), ('BCUT2D_LOGPLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_LOGPLOW), ('BCUT2D_MRHI', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRHI), ('BCUT2D_MRLOW', rdkit.Chem.ChemUtils.DescriptorUtilities.BCUT2D_MRLOW), ('AvgIpc', rdkit.Chem.GraphDescriptors.AvgIpc), ('BalabanJ', rdkit.Chem.GraphDescriptors.BalabanJ), ('BertzCT', rdkit.Chem.GraphDescriptors.BertzCT), ('Chi0', rdkit.Chem.GraphDescriptors.Chi0), ('Chi0n', <function <lambda> at 0xffff846bd430>), ('Chi0v', <function <lambda> at 0xffff846bd010>), ('Chi1', rdkit.Chem.GraphDescriptors.Chi1), ('Chi1n', <function <lambda> at 0xffff846bd4e0>), ('Chi1v', <function <lambda> at 0xffff846bd0c0>), ('Chi2n', <function <lambda> at 0xffff846bd590>), ('Chi2v', <function <lambda> at 0xffff846bd170>), ('Chi3n', <function <lambda> at 0xffff846bd640>), ('Chi3v', <function <lambda> at 0xffff846bd220>), ('Chi4n', <function <lambda> at 0xffff846bd6f0>), ('Chi4v', <function <lambda> at 0xffff846bd2d0>), ('HallKierAlpha', <function <lambda> at 0xffff846bc250>), ('Ipc', rdkit.Chem.GraphDescriptors.Ipc), ('Kappa1', <function <lambda> at 0xffff846bc300>), ('Kappa2', <function <lambda> at 0xffff846bc3b0>), ('Kappa3', <function <lambda> at 0xffff846bc460>), ('LabuteASA', <function <lambda> at 0xffff846983b0>), ('PEOE_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb8a0>), ('PEOE_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbed0>), ('PEOE_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0xffff84698040>), ('PEOE_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0xffff846980f0>), ('PEOE_VSA13', <function _InstallDescriptors.<locals>.<lambda> at 0xffff846981a0>), ('PEOE_VSA14', <function _InstallDescriptors.<locals>.<lambda> at 0xffff84698250>), ('PEOE_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb950>), ('PEOE_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cba00>), ('PEOE_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbab0>), ('PEOE_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbb60>), ('PEOE_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbc10>), ('PEOE_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbcc0>), ('PEOE_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbd70>), ('PEOE_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cbe20>), ('SMR_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867ca980>), ('SMR_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cafb0>), ('SMR_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caa30>), ('SMR_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caae0>), ('SMR_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cab90>), ('SMR_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cac40>), ('SMR_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cacf0>), ('SMR_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cada0>), ('SMR_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cae50>), ('SMR_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867caf00>), ('SlogP_VSA1', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb060>), ('SlogP_VSA10', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb690>), ('SlogP_VSA11', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb740>), ('SlogP_VSA12', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb7f0>), ('SlogP_VSA2', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb110>), ('SlogP_VSA3', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb1c0>), ('SlogP_VSA4', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb270>), ('SlogP_VSA5', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb320>), ('SlogP_VSA6', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb3d0>), ('SlogP_VSA7', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb480>), ('SlogP_VSA8', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb530>), ('SlogP_VSA9', <function _InstallDescriptors.<locals>.<lambda> at 0xffff867cb5e0>), ('TPSA', <function <lambda> at 0xffff846985c0>), ('EState_VSA1', rdkit.Chem.EState.EState_VSA.EState_VSA1), ('EState_VSA10', rdkit.Chem.EState.EState_VSA.EState_VSA10), ('EState_VSA11', rdkit.Chem.EState.EState_VSA.EState_VSA11), ('EState_VSA2', rdkit.Chem.EState.EState_VSA.EState_VSA2), ('EState_VSA3', rdkit.Chem.EState.EState_VSA.EState_VSA3), ('EState_VSA4', rdkit.Chem.EState.EState_VSA.EState_VSA4), ('EState_VSA5', rdkit.Chem.EState.EState_VSA.EState_VSA5), ('EState_VSA6', rdkit.Chem.EState.EState_VSA.EState_VSA6), ('EState_VSA7', rdkit.Chem.EState.EState_VSA.EState_VSA7), ('EState_VSA8', rdkit.Chem.EState.EState_VSA.EState_VSA8), ('EState_VSA9', rdkit.Chem.EState.EState_VSA.EState_VSA9), ('VSA_EState1', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf5e0>), ('VSA_EState10', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfc10>), ('VSA_EState2', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf690>), ('VSA_EState3', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf740>), ('VSA_EState4', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf7f0>), ('VSA_EState5', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf8a0>), ('VSA_EState6', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bf950>), ('VSA_EState7', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfa00>), ('VSA_EState8', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfab0>), ('VSA_EState9', <function _descriptor_VSA_EState.<locals>.VSA_EState_bin at 0xffff846bfb60>), ('FractionCSP3', <function <lambda> at 0xffff846be4b0>), ('HeavyAtomCount', rdkit.Chem.Lipinski.HeavyAtomCount), ('NHOHCount', <function <lambda> at 0xffff846be2a0>), ('NOCount', <function <lambda> at 0xffff846be1f0>), ('NumAliphaticCarbocycles', <function <lambda> at 0xffff846beae0>), ('NumAliphaticHeterocycles', <function <lambda> at 0xffff846bea30>), ('NumAliphaticRings', <function <lambda> at 0xffff846be980>), ('NumAmideBonds', <function <lambda> at 0xffff846becf0>), ('NumAromaticCarbocycles', <function <lambda> at 0xffff846be770>), ('NumAromaticHeterocycles', <function <lambda> at 0xffff846be6c0>), ('NumAromaticRings', <function <lambda> at 0xffff846be560>), ('NumAtomStereoCenters', <function <lambda> at 0xffff846beda0>), ('NumBridgeheadAtoms', <function <lambda> at 0xffff846bec40>), ('NumHAcceptors', <function <lambda> at 0xffff846bddd0>), ('NumHDonors', <function <lambda> at 0xffff846bdc70>), ('NumHeteroatoms', <function <lambda> at 0xffff846bdf30>), ('NumHeterocycles', <function <lambda> at 0xffff846bef00>), ('NumRotatableBonds', <function <lambda> at 0xffff846be090>), ('NumSaturatedCarbocycles', <function <lambda> at 0xffff846be8d0>), ('NumSaturatedHeterocycles', <function <lambda> at 0xffff846be820>), ('NumSaturatedRings', <function <lambda> at 0xffff846be610>), ('NumSpiroAtoms', <function <lambda> at 0xffff846bee50>), ('NumUnspecifiedAtomStereoCenters', <function <lambda> at 0xffff846beb90>), ('Phi', <function <lambda> at 0xffff846befb0>), ('RingCount', <function <lambda> at 0xffff846be350>), ('MolLogP', <function <lambda> at 0xffff867ca350>), ('MolMR', <function <lambda> at 0xffff867ca400>), ('fr_Al_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bcc0>), ('fr_Al_OH', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b950>), ('fr_Al_OH_noTert', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6b90>), ('fr_ArN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a71c0>), ('fr_Ar_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bd70>), ('fr_Ar_N', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a45c0>), ('fr_Ar_NH', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4670>), ('fr_Ar_OH', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469ba00>), ('fr_COO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469be20>), ('fr_COO2', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bed0>), ('fr_C_O', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b7f0>), ('fr_C_O_noCOO', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469b8a0>), ('fr_C_S', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a57a0>), ('fr_HOCCN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7270>), ('fr_Imine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a47d0>), ('fr_NH0', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4510>), ('fr_NH1', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4460>), ('fr_NH2', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a43b0>), ('fr_N_O', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4b40>), ('fr_Ndealkylation1', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6f00>), ('fr_Ndealkylation2', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6fb0>), ('fr_Nhpyrrole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5170>), ('fr_SH', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a56f0>), ('fr_aldehyde', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4250>), ('fr_alkyl_carbamate', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7060>), ('fr_alkyl_halide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5590>), ('fr_allylic_oxid', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6da0>), ('fr_amide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4eb0>), ('fr_amidine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5010>), ('fr_aniline', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4720>), ('fr_aryl_methyl', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6e50>), ('fr_azide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4e00>), ('fr_azo', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4ca0>), ('fr_barbitur', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5a60>), ('fr_benzene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a66c0>), ('fr_benzodiazepine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6c40>), ('fr_bicyclic', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6610>), ('fr_diazo', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4d50>), ('fr_dihydropyridine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6a30>), ('fr_epoxide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a64b0>), ('fr_ester', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bc10>), ('fr_ether', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a40f0>), ('fr_furan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5d20>), ('fr_guanido', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a50c0>), ('fr_halogen', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a54e0>), ('fr_hdrzine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4930>), ('fr_hdrzone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a49e0>), ('fr_imidazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5c70>), ('fr_imide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5220>), ('fr_isocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a52d0>), ('fr_isothiocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5380>), ('fr_ketone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4040>), ('fr_ketone_Topliss', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a7110>), ('fr_lactam', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a62a0>), ('fr_lactone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6350>), ('fr_methoxy', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bab0>), ('fr_morpholine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a61f0>), ('fr_nitrile', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4880>), ('fr_nitro', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4bf0>), ('fr_nitro_arom', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a68d0>), ('fr_nitro_arom_nonortho', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6980>), ('fr_nitroso', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4a90>), ('fr_oxazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5f30>), ('fr_oxime', <function _LoadPatterns.<locals>.<lambda> at 0xffff8469bb60>), ('fr_para_hydroxylation', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6cf0>), ('fr_phenol', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a41a0>), ('fr_phenol_noOrthoHbond', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6ae0>), ('fr_phos_acid', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6770>), ('fr_phos_ester', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6820>), ('fr_piperdine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6090>), ('fr_piperzine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6140>), ('fr_priamide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4f60>), ('fr_prisulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a59b0>), ('fr_pyridine', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5fe0>), ('fr_quatN', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a4300>), ('fr_sulfide', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5640>), ('fr_sulfonamd', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5900>), ('fr_sulfone', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5850>), ('fr_term_acetylene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5bc0>), ('fr_tetrazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6400>), ('fr_thiazole', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5e80>), ('fr_thiocyan', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5430>), ('fr_thiophene', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5dd0>), ('fr_unbrch_alkane', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a6560>), ('fr_urea', <function _LoadPatterns.<locals>.<lambda> at 0xffff846a5b10>)]
names: list = ['AUTOCORR2D_1', 'AUTOCORR2D_2', 'AUTOCORR2D_3', 'AUTOCORR2D_4', 'AUTOCORR2D_5', 'AUTOCORR2D_6', 'AUTOCORR2D_7', 'AUTOCORR2D_8', 'AUTOCORR2D_9', 'AUTOCORR2D_10', 'AUTOCORR2D_11', 'AUTOCORR2D_12', 'AUTOCORR2D_13', 'AUTOCORR2D_14', 'AUTOCORR2D_15', 'AUTOCORR2D_16', 'AUTOCORR2D_17', 'AUTOCORR2D_18', 'AUTOCORR2D_19', 'AUTOCORR2D_20', 'AUTOCORR2D_21', 'AUTOCORR2D_22', 'AUTOCORR2D_23', 'AUTOCORR2D_24', 'AUTOCORR2D_25', 'AUTOCORR2D_26', 'AUTOCORR2D_27', 'AUTOCORR2D_28', 'AUTOCORR2D_29', 'AUTOCORR2D_30', 'AUTOCORR2D_31', 'AUTOCORR2D_32', 'AUTOCORR2D_33', 'AUTOCORR2D_34', 'AUTOCORR2D_35', 'AUTOCORR2D_36', 'AUTOCORR2D_37', 'AUTOCORR2D_38', 'AUTOCORR2D_39', 'AUTOCORR2D_40', 'AUTOCORR2D_41', 'AUTOCORR2D_42', 'AUTOCORR2D_43', 'AUTOCORR2D_44', 'AUTOCORR2D_45', 'AUTOCORR2D_46', 'AUTOCORR2D_47', 'AUTOCORR2D_48', 'AUTOCORR2D_49', 'AUTOCORR2D_50', 'AUTOCORR2D_51', 'AUTOCORR2D_52', 'AUTOCORR2D_53', 'AUTOCORR2D_54', 'AUTOCORR2D_55', 'AUTOCORR2D_56', 'AUTOCORR2D_57', 'AUTOCORR2D_58', 'AUTOCORR2D_59', 'AUTOCORR2D_60', 'AUTOCORR2D_61', 'AUTOCORR2D_62', 'AUTOCORR2D_63', 'AUTOCORR2D_64', 'AUTOCORR2D_65', 'AUTOCORR2D_66', 'AUTOCORR2D_67', 'AUTOCORR2D_68', 'AUTOCORR2D_69', 'AUTOCORR2D_70', 'AUTOCORR2D_71', 'AUTOCORR2D_72', 'AUTOCORR2D_73', 'AUTOCORR2D_74', 'AUTOCORR2D_75', 'AUTOCORR2D_76', 'AUTOCORR2D_77', 'AUTOCORR2D_78', 'AUTOCORR2D_79', 'AUTOCORR2D_80', 'AUTOCORR2D_81', 'AUTOCORR2D_82', 'AUTOCORR2D_83', 'AUTOCORR2D_84', 'AUTOCORR2D_85', 'AUTOCORR2D_86', 'AUTOCORR2D_87', 'AUTOCORR2D_88', 'AUTOCORR2D_89', 'AUTOCORR2D_90', 'AUTOCORR2D_91', 'AUTOCORR2D_92', 'AUTOCORR2D_93', 'AUTOCORR2D_94', 'AUTOCORR2D_95', 'AUTOCORR2D_96', 'AUTOCORR2D_97', 'AUTOCORR2D_98', 'AUTOCORR2D_99', 'AUTOCORR2D_100', 'AUTOCORR2D_101', 'AUTOCORR2D_102', 'AUTOCORR2D_103', 'AUTOCORR2D_104', 'AUTOCORR2D_105', 'AUTOCORR2D_106', 'AUTOCORR2D_107', 'AUTOCORR2D_108', 'AUTOCORR2D_109', 'AUTOCORR2D_110', 'AUTOCORR2D_111', 'AUTOCORR2D_112', 'AUTOCORR2D_113', 'AUTOCORR2D_114', 'AUTOCORR2D_115', 'AUTOCORR2D_116', 'AUTOCORR2D_117', 'AUTOCORR2D_118', 'AUTOCORR2D_119', 'AUTOCORR2D_120', 'AUTOCORR2D_121', 'AUTOCORR2D_122', 'AUTOCORR2D_123', 'AUTOCORR2D_124', 'AUTOCORR2D_125', 'AUTOCORR2D_126', 'AUTOCORR2D_127', 'AUTOCORR2D_128', 'AUTOCORR2D_129', 'AUTOCORR2D_130', 'AUTOCORR2D_131', 'AUTOCORR2D_132', 'AUTOCORR2D_133', 'AUTOCORR2D_134', 'AUTOCORR2D_135', 'AUTOCORR2D_136', 'AUTOCORR2D_137', 'AUTOCORR2D_138', 'AUTOCORR2D_139', 'AUTOCORR2D_140', 'AUTOCORR2D_141', 'AUTOCORR2D_142', 'AUTOCORR2D_143', 'AUTOCORR2D_144', 'AUTOCORR2D_145', 'AUTOCORR2D_146', 'AUTOCORR2D_147', 'AUTOCORR2D_148', 'AUTOCORR2D_149', 'AUTOCORR2D_150', 'AUTOCORR2D_151', 'AUTOCORR2D_152', 'AUTOCORR2D_153', 'AUTOCORR2D_154', 'AUTOCORR2D_155', 'AUTOCORR2D_156', 'AUTOCORR2D_157', 'AUTOCORR2D_158', 'AUTOCORR2D_159', 'AUTOCORR2D_160', 'AUTOCORR2D_161', 'AUTOCORR2D_162', 'AUTOCORR2D_163', 'AUTOCORR2D_164', 'AUTOCORR2D_165', 'AUTOCORR2D_166', 'AUTOCORR2D_167', 'AUTOCORR2D_168', 'AUTOCORR2D_169', 'AUTOCORR2D_170', 'AUTOCORR2D_171', 'AUTOCORR2D_172', 'AUTOCORR2D_173', 'AUTOCORR2D_174', 'AUTOCORR2D_175', 'AUTOCORR2D_176', 'AUTOCORR2D_177', 'AUTOCORR2D_178', 'AUTOCORR2D_179', 'AUTOCORR2D_180', 'AUTOCORR2D_181', 'AUTOCORR2D_182', 'AUTOCORR2D_183', 'AUTOCORR2D_184', 'AUTOCORR2D_185', 'AUTOCORR2D_186', 'AUTOCORR2D_187', 'AUTOCORR2D_188', 'AUTOCORR2D_189', 'AUTOCORR2D_190', 'AUTOCORR2D_191', 'AUTOCORR2D_192']
