##
# File: BiosymMRParserListener.py
# Date: 17-May-2022
#
# Updates:
""" ParserLister class for BIOSYM MR files.
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
from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.BiosymMRParser import BiosymMRParser
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
                                                       getDstFuncForHBond,
                                                       getDstFuncForSsBond,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import emptyValue
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.BiosymMRParser import BiosymMRParser
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
                                           getDstFuncForHBond,
                                           getDstFuncForSsBond,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import emptyValue


# This class defines a complete listener for a parse tree produced by BiosymMRParser.
class BiosymMRParserListener(ParseTreeListener, BaseLinearMRParserListener):
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

        self.file_type = 'nm-res-bio'
        self.software_name = 'BIOSYM'

    # Enter a parse tree produced by BiosymMRParser#biosym_mr.
    def enterBiosym_mr(self, ctx: BiosymMRParser.Biosym_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#biosym_mr.
    def exitBiosym_mr(self, ctx: BiosymMRParser.Biosym_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by BiosymMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: BiosymMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by BiosymMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: BiosymMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: BiosymMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: BiosymMRParser.Distance_restraintContext):

        try:

            chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # obs_value = self.numberSelection[2]
            weight = self.numberSelection[3]
            # weight_ub = self.numberSelection[4]
            # max_penalty = self.numberSelection[5]

            if not self.hasPolySeq and not self.hasNonPolySeq:
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
                return

            memberId = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
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

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by BiosymMRParser#distance_constraints.
    def enterDistance_constraints(self, ctx: BiosymMRParser.Distance_constraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by BiosymMRParser#distance_constraints.
    def exitDistance_constraints(self, ctx: BiosymMRParser.Distance_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#distance_constraint.
    def enterDistance_constraint(self, ctx: BiosymMRParser.Distance_constraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#distance_constraint.
    def exitDistance_constraint(self, ctx: BiosymMRParser.Distance_constraintContext):

        try:

            chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # max_penalty = self.numberSelection[4]

            if not self.hasPolySeq and not self.hasNonPolySeq:
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
                return

            memberId = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
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

        finally:
            self.numberSelection.clear()

    def __splitAtomSelectionExpr(self, atomSelection: str) -> Tuple[str, int, str, str]:  # pylint: disable=no-self-use
        """ Split BIOSYM atom selection expression.
        """

        try:

            atomSel = atomSelection.upper().split(':')

            chainId = int(atomSel[0])
            residue = atomSel[1].split('_')
            compId = residue[0]
            try:
                seqId = int(residue[1])
            except ValueError:
                seqId = int(''.join(c for c in residue[1] if c.isdigit()))
                chainId = ''.join(c for c in residue[1] if not c.isdigit())
                if len(chainId) == 0:
                    chainId = None
            atomId = atomSel[2]

            return chainId, seqId, compId, atomId

        except ValueError:
            return None, None, None, None

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_restraints.
    def enterDihedral_angle_restraints(self, ctx: BiosymMRParser.Dihedral_angle_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_restraints.
    def exitDihedral_angle_restraints(self, ctx: BiosymMRParser.Dihedral_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: BiosymMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: BiosymMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
            chainId3, seqId3, compId3, atomId3 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
            chainId4, seqId4, compId4, atomId4 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(3)))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            # cco = self.numberSelection[0]
            # cco_err = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # weught_max = self.numberSelection[4]

            if weight < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' must not be a negative value.")
                return
            if weight == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The relative weight value of '{weight}' should be a positive value.")

            target_value = None
            lower_limit = self.numberSelection[5]
            upper_limit = self.numberSelection[6]

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            dstFunc2 = dstFunc3 = dstFunc4 = None

            if len(self.numberSelection) > 8:
                lower_limit2 = self.numberSelection[7]
                upper_limit2 = self.numberSelection[8]

                dstFunc2 = self.validateAngleRange(weight, target_value, lower_limit2, upper_limit2)

            if len(self.numberSelection) > 10:
                lower_limit3 = self.numberSelection[9]
                upper_limit3 = self.numberSelection[10]

                dstFunc3 = self.validateAngleRange(weight, target_value, lower_limit3, upper_limit3)

            if len(self.numberSelection) > 12:
                lower_limit4 = self.numberSelection[11]
                upper_limit4 = self.numberSelection[12]

                dstFunc4 = self.validateAngleRange(weight, target_value, lower_limit4, upper_limit4)

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithChainId(chainId3, seqId3, compId3, atomId3)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithChainId(chainId4, seqId4, compId4, atomId4)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
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
                    _dstFunc = f"{dstFunc}"
                    if dstFunc2 is not None:
                        _dstFunc += f" {dstFunc2}"
                    if dstFunc3 is not None:
                        _dstFunc += f" {dstFunc3}"
                    if dstFunc4 is not None:
                        _dstFunc += f" {dstFunc4}"
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {_dstFunc}")
                if self.createSfDict and sf is not None:
                    if first_item:
                        sf['id'] += 1
                        first_item = False
                    sf['index_id'] += 1
                    if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                        dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                          dstFunc)
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId if dstFunc2 is None else 1, None, angleName,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                    sf['loop'].add_data(row)
                    if dstFunc2 is not None:
                        sf['index_id'] += 1
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                            dstFunc2 = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                               dstFunc2)
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     2, None, angleName,
                                     sf['list_id'], self.entryId, dstFunc2,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)
                    if dstFunc3 is not None:
                        sf['index_id'] += 1
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                            dstFunc3 = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                               dstFunc3)
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     3, None, angleName,
                                     sf['list_id'], self.entryId, dstFunc3,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)
                    if dstFunc4 is not None:
                        sf['index_id'] += 1
                        if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                            dstFunc4 = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                               dstFunc4)
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     4, None, angleName,
                                     sf['list_id'], self.entryId, dstFunc4,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4, asis1=asis1, asis2=asis2, asis3=asis3, asis4=asis4)
                        sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1 and dstFunc2 is None:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_constraints.
    def enterDihedral_angle_constraints(self, ctx: BiosymMRParser.Dihedral_angle_constraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_constraints.
    def exitDihedral_angle_constraints(self, ctx: BiosymMRParser.Dihedral_angle_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_constraint.
    def enterDihedral_angle_constraint(self, ctx: BiosymMRParser.Dihedral_angle_constraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_constraint.
    def exitDihedral_angle_constraint(self, ctx: BiosymMRParser.Dihedral_angle_constraintContext):  # pylint: disable=unused-argument

        try:

            chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
            chainId3, seqId3, compId3, atomId3 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
            chainId4, seqId4, compId4, atomId4 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(3)))

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # weught_max = self.numberSelection[4]

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

            self.retrieveLocalSeqScheme()

            chainAssign1, asis1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2, asis2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)
            chainAssign3, asis3 = self.assignCoordPolymerSequenceWithChainId(chainId3, seqId3, compId3, atomId3)
            chainAssign4, asis4 = self.assignCoordPolymerSequenceWithChainId(chainId4, seqId4, compId4, atomId4)

            if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4)):
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
                if peptide and angleName == 'CHI2' and atom4['atom_id'] == 'CD1' and isLikePheOrTyr(atom2['comp_id'], self.ccU):
                    dstFunc = self.selectRealisticChi2AngleConstraint(atom1, atom2, atom3, atom4,
                                                                      dstFunc)
                if self.debug:
                    print(f"subtype={self.cur_subtype} id={self.dihedRestraints} angleName={angleName} "
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

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by BiosymMRParser#chirality_constraints.
    def enterChirality_constraints(self, ctx: BiosymMRParser.Chirality_constraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by BiosymMRParser#chirality_constraints.
    def exitChirality_constraints(self, ctx: BiosymMRParser.Chirality_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#chirality_constraint.
    def enterChirality_constraint(self, ctx: BiosymMRParser.Chirality_constraintContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#chirality_constraint.
    def exitChirality_constraint(self, ctx: BiosymMRParser.Chirality_constraintContext):
        chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection()))

        chirality = str(ctx.Chiral_code())

        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        self.retrieveLocalSeqScheme()

        chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)

        if len(chainAssign1) == 0:
            return

        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)

        if len(self.atomSelectionSet) < 2:
            return

        if not self.areUniqueCoordAtoms('a chirality'):
            return

        if self.createSfDict:
            sf = self.getSf('BIOSYM chirality constraint')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'chirality',
                                      'list_id']

        for atom1 in self.atomSelectionSet[0]:
            if self.debug:
                print(f"subtype={self.cur_subtype} id={self.geoRestraints} "
                      f"atom={atom1} chirality={chirality}")
            if self.createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           chirality,
                                           sf['list_id']])

    # Enter a parse tree produced by BiosymMRParser#prochirality_constraints.
    def enterProchirality_constraints(self, ctx: BiosymMRParser.Prochirality_constraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by BiosymMRParser#prochirality_constraints.
    def exitProchirality_constraints(self, ctx: BiosymMRParser.Prochirality_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#prochirality_constraint.
    def enterProchirality_constraint(self, ctx: BiosymMRParser.Prochirality_constraintContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#prochirality_constraint.
    def exitProchirality_constraint(self, ctx: BiosymMRParser.Prochirality_constraintContext):
        chainId1, seqId1, compId1, atomId1 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
        chainId2, seqId2, compId2, atomId2 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
        chainId3, seqId3, compId3, atomId3 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
        chainId4, seqId4, compId4, atomId4 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(3)))
        chainId5, seqId5, compId5, atomId5 = self.__splitAtomSelectionExpr(str(ctx.Atom_selection(4)))

        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        self.retrieveLocalSeqScheme()

        chainAssign1, _ = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
        chainAssign2, _ = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)
        chainAssign3, _ = self.assignCoordPolymerSequenceWithChainId(chainId3, seqId3, compId3, atomId3)
        chainAssign4, _ = self.assignCoordPolymerSequenceWithChainId(chainId4, seqId4, compId4, atomId4)
        chainAssign5, _ = self.assignCoordPolymerSequenceWithChainId(chainId5, seqId5, compId5, atomId5)

        if 0 in (len(chainAssign1), len(chainAssign2), len(chainAssign3), len(chainAssign4), len(chainAssign5)):
            return

        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)
        self.selectCoordAtoms(chainAssign3, seqId3, compId3, atomId3, False)
        self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)
        self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)

        if len(self.atomSelectionSet) < 5:
            return

        if self.createSfDict:
            sf = self.getSf('BIOSYM prochirality constraint')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                      'auth_asym_id_4', 'auth_seq_id_4', 'auth_comp_id_4', 'auth_atom_id_4',
                                      'auth_asym_id_5', 'auth_seq_id_5', 'auth_comp_id_5', 'auth_atom_id_5',
                                      'list_id']

        for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                   self.atomSelectionSet[1],
                                                                   self.atomSelectionSet[2],
                                                                   self.atomSelectionSet[3],
                                                                   self.atomSelectionSet[4]):
            if self.debug:
                print(f"subtype={self.cur_subtype} id={self.geoRestraints} "
                      f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5}")
            if self.createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                           atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                           atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id'],
                                           atom5['chain_id'], atom5['seq_id'], atom5['comp_id'], atom5['atom_id'],
                                           sf['list_id']])

    # Enter a parse tree produced by BiosymMRParser#mixing_time.
    def enterMixing_time(self, ctx: BiosymMRParser.Mixing_timeContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#mixing_time.
    def exitMixing_time(self, ctx: BiosymMRParser.Mixing_timeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#number.
    def enterNumber(self, ctx: BiosymMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#number.
    def exitNumber(self, ctx: BiosymMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Float_DecimalComma():
            self.numberSelection.append(float(str(ctx.Float_DecimalComma()).replace(',', '.', 1)))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by BiosymMRParser#ins_distance_restraints.
    def enterIns_distance_restraints(self, ctx: BiosymMRParser.Ins_distance_restraintsContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dist'

    # Exit a parse tree produced by BiosymMRParser#ins_distance_restraints.
    def exitIns_distance_restraints(self, ctx: BiosymMRParser.Ins_distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#ins_distance_restraint.
    def enterIns_distance_restraint(self, ctx: BiosymMRParser.Ins_distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()
        self.insAtomSelection.clear()

    # Exit a parse tree produced by BiosymMRParser#ins_distance_restraint.
    def exitIns_distance_restraint(self, ctx: BiosymMRParser.Ins_distance_restraintContext):  # pylint: disable=unused-argument

        if len(self.insAtomSelection) != 2:
            self.distRestraints -= 1
            return

        chainId1, seqId1, atomId1 = self.insAtomSelection[0]
        chainId2, seqId2, atomId2 = self.insAtomSelection[1]

        target_value = None
        lower_limit = self.cur_lower_limit
        upper_limit = self.cur_upper_limit

        weight = 1.0

        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        self.retrieveLocalSeqScheme()

        if not any(True for ps in self.polySeq if ps['auth_chain_id'] == chainId1):
            chainId1 = None
        if not any(True for ps in self.polySeq if ps['auth_chain_id'] == chainId2):
            chainId2 = None

        chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1.split('|', 1)[0])
        chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2.split('|', 1)[0])

        if 0 in (len(chainAssign1), len(chainAssign2)):
            return

        self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
        self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

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

        dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, None, self.omitDistLimitOutlier)

        if dstFunc is None:
            atom1 = self.atomSelectionSet[0][0]
            atom2 = self.atomSelectionSet[1][0]

            dstFunc = getDstFuncForHBond(atom1, atom2) if atom1['atom_id'][0] != 'S' or atom2['atom_id'][1] != 'S' else getDstFuncForSsBond(atom1, atom2)

            try:
                if self.validateDistanceRange(float(dstFunc['weight']), None,
                                              float(dstFunc['lower_limit']),
                                              float(dstFunc['upper_limit']),
                                              None, self.omitDistLimitOutlier) is None:
                    return
            except (ValueError, TypeError):
                return

        memberId = '.'
        if self.createSfDict:
            sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                 self.csStat, self.originalFileName),
                            potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
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
                             atom1, atom2)
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

    # Enter a parse tree produced by BiosymMRParser#decl_create.
    def enterDecl_create(self, ctx: BiosymMRParser.Decl_createContext):
        if ctx.Double_quote_string(0):
            self.cur_ins_decl = str(ctx.Double_quote_string(0))

        if ctx.Double_quote_string(1):
            self.insAtomSelection.append(self.splitInsAtomSelectionExpr(str(ctx.Double_quote_string(1)).strip('"')))

        if ctx.Double_quote_string(2):
            self.insAtomSelection.append(self.splitInsAtomSelectionExpr(str(ctx.Double_quote_string(2)).strip('"')))

    # Exit a parse tree produced by BiosymMRParser#decl_create.
    def exitDecl_create(self, ctx: BiosymMRParser.Decl_createContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#decl_function.
    def enterDecl_function(self, ctx: BiosymMRParser.Decl_functionContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#decl_function.
    def exitDecl_function(self, ctx: BiosymMRParser.Decl_functionContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#decl_target.
    def enterDecl_target(self, ctx: BiosymMRParser.Decl_targetContext):
        if ctx.Double_quote_string(0):
            if str(ctx.Double_quote_string(0)) != self.cur_ins_decl:
                return

            if ctx.Relative():
                self.cur_upper_limit = None
                self.cur_lower_limit = None

            else:
                if ctx.Double_quote_string(1):
                    try:
                        self.cur_lower_limit = float(str(ctx.Double_quote_string(1)).strip('"'))
                    except (ValueError, TypeError):
                        pass

                if ctx.Double_quote_string(2):
                    try:
                        self.cur_upper_limit = float(str(ctx.Double_quote_string(2)).strip('"'))
                    except (ValueError, TypeError):
                        pass

    # Exit a parse tree produced by BiosymMRParser#decl_target.
    def exitDecl_target(self, ctx: BiosymMRParser.Decl_targetContext):  # pylint: disable=unused-argument
        pass

    def splitInsAtomSelectionExpr(self, atomSelection: str) -> Tuple[str, int, str]:  # pylint: disable=no-self-use
        """ Split Insight II atom selection expression.
        """

        try:

            atomSel = atomSelection.upper().split(':')

            return atomSel[0], int(atomSel[1]), atomSel[2]

        except (IndexError, ValueError, TypeError):
            return None, None, None

# del BiosymMRParser
