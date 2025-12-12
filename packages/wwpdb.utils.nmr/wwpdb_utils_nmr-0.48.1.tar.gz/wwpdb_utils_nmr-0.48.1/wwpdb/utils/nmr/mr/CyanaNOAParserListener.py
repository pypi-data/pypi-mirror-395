##
# File: CyanaNOAParserListener.py
# Date: 21-Nov-2024
#
# Updates:
""" ParserLister class for CYANA NOA files.
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
    from wwpdb.utils.nmr.mr.CyanaNOAParser import CyanaNOAParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                                       hasIntraChainRestraint,
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
    from wwpdb.utils.nmr.AlignUtil import deepcopy
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.CyanaNOAParser import CyanaNOAParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                           hasIntraChainRestraint,
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
    from nmr.AlignUtil import deepcopy


# This class defines a complete listener for a parse tree produced by CyanaNOAParser.
class CyanaNOAParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ('noeAssignments',
                 'asisList',
                 'weights',
                 'dstFunc')

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

        self.file_type = 'nm-res-noa'
        self.software_name = 'CYANA'

        self.noeAssignments = []
        self.asisList = []
        self.weights = []

        # potential
        self.dstFunc = None

    # Enter a parse tree produced by CyanaNOAParser#cyana_noa.
    def enterCyana_noa(self, ctx: CyanaNOAParser.Cyana_noaContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#cyana_noa.
    def exitCyana_noa(self, ctx: CyanaNOAParser.Cyana_noaContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by CyanaNOAParser#comment.
    def enterComment(self, ctx: CyanaNOAParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#comment.
    def exitComment(self, ctx: CyanaNOAParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#noe_peaks.
    def enterNoe_peaks(self, ctx: CyanaNOAParser.Noe_peaksContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by CyanaNOAParser#noe_peaks.
    def exitNoe_peaks(self, ctx: CyanaNOAParser.Noe_peaksContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#peak_header.
    def enterPeak_header(self, ctx: CyanaNOAParser.Peak_headerContext):
        if ctx.Angstrome(0):
            self.dstFunc = self.validateDistanceRange(1.0, None, None, float(str(ctx.Angstrome(0))[:-2]),
                                                      None, self.omitDistLimitOutlier)
        else:
            self.dstFunc = None

    # Exit a parse tree produced by CyanaNOAParser#peak_header.
    def exitPeak_header(self, ctx: CyanaNOAParser.Peak_headerContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#peak_quality.
    def enterPeak_quality(self, ctx: CyanaNOAParser.Peak_qualityContext):
        if ctx.Float() and self.dstFunc is not None:
            quality = float(str(ctx.Float()))

            if 0.0 < quality <= 1.0:

                if quality < 1.0:
                    self.dstFunc['weight'] = quality

                self.distRestraints += 1

                self.noeAssignments.clear()
                self.asisList.clear()
                self.weights.clear()

    # Exit a parse tree produced by CyanaNOAParser#peak_quality.
    def exitPeak_quality(self, ctx: CyanaNOAParser.Peak_qualityContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#noe_assignments.
    def enterNoe_assignments(self, ctx: CyanaNOAParser.Noe_assignmentsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#noe_assignments.
    def exitNoe_assignments(self, ctx: CyanaNOAParser.Noe_assignmentsContext):  # pylint: disable=unused-argument

        if len(self.noeAssignments) > 0 and self.dstFunc is not None:

            try:

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.noeAssignments[0], self.dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, self.dstFunc))
                    sf['id'] += 1

                for idx, atomSelectionSet in enumerate(self.noeAssignments):
                    self.dstFunc['weight'] = self.weights[idx]
                    memberLogicCode = 'OR' if len(atomSelectionSet[0]) * len(atomSelectionSet[1]) > 1 else '.'
                    has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(atomSelectionSet)

                    if self.createSfDict:
                        if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                            memberLogicCode = '.'
                        memberId = '.'
                        if len(self.noeAssignments) > 1:
                            memberId = idx + 1
                            _atom1 = _atom2 = None
                        elif memberLogicCode == 'OR':
                            if len(atomSelectionSet[0]) * len(atomSelectionSet[1]) > 1\
                               and (isAmbigAtomSelection(atomSelectionSet[0], self.csStat)
                                    or isAmbigAtomSelection(atomSelectionSet[1], self.csStat)):
                                memberId = 0
                                _atom1 = _atom2 = None

                    for atom1, atom2 in itertools.product(atomSelectionSet[0],
                                                          atomSelectionSet[1]):
                        atoms = [atom1, atom2]
                        if isIdenticalRestraint(atoms, self.nefT):
                            continue
                        if self.createSfDict and isinstance(memberId, int):  # pylint: disable=used-before-assignment
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
                                                                       self.dstFunc)
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.distRestraints} "
                                  f"atom1={atom1} atom2={atom2} {self.dstFunc}")
                        if self.createSfDict and sf is not None:
                            if isinstance(memberId, int):
                                if _atom1 is None or isAmbigAtomSelection([_atom1, atom1], self.csStat)\
                                   or isAmbigAtomSelection([_atom2, atom2], self.csStat):
                                    if memberId != idx + 1:
                                        memberId += 1
                                    _atom1, _atom2 = atom1, atom2
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', memberId, memberLogicCode,
                                         sf['list_id'], self.entryId, self.dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         atom1, atom2, asis1=self.asisList[idx][0], asis2=self.asisList[idx][1])
                            sf['loop'].add_data(row)

                            if sf['constraint_subsubtype'] == 'ambi':
                                continue

                            if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                                sf['constraint_subsubtype'] = 'ambi'

                            if memberLogicCode == 'OR'\
                               and (isAmbigAtomSelection(atomSelectionSet[0], self.csStat)
                                    or isAmbigAtomSelection(atomSelectionSet[1], self.csStat)):
                                sf['constraint_subsubtype'] = 'ambi'

                            if 'upper_limit' in self.dstFunc and self.dstFunc['upper_limit'] is not None:
                                upperLimit = float(self.dstFunc['upper_limit'])
                                if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                                    sf['constraint_subsubtype'] = 'ambi'

                if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                    sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

            finally:
                self.noeAssignments.clear()
                self.asisList.clear()
                self.weights.clear()

    # Enter a parse tree produced by CyanaNOAParser#noe_assignment.
    def enterNoe_assignment(self, ctx: CyanaNOAParser.Noe_assignmentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#noe_assignment.
    def exitNoe_assignment(self, ctx: CyanaNOAParser.Noe_assignmentContext):

        if ctx.Ok():

            try:

                seqId1 = int(str(ctx.Integer(0)))
                compId1 = str(ctx.Simple_name(1)).upper()
                atomId1 = str(ctx.Simple_name(0)).upper()
                seqId2 = int(str(ctx.Integer(1)))
                compId2 = str(ctx.Simple_name(3)).upper()
                atomId2 = str(ctx.Simple_name(2)).upper()

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1.split('|', 1)[0])
                chainAssign2, asis2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                self.noeAssignments.append(deepcopy(self.atomSelectionSet))
                self.asisList.append([asis1, asis2])
                self.weights.append(float(str(ctx.Integer(2))) / 100.0)

            finally:
                self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaNOAParser#numerical_report.
    def enterNumerical_report(self, ctx: CyanaNOAParser.Numerical_reportContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#numerical_report.
    def exitNumerical_report(self, ctx: CyanaNOAParser.Numerical_reportContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#extended_report.
    def enterExtended_report(self, ctx: CyanaNOAParser.Extended_reportContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#extended_report.
    def exitExtended_report(self, ctx: CyanaNOAParser.Extended_reportContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#noe_stat.
    def enterNoe_stat(self, ctx: CyanaNOAParser.Noe_statContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#noe_stat.
    def exitNoe_stat(self, ctx: CyanaNOAParser.Noe_statContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#list_of_proton.
    def enterList_of_proton(self, ctx: CyanaNOAParser.List_of_protonContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#list_of_proton.
    def exitList_of_proton(self, ctx: CyanaNOAParser.List_of_protonContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaNOAParser#peak_stat.
    def enterPeak_stat(self, ctx: CyanaNOAParser.Peak_statContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaNOAParser#peak_stat.
    def exitPeak_stat(self, ctx: CyanaNOAParser.Peak_statContext):  # pylint: disable=unused-argument
        pass

# del CyanaNOAParser
