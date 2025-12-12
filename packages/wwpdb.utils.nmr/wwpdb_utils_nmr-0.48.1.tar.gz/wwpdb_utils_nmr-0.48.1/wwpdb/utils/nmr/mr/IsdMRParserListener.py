##
# File: IsdMRParserListener.py
# Date: 13-Sep-2022
#
# Updates:
""" ParserLister class for ISD MR files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import re
import copy
import itertools

from antlr4 import ParseTreeListener
from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.IsdMRParser import IsdMRParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                                       hasIntraChainRestraint,
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
    from nmr.mr.IsdMRParser import IsdMRParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (isIdenticalRestraint,
                                           hasIntraChainRestraint,
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


# This class defines a complete listener for a parse tree produced by IsdMRParser.
class IsdMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ()

    __atom_sel_pat = re.compile(r'([A-Z][0-9A-Z]{2})(\d+)([A-Z][0-9A-Z]*)')

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

        self.file_type = 'nm-res-isd'
        self.software_name = 'ISD'

    # Enter a parse tree produced by IsdMRParser#biosym_mr.
    def enterIsd_mr(self, ctx: IsdMRParser.Isd_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by IsdMRParser#biosym_mr.
    def exitIsd_mr(self, ctx: IsdMRParser.Isd_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by IsdMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: IsdMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

        if ctx.Distance():
            self.distRestraints += 1

            self.cur_upper_limit = float(str(ctx.Distance()).split('=')[1])

    # Exit a parse tree produced by IsdMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: IsdMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by IsdMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: IsdMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()

    # Exit a parse tree produced by IsdMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: IsdMRParser.Distance_restraintContext):
        seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
        seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))

        if atomId1 is None or atomId2 is None:  # syntax error
            return

        target_value = None
        lower_limit = None
        upper_limit = self.cur_upper_limit

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

        dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit, None, self.omitDistLimitOutlier)

        if dstFunc is None:
            return

        if self.createSfDict:
            sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                 self.csStat, self.originalFileName),
                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
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

    def __splitAtomSelectionExpr(self, atomSelection: str) -> Tuple[Optional[int], Optional[str], Optional[str]]:  # pylint: disable=no-self-use
        """ Split ISD atom selection expression.
        """

        try:

            g = self.__atom_sel_pat.search(atomSelection.upper()).groups()

            return int(g[1]), g[0], g[2]

        except (ValueError, AttributeError):
            return None, None, None

# del IsdMRParser
