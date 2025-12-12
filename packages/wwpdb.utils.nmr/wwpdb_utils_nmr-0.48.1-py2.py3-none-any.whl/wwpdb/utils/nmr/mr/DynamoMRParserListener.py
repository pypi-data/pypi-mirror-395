##
# File: DynamoMRParserListener.py
# Date: 17-Jun-2022
#
# Updates:
""" ParserLister class for DYNAMO/PALES/TALOS MR files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import itertools
import copy

from antlr4 import ParseTreeListener
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.DynamoMRParser import DynamoMRParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       hasIntraChainRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       getRdcCode,
                                                       getStructConnPtnrAtom,
                                                       getRow,
                                                       getStarAtom,
                                                       resetCombinationId,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       KNOWN_ANGLE_ATOM_NAMES,
                                                       KNOWN_ANGLE_SEQ_OFFSET)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           emptyValue,
                                           rdcBbPairCode)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.DynamoMRParser import DynamoMRParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           hasIntraChainRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRdcCode,
                                           getStructConnPtnrAtom,
                                           getRow,
                                           getStarAtom,
                                           resetCombinationId,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getPotentialType,
                                           ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           KNOWN_ANGLE_ATOM_NAMES,
                                           KNOWN_ANGLE_SEQ_OFFSET)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               emptyValue,
                               rdcBbPairCode)


TALOS_PREDICTION_CLASSES = ('Strong', 'Good', 'Generous', 'Warn', 'Bad', 'Dyn', 'New', 'None')
TALOS_PREDICTION_MIN_CLASSES = ('Strong', 'Good')


# This class defines a complete listener for a parse tree produced by DynamoMRParser.
class DynamoMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ()

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None,
                 reasons: Optional[dict] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        super().__init__(verbose, log, representativeModelId, representativeAltId, mrAtomNameMapping,
                         cR, caC, nefT, reasons)

        self.file_type = 'nm-res-dyn'
        self.software_name = 'DYNAMO/PALES/TALOS'

    # Enter a parse tree produced by DynamoMRParser#dynamo_mr.
    def enterDynamo_mr(self, ctx: DynamoMRParser.Dynamo_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by DynamoMRParser#dynamo_mr.
    def exitDynamo_mr(self, ctx: DynamoMRParser.Dynamo_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by DynamoMRParser#sequence.
    def enterSequence(self, ctx: DynamoMRParser.SequenceContext):
        if self.has_sequence and not self.open_sequence:
            self.first_resid = 1
            self.cur_sequence = ''

        if ctx.First_resid():
            self.first_resid = int(str(ctx.Integer_DA()))

        if ctx.Sequence():
            if self.hasCoord:
                i = 0
                while ctx.One_letter_code(i):
                    self.cur_sequence += str(ctx.One_letter_code(i))
                    i += 1

        self.open_sequence = True

    # Exit a parse tree produced by DynamoMRParser#sequence.
    def exitSequence(self, ctx: DynamoMRParser.SequenceContext):  # pylint: disable=unused-argument
        pass

    def closeSequence(self):
        self.has_seq_align_err = False

        if not self.open_sequence:
            return

        self.has_sequence = len(self.cur_sequence) > 0

        self.open_sequence = False

    # Enter a parse tree produced by DynamoMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: DynamoMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: DynamoMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: DynamoMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: DynamoMRParser.Distance_restraintContext):

        try:

            index = int(str(ctx.Integer(0)))
            group = int(str(ctx.Integer(1)))

            seqId1 = int(str(ctx.Integer(2)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(3)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]
            weight = self.numberSelection[3]
            scale = self.numberSelection[4]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            if scale < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' must not be a negative value.")
                return
            if scale == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' should be a positive value.")

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(None, seqId1, compId1, atomId1.split('|', 1)[0], index, group)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(None, seqId2, compId2, atomId2.split('|', 1)[0], index, group)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, True, index, group)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, True, index, group)

            if len(self.atomSelectionSet) < 2:
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

            dstFunc = self.validateDistanceRangeWithIndex(index, group, weight, scale, target_value, lower_limit, upper_limit, self.omitDistLimitOutlier)

            if dstFunc is None:
                return

            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                                 self.csStat, self.originalFileName),
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            memberId = '.'
            if self.createSfDict:
                if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                    memberLogicCode = '.'

                if memberLogicCode == 'OR':
                    if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        memberId = 0
                        _atom1 = _atom2 = None

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if self.createSfDict and isinstance(memberId, int):
                    star_atom1 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom1))
                    star_atom2 = getStarAtom(self.authToStarSeq, self.authToOrigSeq, self.offsetHolder, copy.copy(atom2))
                    if None in (star_atom1, star_atom2) or isIdenticalRestraint([star_atom1, star_atom2], self.nefT):
                        continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.createSfDict and memberLogicCode == '.':
                    altAtomId1, altAtomId2 = getAltProtonIdInBondConstraint(atoms, self.csStat)
                    if altAtomId1 is not None or altAtomId2 is not None:
                        atom1, atom2 =\
                            self.selectRealisticBondConstraint(atom1, atom2,
                                                               altAtomId1, altAtomId2,
                                                               dstFunc)
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.distRestraints} (index={index}, group={group}) "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if isinstance(memberId, int):
                        if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                           or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                            memberId += 1
                            _atom1, _atom2 = atom1, atom2
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberId, memberLogicCode,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

                    if sf['constraint_subsubtype'] == 'ambi':
                        continue

                    if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                        sf['constraint_subsubtype'] = 'ambi'

                    if memberLogicCode == 'OR'\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        sf['constraint_subsubtype'] = 'ambi'

                    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                        upperLimit = float(dstFunc['upper_limit'])
                        if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                            sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.distRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#distance_restraints_sw_segid.
    def enterDistance_restraints_sw_segid(self, ctx: DynamoMRParser.Distance_restraints_sw_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#distance_restraints_sw_segid.
    def exitDistance_restraints_sw_segid(self, ctx: DynamoMRParser.Distance_restraints_sw_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#distance_restraint_sw_segid.
    def enterDistance_restraint_sw_segid(self, ctx: DynamoMRParser.Distance_restraint_sw_segidContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#distance_restraint_sw_segid.
    def exitDistance_restraint_sw_segid(self, ctx: DynamoMRParser.Distance_restraint_sw_segidContext):

        try:

            index = int(str(ctx.Integer(0)))
            group = int(str(ctx.Integer(1)))

            chainId1 = str(ctx.Simple_name(0))
            seqId1 = int(str(ctx.Integer(2)))
            compId1 = str(ctx.Simple_name(1)).upper()
            atomId1 = str(ctx.Simple_name(2)).upper()
            chainId2 = str(ctx.Simple_name(3))
            seqId2 = int(str(ctx.Integer(3)))
            compId2 = str(ctx.Simple_name(4)).upper()
            atomId2 = str(ctx.Simple_name(5)).upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]
            weight = self.numberSelection[3]
            scale = self.numberSelection[4]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            if scale < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' must not be a negative value.")
                return
            if scale == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' should be a positive value.")

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1.split('|', 1)[0], index, group)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2.split('|', 1)[0], index, group)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, True, index, group)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, True, index, group)

            if len(self.atomSelectionSet) < 2:
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

            dstFunc = self.validateDistanceRangeWithIndex(index, group, weight, scale, target_value, lower_limit, upper_limit, self.omitDistLimitOutlier)

            if dstFunc is None:
                return

            memberId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                                 self.csStat, self.originalFileName),
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                if memberLogicCode == 'OR':
                    if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        memberId = 0
                        _atom1 = _atom2 = None

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
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
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.distRestraints} (index={index}, group={group}) "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if isinstance(memberId, int):
                        if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                           or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                            memberId += 1
                            _atom1, _atom2 = atom1, atom2
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberId, memberLogicCode,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

                    if sf['constraint_subsubtype'] == 'ambi':
                        continue

                    if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                        sf['constraint_subsubtype'] = 'ambi'

                    if memberLogicCode == 'OR'\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        sf['constraint_subsubtype'] = 'ambi'

                    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                        upperLimit = float(dstFunc['upper_limit'])
                        if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                            sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.distRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#distance_restraints_ew_segid.
    def enterDistance_restraints_ew_segid(self, ctx: DynamoMRParser.Distance_restraints_ew_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#distance_restraints_ew_segid.
    def exitDistance_restraints_ew_segid(self, ctx: DynamoMRParser.Distance_restraints_ew_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#distance_restraint_ew_segid.
    def enterDistance_restraint_ew_segid(self, ctx: DynamoMRParser.Distance_restraint_ew_segidContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#distance_restraint_ew_segid.
    def exitDistance_restraint_ew_segid(self, ctx: DynamoMRParser.Distance_restraint_ew_segidContext):

        try:

            index = int(str(ctx.Integer(0)))
            group = int(str(ctx.Integer(1)))

            seqId1 = int(str(ctx.Integer(2)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            chainId1 = str(ctx.Simple_name(2))
            chainId2 = str(ctx.Simple_name(5))
            seqId2 = int(str(ctx.Integer(3)))
            compId2 = str(ctx.Simple_name(3)).upper()
            atomId2 = str(ctx.Simple_name(4)).upper()
            chainId2 = str(ctx.Simple_name(5))

            target_value = None
            lower_limit = None
            upper_limit = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]
            weight = self.numberSelection[3]
            scale = self.numberSelection[4]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            if scale < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' must not be a negative value.")
                return
            if scale == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The relative scale value of '{scale}' should be a positive value.")

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1.split('|', 1)[0], index, group)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2.split('|', 1)[0], index, group)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, True, index, group)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, True, index, group)

            if len(self.atomSelectionSet) < 2:
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

            dstFunc = self.validateDistanceRangeWithIndex(index, group, weight, scale, target_value, lower_limit, upper_limit, self.omitDistLimitOutlier)

            if dstFunc is None:
                return

            memberId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                                 self.csStat, self.originalFileName),
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                if memberLogicCode == 'OR':
                    if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        memberId = 0
                        _atom1 = _atom2 = None

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
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
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.distRestraints} (index={index}, group={group}) "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if isinstance(memberId, int):
                        if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                           or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                            memberId += 1
                            _atom1, _atom2 = atom1, atom2
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberId, memberLogicCode,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

                    if sf['constraint_subsubtype'] == 'ambi':
                        continue

                    if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                        sf['constraint_subsubtype'] = 'ambi'

                    if memberLogicCode == 'OR'\
                       and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                            or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                        sf['constraint_subsubtype'] = 'ambi'
                    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                        upperLimit = float(dstFunc['upper_limit'])
                        if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                            sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.distRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraints.
    def enterTorsion_angle_restraints(self, ctx: DynamoMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraints.
    def exitTorsion_angle_restraints(self, ctx: DynamoMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraint.
    def enterTorsion_angle_restraint(self, ctx: DynamoMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraint.
    def exitTorsion_angle_restraint(self, ctx: DynamoMRParser.Torsion_angle_restraintContext):

        try:

            index = int(str(ctx.Integer(0)))

            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(4)).upper()
            atomId3 = str(ctx.Simple_name(5)).upper()
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(6)).upper()
            atomId4 = str(ctx.Simple_name(7)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]

            dstFunc = self.validateAngleRangeWithIndex(index, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(None, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(None, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(None, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(None, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                self.areUniqueCoordAtoms('a torsion angle')
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a torsion angle',
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
                                                                                           self.getCurrentRestraint(n=index))
                        self.f.append(err)

                    if angleName in emptyValue and atomSelTotal != 4:
                        continue

                    fixedAngleName = angleName
                    break

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO/TALOS')

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
                                                                                       self.getCurrentRestraint(n=index))
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
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} (index={index}) angleName={angleName} "
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
                                 atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraints_sw_segid.
    def enterTorsion_angle_restraints_sw_segid(self, ctx: DynamoMRParser.Torsion_angle_restraints_sw_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraints_sw_segid.
    def exitTorsion_angle_restraints_sw_segid(self, ctx: DynamoMRParser.Torsion_angle_restraints_sw_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraint_sw_segid.
    def enterTorsion_angle_restraint_sw_segid(self, ctx: DynamoMRParser.Torsion_angle_restraint_sw_segidContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraint_sw_segid.
    def exitTorsion_angle_restraint_sw_segid(self, ctx: DynamoMRParser.Torsion_angle_restraint_sw_segidContext):

        try:

            index = int(str(ctx.Integer(0)))

            chainId1 = str(ctx.Simple_name(0))
            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(1)).upper()
            atomId1 = str(ctx.Simple_name(2)).upper()
            chainId2 = str(ctx.Simple_name(3))
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(4)).upper()
            atomId2 = str(ctx.Simple_name(5)).upper()
            chainId3 = str(ctx.Simple_name(6))
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(7)).upper()
            atomId3 = str(ctx.Simple_name(8)).upper()
            chainId4 = str(ctx.Simple_name(9))
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(10)).upper()
            atomId4 = str(ctx.Simple_name(11)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]

            dstFunc = self.validateAngleRangeWithIndex(None, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(chainId3, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(chainId4, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                self.areUniqueCoordAtoms('a torsion angle')
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a torsion angle',
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
                                                                                           self.getCurrentRestraint(n=index))
                        self.f.append(err)

                    if angleName in emptyValue and atomSelTotal != 4:
                        continue

                    fixedAngleName = angleName
                    break

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO/TALOS')

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
                                                                                       self.getCurrentRestraint(n=index))
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
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} (index={index}) angleName={angleName} "
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
                                 atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraints_ew_segid.
    def enterTorsion_angle_restraints_ew_segid(self, ctx: DynamoMRParser.Torsion_angle_restraints_ew_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraints_ew_segid.
    def exitTorsion_angle_restraints_ew_segid(self, ctx: DynamoMRParser.Torsion_angle_restraints_ew_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#torsion_angle_restraint_ew_segid.
    def enterTorsion_angle_restraint_ew_segid(self, ctx: DynamoMRParser.Torsion_angle_restraint_ew_segidContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#torsion_angle_restraint_ew_segid.
    def exitTorsion_angle_restraint_ew_segid(self, ctx: DynamoMRParser.Torsion_angle_restraint_ew_segidContext):

        try:

            index = int(str(ctx.Integer(0)))

            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            chainId1 = str(ctx.Simple_name(2))
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(3)).upper()
            atomId2 = str(ctx.Simple_name(4)).upper()
            chainId2 = str(ctx.Simple_name(5))
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(6)).upper()
            atomId3 = str(ctx.Simple_name(7)).upper()
            chainId3 = str(ctx.Simple_name(8))
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(9)).upper()
            atomId4 = str(ctx.Simple_name(10)).upper()
            chainId4 = str(ctx.Simple_name(11))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # fource_const = self.numberSelection[2]

            dstFunc = self.validateAngleRangeWithIndex(None, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(chainId3, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(chainId4, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                self.areUniqueCoordAtoms('a torsion angle')
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a torsion angle',
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
                                                                                           self.getCurrentRestraint(n=index))
                        self.f.append(err)

                    if angleName in emptyValue and atomSelTotal != 4:
                        continue

                    fixedAngleName = angleName
                    break

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO/TALOS')

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
                                                                                       self.getCurrentRestraint(n=index))
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
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} (index={index}) angleName={angleName} "
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
                                 atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#rdc_restraints.
    def enterRdc_restraints(self, ctx: DynamoMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'rdc'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraints.
    def exitRdc_restraints(self, ctx: DynamoMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: DynamoMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: DynamoMRParser.Rdc_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            diffSeqId = seqId1 - seqId2

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(None, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(None, seqId2, compId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC'):
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
            except IndexError:
                self.areUniqueCoordAtoms('an RDC')
                return

            if self.has_seq_align_err and seq_id_1 - seq_id_2 != diffSeqId:
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-chain RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                      "Found an RDC vector over multiple covalent bonds; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                            softwareName='DYNAMO/PALES')
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) > 1 or len(self.atomSelectionSet[1]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.rdcRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#rdc_restraints_sw_segid.
    def enterRdc_restraints_sw_segid(self, ctx: DynamoMRParser.Rdc_restraints_sw_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'rdc'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraints_sw_segid.
    def exitRdc_restraints_sw_segid(self, ctx: DynamoMRParser.Rdc_restraints_sw_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#rdc_restraint_sw_segid.
    def enterRdc_restraint_sw_segid(self, ctx: DynamoMRParser.Rdc_restraint_sw_segidContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraint_sw_segid.
    def exitRdc_restraint_sw_segid(self, ctx: DynamoMRParser.Rdc_restraint_sw_segidContext):

        try:

            chainId1 = str(ctx.Simple_name(0))
            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(1)).upper()
            atomId1 = str(ctx.Simple_name(2)).upper()
            chainId2 = str(ctx.Simple_name(3))
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(4)).upper()
            atomId2 = str(ctx.Simple_name(5)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            diffSeqId = seqId1 - seqId2

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC'):
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
            except IndexError:
                self.areUniqueCoordAtoms('an RDC')
                return

            if self.has_seq_align_err and seq_id_1 - seq_id_2 != diffSeqId:
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-chain RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                      "Found an RDC vector over multiple covalent bonds; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                            softwareName='DYNAMO/PALES')
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) > 1 or len(self.atomSelectionSet[1]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.rdcRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#rdc_restraints_ew_segid.
    def enterRdc_restraints_ew_segid(self, ctx: DynamoMRParser.Rdc_restraints_ew_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'rdc'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraints_ew_segid.
    def exitRdc_restraints_ew_segid(self, ctx: DynamoMRParser.Rdc_restraints_ew_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#rdc_restraint_ew_segid.
    def enterRdc_restraint_ew_segid(self, ctx: DynamoMRParser.Rdc_restraint_ew_segidContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#rdc_restraint_ew_segid.
    def exitRdc_restraint_ew_segid(self, ctx: DynamoMRParser.Rdc_restraint_ew_segidContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            chainId1 = str(ctx.Simple_name(2))
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(3)).upper()
            atomId2 = str(ctx.Simple_name(4)).upper()
            chainId2 = str(ctx.Simple_name(5))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            diffSeqId = seqId1 - seqId2

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC'):
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
            except IndexError:
                self.areUniqueCoordAtoms('an RDC')
                return

            if self.has_seq_align_err and seq_id_1 - seq_id_2 != diffSeqId:
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-chain RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                      "Found an RDC vector over multiple covalent bonds; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                            softwareName='DYNAMO/PALES')
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) > 1 or len(self.atomSelectionSet[1]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.rdcRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#pales_meta_outputs.
    def enterPales_meta_outputs(self, ctx: DynamoMRParser.Pales_meta_outputsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by DynamoMRParser#pales_meta_outputs.
    def exitPales_meta_outputs(self, ctx: DynamoMRParser.Pales_meta_outputsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#pales_rdc_outputs.
    def enterPales_rdc_outputs(self, ctx: DynamoMRParser.Pales_rdc_outputsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'rdc'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#pales_rdc_outputs.
    def exitPales_rdc_outputs(self, ctx: DynamoMRParser.Pales_rdc_outputsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#pales_rdc_output.
    def enterPales_rdc_output(self, ctx: DynamoMRParser.Pales_rdc_outputContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#pales_rdc_output.
    def exitPales_rdc_output(self, ctx: DynamoMRParser.Pales_rdc_outputContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            # di
            target = self.numberSelection[1]  # d_obs
            # d (calc)
            # d_diff
            error = abs(self.numberSelection[4])
            weight = self.numberSelection[5]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            diffSeqId = seqId1 - seqId2

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(None, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(None, seqId2, compId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC'):
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']
            except IndexError:
                self.areUniqueCoordAtoms('an RDC')
                return

            if self.has_seq_align_err and seq_id_1 - seq_id_2 != diffSeqId:
                return

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-chain RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                      "Found an RDC vector over multiple covalent bonds; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.createSfDict:
                sf = self.getSfWithSoftware(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                            softwareName='PALES')
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) > 1 or len(self.atomSelectionSet[1]) > 1:
                    combinationId = 0

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                atoms = [atom1, atom2]
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                    continue
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except ValueError:
            self.rdcRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#coupling_restraints.
    def enterCoupling_restraints(self, ctx: DynamoMRParser.Coupling_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'jcoup'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraints.
    def exitCoupling_restraints(self, ctx: DynamoMRParser.Coupling_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#coupling_restraint.
    def enterCoupling_restraint(self, ctx: DynamoMRParser.Coupling_restraintContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraint.
    def exitCoupling_restraint(self, ctx: DynamoMRParser.Coupling_restraintContext):

        try:

            index = int(str(ctx.Integer(0)))

            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(4)).upper()
            atomId3 = str(ctx.Simple_name(5)).upper()
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(6)).upper()
            atomId4 = str(ctx.Simple_name(7)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            A = self.numberSelection[0]
            B = self.numberSelection[1]
            C = self.numberSelection[2]
            phase = self.numberSelection[3]
            target_value = self.numberSelection[4]
            lower_limit = upper_limit = None
            # fource_const = self.numberSelection[5]

            dstFunc = self.validateCoupRangeWithIndex(index, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(None, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(None, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(None, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(None, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            if not self.areUniqueCoordAtoms('a scalar coupling'):
                return

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)

            first_item = True

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

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
                                                                                       self.getCurrentRestraint(n=index))
                    self.f.append(err)

                if angleName in emptyValue and atomSelTotal != 4:
                    continue

                if angleName == 'PHI':
                    self.auxAtomSelectionSet.clear()
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'H', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'N', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'CA', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'HA', False)
                if self.debug:
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 2:
                            print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                                  f"A={A} B={B} C={C} phase={phase} "
                                  f"atom1={self.auxAtomSelectionSet[0][0]} atom2={self.auxAtomSelectionSet[1][0]} "
                                  f"atom1={self.auxAtomSelectionSet[2][0]} atom2={self.auxAtomSelectionSet[3][0]} {dstFunc}")
                    else:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                              f"A={A} B={B} C={C} phase={phase} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 4:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         self.auxAtomSelectionSet[0][0], self.auxAtomSelectionSet[1][0],
                                         self.auxAtomSelectionSet[2][0], self.auxAtomSelectionSet[3][0])
                            sf['loop'].add_data(row)
                    else:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)

        except ValueError:
            self.jcoupRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#coupling_restraints_sw_segid.
    def enterCoupling_restraints_sw_segid(self, ctx: DynamoMRParser.Coupling_restraints_sw_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'jcoup'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraints_sw_segid.
    def exitCoupling_restraints_sw_segid(self, ctx: DynamoMRParser.Coupling_restraints_sw_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#coupling_restraint_sw_segid.
    def enterCoupling_restraint_sw_segid(self, ctx: DynamoMRParser.Coupling_restraint_sw_segidContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraint_sw_segid.
    def exitCoupling_restraint_sw_segid(self, ctx: DynamoMRParser.Coupling_restraint_sw_segidContext):

        try:

            index = int(str(ctx.Integer(0)))

            chainId1 = str(ctx.Simple_name(0))
            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(1)).upper()
            atomId1 = str(ctx.Simple_name(2)).upper()
            chainId2 = str(ctx.Simple_name(3))
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(4)).upper()
            atomId2 = str(ctx.Simple_name(5)).upper()
            chainId3 = str(ctx.Simple_name(6))
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(7)).upper()
            atomId3 = str(ctx.Simple_name(8)).upper()
            chainId4 = str(ctx.Simple_name(9))
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(10)).upper()
            atomId4 = str(ctx.Simple_name(11)).upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            A = self.numberSelection[0]
            B = self.numberSelection[1]
            C = self.numberSelection[2]
            phase = self.numberSelection[3]
            target_value = self.numberSelection[4]
            lower_limit = upper_limit = None
            # fource_const = self.numberSelection[5]

            dstFunc = self.validateCoupRangeWithIndex(index, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(chainId3, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(chainId4, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            if not self.areUniqueCoordAtoms('a scalar coupling'):
                return

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)

            first_item = True

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

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
                                                                                       self.getCurrentRestraint(n=index))
                    self.f.append(err)

                if angleName in emptyValue and atomSelTotal != 4:
                    continue

                if angleName == 'PHI':
                    self.auxAtomSelectionSet.clear()
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'H', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'N', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'CA', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'HA', False)
                if self.debug:
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 2:
                            print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                                  f"A={A} B={B} C={C} phase={phase} "
                                  f"atom1={self.auxAtomSelectionSet[0][0]} atom2={self.auxAtomSelectionSet[1][0]} "
                                  f"atom1={self.auxAtomSelectionSet[2][0]} atom2={self.auxAtomSelectionSet[3][0]} {dstFunc}")
                    else:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                              f"A={A} B={B} C={C} phase={phase} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 4:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         self.auxAtomSelectionSet[0][0], self.auxAtomSelectionSet[1][0],
                                         self.auxAtomSelectionSet[2][0], self.auxAtomSelectionSet[3][0])
                            sf['loop'].add_data(row)
                    else:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)

        except ValueError:
            self.jcoupRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#coupling_restraints_ew_segid.
    def enterCoupling_restraints_ew_segid(self, ctx: DynamoMRParser.Coupling_restraints_ew_segidContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'jcoup'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraints_ew_segid.
    def exitCoupling_restraints_ew_segid(self, ctx: DynamoMRParser.Coupling_restraints_ew_segidContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#coupling_restraint_ew_segid.
    def enterCoupling_restraint_ew_segid(self, ctx: DynamoMRParser.Coupling_restraint_ew_segidContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#coupling_restraint_ew_segid.
    def exitCoupling_restraint_ew_segid(self, ctx: DynamoMRParser.Coupling_restraint_ew_segidContext):

        try:

            index = int(str(ctx.Integer(0)))

            seqId1 = int(str(ctx.Integer(1)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            chainId1 = str(ctx.Simple_name(2))
            seqId2 = int(str(ctx.Integer(2)))
            compId2 = str(ctx.Simple_name(3)).upper()
            atomId2 = str(ctx.Simple_name(4)).upper()
            chainId2 = str(ctx.Simple_name(5))
            seqId3 = int(str(ctx.Integer(3)))
            compId3 = str(ctx.Simple_name(6)).upper()
            atomId3 = str(ctx.Simple_name(7)).upper()
            chainId3 = str(ctx.Simple_name(8))
            seqId4 = int(str(ctx.Integer(4)))
            compId4 = str(ctx.Simple_name(9)).upper()
            atomId4 = str(ctx.Simple_name(10)).upper()
            chainId4 = str(ctx.Simple_name(11))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            A = self.numberSelection[0]
            B = self.numberSelection[1]
            C = self.numberSelection[2]
            phase = self.numberSelection[3]
            target_value = self.numberSelection[4]
            lower_limit = upper_limit = None
            # fource_const = self.numberSelection[5]

            dstFunc = self.validateCoupRangeWithIndex(index, 1.0, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithIndex(chainId1, seqId1, compId1, atomId1, index)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithIndex(chainId2, seqId2, compId2, atomId2, index)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithIndex(chainId3, seqId3, compId3, atomId3, index)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithIndex(chainId4, seqId4, compId4, atomId4, index)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                return

            self.selectCoordAtomsWithIndex(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtomsWithIndex(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtomsWithIndex(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtomsWithIndex(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            if not self.areUniqueCoordAtoms('a scalar coupling'):
                return

            sf = None
            if self.createSfDict:
                sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                            softwareName='DYNAMO')

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)

            first_item = True

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

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
                                                                                       self.getCurrentRestraint(n=index))
                    self.f.append(err)

                if angleName in emptyValue and atomSelTotal != 4:
                    continue

                if angleName == 'PHI':
                    self.auxAtomSelectionSet.clear()
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'H', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign2, seqId2, compId2, 'N', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'CA', False)
                    self.selectAuxCoordAtomsWithIndex(chainAssign3, seqId3, compId3, 'HA', False)
                if self.debug:
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 2:
                            print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                                  f"A={A} B={B} C={C} phase={phase} "
                                  f"atom1={self.auxAtomSelectionSet[0][0]} atom2={self.auxAtomSelectionSet[1][0]} "
                                  f"atom1={self.auxAtomSelectionSet[2][0]} atom2={self.auxAtomSelectionSet[3][0]} {dstFunc}")
                    else:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} (index={index}) angleName={angleName} "
                              f"A={A} B={B} C={C} phase={phase} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    if angleName == 'PHI':
                        if len(self.auxAtomSelectionSet) == 4:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         self.auxAtomSelectionSet[0][0], self.auxAtomSelectionSet[1][0],
                                         self.auxAtomSelectionSet[2][0], self.auxAtomSelectionSet[3][0])
                            sf['loop'].add_data(row)
                    else:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)

        except ValueError:
            self.jcoupRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#talos_restraints.
    def enterTalos_restraints(self, ctx: DynamoMRParser.Talos_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#talos_restraints.
    def exitTalos_restraints(self, ctx: DynamoMRParser.Talos_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#talos_restraint.
    def enterTalos_restraint(self, ctx: DynamoMRParser.Talos_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#talos_restraint.
    def exitTalos_restraint(self, ctx: DynamoMRParser.Talos_restraintContext):

        try:

            seqId = int(str(ctx.Integer(0)))
            compId = str(ctx.Simple_name(0)).upper()

            if compId not in monDict3.values() and compId not in monDict3:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Found unknown residue name {compId!r}.")
                return

            if len(compId) >= 3:
                pass
            else:
                compId = next(k for k, v in monDict3.items() if v == compId and len(k) == 3)

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            # phi
            phi_target_value = self.numberSelection[0]
            psi_target_value = self.numberSelection[1]

            delta_phi_value = self.numberSelection[2]
            delta_psi_value = self.numberSelection[3]

            # dist = self.numberSelection[4]
            # s2 = self.numberSelection[5]

            # count = int(str(ctx.Integer(1)))
            # cs_count = int(str(ctx.Integer(2)))

            _class = str(ctx.Simple_name(1))

            if _class not in TALOS_PREDICTION_CLASSES:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The class name {_class!r} should be one of {TALOS_PREDICTION_CLASSES}.")
                return

            if _class not in TALOS_PREDICTION_MIN_CLASSES:  # ignore suspicious predictions
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            for angleName in ('PHI', 'PSI'):
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                if angleName == 'PHI':
                    target_value = phi_target_value
                    if delta_phi_value > 0.0:
                        lower_limit = phi_target_value - delta_phi_value
                        upper_limit = phi_target_value + delta_phi_value
                    else:
                        lower_limit = upper_limit = None
                else:
                    target_value = psi_target_value
                    if delta_psi_value > 0.0:
                        lower_limit = psi_target_value - delta_psi_value
                        upper_limit = psi_target_value + delta_psi_value
                    else:
                        lower_limit = upper_limit = None

                dstFunc = self.validateAngleRangeWithIndex(None, 1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                    if atomId is None:
                        resKey = (seqId, compId)
                        if resKey not in self.extResKey:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{seqId}:{compId} is not present in the coordinates.")
                        return

                self.retrieveLocalSeqScheme()

                chainAssign, _ = self.assignCoordPolymerSequenceWithIndex(None, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    for ord, (atomId, offset) in enumerate(zip(atomNames, seqOffset)):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)]
                                                                    if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None and offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            idx = ps['auth_seq_id'].index(cifSeqId)
                            try:
                                _cifSeqId = ps['auth_seq_id'][idx + offset]
                                _cifCompId = ps['comp_id'][idx + offset]
                            except IndexError:
                                pass

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None and not self.allow_ext_seq:
                                self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                              f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                              f"of chain {chainId} of the coordinates. "
                                              "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList
                                              if cca[self.ccU.ccaAtomId] == atomId), None)
                            if cifAtomId is None:
                                if ord == 0:
                                    _cifSeqId += seqOffset[ord + 1] - offset
                                    ptnr = getStructConnPtnrAtom(self.cR, chainId, _cifSeqId, atomNames[ord + 1])
                                    if ptnr is not None and atomId[0] == ptnr['atom_id'][0]:
                                        cifAtomId = ptnr['atom_id']
                                elif ord == 3:
                                    _cifSeqId += seqOffset[ord - 1] - offset
                                    ptnr = getStructConnPtnrAtom(self.cR, chainId, _cifSeqId, atomNames[ord - 1])
                                    if ptnr is not None and atomId[0] == ptnr['atom_id'][0]:
                                        cifAtomId = ptnr['atom_id']

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
                    except IndexError:
                        self.areUniqueCoordAtoms('a torsion angle (TALOS)')
                        return

                    len_f = len(self.f)
                    self.areUniqueCoordAtoms('a torsion angle (TALOS)',
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
                            _angleName = getTypeOfDihedralRestraint(True, False, False,
                                                                    atoms,
                                                                    'plane_like' in dstFunc)

                            if _angleName is not None and _angleName.startswith('pseudo'):
                                _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                    atoms,
                                                                                                    self.getCurrentRestraint())
                                self.f.append(err)

                            if _angleName in emptyValue and atomSelTotal != 4:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                                    softwareName='TALOS')
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        atoms = [atom1, atom2, atom3, atom4]
                        if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(True, False, False,
                                                                atoms,
                                                                'plane_like' in dstFunc)

                        if _angleName is not None and _angleName.startswith('pseudo'):
                            _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                atoms,
                                                                                                self.getCurrentRestraint())
                            self.f.append(err)

                        if _angleName in emptyValue and atomSelection != 4:
                            continue

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} className={_class} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         combinationId, None, angleName,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

                    if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                        sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

                    self.atomSelectionSet.clear()

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#talos_restraints_wo_s2.
    def enterTalos_restraints_wo_s2(self, ctx: DynamoMRParser.Talos_restraints_wo_s2Context):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        self.closeSequence()

    # Exit a parse tree produced by DynamoMRParser#talos_restraints_wo_s2.
    def exitTalos_restraints_wo_s2(self, ctx: DynamoMRParser.Talos_restraints_wo_s2Context):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by DynamoMRParser#talos_restraint_wo_s2.
    def enterTalos_restraint_wo_s2(self, ctx: DynamoMRParser.Talos_restraint_wo_s2Context):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by DynamoMRParser#talos_restraint_wo_s2.
    def exitTalos_restraint_wo_s2(self, ctx: DynamoMRParser.Talos_restraint_wo_s2Context):

        try:

            seqId = int(str(ctx.Integer(0)))
            compId = str(ctx.Simple_name(0)).upper()

            if compId not in monDict3.values() and compId not in monDict3:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Found unknown residue name {compId!r}.")
                return

            if len(compId) >= 3:
                pass
            else:
                compId = next(k for k, v in monDict3.items() if v == compId and len(k) == 3)

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            # phi
            phi_target_value = self.numberSelection[0]
            psi_target_value = self.numberSelection[1]

            delta_phi_value = self.numberSelection[2]
            delta_psi_value = self.numberSelection[3]

            # dist = self.numberSelection[4]

            # count = int(str(ctx.Integer(1)))

            _class = str(ctx.Simple_name(1))

            if _class not in TALOS_PREDICTION_CLASSES:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The class name {_class!r} should be one of {TALOS_PREDICTION_CLASSES}.")
                return

            if _class not in TALOS_PREDICTION_MIN_CLASSES:  # ignore suspicious predictions
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            for angleName in ('PHI', 'PSI'):
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                if angleName == 'PHI':
                    target_value = phi_target_value
                    if delta_phi_value > 0.0:
                        lower_limit = phi_target_value - delta_phi_value
                        upper_limit = phi_target_value + delta_phi_value
                    else:
                        lower_limit = upper_limit = None
                else:
                    target_value = psi_target_value
                    if delta_psi_value > 0.0:
                        lower_limit = psi_target_value - delta_psi_value
                        upper_limit = psi_target_value + delta_psi_value
                    else:
                        lower_limit = upper_limit = None

                dstFunc = self.validateAngleRangeWithIndex(None, 1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                    if atomId is None:
                        resKey = (seqId, compId)
                        if resKey not in self.extResKey:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{seqId}:{compId} is not present in the coordinates.")
                        return

                self.retrieveLocalSeqScheme()

                chainAssign, _ = self.assignCoordPolymerSequenceWithIndex(None, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)]
                                                                    if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None and offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            idx = ps['auth_seq_id'].index(cifSeqId)
                            try:
                                _cifSeqId = ps['auth_seq_id'][idx + offset]
                                _cifCompId = ps['comp_id'][idx + offset]
                            except IndexError:
                                pass

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None and not self.allow_ext_seq:
                                self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                              f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                              f"of chain {chainId} of the coordinates. "
                                              "Please update the sequence in the Macromolecules page.")
                                return
                                # _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList
                                              if cca[self.ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
                    except IndexError:
                        self.areUniqueCoordAtoms('a torsion angle (TALOS)')
                        return

                    len_f = len(self.f)
                    self.areUniqueCoordAtoms('a torsion angle (TALOS)',
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
                            _angleName = getTypeOfDihedralRestraint(True, False, False,
                                                                    atoms,
                                                                    'plane_like' in dstFunc)

                            if _angleName is not None and _angleName.startswith('pseudo'):
                                _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                    atoms,
                                                                                                    self.getCurrentRestraint())
                                self.f.append(err)

                            if _angleName in emptyValue and atomSelTotal != 4:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSfWithSoftware(constraintType='backbone chemical shifts',
                                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                                    softwareName='TALOS')
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        atoms = [atom1, atom2, atom3, atom4]
                        if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(True, False, False,
                                                                atoms,
                                                                'plane_like' in dstFunc)

                        if _angleName is not None and _angleName.startswith('pseudo'):
                            _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                atoms,
                                                                                                self.getCurrentRestraint())
                            self.f.append(err)

                        if _angleName in emptyValue and atomSelTotal != 4:
                            continue

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} className={_class} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         combinationId, None, angleName,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

                    if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                        sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

                    self.atomSelectionSet.clear()

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by DynamoMRParser#number.
    def enterNumber(self, ctx: DynamoMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by DynamoMRParser#number.
    def exitNumber(self, ctx: DynamoMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Float_DecimalComma():
            self.numberSelection.append(float(str(ctx.Float_DecimalComma()).replace(',', '.', 1)))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

# del DynamoMRParser
