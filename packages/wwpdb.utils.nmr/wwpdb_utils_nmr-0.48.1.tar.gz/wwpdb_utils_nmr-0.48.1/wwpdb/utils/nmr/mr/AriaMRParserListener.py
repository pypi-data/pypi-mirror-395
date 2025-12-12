##
# File: AriaMRParserListener.py
# Date: 16-Jan-2024
#
# Updates:
""" ParserLister class for ARIA MR files.
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
    from wwpdb.utils.nmr.mr.AriaMRParser import AriaMRParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getRow,
                                                       getStarAtom,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.AriaMRParser import AriaMRParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getRow,
                                           getStarAtom,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getPotentialType,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP)
    from nmr.nef.NEFTranslator import NEFTranslator


# This class defines a complete listener for a parse tree produced by AriaMRParser.
class AriaMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ()

    # current contributions
    __cur_contrib = []

    # current combination
    __cur_comb_id = None

    # current atom pair
    __cur_atom_pair = []

    # collection of number selection in contributions
    __numberCSelection = []

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

        self.file_type = 'nm-res-ari'
        self.software_name = 'ARIA'

    # Enter a parse tree produced by AriaMRParser#aria_mr.
    def enterAria_mr(self, ctx: AriaMRParser.Aria_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AriaMRParser#aria_mr.
    def exitAria_mr(self, ctx: AriaMRParser.Aria_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by AriaMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: AriaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by AriaMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: AriaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: AriaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.__cur_comb_id = 0
        self.__cur_contrib.clear()
        self.atomSelectionSet.clear()

    # Exit a parse tree produced by AriaMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: AriaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            # ref_spec = str(ctx.RefSpecName()).rstrip(',')
            # ref_peak = int(str(ctx.Integer(0)).rstrip(','))
            # id = int(str(ctx.Integer(1)).rstrip(','))
            # dist = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # u_viol = self.numberSelection[2]
            # p_viol = self.numberSelection[3]
            # viol = str(ctx.ViolFlag()).rstrip(',') in trueValue
            # reliable = str(ctx.ReliableFlag()).rstrip(',') in trueValue
            # a_type = str(ctx.ATypeFlag())[0]

            if len(self.__cur_contrib) == 0:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            total = 0
            weights = []

            for contlib in self.__cur_contrib:

                atom_pair = contlib['atom_pair']
                weight = contlib['weight']

                if weight <= 0.0:
                    continue

                chainId1 = atom_pair[0]['chain_id'] if 'chain_id' in atom_pair[0] else None
                seqId1 = atom_pair[0]['seq_id']
                compId1 = atom_pair[0]['comp_id']
                atomId1 = atom_pair[0]['atom_id']

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])\
                    if chainId1 is not None else self.assignCoordPolymerSequence(seqId1, compId1, atomId1.split('|', 1)[0])

                chainId2 = atom_pair[1]['chain_id'] if 'chain_id' in atom_pair[1] else None
                seqId2 = atom_pair[1]['seq_id']
                compId2 = atom_pair[1]['comp_id']
                atomId2 = atom_pair[1]['atom_id']

                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])\
                    if chainId2 is not None else self.assignCoordPolymerSequence(seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    continue

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < (total + 1) * 2:
                    continue

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

                dstFunc = self.validateDistanceRange(weight, None, None, upper_limit, None, self.omitDistLimitOutlier)

                if dstFunc is None:
                    return

                total += 1
                weights.append(weight)

            if total == 0:
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                sf['id'] += 1
                if self.__cur_comb_id > 1:
                    combinationId = 0
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0

            for i in range(0, total * 2, 2):
                if isinstance(combinationId, int):
                    combinationId += 1
                if isinstance(memberId, int):
                    memberId = 0
                    _atom1 = _atom2 = None
                if self.createSfDict:
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[i]) * len(self.atomSelectionSet[i + 1]) > 1 else '.'
                dstFunc['weight'] = weights[i // 2]
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints} "
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
                                     atom1, atom2, asis1=asis1, asis2=asis2)
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

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by AriaMRParser#contribution.
    def enterContribution(self, ctx: AriaMRParser.ContributionContext):
        pass

    # Exit a parse tree produced by AriaMRParser#contribution.
    def exitContribution(self, ctx: AriaMRParser.ContributionContext):  # pylint: disable=unused-argument

        try:

            len_num_c_sel = len(self.__numberCSelection)

            if len_num_c_sel == 0:
                pass

            elif len_num_c_sel != 3:
                return

            elif self.__numberCSelection[2] is not None:
                # dist = self.__numberCSelection[0]
                # dist_err = self.__numberCSelection[1]
                self.cur_weight = self.__numberCSelection[2]
                self.__cur_comb_id += 1

            if len(self.__cur_atom_pair) != 2:
                return

            self.__cur_contrib.append({'atom_pair': copy.copy(self.__cur_atom_pair),
                                       'weight': self.cur_weight,
                                       'combination_id': self.__cur_comb_id})

        finally:
            self.__numberCSelection.clear()

    # Enter a parse tree produced by AriaMRParser#atom_pair.
    def enterAtom_pair(self, ctx: AriaMRParser.Atom_pairContext):  # pylint: disable=unused-argument
        self.__cur_atom_pair.clear()

    # Exit a parse tree produced by AriaMRParser#atom_pair.
    def exitAtom_pair(self, ctx: AriaMRParser.Atom_pairContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#atom_selection.
    def enterAtom_selection(self, ctx: AriaMRParser.Atom_selectionContext):

        try:

            atom_sel = {'atom_id': str(ctx.Simple_name(1)).upper()}

            res_name = str(ctx.Simple_name(0)).upper()

            if len(res_name) > 1 and not res_name[0].isdigit() and res_name[-1].isdigit():
                col = len(res_name) - 1
                while res_name[col - 1].isdigit():
                    col -= 1
                atom_sel['seq_id'] = int(res_name[col:])
                atom_sel['comp_id'] = res_name[:col]

            if ctx.Simple_name(2):
                atom_sel['chain_id'] = str(ctx.Simple_name(2))

        finally:
            self.__cur_atom_pair.append(atom_sel)

    # Exit a parse tree produced by AriaMRParser#atom_selection.
    def exitAtom_selection(self, ctx: AriaMRParser.Atom_selectionContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#old_distance_restraints.
    def enterOld_distance_restraints(self, ctx: AriaMRParser.Old_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by AriaMRParser#old_distance_restraints.
    def exitOld_distance_restraints(self, ctx: AriaMRParser.Old_distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#old_distance_restraint.
    def enterOld_distance_restraint(self, ctx: AriaMRParser.Old_distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.__cur_comb_id = 0
        self.__cur_contrib.clear()
        self.atomSelectionSet.clear()

    # Exit a parse tree produced by AriaMRParser#old_distance_restraint.
    def exitOld_distance_restraint(self, ctx: AriaMRParser.Old_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            if len(self.__cur_contrib) == 0:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            total = 0
            weights = []

            for contlib in self.__cur_contrib:

                atom_pair = contlib['atom_pair']
                weight = contlib['weight']

                if weight <= 0.0:
                    continue

                chainId1 = atom_pair[0]['chain_id'] if 'chain_id' in atom_pair[0] else None
                seqId1 = atom_pair[0]['seq_id']
                compId1 = atom_pair[0]['comp_id']
                atomId1 = atom_pair[0]['atom_id']

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])\
                    if chainId1 is not None else self.assignCoordPolymerSequence(seqId1, compId1, atomId1.split('|', 1)[0])

                chainId2 = atom_pair[1]['chain_id'] if 'chain_id' in atom_pair[1] else None
                seqId2 = atom_pair[1]['seq_id']
                compId2 = atom_pair[1]['comp_id']
                atomId2 = atom_pair[1]['atom_id']

                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])\
                    if chainId2 is not None else self.assignCoordPolymerSequence(seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    continue

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < (total + 1) * 2:
                    continue

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

                dstFunc = self.validateDistanceRange(weight, None, self.cur_lower_limit, self.cur_upper_limit, None, self.omitDistLimitOutlier)

                if dstFunc is None:
                    return

                total += 1
                weights.append(weight)

            if total == 0:
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                sf['id'] += 1
                if self.__cur_comb_id > 1:
                    combinationId = 0
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0

            for i in range(0, total * 2, 2):
                if isinstance(combinationId, int):
                    combinationId += 1
                if isinstance(memberId, int):
                    memberId = 0
                    _atom1 = _atom2 = None
                if self.createSfDict:
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[i]) * len(self.atomSelectionSet[i + 1]) > 1 else '.'
                dstFunc['weight'] = weights[i // 2]
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints} "
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
                                     atom1, atom2, asis1=asis1, asis2=asis2)
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

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by AriaMRParser#p_row.
    def enterP_row(self, ctx: AriaMRParser.P_rowContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AriaMRParser#p_row.
    def exitP_row(self, ctx: AriaMRParser.P_rowContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#a_row.
    def enterA_row(self, ctx: AriaMRParser.A_rowContext):
        self.cur_lower_limit = float(str(ctx.Float(2))) if ctx.Float(2) else -1.0
        self.cur_upper_limit = float(str(ctx.Float(3))) if ctx.Float(3) else -1.0

    # Exit a parse tree produced by AriaMRParser#a_row.
    def exitA_row(self, ctx: AriaMRParser.A_rowContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by AriaMRParser#c_row.
    def enterC_row(self, ctx: AriaMRParser.C_rowContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AriaMRParser#c_row.
    def exitC_row(self, ctx: AriaMRParser.C_rowContext):
        self.__cur_comb_id += 1

        atom_pair = [{'atom_id': str(ctx.Simple_name(2)).upper(),
                      'seq_id': int(str(ctx.Integer(0))),
                      'comp_id': str(ctx.Simple_name(0)).upper()},
                     {'atom_id': str(ctx.Simple_name(5)).upper(),
                      'seq_id': int(str(ctx.Integer(1))),
                      'comp_id': str(ctx.Simple_name(3)).upper()}]

        weight = float(str(ctx.Float(1))) if ctx.Float(1) else -1.0

        self.__cur_contrib.append({'atom_pair': copy.copy(atom_pair),
                                   'weight': weight,
                                   'combination_id': self.__cur_comb_id})

    # Enter a parse tree produced by AriaMRParser#number.
    def enterNumber(self, ctx: AriaMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AriaMRParser#number.
    def exitNumber(self, ctx: AriaMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float()).rstrip(',')))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer()).rstrip(',')))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by AriaMRParser#number_c.
    def enterNumber_c(self, ctx: AriaMRParser.Number_cContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by AriaMRParser#number_c.
    def exitNumber_c(self, ctx: AriaMRParser.Number_cContext):
        if ctx.Float():
            self.__numberCSelection.append(float(str(ctx.Float()).rstrip(',')))

        elif ctx.Integer():
            self.__numberCSelection.append(float(str(ctx.Integer()).rstrip(',')))

        else:
            self.__numberCSelection.append(None)

# del AriaMRParser
