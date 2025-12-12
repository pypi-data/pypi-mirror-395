##
# File: BareMRParserListener.py
# Date: 02-Oct-2025
#
# Updates:
""" ParserLister class for Bare WSV/TSV/CSV MR files.
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
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.BareMRParser import BareMRParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isIdenticalRestraint,
                                                       hasInterChainRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       isLikePheOrTyr,
                                                       getRow,
                                                       getStarAtom,
                                                       resetCombinationId,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           emptyValue)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.BareMRParser import BareMRParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isIdenticalRestraint,
                                           hasInterChainRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           isLikePheOrTyr,
                                           getRow,
                                           getStarAtom,
                                           resetCombinationId,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getPotentialType,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               emptyValue)


# This class defines a complete listener for a parse tree produced by BareMRParser.
class BareMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ()

    # collection of any selection
    anySelection = []

    # collection of column name
    columnNameSelection = []

    __col_name = None
    __col_order = None

    __reduced_residue_name_pattern = re.compile(r'([A-Za-z]+)(\d+)')
    __rev_reduced_residue_name_pattern = re.compile(r'(\d+)([A-Za-z]+)')

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

        self.file_type = 'nm-res-bar'
        self.software_name = ''

    # Enter a parse tree produced by BareMRParser#bare_mr.
    def enterBare_mr(self, ctx: BareMRParser.Bare_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BareMRParser#bare_mr.
    def exitBare_mr(self, ctx: BareMRParser.Bare_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by BareMRParser#mr_row_format.
    def enterMr_row_format(self, ctx: BareMRParser.Mr_row_formatContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BareMRParser#mr_row_format.
    def exitMr_row_format(self, ctx: BareMRParser.Mr_row_formatContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BareMRParser#header.
    def enterHeader(self, ctx: BareMRParser.HeaderContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BareMRParser#header.
    def exitHeader(self, ctx: BareMRParser.HeaderContext):  # pylint: disable=unused-argument
        self.__col_name = []
        self.__col_order = []

        def register_column_info(col_name):
            self.__col_name.append(col_name)
            if 'RES' in col_name or 'SEQ' in col_name or 'COMP' in col_name or 'GROUP' in col_name or 'LABEL' in col_name:
                if 'COMP_ID' in col_name or 'NAME' in col_name or 'TYPE' in col_name or 'GROUP' in col_name or 'LABEL' in col_name:
                    self.__col_order.append('residue_name')
                else:
                    self.__col_order.append('sequence_code')
            elif 'CHAIN' in col_name or 'ASYM' in col_name or 'ENTITY' in col_name or 'CHN' in col_name:
                self.__col_order.append('chain_code')
            elif ('ATOM' in col_name or 'PROTON' in col_name) and 'TYPE' not in col_name and 'NUM' not in col_name:
                self.__col_order.append('atom_name')
            elif ('ID' in col_name or 'NUM' in col_name or 'INDEX' in col_name) and 'WIDTH' not in col_name:
                self.__col_order.append('index')
            elif ('TARGET' in col_name or 'CENTER' in col_name or 'MID' in col_name or 'DIST' in col_name or 'VALUE' in col_name)\
                    and 'ERR' not in col_name and 'UNCERT' not in col_name and 'UP' not in col_name and 'LOW' not in col_name\
                    and 'MAX' not in col_name and 'MIN' not in col_name:
                self.__col_order.append('target_value')
            elif 'ERR' in col_name or 'UNCERT' in col_name or 'DEV' in col_name or 'STD' in col_name\
                    or 'WIDTH' in col_name or 'WINDOW' in col_name or 'DELTA' in col_name:
                self.__col_order.append('value_uncertainty')
            elif 'UP' in col_name or 'MAX' in col_name and 'DST' not in col_name:
                self.__col_order.append('upper_limit')
            elif col_name.startswith('LO') or 'LOW' in col_name or 'MIN' in col_name and 'DST' not in col_name:
                self.__col_order.append('lower_limit')
            elif 'COMMENT' in col_name or 'DETAIL' in col_name or 'MEMO' in col_name:
                self.__col_order.append('details')
            elif 'WEIGHT' in col_name:
                self.__col_order.append('weight')
            elif 'PEAK' in col_name or 'RESONANCE' in col_name:
                self.__col_order.append('evidence')
            else:
                self.__col_order.append('unknown')

        for columnName in self.columnNameSelection:
            register_column_info(columnName.upper())

        self.columnNameSelection.clear()

        if self.__col_order.count('atom_name') == 2:
            self.cur_subtype = 'dist'
            self.distRestraints = 0

        if self.__col_order.count('atom_name') == 4:
            self.cur_subtype = 'dihed'
            self.dihedRestraints = 0

    # Enter a parse tree produced by BareMRParser#mr_row_list.
    def enterMr_row_list(self, ctx: BareMRParser.Mr_row_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BareMRParser#mr_row_list.
    def exitMr_row_list(self, ctx: BareMRParser.Mr_row_listContext):  # pylint: disable=unused-argument
        if self.cur_subtype == 'dist':
            self.exitDist_row_list()
        if self.cur_subtype == 'dihed':
            self.exitDihed_row_list()

    def exitDist_row_list(self):

        try:

            len_ord = len(self.__col_order)
            len_any = len(self.anySelection)

            if len_ord > len_any:
                return

            if self.distRestraints == 0:
                if len_ord + 1 == len_any:
                    if 'index' not in self.__col_order:
                        self.__col_order.insert(0, 'index')
                    else:
                        self.__col_order.insert(0, 'unknown')
                    self.__col_name.insert(0, 'N/A')
                    len_ord += 1

                elif len_ord + 2 == len_any and self.__col_name[0] == 'ATOM_I' and self.__col_name[1] == 'ATOM_J'\
                        and 'sequence_code' not in self.__col_order:
                    self.__col_order.insert(2, 'sequence_code')
                    self.__col_name.insert(2, 'RES_J')
                    self.__col_order.insert(1, 'sequence_code')
                    self.__col_name.insert(1, 'RES_I')
                    len_ord += 2

                elif self.__col_order.count('sequence_code') == 4 and self.__col_order.count('residue_name') == 0:
                    name_test = 0
                    for name, order in zip(self.__col_name, self.__col_order):
                        if order == 'sequence_code':
                            if 'NUM' in name or 'NM' in name or name.endswith('ID'):
                                continue
                            name_test += 1
                    if name_test == 2:
                        for idx, (name, order) in enumerate(zip(self.__col_name, self.__col_order)):
                            if order == 'sequence_code':
                                if 'NUM' in name or 'NM' in name or name.endswith('ID'):
                                    continue
                                self.__col_order[idx] = 'residue_name'

            if self.__col_order.count('sequence_code') != 2 or self.__col_order.count('atom_name') != 2\
               or ('target_value' not in self.__col_order and 'upper_limit' not in self.__col_order):
                return

            for col_type in ('chain_code', 'residue_name'):
                if col_type in self.__col_order and self.__col_order.count(col_type) != 2:
                    return

            for col_type in ('target_value', 'upper_limit', 'lower_limit'):
                if col_type in self.__col_order and self.__col_order.count(col_type) != 1:
                    return

            self.distRestraints += 1

            self.atomSelectionSet.clear()

            if not self.hasPolySeq:
                return

            chainIds, seqIds, compIds, atomIds = [], [], [], []
            target_value = value_uncertainty = lower_limit = upper_limit = None
            weight = 1.0

            for idx in range(len_any):
                if idx < len_ord:
                    order = self.__col_order[idx]
                    if order == 'chain_code':
                        if isinstance(self.anySelection[idx], str):
                            chainIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            chainIds.append(str(self.anySelection[idx]))
                    elif order == 'sequence_code':
                        if isinstance(self.anySelection[idx], int):
                            seqIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], str):
                            if self.__col_order.count('residue_name') == 0 and self.__reduced_residue_name_pattern.match(self.anySelection[idx]):
                                g = self.__reduced_residue_name_pattern.search(self.anySelection[idx]).groups()
                                seqIds.append(int(g[1]))
                                compId = g[0]
                                if len(compId) == 1:
                                    if self.polyPeptide and not self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        try:
                                            compId = next(k for k, v in monDict3.items() if v == compId)
                                        except StopIteration:
                                            pass
                                    elif not self.polyPeptide and self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        compId = 'D' + compId
                                compIds.append(compId)
                            elif self.__col_order.count('residue_name') == 0 and self.__rev_reduced_residue_name_pattern.match(self.anySelection[idx]):
                                g = self.__rev_reduced_residue_name_pattern.search(self.anySelection[idx]).groups()
                                seqIds.append(int(g[0]))
                                compId = g[1]
                                if len(compId) == 1:
                                    if self.polyPeptide and not self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        try:
                                            compId = next(k for k, v in monDict3.items() if v == compId)
                                        except StopIteration:
                                            pass
                                    elif not self.polyPeptide and self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        compId = 'D' + compId
                                compIds.append(compId)
                            else:
                                compIds.append(self.anySelection[idx])
                    elif order == 'residue_name':
                        if isinstance(self.anySelection[idx], str):
                            compIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            seqIds.append(self.anySelection[idx])
                    elif order == 'atom_name':
                        if isinstance(self.anySelection[idx], str):
                            atomIds.append(self.anySelection[idx])
                    elif order == 'target_value':
                        if isinstance(self.anySelection[idx], float):
                            target_value = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            target_value = float(self.anySelection[idx])
                    elif order == 'lower_limit':
                        if isinstance(self.anySelection[idx], float):
                            lower_limit = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            lower_limit = float(self.anySelection[idx])
                    elif order == 'upper_limit':
                        if isinstance(self.anySelection[idx], float):
                            upper_limit = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            upper_limit = float(self.anySelection[idx])
                    elif order == 'value_uncertainty':
                        if isinstance(self.anySelection[idx], float):
                            value_uncertainty = abs(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            value_uncertainty = float(self.anySelection[idx])
                    elif order == 'weight':
                        if isinstance(self.anySelection[idx], float):
                            weight = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            weight = float(self.anySelection[idx])

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The weight value '{weight}' must not be a negative value.")
                self.distRestraints -= 1
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The weight value '{weight}' should be a positive value.")

            if len(chainIds) not in (0, 2) or len(seqIds) != 2 or len(compIds) not in (0, 2)\
               or len(atomIds) != 2 or (target_value is None and upper_limit is None):
                self.distRestraints -= 1
                return

            chainId1 = chainId2 = seqId1 = seqId2 = compId1 = compId2 = atomId1 = atomId2 = None

            if len(chainIds) > 0:
                chainId1, chainId2 = chainIds[0], chainIds[1]

            seqId1, seqId2 = seqIds[0], seqIds[1]

            if len(compIds) > 0:
                compId1, compId2 = compIds[0], compIds[1]

            atomId1, atomId2 = atomIds[0], atomIds[1]

            if upper_limit is None and lower_limit is None and value_uncertainty is not None:
                upper_limit = target_value + value_uncertainty
                lower_limit = target_value - value_uncertainty

            self.retrieveLocalSeqScheme()

            if compId1 is not None:
                chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])\
                    if chainId1 is not None else self.assignCoordPolymerSequence(seqId1, compId1, atomId1.split('|', 1)[0])
            else:
                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1.split('|', 1)[0])\
                    if chainId1 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1.split('|', 1)[0])

            if compId2 is not None:
                chainAssign2, _ = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])\
                    if chainId2 is not None else self.assignCoordPolymerSequence(seqId2, compId2, atomId2.split('|', 1)[0])
            else:
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2.split('|', 1)[0])\
                    if chainId2 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2.split('|', 1)[0])

            if 0 in (len(chainAssign1), len(chainAssign2)):
                self.distRestraints -= 1
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                self.distRestraints -= 1
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

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, None, self.omitDistLimitOutlier)

            if dstFunc is None:
                self.distRestraints -= 1
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                sf['id'] += 1
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0

            if isinstance(combinationId, int):
                combinationId += 1
            if isinstance(memberId, int):
                memberId = 0
                _atom1 = _atom2 = None
            if self.createSfDict:
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'
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
                                 atom1, atom2)
                    sf['loop'].add_data(row)

                    if sf['constraint_subsubtype'] == 'ambi':
                        continue

                    if self.cur_constraint_type is not None and self.cur_constraint_type.startswith('ambiguous'):
                        sf['constraint_subsubtype'] = 'ambi'

                    if isinstance(combinationId, int)\
                       or (memberLogicCode == 'OR'
                           and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                                or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat))):
                        sf['constraint_subsubtype'] = 'ambi'

                    if 'upper_limit' in dstFunc and dstFunc['upper_limit'] is not None:
                        upperLimit = float(dstFunc['upper_limit'])
                        if upperLimit <= DIST_AMBIG_LOW or upperLimit >= DIST_AMBIG_UP:
                            sf['constraint_subsubtype'] = 'ambi'

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.anySelection.clear()

    def exitDihed_row_list(self):

        try:

            len_ord = len(self.__col_order)
            len_any = len(self.anySelection)

            if len_ord > len_any:
                return

            if self.dihedRestraints == 0:
                if len_ord + 1 == len_any:
                    if 'index' not in self.__col_order:
                        self.__col_order.insert(0, 'index')
                    else:
                        self.__col_order.insert(0, 'unknown')
                    self.__col_name.insert(0, 'N/A')
                    len_ord += 1

                elif len_ord + 4 == len_any and self.__col_name[0] == 'ATOM_I' and self.__col_name[1] == 'ATOM_J'\
                        and self.__col_name[2] == 'ATOM_K' and self.__col_name[3] == 'ATOM_L'\
                        and 'sequence_code' not in self.__col_order:
                    self.__col_order.insert(4, 'sequence_code')
                    self.__col_name.insert(4, 'RES_L')
                    self.__col_order.insert(3, 'sequence_code')
                    self.__col_name.insert(3, 'RES_K')
                    self.__col_order.insert(2, 'sequence_code')
                    self.__col_name.insert(2, 'RES_J')
                    self.__col_order.insert(1, 'sequence_code')
                    self.__col_name.insert(1, 'RES_I')
                    len_ord += 4

                elif self.__col_order.count('sequence_code') == 8 and self.__col_order.count('residue_name') == 0:
                    name_test = 0
                    for name, order in zip(self.__col_name, self.__col_order):
                        if order == 'sequence_code':
                            if 'NUM' in name or 'NM' in name or name.endswith('ID'):
                                continue
                            name_test += 1
                    if name_test == 4:
                        for idx, (name, order) in enumerate(zip(self.__col_name, self.__col_order)):
                            if order == 'sequence_code':
                                if 'NUM' in name or 'NM' in name or name.endswith('ID'):
                                    continue
                                self.__col_order[idx] = 'residue_name'

            if self.__col_order.count('sequence_code') != 4 or self.__col_order.count('atom_name') != 4\
               or ('target_value' not in self.__col_order and 'upper_limit' not in self.__col_order):
                return

            for col_type in ('chain_code', 'residue_name'):
                if col_type in self.__col_order and self.__col_order.count(col_type) != 4:
                    return

            for col_type in ('target_value', 'upper_limit', 'lower_limit'):
                if col_type in self.__col_order and self.__col_order.count(col_type) != 1:
                    return

            self.dihedRestraints += 1

            self.atomSelectionSet.clear()

            if not self.hasPolySeq:
                return

            chainIds, seqIds, compIds, atomIds = [], [], [], []
            target_value = value_uncertainty = lower_limit = upper_limit = None
            weight = 1.0

            for idx in range(len_any):
                if idx < len_ord:
                    order = self.__col_order[idx]
                    if order == 'chain_code':
                        if isinstance(self.anySelection[idx], str):
                            chainIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            chainIds.append(str(self.anySelection[idx]))
                    elif order == 'sequence_code':
                        if isinstance(self.anySelection[idx], int):
                            seqIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], str):
                            if self.__col_order.count('residue_name') == 0 and self.__reduced_residue_name_pattern.match(self.anySelection[idx]):
                                g = self.__reduced_residue_name_pattern.search(self.anySelection[idx]).groups()
                                seqIds.append(int(g[1]))
                                compId = g[0]
                                if len(compId) == 1:
                                    if self.polyPeptide and not self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        try:
                                            compId = next(k for k, v in monDict3.items() if v == compId)
                                        except StopIteration:
                                            pass
                                    elif not self.polyPeptide and self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        compId = 'D' + compId
                                compIds.append(compId)
                            elif self.__col_order.count('residue_name') == 0 and self.__rev_reduced_residue_name_pattern.match(self.anySelection[idx]):
                                g = self.__rev_reduced_residue_name_pattern.search(self.anySelection[idx]).groups()
                                seqIds.append(int(g[0]))
                                compId = g[1]
                                if len(compId) == 1:
                                    if self.polyPeptide and not self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        try:
                                            compId = next(k for k, v in monDict3.items() if v == compId)
                                        except StopIteration:
                                            pass
                                    elif not self.polyPeptide and self.polyDeoxyribonucleotide and not self.polyRibonucleotide:
                                        compId = 'D' + compId
                                compIds.append(compId)
                            else:
                                compIds.append(self.anySelection[idx])
                    elif order == 'residue_name':
                        if isinstance(self.anySelection[idx], str):
                            compIds.append(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            seqIds.append(self.anySelection[idx])
                    elif order == 'atom_name':
                        if isinstance(self.anySelection[idx], str):
                            atomIds.append(self.anySelection[idx])
                    elif order == 'target_value':
                        if isinstance(self.anySelection[idx], float):
                            target_value = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            target_value = float(self.anySelection[idx])
                    elif order == 'lower_limit':
                        if isinstance(self.anySelection[idx], float):
                            lower_limit = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            lower_limit = float(self.anySelection[idx])
                    elif order == 'upper_limit':
                        if isinstance(self.anySelection[idx], float):
                            upper_limit = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            upper_limit = float(self.anySelection[idx])
                    elif order == 'value_uncertainty':
                        if isinstance(self.anySelection[idx], float):
                            value_uncertainty = abs(self.anySelection[idx])
                        elif isinstance(self.anySelection[idx], int):
                            value_uncertainty = float(self.anySelection[idx])
                    elif order == 'weight':
                        if isinstance(self.anySelection[idx], float):
                            weight = self.anySelection[idx]
                        elif isinstance(self.anySelection[idx], int):
                            weight = float(self.anySelection[idx])

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The weight value '{weight}' must not be a negative value.")
                self.dihedRestraints -= 1
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The weight value '{weight}' should be a positive value.")

            if len(chainIds) not in (0, 4) or len(seqIds) != 4 or len(compIds) not in (0, 4)\
               or len(atomIds) != 4 or (target_value is None and upper_limit is None):
                self.dihedRestraints -= 1
                return

            chainId1 = chainId2 = chainId3 = chainId4 =\
                seqId1 = seqId2 = seqId3 = seqId4 =\
                compId1 = compId2 = compId3 = compId4 =\
                atomId1 = atomId2 = atomId3 = atomId4 = None

            if len(chainIds) > 0:
                chainId1, chainId2, chainId3, chainId4 = chainIds[0], chainIds[1], chainIds[2], chainIds[3]

            seqId1, seqId2, seqId3, seqId4 = seqIds[0], seqIds[1], seqIds[2], seqIds[3]

            if len(compIds) > 0:
                compId1, compId2, compId3, compId4 = compIds[0], compIds[1], compIds[2], compIds[3]

            atomId1, atomId2, atomId3, atomId4 = atomIds[0], atomIds[1], atomIds[2], atomIds[3]

            if upper_limit is None and lower_limit is None and value_uncertainty is not None:
                upper_limit = target_value + value_uncertainty
                lower_limit = target_value - value_uncertainty

            self.retrieveLocalSeqScheme()

            if compId1 is not None:
                chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)\
                    if chainId1 is not None else self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            else:
                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)\
                    if chainId1 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

            if compId2 is not None:
                chainAssign2, _ = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)\
                    if chainId2 is not None else self.assignCoordPolymerSequence(seqId2, compId2, atomId2)
            else:
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)\
                    if chainId2 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if compId3 is not None:
                chainAssign3, _ = self.assignCoordPolymerSequenceWithChainId(chainId3, seqId3, compId3, atomId3)\
                    if chainId3 is not None else self.assignCoordPolymerSequence(seqId3, compId3, atomId3)
            else:
                chainAssign3 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId3, seqId3, atomId3)\
                    if chainId3 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId3, atomId3)

            if compId4 is not None:
                chainAssign4, _ = self.assignCoordPolymerSequenceWithChainId(chainId4, seqId4, compId4, atomId4)\
                    if chainId4 is not None else self.assignCoordPolymerSequence(seqId4, compId4, atomId4)
            else:
                chainAssign4 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId4, seqId4, atomId4)\
                    if chainId4 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId4, atomId4)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
                self.dihedRestraints -= 1
                return

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                self.dihedRestraints -= 1
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtoms(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                self.areUniqueCoordAtoms('a dihedral angle')
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a dihedral angle',
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
                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))

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
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    sf['index_id'] += 1
                    if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                        dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                          dstFunc)
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, angleName,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.anySelection.clear()

    # Enter a parse tree produced by BareMRParser#any.
    def enterAny(self, ctx: BareMRParser.AnyContext):

        try:

            if ctx.Float():
                value = str(ctx.Float())
                self.anySelection.append(float(value))

            elif ctx.Integer():
                value = str(ctx.Integer())
                self.anySelection.append(int(value))

            elif ctx.Simple_name():
                self.anySelection.append(str(ctx.Simple_name()))

            elif ctx.Double_quote_float():
                value = str(ctx.Double_quote_float()).strip('"')
                self.anySelection.append(float(value))

            elif ctx.Double_quote_integer():
                value = str(ctx.Double_quote_integer()).strip('"')
                self.anySelection.append(int(value))

            else:
                self.anySelection.append(str(ctx.Double_quote_string()).strip('"'))

        except ValueError:
            self.anySelection.append(None)

    # Exit a parse tree produced by BareMRParser#any.
    def exitAny(self, ctx: BareMRParser.AnyContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BareMRParser#column_name.
    def enterColumn_name(self, ctx: BareMRParser.Column_nameContext):
        if ctx.Simple_name():
            self.columnNameSelection.append(str(ctx.Simple_name()))

        elif ctx.Double_quote_string():
            self.columnNameSelection.append(str(ctx.Double_quote_string()).strip('"'))

        else:
            self.columnNameSelection.append(str(ctx.Number_of_name()))

    # Exit a parse tree produced by BareMRParser#column_name.
    def exitColumn_name(self, ctx: BareMRParser.Column_nameContext):  # pylint: disable=unused-argument
        pass

# del BareMRParser
