##
# File: AriaMRXParserListener.py
# Date: 01-Oct-2025
#
# Updates:
""" ParserLister class for ARIA MRX files.
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
    from wwpdb.utils.nmr.pk.XMLParser import XMLParser
    from wwpdb.utils.nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (translateToStdResName,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       isDefinedInterChainRestraint,
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
    from wwpdb.utils.nmr.AlignUtil import (MAX_MAG_IDENT_ASYM_ID,
                                           monDict3,
                                           emptyValue,
                                           indexToLetter,
                                           updatePolySeqRst,
                                           sortPolySeqRst,
                                           alignPolymerSequence,
                                           assignPolymerSequence)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.pk.XMLParser import XMLParser
    from nmr.mr.BaseLinearMRParserListener import BaseLinearMRParserListener
    from nmr.mr.ParserListenerUtil import (translateToStdResName,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           isDefinedInterChainRestraint,
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
    from nmr.AlignUtil import (MAX_MAG_IDENT_ASYM_ID,
                               monDict3,
                               emptyValue,
                               indexToLetter,
                               updatePolySeqRst,
                               sortPolySeqRst,
                               alignPolymerSequence,
                               assignPolymerSequence)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance)


# This class defines a complete listener for a parse tree produced by XMLParser.
class AriaMRXParserListener(ParseTreeListener, BaseLinearMRParserListener):
    __slots__ = ()

    __polySeqRstRef = None

    # current contributions
    __cur_contrib = []

    # weight of current contribution
    __cur_contrib_weight = None

    # collection of number selection in contributions
    __numberCSelection = []

    __cur_path = None

    __contribution_id = None

    __spin_system_id = None

    __segid = None
    __resid = None
    __name = None

    __restraint_key = None

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

        self.file_type = 'nm-res-arx'
        self.software_name = 'ARIA'

    # Enter a parse tree produced by XMLParser#document.
    def enterDocument(self, ctx: XMLParser.DocumentContext):  # pylint: disable=unused-argument
        self.__cur_path = ''
        self.__polySeqRstRef = []

    # Exit a parse tree produced by XMLParser#document.
    def exitDocument(self, ctx: XMLParser.DocumentContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by XMLParser#prolog.
    def enterProlog(self, ctx: XMLParser.PrologContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XMLParser#prolog.
    def exitProlog(self, ctx: XMLParser.PrologContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XMLParser#content.
    def enterContent(self, ctx: XMLParser.ContentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XMLParser#content.
    def exitContent(self, ctx: XMLParser.ContentContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XMLParser#element.
    def enterElement(self, ctx: XMLParser.ElementContext):
        self.__cur_path += '/' + str(ctx.Name(0))

        # noe_restraint_list
        if self.__cur_path == '/noe_restraint_list':
            self.cur_subtype = 'dist'
            self.__restraint_key = None

        elif self.__cur_path == '/noe_restraint_list/peak':
            self.cur_weight = None
            self.cur_target_value = None
            self.cur_lower_limit = None
            self.cur_upper_limit = None
            self.__contribution_id = -1
            self.__cur_contrib = []

        elif self.__cur_path == '/noe_restraint_list/peak/contribution':
            self.__cur_contrib_weight = None
            self.__contribution_id += 1
            self.__spin_system_id = -1
            self.__cur_contrib.append([])

        elif self.__cur_path == '/noe_restraint_list/peak/contribution/spin_system':
            self.__spin_system_id += 1
            self.__cur_contrib[self.__contribution_id].append([])

        elif self.__cur_path == '/noe_restraint_list/peak/contribution/spin_system/atom':
            self.__segid = None
            self.__resid = None
            self.__name = None

        # data_set
        elif self.__cur_path == '/data_set/sequence':
            self.__restraint_key = None

        elif self.__cur_path == '/data_set/sequence/residue':
            self.__resid = None
            self.__name = None

        elif self.__cur_path == '/data_set/restraint_list':
            self.cur_subtype = 'dist'
            self.__restraint_key = None

        elif self.__cur_path == '/data_set/restraint_list/restraint':
            self.cur_weight = 1.0  # default
            self.cur_target_value = None
            self.cur_lower_limit = None
            self.cur_upper_limit = None
            self.__contribution_id = -1
            self.__cur_contrib = []

        elif self.__cur_path == '/data_set/restraint_list/restraint/contribution':
            self.__cur_contrib_weight = 1.0  # default
            self.__contribution_id += 1
            self.__cur_contrib.append([])
            self.__spin_system_id = -1

        elif self.__cur_path == '/data_set/restraint_list/restraint/contribution/atom':
            self.__segid = None
            self.__resid = None
            self.__name = None

        elif self.__cur_path == '/data_set/torsion_angles':
            self.cur_subtype = 'dihed'
            self.__restraint_key = None

        elif self.__cur_path == '/data_set/torsion_angles/torsion_angle':
            self.cur_weight = 1.0  # default
            self.__segid = None
            self.__resid = None
            self.__name = None
            self.cur_target_value = None
            self.cur_target_value_uncertainty = None

    # Exit a parse tree produced by XMLParser#element.
    def exitElement(self, ctx: XMLParser.ElementContext):

        try:

            if self.__cur_path in ('/noe_restraint_list/peak', '/data_set/restraint_list/restraint'):

                if self.cur_weight <= 0.0:
                    return

                del_contrib_id = []

                for contrib_id, contrib in enumerate(self.__cur_contrib):
                    valid = True
                    for spin_system_id, spin_system in enumerate(contrib):
                        if any(atom is None or atom['weight'] <= 0.0 for atom in spin_system):
                            valid = False
                            break
                        if len(spin_system) > 1:
                            ref_atom = spin_system[0]
                            has_chain_id = 'chain_id' in ref_atom
                            for atom in spin_system[1:]:
                                if ref_atom['seq_id'] != atom['seq_id']\
                                   or ref_atom['atom_id'][0] != atom['atom_id'][0]\
                                   or (has_chain_id and ref_atom['chain_id'] != atom['chain_id']):
                                    valid = False
                                    break
                            if valid:
                                self.__cur_contrib[contrib_id][spin_system_id][0]['atom_id'] = self.extractCommonAtomName(spin_system)

                    if not valid or len(contrib) != 2:
                        del_contrib_id.append(contrib_id)

                if len(del_contrib_id) > 0:
                    for contrib_id in reversed(del_contrib_id):
                        del self.__cur_contrib[contrib_id]

                if len(self.__cur_contrib) == 0:
                    return

                self.distRestraints += 1

                self.atomSelectionSet.clear()

                self.exitDistance_restraint()

            elif self.__cur_path == '/noe_restraint_list/peak/contribution/spin_system/atom':
                if self.__cur_contrib_weight is not None:
                    atom = {'weight': self.__cur_contrib_weight}
                    if self.__resid is not None:
                        atom['seq_id'] = self.__resid
                        if self.__name is not None:
                            atom['atom_id'] = self.__name
                            if self.__segid is not None:
                                atom['chain_id'] = self.__segid
                        else:
                            atom = None
                    else:
                        atom = None
                else:
                    atom = None

                self.__cur_contrib[self.__contribution_id][self.__spin_system_id].append(atom)

            elif self.__cur_path == '/data_set/restraint_list/restraint/contribution/atom':
                if self.__cur_contrib_weight is not None:
                    atom = {'weight': self.__cur_contrib_weight}
                    if self.__resid is not None:
                        atom['seq_id'] = self.__resid
                        if self.__name is not None:
                            atom['atom_id'] = self.__name
                            if self.__segid is not None:
                                atom['chain_id'] = self.__segid
                        else:
                            atom = None
                    else:
                        atom = None
                else:
                    atom = None

                self.__spin_system_id += 1
                self.__cur_contrib[self.__contribution_id].append([])

                self.__cur_contrib[self.__contribution_id][self.__spin_system_id].append(atom)

            elif self.__cur_path == '/data_set/torsion_angles/torsion_angle':

                if self.cur_weight <= 0.0 or None in (self.__resid, self.__name, self.cur_target_value):
                    return

                self.dihedRestraints += 1

                self.atomSelectionSet.clear()

                self.exitTorsion_angle_restraint()

            elif self.__cur_path == '/data_set/sequence':
                sortPolySeqRst(self.__polySeqRstRef)

                seqAlign, _ = alignPolymerSequence(self.pA, self.polySeq, self.__polySeqRstRef, resolvedMultimer=self.reasons is not None)
                chainAssign, _ = assignPolymerSequence(self.pA, self.ccU, self.file_type, self.polySeq, self.__polySeqRstRef, seqAlign)

                if chainAssign is not None and len(chainAssign) > 0:
                    for ca in chainAssign:
                        ref_chain_id = ca['ref_chain_id']
                        test_chain_id = ca['test_chain_id']

                        sa = next(sa for sa in seqAlign
                                  if sa['ref_chain_id'] == ref_chain_id
                                  and sa['test_chain_id'] == test_chain_id)

                        if sa['conflict'] != 0:
                            continue

                        poly_seq_model = next(ps for ps in self.polySeq
                                              if ps['auth_chain_id'] == ref_chain_id)
                        poly_seq_rst = next(ps for ps in self.__polySeqRstRef
                                            if ps['chain_id'] == test_chain_id)

                        if 'auth_seq_id' in poly_seq_rst:
                            continue

                        seq_id_mapping = {}
                        offset = None
                        for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                            if test_seq_id is None:
                                continue
                            if mid_code == '|':
                                try:
                                    seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                       in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                       if seq_id == ref_seq_id and isinstance(auth_seq_id, int))
                                    if offset is None:
                                        offset = seq_id_mapping[test_seq_id] - test_seq_id
                                except StopIteration:
                                    pass
                            elif mid_code == ' ' and test_seq_id in poly_seq_rst['seq_id']:
                                idx = poly_seq_rst['seq_id'].index(test_seq_id)
                                if poly_seq_rst['comp_id'][idx] == '.' and poly_seq_rst['auth_comp_id'][idx] not in emptyValue:
                                    seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                       in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                       if seq_id == ref_seq_id and isinstance(auth_seq_id, int))

                        if offset is not None and all(v - k == offset for k, v in seq_id_mapping.items()):
                            poly_seq_rst['auth_seq_id'] = [seq_id + offset for seq_id in poly_seq_rst['seq_id']]

            elif self.__cur_path == '/data_set/sequence/residue':

                if self.__restraint_key is None:
                    self.__restraint_key = indexToLetter(len(self.__polySeqRstRef))

                if None in (self.__resid, self.__name):
                    return

                updatePolySeqRst(self.__polySeqRstRef, self.__restraint_key, self.__resid, self.__name)

        finally:
            self.__cur_path = self.__cur_path[:-(1 + len(str(ctx.Name(0))))]

    # Enter a parse tree produced by XMLParser#reference.
    def enterReference(self, ctx: XMLParser.ReferenceContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XMLParser#reference.
    def exitReference(self, ctx: XMLParser.ReferenceContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XMLParser#attribute.
    def enterAttribute(self, ctx: XMLParser.AttributeContext):

        if ctx.Name() and ctx.STRING():
            name = str(ctx.Name())
            string = str(ctx.STRING())[1:-1].strip()

            try:

                if self.__cur_path in ('/noe_restraint_list/peak', '/data_set/restraint_list/restraint'):

                    if name == 'weight':
                        self.cur_weight = float(string)

                    elif name == 'distance':
                        self.cur_target_value = float(string)

                    elif name in ('lower_bound', 'lower'):
                        self.cur_lower_limit = float(string)

                    elif name in ('upper_bound', 'upper'):
                        self.cur_upper_limit = float(string)

                elif self.__cur_path == '/noe_restraint_list/peak/contribution':

                    if name == 'weight':
                        self.__cur_contrib_weight = float(string)

                elif self.__cur_path in ('/noe_restraint_list/peak/contribution/spin_system/atom', '/data_set/restraint_list/restraint/contribution/atom'):

                    if name == 'segid' and len(string) > 0:
                        self.__segid = string

                    elif name == 'residue' and len(string) > 0 and string.isdigit():
                        self.__resid = int(string)

                    elif name == 'name' and len(string) > 0:
                        self.__name = string

                elif self.__cur_path in ('/data_set/restraint_list', '/data_set/torsion_angles'):

                    if name == 'key' and len(string) > 0:
                        self.__restraint_key = string

                elif self.__cur_path == '/data_set/torsion_angles/torsion_angle':

                    if name == 'segid' and len(string) > 0:
                        self.__segid = string

                    elif name == 'residue_number' and len(string) > 0 and string.isdigit():
                        self.__resid = int(string)

                    elif name == 'name' and len(string) > 0:
                        self.__name = string

                    elif name == 'value' and len(string) > 0:
                        self.cur_target_value = float(string)

                    elif name == 'error' and len(string) > 0:
                        self.cur_target_value_uncertainty = float(string)

                elif self.__cur_path == '/data_set/sequence':

                    if name == 'name' and len(string) > 0:
                        self.__restraint_key = string

                elif self.__cur_path == '/data_set/sequence/residue':

                    if name == 'number' and len(string) > 0 and string.isdigit():
                        self.__resid = int(string)

                    elif name == 'name' and len(string) > 0:
                        self.__name = string

            except ValueError:
                pass

    # Exit a parse tree produced by XMLParser#attribute.
    def exitAttribute(self, ctx: XMLParser.AttributeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XMLParser#chardata.
    def enterChardata(self, ctx: XMLParser.ChardataContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XMLParser#chardata.
    def exitChardata(self, ctx: XMLParser.ChardataContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by XMLParser#misc.
    def enterMisc(self, ctx: XMLParser.MiscContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by XMLParser#misc.
    def exitMisc(self, ctx: XMLParser.MiscContext):  # pylint: disable=unused-argument
        pass

    def extractCommonAtomName(self, atom_sel: List[dict]) -> str:

        if len(atom_sel) == 0:
            return None

        ref_atom_id = atom_sel[0]['atom_id']

        if len(atom_sel) == 1:
            return ref_atom_id

        strings = [a['atom_id'] for a in atom_sel]

        min_str = min(strings, key=len)
        max_str = max(strings, key=len)

        len_min_str = len(min_str)
        len_max_str = len(max_str)
        longest_substr = ''

        for i in range(len_min_str):
            for j in range(i + 1, len_min_str + 1):
                substr = min_str[i:j]
                if all(substr in s for s in strings):
                    if len(substr) > len(longest_substr):
                        longest_substr = substr

        if len(longest_substr) == 0:
            return ref_atom_id

        self.pA.setReferenceSequence(list(longest_substr), 'REFNAME')
        self.pA.addTestSequence(list(max_str), 'NAME')
        self.pA.doAlign()

        myAlign = self.pA.getAlignment('NAME')

        length = len(myAlign)

        if length == 0:
            return ref_atom_id

        common_name = []

        for i in range(length):
            myPr = myAlign[i]
            myPr0 = str(myPr[0])
            myPr1 = str(myPr[1])
            if myPr0 == myPr1:
                if myPr0 not in emptyValue:
                    common_name.append(myPr0)
            elif myPr0 in emptyValue:
                if myPr1 not in emptyValue:
                    common_name.append(('#' if myPr1.isdigit() else '%') if len_min_str == len_max_str else '*')

        if len(common_name) == 0:
            return ref_atom_id

        common_name = ''.join(common_name)

        while '##' in common_name:
            common_name = common_name.replace('##', '*')

        while '%%' in common_name:
            common_name = common_name.replace('%%', '*')

        while '*%' in common_name:
            common_name = common_name.replace('*%', '*')

        while '%*' in common_name:
            common_name = common_name.replace('%*', '*')

        while '**' in common_name:
            common_name = common_name.replace('**', '*')

        return common_name

    def exitDistance_restraint(self):

        try:

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            total = 0

            for atom_pair in self.__cur_contrib:

                chainId1 = atom_pair[0][0]['chain_id'] if 'chain_id' in atom_pair[0][0] else None
                seqId1 = atom_pair[0][0]['seq_id']
                atomId1 = atom_pair[0][0]['atom_id']

                compId1 = None
                if len(self.__polySeqRstRef) > 0:
                    if chainId1 is None:
                        chainId1 = self.__polySeqRstRef[0]['chain_id']
                    ps = next((ps for ps in self.__polySeqRstRef if ps['chain_id'] == chainId1), None)
                    if ps is not None and seqId1 in ps['seq_id']:
                        compId1 = ps['comp_id'][ps['seq_id'].index(seqId1)]
                        if 'auth_seq_id' in ps:
                            seqId1 = ps['auth_seq_id'][ps['seq_id'].index(seqId1)]

                if compId1 is not None:
                    chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1.split('|', 1)[0])\
                        if chainId1 is not None else self.assignCoordPolymerSequence(seqId1, compId1, atomId1.split('|', 1)[0])
                else:
                    chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1.split('|', 1)[0])\
                        if chainId1 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1.split('|', 1)[0])

                chainId2 = atom_pair[1][0]['chain_id'] if 'chain_id' in atom_pair[1][0] else None
                seqId2 = atom_pair[1][0]['seq_id']
                atomId2 = atom_pair[1][0]['atom_id']

                compId2 = None
                if len(self.__polySeqRstRef) > 0:
                    if chainId2 is None:
                        chainId2 = self.__polySeqRstRef[0]['chain_id']
                    ps = next((ps for ps in self.__polySeqRstRef if ps['chain_id'] == chainId2), None)
                    if ps is not None and seqId2 in ps['seq_id']:
                        compId2 = ps['comp_id'][ps['seq_id'].index(seqId2)]
                        if 'auth_seq_id' in ps:
                            seqId2 = ps['auth_seq_id'][ps['seq_id'].index(seqId2)]

                if compId2 is not None:
                    chainAssign2, _ = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2.split('|', 1)[0])\
                        if chainId2 is not None else self.assignCoordPolymerSequence(seqId2, compId2, atomId2.split('|', 1)[0])
                else:
                    chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2.split('|', 1)[0])\
                        if chainId2 is not None else self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2.split('|', 1)[0])

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

                dstFunc = self.validateDistanceRange(self.cur_weight, self.cur_target_value, self.cur_lower_limit, self.cur_upper_limit,
                                                     None, self.omitDistLimitOutlier)

                if dstFunc is None:
                    return

                total += 1

            if total == 0:
                return

            if self.__restraint_key is not None and 'inter' in self.__restraint_key:
                if self.exptlMethod == 'SOLID-STATE NMR':
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId1 and 'identical_auth_chain_id' in ps), None)
                    if ps is not None:
                        chain_id_set = [chainId1]
                        chain_id_set.extend(ps['identical_auth_chain_id'])
                        chain_id_set.sort()
                        if self.symmetric != 'no':
                            pass
                        elif len(chain_id_set) > MAX_MAG_IDENT_ASYM_ID and chainId2 in chain_id_set:
                            self.symmetric = 'linear'

                            try:

                                _head =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': chain_id_set[0]},
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
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': chain_id_set[-1]},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': seq_id_1},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': atom_id_1},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_head) == 1 and len(_tail) == 1:
                                    if distance(to_np_array(_head[0]), to_np_array(_tail[0])) < 10.0:
                                        self.symmetric = 'circular'

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.__class_name__}.exitDistance_restraint() ++ Error  - {str(e)}")

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                sf['id'] += 1
                if len(self.__cur_contrib) > 1:
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
                for atom1, atom2 in itertools.product(self.atomSelectionSet[i],
                                                      self.atomSelectionSet[i + 1]):
                    atoms = [atom1, atom2]
                    if self.__restraint_key is not None and isDefinedInterChainRestraint(atoms, self.__restraint_key, self.symmetric, self.polySeq):
                        continue
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
                        print(f"subtype={self.cur_subtype} comment={self.__restraint_key} id={self.distRestraints} "
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

            if self.createSfDict and sf is not None and isinstance(memberId, int) and memberId == 1:
                sf['loop'].data[-1] = resetMemberId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    def exitTorsion_angle_restraint(self):

        try:

            seqId = self.__resid
            angleName = self.__name.upper()

            if self.__segid is None and len(self.__polySeqRstRef) > 0:
                self.__segid = self.__polySeqRstRef[0]['chain_id']

            ps = next((ps for ps in self.__polySeqRstRef if ps['chain_id'] == self.__segid), None)

            if ps is None or seqId not in ps['seq_id']:
                self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                              f"'Residue number '{self.__resid}' is not defined in /data_set/sequence XML element.")
                self.dihedRestraints -= 1
                return

            _compId = ps['comp_id'][ps['seq_id'].index(seqId)].upper()
            compId = translateToStdResName(_compId, ccU=self.ccU)
            if _compId != compId:
                _types = self.csStat.getTypeOfCompId(_compId)
                if any(t for t in _types) and _types != self.csStat.getTypeOfCompId(compId):
                    compId = _compId

            if 'auth_seq_id' in ps:
                seqId = ps['auth_seq_id'][ps['seq_id'].index(seqId)]

            target_value = self.cur_target_value
            lower_limit = self.cur_target_value - self.cur_target_value_uncertainty
            upper_limit = self.cur_target_value + self.cur_target_value_uncertainty

            weight = self.cur_weight

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

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
                                  f"The angle identifier {self.__name!r} is unknown for the residue {_compId!r}, "
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
                                      f"The angle identifier {self.__name!r} is unknown for the residue {_compId!r}, "
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
                                                  f"The angle identifier {self.__name!r} is unknown for the residue {_compId!r}.")
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
                                      f"The angle identifier {self.__name!r} did not match with residue {_compId!r}.")
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
                                                  f"The angle identifier {self.__name!r} is unknown for the residue {_compId!r}.")
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

        except ValueError:
            self.dihedRestraints -= 1

        finally:
            self.numberSelection.clear()
