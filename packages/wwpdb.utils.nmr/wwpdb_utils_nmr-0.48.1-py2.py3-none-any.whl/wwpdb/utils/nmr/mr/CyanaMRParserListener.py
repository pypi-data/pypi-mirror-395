##
# File: CyanaMRParserListener.py
# Date: 03-Oct-2025
#
# Updates:
""" ParserLister class for CYANA MR files.
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

from antlr4 import ParseTreeListener
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.CyanaMRParser import CyanaMRParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import (BaseLinearMRParserListener,
                                                               DIST_RANGE_MIN,
                                                               DIST_RANGE_MAX,
                                                               DIST_ERROR_MAX)
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (translateToStdResName,
                                                       translateToStdAtomName,
                                                       getRdcCode,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       hasIntraChainRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       getStructConnPtnrAtom,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       getRow,
                                                       getStarAtom,
                                                       resetCombinationId,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       getDstFuncForHBond,
                                                       getDstFuncForSsBond,
                                                       ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       KNOWN_ANGLE_NAMES,
                                                       KNOWN_ANGLE_ATOM_NAMES,
                                                       KNOWN_ANGLE_SEQ_OFFSET,
                                                       KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                                       KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                                       CARTN_DATA_ITEMS)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           emptyValue,
                                           protonBeginCode,
                                           rdcBbPairCode)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.CyanaMRParser import CyanaMRParser
    from nmr.mr.BaseLinearMRParserListener import (BaseLinearMRParserListener,
                                                   DIST_RANGE_MIN,
                                                   DIST_RANGE_MAX,
                                                   DIST_ERROR_MAX)
    from nmr.mr.ParserListenerUtil import (translateToStdResName,
                                           translateToStdAtomName,
                                           getRdcCode,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           hasIntraChainRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           getStructConnPtnrAtom,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRow,
                                           getStarAtom,
                                           resetCombinationId,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getPotentialType,
                                           getDstFuncForHBond,
                                           getDstFuncForSsBond,
                                           ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           KNOWN_ANGLE_NAMES,
                                           KNOWN_ANGLE_ATOM_NAMES,
                                           KNOWN_ANGLE_SEQ_OFFSET,
                                           KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                           KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                           CARTN_DATA_ITEMS)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               emptyValue,
                               protonBeginCode,
                               rdcBbPairCode)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance)


# This class defines a complete listener for a parse tree produced by CyanaMRParser.
class CyanaMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ('col_order_of_dist_w_chain', )

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None,
                 reasons: Optional[dict] = None, upl_or_lol: Optional[str] = None, file_ext: Optional[str] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        super().__init__(verbose, log, representativeModelId, representativeAltId, mrAtomNameMapping,
                         cR, caC, nefT, reasons, upl_or_lol, file_ext)

        self.file_type = 'nm-res-cya'
        self.software_name = 'CYANA'

        self.col_order_of_dist_w_chain = {}

    # Enter a parse tree produced by CyanaMRParser#cyana_mr.
    def enterCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#cyana_mr.
    def exitCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by CyanaMRParser#comment.
    def enterComment(self, ctx: CyanaMRParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#comment.
    def exitComment(self, ctx: CyanaMRParser.CommentContext):
        if self.cur_comment_inlined:
            return

        def is_eff_ext(txt, ext):
            if ext not in txt:
                return False
            idx = txt.index(ext)
            if idx == 0:
                return True
            len_ext = len(ext)
            if idx + len_ext == len(txt):
                return True
            return not txt[idx - 1].isalpha() and not txt[idx + len_ext].isalpha()

        for col in range(20):
            if ctx.Any_name(col):
                text = str(ctx.Any_name(col)).lower()
                if 'coupling' in text:
                    self.cur_dist_type = 'cco'
                    break
                if is_eff_ext(text, 'cco'):  # 'according' is not cco (6wa5)
                    self.cur_dist_type = 'cco'
                    break
                if not ('lol' in text or 'lower' in text):
                    if 'upper' in text:
                        if self.file_ext != 'lol':
                            self.cur_dist_type = 'upl'
                            break
                    if is_eff_ext(text, 'upl') and self.file_ext != 'lol':
                        self.cur_dist_type = 'upl'
                        break
                if not ('upl' in text or 'upper' in text):
                    if 'lower' in text:
                        if self.file_ext != 'upl':
                            self.cur_dist_type = 'lol'
                            break
                    if is_eff_ext(text, 'lol') and self.file_ext != 'upl':
                        self.cur_dist_type = 'lol'
                        break
                if self.cur_dist_type == 'cco' and ('bond' in text or 'distance' in text):
                    self.cur_dist_type = ''
            else:
                break

    # Enter a parse tree produced by CyanaMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext != 'cco' else 'jcoup'
        if (self.file_ext is not None and self.file_ext in ('upv', 'lov')) or (self.reasons is not None and 'noepk' in self.reasons):
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.cur_subtype == 'jcoup':
            self.jcoupRestraints += 1
        elif self.cur_subtype == 'noepk':
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument

        if self.cur_subtype in ('dist', 'noepk') and (self.cur_dist_type == 'cco' or len(self.numberSelection) == 6):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.cur_subtype == 'noepk':
                self.noepkRestraints -= 1
            self.cur_subtype = 'jcoup'
            self.jcoupRestraints += 1

        try:

            if None in self.genAtomNameSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                elif self.cur_subtype == 'noepk':
                    self.noepkRestraints -= 1
                return

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genAtomNameSelection[0].upper()
            seqId2, chainId2 = self.genResNumSelection[1]
            compId2 = self.genSimpleNameSelection[1].upper()
            atomId2 = self.genAtomNameSelection[1].upper()

            if len(compId1) == 1 and len(compId2) == 1 and compId1.isalpha() and compId2.isalpha():
                atom_like = self.csStat.getAtomLikeNameSet(True, True, 1)
                if atomId1 in atom_like and atomId2 in atom_like:
                    one_letter_na = False
                    if self.hasPolySeq\
                       and (compId1 in ('A', 'C', 'G', 'I', 'T', 'U') or compId2 in ('A', 'C', 'G', 'I', 'T', 'U')):
                        chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0], False)
                        for cifChainId, cifSeqId, cifCompId, isPolySeq in chainAssign1:
                            if isPolySeq:
                                seqKey = (cifChainId, cifSeqId, cifCompId)
                                if seqKey in self.authToEntityType and 'ribonucleotide' in self.authToEntityType[seqKey]:
                                    one_letter_na = True
                                    break
                        chainAssign2, _ = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0], False)
                        for cifChainId, cifSeqId, cifCompId, isPolySeq in chainAssign2:
                            if isPolySeq:
                                seqKey = (cifChainId, cifSeqId, cifCompId)
                                if seqKey in self.authToEntityType and 'ribonucleotide' in self.authToEntityType[seqKey]:
                                    one_letter_na = True
                                    break
                    if not one_letter_na:
                        self.exitDistance_wo_comp_restraint(compId1, seqId1, atomId1, compId2, seqId2, atomId2)
                        return

            target_value = None
            lower_limit = None
            upper_limit = None
            target_value_uncertainty = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                elif self.cur_subtype == 'noepk':
                    self.noepkRestraints -= 1
                return

            if self.cur_subtype == 'jcoup' and self.hasPolySeq:

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                if len(chainAssign1) > 0 and len(chainAssign2) > 0:

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) >= 2:

                        if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                            isCco = True

                            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                                isCco = False

                            if chain_id_1 != chain_id_2:
                                isCco = False

                            if abs(seq_id_1 - seq_id_2) > 1:
                                isCco = False

                            if not isCco:
                                self.jcoupRestraints -= 1
                                self.cur_subtype = 'dist'
                                self.cur_dist_type = ''
                                self.distRestraints += 1

            if self.cur_subtype in ('dist', 'noepk'):

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.cur_subtype_altered and self.cur_subtype == 'dist':
                    self.max_dist_value = max(self.max_dist_value, value)
                    self.min_dist_value = min(self.min_dist_value, value)

                if has_square:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        upper_limit = value2
                        lower_limit = value

                    elif value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif (0.0 if self.file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta

                    else:
                        if self.applyPdbStatCap:
                            target_value = value
                            if delta > 0.0:
                                lower_limit = value - delta
                                upper_limit = value + delta
                        else:
                            if value > 1.8:
                                upper_limit = value
                            else:
                                lower_limit = value
                            if value2 > 0.0:
                                target_value_uncertainty = value2

                elif 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                    upper_limit = value

                elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                    lower_limit = value

                elif self.cur_subtype == 'noepk':
                    target_value = value

                elif self.upl_or_lol is None:
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_only':
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                    self.local_dist_types.append(self.cur_dist_type)

                if not self.hasPolySeq and not self.hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if atom_id_1[0] not in ('H', 'C', 'N') or atom_id_2[0] not in ('H', 'C', 'N')\
                       or atom_id_1[0] == atom_id_2[0] == 'H':
                        isRdc = False

                    elif chain_id_1 != chain_id_2:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) == 1:

                        if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            pass
                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        bbAtoms = self.csStat.getBackBoneAtoms(comp_id_1, excl_minor_atom=True)
                        if atom_id_1 not in bbAtoms or atom_id_2 not in bbAtoms:
                            isRdc = False

                        elif not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                            if (atom_id_1[0] == 'H' and atom_id_2[0] != 'H')\
                               or (atom_id_1[0] != 'H' and atom_id_2[0] == 'H'):
                                isRdc = False
                            elif comp_id_1 in monDict3\
                                    and self.nefT.validate_comp_atom(comp_id_1, atom_id_1)\
                                    and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                pass
                            else:
                                isRdc = False

                    else:
                        isRdc = False

                    if not isRdc:
                        self.cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.cur_subtype_altered = True
                            self.cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            if self.cur_subtype == 'dist':
                                self.distRestraints -= 1
                            elif self.cur_subtype == 'noepk':
                                self.noepkRestraints -= 1
                            self.cur_subtype = 'rdc'
                            self.rdcRestraints += 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.createSfDict:
                                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                                rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                                orientationId=self.cur_rdc_orientation)
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                atoms = [atom1, atom2]
                                if isIdenticalRestraint(atoms, self.nefT):
                                    continue
                                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                                    continue
                                if self.debug:
                                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None, None,
                                                 sf['list_id'], self.entryId, dstFunc,
                                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                                 atom1, atom2, asis1=asis1, asis2=asis2)
                                    sf['loop'].add_data(row)

                            self.cur_subtype = 'dist'

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

                if self.cur_subtype == 'noepk':
                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)
                else:
                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         self.omitDistLimitOutlier)

                if self.cur_subtype == 'dist' and dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                    self.reasonsForReParsing['noepk'] = True

                if dstFunc is None:
                    return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                        # print(f"constraint_type={getDistConstraintType(self.atomSelectionSet, dstFunc, self.csStat, self.originalFileName)}")
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

                        if self.cur_subtype == 'noepk':
                            break

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

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                  f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-chain scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 in ('H', 'N'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('H', 'N') and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}
                             or (seq_id_1 < seq_id_2 and atom_id_2 == 'P')):
                        pass

                    else:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found zero scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if self.createSfDict:
                    sf = self.getSf()
                    sf['id'] += 1

                for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    self.ccU.updateChemCompDict(atom1['comp_id'])
                    atom2_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                    atom3_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                    atom_id_2 = atom_id_3 = None
                    for ccb in self.ccU.lastBonds:
                        if ccb[self.ccU.ccbAtomId1] in atom2_can and ccb[self.ccU.ccbAtomId2] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId1]
                            atom_id_3 = ccb[self.ccU.ccbAtomId2]
                            break
                        if ccb[self.ccU.ccbAtomId2] in atom2_can and ccb[self.ccU.ccbAtomId1] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId2]
                            atom_id_3 = ccb[self.ccU.ccbAtomId1]
                            break
                    if None in (atom_id_2, atom_id_3):
                        continue
                    atom2 = copy.copy(atom1)
                    atom2['atom_id'] = atom_id_2
                    atom3 = copy.copy(atom4)
                    atom3['atom_id'] = atom_id_3
                    if self.debug:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4,
                                     asis1=asis1, asis2=asis1, asis3=asis2, asis4=asis2)
                        sf['loop'].add_data(row)

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
            elif self.cur_subtype == 'noepk':
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()
            self.genAtomNameSelection.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_wo_comp_restraint(self, chainId1: str, seqId1: int, atomId1: str,
                                       chainId2: str, seqId2: int, atomId2: str):

        try:

            target_value = None
            lower_limit = None
            upper_limit = None
            target_value_uncertainty = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                elif self.cur_subtype == 'noepk':
                    self.noepkRestraints -= 1
                return

            if self.cur_subtype == 'jcoup' and self.hasPolySeq:

                self.retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if len(chainAssign1) > 0 and len(chainAssign2) > 0:

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                    if len(self.atomSelectionSet) >= 2:

                        if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                            isCco = True

                            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                                isCco = False

                            if chain_id_1 != chain_id_2:
                                isCco = False

                            if abs(seq_id_1 - seq_id_2) > 1:
                                isCco = False

                            if not isCco:
                                self.jcoupRestraints -= 1
                                self.cur_subtype = 'dist'
                                self.cur_dist_type = ''
                                self.distRestraints += 1

            if self.cur_subtype in ('dist', 'noepk'):

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.cur_subtype_altered and self.cur_subtype == 'dist':
                    self.max_dist_value = max(self.max_dist_value, value)
                    self.min_dist_value = min(self.min_dist_value, value)

                if has_square:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        upper_limit = value2
                        lower_limit = value

                    elif value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif (0.0 if self.file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta

                    else:
                        if self.applyPdbStatCap:
                            target_value = value
                            if delta > 0.0:
                                lower_limit = value - delta
                                upper_limit = value + delta
                        else:
                            upper_limit = value
                            if value2 > 0.0:
                                target_value_uncertainty = value2

                elif 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                    upper_limit = value

                elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                    lower_limit = value

                elif self.cur_subtype == 'noepk':
                    target_value = value

                elif self.upl_or_lol is None:
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_only':
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                    self.local_dist_types.append(self.cur_dist_type)

                if not self.hasPolySeq and not self.hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1.split('|', 1)[0])
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if atom_id_1[0] not in ('H', 'C', 'N') or atom_id_2[0] not in ('H', 'C', 'N')\
                       or atom_id_1[0] == atom_id_2[0] == 'H':
                        isRdc = False

                    elif chain_id_1 != chain_id_2:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) == 1:

                        if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            pass
                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        bbAtoms = self.csStat.getBackBoneAtoms(comp_id_1, excl_minor_atom=True)
                        if atom_id_1 not in bbAtoms or atom_id_2 not in bbAtoms:
                            isRdc = False

                        elif not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                            if (atom_id_1[0] == 'H' and atom_id_2[0] != 'H')\
                               or (atom_id_1[0] != 'H' and atom_id_2[0] == 'H'):
                                isRdc = False
                            elif comp_id_1 in monDict3\
                                    and self.nefT.validate_comp_atom(comp_id_1, atom_id_1)\
                                    and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                pass
                            else:
                                isRdc = False

                    else:
                        isRdc = False

                    if not isRdc:
                        self.cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.cur_subtype_altered = True
                            self.cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            if self.cur_subtype == 'dist':
                                self.distRestraints -= 1
                            elif self.cur_subtype == 'noepk':
                                self.noepkRestraints -= 1
                            self.cur_subtype = 'rdc'
                            self.rdcRestraints += 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.createSfDict:
                                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                                rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                                orientationId=self.cur_rdc_orientation)
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                atoms = [atom1, atom2]
                                if isIdenticalRestraint(atoms, self.nefT):
                                    continue
                                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                                    continue
                                if self.debug:
                                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None, None,
                                                 sf['list_id'], self.entryId, dstFunc,
                                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                                 atom1, atom2)
                                    sf['loop'].add_data(row)

                            self.cur_subtype = 'dist'

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

                if self.cur_subtype == 'noepk':
                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)
                else:
                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         self.omitDistLimitOutlier)

                if self.cur_subtype == 'dist' and dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                    self.reasonsForReParsing['noepk'] = True

                if dstFunc is None:
                    return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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
                                     atom1, atom2)
                        sf['loop'].add_data(row)

                        if self.cur_subtype == 'noepk':
                            break

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

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                  f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-chain scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 in ('H', 'N'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('H', 'N') and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}
                             or (seq_id_1 < seq_id_2 and atom_id_2 == 'P')):
                        pass

                    else:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found zero scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if self.createSfDict:
                    sf = self.getSf()
                    sf['id'] += 1

                for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    self.ccU.updateChemCompDict(atom1['comp_id'])
                    atom2_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                    atom3_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                    atom_id_2 = atom_id_3 = None
                    for ccb in self.ccU.lastBonds:
                        if ccb[self.ccU.ccbAtomId1] in atom2_can and ccb[self.ccU.ccbAtomId2] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId1]
                            atom_id_3 = ccb[self.ccU.ccbAtomId2]
                            break
                        if ccb[self.ccU.ccbAtomId2] in atom2_can and ccb[self.ccU.ccbAtomId1] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId2]
                            atom_id_3 = ccb[self.ccU.ccbAtomId1]
                            break
                    if None in (atom_id_2, atom_id_3):
                        continue
                    atom2 = copy.copy(atom1)
                    atom2['atom_id'] = atom_id_2
                    atom3 = copy.copy(atom4)
                    atom3['atom_id'] = atom_id_3
                    if self.debug:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        except ValueError:
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
            elif self.cur_subtype == 'noepk':
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def enterTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'
        self.cur_dist_type = ''

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def exitTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def enterTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def exitTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            _compId = self.genSimpleNameSelection[0].upper()
            compId = translateToStdResName(_compId, ccU=self.ccU)
            if _compId != compId:
                _types = self.csStat.getTypeOfCompId(_compId)
                if any(t for t in _types) and _types != self.csStat.getTypeOfCompId(compId):
                    compId = _compId

            if self.cur_subtype_altered:  # invoked from exitCco_restraint()
                seqId, _ = self.genResNumSelection[0]
                chainId = self.genSimpleNameSelection[1]
                angleName = self.genSimpleNameSelection[2].upper()
            else:
                seqId, chainId = self.genResNumSelection[0]
                angleName = self.genSimpleNameSelection[1].upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.remediate and self.reasons is not None and 'dihed_unusual_order' in self.reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")
            """
            if lower_limit > upper_limit:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.")
                if self.remediate:
                    self.dihed_lb_greater_than_ub = True
                return
            """
            if self.remediate and upper_limit < 0.0:
                self.dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                  f"The angle identifier {self.genSimpleNameSelection[1]!r} is unknown for the residue {_compId!r}, "
                                  "of which CYANA residue library should be uploaded.")
                    return

            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign, _ = self.assignCoordPolymerSequence(seqId, compId, 'CA', False)
                if len(chainAssign) > 0:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainAssign[0][0]), None)
                    if ps is not None and 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                            if atomId is None:
                                resKey = (seqId, _compId)
                                if resKey not in self.extResKey:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId}:{_compId} is not present in the coordinates.")
                                return

                self.retrieveLocalSeqScheme()

                if self.cur_subtype_altered:  # invoked from exitCco_restraint()
                    chainAssign, _ = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)
                else:
                    chainAssign, _ = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, _compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = None

                    if carbohydrate:
                        if self.branched is not None:
                            ps = next((ps for ps in self.branched if ps['auth_chain_id'] == chainId), None)
                            if ps is None:
                                ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)
                    else:
                        ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                      f"The angle identifier {self.genSimpleNameSelection[1]!r} is unknown for the residue {_compId!r}, "
                                      "of which CYANA residue library should be uploaded.")
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    prevCifAtomId = None
                    prevOffset = None

                    for ord, (atomId, offset) in enumerate(zip(atomNames, seqOffset)):

                        atomSelection = []

                        if offset != 0 and ps is None:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                          f"of chain {chainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            return

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)

                        if _cifCompId is None and offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            idx = ps['auth_seq_id'].index(cifSeqId)
                            try:
                                _cifSeqId = ps['auth_seq_id'][idx + offset]
                                _cifCompId = ps['comp_id'][idx + offset]

                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)
                            except IndexError:
                                pass

                        if _cifCompId is None:
                            # """
                            # try:
                            #     _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            # except IndexError:
                            #     pass
                            # """
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

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)
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
                            else:
                                cifAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList
                                              if atomId.match(cca[self.ccU.ccaAtomId])
                                              and (coordAtomSite is None
                                                   or (coordAtomSite is not None and cca[self.ccU.ccaAtomId] in coordAtomSite['atom_id']))]

                                if len(cifAtomIds) > 0:
                                    if prevCifAtomId is not None and offset == prevOffset:
                                        cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds
                                                          if any(True for b in self.ccU.lastBonds
                                                                 if ((b[self.ccU.ccbAtomId1] == prevCifAtomId and b[self.ccU.ccbAtomId2] == _cifAtomId)
                                                                     or (b[self.ccU.ccbAtomId1] == _cifAtomId and b[self.ccU.ccbAtomId2] == prevCifAtomId)))), None)
                                        if cifAtomId is None:
                                            offset -= 1
                                            _cifSeqId = cifSeqId + offset
                                            _cifCompId = cifCompId if offset == 0\
                                                else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)
                                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)
                                            if coordAtomSite is not None:
                                                cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds if _cifAtomId in coordAtomSite['atom_id']), None)

                                    else:
                                        cifAtomId = cifAtomIds[0]
                                else:
                                    cifAtomId = None

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                elif _compId in monDict3:
                                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                                  f"The angle identifier {self.genSimpleNameSelection[1]!r} is unknown for the residue {_compId!r}.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle "
                                                  "is not present in the coordinates.")
                                return

                        prevCifAtomId = cifAtomId
                        prevOffset = offset

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        self.testCoordAtomIdConsistency(chainId, _cifSeqId, _cifCompId, cifAtomId, seqKey, coordAtomSite, True)

                        if self.hasCoord and coordAtomSite is None:
                            return

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
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
                            _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                    [atom1, atom2, atom3, atom4],
                                                                    'plane_like' in dstFunc)

                            if _angleName is not None and _angleName.startswith('pseudo'):
                                _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                    [atom1, atom2, atom3, atom4],
                                                                                                    self.getCurrentRestraint())
                                self.f.append(err)

                            if _angleName in emptyValue and atomSelTotal != 4:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                [atom1, atom2, atom3, atom4],
                                                                'plane_like' in dstFunc)

                        if _angleName is not None and _angleName.startswith('pseudo'):
                            _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                [atom1, atom2, atom3, atom4],
                                                                                                self.getCurrentRestraint())
                            self.f.append(err)

                        if _angleName in emptyValue and atomSelTotal != 4:
                            continue

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                            dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                              dstFunc)
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
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

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId]))

                self.retrieveLocalSeqScheme()

                chainAssign, _ = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, _compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                      f"The angle identifier {self.genSimpleNameSelection[1]!r} did not match with residue {_compId!r}.")
                        return

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

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

                            cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                elif _compId in monDict3:
                                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                                  f"The angle identifier {self.genSimpleNameSelection[1]!r} is unknown for the residue {_compId!r}.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle "
                                                  "is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
                    except IndexError:
                        self.areUniqueCoordAtoms('a torsion angle')
                        return

                    len_f = len(self.f)
                    self.areUniqueCoordAtoms('a torsion angle',
                                             allow_ambig=True, allow_ambig_warn_title='Ambiguous dihedral angle')
                    combinationId = '.' if len_f == len(self.f) else 0

                    if isinstance(combinationId, int):
                        fixedAngleName = '.'
                        for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                            self.atomSelectionSet[1],
                                                                            self.atomSelectionSet[2],
                                                                            self.atomSelectionSet[3]):
                            _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                    [atom1, atom2, atom3, atom4],
                                                                    False)

                            if _angleName in emptyValue:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                [atom1, atom2, atom3, atom4],
                                                                False)

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         combinationId, None, angleName,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         None, None, None, None, atom5)
                            sf['loop'].add_data(row)

                    if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                        sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except (ValueError, AttributeError):
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#rdc_restraints.
    def enterRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'rdc'
        self.cur_dist_type = ''

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

        self.rdcParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#rdc_restraints.
    def exitRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#rdc_parameter.
    def enterRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#rdc_parameter.
    def exitRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):
        orientation = self.cur_rdc_orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1))) if ctx.Integer(1)\
            else str(ctx.Capital_integer()) if ctx.Capital_integer()\
            else str(ctx.Integer_capital()) if ctx.Integer_capital()\
            else str(ctx.Simple_name())

        self.rdcParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.debug:
            print(f"subtype={self.cur_subtype} orientation={orientation} "
                  f"parameters={self.rdcParameterDict[orientation]}")

        self.numberSelection.clear()

        # if self.createSfDict:
        #     self.addSf(constraintType='RDC', orientationId=orientation, cyanaParameter=self.rdcParameterDict[orientation])

    # Enter a parse tree produced by CyanaMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

        if self.createSfDict:
            self.trimSfWoLp()

    # Exit a parse tree produced by CyanaMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()
            seqId2, chainId2 = self.genResNumSelection[1]
            compId2 = self.genSimpleNameSelection[2].upper()
            atomId2 = self.genSimpleNameSelection[3].upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer()))

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            if orientation not in self.rdcParameterDict:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The orientation '{orientation}' must be defined before you start to describe RDC restraints.")
                return

            if seqId1 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The residue number '{seqId1}' must not be the same as the center of orientation.")
                return

            if seqId2 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The residue number '{seqId2}' must not be the same as the center of orientation.")
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

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
                cyanaParameter = None if orientation not in self.rdcParameterDict else self.rdcParameterDict[orientation]
                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                orientationId=orientation, cyanaParameter=cyanaParameter)
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

        except (ValueError, AttributeError):
            self.rdcRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#pcs_restraints.
    def enterPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'pcs'
        self.cur_dist_type = ''

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

        self.pcsParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#pcs_restraints.
    def exitPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#pcs_parameter.
    def enterPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#pcs_parameter.
    def exitPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):
        orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1))) if ctx.Integer(1)\
            else str(ctx.Capital_integer()) if ctx.Capital_integer()\
            else str(ctx.Integer_capital()) if ctx.Integer_capital()\
            else str(ctx.Simple_name())

        self.pcsParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.debug:
            print(f"subtype={self.cur_subtype} orientation={orientation} "
                  f"parameters={self.pcsParameterDict[orientation]}")

        self.numberSelection.clear()

        # if self.createSfDict:
        #     self.addSf(orientationId=orientation, cyanaParameter=self.pcsParameterDict[orientation])

    # Enter a parse tree produced by CyanaMRParser#pcs_restraint.
    def enterPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument
        self.pcsRestraints += 1

        self.atomSelectionSet.clear()

        if self.createSfDict:
            self.trimSfWoLp()

    # Exit a parse tree produced by CyanaMRParser#pcs_restraint.
    def exitPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId, chainId = self.genResNumSelection[0]
            compId = self.genSimpleNameSelection[0].upper()
            atomId = self.genSimpleNameSelection[1].upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.pcsRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer()))

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            if orientation not in self.pcsParameterDict:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The orientation '{orientation}' must be defined before you start to describe PCS restraints.")
                return

            if seqId == self.pcsParameterDict[orientation]['orientation_center_seq_id']:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The residue number '{seqId}' must not be the same as the center of orientation.")
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validatePcsRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign, asis = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

            if len(chainAssign) == 0:
                return

            self.selectCoordAtoms(chainAssign, seqId, compId, atomId)

            if len(self.atomSelectionSet) < 1:
                return

            if self.createSfDict:
                cyanaParameter = None if orientation not in self.pcsParameterDict else self.pcsParameterDict[orientation]
                sf = self.getSf(orientationId=orientation, cyanaParameter=cyanaParameter)
                sf['id'] += 1

            for atom in self.atomSelectionSet[0]:
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.pcsRestraints} "
                          f"atom={atom} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom, asis1=asis)
                    sf['loop'].add_data(row)

        except (ValueError, AttributeError):
            self.pcsRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def enterFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixres' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def exitFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def enterFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def exitFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col, value in enumerate(self.numberSelection):
                atomId1 = self.genSimpleNameSelection[str_col].upper()
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col + 1].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 2].upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if 'upl' in (self.file_ext, self.cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.file_ext, self.cur_dist_type):
                        lower_limit = value

                    elif self.upl_or_lol is None:
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_only':
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                        self.local_dist_types.append(self.cur_dist_type)

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixres'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def enterFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixresw' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def exitFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def enterFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def exitFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col in range(0, len(self.numberSelection), 2):
                atomId1 = self.genSimpleNameSelection[str_col].upper()
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col + 1].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 2].upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = 1.0

                delta = None
                has_square = False

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    has_square = True

                target_value = None
                lower_limit = None
                upper_limit = None
                target_value_uncertainty = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if has_square:

                        if 'upl' in (self.file_ext, self.cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.file_ext, self.cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif (0.0 if self.file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:

                        if 'upl' in (self.file_ext, self.cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.file_ext, self.cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        else:
                            if self.applyPdbStatCap:
                                target_value = value
                                if delta > 0.0:
                                    lower_limit = value - delta
                                    upper_limit = value + delta
                            else:
                                upper_limit = value
                                if value2 > 0.0:
                                    target_value_uncertainty = value2

                    elif 'upl' in (self.file_ext, self.cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.file_ext, self.cur_dist_type):
                        lower_limit = value

                    elif self.upl_or_lol is None:
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_only':
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                        self.local_dist_types.append(self.cur_dist_type)

                    if weight < 0.0:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"The relative weight value of '{weight}' must not be a negative value.")
                        return
                    if weight == 0.0:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The relative weight value of '{weight}' should be a positive value.")

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    elif has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def enterFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixresw2' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def exitFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def enterFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def exitFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col in range(0, len(self.numberSelection), 3):
                atomId1 = self.genSimpleNameSelection[str_col].upper()
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col + 1].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 2].upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw2'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    else:
                        lower_limit = value
                        upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 3

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def enterFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixatm' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def exitFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def enterFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def exitFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col, value in enumerate(self.numberSelection):
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 1].upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if 'upl' in (self.file_ext, self.cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.file_ext, self.cur_dist_type):
                        lower_limit = value

                    elif self.upl_or_lol is None:
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_only':
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                        self.local_dist_types.append(self.cur_dist_type)

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixatm'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def enterFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixatmw' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def exitFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def enterFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def exitFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col in range(0, len(self.numberSelection), 2):
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 1].upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = 1.0

                delta = None
                has_square = False

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    has_square = True

                target_value = None
                lower_limit = None
                upper_limit = None
                target_value_uncertainty = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if has_square:

                        if 'upl' in (self.file_ext, self.cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.file_ext, self.cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif (0.0 if self.file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:

                        if 'upl' in (self.file_ext, self.cur_dist_type):
                            upper_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        elif 'lol' in (self.file_ext, self.cur_dist_type):
                            lower_limit = value
                            if len(self.numberSelection) > 1:
                                weight = abs(value2)

                        else:
                            if self.applyPdbStatCap:
                                target_value = value
                                if delta > 0.0:
                                    lower_limit = value - delta
                                    upper_limit = value + delta
                            else:
                                upper_limit = value
                                if value2 > 0.0:
                                    target_value_uncertainty = value2

                    elif 'upl' in (self.file_ext, self.cur_dist_type):
                        upper_limit = value

                    elif 'lol' in (self.file_ext, self.cur_dist_type):
                        lower_limit = value

                    elif self.upl_or_lol is None:
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_only':
                        if self.cur_dist_type == 'upl':
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                        self.local_dist_types.append(self.cur_dist_type)

                    if weight < 0.0:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      f"The relative weight value of '{weight}' must not be a negative value.")
                        return
                    if weight == 0.0:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The relative weight value of '{weight}' should be a positive value.")

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    elif has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def enterFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext not in ('upv', 'lov') else 'noepk'
        if self.reasons is not None and 'noepk_fixatmw2' in self.reasons:
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False
        self.cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def exitFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def enterFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def exitFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.reasons is not None and self.omitDistLimitOutlier

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            asis1 = asis2 = False

            for num_col in range(0, len(self.numberSelection), 3):
                seqId2, chainId2 = self.genResNumSelection[int_col]
                compId2 = self.genSimpleNameSelection[str_col].upper()
                atomId2 = self.genSimpleNameSelection[str_col + 1].upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        self.max_dist_value = max(self.max_dist_value, value)
                        self.min_dist_value = min(self.min_dist_value, value)

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    if self.hasPolySeq:

                        self.retrieveLocalSeqScheme()

                        chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                        chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         None,
                                                         omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw2'] = True

                else:  # 'noepk'

                    if self.file_ext == 'upv':
                        upper_limit = value
                    elif self.file_ext == 'lov':
                        lower_limit = value
                    else:
                        lower_limit = value
                        upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                if self.cur_subtype != 'dist':

                    self.retrieveLocalSeqScheme()

                    chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                    chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

                if self.createSfDict:
                    if memberLogicCode == 'OR' and has_intra_chain and len(rep_chain_id_set) == 1:
                        memberLogicCode = '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

                if num_col > 0 and self.cur_subtype == 'dist':
                    self.distRestraints += 1

                self.atomSelectionSet.clear()

                int_col += 1
                str_col += 2

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def enterQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def exitQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def enterQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def exitQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):  # pylint: disable=unused-argument

        try:

            upl = bool(ctx.NoeUpp())

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()
            seqId2, chainId2 = self.genResNumSelection[1]
            compId2 = self.genSimpleNameSelection[2].upper()
            atomId2 = self.genSimpleNameSelection[3].upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            value = self.numberSelection[0]
            weight = 1.0

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                if upl and value > self.max_dist_value:
                    self.max_dist_value = value
                if not upl and value < self.min_dist_value:
                    self.min_dist_value = value

            if upl:
                upper_limit = value
            else:
                lower_limit = value

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

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

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                 None,
                                                 self.omitDistLimitOutlier)

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

        except (ValueError, AttributeError):
            self.distRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def enterDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext != 'cco' else 'jcoup'
        if (self.file_ext is not None and self.file_ext in ('upv', 'lov')) or (self.reasons is not None and 'noepk_w_chain' in self.reasons):
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def exitDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def enterDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.cur_subtype == 'jcoup':
            self.jcoupRestraints += 1
        elif self.cur_subtype == 'noepk':
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def exitDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):

        if self.cur_subtype in ('dist', 'noepk') and (self.cur_dist_type == 'cco' or len(self.numberSelection) == 6):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.cur_subtype == 'noepk':
                self.noepkRestraints -= 1
            self.cur_subtype = 'jcoup'
            self.jcoupRestraints += 1

        try:

            unambig = self.cur_subtype != 'dist'

            seqId1 = int(str(ctx.Integer(0)))
            seqId2 = int(str(ctx.Integer(1)))
            jVal = [''] * 6
            for j in range(6):
                jVal[j] = self.genSimpleNameSelection[j].upper()

            minLenCompId = 2 if self.polyPeptide else (1 if self.polyDeoxyribonucleotide else 0)
            if minLenCompId == 0:
                if any(True for _compId in jVal if _compId.startswith('R')):
                    minLenCompId = 1

            if len(self.col_order_of_dist_w_chain) == 0:
                for j in range(3):
                    if len(jVal[j]) > minLenCompId and translateToStdResName(jVal[j], ccU=self.ccU) in monDict3:
                        compId = translateToStdResName(jVal[j], ccU=self.ccU)
                        if self.ccU.updateChemCompDict(compId):
                            for k in range(3):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                chainId = jVal[3 - (j + k)]
                                if atomId in ('M', 'Q'):
                                    continue
                                if self.hasPolySeq and len(atomId) < len(chainId) and any(True for ps in self.polySeq if atomId in (ps['auth_chain_id'], ps['chain_id'])):
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, chainId, leave_unmatched=True)
                                    if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                        _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                        if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                            _atomId = [_atomId[int(atomId[-1]) - 1]]

                                    if details is not None or atomId.endswith('"'):
                                        _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                        if _atomId_ != atomId:
                                            if atomId.startswith('HT') and len(_atomId_) == 2:
                                                _atomId_ = 'H'
                                            _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                    if len(_atomId) > 0:
                                        continue
                                _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None or atomId.endswith('"'):
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                    if _atomId_ != atomId:
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        if minLenCompId == 0 and 3 - (j + k) != 0:
                                            continue
                                        self.col_order_of_dist_w_chain['comp_id_1'] = j
                                        self.col_order_of_dist_w_chain['atom_id_1'] = k
                                        self.col_order_of_dist_w_chain['chain_id_1'] = 3 - (j + k)
                                        break
                            if len(self.col_order_of_dist_w_chain) == 3:
                                break
                    elif len(jVal[j]) > 1 and translateToStdResName(jVal[j], ccU=self.ccU) not in monDict3:
                        compId = translateToStdResName(jVal[j], ccU=self.ccU)
                        if self.ccU.updateChemCompDict(compId):
                            for k in range(3):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                chainId = jVal[3 - (j + k)]
                                if atomId in ('M', 'Q'):
                                    continue
                                if self.hasPolySeq and len(atomId) < len(chainId) and any(True for ps in self.polySeq if atomId in (ps['auth_chain_id'], ps['chain_id'])):
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, chainId, leave_unmatched=True)
                                    if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                        _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                        if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                            _atomId = [_atomId[int(atomId[-1]) - 1]]

                                    if details is not None or atomId.endswith('"'):
                                        _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                        if _atomId_ != atomId:
                                            if atomId.startswith('HT') and len(_atomId_) == 2:
                                                _atomId_ = 'H'
                                            _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                    if len(_atomId) > 0:
                                        continue
                                _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None or atomId.endswith('"'):
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                    if _atomId_ != atomId:
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.col_order_of_dist_w_chain['comp_id_1'] = j
                                        self.col_order_of_dist_w_chain['atom_id_1'] = k
                                        self.col_order_of_dist_w_chain['chain_id_1'] = 3 - (j + k)
                                        break
                            if len(self.col_order_of_dist_w_chain) == 3:
                                break
                for j in range(3, 6):
                    if len(jVal[j]) > minLenCompId and translateToStdResName(jVal[j], ccU=self.ccU) in monDict3:
                        compId = translateToStdResName(jVal[j], ccU=self.ccU)
                        if self.ccU.updateChemCompDict(compId):
                            for k in range(3, 6):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                chainId = jVal[12 - (j + k)]
                                if atomId in ('M', 'Q'):
                                    continue
                                if self.hasPolySeq and len(atomId) < len(chainId) and any(True for ps in self.polySeq if atomId in (ps['auth_chain_id'], ps['chain_id'])):
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, chainId, leave_unmatched=True)
                                    if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                        _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                        if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                            _atomId = [_atomId[int(atomId[-1]) - 1]]

                                    if details is not None or atomId.endswith('"'):
                                        _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        if _atomId_ != atomId:
                                            _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                    if len(_atomId) > 0:
                                        continue
                                _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None or atomId.endswith('"'):
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                    if atomId.startswith('HT') and len(_atomId_) == 2:
                                        _atomId_ = 'H'
                                    if _atomId_ != atomId:
                                        _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        if minLenCompId == 0 and 12 - (j + k) != 3:
                                            continue
                                        self.col_order_of_dist_w_chain['comp_id_2'] = j
                                        self.col_order_of_dist_w_chain['atom_id_2'] = k
                                        self.col_order_of_dist_w_chain['chain_id_2'] = 12 - (j + k)
                                        break
                            if len(self.col_order_of_dist_w_chain) == 6:
                                break
                    elif len(jVal[j]) > 1 and translateToStdResName(jVal[j], ccU=self.ccU) not in monDict3:
                        compId = translateToStdResName(jVal[j], ccU=self.ccU)
                        if self.ccU.updateChemCompDict(compId):
                            for k in range(3, 6):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                chainId = jVal[12 - (j + k)]
                                if atomId in ('M', 'Q'):
                                    continue
                                if self.hasPolySeq and len(atomId) < len(chainId) and any(True for ps in self.polySeq if atomId in (ps['auth_chain_id'], ps['chain_id'])):
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, chainId, leave_unmatched=True)
                                    if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                        _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                        if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                            _atomId = [_atomId[int(atomId[-1]) - 1]]

                                    if details is not None or atomId.endswith('"'):
                                        _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                        if atomId.startswith('HT') and len(_atomId_) == 2:
                                            _atomId_ = 'H'
                                        if _atomId_ != atomId:
                                            _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                    if len(_atomId) > 0:
                                        continue
                                _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                                    if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                                        _atomId = [_atomId[int(atomId[-1]) - 1]]

                                if details is not None or atomId.endswith('"'):
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=unambig)
                                    if atomId.startswith('HT') and len(_atomId_) == 2:
                                        _atomId_ = 'H'
                                    if _atomId_ != atomId:
                                        _atomId = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.col_order_of_dist_w_chain['comp_id_2'] = j
                                        self.col_order_of_dist_w_chain['atom_id_2'] = k
                                        self.col_order_of_dist_w_chain['chain_id_2'] = 12 - (j + k)
                                        break
                            if len(self.col_order_of_dist_w_chain) == 6:
                                break

            if len(self.col_order_of_dist_w_chain) != 6:

                if not self.hasPolySeq:
                    return

                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Failed to identify columns for comp_id_1, atom_id_1, chain_id_1, comp_id_2, atom_id_2, chain_id_2.")

                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                elif self.cur_subtype == 'noepk':
                    self.noepkRestraints -= 1
                return

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                if self.cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                elif self.cur_subtype == 'noepk':
                    self.noepkRestraints -= 1
                return

            if self.cur_subtype == 'jcoup' and self.hasPolySeq:

                chainId1 = jVal[self.col_order_of_dist_w_chain['chain_id_1']]
                chainId2 = jVal[self.col_order_of_dist_w_chain['chain_id_2']]
                compId1 = jVal[self.col_order_of_dist_w_chain['comp_id_1']]
                compId2 = jVal[self.col_order_of_dist_w_chain['comp_id_2']]
                atomId1 = jVal[self.col_order_of_dist_w_chain['atom_id_1']]
                atomId2 = jVal[self.col_order_of_dist_w_chain['atom_id_2']]

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                if len(chainAssign1) > 0 and len(chainAssign2) > 0:

                    self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                    if len(self.atomSelectionSet) >= 2:

                        if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                            isCco = True

                            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                                isCco = False

                            if chain_id_1 != chain_id_2:
                                isCco = False

                            if abs(seq_id_1 - seq_id_2) > 1:
                                isCco = False

                            if not isCco:
                                self.jcoupRestraints -= 1
                                self.cur_subtype = 'dist'
                                self.cur_dist_type = ''
                                self.distRestraints += 1

            if self.cur_subtype in ('dist', 'noepk'):

                target_value = None
                lower_limit = None
                upper_limit = None
                target_value_uncertainty = None

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.cur_subtype_altered and self.cur_subtype == 'dist':
                    self.max_dist_value = max(self.max_dist_value, value)
                    self.min_dist_value = min(self.min_dist_value, value)

                if has_square:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        upper_limit = value2
                        lower_limit = value

                    elif value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif (0.0 if self.file_ext in ('upl', 'lol') else 1.8) <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:

                    if 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                        upper_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                        lower_limit = value
                        if len(self.numberSelection) > 1:
                            weight = abs(value2)

                    elif self.cur_subtype == 'noepk':
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta

                    else:
                        if self.applyPdbStatCap:
                            target_value = value
                            if delta > 0.0:
                                lower_limit = value - delta
                                upper_limit = value + delta
                        else:
                            upper_limit = value
                            if value2 > 0.0:
                                target_value_uncertainty = value2

                elif 'upl' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'upv':
                    upper_limit = value

                elif 'lol' in (self.file_ext, self.cur_dist_type) or self.file_ext == 'lov':
                    lower_limit = value

                elif self.cur_subtype == 'noepk':
                    target_value = value

                elif self.upl_or_lol is None:
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_only':
                    if self.cur_dist_type == 'upl':
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.cur_dist_type) > 0 and self.cur_dist_type not in self.local_dist_types:
                    self.local_dist_types.append(self.cur_dist_type)

                if not self.hasPolySeq and not self.hasNonPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                chainId1 = jVal[self.col_order_of_dist_w_chain['chain_id_1']]
                chainId2 = jVal[self.col_order_of_dist_w_chain['chain_id_2']]
                compId1 = jVal[self.col_order_of_dist_w_chain['comp_id_1']]
                compId2 = jVal[self.col_order_of_dist_w_chain['comp_id_2']]
                atomId1 = jVal[self.col_order_of_dist_w_chain['atom_id_1']]
                atomId2 = jVal[self.col_order_of_dist_w_chain['atom_id_2']]

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if atom_id_1[0] not in ('H', 'C', 'N') or atom_id_2[0] not in ('H', 'C', 'N')\
                       or atom_id_1[0] == atom_id_2[0] == 'H':
                        isRdc = False

                    elif chain_id_1 != chain_id_2:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    elif abs(seq_id_1 - seq_id_2) == 1:

                        if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')):
                            pass
                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        bbAtoms = self.csStat.getBackBoneAtoms(comp_id_1, excl_minor_atom=True)
                        if atom_id_1 not in bbAtoms or atom_id_2 not in bbAtoms:
                            isRdc = False

                        elif not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                            if (atom_id_1[0] == 'H' and atom_id_2[0] != 'H')\
                               or (atom_id_1[0] != 'H' and atom_id_2[0] == 'H'):
                                isRdc = False
                            elif comp_id_1 in monDict3\
                                    and self.nefT.validate_comp_atom(comp_id_1, atom_id_1)\
                                    and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                pass
                            else:
                                isRdc = False

                    else:
                        isRdc = False

                    if not isRdc:
                        self.cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.cur_subtype_altered = True
                            self.cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            if self.cur_subtype == 'dist':
                                self.distRestraints -= 1
                            else:
                                self.noepkRestraints -= 1
                            self.cur_subtype = 'rdc'
                            self.rdcRestraints += 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.createSfDict:
                                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                                rdcCode=getRdcCode([self.atomSelectionSet[0][0], self.atomSelectionSet[1][0]]),
                                                orientationId=self.cur_rdc_orientation)
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                atoms = [atom1, atom2]
                                if isIdenticalRestraint(atoms, self.nefT):
                                    continue
                                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                                    continue
                                if self.debug:
                                    print(f"subtype={self.cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None, None,
                                                 sf['list_id'], self.entryId, dstFunc,
                                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                                 atom1, atom2, asis1=asis1, asis2=asis2)
                                    sf['loop'].add_data(row)

                            self.cur_subtype = 'dist'

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

                if self.cur_subtype == 'noepk':
                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)
                else:
                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit,
                                                         target_value_uncertainty,
                                                         self.omitDistLimitOutlier)

                if self.cur_subtype == 'dist' and dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                    self.reasonsForReParsing['noepk_w_chain'] = True

                if dstFunc is None:
                    return

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.atomSelectionSet.clear()

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.createSfDict:
                    sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                         self.csStat, self.originalFileName),
                                    potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                    sf['id'] += 1
                    memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'

                    memberId = '.'
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
                        print(f"subtype={self.cur_subtype} id={self.distRestraints if self.cur_subtype == 'dist' else self.noepkRestraints} "
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

                        if self.cur_subtype == 'noepk':
                            break

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

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' must not be a negative value.")
                    return
                if weight == 0.0:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The relative weight value of '{weight}' should be a positive value.")

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                chainId1 = jVal[self.col_order_of_dist_w_chain['chain_id_1']]
                chainId2 = jVal[self.col_order_of_dist_w_chain['chain_id_2']]
                compId1 = jVal[self.col_order_of_dist_w_chain['comp_id_1']]
                compId2 = jVal[self.col_order_of_dist_w_chain['comp_id_2']]
                atomId1 = jVal[self.col_order_of_dist_w_chain['atom_id_1']]
                atomId2 = jVal[self.col_order_of_dist_w_chain['atom_id_2']]

                self.retrieveLocalSeqScheme()

                chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
                chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Non-magnetic susceptible spin appears in scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                  f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-chain scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:

                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 in ('H', 'N'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('H', 'N') and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}
                             or (seq_id_1 < seq_id_2 and atom_id_2 == 'P')):
                        pass

                    else:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-residue scalar coupling constant; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found zero scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if self.createSfDict:
                    sf = self.getSf()
                    sf['id'] += 1

                for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    self.ccU.updateChemCompDict(atom1['comp_id'])
                    atom2_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                    atom3_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                    atom_id_2 = atom_id_3 = None
                    for ccb in self.ccU.lastBonds:
                        if ccb[self.ccU.ccbAtomId1] in atom2_can and ccb[self.ccU.ccbAtomId2] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId1]
                            atom_id_3 = ccb[self.ccU.ccbAtomId2]
                            break
                        if ccb[self.ccU.ccbAtomId2] in atom2_can and ccb[self.ccU.ccbAtomId1] in atom3_can:
                            atom_id_2 = ccb[self.ccU.ccbAtomId2]
                            atom_id_3 = ccb[self.ccU.ccbAtomId1]
                            break
                    if None in (atom_id_2, atom_id_3):
                        continue
                    atom2 = copy.copy(atom1)
                    atom2['atom_id'] = atom_id_2
                    atom3 = copy.copy(atom4)
                    atom3['atom_id'] = atom_id_3
                    if self.debug:
                        print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4,
                                     asis1=asis1, asis2=asis1, asis3=asis2, asis4=asis2)
                        sf['loop'].add_data(row)

        except (ValueError, AttributeError):
            if self.cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def enterDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext != 'cco' else 'jcoup'
        if (self.file_ext is not None and self.file_ext in ('upv', 'lov')) or (self.reasons is not None and 'noepk_w_chain' in self.reasons):
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def exitDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def enterDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.cur_subtype == 'jcoup':
            self.jcoupRestraints += 1
        elif self.cur_subtype == 'noepk':
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def exitDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def enterDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist' if self.file_ext is None or self.file_ext != 'cco' else 'jcoup'
        if (self.file_ext is not None and self.file_ext in ('upv', 'lov')) or (self.reasons is not None and 'noepk_w_chain' in self.reasons):
            self.cur_subtype = 'noepk'

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def exitDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def enterDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.cur_subtype == 'jcoup':
            self.jcoupRestraints += 1
        elif self.cur_subtype == 'noepk':
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def exitDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def enterTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'
        self.cur_dist_type = ''

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def exitTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def enterTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def exitTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):

        try:

            chainId = self.genSimpleNameSelection[0]
            seqId = int(str(ctx.Integer(0)))
            compId = self.genSimpleNameSelection[1].upper()
            _compId = translateToStdResName(compId, ccU=self.ccU)
            angleName = self.genSimpleNameSelection[2].upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.remediate and self.reasons is not None and 'dihed_unusual_order' in self.reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")
            """
            if lower_limit > upper_limit:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.")
                if self.remediate:
                    self.dihed_lb_greater_than_ub = True
                return
            """
            if self.remediate and upper_limit < 0.0:
                self.dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                  f"The angle identifier {self.genSimpleNameSelection[2]!r} is unknown for the residue {_compId!r}, "
                                  "of which CYANA residue library should be uploaded.")
                    return

            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign, _ = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, 'CA', False)
                if len(chainAssign) > 0:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainAssign[0][0]), None)
                    if ps is not None and 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId])), None)
                            if atomId is None:
                                resKey = (seqId, _compId)
                                if resKey not in self.extResKey:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId}:{_compId} is not present in the coordinates.")
                                return

                self.retrieveLocalSeqScheme()

                chainAssign, _ = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, _compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = None

                    if carbohydrate:
                        if self.branched is not None:
                            ps = next((ps for ps in self.branched if ps['auth_chain_id'] == chainId), None)
                            if ps is None:
                                ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)
                    else:
                        ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                      f"The angle identifier {self.genSimpleNameSelection[2]!r} is unknown for the residue {_compId!r}, "
                                      "of which CYANA residue library should be uploaded.")
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    prevCifAtomId = None
                    prevOffset = None

                    for ord, (atomId, offset) in enumerate(zip(atomNames, seqOffset)):

                        atomSelection = []

                        if offset != 0 and ps is None:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                          f"of chain {chainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            return

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)

                        if _cifCompId is None and offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            idx = ps['auth_seq_id'].index(cifSeqId)
                            try:
                                _cifSeqId = ps['auth_seq_id'][idx + offset]
                                _cifCompId = ps['comp_id'][idx + offset]

                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)
                            except IndexError:
                                pass

                        if _cifCompId is None:
                            # """
                            # try:
                            #     _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            # except IndexError:
                            #     pass
                            # """
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

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)
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
                            else:
                                cifAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList
                                              if atomId.match(cca[self.ccU.ccaAtomId])
                                              and (coordAtomSite is None
                                                   or (coordAtomSite is not None and cca[self.ccU.ccaAtomId] in coordAtomSite['atom_id']))]

                                if len(cifAtomIds) > 0:
                                    if prevCifAtomId is not None and offset == prevOffset:
                                        cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds
                                                          if any(True for b in self.ccU.lastBonds
                                                                 if ((b[self.ccU.ccbAtomId1] == prevCifAtomId and b[self.ccU.ccbAtomId2] == _cifAtomId)
                                                                     or (b[self.ccU.ccbAtomId1] == _cifAtomId and b[self.ccU.ccbAtomId2] == prevCifAtomId)))), None)
                                        if cifAtomId is None:
                                            offset -= 1
                                            _cifSeqId = cifSeqId + offset
                                            _cifCompId = cifCompId if offset == 0\
                                                else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)
                                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, _cifSeqId, _cifCompId, cifCheck=self.hasCoord)
                                            if coordAtomSite is not None:
                                                cifAtomId = next((_cifAtomId for _cifAtomId in cifAtomIds if _cifAtomId in coordAtomSite['atom_id']), None)

                                    else:
                                        cifAtomId = cifAtomIds[0]
                                else:
                                    cifAtomId = None

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                elif _compId in monDict3:
                                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                                  f"The angle identifier {self.genSimpleNameSelection[2]!r} is unknown for the residue {_compId!r}.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle "
                                                  "is not present in the coordinates.")
                                return

                        prevCifAtomId = cifAtomId
                        prevOffset = offset

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        self.testCoordAtomIdConsistency(chainId, _cifSeqId, _cifCompId, cifAtomId, seqKey, coordAtomSite, True)

                        if self.hasCoord and coordAtomSite is None:
                            return

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
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
                            _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                    [atom1, atom2, atom3, atom4],
                                                                    'plane_like' in dstFunc)

                            if _angleName is not None and _angleName.startswith('pseudo'):
                                _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                    [atom1, atom2, atom3, atom4],
                                                                                                    self.getCurrentRestraint())
                                self.f.append(err)

                            if _angleName in emptyValue and atomSelTotal != 4:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                [atom1, atom2, atom3, atom4],
                                                                'plane_like' in dstFunc)

                        if _angleName is not None and _angleName.startswith('pseudo'):
                            _angleName, atom2, atom3, err = fixBackboneAtomsOfDihedralRestraint(_angleName,
                                                                                                [atom1, atom2, atom3, atom4],
                                                                                                self.getCurrentRestraint())
                            self.f.append(err)

                        if _angleName in emptyValue and atomSelTotal != 4:
                            continue

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                            dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                              dstFunc)
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
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

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if atomId.match(cca[self.ccU.ccaAtomId]))

                self.retrieveLocalSeqScheme()

                chainAssign, _ = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    resKey = (seqId, _compId)
                    if resKey not in self.extResKey:
                        self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                      f"{seqId}:{_compId} is not present in the coordinates.")
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                      f"The angle identifier {self.genSimpleNameSelection[2]!r} did not match with residue {_compId!r}.")
                        return

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection = []

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

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

                            cifAtomId = next((cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                if _cifCompId is None and not self.allow_ext_seq:
                                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                  f"The residue number '{seqId+offset}' is not present in polymer sequence "
                                                  f"of chain {chainId} of the coordinates. "
                                                  "Please update the sequence in the Macromolecules page.")
                                elif _compId in monDict3:
                                    self.f.append(f"[Insufficient angle selection] {self.getCurrentRestraint()}"
                                                  f"The angle identifier {self.genSimpleNameSelection[2]!r} is unknown for the residue {_compId!r}.")
                                else:
                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                  f"{seqId+offset}:{_compId}:{atomId} involved in the {angleName} dihedral angle "
                                                  "is not present in the coordinates.")
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    try:
                        self.atomSelectionSet[0][0]['comp_id']
                    except IndexError:
                        self.areUniqueCoordAtoms('a torsion angle')
                        return

                    len_f = len(self.f)
                    self.areUniqueCoordAtoms('a torsion angle',
                                             allow_ambig=True, allow_ambig_warn_title='Ambiguous dihedral angle')
                    combinationId = '.' if len_f == len(self.f) else 0

                    if isinstance(combinationId, int):
                        fixedAngleName = '.'
                        for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                            self.atomSelectionSet[1],
                                                                            self.atomSelectionSet[2],
                                                                            self.atomSelectionSet[3]):
                            _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                    [atom1, atom2, atom3, atom4],
                                                                    False)

                            if _angleName in emptyValue:
                                continue

                            fixedAngleName = _angleName
                            break

                    if self.createSfDict:
                        sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.polySeq if self.gapInAuthSeq else None):
                            continue
                        _angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                                [atom1, atom2, atom3, atom4],
                                                                False)

                        if isinstance(combinationId, int):
                            if _angleName != fixedAngleName:
                                continue
                            combinationId += 1
                        if self.debug:
                            print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         combinationId, None, angleName,
                                         sf['list_id'], self.entryId, dstFunc,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         None, None, None, None, atom5)
                            sf['loop'].add_data(row)

                    if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                        sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        except (ValueError, AttributeError):
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#cco_restraints.
    def enterCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'jcoup'

        self.cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#cco_restraints.
    def exitCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#cco_restraint.
    def enterCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#cco_restraint.
    def exitCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):

        try:

            seqId1, chainId1 = self.genResNumSelection[0]
            compId1 = self.genSimpleNameSelection[0].upper()
            atomId1 = self.genSimpleNameSelection[1].upper()
            atomId2 = self.genSimpleNameSelection[2].upper()

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            if atomId2 in KNOWN_ANGLE_NAMES:
                self.cur_subtype_altered = True
                self.cur_subtype = 'dihed'
                self.dihedRestraints += 1
                self.jcoupRestraints -= 1
                self.exitTorsion_angle_restraint(ctx)
                return

            target = self.numberSelection[0]
            error = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                error = abs(self.numberSelection[1])
                weight = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                error = abs(self.numberSelection[1])

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = target
            lower_limit = target - error if error is not None else None
            upper_limit = target + error if error is not None else None

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId1, compId1, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a scalar coupling'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in scalar coupling constant; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found inter-chain scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:

                if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found inter-residue scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in rdcBbPairCode)
                         or (seq_id_1 > seq_id_2 and atom_id_1 in rdcBbPairCode and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 in ('H', 'N'))
                         or (seq_id_1 > seq_id_2 and atom_id_1 in ('H', 'N') and atom_id_2.startswith('HA'))
                         or {atom_id_1, atom_id_2} == {'H', 'N'}):
                    pass

                elif self.csStat.getTypeOfCompId(comp_id_1)[1] and self.csStat.getTypeOfCompId(comp_id_1)[1]\
                        and seq_id_1 < seq_id_2 and atom_id_2 == 'P':
                    pass

                else:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found inter-residue scalar coupling constant; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero scalar coupling constant; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if self.createSfDict:
                sf = self.getSf()
                sf['id'] += 1

            for atom1, atom4 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isLongRangeRestraint([atom1, atom4], self.polySeq if self.gapInAuthSeq else None):
                    if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                        continue
                self.ccU.updateChemCompDict(atom1['comp_id'])
                atom2_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom1['atom_id'])
                atom3_can = self.ccU.getBondedAtoms(atom1['comp_id'], atom4['atom_id'])
                atom_id_2 = atom_id_3 = None
                for ccb in self.ccU.lastBonds:
                    if ccb[self.ccU.ccbAtomId1] in atom2_can and ccb[self.ccU.ccbAtomId2] in atom3_can:
                        atom_id_2 = ccb[self.ccU.ccbAtomId1]
                        atom_id_3 = ccb[self.ccU.ccbAtomId2]
                        break
                    if ccb[self.ccU.ccbAtomId2] in atom2_can and ccb[self.ccU.ccbAtomId1] in atom3_can:
                        atom_id_2 = ccb[self.ccU.ccbAtomId2]
                        atom_id_3 = ccb[self.ccU.ccbAtomId1]
                        break
                if None in (atom_id_2, atom_id_3):
                    continue
                atom2 = copy.copy(atom1)
                atom2['atom_id'] = atom_id_2
                atom3 = copy.copy(atom4)
                atom3['atom_id'] = atom_id_3
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.jcoupRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis1, asis3=asis2, asis4=asis2)
                    sf['loop'].add_data(row)

        except (ValueError, AttributeError):
            self.jcoupRestraints -= 1

        finally:
            self.numberSelection.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#ssbond_macro.
    def enterSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'ssbond'
        self.cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#ssbond_macro.
    def exitSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):

        try:

            self.ssbondRestraints += 1

            try:
                _seqId1, _seqId2 = str(ctx.Ssbond_resids()).split('-')
                seqId1, seqId2 = int(_seqId1), int(_seqId2)
            except ValueError:
                self.ssbondRestraints -= 1
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            compId = 'CYSS'
            atomId = 'SG'

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequence(seqId1, compId, atomId)
            chainAssign2, asis2 = self.assignCoordPolymerSequence(seqId2, compId, atomId)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId, atomId)
            self.selectCoordAtoms(chainAssign2, seqId2, compId, atomId)

            if len(self.atomSelectionSet) < 2:
                return

            for atom1 in self.atomSelectionSet[0]:
                if atom1['comp_id'] != 'CYS':
                    self.f.append(f"[Invalid atom selection] {self.getCurrentRestraint()}"
                                  f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.")
                    self.ssbondRestraints -= 1
                    return

            for atom2 in self.atomSelectionSet[1]:
                if atom2['comp_id'] != 'CYS':
                    self.f.append(f"[Invalid atom selection] {self.getCurrentRestraint()}"
                                  f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.")
                    self.ssbondRestraints -= 1
                    return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
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

                _tail =\
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

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > 2.5:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The distance of the disulfide bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                      f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.verbose:
                    self.log.write(f"+{self.__class_name__}.exitSsbond_macro() ++ Error  - {str(e)}")

            if self.createSfDict:
                sf = self.getSf()
                sf['id'] += 1

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2], self.nefT):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CYANA macro: disulfide bond linkage) id={self.ssbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, getDstFuncForSsBond(atom1, atom2),
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, asis1=asis1, asis2=asis2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#hbond_macro.
    def enterHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'hbond'
        self.cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#hbond_macro.
    def exitHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):

        try:

            self.hbondRestraints += 1

            seqId1 = int(str(ctx.Integer_HB(0)))
            seqId2 = int(str(ctx.Integer_HB(1)))
            atomId1 = str(ctx.Simple_name_HB(0))
            atomId2 = str(ctx.Simple_name_HB(1))

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a hydrogen bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
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

                _tail =\
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

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > (3.4 if atom_id_1[0] not in protonBeginCode and atom_id_2[0] not in protonBeginCode else 2.4):
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                      f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.verbose:
                    self.log.write(f"+{self.__class_name__}.exitHbond_macro() ++ Error  - {str(e)}")

            if self.createSfDict:
                sf = self.getSf()
                sf['id'] += 1

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2], self.nefT):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CYANA macro: hydrogen bond linkage) id={self.hbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, getDstFuncForHBond(atom1, atom2),
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#link_statement.
    def enterLink_statement(self, ctx: CyanaMRParser.Link_statementContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'
        self.cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#link_statement.
    def exitLink_statement(self, ctx: CyanaMRParser.Link_statementContext):  # pylint: disable=unused-argument

        try:

            self.geoRestraints += 1

            seqId1, chainId1 = self.genResNumSelection[0]
            seqId2, chainId2 = self.genResNumSelection[1]
            atomId1 = self.genSimpleNameSelection[0]
            atomId2 = self.genSimpleNameSelection[1]

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

            if 0 in (len(chainAssign1), len(chainAssign2)):
                return

            # circular shift
            if self.reasons is not None and len(chainAssign1) == 1 and len(chainAssign2) == 1 and {atomId1, atomId2} == {'N', 'C'}:
                if 'seq_id_remap' in self.reasons:
                    chainId1 = chainAssign1[0][0]
                    chainId2 = chainAssign2[0][0]
                    if chainId1 == chainId2:
                        seqIdDict = next((remap['seq_id_dict'] for remap in self.reasons['seq_id_remap'] if remap['chain_id'] == chainId1), None)
                        if seqIdDict is not None:
                            seqIdDictKeys = seqIdDict.keys()
                            seqIdDictVals = seqIdDict.values()
                            minSeqId = min(seqIdDictKeys)
                            maxSeqId = max(seqIdDictKeys)
                            if {seqId1, seqId2} == {minSeqId, maxSeqId}:
                                _minSeqId = min(seqIdDictVals)
                                _maxSeqId = max(seqIdDictVals)
                                if seqId1 == minSeqId and atomId1 == 'N' and seqId2 == maxSeqId and atomId2 == 'C':
                                    seqId1 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                    seqId2 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

                                elif seqId2 == minSeqId and atomId2 == 'N' and seqId1 == maxSeqId and atomId1 == 'C':
                                    seqId2 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                    seqId1 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

                if 'chain_seq_id_remap' in self.reasons:
                    chainId1 = chainAssign1[0][0]
                    chainId2 = chainAssign2[0][0]
                    if chainId1 == chainId2:
                        seqIdDict = next((remap['seq_id_dict'] for remap in self.reasons['chain_seq_id_remap'] if remap['chain_id'] == chainId1), None)
                        if seqIdDict is not None:
                            seqIdDictKeys = seqIdDict.keys()
                            seqIdDictVals = seqIdDict.values()
                            minSeqId = min(seqIdDictKeys)
                            maxSeqId = max(seqIdDictKeys)
                            if {seqId1, seqId2} == {minSeqId, maxSeqId}:
                                _minSeqId = min(seqIdDictVals)
                                _maxSeqId = max(seqIdDictVals)
                                if seqId1 == minSeqId and atomId1 == 'N' and seqId2 == maxSeqId and atomId2 == 'C':
                                    seqId1 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                    seqId2 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

                                elif seqId2 == minSeqId and atomId2 == 'N' and seqId1 == maxSeqId and atomId1 == 'C':
                                    seqId2 = next(k for k, v in seqIdDict.items() if v == _minSeqId)
                                    seqId1 = next(k for k, v in seqIdDict.items() if v == _maxSeqId)

                                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a covalent bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
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

                _tail =\
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

                if len(_head) == 1 and len(_tail) == 1:
                    dist = distance(to_np_array(_head[0]), to_np_array(_tail[0]))
                    if dist > (3.5 if atom_id_1[0] not in protonBeginCode and atom_id_2[0] not in protonBeginCode else 2.5):
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The distance of the covalent bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "
                                      f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({dist:.3f}Å).")

            except Exception as e:
                if self.verbose:
                    self.log.write(f"+{self.__class_name__}.exitLink_statement() ++ Error  - {str(e)}")

            if self.createSfDict:
                sf = self.getSf('covalent bond linkage')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          'list_id']

            has_intra_chain, rep_chain_id_set = hasIntraChainRestraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isIdenticalRestraint([atom1, atom2], self.nefT):
                    continue
                if has_intra_chain and (atom1['chain_id'] != atom2['chain_id'] or atom1['chain_id'] not in rep_chain_id_set):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CYANA statement: covalent bond linkage) id={self.geoRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               sf['list_id']])

        finally:
            self.atomSelectionSet.clear()
            self.genResNumSelection.clear()
            self.genSimpleNameSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#stereoassign_macro.
    def enterStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'fchiral'
        self.cur_dist_type = ''

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#stereoassign_macro.
    def exitStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):

        try:

            self.fchiralRestraints += 1

            _strip = str(ctx.Double_quote_string()).strip('"').strip()
            _split = re.sub(' +', ' ', _strip).split(' ')

            len_split = len(_split)

            if len_split < 2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                return

            atomId1 = _split[0].upper()
            atomId2 = None

            if not atomId1.isalnum():
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                return

            if _split[1].isdecimal():
                seq_id_offset = 1
            else:
                seq_id_offset = 2
                atomId2 = _split[1].upper()

            for p in range(seq_id_offset, len_split):
                if not _split[p].isdecimal():
                    if len(_split[p]) > 1 and _split[p][1:].isdecimal():
                        continue
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.")
                    return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            seqId1 = int(_split[seq_id_offset] if _split[seq_id_offset][0].isdecimal() else _split[seq_id_offset][1:])

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

            if atomId2 is not None:

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if 0 in (len(chainAssign1), len(chainAssign2)):
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.createSfDict:
                    sf = self.getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2], self.nefT):
                        continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, None,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)
                        break

                for p in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[p] if _split[p][0].isdecimal() else _split[p][1:])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if 0 in (len(chainAssign1), len(chainAssign2)):
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if isIdenticalRestraint([atom1, atom2], self.nefT):
                            continue
                        if self.debug:
                            print(f"subtype={self.cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.entryId, None,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         atom1, atom2)
                            sf['loop'].add_data(row)
                            break

            else:

                if len(chainAssign1) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                if len(self.atomSelectionSet) < 1:
                    return

                comp_id = self.atomSelectionSet[0][0]['comp_id']
                atom_id = self.atomSelectionSet[0][0]['atom_id']

                atomId2 = self.csStat.getGeminalAtom(comp_id, atom_id)

                if atomId2 is None:
                    return

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.createSfDict:
                    sf = self.getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isIdenticalRestraint([atom1, atom2], self.nefT):
                        continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, None,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2)
                        sf['loop'].add_data(row)
                        break

                for p in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[p] if _split[p][0].isdecimal() else _split[p][1:])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

                    if len(chainAssign1) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                    if len(self.atomSelectionSet) < 1:
                        return

                    comp_id = self.atomSelectionSet[0][0]['comp_id']
                    atom_id = self.atomSelectionSet[0][0]['atom_id']

                    atomId2 = self.csStat.getGeminalAtom(comp_id, atom_id)

                    if atomId2 is None:
                        return

                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if isIdenticalRestraint([atom1, atom2], self.nefT):
                            continue
                        if self.debug:
                            print(f"subtype={self.cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                         '.', None, None,
                                         sf['list_id'], self.entryId, None,
                                         self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                         atom1, atom2)
                            sf['loop'].add_data(row)
                            break

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#declare_variable.
    def enterDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#declare_variable.
    def exitDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#set_variable.
    def enterSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#set_variable.
    def exitSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unset_variable.
    def enterUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#unset_variable.
    def exitUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#print_macro.
    def enterPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#print_macro.
    def exitPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def enterUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        if len(self.genSimpleNameSelection) == 0:
            return

        self.cur_resname_for_mapping = self.genSimpleNameSelection[0].upper()

        self.cur_comment_inlined = True

        self.genSimpleNameSelection.clear()

    # Exit a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def exitUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#mapping_list.
    def enterMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#mapping_list.
    def exitMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):
        atomName = str(ctx.Simple_name_MP(0)).upper()
        iupacName = set()

        i = 1
        while ctx.Simple_name_MP(i):
            iupacName.add(str(ctx.Simple_name_MP(i)).upper())
            i += 1

        if self.cur_resname_for_mapping in emptyValue:
            return

        if self.cur_resname_for_mapping not in self.unambigAtomNameMapping:
            self.unambigAtomNameMapping[self.cur_resname_for_mapping] = {}
        self.unambigAtomNameMapping[self.cur_resname_for_mapping][atomName] = list(iupacName)

    # Enter a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def enterAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        if len(self.genSimpleNameSelection) == 0:
            return

        self.cur_resname_for_mapping = self.genSimpleNameSelection[0].upper()

        self.cur_comment_inlined = True

        self.genSimpleNameSelection.clear()

    # Exit a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def exitAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.updateAmbigAtomNameMapping()

        self.cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#ambig_list.
    def enterAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#ambig_list.
    def exitAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):
        if ctx.Ambig_code_MP():
            ambigCode = str(ctx.Ambig_code_MP())
            i = 0
        else:
            ambigCode = str(ctx.Simple_name_MP(0)).upper()
            i = 1

        if self.hasCoord:
            mapName = []

            j = 0
            while ctx.Simple_name_MP(i):
                mapName.append({'atom_name': str(ctx.Simple_name_MP(i)).upper(),
                                'seq_id': int(str(ctx.Integer_MP(j)))})
                i += 1
                j += 1

            if self.cur_resname_for_mapping in emptyValue:
                return

            if self.cur_resname_for_mapping not in self.ambigAtomNameMapping:
                self.ambigAtomNameMapping[self.cur_resname_for_mapping] = {}
            self.ambigAtomNameMapping[self.cur_resname_for_mapping][ambigCode] = mapName

    # Enter a parse tree produced by CyanaMRParser#number.
    def enterNumber(self, ctx: CyanaMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#number.
    def exitNumber(self, ctx: CyanaMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Float_DecimalComma():
            self.numberSelection.append(float(str(ctx.Float_DecimalComma()).replace(',', '.', 1)))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by CyanaMRParser#gen_res_num.
    def enterGen_res_num(self, ctx: CyanaMRParser.Gen_res_numContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#gen_res_num.
    def exitGen_res_num(self, ctx: CyanaMRParser.Gen_res_numContext):
        if ctx.Integer():
            self.genResNumSelection.append((int(str(ctx.Integer())), None))

        elif ctx.Capital_integer():
            self.genResNumSelection.append((int(str(ctx.Capital_integer())[1:]), str(ctx.Capital_integer())[0]))

        elif ctx.Integer_capital():
            self.genResNumSelection.append((int(str(ctx.Integer_capital())[:-1]), str(ctx.Integer_capital())[-1]))

        else:
            self.genResNumSelection.append((None, None))

    # Enter a parse tree produced by CyanaMRParser#gen_simple_name.
    def enterGen_simple_name(self, ctx: CyanaMRParser.Gen_simple_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#gen_simple_name.
    def exitGen_simple_name(self, ctx: CyanaMRParser.Gen_simple_nameContext):
        if ctx.Simple_name():
            self.genSimpleNameSelection.append(str(ctx.Simple_name()))

        elif ctx.Capital_integer():
            self.genSimpleNameSelection.append(str(ctx.Capital_integer()))

        elif ctx.Integer_capital():
            self.genSimpleNameSelection.append(str(ctx.Integer_capital()))

        else:
            self.genSimpleNameSelection.append(None)

    # Enter a parse tree produced by CyanaMRParser#gen_atom_name.
    def enterGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#gen_atom_name.
    def exitGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):
        if ctx.Simple_name():
            self.genAtomNameSelection.append(str(ctx.Simple_name()))

        elif ctx.Capital_integer():
            self.genAtomNameSelection.append(str(ctx.Capital_integer()))

        elif ctx.Integer_capital():
            self.genAtomNameSelection.append(str(ctx.Integer_capital()))

        elif ctx.Ambig_code():
            self.genAtomNameSelection.append(str(ctx.Ambig_code()))

        else:
            self.genAtomNameSelection.append(None)

# del CyanaMRParser
