##
# File: SchrodingerMRParserListener.py
# Date: 05-Aug-2025
#
# Updates:
""" ParserLister class for SCHRODINGER MR files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import re
import itertools
import copy
import collections

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import (int_atom, ELEMENT_WEIGHTS)  # noqa: F401 pylint: disable=no-name-in-module, import-error
from operator import itemgetter
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.SchrodingerMRParser import SchrodingerMRParser
    from wwpdb.utils.nmr.mr.BaseStackedMRParserListener import BaseStackedMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx,
                                                       hasInterChainRestraint,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       isDefinedSegmentRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       getRow,
                                                       getStarAtom,
                                                       resetCombinationId,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getDstFuncForHBond,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                                       CARTN_DATA_ITEMS,
                                                       AUTH_ATOM_DATA_ITEMS,
                                                       AUTH_ATOM_CARTN_DATA_ITEMS)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (emptyValue,
                                           monDict3,
                                           deepcopy,
                                           getOneLetterCode,
                                           protonBeginCode,
                                           updatePolySeqRstFromAtomSelectionSet)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.SchrodingerMRParser import SchrodingerMRParser
    from nmr.mr.BaseStackedMRParserListener import BaseStackedMRParserListener
    from nmr.mr.ParserListenerUtil import (toRegEx,
                                           hasInterChainRestraint,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           isDefinedSegmentRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRow,
                                           getStarAtom,
                                           resetCombinationId,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getDstFuncForHBond,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                           CARTN_DATA_ITEMS,
                                           AUTH_ATOM_DATA_ITEMS,
                                           AUTH_ATOM_CARTN_DATA_ITEMS)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (emptyValue,
                               monDict3,
                               deepcopy,
                               getOneLetterCode,
                               protonBeginCode,
                               updatePolySeqRstFromAtomSelectionSet)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance)


# This class defines a complete listener for a parse tree produced by SchrodingerMRParser.
class SchrodingerMRParserListener(ParseTreeListener, BaseStackedMRParserListener):
    __slots__ = ('__atomNumberDict', )

    __compIdSet = None
    __altCompIdSet = None
    __cyanaCompIdSet = None

    # store set
    __cur_store_name = ''

    __asl_int_range_pat = re.compile(r'^(-?\\d+)-(-?\\d+)')

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None,
                 atomNumberDict: Optional[dict] = None, reasons: Optional[dict] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        super().__init__(verbose, log, representativeModelId, representativeAltId, mrAtomNameMapping,
                         cR, caC, nefT, reasons)

        self.file_type = 'nm-res-sch'
        self.software_name = 'SCHRODINGER/ASL'

        if atomNumberDict is not None:
            self.__atomNumberDict = atomNumberDict
            self.offsetHolder = None

        else:
            self.__atomNumberDict = {}

        self.storeSet = {}

    # Enter a parse tree produced by SchrodingerMRParser#schrodinger_mr
    def enterSchrodinger_mr(self, ctx: SchrodingerMRParser.Schrodinger_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#schrodinger_mr.
    def exitSchrodinger_mr(self, ctx: SchrodingerMRParser.Schrodinger_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by SchrodingerMRParser#import_structure.
    def enterImport_structure(self, ctx: SchrodingerMRParser.Import_structureContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#import_structure.
    def exitImport_structure(self, ctx: SchrodingerMRParser.Import_structureContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#struct_statement.
    def enterStruct_statement(self, ctx: SchrodingerMRParser.Struct_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#struct_statement.
    def exitStruct_statement(self, ctx: SchrodingerMRParser.Struct_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: SchrodingerMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: SchrodingerMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: SchrodingerMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: SchrodingerMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#angle_restraint.
    def enterAngle_restraint(self, ctx: SchrodingerMRParser.Angle_restraintContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#angle_restraint.
    def exitAngle_restraint(self, ctx: SchrodingerMRParser.Angle_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#distance_statement.
    def enterDistance_statement(self, ctx: SchrodingerMRParser.Distance_statementContext):  # pylint: disable=unused-argument
        self.distStatements += 1
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#distance_statement.
    def exitDistance_statement(self, ctx: SchrodingerMRParser.Distance_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#distance_assign.
    def enterDistance_assign(self, ctx: SchrodingerMRParser.Distance_assignContext):  # pylint: disable=unused-argument
        self.distRestraints += 1
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        if self.cur_subtype_altered:
            self.distStatements += 1
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        self.atomSelectionSet.clear()
        self.g.clear()

        self.has_nx = False

    # Exit a parse tree produced by SchrodingerMRParser#distance_assign.
    def exitDistance_assign(self, ctx: SchrodingerMRParser.Distance_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            fc = self.numberSelection[2]

            if fc < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The force constant '{fc}' must not be a negative value.")
                return
            if fc == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The force constant '{fc}' should be a positive value.")

            target_value = lower_linear_limit = upper_linear_limit = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.allowZeroUpperLimit = False
            if self.reasons is not None and 'model_chain_id_ext' in self.reasons\
               and len(self.atomSelectionSet[0]) > 0\
               and len(self.atomSelectionSet[0]) == len(self.atomSelectionSet[1]):
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if chain_id_1 != chain_id_2 and seq_id_1 == seq_id_2 and atom_id_1 == atom_id_2\
                   and ((chain_id_1 in self.reasons['model_chain_id_ext'] and chain_id_2 in self.reasons['model_chain_id_ext'][chain_id_1])
                        or (chain_id_2 in self.reasons['model_chain_id_ext'] and chain_id_1 in self.reasons['model_chain_id_ext'][chain_id_2])):
                    self.allowZeroUpperLimit = True
            self.allowZeroUpperLimit |= hasInterChainRestraint(self.atomSelectionSet)

            dstFunc = self.validateDistanceRange(1.0,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit, fc)

            if dstFunc is None:
                return

            if 0 in (len(self.atomSelectionSet[0]), len(self.atomSelectionSet[1])):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName))
                sf['id'] += 1
                if len(self.atomSelectionSet) > 2:
                    combinationId = 0
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0

            if self.reasons is None\
               and 'segment_id' in self.atomSelectionSet[0][0] and 'segment_id' in self.atomSelectionSet[1][0]\
               and self.atomSelectionSet[0][0]['segment_id'] != self.atomSelectionSet[1][0]['segment_id']\
               and 'assert_uniq_segment_id' not in self.reasonsForReParsing:
                self.reasonsForReParsing['assert_uniq_segment_id'] = True
            assert_uniq_segment_id = self.reasons is not None and 'assert_uniq_segment_id' in self.reasons

            for i in range(0, len(self.atomSelectionSet), 2):
                if isinstance(combinationId, int):
                    combinationId += 1
                if isinstance(memberId, int):
                    memberId = 0
                    _atom1 = _atom2 = None
                if self.createSfDict:
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[i]) * len(self.atomSelectionSet[i + 1]) > 1 else '.'
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
                    atoms = [atom1, atom2]
                    if isDefinedSegmentRestraint(atoms):
                        continue
                    if isIdenticalRestraint(atoms, self.nefT, assert_uniq_segment_id):
                        continue
                    if self.createSfDict and isinstance(memberId, int):
                        star_atom1 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom1))
                        star_atom2 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom2))
                        if None in (star_atom1, star_atom2) or isIdenticalRestraint([star_atom1, star_atom2], self.nefT):
                            continue
                    if self.createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint(atoms, self.csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if len(self.fibril_chain_ids) > 0\
                       and atom1['chain_id'] in self.fibril_chain_ids\
                       and atom2['chain_id'] in self.fibril_chain_ids\
                       and not self.isRealisticDistanceRestraint(atom1, atom2, dstFunc):
                        continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (DIST) id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        if isinstance(memberId, int):
                            if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                               or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                                memberId += 1
                                _atom1, _atom2 = atom1, atom2
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     combinationId, memberId, memberLogicCode,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)

                        if sf['constraint_subsubtype'] == 'ambi':
                            continue

                        if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                            sf['constraint_subsubtype'] = 'ambi'

                        if isinstance(combinationId, int)\
                           or (memberLogicCode == 'OR'
                               and (isAmbigAtomSelection(self.atomSelectionSet[i], self.csStat)
                                    or isAmbigAtomSelection(self.atomSelectionSet[i + 1], self.csStat))):
                            sf['constraint_subsubtype'] = 'ambi'

                        if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                            upperLimit = float(dstFunc['upper_limit'])
                            if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                                sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None:
                if isinstance(memberId, int) and memberId == 1:
                    sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])
                    memberId = '.'
                if isinstance(memberId, str) and isinstance(combinationId, int) and combinationId == 1:
                    sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Exit a parse tree produced by SchrodingerMRParser#distance_assign_by_number.
    def enterDistance_assign_by_number(self, ctx: SchrodingerMRParser.Distance_assign_by_numberContext):
        self.distRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXDI' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.distRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")
                    self.distRestraints -= 1

    # Exit a parse tree produced by SchrodingerMRParser#distance_assign_by_number.
    def exitDistance_assign_by_number(self, ctx: SchrodingerMRParser.Distance_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#dihedral_angle_statement.
    def enterDihedral_angle_statement(self, ctx: SchrodingerMRParser.Dihedral_angle_statementContext):  # pylint: disable=unused-argument
        self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#dihedral_angle_statement.
    def exitDihedral_angle_statement(self, ctx: SchrodingerMRParser.Dihedral_angle_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#dihedral_angle_assign.
    def enterDihedral_angle_assign(self, ctx: SchrodingerMRParser.Dihedral_angle_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1
        if self.cur_subtype != 'dihed':
            self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by SchrodingerMRParser#dihedral_angle_assign.
    def exitDihedral_angle_assign(self, ctx: SchrodingerMRParser.Dihedral_angle_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target = self.numberSelection[0]
            fc = self.numberSelection[1]

            if fc <= 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The energy constant value {fc} must be a positive value.")
                return

            target_value = target
            lower_limit = upper_limit = lower_linear_limit = upper_linear_limit = None

            dstFunc = self.validateAngleRange(1.0, {'energy_const': fc},
                                              target_value, lower_limit, upper_limit,
                                              lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                if not self.areUniqueCoordAtoms('a dihedral angle (TORS)'):
                    if len(self.g) > 0:
                        self.f.extend(self.g)
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a dihedral angle (TORS)',
                                     allow_ambig=True, allow_ambig_warn_title='Ambiguous dihedral angle')
            combinationId = '.' if len_f == len(self.f) else 0

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

            if isinstance(combinationId, int):
                fixedAngleName = '.'
                for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                    self.atomSelectionSet[1],
                                                                    self.atomSelectionSet[2],
                                                                    self.atomSelectionSet[3]):
                    atoms = [atom1, atom2, atom3, atom4]
                    angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                           atoms,
                                                           'plane_like' in dstFunc,
                                                           self.cR, self.ccU,
                                                           self.representativeModelId, self.representativeAltId, self.modelNumName)

                    if angleName is not None and angleName.startswith('pseudo'):
                        angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(angleName,
                                                                                           atoms,
                                                                                           self.getCurrentRestraint())
                        self.f.append(err)

                    if angleName in emptyValue and atomSelTotal != 4:
                        continue

                    fixedAngleName = angleName
                    break

            sf = None
            if self.createSfDict:
                sf = self.getSf()

            first_item = True

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                atoms = [atom1, atom2, atom3, atom4]
                angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                       atoms,
                                                       'plane_like' in dstFunc,
                                                       self.cR, self.ccU,
                                                       self.representativeModelId, self.representativeAltId, self.modelNumName)

                if angleName is not None and angleName.startswith('pseudo'):
                    angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(angleName,
                                                                                       atoms,
                                                                                       self.getCurrentRestraint())
                    self.f.append(err)

                if angleName in emptyValue and atomSelTotal != 4:
                    continue

                if isinstance(combinationId, int):
                    if angleName != fixedAngleName:
                        continue
                    combinationId += 1
                if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                    dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                      dstFunc)
                if self.debug:
                    print(f"subtype={self.cur_subtype} (TORS) id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, angleName,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by SchrodingerMRParser#dihedral_angle_assign_by_number.
    def enterDihedral_angle_assign_by_number(self, ctx: SchrodingerMRParser.Dihedral_angle_assign_by_numberContext):
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1))), int(str(ctx.Integer(2))), int(str(ctx.Integer(3)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXTA' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.dihedRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")
                    self.dihedRestraints -= 1

    # Exit a parse tree produced by SchrodingerMRParser#dihedral_angle_assign_by_number.
    def exitDihedral_angle_assign_by_number(self, ctx: SchrodingerMRParser.Dihedral_angle_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#angle_statement.
    def enterAngle_statement(self, ctx: SchrodingerMRParser.Angle_statementContext):  # pylint: disable=unused-argument
        self.angStatements += 1
        self.cur_subtype = 'ang'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#angle_statement.
    def exitAngle_statement(self, ctx: SchrodingerMRParser.Angle_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#angle_assign.
    def enterAngle_assign(self, ctx: SchrodingerMRParser.Angle_assignContext):  # pylint: disable=unused-argument
        self.angRestraints += 1
        if self.cur_subtype != 'ang':
            self.angStatements += 1
        self.cur_subtype = 'ang'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by SchrodingerMRParser#angle_assign.
    def exitAngle_assign(self, ctx: SchrodingerMRParser.Angle_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.angRestraints -= 1
                return

            target_value = self.numberSelection[0]
            fc = self.numberSelection[1]

            if fc <= 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The energy constant value {fc} must be a positive value.")
                return

            lower_limit = upper_limit = None

            dstFunc = self.validateAngleRange(1.0, {'energy_const': fc}, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a angle (ANGLE)'):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            if self.createSfDict:
                sf = self.getSf('angle restraint')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                          'target_value', 'target_value_uncertainty',
                                          'lower_linear_limit', 'lower_limit', 'upper_limit', 'upper_linear_limit',
                                          'force_constant',
                                          'list_id']

            updatePolySeqRstFromAtomSelectionSet(self.polySeqRst, self.atomSelectionSet)

            for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[0],
                                                         self.atomSelectionSet[1],
                                                         self.atomSelectionSet[2]):
                if isLongRangeRestraint([atom1, atom2, atom3], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.angRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                               dstFunc.get('target_value'), None,
                                               dstFunc.get('lower_linear_limit'),
                                               dstFunc.get('lower_limit'),
                                               dstFunc.get('upper_limit'),
                                               dstFunc.get('upper_linear_limit'),
                                               fc,
                                               sf['list_id']])

        except ValueError:
            self.angRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by SchrodingerMRParser#angle_assign_by_number.
    def enterAngle_assign_by_number(self, ctx: SchrodingerMRParser.Angle_assign_by_numberContext):
        self.angRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1))), int(str(ctx.Integer(2)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXBA' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.distRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")
                    self.distRestraints -= 1

    # Exit a parse tree produced by SchrodingerMRParser#angle_assign_by_number.
    def exitAngle_assign_by_number(self, ctx: SchrodingerMRParser.Angle_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#fxdi_statement.
    def enterFxdi_statement(self, ctx: SchrodingerMRParser.Fxdi_statementContext):  # pylint: disable=unused-argument
        self.distStatements += 1
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#fxdi_statement.
    def exitFxdi_statement(self, ctx: SchrodingerMRParser.Fxdi_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#fxdi_assign.
    def enterFxdi_assign(self, ctx: SchrodingerMRParser.Fxdi_assignContext):  # pylint: disable=unused-argument
        self.distRestraints += 1
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        if self.cur_subtype_altered:
            self.distStatements += 1
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        self.atomSelectionSet.clear()
        self.g.clear()

        self.has_nx = False

    # Exit a parse tree produced by SchrodingerMRParser#fxdi_assign.
    def exitFxdi_assign(self, ctx: SchrodingerMRParser.Fxdi_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            target_value = self.numberSelection[1]

            if target_value <= 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target distance '{target_value}' should be a positive value because we cannot refer the initial coordinates.")
                return

            delta = abs(self.numberSelection[2])

            lower_limit = upper_limit = None
            if delta > 0.0:
                lower_limit = target_value - delta
                upper_limit = target_value + delta

            fc = self.numberSelection[0]

            if fc < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The force constant '{fc}' must not be a negative value.")
                return
            if fc == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The force constant '{fc}' should be a positive value.")

            lower_linear_limit = upper_linear_limit = None

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.allowZeroUpperLimit = False
            if self.reasons is not None and 'model_chain_id_ext' in self.reasons\
               and len(self.atomSelectionSet[0]) > 0\
               and len(self.atomSelectionSet[0]) == len(self.atomSelectionSet[1]):
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if chain_id_1 != chain_id_2 and seq_id_1 == seq_id_2 and atom_id_1 == atom_id_2\
                   and ((chain_id_1 in self.reasons['model_chain_id_ext'] and chain_id_2 in self.reasons['model_chain_id_ext'][chain_id_1])
                        or (chain_id_2 in self.reasons['model_chain_id_ext'] and chain_id_1 in self.reasons['model_chain_id_ext'][chain_id_2])):
                    self.allowZeroUpperLimit = True
            self.allowZeroUpperLimit |= hasInterChainRestraint(self.atomSelectionSet)

            dstFunc = self.validateDistanceRange(1.0,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit, fc)

            if dstFunc is None:
                return

            if 0 in (len(self.atomSelectionSet[0]), len(self.atomSelectionSet[1])):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName))
                sf['id'] += 1
                if len(self.atomSelectionSet) > 2:
                    combinationId = 0
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0

            if self.reasons is None\
               and 'segment_id' in self.atomSelectionSet[0][0] and 'segment_id' in self.atomSelectionSet[1][0]\
               and self.atomSelectionSet[0][0]['segment_id'] != self.atomSelectionSet[1][0]['segment_id']\
               and 'assert_uniq_segment_id' not in self.reasonsForReParsing:
                self.reasonsForReParsing['assert_uniq_segment_id'] = True
            assert_uniq_segment_id = self.reasons is not None and 'assert_uniq_segment_id' in self.reasons

            for i in range(0, len(self.atomSelectionSet), 2):
                if isinstance(combinationId, int):
                    combinationId += 1
                if isinstance(memberId, int):
                    memberId = 0
                    _atom1 = _atom2 = None
                if self.createSfDict:
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[i]) * len(self.atomSelectionSet[i + 1]) > 1 else '.'
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
                    atoms = [atom1, atom2]
                    if isDefinedSegmentRestraint(atoms):
                        continue
                    if isIdenticalRestraint(atoms, self.nefT, assert_uniq_segment_id):
                        continue
                    if self.createSfDict and isinstance(memberId, int):
                        star_atom1 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom1))
                        star_atom2 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom2))
                        if None in (star_atom1, star_atom2) or isIdenticalRestraint([star_atom1, star_atom2], self.nefT):
                            continue
                    if self.createSfDict and memberLogicCode == '.':
                        altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint(atoms, self.csStat)
                        if altAtomId1 is not None or altAtomId2 is not None:
                            atom1, atom2 =\
                                self.selectRealisticBondConstraint(atom1, atom2,
                                                                   altAtomId1, altAtomId2,
                                                                   dstFunc)
                    if len(self.fibril_chain_ids) > 0\
                       and atom1['chain_id'] in self.fibril_chain_ids\
                       and atom2['chain_id'] in self.fibril_chain_ids\
                       and not self.isRealisticDistanceRestraint(atom1, atom2, dstFunc):
                        continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (FXDI) id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        if isinstance(memberId, int):
                            if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                               or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                                memberId += 1
                                _atom1, _atom2 = atom1, atom2
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     combinationId, memberId, memberLogicCode,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)

                        if sf['constraint_subsubtype'] == 'ambi':
                            continue

                        if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                            sf['constraint_subsubtype'] = 'ambi'

                        if isinstance(combinationId, int)\
                           or (memberLogicCode == 'OR'
                               and (isAmbigAtomSelection(self.atomSelectionSet[i], self.csStat)
                                    or isAmbigAtomSelection(self.atomSelectionSet[i + 1], self.csStat))):
                            sf['constraint_subsubtype'] = 'ambi'

                        if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                            upperLimit = float(dstFunc['upper_limit'])
                            if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                                sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None:
                if isinstance(memberId, int) and memberId == 1:
                    sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])
                    memberId = '.'
                if isinstance(memberId, str) and isinstance(combinationId, int) and combinationId == 1:
                    sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by SchrodingerMRParser#fxdi_assign_by_number.
    def enterFxdi_assign_by_number(self, ctx: SchrodingerMRParser.Fxdi_assign_by_numberContext):
        self.distRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXDI' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.distRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")

            self.exitFxdi_assign(ctx)

    # Exit a parse tree produced by SchrodingerMRParser#fxdi_assign_by_number.
    def exitFxdi_assign_by_number(self, ctx: SchrodingerMRParser.Fxdi_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#fxta_statement.
    def enterFxta_statement(self, ctx: SchrodingerMRParser.Fxta_statementContext):  # pylint: disable=unused-argument
        self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#fxta_statement.
    def exitFxta_statement(self, ctx: SchrodingerMRParser.Fxta_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#fxta_assign.
    def enterFxta_assign(self, ctx: SchrodingerMRParser.Fxta_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1
        if self.cur_subtype != 'dihed':
            self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by SchrodingerMRParser#fxta_assign.
    def exitFxta_assign(self, ctx: SchrodingerMRParser.Fxta_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = self.numberSelection[1]

            if target_value > 360.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target angle '{target_value}' should be less than 360.0 because we cannot refer the initial coordinates.")
                return

            delta = abs(self.numberSelection[2])

            lower_limit = upper_limit = None
            if delta > 0.0:
                lower_limit = target_value - delta
                upper_limit = target_value + delta

            fc = self.numberSelection[0]

            if fc <= 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The energy constant value {fc} must be a positive value.")
                return

            lower_linear_limit = upper_linear_limit = None

            multiplicity = int(self.numberSelection[4])

            if multiplicity <= 0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The multiplicity of angle restraint '{multiplicity}' must be a positive integer.")
                return

            dstFunc = self.validateAngleRange(1.0, {'energy_const': fc},
                                              target_value, lower_limit, upper_limit,
                                              lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                if not self.areUniqueCoordAtoms('a dihedral angle (FXTA)'):
                    if len(self.g) > 0:
                        self.f.extend(self.g)
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a dihedral angle (FXTA)',
                                     allow_ambig=True, allow_ambig_warn_title='Ambiguous dihedral angle')
            combinationId = '.' if len_f == len(self.f) else 0

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

            if isinstance(combinationId, int):
                fixedAngleName = '.'
                for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                    self.atomSelectionSet[1],
                                                                    self.atomSelectionSet[2],
                                                                    self.atomSelectionSet[3]):
                    atoms = [atom1, atom2, atom3, atom4]
                    angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                           atoms,
                                                           'plane_like' in dstFunc,
                                                           self.cR, self.ccU,
                                                           self.representativeModelId, self.representativeAltId, self.modelNumName)

                    if angleName is not None and angleName.startswith('pseudo'):
                        angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(angleName,
                                                                                           atoms,
                                                                                           self.getCurrentRestraint())
                        self.f.append(err)

                    if angleName in emptyValue and atomSelTotal != 4:
                        continue

                    fixedAngleName = angleName
                    break

            if multiplicity > 1:
                combinationId = 0

            sf = None
            if self.createSfDict:
                sf = self.getSf()

            first_item = True

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                atoms = [atom1, atom2, atom3, atom4]
                angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                       atoms,
                                                       'plane_like' in dstFunc,
                                                       self.cR, self.ccU,
                                                       self.representativeModelId, self.representativeAltId, self.modelNumName)

                if angleName is not None and angleName.startswith('pseudo'):
                    angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(angleName,
                                                                                       atoms,
                                                                                       self.getCurrentRestraint())
                    self.f.append(err)

                if angleName in emptyValue and atomSelTotal != 4:
                    continue

                if isinstance(combinationId, int):
                    if angleName != fixedAngleName:
                        continue
                    combinationId += 1
                if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                    dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                      dstFunc)
                if self.debug:
                    print(f"subtype={self.cur_subtype} (FXTA) id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} multiplicity={multiplicity} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if multiplicity > 1:
                        _atoms = str(atoms)
                        if _atoms in self.atomSelectionSetForFxta:
                            sf_id = self.atomSelectionSetForFxta[_atoms]['id']
                            self.atomSelectionSetForFxta[_atoms]['cimbination_id'] += 1
                            combinationId = self.atomSelectionSetForFxta[_atoms]['cimbination_id']
                        else:
                            sf['id'] += 1
                            sf_id = sf['id']
                            self.atomSelectionSetForFxta[_atoms] = {'id': sf_id,
                                                                    'combination_id': combinationId}
                    elif first_item:
                        sf['id'] += 1
                        sf_id = sf['id']
                        first_item = False
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf_id, sf['index_id'],
                                 combinationId, None, angleName,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1 and multiplicity == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by SchrodingerMRParser#fxta_assign_by_number.
    def enterFxta_assign_by_number(self, ctx: SchrodingerMRParser.Fxta_assign_by_numberContext):
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1))), int(str(ctx.Integer(2))), int(str(ctx.Integer(3)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXTA' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.dihedRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")

            self.exitFxta_assign(ctx)

    # Exit a parse tree produced by SchrodingerMRParser#fxba_assign_by_number.
    def exitFxba_assign_by_number(self, ctx: SchrodingerMRParser.Fxba_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#fxhb_statement.
    def enterFxhb_statement(self, ctx: SchrodingerMRParser.Fxhb_statementContext):  # pylint: disable=unused-argument
        self.dihedStatements += 1
        self.cur_subtype = 'hbond'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by SchrodingerMRParser#fxhb_statement.
    def exitFxhb_statement(self, ctx: SchrodingerMRParser.Fxhb_statementContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by SchrodingerMRParser#fxhb_assign.
    def enterFxhb_assign(self, ctx: SchrodingerMRParser.Fxhb_assignContext):  # pylint: disable=unused-argument
        self.hbondRestraints += 1
        if self.cur_subtype != 'hbond':
            self.hbondStatements += 1
        self.cur_subtype = 'hbond'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by SchrodingerMRParser#fxhb_assign.
    def exitFxhb_assign(self, ctx: SchrodingerMRParser.Fxhb_assignContext):  # pylint: disable=unused-argument

        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a hydrogen bond (FXHB)'):
            if len(self.g) > 0:
                self.f.extend(self.g)
            return

        donor = self.atomSelectionSet[0][0]
        hydrogen = self.atomSelectionSet[1][0]
        acceptor = self.atomSelectionSet[2][0]

        is_hbond = True

        if donor['chain_id'] != hydrogen['chain_id']:
            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                          "The donor atom and its hygrogen are in different chains; "
                          f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                          f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
            return

        if donor['seq_id'] != hydrogen['seq_id']:
            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                          "The donor atom and its hygrogen are in different residues; "
                          f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                          f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
            return

        if hydrogen['atom_id'][0] not in protonBeginCode:
            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                          "Not a hydrogen; "
                          f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}. "
                          "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            return

        if donor['atom_id'][0] not in ('N', 'O', 'F'):
            self.f.append(f"[Unmatched atom type] {self.getCurrentRestraint()}"
                          "The donor atom type should be one of Nitrogen, Oxygen, Fluorine; "
                          f"{donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}. "
                          "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            is_hbond = False
            # return

        if acceptor['atom_id'][0] not in ('N', 'O', 'F'):
            self.f.append(f"[Unmatched atom type] {self.getCurrentRestraint()}"
                          "The acceptor atom type should be one of Nitrogen, Oxygen, Fluorine; "
                          f"{acceptor['chain_id']}:{acceptor['seq_id']}:{acceptor['comp_id']}:{acceptor['atom_id']}. "
                          "The XPLOR-NIH atom selections for hydrogen bond geometry restraint must be in the order of donor, hydrogen, and acceptor.")
            is_hbond = False
            # return

        comp_id = donor['comp_id']

        if self.ccU.updateChemCompDict(comp_id):  # matches with comp_id in CCD

            atom_id_1 = donor['atom_id']
            atom_id_2 = hydrogen['atom_id']

            if not self.ccU.hasBond(comp_id, atom_id_1, atom_id_2):

                if self.nefT.validate_comp_atom(comp_id, atom_id_1) and self.nefT.validate_comp_atom(comp_id, atom_id_2):
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found a donor-hydrogen vector over multiple covalent bonds in the 'HBDA' statement; "
                                  f"({donor['chain_id']}:{donor['seq_id']}:{donor['comp_id']}:{donor['atom_id']}, "
                                  f"{hydrogen['chain_id']}:{hydrogen['seq_id']}:{hydrogen['comp_id']}:{hydrogen['atom_id']}).")
                    return

        if not is_hbond:
            self.hbondRestraints -= 1
            self.distRestraints += 1
            if self.distStatements == 0:
                self.distStatements += 1
            self.cur_subtype = 'dist'

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
        seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
        atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

        try:

            _donor =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': chain_id_1},
                                               {'name': self.authSeqId, 'type': 'int', 'value': seq_id_1},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom_id_1},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            _hydrogen =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': chain_id_2},
                                               {'name': self.authSeqId, 'type': 'int', 'value': seq_id_2},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom_id_2},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            _acceptor =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': chain_id_3},
                                               {'name': self.authSeqId, 'type': 'int', 'value': seq_id_3},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom_id_3},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_donor) == 1 and len(_hydrogen) == 1 and len(_acceptor) == 1:
                dist = distance(to_np_array(_hydrogen[0]), to_np_array(_acceptor[0]))
                if dist > 2.5 and is_hbond:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The distance of the hydrogen bond linkage ({chain_id_2}:{seq_id_2}:{atom_id_2} - "
                                  f"{chain_id_3}:{seq_id_3}:{atom_id_3}) is too far apart in the coordinates ({dist:.3f}Å).")

                dist = distance(to_np_array(_donor[0]), to_np_array(_acceptor[0]))
                if dist > 3.5 and is_hbond:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                  f"{chain_id_3}:{seq_id_3}:{atom_id_3}) is too far apart in the coordinates ({dist:.3f}Å).")

        except Exception as e:
            if self.verbose:
                self.log.write(f"+{self.__class_name__}.exitFxhb_assign() ++ Error  - {str(e)}")

        if self.createSfDict:
            sf = self.getSf()
            sf['id'] += 1

        for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[0],
                                                     self.atomSelectionSet[1],
                                                     self.atomSelectionSet[2]):
            if isLongRangeRestraint([atom1, atom2], self.polySeq if self.gapInAuthSeq else None):
                continue
            if self.debug:
                print(f"subtype={self.cur_subtype} (FXHB) id={self.hbondRestraints} "
                      f"donor={atom1} hydrogen={atom2} acceptor={atom3}")
            if self.createSfDict and sf is not None:
                sf['index_id'] += 1
                memberLogicCode = 'AND'
                row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                             1, None, memberLogicCode,
                             sf['list_id'], self.entryId, getDstFuncForHBond(atom1, atom3),
                             self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                             atom1, atom3)
                sf['loop'].add_data(row)

                sf['index_id'] += 1
                memberLogicCode = 'AND'
                row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                             2, None, memberLogicCode,
                             sf['list_id'], self.entryId, getDstFuncForHBond(atom2, atom3),
                             self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                             atom2, atom3)
                sf['loop'].add_data(row)

        if not is_hbond:
            self.cur_subtype = 'hbond'

    # Enter a parse tree produced by SchrodingerMRParser#fxhb_assign_by_number.
    def enterFxhb_assign_by_number(self, ctx: SchrodingerMRParser.Fxhb_assign_by_numberContext):
        self.hbondRestraints += 1

        self.atomSelectionSet.clear()

        atom_sel = [int(str(ctx.Integer(0))), int(str(ctx.Integer(1))), int(str(ctx.Integer(2)))]

        if len(self.__atomNumberDict) == 0:
            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                          "The 'FXHB' clause has no effect "
                          f"because atom number dictionary is necessary to interpret the internal atom selection {atom_sel}.")
            self.hbondRestraints -= 1
        else:
            for ai in atom_sel:
                if ai in self.__atomNumberDict:
                    atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                    self.atomSelectionSet.append(atomSelection)
                else:
                    self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                  f"'{ai}' is not defined in the atom number dictionary.")

            self.exitFxhb_assign(ctx)

    # Exit a parse tree produced by SchrodingerMRParser#fxhb_assign_by_number.
    def exitFxhb_assign_by_number(self, ctx: SchrodingerMRParser.Fxhb_assign_by_numberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by SchrodingerMRParser#selection.
    def enterSelection(self, ctx: SchrodingerMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.verbose_debug:
            print("  " * self.depth + "enter_selection")

        if self.depth == 0:
            self.stackSelections = []
            self.stackTerms = []
            self.factor = {}

    # Exit a parse tree produced by SchrodingerMRParser#selection.
    def exitSelection(self, ctx: SchrodingerMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.verbose_debug:
            print("  " * self.depth + "exit_selection")

        if 'or' in self.stackSelections:
            top_union_exprs = self.stackSelections.count('or')

            unionSelections = []
            unionSelections.append(None)
            unionId = 0

            for _selection in self.stackSelections:

                if _selection is None:
                    continue

                if isinstance(_selection, str) and _selection == 'or':

                    if unionId == top_union_exprs - 1:
                        break

                    unionSelections.append(None)
                    unionId += 1

                    continue

                if unionSelections[unionId] is None:
                    unionSelections[unionId] = []

                unionSelections[unionId].append(_selection)

            self.stackSelections.clear()

            unionAtomSelection = []

            for stackSelections in unionSelections:

                if stackSelections is None:
                    continue

                if 'and' not in stackSelections:

                    atomSelection = stackSelections.pop() if stackSelections else []

                    while stackSelections:
                        _selection = stackSelections.pop()
                        if _selection is not None:
                            atomSelection = self.intersectionAtom_selections(_selection, atomSelection)

                else:

                    blockSelections = []
                    blockSelections.append(None)
                    blockId = 0

                    for _selection in stackSelections:

                        if _selection is None:
                            continue

                        if isinstance(_selection, str) and _selection == 'and':
                            blockSelections.append(None)
                            blockId += 1
                            continue

                        if blockSelections[blockId] is None:
                            blockSelections[blockId] = _selection

                        else:
                            for _atom in _selection:
                                if _atom not in blockSelections[blockId]:
                                    blockSelections[blockId].append(_atom)

                    stackSelections.clear()

                    atomSelection = blockSelections.pop()

                    while blockSelections:
                        atomSelection = self.intersectionAtom_selections(blockSelections.pop(), atomSelection)

                if len(atomSelection) > 0:
                    unionAtomSelection.extend(atomSelection)

            atomSelection = unionAtomSelection

            if '*' in atomSelection:
                atomSelection.remove('*')

            if self.createSfDict:
                atomSelection = sorted(atomSelection, key=itemgetter('chain_id', 'seq_id', 'atom_id'))

            if self.verbose_debug:
                print("  " * self.depth + f"atom selection: {atomSelection}")

            self.atomSelectionSet.append(atomSelection)

            return

        if 'and' not in self.stackSelections:

            atomSelection = self.stackSelections.pop() if self.stackSelections else []

            while self.stackSelections:
                _selection = self.stackSelections.pop()
                if _selection is not None:
                    if self.con_union_expr:
                        for _atom in _selection:
                            if _atom not in atomSelection:
                                atomSelection.append(_atom)
                    else:
                        atomSelection = self.intersectionAtom_selections(_selection, atomSelection)

        else:

            blockSelections = []
            blockSelections.append(None)
            blockId = 0

            for _selection in self.stackSelections:

                if _selection is None:
                    continue

                if isinstance(_selection, str) and _selection == 'and':
                    blockSelections.append(None)
                    blockId += 1
                    continue

                if blockSelections[blockId] is None:
                    blockSelections[blockId] = _selection

                else:
                    for _atom in _selection:
                        if _atom not in blockSelections[blockId]:
                            blockSelections[blockId].append(_atom)

            self.stackSelections.clear()

            atomSelection = blockSelections.pop()

            while blockSelections:
                atomSelection = self.iIntersectionAtom_selections(blockSelections.pop(), atomSelection)

        while self.stackSelections:
            _selection = self.stackSelections.pop()
            if _selection is not None:
                for _atom in _selection:
                    if _atom not in atomSelection:
                        atomSelection.append(_atom)

        if '*' in atomSelection:
            atomSelection.remove('*')

        if self.createSfDict:
            atomSelection = sorted(atomSelection, key=itemgetter('chain_id', 'seq_id', 'atom_id'))

        if self.verbose_debug:
            print("  " * self.depth + f"atom selection: {atomSelection}")

        self.atomSelectionSet.append(atomSelection)

    # Enter a parse tree produced by SchrodingerMRParser#selection_expression.
    def enterSelection_expression(self, ctx: SchrodingerMRParser.Selection_expressionContext):
        self.cur_union_expr = self.con_union_expr = bool(ctx.Or_op(0))
        if self.depth == 0:
            self.top_union_expr = self.cur_union_expr

        if self.depth > 0 and self.cur_union_expr:
            self.unionFactor = {}

        if self.verbose_debug:
            print("  " * self.depth + f"enter_sel_expr, union: {self.cur_union_expr}")

        if self.depth > 0 and len(self.factor) > 0:
            if 'atom_selection' not in self.factor:
                self.consumeFactor_expressions(cifCheck=True)
            if 'atom_selection' in self.factor:
                self.stackSelections.append(self.factor['atom_selection'])
                self.stackSelections.append('and')  # intersection

        self.depth += 1

    # Exit a parse tree produced by SchrodingerMRParser#selection_expression.
    def exitSelection_expression(self, ctx: SchrodingerMRParser.Selection_expressionContext):  # pylint: disable=unused-argument
        self.depth -= 1
        if self.verbose_debug:
            print("  " * self.depth + "exit_sel_expr")

        _atomSelection = []
        while self.stackTerms:
            _term = self.stackTerms.pop()
            if _term is not None:
                _atomSelection.extend(_term)

        atomSelection = [dict(s) for s in set(frozenset(atom.items())
                                              for atom in _atomSelection
                                              if isinstance(atom, dict))] if len(_atomSelection) > 1 else _atomSelection

        if len(atomSelection) > 0:
            if self.depth == 0 and not self.top_union_expr:
                self.stackSelections.append(atomSelection)
            elif self.depth > 0 and self.top_union_expr and not self.cur_union_expr:
                if len(self.stackSelections) > 0 and isinstance(self.stackSelections[-1], str):
                    self.stackSelections.append(atomSelection)
            else:
                self.stackSelections.append(atomSelection)

        if self.depth == 0 or not self.top_union_expr:
            self.factor = {}

        if self.cur_union_expr:
            self.cur_union_expr = False
        if self.con_union_expr and self.depth == 0:
            self.con_union_expr = False
            self.unionFactor = None

    # Enter a parse tree produced by SchrodingerMRParser#term.
    def enterTerm(self, ctx: SchrodingerMRParser.TermContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_term, intersection: {bool(ctx.And_op(0))}")

        self.stackFactors = []
        self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by SchrodingerMRParser#term.
    def exitTerm(self, ctx: SchrodingerMRParser.TermContext):  # pylint: disable=unused-argument
        self.depth -= 1
        if self.verbose_debug:
            print("  " * self.depth + "exit_term")

        if self.depth == 1 and self.top_union_expr:

            if self.stackFactors:
                while self.stackFactors:
                    _factor = self.doConsumeFactor_expressions(self.stackFactors.pop(), cifCheck=True)
                    self.factor = self.doIntersectionFactor_expressions(self.factor,
                                                                        None if 'atom_selection' not in _factor
                                                                        or isinstance(_factor['atom_selection'], str)
                                                                        else _factor['atom_selection'])
            else:
                self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)

            if 'atom_selection' in self.factor:
                self.stackTerms.append(self.factor['atom_selection'])

            _atomSelection = []
            while self.stackTerms:
                _term = self.stackTerms.pop()
                if _term is not None and not isinstance(_term, str):
                    _atomSelection.extend(_term)

            atomSelection = [dict(s) for s in set(frozenset(atom.items())
                                                  for atom in _atomSelection
                                                  if isinstance(atom, dict))] if len(_atomSelection) > 1 else _atomSelection

            if len(atomSelection) > 0:
                self.stackSelections.append(atomSelection)

            self.stackSelections.append('or')  # union

            self.stackTerms = []
            self.stackFactors = []
            self.factor = {}

            return

        if self.depth == 1 or not self.top_union_expr:
            while self.stackFactors:
                p = self.stackFactors.pop()
                if 'has_nitroxide' in p:
                    self.factor = p
                else:
                    _factor = self.doConsumeFactor_expressions(p, cifCheck=True)
                    self.factor = self.doIntersectionFactor_expressions(self.factor, _factor.get('atom_selection'))

        if self.unionFactor is not None and len(self.unionFactor) > 0:
            if 'atom_selection' not in self.unionFactor:
                self.unionFactor = self.doConsumeFactor_expressions(self.unionFactor, cifCheck=True)
            if 'atom_selection' in self.unionFactor:
                _atomSelection = self.unionFactor['atom_selection']
                del self.unionFactor['atom_selection']
                __factor = self.doConsumeFactor_expressions(self.unionFactor, cifCheck=True)
                if 'atom_selection' in __factor:
                    for _atom in __factor['atom_selection']:
                        if _atom not in _atomSelection:
                            _atomSelection.append(_atom)
                if len(_atomSelection) > 0:
                    self.factor['atom_selection'] = _atomSelection
            self.unionFactor = None

        if 'atom_selection' in self.factor and not isinstance(self.factor['atom_selection'], str):
            self.stackTerms.append(self.factor['atom_selection'])

    # Enter a parse tree produced by SchrodingerMRParser#factor.
    def enterFactor(self, ctx: SchrodingerMRParser.FactorContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_factor, concatenation: {bool(ctx.factor())}")

        if ctx.Not_op():
            if len(self.factor) > 0:
                self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)
                if 'atom_selection' in self.factor:
                    self.stackFactors.append(self.factor)
                self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by SchrodingerMRParser#factor.
    def exitFactor(self, ctx: SchrodingerMRParser.FactorContext):
        self.depth -= 1
        if self.verbose_debug:
            print("  " * self.depth + "exit_factor")

        def get_int_range(_ctx):
            ret = {}
            unq = None

            try:

                if _ctx.IntRange():
                    if self.__asl_int_range_pat.match(str(_ctx.IntRange())):
                        g = self.__asl_int_range_pat.search(str(_ctx.IntRange())).groups()
                        _range = [int(g[0]), int(g[1])]
                        ret['range'] = [min(_range), max(_range)]

                elif _ctx.Lt_op():
                    ret['max_exclusive'] = int(str(_ctx.Integer(0)))

                elif _ctx.Gt_op():
                    ret['min_exclusive'] = int(str(_ctx.Integer(0)))

                elif _ctx.Leq_op():
                    ret['max_inclusive'] = int(str(_ctx.Integer(0)))

                elif _ctx.Geq_op():
                    ret['min_inclusive'] = int(str(_ctx.Integer(0)))

                elif _ctx.Integer(0):
                    unq = int(str(_ctx.Integer(0)))
                    ret['range'] = [unq, unq]

            except Exception:
                pass

            if len(ret) == 0:
                self.factor['atom_id'] = [None]
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Couldn't specify range of integer from {str(_ctx.IntRange())!r}.")
                return None, None

            return ret, unq

        def get_str_pattern(_ctx, upper=False):
            ret, alt, unq = [], [], []

            s_idx = m_idx = i_idx = 0

            while _ctx.Simple_names(m_idx):
                _val = _val_ = str(_ctx.Simple_names(m_idx))
                if upper:
                    _val = _val.upper()
                ret.append(toRegEx(_val))
                alt.append(_val_)
                m_idx += 1

            while _ctx.Simple_name(s_idx):
                _val = _val_ = str(_ctx.Simple_name(s_idx))
                if upper:
                    _val = _val.upper()
                ret.append(_val)
                alt.append(_val_)
                if s_idx == 0:
                    unq.append(_val_)
                s_idx += 1

            while _ctx.Integer(i_idx):
                _val = _val_ = str(_ctx.Integer(i_idx))
                ret.append(_val)
                alt.append(_val_)
                if i_idx == 0:
                    unq.append(_val_)
                i_idx += 1

            return ret, alt, unq

        try:

            # concatenation
            if ctx.factor() and self.stackSelections:
                if self.con_union_expr and not self.cur_union_expr and ctx.Not_op():
                    if len(self.stackFactors) > 0:
                        self.stackFactors.pop()
                        self.factor['atom_selection'] = self.stackSelections[-1]
                        self.stackSelections.append('and')  # intersection

                elif not self.top_union_expr:
                    if len(self.stackFactors) > 0:
                        self.stackFactors.pop()
                        self.factor = {'atom_selection': self.stackSelections.pop()}

            elif ctx.Entry() or ctx.Entry_name():
                clauseName = 'entry.' if ctx.Entry() else 'entry.name'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal name of the molecular assembly "
                              "cannot be assigned to the auth_asym_id of the result coordinates.")

            elif ctx.Molecule() or ctx.Molecule_number():
                clauseName = 'molecule.' if ctx.Molecule() else 'moelcule.number'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal entity order in the molecular assembly "
                              "cannot be assigned to the auth_asym_id of the result coordinates.")

            elif ctx.Molecule_modulo() or ctx.Molecule_entrynum():
                clauseName = 'molecule.modulo' if ctx.Molecule_modulo() else 'moelcule.entrynum'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal entity order in the internal entry "
                              "cannot be assigned to the auth_asym_id of the result coordinates.")

            elif ctx.Molecule_atoms():
                clauseName = 'molecule.atoms'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                int_range, _ = get_int_range(ctx)

                if int_range is not None:
                    atoms_per_chain = {}
                    for k, v in self.coordAtomSite.items():
                        chain_id = k[0]
                        if chain_id not in atoms_per_chain:
                            atoms_per_chain[chain_id] = 0
                        atoms_per_chain[chain_id] += len(v['atom_id'])

                    chain_ids = []
                    if 'range' in int_range:
                        chain_ids = [k for k, v in atoms_per_chain if int_range['range'][0] <= v <= int_range['range'][1]]
                    elif 'max_exclusive' in int_range:
                        chain_ids = [k for k, v in atoms_per_chain if v < int_range['max_exclusive']]
                    elif 'min_exclusive' in int_range:
                        chain_ids = [k for k, v in atoms_per_chain if v > int_range['min_exclusive']]
                    elif 'max_inclusive' in int_range:
                        chain_ids = [k for k, v in atoms_per_chain if v <= int_range['max_inclusive']]
                    elif 'min_inclusive' in int_range:
                        chain_ids = [k for k, v in atoms_per_chain if v >= int_range['min_inclusive']]

                    if len(chain_ids) > 0:
                        self.factor['chain_id'] = chain_ids
                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

            elif ctx.Molecule_weight():
                clauseName = 'molecule.weight'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                int_range, _ = get_int_range(ctx)

                if int_range is not None:
                    weight_per_chain = {}
                    for k, v in self.coordAtomSite.items():
                        chain_id = k[0]
                        if chain_id not in weight_per_chain:
                            weight_per_chain[chain_id] = 0.0
                        common_types = collections.Counter(v['type_symbol']).most_common()
                        weight_per_chain[chain_id] += sum(ELEMENT_WEIGHTS[int_atom[t]] * count for t, count in common_types)

                    chain_ids = []
                    if 'range' in int_range:
                        chain_ids = [k for k, v in weight_per_chain if int_range['range'][0] <= v <= int_range['range'][1]]
                    elif 'max_exclusive' in int_range:
                        chain_ids = [k for k, v in weight_per_chain if v < int_range['max_exclusive']]
                    elif 'min_exclusive' in int_range:
                        chain_ids = [k for k, v in weight_per_chain if v > int_range['min_exclusive']]
                    elif 'max_inclusive' in int_range:
                        chain_ids = [k for k, v in weight_per_chain if v <= int_range['max_inclusive']]
                    elif 'min_inclusive' in int_range:
                        chain_ids = [k for k, v in weight_per_chain if v >= int_range['min_inclusive']]

                    if len(chain_ids) > 0:
                        self.factor['chain_id'] = chain_ids
                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

            elif ctx.Chain() or ctx.Chain_name():
                clauseName = 'chain.' if ctx.Chain() else 'chain.name'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'chain_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                str_pattern, alt_pattern, chainIds = get_str_pattern(ctx)
                if len(chainIds) > 0:
                    chainId = chainIds[0]
                else:
                    chainId = self.polySeq[0]['auth_chain_id']

                self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq if any(re.match(p, ps['auth_chain_id']) for p in str_pattern)]
                if self.hasNonPolySeq:
                    for np in self.nonPolySeq:
                        _chainId = np['auth_chain_id']
                        if any(re.match(p, _chainId) for p in str_pattern) and _chainId not in self.factor['chain_id']:
                            self.factor['chain_id'].append(_chainId)

                if len(self.factor['chain_id']) == 0:
                    if len(self.fibril_chain_ids) > 0 and not self.hasNonPoly:
                        if chainId[0] in self.fibril_chain_ids:
                            self.factor['chain_id'] = [chainId[0]]
                    elif self.monoPolymer and not self.hasBranched and not self.hasNonPoly:
                        self.factor['chain_id'] = self.polySeq[0]['auth_chain_id']
                        self.factor['auth_chain_id'] = alt_pattern
                    elif self.reasons is not None:
                        if 'atom_id' not in self.factor or not any(a in XPLOR_RDC_PRINCIPAL_AXIS_NAMES for a in self.factor['atom_id']):
                            if 'segment_id_mismatch' in self.reasons\
                               and chainId not in self.reasons['segment_id_mismatch']:
                                self.reasons = None
                                if 'segment_id_mismatch' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['segment_id_mismatch'] = {}
                                    self.reasonsForReParsing['segment_id_match_stats'] = {}
                                    self.reasonsForReParsing['segment_id_poly_type_stats'] = {}
                                if chainId not in self.reasonsForReParsing['segment_id_mismatch']:
                                    self.reasonsForReParsing['segment_id_mismatch'][chainId] = None
                                    self.reasonsForReParsing['segment_id_match_stats'][chainId] = {}
                                    self.reasonsForReParsing['segment_id_poly_type_stats'][chainId] = {'polymer': 0, 'non-poly': 0}
                                self.factor['alt_chain_id'] = chainId
                            else:
                                self.factor['atom_id'] = [None]
                                if 'segment_id_mismatch' in self.reasons\
                                   and (chainId not in self.reasons['segment_id_mismatch']
                                        or self.reasons['segment_id_mismatch'][chainId] is not None):
                                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                                  f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")
                    else:
                        if 'segment_id_mismatch' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['segment_id_mismatch'] = {}
                            self.reasonsForReParsing['segment_id_match_stats'] = {}
                            self.reasonsForReParsing['segment_id_poly_type_stats'] = {}
                        if chainId not in self.reasonsForReParsing['segment_id_mismatch']:
                            self.reasonsForReParsing['segment_id_mismatch'][chainId] = None
                            self.reasonsForReParsing['segment_id_match_stats'][chainId] = {}
                            self.reasonsForReParsing['segment_id_poly_type_stats'][chainId] = {'polymer': 0, 'non-poly': 0}
                        self.factor['alt_chain_id'] = chainId

            elif ctx.Residue() or ctx.Residue_name_or_number():
                has_name = ctx.Simple_names(0) or ctx.Simple_name(0)
                if ctx.Residue():
                    clauseName = 'residue.'
                else:
                    clauseName = 'residue.name' if has_name else 'residue.number'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                if has_name:

                    eval_factor = False
                    if 'comp_id' in self.factor:
                        self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                        eval_factor = True

                    if not eval_factor and 'atom_selection' in self.factor:
                        self.factor = {}

                    str_pattern, alt_pattern, compIds = get_str_pattern(ctx, True)

                    self.factor['comp_id'] = []
                    for _compId in self.compIdSet:
                        if any(re.match(p, _compId) for p in str_pattern):
                            self.factor['comp_id'].append(_compId)
                    for _compId in self.altCompIdSet:
                        if any(re.match(p, _compId) for p in str_pattern) and _compId not in self.factor['comp_id']:
                            self.factor['comp_id'].append(_compId)
                    for _compId in self.cyanaCompIdSet:
                        if any(re.match(p, _compId) for p in str_pattern) and _compId not in self.factor['comp_id']:
                            self.factor['comp_id'].append(_compId)

                    if len(self.factor['comp_id']) == 0:
                        if len(compIds) > 0:
                            self.factor['comp_id'] = compIds
                        else:
                            del self.factor['comp_id']
                            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                          f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")

                else:

                    eval_factor = False
                    if 'seq_id' in self.factor:
                        self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                        eval_factor = True

                    if not eval_factor and 'atom_selection' in self.factor:
                        self.factor = {}

                    int_range, _seqId = get_int_range(ctx)

                    if int_range is not None:
                        seqIds = set()

                        for ps in self.fullPolySeq:
                            for seqId in ps['auth_seq_id']:
                                if 'range' in int_range:
                                    if int_range['range'][0] <= seqId <= int_range['range'][1]:
                                        seqIds.add(seqId)
                                elif 'max_exclusive' in int_range:
                                    if seqId < int_range['max_exclusive']:
                                        seqIds.add(seqId)
                                elif 'min_exclusive' in int_range:
                                    if seqId > int_range['min_exclusive']:
                                        seqIds.add(seqId)
                                elif 'max_incl=usive' in int_range:
                                    if seqId <= int_range['max_inclusive']:
                                        seqIds.add(seqId)
                                elif 'min_inclusive' in int_range:
                                    if seqId >= int_range['min_inclusive']:
                                        seqIds.add(seqId)

                        self.factor['seq_id'] = sorted(list(seqIds))
                        if len(self.factor['seq_id']) == 0:
                            if _seqId is not None:
                                self.factor['seq_id'] = [_seqId]
                            elif 'range' in int_range:
                                self.factor['seq_id'] = list(range(int_range['range'][0], int_range['range'][1] + 1))
                            else:
                                del self.factor['seq_id']
                                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                              f"The {clauseName!r} clause has no effect.")

            elif ctx.Residue_ptype():
                clauseName = 'residue.ptype'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'comp_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                str_pattern, alt_pattern, compIds = get_str_pattern(ctx, True)

                self.factor['comp_id'] = []
                for _compId in self.compIdSet:
                    if any(re.match(p, _compId) for p in str_pattern):
                        self.factor['comp_id'].append(_compId)
                for _compId in self.altCompIdSet:
                    if any(re.match(p, _compId) for p in str_pattern) and _compId not in self.factor['comp_id']:
                        self.factor['comp_id'].append(_compId)
                for _compId in self.cyanaCompIdSet:
                    if any(re.match(p, _compId) for p in str_pattern) and _compId not in self.factor['comp_id']:
                        self.factor['comp_id'].append(_compId)

                if len(self.factor['comp_id']) == 0:
                    if len(compIds) > 0:
                        self.factor['comp_id'] = compIds
                    else:
                        del self.factor['comp_id']
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")

            elif ctx.Residue_mtype():
                clauseName = 'residue.mtype'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                oneLetterCodeSet = []
                if self.polyPeptide and not self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                    oneLetterCodeSet = [getOneLetterCode(compId) for compId in self.compIdSet if len(compId) == 3]
                elif not self.polyPeptide and self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                    oneLetterCodeSet = [getOneLetterCode(compId) for compId in self.compIdSet if len(compId) == 2]
                elif not self.polyPeptide and not self.polyDeoxyribonucleotide and self.polyRibonucleotide:
                    oneLetterCodeSet = [getOneLetterCode(compId) for compId in self.compIdSet if len(compId) == 1]

                if self.hasNonPolySeq:
                    for np in self.nonPoly:
                        if np['comp_id'][0][0].isalpha() and np['comp_id'][0][0] not in oneLetterCodeSet:
                            oneLetterCodeSet.append(np['comp_id'][0][0])
                        if np['auth_comp_id'][0][0].isalpha() and np['auth_comp_id'][0][0] not in oneLetterCodeSet:
                            oneLetterCodeSet.append(np['auth_comp_id'][0][0])
                        if np['alt_comp_id'][0][0].isalpha() and np['alt_comp_id'][0][0] not in oneLetterCodeSet:
                            oneLetterCodeSet.append(np['alt_comp_id'][0][0])

                eval_factor = False
                if 'comp_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                str_pattern, alt_pattern, compIds = get_str_pattern(ctx, True)

                self.factor['comp_id'] = []
                for _compId in oneLetterCodeSet:
                    if any(re.match(p, _compId) for p in str_pattern):
                        _compId = next((__compId for __compId in self.compIdSet if getOneLetterCode(__compId) == _compId), _compId)
                        self.factor['comp_id'].append(_compId)

                if len(self.factor['comp_id']) == 0:
                    if len(compIds) > 0:
                        self.factor['comp_id'] = [next(k for k, v in monDict3.items() if v == compId)
                                                  for compId in compIds
                                                  if any(True for _v in monDict3.values() if _v == compId)]
                    else:
                        del self.factor['comp_id']
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")

            elif ctx.Residue_polarity():
                clauseName = 'residue.polarity'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")

                eval_factor = False
                if 'comp_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                if ctx.Hydrophilic():
                    self.factor['comp_id'] = ['ARG', 'ASN', 'ASP', 'GLN', 'GLU', 'HIS', 'LYS', 'SER', 'THR']

                elif ctx.Hydrophobic():
                    self.factor['comp_id'] = ['ALA', 'ILE', 'LEU', 'MET', 'PHE', 'TRP', 'TYR', 'VAL']

                elif ctx.Non_polar():
                    self.factor['comp_id'] = ['ALA', 'GLY', 'ILE', 'LEU', 'MET', 'PHE', 'PRO', 'TRP', 'VAL']

                elif ctx.Polar():
                    self.factor['comp_id'] = ['ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'HIS', 'LYS', 'SER', 'THR', 'TYR']

                elif ctx.Charged():
                    self.factor['comp_id'] = ['ARG', 'ASP', 'GLU', 'HIS', 'LYS']

                elif ctx.Positive():
                    self.factor['comp_id'] = ['ARG', 'LYS', 'HIS']

                elif ctx.Negative():
                    self.factor['comp_id'] = ['ASP', 'GLU']

            elif ctx.Residue_secondary_structure():
                clauseName = 'residue.secondary_structure'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'seq_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                authAsymIds = []
                for entity in self.entityAssembly:
                    if 'entity_poly_type' in entity:
                        poly_type = entity['entity_poly_type']
                        if poly_type.startswith('polypeptide'):
                            authAsymIds.extend(entity['auth_asym_id'].split(','))

                struct_conf = self.cR.getDictList('struct_conf')
                struct_sheet_range = self.cR.getDictList('struct_sheet_range')

                helix, strand, loop = {}, {}, {}

                for ps in self.polySeq:
                    chainId = ps['auth_chain_id']
                    if chainId not in authAsymIds:
                        continue
                    for seqId in ps['auth_seq_id']:
                        in_helix = in_strand = False
                        for sc in struct_conf:
                            if sc['beg_auth_asym_id'] != chainId:
                                continue
                            if int(sc['beg_auth_seq_id']) <= seqId <= int(sc['end_auth_seq_id']):
                                in_helix = True
                                break
                        if not in_helix:
                            for ssr in struct_sheet_range:
                                if ssr['beg_auth_asym_id'] != chainId:
                                    continue
                                if int(ssr['beg_auth_seq_id']) <= seqId <= int(ssr['end_auth_seq_id']):
                                    in_strand = True
                                    break
                        if in_helix:
                            if chainId not in helix:
                                helix[chainId] = []
                            helix[chainId].append(seqId)
                        elif in_strand:
                            if chainId not in strand:
                                strand[chainId] = []
                            strand[chainId].append(seqId)
                        else:
                            if chainId not in loop:
                                loop[chainId] = []
                            loop[chainId].append(seqId)

                if ctx.Helix_or_strand():
                    subClauseName = 'helix,strand'
                    both = {}
                    for k, v in helix.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    for k, v in strand.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    if len(both) > 0:
                        self.factor['chain_id'] = list(both.keys())
                        m = []
                        for v in both.values():
                            m.extend(v)
                        self.factor['seq_id'] = m
                elif ctx.Strand_or_loop():
                    subClauseName = 'strand,loop'
                    both = {}
                    for k, v in strand.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    for k, v in loop.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    if len(both) > 0:
                        self.factor['chain_id'] = list(both.keys())
                        m = []
                        for v in both.values():
                            m.extend(v)
                        self.factor['seq_id'] = m
                elif ctx.Helix_or_loop():
                    subClauseName = 'helix,loop'
                    both = {}
                    for k, v in helix.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    for k, v in loop.items():
                        if len(v) == 0:
                            continue
                        if k not in both:
                            both[k] = []
                        both[k].extend(v)
                    if len(both) > 0:
                        self.factor['chain_id'] = list(both.keys())
                        m = []
                        for v in both.values():
                            m.extend(v)
                        self.factor['seq_id'] = m
                elif ctx.Helix():
                    subClauseName = 'helix'
                    self.factor['chain_id'] = list(helix.keys())
                    m = []
                    for v in helix.values():
                        m.extend(v)
                    self.factor['seq_id'] = m
                elif ctx.Strand():
                    subClauseName = 'strand'
                    self.factor['chain_id'] = list(strand.keys())
                    m = []
                    for v in strand.values():
                        m.extend(v)
                    self.factor['seq_id'] = m
                elif ctx.Loop():
                    subClauseName = 'loop'
                    self.factor['chain_id'] = list(loop.keys())
                    m = []
                    for v in loop.values():
                        m.extend(v)
                    self.factor['seq_id'] = m

                if 'seq_id' not in self.factor or len(self.factor['seq_id']) == 0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"  # pylint: disable=possibly-used-before-assignment
                                  f"The {clauseName!r} {subClauseName} clause has no effect.")

            elif ctx.Residue_position():
                clauseName = 'residue.position'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return

                begin = self.numberFSelection[0]
                end = self.numberFSelection[1]

                if begin > end:
                    begin, end = end, begin

                if begin < 0.0 or begin > 1.0 or end < 0.0 or end > 1.0 or begin == end:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {begin} {end} clause has no effect "
                                  "because given positions are out of range.")

                else:

                    eval_factor = False
                    if 'seq_id' in self.factor:
                        self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                        eval_factor = True

                    if not eval_factor and 'atom_selection' in self.factor:
                        self.factor = {}

                    chainIds = set()
                    seqIds = set()
                    for ps in self.polySeq:
                        len_ps = len(ps['seq_id'])
                        for seqId, authSeqId in zip(ps['seq_id'], ps['auth_seq_id']):
                            if len_ps * begin <= seqId <= len_ps * end:
                                chainIds.add(ps['auth_chain_id'])
                                seqIds.add(authSeqId)

                    if 'chain_id' not in self.factor:
                        self.factor['chain_id'] = list(chainIds)
                    self.factor['seq_id'] = sorted(list(seqIds))
                    if len(self.factor['seq_id']) == 0:
                        del self.factor['seq_id']
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} {begin} {end} clause has no effect.")

            elif ctx.Residue_inscode():
                clauseName = 'residue.inscode'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                inscode = str(ctx.Simple_name(0))
                chainIds = set()
                seqIds = set()
                compIds = set()

                if inscode not in emptyValue:

                    eval_factor = False
                    if 'comp_id' in self.factor:
                        self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                        eval_factor = True

                    if not eval_factor and 'atom_selection' in self.factor:
                        self.factor = {}

                    for ps in self.fullPolySeq:
                        if 'ins_code' not in ps:
                            continue
                        if inscode in ps['ins_code']:
                            for ins_code, authSeqId, compId in zip(ps['ins_code'], ps['auth_seq_id'], ps['comp_id']):
                                if ins_code != inscode:
                                    continue
                                chainIds.add(ps['auth_chain_id'])
                                seqIds.add(authSeqId)
                                compIds.add(compId)

                if len(seqIds) == 0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {inscode} clause has no effect.")
                else:
                    if 'chain_id' not in self.factor:
                        self.factor['chain_id'] = list(chainIds)
                    if 'seq_id' not in self.factor:
                        self.factor['seq_id'] = sorted(list(seqIds))
                    if 'comp_id' not in self.factor:
                        self.factor['comp_id'] = list(compIds)

            elif ctx.Atom_ptype() or ctx.Atom_name():
                clauseName = 'atom.ptype' if ctx.Atom_ptype() else 'atom.name'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'atom_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                str_pattern, alt_pattern, atomIds = get_str_pattern(ctx, True)

                self.factor['atom_id'] = []
                for _atomId in self.atomIdSetPerChain.values():
                    if any(re.match(p, _atomId) for p in str_pattern):
                        if _atomId not in self.factor['atom_id']:
                            self.factor['atom_id'].append(_atomId)

                if len(self.factor['atom_id']) == 0:
                    if len(atomIds) > 0:
                        self.factor['atom_id'] = atomIds
                    else:
                        self.factor['atom_id'] = None
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")

            elif ctx.Atom() or ctx.Atom_number():
                clauseName = 'atom.' if ctx.Atom() else 'atom.number'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal atom number cannot validate with the coordinates.")

            elif ctx.Atom_molnum() or ctx.Atom_entrynum():
                clauseName = 'atom.molnum' if ctx.Atom() else 'atom.entrynum'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal atom number cannot validate with the coordinates.")

            elif ctx.Atom_mtype():
                clauseName = 'atom.mtype'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the Maestro atom type cannot validate with the coordinates.")

            elif ctx.Atom_element():
                clauseName = 'atom.element'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'type_symbol' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                str_pattern, alt_pattern, typeSymbols = get_str_pattern(ctx, True)

                typeSymbolSet = set()
                for v in self.coordAtomSite.values():
                    typeSymbolSet |= set(v['type_symbol'])

                self.factor['type_symbol'] = []
                for typeSymbol in typeSymbolSet:
                    if re.match(str_pattern, typeSymbol):
                        self.factor['type_symbol'].append(typeSymbol)

                if len(self.factor['type_symbol']) == 0:
                    if len(typeSymbols) > 0:
                        self.factor['type_symbol'] = typeSymbols
                    else:
                        del self.factor['type_symbol']
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"Couldn't specify {clauseName}:'{alt_pattern}' in the coordinates.")

            elif ctx.Atom_attachements():
                clauseName = 'atom.attachements'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'atom_id' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                int_range, _ = get_int_range(ctx)

                if int_range is not None:
                    chainIds = set()
                    seqIds = set()
                    compIds = set()
                    atomIds = set()

                    for k, v in self.coordAtomSite.items():
                        chainId, seqId = k
                        compId = v['comp_id']
                        for atomId in v['atom_id']:
                            attachements = len(self.ccU.getBondedAtoms(compId, atomId))

                            if 'range' in int_range:
                                if int_range['range'][0] <= attachements <= int_range['range'][1]:
                                    chainIds.add(chainId)
                                    seqIds.add(seqId)
                                    compIds.add(compId)
                                    atomIds.add(atomId)
                            elif 'max_exclusive' in int_range:
                                if attachements < int_range['max_exclusive']:
                                    chainIds.add(chainId)
                                    seqIds.add(seqId)
                                    compIds.add(compId)
                                    atomIds.add(atomId)
                            elif 'min_exclusive' in int_range:
                                if attachements > int_range['min_exclusive']:
                                    chainIds.add(chainId)
                                    seqIds.add(seqId)
                                    compIds.add(compId)
                                    atomIds.add(atomId)
                            elif 'max_incl=usive' in int_range:
                                if attachements <= int_range['max_inclusive']:
                                    chainIds.add(chainId)
                                    seqIds.add(seqId)
                                    compIds.add(compId)
                                    atomIds.add(atomId)
                            elif 'min_inclusive' in int_range:
                                if attachements >= int_range['min_inclusive']:
                                    chainIds.add(chainId)
                                    seqIds.add(seqId)
                                    compIds.add(compId)
                                    atomIds.add(atomId)

                    self.factor['atom_id'] = list(atomIds)
                    if len(self.factor['atom_id']) == 0:
                        self.factor['atom_id'] = None
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")
                    else:
                        if 'chain_id' not in self.factor:
                            self.factor['chain_id'] = list(chainIds)
                        if 'seq_id' not in self.factor:
                            self.factor['seq_id'] = sorted(list(seqIds))
                        if 'comp_id' not in self.factor:
                            self.factor['comp_id'] = list(compIds)

            elif ctx.Atom_atomicnumber():
                clauseName = 'atom.atomicnumber'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                eval_factor = False
                if 'type_symbol' in self.factor:
                    self.consumeFactor_expressions(f"'{clauseName}' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                int_range, _ = get_int_range(ctx)

                if int_range is not None:
                    typeSymbolSet = set()
                    for v in self.coordAtomSite.values():
                        typeSymbolSet |= set(v['type_symbol'])

                    self.factor['type_symbol'] = []
                    for typeSymbol in typeSymbolSet:
                        atomicnumber = int_atom(typeSymbol)

                        if 'range' in int_range:
                            if int_range['range'][0] <= atomicnumber <= int_range['range'][1]:
                                self.factor['type_symbol'].append(typeSymbol)
                        elif 'max_exclusive' in int_range:
                            if atomicnumber < int_range['max_exclusive']:
                                self.factor['type_symbol'].append(typeSymbol)
                        elif 'min_exclusive' in int_range:
                            if atomicnumber > int_range['min_exclusive']:
                                self.factor['type_symbol'].append(typeSymbol)
                        elif 'max_incl=usive' in int_range:
                            if atomicnumber <= int_range['max_inclusive']:
                                self.factor['type_symbol'].append(typeSymbol)
                        elif 'min_inclusive' in int_range:
                            if atomicnumber >= int_range['min_inclusive']:
                                self.factor['type_symbol'].append(typeSymbol)

                    if len(self.factor['type_symbol']) == 0:
                        del self.factor['type_symbol']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

            elif ctx.Atom_charge():
                clauseName = 'atom.charge'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the partial charge cannot validate with the coordinates.")

            elif ctx.Atom_formalcharge():
                clauseName = 'atom.formalcharge'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                int_range, _ = get_int_range(ctx)

                if int_range is not None:
                    valueType = {'name': 'pdbx_formal_charge'}
                    if 'range' in int_range:
                        valueType['type'] = 'enum'
                        valueType['enum'] = list(range(int_range['range'][0], int_range['range'][1] + 1))
                    elif 'max_exclusive' in int_range:
                        valueType['type'] = 'range-int'
                        valueType['range'] = {'max_exclusive': int_range['max_exclusive']}
                    elif 'min_exclusive' in int_range:
                        valueType['type'] = 'range-int'
                        valueType['range'] = {'min_exclusive': int_range['min_exclusive']}
                    elif 'max_inclusive' in int_range:
                        valueType['type'] = 'range-int'
                        valueType['range'] = {'max_inclusive': int_range['max_inclusive']}
                    elif 'min_inclusive' in int_range:
                        valueType['type'] = 'range-int'
                        valueType['range'] = {'min_inclusive': int_range['min_inclusive']}
                    atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [valueType,
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])
                    self.factor['atom_selection'] = atomSelection
                    if len(atomSelection) == 0:
                        del self.factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

            elif ctx.Atom_displayed() or ctx.Atom_selected():
                clauseName = 'atom.displayed' if ctx.Atom_displayed() else 'atom.selected'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} clause has no effect "
                              "because the internal attribute cannot validate with the coordinates.")

            elif ctx.Fillres_op():
                clauseName = 'fillres'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    seqKeySet = []
                    for _atom in self.factor['atom_selection']:
                        seqKey = (_atom['chain_id'], _atom['seq_id'])
                        if seqKey not in seqKeySet:
                            seqKeySet.append(seqKey)

                    for seqKey in seqKeySet:
                        chainId, seqKey = seqKey
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                        if coordAtomSite is not None:
                            compId = coordAtomSite['comp_id']
                            for atomId in coordAtomSite['atom_id']:
                                _atomSelection.append({'chain_id': chainId,
                                                       'seq_id': seqId,
                                                       'comp_id': compId,
                                                       'atom_id': atomId})

                    self.factor['atom_selection'] = _atomSelection
                    if len(_atomSelection) == 0:
                        del self.factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} clause has no effect because no atom is selected.")

            elif ctx.Fillmol_op():
                clauseName = 'fillmol'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    chainIdSet = []
                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        if chainId not in chainIdSet:
                            chainIdSet.append(chainId)

                    for chainId in chainIdSet:
                        for seqKey in self.coordAtomSite:
                            if seqKey[0] != chainId:
                                continue
                            seqId = seqKey[1]
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                            if coordAtomSite is not None:
                                compId = coordAtomSite['comp_id']
                                for atomId in coordAtomSite['atom_id']:
                                    _atomSelection.append({'chain_id': chainId,
                                                           'seq_id': seqId,
                                                           'comp_id': compId,
                                                           'atom_id': atomId})

                    self.factor['atom_selection'] = _atomSelection
                    if len(_atomSelection) == 0:
                        del self.factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} clause has no effect because no atom is selected.")

            elif ctx.Within_op():
                clauseName = 'within'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return

                around = self.numberFSelection[0]

                if around <= 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {around} clause has no effect "
                                  "because a given distance is out of range.")

                else:

                    self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                    if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                        _atomSelection = []

                        for _atom in self.factor['atom_selection']:

                            try:

                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': _atom['chain_id']},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': _atom['seq_id']},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': _atom['atom_id']},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) != 1:
                                    continue

                                origin = to_np_array(_origin[0])

                                _neighbor =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                  [{'name': 'Cartn_x', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[0] - around),
                                                                              'max_exclusive': (origin[0] + around)}},
                                                                   {'name': 'Cartn_y', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[1] - around),
                                                                              'max_exclusive': (origin[1] + around)}},
                                                                   {'name': 'Cartn_z', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[2] - around),
                                                                              'max_exclusive': (origin[2] + around)}},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_neighbor) == 0:
                                    continue

                                neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), origin) < around]

                                for atom in neighbor:
                                    del atom['x']
                                    del atom['y']
                                    del atom['z']
                                    _atomSelection.append(atom)

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        self.factor['atom_selection'] = _atomSelection
                        if len(_atomSelection) == 0:
                            del self.factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName!r} {around} clause has no effect.")

                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect because no atom is selected.")

            elif ctx.Beyond_op():
                clauseName = 'beyond'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return

                around = self.numberFSelection[0]

                if around <= 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {around} clause has no effect "
                                  "because a given distance is out of range.")

                else:

                    self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                    if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                        _atomSel, _atomAll, _atomSelection = [], [], []

                        for _atom in self.factor['atom_selection']:

                            try:

                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': _atom['chain_id']},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': _atom['seq_id']},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': _atom['atom_id']},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) != 1:
                                    continue

                                origin = to_np_array(_origin[0])

                                _neighbor =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                  [{'name': 'Cartn_x', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[0] - around),
                                                                              'max_exclusive': (origin[0] + around)}},
                                                                   {'name': 'Cartn_y', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[1] - around),
                                                                              'max_exclusive': (origin[1] + around)}},
                                                                   {'name': 'Cartn_z', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[2] - around),
                                                                              'max_exclusive': (origin[2] + around)}},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_neighbor) == 0:
                                    continue

                                neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), origin) < around]

                                for atom in neighbor:
                                    del atom['x']
                                    del atom['y']
                                    del atom['z']
                                    _atomSel.append(atom)

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        try:

                            _atomAll =\
                                self.cR.getDictListWithFilter('atom_site',
                                                              AUTH_ATOM_DATA_ITEMS,
                                                              [{'name': self.modelNumName, 'type': 'int',
                                                                'value': self.representativeModelId},
                                                               {'name': 'label_alt_id', 'type': 'enum',
                                                                'enum': (self.representativeAltId,)}
                                                               ])

                            _atomSelection = [atom for atom in _atomAll if atom not in _atomSel]

                        except Exception as e:
                            if self.verbose:
                                self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        self.factor['atom_selection'] = _atomSelection
                        if len(_atomSelection) == 0:
                            del self.factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName!r} clause has no effect.")

                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} {around} clause has no effect because no atom is selected.")

            elif ctx.Withinbonds_op():
                clauseName = 'withinbonds'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return

                num_bonds = int(str(ctx.Integer(0)))

                if num_bonds <= 0 or num_bonds > 6:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {num_bonds} clause has no effect "
                                  "because the number of bonds is out of range.")

                else:

                    _CARTN_DATA_ITEMS = CARTN_DATA_ITEMS
                    _CARTN_DATA_ITEMS.append({'name': 'label_asym_id', 'type': 'str'})

                    self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                    if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:

                        around = num_bonds * 2.0

                        _atomNeighbors = {}

                        for _atom in self.factor['atom_selection']:

                            try:

                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  _CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': _atom['chain_id']},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': _atom['seq_id']},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': _atom['atom_id']},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) != 1:
                                    continue

                                origin = to_np_array(_origin[0])
                                label_asym_id = _origin[0]['label_asym_id']

                                _neighbor =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                  [{'name': 'Cartn_x', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[0] - around),
                                                                              'max_exclusive': (origin[0] + around)}},
                                                                   {'name': 'Cartn_y', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[1] - around),
                                                                              'max_exclusive': (origin[1] + around)}},
                                                                   {'name': 'Cartn_z', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[2] - around),
                                                                              'max_exclusive': (origin[2] + around)}},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)},
                                                                   {'name': 'label_asym_id', 'type': 'str',
                                                                    'value': label_asym_id}
                                                                   ])

                                if len(_neighbor) == 0:
                                    continue

                                neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), origin) < around]

                                n = 0

                                if n not in _atomNeighbors:
                                    _atomNeighbors[n] = []

                                _origin = next(atom for atom in neighbor if distance(to_np_array(atom), origin) < 0.001)

                                _atomNeighbors[n].append(_origin)
                                neighbor.remove(_origin)

                                while n < num_bonds:
                                    n += 1

                                    for _origin in _atomNeighbors[n - 1]:
                                        origin = to_np_array(_origin)
                                        _neighbor = [atom for atom in neighbor if distance(to_np_array(atom), origin) < 2.0]

                                        if len(_neighbor) == 0:
                                            break

                                        for _n in range(0, n):
                                            if _n in _atomNeighbors:
                                                for atom in _atomNeighbors[_n]:
                                                    if atom in _neighbor:
                                                        _neighbor.remove(atom)

                                        if len(_neighbor) == 0:
                                            break

                                        if n not in _atomNeighbors:
                                            _atomNeighbors[n] = []

                                        _atomNeighbors[n].extend(_neighbor)
                                        for atom in _neighbor:
                                            neighbor.remove(atom)

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        if num_bonds in _atomNeighbors and len(_atomNeighbors[num_bonds]) > 0:
                            _atomSelection = []

                            for atom in _atomNeighbors[num_bonds]:
                                del atom['x']
                                del atom['y']
                                del atom['z']
                                _atomSelection.append(atom)

                            self.factor['atom_selection'] = _atomSelection

                        else:
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName!r} {num_bonds} clause has no effect.")

                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} {num_bonds} clause has no effect because no atom is selected.")

            elif ctx.Beyondbonds_op():
                clauseName = 'beyondbonds'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return

                num_bonds = int(str(ctx.Integer(0)))

                if num_bonds <= 0 or num_bonds > 6:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} {num_bonds} clause has no effect "
                                  "because the number of bonds is out of range.")

                else:

                    _CARTN_DATA_ITEMS = CARTN_DATA_ITEMS
                    _CARTN_DATA_ITEMS.append({'name': 'label_asym_id', 'type': 'str'})

                    self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                    if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                        _atomSel, _atomAll, _atomSelection = [], [], []

                        around = num_bonds * 2.0
                        label_asym_id = ''

                        _atomNeighbors = {}

                        for _atom in self.factor['atom_selection']:

                            try:

                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  _CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': _atom['chain_id']},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': _atom['seq_id']},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': _atom['atom_id']},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) != 1:
                                    continue

                                origin = to_np_array(_origin[0])
                                label_asym_id = _origin[0]['label_asym_id']

                                _neighbor =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                  [{'name': 'Cartn_x', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[0] - around),
                                                                              'max_exclusive': (origin[0] + around)}},
                                                                   {'name': 'Cartn_y', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[1] - around),
                                                                              'max_exclusive': (origin[1] + around)}},
                                                                   {'name': 'Cartn_z', 'type': 'range-float',
                                                                    'range': {'min_exclusive': (origin[2] - around),
                                                                              'max_exclusive': (origin[2] + around)}},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)},
                                                                   {'name': 'label_asym_id', 'type': 'str',
                                                                    'value': label_asym_id}
                                                                   ])

                                if len(_neighbor) == 0:
                                    continue

                                neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), origin) < around]

                                n = 0

                                if n not in _atomNeighbors:
                                    _atomNeighbors[n] = []

                                _origin = next(atom for atom in neighbor if distance(to_np_array(atom), origin) < 0.001)

                                _atomNeighbors[n].append(_origin)
                                neighbor.remove(_origin)

                                while n < num_bonds:
                                    n += 1

                                    for _origin in _atomNeighbors[n - 1]:
                                        origin = to_np_array(_origin)
                                        _neighbor = [atom for atom in neighbor if distance(to_np_array(atom), origin) < 2.0]

                                        if len(_neighbor) == 0:
                                            break

                                        for _n in range(0, n):
                                            if _n in _atomNeighbors:
                                                for atom in _atomNeighbors[_n]:
                                                    if atom in _neighbor:
                                                        _neighbor.remove(atom)

                                        if len(_neighbor) == 0:
                                            break

                                        if n not in _atomNeighbors:
                                            _atomNeighbors[n] = []

                                        _atomNeighbors[n].extend(_neighbor)
                                        for atom in _neighbor:
                                            neighbor.remove(atom)

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        for n in range(0, num_bonds + 1):
                            if n in _atomNeighbors and len(_atomNeighbors[n]) > 0:
                                for atom in _atomNeighbors[n]:
                                    del atom['x']
                                    del atom['y']
                                    del atom['z']
                                    _atomSel.append(atom)

                        try:

                            _atomAll =\
                                self.cR.getDictListWithFilter('atom_site',
                                                              AUTH_ATOM_DATA_ITEMS,
                                                              [{'name': self.modelNumName, 'type': 'int',
                                                                'value': self.representativeModelId},
                                                               {'name': 'label_alt_id', 'type': 'enum',
                                                                'enum': (self.representativeAltId,)},
                                                               {'name': 'label_asym_id', 'type': 'str',
                                                                'value': label_asym_id}
                                                               ])

                            _atomSelection = [atom for atom in _atomAll if atom not in _atomSel]

                        except Exception as e:
                            if self.verbose:
                                self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                        self.factor['atom_selection'] = _atomSelection
                        if len(_atomSelection) == 0:
                            del self.factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName!r} {num_bonds} clause has no effect.")

                    else:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} {num_bonds} clause has no effect because no atom is selected.")

            elif ctx.Backbone():
                clauseName = 'backbone'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                atomIdSet = set()
                for compId in self.compIdSet:
                    atomIdSet |= set(atomId for atomId in self.csStat.getBackBoneAtoms(compId) if atomId[0] != 'H')

                self.factor['atom_id'] = list(atomIdSet) if len(atomIdSet) > 0 else None

            elif ctx.Sidechain():
                clauseName = 'sidechain'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                atomIdSet = set()
                for compId in self.compIdSet:
                    atomIdSet |= set(atomId for atomId in self.csStat.getSideChainAtoms(compId) if atomId[0] != 'H')

                self.factor['atom_id'] = list(atomIdSet) if len(atomIdSet) > 0 else None

            elif ctx.Water():
                clauseName = 'water'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")

                self.factor['comp_id'] = ['HOH']
                self.factor['atom_id'] = ['O']

            elif ctx.Methyl():  # /C3(-H1)(-H1)(-H1)/
                clauseName = 'methyl'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                chainIds = set()
                seqIds = set()
                compIds = set()
                atomIds = set()

                for k, v in self.coordAtomSite.items():
                    chainId, seqId = k
                    compId = v['comp_id']
                    c3 = [atomId for atomId in self.csStat.getMethylAtoms(compId) if atomId[0] == 'C']
                    if len(c3) == 0:
                        continue
                    for atomId in v['atom_id']:
                        if atomId in c3:
                            chainIds.add(chainId)
                            seqIds.add(seqId)
                            compIds.add(compId)
                            atomIds.add(atomId)

                if len(seqIds) == 0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} clause has no effect.")
                else:
                    self.factor['chain_id'] = list(chainIds)
                    self.factor['seq_id'] = sorted(list(seqIds))
                    self.factor['comp_id'] = list(compIds)
                    self.factor['atom_id'] = list(atomIds)

            elif ctx.Amide():  # /C2(=O2)-N2-H2/
                clauseName = 'amide'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return

                if self.polyPeptide:
                    authAsymIds = []
                    for entity in self.entityAssembly:
                        if 'entity_poly_type' in entity:
                            poly_type = entity['entity_poly_type']
                            if poly_type.startswith('polypeptide'):
                                authAsymIds.extend(entity['auth_asym_id'].split(','))
                    self.factor['chain_id'] = authAsymIds
                    self.factor['atom_id'] = ['C', 'N', 'H']

            elif ctx.Smarts():
                clauseName = 'smarts.'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {clauseName!r} {str(ctx.Simple_name(0))} clause has no effect "
                              "because the SMILES/SMARTS notation is not supported.")

            elif ctx.Slash_quote_string():
                clauseName = 'ASL slash quoted notation'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The {str(ctx.Slash_quote_string())} clause has no effect "
                              f"because the {clauseName} is not supported.")

            elif ctx.Not_op():
                if self.verbose_debug:
                    print("  " * self.depth + "--> not")
                if not self.hasCoord:
                    return

                if 'atom_selection' in self.factor and ('atom_id' in self.factor or 'atom_ids' in self.factor):
                    _refAtomSelection = self.factor['atom_selection']
                    del self.factor['atom_selection']
                    if self.stackFactors:
                        self.stackFactors.pop()
                    self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)
                    if 'atom_selection' in self.factor:
                        self.factor['atom_selection'] = [atom for atom in _refAtomSelection
                                                         if isinstance(atom, dict)
                                                         and not any(True for _atom in self.factor['atom_selection']
                                                                     if _atom['chain_id'] == atom['chain_id']
                                                                     and _atom['seq_id'] == atom['seq_id']
                                                                     and _atom['atom_id'] == atom['atom_id'])]
                    else:
                        self.factor['atom_selection'] = _refAtomSelection
                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      "The 'not' clause has no effect.")

                elif 'atom_selection' not in self.factor:

                    if len(self.factor) <= 3 and 'chain_id' in self.factor and len(self.factor['chain_id']) == 0\
                       and 'alt_chain_id' in self.factor:
                        self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)
                        for atom in self.factor['atom_selection']:
                            atom['segment_id'] = 'not ' + atom['segment_id']

                    else:
                        self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)

                        if 'atom_selection' in self.factor:
                            _refAtomSelection = deepcopy(self.factor['atom_selection'])
                            for atom in _refAtomSelection:
                                if 'is_poly' in atom:
                                    del atom['is_poly']
                                if 'auth_atom_id' in atom:
                                    del atom['auth_atom_id']
                                if 'segment_id' in atom:
                                    del atom['segment_id']

                            try:

                                _atomSelection =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_DATA_ITEMS,
                                                                  [{'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                            self.factor['atom_selection'] = [atom for atom in _atomSelection if atom not in _refAtomSelection]

                            if len(self.factor['atom_selection']) == 0:
                                self.factor['atom_id'] = [None]
                                self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                              "The 'not' clause has no effect.")

                        else:
                            self.factor['atom_id'] = [None]
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          "The 'not' clause has no effect.")

                else:

                    try:

                        _atomSelection =\
                            self.cR.getDictListWithFilter('atom_site',
                                                          AUTH_ATOM_DATA_ITEMS,
                                                          [{'name': self.modelNumName, 'type': 'int',
                                                            'value': self.representativeModelId},
                                                           {'name': 'label_alt_id', 'type': 'enum',
                                                            'enum': (self.representativeAltId,)}
                                                           ])

                    except Exception as e:
                        if self.verbose:
                            self.log.write(f"+{self.class_name__}.exitFactor() ++ Error  - {str(e)}")

                    _refAtomSelection = deepcopy(self.factor['atom_selection'])
                    for atom in _refAtomSelection:
                        if 'is_poly' in atom:
                            del atom['is_poly']
                        if 'auth_atom_id' in atom:
                            del atom['auth_atom_id']
                        if 'segment_id' in atom:
                            del atom['segment_id']

                    _refAtomSelection = [atom for atom in _refAtomSelection if atom in _atomSelection]

                    self.factor['atom_selection'] = [atom for atom in _atomSelection if atom not in _refAtomSelection]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      "The 'not' clause has no effect.")

            elif ctx.Simple_name(0):
                clauseName = 'store'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")

                name = str(ctx.Simple_name(0))

                if name not in self.storeSet:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The '{name}' clause has no effect "
                                  "because the internal statement is not set yet.")
                else:
                    self.factor = deepcopy(self.storeSet[name])

            if self.depth > 0 and self.cur_union_expr:
                self.unionFactor = self.factor
            else:
                self.stackFactors.append(self.factor)

        finally:
            self.numberFSelection.clear()

    # Enter a parse tree produced by SchrodingerMRParser#number.
    def enterNumber(self, ctx: SchrodingerMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#number.
    def exitNumber(self, ctx: SchrodingerMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by SchrodingerMRParser#number_f.
    def enterNumber_f(self, ctx: SchrodingerMRParser.Number_fContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by SchrodingerMRParser#number_f.
    def exitNumber_f(self, ctx: SchrodingerMRParser.Number_fContext):
        if ctx.Float():
            self.numberFSelection.append(float(str(ctx.Float())))

        elif ctx.Integer():
            self.numberFSelection.append(float(str(ctx.Integer())))

        else:
            self.numberFSelection.append(None)

    # Enter a parse tree produced by SchrodingerMRParser#parameter_statement.
    def enterParameter_statement(self, ctx: SchrodingerMRParser.Parameter_statementContext):
        self.__cur_store_name = str(ctx.Simple_name())

        self.depth = 0
        self.atomSelectionSet.clear()

        self.enterSelection(ctx)

    # Exit a parse tree produced by SchrodingerMRParser#parameter_statement.
    def exitParameter_statement(self, ctx: SchrodingerMRParser.Parameter_statementContext):
        self.exitSelection(ctx)

        if len(self.atomSelectionSet) == 1 and len(self.atomSelectionSet[0]) > 0 and self.__cur_store_name not in emptyValue:
            self.storeSet[self.__cur_store_name] = copy.copy(self.atomSelectionSet[0])

        self.atomSelectionSet.clear()
        self.g.clear()

# del SchrodingerMRParser
