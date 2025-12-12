##
# File: AmberPTParserListener.py
# Date: 27-Jan-2022
#
# Updates:
""" ParserLister class for AMBER PT files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import re

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import NAMES_ELEMENT  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import
from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.AmberPTParser import AmberPTParser
    from wwpdb.utils.nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           protonBeginCode,
                                           letterToDigit,
                                           indexToLetter,
                                           retrieveAtomIdentFromMRMap)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.AmberPTParser import AmberPTParser
    from nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from nmr.mr.ParserListenerUtil import (REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode,
                               letterToDigit,
                               indexToLetter,
                               retrieveAtomIdentFromMRMap)


def chunk_string(line: str, length: int = 4) -> List[str]:
    """ Split a string into fixed length chunks.
    """

    return [line[i:i + length] for i in range(0, len(line), length)]


# This class defines a complete listener for a parse tree produced by AmberPTParser.
class AmberPTParserListener(ParseTreeListener, BaseTopologyParserListener):
    __slots__ = ('versionStatements',
                 'amberAtomTypeStatements',
                 'angleEquilValueStatements',
                 'angleForceConstantStatements',
                 'anglesIncHydrogenStatements',
                 'anglesWithoutHydrogenStatements',
                 'atomicNumberStatements',
                 'atomNameStatements',
                 'atomTypeIndexStatements',
                 'atomsPerMoleculeStatements',
                 'bondEquilValueStatements',
                 'bondForceConstantStatements',
                 'bondsIncHydrogenStatements',
                 'bondsWithoutHydrogenStatements',
                 'boxDimensionsStatements',
                 'capInfoStatements',
                 'capInfo2Statements',
                 'chargeStatements',
                 'cmapCountStatements',
                 'cmapResolutionStatements',
                 'cmapParameterStatements',
                 'cmapIndexStatements',
                 'dihedralForceConstantStatements',
                 'dihedralPeriodicityStatements',
                 'dihedralPhaseStatements',
                 'dihedralsIncHydrogenStatements',
                 'dihedralsWithoutHydrogenStatements',
                 'excludedAtomsListStatements',
                 'hbcutStatements',
                 'hbondAcoefStatements',
                 'hbondBcoefStatements',
                 'ipolStatements',
                 'irotatStatements',
                 'joinArrayStatements',
                 'lennardJonesAcoefStatements',
                 'lennardJonesBcoefStatements',
                 'massStatements',
                 'nonbondedParmIndexStatements',
                 'numberExcludedAtomsStatements',
                 'pointersStatements',
                 'polarizabilityStatements',
                 'radiiStatements',
                 'radiusSetStatements',
                 'residueLabelStatements',
                 'residuePointerStatements',
                 'sceeScaleFactorStatements',
                 'scnbScaleFactorStatements',
                 'screenStatements',
                 'soltyStatements',
                 'solventPointersStatements',
                 'titleStatements',
                 'treeChainClassificationStatements')

    # version information
    __version = None
    __date = None
    __time = None

    # title
    __title = None

    # radius set
    __radiusSet = None

    # residue label
    __residueLabel = None

    # residue_pointer
    __residuePointer = None

    # atom_name
    __atomName = None

    # amber_atom_type
    __amberAtomType = None

    # Fortran format
    __a_format_pat = re.compile(r'\((\d+)[aA](\d+)\)$')
    __i_format_pat = re.compile(r'\((\d+)[iI](\d+)\)$')
    __i_format_pat = re.compile(r'\((\d+)[eE](\d+)\.?(\d+)?\)$')

    # __cur_column_len = None
    __cur_word_len = None

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        super().__init__(verbose, log, representativeModelId, representativeAltId, mrAtomNameMapping,
                         cR, caC, nefT)

        self.file_type = 'nm-aux-amb'

        self.versionStatements = 0
        self.amberAtomTypeStatements = 0
        self.angleEquilValueStatements = 0
        self.angleForceConstantStatements = 0
        self.anglesIncHydrogenStatements = 0
        self.anglesWithoutHydrogenStatements = 0
        self.atomicNumberStatements = 0
        self.atomNameStatements = 0
        self.atomTypeIndexStatements = 0
        self.atomsPerMoleculeStatements = 0
        self.bondEquilValueStatements = 0
        self.bondForceConstantStatements = 0
        self.bondsIncHydrogenStatements = 0
        self.bondsWithoutHydrogenStatements = 0
        self.boxDimensionsStatements = 0
        self.capInfoStatements = 0
        self.capInfo2Statements = 0
        self.chargeStatements = 0
        self.cmapCountStatements = 0
        self.cmapResolutionStatements = 0
        self.cmapParameterStatements = 0
        self.cmapIndexStatements = 0
        self.dihedralForceConstantStatements = 0
        self.dihedralPeriodicityStatements = 0
        self.dihedralPhaseStatements = 0
        self.dihedralsIncHydrogenStatements = 0
        self.dihedralsWithoutHydrogenStatements = 0
        self.excludedAtomsListStatements = 0
        self.hbcutStatements = 0
        self.hbondAcoefStatements = 0
        self.hbondBcoefStatements = 0
        self.ipolStatements = 0
        self.irotatStatements = 0
        self.joinArrayStatements = 0
        self.lennardJonesAcoefStatements = 0
        self.lennardJonesBcoefStatements = 0
        self.massStatements = 0
        self.nonbondedParmIndexStatements = 0
        self.numberExcludedAtomsStatements = 0
        self.pointersStatements = 0
        self.polarizabilityStatements = 0
        self.radiiStatements = 0
        self.radiusSetStatements = 0
        self.residueLabelStatements = 0
        self.residuePointerStatements = 0
        self.sceeScaleFactorStatements = 0
        self.scnbScaleFactorStatements = 0
        self.screenStatements = 0
        self.soltyStatements = 0
        self.solventPointersStatements = 0
        self.titleStatements = 0
        self.treeChainClassificationStatements = 0

    # Enter a parse tree produced by AmberPTParser#amber_pt.
    def enterAmber_pt(self, ctx: AmberPTParser.Amber_ptContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AmberPTParser#amber_pt.
    def exitAmber_pt(self, ctx: AmberPTParser.Amber_ptContext):  # pylint: disable=unused-argument

        if not self.hasPolySeqModel:
            return

        if None in (self.__residueLabel, self.__residuePointer, self.__atomName, self.__amberAtomType):
            return

        if 0 in (len(self.__residueLabel), len(self.__residuePointer), len(self.__atomName), len(self.__amberAtomType)):
            return

        residuePointer2 = [resPoint - 1 for resPoint in self.__residuePointer]
        del residuePointer2[0]
        residuePointer2.append(self.__residuePointer[-1] + 1000)

        chainIndex = letterToDigit(self.polySeqModel[0]['chain_id']) - 1  # set tentative chain_id from label_asym_id, which will be assigned to coordinate auth_asym_id
        chainId = indexToLetter(chainIndex)

        terminus = [atomName.endswith('T') for atomName in self.__atomName]

        atomTotal = len(self.__atomName)
        if terminus[0]:
            terminus[0] = False
        for i in range(0, atomTotal - 1):
            j = i + 1
            if terminus[i] and terminus[j]:
                terminus[i] = False
        if terminus[-1]:
            terminus[-1] = False

        seqIdList, compIdList, retrievedAtomNumList = [], [], []

        hasSegCompId = False
        ancAtomName = prevAtomName = ''
        prevSeqId = prevCompId = None
        offset = 0
        for atomNum, (atomName, atomType) in enumerate(zip(self.__atomName, self.__amberAtomType), start=1):
            _seqId = next(resNum for resNum, (atomNumBegin, atomNumEnd)
                          in enumerate(zip(self.__residuePointer, residuePointer2), start=1)
                          if atomNumBegin <= atomNum <= atomNumEnd)
            compId = self.__residueLabel[_seqId - 1]
            if self.noWaterMol and (compId in ('HOH', 'H2O', 'WAT') or (len(compId) > 3 and compId[:3] in ('HOH', 'H2O', 'WAT'))):
                break
            if not hasSegCompId and (compId.endswith('5') or compId.endswith('3')):
                hasSegCompId = True
            if not hasSegCompId and compId not in monDict3 and self.mrAtomNameMapping is not None and atomName[0] in protonBeginCode:
                _, compId, _atomName = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, _seqId, compId, atomName)
                if _atomName != atomName:
                    atomName = _atomName
                    retrievedAtomNumList.append(atomNum)

            if (0 < atomNum < len(terminus) + 1
                and ((terminus[atomNum - 1] and ancAtomName.endswith('T'))
                     or (terminus[atomNum - 2] and prevAtomName.endswith('T')
                         and self.csStat.getTypeOfCompId(prevCompId) != self.csStat.getTypeOfCompId(compId))))\
               or self.isSegment(prevCompId, prevAtomName, compId, atomName)\
               or self.isLigand(prevCompId, compId)\
               or self.isMetalIon(compId, atomName)\
               or self.isMetalIon(prevCompId, prevAtomName)\
               or self.isMetalElem(prevAtomName, prevSeqId, _seqId):

                self.polySeqPrmTop.append({'chain_id': chainId,
                                           'seq_id': seqIdList,
                                           'auth_comp_id': compIdList})
                seqIdList = []
                compIdList = []
                chainIndex += 1
                chainId = indexToLetter(chainIndex)
                offset = 1 - _seqId

            seqId = _seqId + offset
            if seqId not in seqIdList:
                seqIdList.append(seqId)
                compIdList.append(compId)
            self.atomNumberDict[atomNum] = {'chain_id': chainId,
                                            'seq_id': seqId,
                                            'auth_comp_id': compId,
                                            'auth_atom_id': atomName,
                                            'atom_type': atomType}
            ancAtomName = prevAtomName
            prevAtomName = atomName
            prevSeqId = _seqId
            prevCompId = compId

        self.polySeqPrmTop.append({'chain_id': chainId,
                                   'seq_id': seqIdList,
                                   'auth_comp_id': compIdList})

        self.exit(retrievedAtomNumList)

    # Enter a parse tree produced by AmberPTParser#version_statement.
    def enterVersion_statement(self, ctx: AmberPTParser.Version_statementContext):  # pylint: disable=unused-argument
        self.versionStatements += 1

    # Exit a parse tree produced by AmberPTParser#version_statement.
    def exitVersion_statement(self, ctx: AmberPTParser.Version_statementContext):
        self.__version = str(ctx.Version())
        self.__date = str(ctx.Date_time(0))
        if ctx.Date_time(0):
            self.__time = str(ctx.Date_time(1))

    # Enter a parse tree produced by AmberPTParser#amber_atom_type_statement.
    def enterAmber_atom_type_statement(self, ctx: AmberPTParser.Amber_atom_type_statementContext):  # pylint: disable=unused-argument
        self.amberAtomTypeStatements += 1

    # Exit a parse tree produced by AmberPTParser#amber_atom_type_statement.
    def exitAmber_atom_type_statement(self, ctx: AmberPTParser.Amber_atom_type_statementContext):
        if ctx.Simple_name(0):
            if self.hasCoord:
                atomTypeList = []
                i = 0
                while ctx.Simple_name(i):
                    atomTypeList += chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len)
                    if self.noWaterMol and set(atomTypeList[-2:]) == {'OW', 'HW'}:
                        break
                    # atomTypeList.extend(chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len))
                    i += 1
                self.__amberAtomType = atomTypeList
            return
        self.amberAtomTypeStatements -= 1

    # Enter a parse tree produced by AmberPTParser#angle_equil_value_statement.
    def enterAngle_equil_value_statement(self, ctx: AmberPTParser.Angle_equil_value_statementContext):  # pylint: disable=unused-argument
        self.angleEquilValueStatements += 1

    # Exit a parse tree produced by AmberPTParser#angle_equil_value_statement.
    def exitAngle_equil_value_statement(self, ctx: AmberPTParser.Angle_equil_value_statementContext):
        if ctx.Real(0):
            return
        self.angleEquilValueStatements -= 1

    # Enter a parse tree produced by AmberPTParser#angle_force_constant_statement.
    def enterAngle_force_constant_statement(self, ctx: AmberPTParser.Angle_force_constant_statementContext):  # pylint: disable=unused-argument
        self.angleForceConstantStatements += 1

    # Exit a parse tree produced by AmberPTParser#angle_force_constant_statement.
    def exitAngle_force_constant_statement(self, ctx: AmberPTParser.Angle_force_constant_statementContext):
        if ctx.Real(0):
            return
        self.angleForceConstantStatements -= 1

    # Enter a parse tree produced by AmberPTParser#angles_inc_hydrogen_statement.
    def enterAngles_inc_hydrogen_statement(self, ctx: AmberPTParser.Angles_inc_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.anglesIncHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#angles_inc_hydrogen_statement.
    def exitAngles_inc_hydrogen_statement(self, ctx: AmberPTParser.Angles_inc_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.anglesIncHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#angles_without_hydrogen_statement.
    def enterAngles_without_hydrogen_statement(self, ctx: AmberPTParser.Angles_without_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.anglesWithoutHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#angles_without_hydrogen_statement.
    def exitAngles_without_hydrogen_statement(self, ctx: AmberPTParser.Angles_without_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.anglesWithoutHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#atomic_number_statement.
    def enterAtomic_number_statement(self, ctx: AmberPTParser.Atomic_number_statementContext):  # pylint: disable=unused-argument
        self.atomicNumberStatements += 1

    # Exit a parse tree produced by AmberPTParser#atomic_number_statement.
    def exitAtomic_number_statement(self, ctx: AmberPTParser.Atomic_number_statementContext):
        if ctx.Integer(0):
            return
        self.atomicNumberStatements -= 1

    # Enter a parse tree produced by AmberPTParser#atom_name_statement.
    def enterAtom_name_statement(self, ctx: AmberPTParser.Atom_name_statementContext):  # pylint: disable=unused-argument
        self.atomNameStatements += 1

    # Exit a parse tree produced by AmberPTParser#atom_name_statement.
    def exitAtom_name_statement(self, ctx: AmberPTParser.Atom_name_statementContext):
        if ctx.Simple_name(0):
            if self.hasCoord:
                atomIdList = []
                i = 0
                while ctx.Simple_name(i):
                    atomIdList += chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len)
                    if self.noWaterMol and set(atomIdList[-3:]) == {'O', 'H1', 'H2'}:
                        break
                    # atomIdList.extend(chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len))
                    i += 1
                self.__atomName = atomIdList
            return
        self.atomNameStatements -= 1

    # Enter a parse tree produced by AmberPTParser#atom_type_index_statement.
    def enterAtom_type_index_statement(self, ctx: AmberPTParser.Atom_type_index_statementContext):  # pylint: disable=unused-argument
        self.atomTypeIndexStatements += 1

    # Exit a parse tree produced by AmberPTParser#atom_type_index_statement.
    def exitAtom_type_index_statement(self, ctx: AmberPTParser.Atom_type_index_statementContext):
        if ctx.Integer(0):
            return
        self.atomTypeIndexStatements += 1

    # Enter a parse tree produced by AmberPTParser#atoms_per_molecule_statement.
    def enterAtoms_per_molecule_statement(self, ctx: AmberPTParser.Atoms_per_molecule_statementContext):  # pylint: disable=unused-argument
        self.atomsPerMoleculeStatements += 1

    # Exit a parse tree produced by AmberPTParser#atoms_per_molecule_statement.
    def exitAtoms_per_molecule_statement(self, ctx: AmberPTParser.Atoms_per_molecule_statementContext):
        if ctx.Integer(0):
            return
        self.atomsPerMoleculeStatements -= 1

    # Enter a parse tree produced by AmberPTParser#bond_equil_value_statement.
    def enterBond_equil_value_statement(self, ctx: AmberPTParser.Bond_equil_value_statementContext):  # pylint: disable=unused-argument
        self.bondEquilValueStatements += 1

    # Exit a parse tree produced by AmberPTParser#bond_equil_value_statement.
    def exitBond_equil_value_statement(self, ctx: AmberPTParser.Bond_equil_value_statementContext):
        if ctx.Real(0):
            return
        self.bondEquilValueStatements -= 1

    # Enter a parse tree produced by AmberPTParser#bond_force_constant_statement.
    def enterBond_force_constant_statement(self, ctx: AmberPTParser.Bond_force_constant_statementContext):  # pylint: disable=unused-argument
        self.bondForceConstantStatements += 1

    # Exit a parse tree produced by AmberPTParser#bond_force_constant_statement.
    def exitBond_force_constant_statement(self, ctx: AmberPTParser.Bond_force_constant_statementContext):
        if ctx.Real(0):
            return
        self.bondForceConstantStatements -= 1

    # Enter a parse tree produced by AmberPTParser#bonds_inc_hydrogen_statement.
    def enterBonds_inc_hydrogen_statement(self, ctx: AmberPTParser.Bonds_inc_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.bondsIncHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#bonds_inc_hydrogen_statement.
    def exitBonds_inc_hydrogen_statement(self, ctx: AmberPTParser.Bonds_inc_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.bondsIncHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#bonds_without_hydrogen_statement.
    def enterBonds_without_hydrogen_statement(self, ctx: AmberPTParser.Bonds_without_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.bondsWithoutHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#bonds_without_hydrogen_statement.
    def exitBonds_without_hydrogen_statement(self, ctx: AmberPTParser.Bonds_without_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.bondsWithoutHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#box_dimensions_statement.
    def enterBox_dimensions_statement(self, ctx: AmberPTParser.Box_dimensions_statementContext):  # pylint: disable=unused-argument
        self.boxDimensionsStatements += 1

    # Exit a parse tree produced by AmberPTParser#box_dimensions_statement.
    def exitBox_dimensions_statement(self, ctx: AmberPTParser.Box_dimensions_statementContext):
        if ctx.Real(0):
            return
        self.boxDimensionsStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cap_info_statement.
    def enterCap_info_statement(self, ctx: AmberPTParser.Cap_info_statementContext):  # pylint: disable=unused-argument
        self.capInfoStatements += 1

    # Exit a parse tree produced by AmberPTParser#cap_info_statement.
    def exitCap_info_statement(self, ctx: AmberPTParser.Cap_info_statementContext):
        if ctx.Integer(0):
            return
        self.capInfoStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cap_info2_statement.
    def enterCap_info2_statement(self, ctx: AmberPTParser.Cap_info2_statementContext):  # pylint: disable=unused-argument
        self.capInfo2Statements += 1

    # Exit a parse tree produced by AmberPTParser#cap_info2_statement.
    def exitCap_info2_statement(self, ctx: AmberPTParser.Cap_info2_statementContext):
        if ctx.Real(0):
            return
        self.capInfo2Statements -= 1

    # Enter a parse tree produced by AmberPTParser#charge_statement.
    def enterCharge_statement(self, ctx: AmberPTParser.Charge_statementContext):  # pylint: disable=unused-argument
        self.chargeStatements += 1

    # Exit a parse tree produced by AmberPTParser#charge_statement.
    def exitCharge_statement(self, ctx: AmberPTParser.Charge_statementContext):
        if ctx.Real(0):
            return
        self.chargeStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cmap_count_statement.
    def enterCmap_count_statement(self, ctx: AmberPTParser.Cmap_count_statementContext):  # pylint: disable=unused-argument
        self.cmapCountStatements += 1

    # Exit a parse tree produced by AmberPTParser#cmap_count_statement.
    def exitCmap_count_statement(self, ctx: AmberPTParser.Cmap_count_statementContext):
        if ctx.Integer(0):
            return
        self.cmapCountStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cmap_resolution_statement.
    def enterCmap_resolution_statement(self, ctx: AmberPTParser.Cmap_resolution_statementContext):  # pylint: disable=unused-argument
        self.cmapResolutionStatements += 1

    # Exit a parse tree produced by AmberPTParser#cmap_resolution_statement.
    def exitCmap_resolution_statement(self, ctx: AmberPTParser.Cmap_resolution_statementContext):
        if ctx.Integer(0):
            return
        self.cmapResolutionStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cmap_parameter_statement.
    def enterCmap_parameter_statement(self, ctx: AmberPTParser.Cmap_parameter_statementContext):  # pylint: disable=unused-argument
        self.cmapParameterStatements += 1

    # Exit a parse tree produced by AmberPTParser#cmap_parameter_statement.
    def exitCmap_parameter_statement(self, ctx: AmberPTParser.Cmap_parameter_statementContext):
        if ctx.Real(0):
            return
        self.cmapParameterStatements -= 1

    # Enter a parse tree produced by AmberPTParser#cmap_index_statement.
    def enterCmap_index_statement(self, ctx: AmberPTParser.Cmap_index_statementContext):  # pylint: disable=unused-argument
        self.cmapIndexStatements += 1

    # Exit a parse tree produced by AmberPTParser#cmap_index_statement.
    def exitCmap_index_statement(self, ctx: AmberPTParser.Cmap_index_statementContext):
        if ctx.Integer(0):
            return
        self.cmapIndexStatements -= 1

    # Enter a parse tree produced by AmberPTParser#dihedral_force_constant_statement.
    def enterDihedral_force_constant_statement(self, ctx: AmberPTParser.Dihedral_force_constant_statementContext):  # pylint: disable=unused-argument
        self.dihedralForceConstantStatements += 1

    # Exit a parse tree produced by AmberPTParser#dihedral_force_constant_statement.
    def exitDihedral_force_constant_statement(self, ctx: AmberPTParser.Dihedral_force_constant_statementContext):
        if ctx.Real(0):
            return
        self.dihedralForceConstantStatements -= 1

    # Enter a parse tree produced by AmberPTParser#dihedral_periodicity_statement.
    def enterDihedral_periodicity_statement(self, ctx: AmberPTParser.Dihedral_periodicity_statementContext):  # pylint: disable=unused-argument
        self.dihedralPeriodicityStatements += 1

    # Exit a parse tree produced by AmberPTParser#dihedral_periodicity_statement.
    def exitDihedral_periodicity_statement(self, ctx: AmberPTParser.Dihedral_periodicity_statementContext):
        if ctx.Real(0):
            return
        self.dihedralPeriodicityStatements -= 1

    # Enter a parse tree produced by AmberPTParser#dihedral_phase_statement.
    def enterDihedral_phase_statement(self, ctx: AmberPTParser.Dihedral_phase_statementContext):  # pylint: disable=unused-argument
        self.dihedralPhaseStatements += 1

    # Exit a parse tree produced by AmberPTParser#dihedral_phase_statement.
    def exitDihedral_phase_statement(self, ctx: AmberPTParser.Dihedral_phase_statementContext):
        if ctx.Real(0):
            return
        self.dihedralPhaseStatements -= 1

    # Enter a parse tree produced by AmberPTParser#dihedrals_inc_hydrogen_statement.
    def enterDihedrals_inc_hydrogen_statement(self, ctx: AmberPTParser.Dihedrals_inc_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.dihedralsIncHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#dihedrals_inc_hydrogen_statement.
    def exitDihedrals_inc_hydrogen_statement(self, ctx: AmberPTParser.Dihedrals_inc_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.dihedralsIncHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#dihedrals_without_hydrogen_statement.
    def enterDihedrals_without_hydrogen_statement(self, ctx: AmberPTParser.Dihedrals_without_hydrogen_statementContext):  # pylint: disable=unused-argument
        self.dihedralsWithoutHydrogenStatements += 1

    # Exit a parse tree produced by AmberPTParser#dihedrals_without_hydrogen_statement.
    def exitDihedrals_without_hydrogen_statement(self, ctx: AmberPTParser.Dihedrals_without_hydrogen_statementContext):
        if ctx.Integer(0):
            return
        self.dihedralsWithoutHydrogenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#excluded_atoms_list_statement.
    def enterExcluded_atoms_list_statement(self, ctx: AmberPTParser.Excluded_atoms_list_statementContext):  # pylint: disable=unused-argument
        self.excludedAtomsListStatements += 1

    # Exit a parse tree produced by AmberPTParser#excluded_atoms_list_statement.
    def exitExcluded_atoms_list_statement(self, ctx: AmberPTParser.Excluded_atoms_list_statementContext):
        if ctx.Integer(0):
            return
        self.excludedAtomsListStatements -= 1

    # Enter a parse tree produced by AmberPTParser#hbcut_statement.
    def enterHbcut_statement(self, ctx: AmberPTParser.Hbcut_statementContext):  # pylint: disable=unused-argument
        self.hbcutStatements += 1

    # Exit a parse tree produced by AmberPTParser#hbcut_statement.
    def exitHbcut_statement(self, ctx: AmberPTParser.Hbcut_statementContext):
        if ctx.Real(0):
            return
        self.hbcutStatements -= 1

    # Enter a parse tree produced by AmberPTParser#hbond_acoef_statement.
    def enterHbond_acoef_statement(self, ctx: AmberPTParser.Hbond_acoef_statementContext):  # pylint: disable=unused-argument
        self.hbondAcoefStatements += 1

    # Exit a parse tree produced by AmberPTParser#hbond_acoef_statement.
    def exitHbond_acoef_statement(self, ctx: AmberPTParser.Hbond_acoef_statementContext):
        if ctx.Real(0):
            return
        self.hbondAcoefStatements -= 1

    # Enter a parse tree produced by AmberPTParser#hbond_bcoef_statement.
    def enterHbond_bcoef_statement(self, ctx: AmberPTParser.Hbond_bcoef_statementContext):  # pylint: disable=unused-argument
        self.hbondBcoefStatements += 1

    # Exit a parse tree produced by AmberPTParser#hbond_bcoef_statement.
    def exitHbond_bcoef_statement(self, ctx: AmberPTParser.Hbond_bcoef_statementContext):
        if ctx.Real(0):
            return
        self.hbondBcoefStatements -= 1

    # Enter a parse tree produced by AmberPTParser#ipol_statement.
    def enterIpol_statement(self, ctx: AmberPTParser.Ipol_statementContext):  # pylint: disable=unused-argument
        self.ipolStatements += 1

    # Exit a parse tree produced by AmberPTParser#ipol_statement.
    def exitIpol_statement(self, ctx: AmberPTParser.Ipol_statementContext):
        if ctx.Integer(0):
            return
        self.ipolStatements -= 1

    # Enter a parse tree produced by AmberPTParser#irotat_statement.
    def enterIrotat_statement(self, ctx: AmberPTParser.Irotat_statementContext):  # pylint: disable=unused-argument
        self.irotatStatements += 1

    # Exit a parse tree produced by AmberPTParser#irotat_statement.
    def exitIrotat_statement(self, ctx: AmberPTParser.Irotat_statementContext):
        if ctx.Integer(0):
            return
        self.irotatStatements -= 1

    # Enter a parse tree produced by AmberPTParser#join_array_statement.
    def enterJoin_array_statement(self, ctx: AmberPTParser.Join_array_statementContext):  # pylint: disable=unused-argument
        self.joinArrayStatements += 1

    # Exit a parse tree produced by AmberPTParser#join_array_statement.
    def exitJoin_array_statement(self, ctx: AmberPTParser.Join_array_statementContext):
        if ctx.Integer(0):
            return
        self.joinArrayStatements -= 1

    # Enter a parse tree produced by AmberPTParser#lennard_jones_acoef_statement.
    def enterLennard_jones_acoef_statement(self, ctx: AmberPTParser.Lennard_jones_acoef_statementContext):  # pylint: disable=unused-argument
        self.lennardJonesAcoefStatements += 1

    # Exit a parse tree produced by AmberPTParser#lennard_jones_acoef_statement.
    def exitLennard_jones_acoef_statement(self, ctx: AmberPTParser.Lennard_jones_acoef_statementContext):
        if ctx.Real(0):
            return
        self.lennardJonesAcoefStatements -= 1

    # Enter a parse tree produced by AmberPTParser#lennard_jones_bcoef_statement.
    def enterLennard_jones_bcoef_statement(self, ctx: AmberPTParser.Lennard_jones_bcoef_statementContext):  # pylint: disable=unused-argument
        self.lennardJonesBcoefStatements += 1

    # Exit a parse tree produced by AmberPTParser#lennard_jones_bcoef_statement.
    def exitLennard_jones_bcoef_statement(self, ctx: AmberPTParser.Lennard_jones_bcoef_statementContext):
        if ctx.Real(0):
            return
        self.lennardJonesBcoefStatements -= 1

    # Enter a parse tree produced by AmberPTParser#mass_statement.
    def enterMass_statement(self, ctx: AmberPTParser.Mass_statementContext):  # pylint: disable=unused-argument
        self.massStatements += 1

    # Exit a parse tree produced by AmberPTParser#mass_statement.
    def exitMass_statement(self, ctx: AmberPTParser.Mass_statementContext):
        if ctx.Real(0):
            return
        self.massStatements -= 1

    # Enter a parse tree produced by AmberPTParser#nonbonded_parm_index_statement.
    def enterNonbonded_parm_index_statement(self, ctx: AmberPTParser.Nonbonded_parm_index_statementContext):  # pylint: disable=unused-argument
        self.nonbondedParmIndexStatements += 1

    # Exit a parse tree produced by AmberPTParser#nonbonded_parm_index_statement.
    def exitNonbonded_parm_index_statement(self, ctx: AmberPTParser.Nonbonded_parm_index_statementContext):
        if ctx.Integer(0):
            return
        self.nonbondedParmIndexStatements -= 1

    # Enter a parse tree produced by AmberPTParser#number_excluded_atoms_statement.
    def enterNumber_excluded_atoms_statement(self, ctx: AmberPTParser.Number_excluded_atoms_statementContext):  # pylint: disable=unused-argument
        self.numberExcludedAtomsStatements += 1

    # Exit a parse tree produced by AmberPTParser#number_excluded_atoms_statement.
    def exitNumber_excluded_atoms_statement(self, ctx: AmberPTParser.Number_excluded_atoms_statementContext):
        if ctx.Integer(0):
            return
        self.numberExcludedAtomsStatements -= 1

    # Enter a parse tree produced by AmberPTParser#pointers_statement.
    def enterPointers_statement(self, ctx: AmberPTParser.Pointers_statementContext):  # pylint: disable=unused-argument
        self.pointersStatements += 1

    # Exit a parse tree produced by AmberPTParser#pointers_statement.
    def exitPointers_statement(self, ctx: AmberPTParser.Pointers_statementContext):
        if ctx.Integer(0):
            return
        self.pointersStatements -= 1

    # Enter a parse tree produced by AmberPTParser#polarizability_statement.
    def enterPolarizability_statement(self, ctx: AmberPTParser.Polarizability_statementContext):  # pylint: disable=unused-argument
        self.polarizabilityStatements += 1

    # Exit a parse tree produced by AmberPTParser#polarizability_statement.
    def exitPolarizability_statement(self, ctx: AmberPTParser.Polarizability_statementContext):
        if ctx.Real(0):
            return
        self.polarizabilityStatements -= 1

    # Enter a parse tree produced by AmberPTParser#radii_statement.
    def enterRadii_statement(self, ctx: AmberPTParser.Radii_statementContext):  # pylint: disable=unused-argument
        self.radiiStatements += 1

    # Exit a parse tree produced by AmberPTParser#radii_statement.
    def exitRadii_statement(self, ctx: AmberPTParser.Radii_statementContext):
        if ctx.Real(0):
            return
        self.radiiStatements -= 1

    # Enter a parse tree produced by AmberPTParser#radius_set_statement.
    def enterRadius_set_statement(self, ctx: AmberPTParser.Radius_set_statementContext):  # pylint: disable=unused-argument
        self.radiusSetStatements += 1

    # Exit a parse tree produced by AmberPTParser#radius_set_statement.
    def exitRadius_set_statement(self, ctx: AmberPTParser.Radius_set_statementContext):
        if ctx.Simple_name(0):
            if self.hasCoord:
                radiusSet = []
                i = 0
                while ctx.Simple_name(i):
                    radiusSet.append(str(ctx.Simple_name(i)))
                    i += 1

                self.__radiusSet = ' '.join(radiusSet)
            return
        self.radiusSetStatements -= 1

    # Enter a parse tree produced by AmberPTParser#residue_label_statement.
    def enterResidue_label_statement(self, ctx: AmberPTParser.Residue_label_statementContext):  # pylint: disable=unused-argument
        self.residueLabelStatements += 1

        self.__residueLabel = []

    # Exit a parse tree produced by AmberPTParser#residue_label_statement.
    def exitResidue_label_statement(self, ctx: AmberPTParser.Residue_label_statementContext):
        if ctx.Simple_name(0):
            if self.hasCoord:
                i = 0
                while ctx.Simple_name(i):
                    self.__residueLabel += chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len)
                    if self.noWaterMol and (self.__residueLabel[-1] in ('HOH', 'H2O', 'WAT')
                                            or (len(self.__residueLabel[-1]) > 3 and self.__residueLabel[:3] in ('HOH', 'H2O', 'WAT'))):
                        break
                    # self.__residueLabel.extend(chunk_string(str(ctx.Simple_name(i)).upper(), self.__cur_word_len))
                    i += 1
            return
        self.residueLabelStatements -= 1

    # Enter a parse tree produced by AmberPTParser#residue_pointer_statement.
    def enterResidue_pointer_statement(self, ctx: AmberPTParser.Residue_pointer_statementContext):  # pylint: disable=unused-argument
        self.residuePointerStatements += 1

        self.__residuePointer = []

    # Exit a parse tree produced by AmberPTParser#residue_pointer_statement.
    def exitResidue_pointer_statement(self, ctx: AmberPTParser.Residue_pointer_statementContext):
        if ctx.Integer(0):
            if self.hasCoord:
                i = 0
                while ctx.Integer(i):
                    self.__residuePointer.append(int(str(ctx.Integer(i))))
                    i += 1
            return
        self.residueLabelStatements -= 1

    # Enter a parse tree produced by AmberPTParser#scee_scale_factor_statement.
    def enterScee_scale_factor_statement(self, ctx: AmberPTParser.Scee_scale_factor_statementContext):  # pylint: disable=unused-argument
        self.sceeScaleFactorStatements += 1

    # Exit a parse tree produced by AmberPTParser#scee_scale_factor_statement.
    def exitScee_scale_factor_statement(self, ctx: AmberPTParser.Scee_scale_factor_statementContext):
        if ctx.Real(0):
            return
        self.sceeScaleFactorStatements -= 1

    # Enter a parse tree produced by AmberPTParser#scnb_scale_factor_statement.
    def enterScnb_scale_factor_statement(self, ctx: AmberPTParser.Scnb_scale_factor_statementContext):  # pylint: disable=unused-argument
        self.scnbScaleFactorStatements += 1

    # Exit a parse tree produced by AmberPTParser#scnb_scale_factor_statement.
    def exitScnb_scale_factor_statement(self, ctx: AmberPTParser.Scnb_scale_factor_statementContext):
        if ctx.Real(0):
            return
        self.scnbScaleFactorStatements -= 1

    # Enter a parse tree produced by AmberPTParser#screen_statement.
    def enterScreen_statement(self, ctx: AmberPTParser.Screen_statementContext):  # pylint: disable=unused-argument
        self.screenStatements += 1

    # Exit a parse tree produced by AmberPTParser#screen_statement.
    def exitScreen_statement(self, ctx: AmberPTParser.Screen_statementContext):
        if ctx.Real(0):
            return
        self.screenStatements -= 1

    # Enter a parse tree produced by AmberPTParser#solty_statement.
    def enterSolty_statement(self, ctx: AmberPTParser.Solty_statementContext):  # pylint: disable=unused-argument
        self.soltyStatements += 1

    # Exit a parse tree produced by AmberPTParser#solty_statement.
    def exitSolty_statement(self, ctx: AmberPTParser.Solty_statementContext):
        if ctx.Real(0):
            return
        self.soltyStatements -= 1

    # Enter a parse tree produced by AmberPTParser#solvent_pointers_statement.
    def enterSolvent_pointers_statement(self, ctx: AmberPTParser.Solvent_pointers_statementContext):  # pylint: disable=unused-argument
        self.solventPointersStatements += 1

    # Exit a parse tree produced by AmberPTParser#solvent_pointers_statement.
    def exitSolvent_pointers_statement(self, ctx: AmberPTParser.Solvent_pointers_statementContext):
        if ctx.Integer(0):
            return
        self.solventPointersStatements -= 1

    # Enter a parse tree produced by AmberPTParser#title_statement.
    def enterTitle_statement(self, ctx: AmberPTParser.Title_statementContext):  # pylint: disable=unused-argument
        self.titleStatements += 1

    # Exit a parse tree produced by AmberPTParser#title_statement.
    def exitTitle_statement(self, ctx: AmberPTParser.Title_statementContext):
        if ctx.Simple_name(0):
            if self.hasCoord:
                title = []
                i = 0
                while ctx.Simple_name(i):
                    title.append(str(ctx.Simple_name(i)))
                    i += 1

                self.__title = ' '.join(title)
            return
        self.titleStatements -= 1

    # Enter a parse tree produced by AmberPTParser#tree_chain_classification_statement.
    def enterTree_chain_classification_statement(self, ctx: AmberPTParser.Tree_chain_classification_statementContext):  # pylint: disable=unused-argument
        self.treeChainClassificationStatements += 1

    # Exit a parse tree produced by AmberPTParser#tree_chain_classification_statement.
    def exitTree_chain_classification_statement(self, ctx: AmberPTParser.Tree_chain_classification_statementContext):
        if ctx.Simple_name(0):
            return
        self.treeChainClassificationStatements -= 1

    # Enter a parse tree produced by AmberPTParser#format_function.
    def enterFormat_function(self, ctx: AmberPTParser.Format_functionContext):

        try:

            if ctx.Fortran_format_A():
                g = self.__a_format_pat.search(str(ctx.Fortran_format_A())).groups()
                # self.__cur_column_len = int(g[0])
                self.__cur_word_len = int(g[1])
            elif ctx.Fortran_format_I():
                g = self.__i_format_pat.search(str(ctx.Fortran_format_I())).groups()
                # self.__cur_column_len = int(g[0])
                self.__cur_word_len = int(g[1])
            else:
                g = self.__e_format_pat.search(str(ctx.Fortran_format_E())).groups()
                # self.__cur_column_len = int(g[0])
                self.__cur_word_len = int(g[1])

        except AttributeError:
            # self.__cur_column_len = None
            self.__cur_word_len = None

    # Exit a parse tree produced by AmberPTParser#format_function.
    def exitFormat_function(self, ctx: AmberPTParser.Format_functionContext):  # pylint: disable=unused-argument
        pass

    def getContentSubtype(self) -> dict:
        """ Return content subtype of AMBER parameter/topology file.
        """

        contentSubtype = {'version': self.versionStatements,
                          'amber_atom_type': self.amberAtomTypeStatements,
                          'angle_equil_value': self.angleEquilValueStatements,
                          'angle_force_constant': self.angleForceConstantStatements,
                          'angles_inc_hydrogen': self.anglesIncHydrogenStatements,
                          'angles_without_hydrogen': self.anglesWithoutHydrogenStatements,
                          'atomic_number': self.atomicNumberStatements,
                          'atom_name': self.atomNameStatements,
                          'atom_type_index': self.atomTypeIndexStatements,
                          'atoms_per_molecule': self.atomsPerMoleculeStatements,
                          'bond_equil_value': self.bondEquilValueStatements,
                          'bond_force_constant': self.bondForceConstantStatements,
                          'bonds_inc_hydrogen': self.bondsIncHydrogenStatements,
                          'bonds_without_hydrogen': self.bondsWithoutHydrogenStatements,
                          'box_dimensions': self.boxDimensionsStatements,
                          'cap_info': self.capInfoStatements,
                          'cap_info2': self.capInfo2Statements,
                          'charge': self.chargeStatements,
                          'cmap_count': self.cmapCountStatements,
                          'cmap_resolution': self.cmapResolutionStatements,
                          'cmap_parameter': self.cmapParameterStatements,
                          'cmap_index': self.cmapIndexStatements,
                          'dihedral_force_constant': self.dihedralForceConstantStatements,
                          'dihedral_periodicity': self.dihedralPeriodicityStatements,
                          'dihedral_phase': self.dihedralPhaseStatements,
                          'dihedrals_inc_hydrogen': self.dihedralsIncHydrogenStatements,
                          'dihedrals_without_hydrogen': self.dihedralsWithoutHydrogenStatements,
                          'excluded_atoms_list': self.excludedAtomsListStatements,
                          'hbcut': self.hbcutStatements,
                          'hbond_acoef': self.hbondAcoefStatements,
                          'hbond_bcoef': self.hbondBcoefStatements,
                          'ipol': self.ipolStatements,
                          'irotat': self.irotatStatements,
                          'join_array': self.joinArrayStatements,
                          'lennard_jones_acoef': self.lennardJonesAcoefStatements,
                          'lennard_jones_bcoef': self.lennardJonesBcoefStatements,
                          'mass': self.massStatements,
                          'nonbonded_parm_index': self.nonbondedParmIndexStatements,
                          'number_excluded_atoms': self.numberExcludedAtomsStatements,
                          'pointers': self.pointersStatements,
                          'polarizability': self.polarizabilityStatements,
                          'radii': self.radiiStatements,
                          'radius_set': self.radiusSetStatements,
                          'residue_label': self.residueLabelStatements,
                          'residue_pointer': self.residuePointerStatements,
                          'scee_scale_factor': self.sceeScaleFactorStatements,
                          'scnb_scale_factor': self.scnbScaleFactorStatements,
                          'screen': self.screenStatements,
                          'solty': self.soltyStatements,
                          'solvent_pointers': self.solventPointersStatements,
                          'title': self.titleStatements,
                          'tree_chain_classification': self.treeChainClassificationStatements
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getVersionInfo(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """ Return version information of AMBER parameter/topology file.
            @return: version, date, time
        """

        return self.__version, self.__date, self.__time

    def getTitle(self) -> Optional[str]:
        """ Return title of AMBER parameter/topology file.
        """

        return self.__title

    def getRadiusSet(self) -> Optional[str]:
        """ Return radius set of AMBER parameter/topology file.
        """

        return self.__radiusSet

# del AmberPTParser
