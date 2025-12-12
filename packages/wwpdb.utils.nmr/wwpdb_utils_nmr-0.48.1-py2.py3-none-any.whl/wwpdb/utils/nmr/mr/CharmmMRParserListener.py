##
# File: CharmmMRParserListener.py
# Date: 21-Sep-2022
#
# Updates:
""" ParserLister class for CHARMM MR files.
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
from rmsd.calculate_rmsd import (int_atom, ELEMENT_WEIGHTS)  # noqa: F401 pylint: disable=no-name-in-module, import-error
from operator import itemgetter
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.CharmmMRParser import CharmmMRParser
    from wwpdb.utils.nmr.mr.BaseStackedMRParserListener import BaseStackedMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx,
                                                       translateToStdAtomName,
                                                       hasInterChainRestraint,
                                                       isIdenticalRestraint,
                                                       isDefinedSegmentRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       contentSubtypeOf,
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
                                                       CARTN_DATA_ITEMS,
                                                       AUTH_ATOM_DATA_ITEMS,
                                                       ATOM_NAME_DATA_ITEMS,
                                                       AUTH_ATOM_CARTN_DATA_ITEMS,
                                                       PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                       PTNR2_AUTH_ATOM_DATA_ITEMS,
                                                       NMR_STAR_LP_KEY_ITEMS)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (emptyValue,
                                           deepcopy)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.CharmmMRParser import CharmmMRParser
    from nmr.mr.BaseStackedMRParserListener import BaseStackedMRParserListener
    from nmr.mr.ParserListenerUtil import (toRegEx,
                                           hasInterChainRestraint,
                                           isIdenticalRestraint,
                                           isDefinedSegmentRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           contentSubtypeOf,
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
                                           CARTN_DATA_ITEMS,
                                           AUTH_ATOM_DATA_ITEMS,
                                           ATOM_NAME_DATA_ITEMS,
                                           AUTH_ATOM_CARTN_DATA_ITEMS,
                                           PTNR1_AUTH_ATOM_DATA_ITEMS,
                                           PTNR2_AUTH_ATOM_DATA_ITEMS,
                                           NMR_STAR_LP_KEY_ITEMS)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (emptyValue,
                               deepcopy)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance)


# This class defines a complete listener for a parse tree produced by CharmmMRParser.
class CharmmMRParserListener(ParseTreeListener, BaseStackedMRParserListener):
    __slots__ = ('__atomNumberDict', )

    # distance
    kMin = 0.0
    kMax = 0.0
    rMin = 0.0
    rMax = None
    fMax = None
    # tCon = 0.0
    rExp = -1.0 / 6.0

    # dihedral angle
    force = None
    min = None
    width = None
    period = 0

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

        self.file_type = 'nm-res-cha'
        self.software_name = 'CHARMM'

        if atomNumberDict is not None:
            self.__atomNumberDict = atomNumberDict
            self.offsetHolder = None

        else:
            self.__atomNumberDict = {}

    # Enter a parse tree produced by CharmmMRParser#charmm_mr.
    def enterCharmm_mr(self, ctx: CharmmMRParser.Charmm_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#charmm_mr.
    def exitCharmm_mr(self, ctx: CharmmMRParser.Charmm_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by CharmmMRParser#comment.
    def enterComment(self, ctx: CharmmMRParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#comment.
    def exitComment(self, ctx: CharmmMRParser.CommentContext):
        comment = []
        for col in range(20):
            if ctx.Any_name(col):
                text = str(ctx.Any_name(col))
                if text[0] in ('#', '!'):
                    break
                comment.append(str(ctx.Any_name(col)))
            else:
                break
        self.lastComment = None if len(comment) == 0 else ' '.join(comment)

    # Enter a parse tree produced by CharmmMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CharmmMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        self.noeAverage = 'r-6'  # default averaging method
        self.squareExponent = 1.0
        self.rSwitch = None
        self.scale = 1.0
        self.kMin = 0.0
        self.kMax = 0.0
        self.rMin = 0.0
        self.rMax = None
        self.fMax = None
        # self.tCon = 0.0
        self.rExp = -1.0 / 6.0

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CharmmMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CharmmMRParser.Distance_restraintContext):  # pylint: disable=unused-argument

        try:

            target_value = None
            lower_limit = self.rMin
            upper_limit = self.rMax
            lower_linear_limit = None
            upper_linear_limit = None

            if self.fMax is not None and self.fMax > 0.0 and self.kMax > 0.0:
                upper_linear_limit = self.rMax + self.fMax / self.kMax
            if self.rSwitch is not None:
                upper_linear_limit = self.rMax + self.rSwitch

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

            dstFunc = self.validateDistanceRange(self.scale,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit,
                                                 self.squareExponent if self.rSwitch is not None else 1.0)

            if dstFunc is None:
                return

            if 0 in (len(self.atomSelectionSet[0]), len(self.atomSelectionSet[1])):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
                sf['id'] += 1
                memberLogicCode = 'OR' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else '.'
                if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1\
                   and (isAmbigAtomSelection(self.atomSelectionSet[0], self.csStat)
                        or isAmbigAtomSelection(self.atomSelectionSet[1], self.csStat)):
                    memberId = 0
                    _atom1 = _atom2 = None
                len_keys = len(NMR_STAR_LP_KEY_ITEMS[contentSubtypeOf(self.cur_subtype)])

            if self.reasons is None\
               and 'segment_id' in self.atomSelectionSet[0][0] and 'segment_id' in self.atomSelectionSet[1][0]\
               and self.atomSelectionSet[0][0]['segment_id'] != self.atomSelectionSet[1][0]['segment_id']\
               and 'assert_uniq_segment_id' not in self.reasonsForReParsing:
                self.reasonsForReParsing['assert_uniq_segment_id'] = True
            assert_uniq_segment_id = self.reasons is not None and 'assert_uniq_segment_id' in self.reasons

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
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
                if self.debug:
                    print(f"subtype={self.cur_subtype} (NOE) id={self.distRestraints} "
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
                    if any(True for _dat in row[1:len_keys] if _dat is None):
                        sf['index_id'] -= 1
                        continue
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

            if self.createSfDict:
                self.trimSfWoLp()

    # Enter a parse tree produced by CharmmMRParser#point_distance_restraint.
    def enterPoint_distance_restraint(self, ctx: CharmmMRParser.Point_distance_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#point_distance_restraint.
    def exitPoint_distance_restraint(self, ctx: CharmmMRParser.Point_distance_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: CharmmMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'dihed'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CharmmMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: CharmmMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            target_value = self.min
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            dstFunc = self.validateAngleRange(1.0, {'force': self.force, 'period': self.period},
                                              target_value, lower_limit, upper_limit,
                                              lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if len(self.atomSelectionSet) != 4:
                return

            try:
                compId = self.atomSelectionSet[0][0]['comp_id']
                peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
            except IndexError:
                if not self.areUniqueCoordAtoms('a dihedral angle (DIHE)'):
                    if len(self.g) > 0:
                        self.f.extend(self.g)
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a dihedral angle (DIHE)',
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
                len_keys = len(NMR_STAR_LP_KEY_ITEMS[contentSubtypeOf(self.cur_subtype)])

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
                    print(f"subtype={self.cur_subtype} (DIHE) id={self.dihedRestraints} angleName={angleName} "
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
                    if any(True for _dat in row[1:len_keys] if _dat is None):
                        sf['index_id'] -= 1
                        continue
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

            if self.createSfDict:
                self.trimSfWoLp()

    # Enter a parse tree produced by CharmmMRParser#harmonic_restraint.
    def enterHarmonic_restraint(self, ctx: CharmmMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#harmonic_restraint.
    def exitHarmonic_restraint(self, ctx: CharmmMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#manipulate_internal_coordinate.
    def enterManipulate_internal_coordinate(self, ctx: CharmmMRParser.Manipulate_internal_coordinateContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#manipulate_internal_coordinate.
    def exitManipulate_internal_coordinate(self, ctx: CharmmMRParser.Manipulate_internal_coordinateContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#droplet_potential.
    def enterDroplet_potential(self, ctx: CharmmMRParser.Droplet_potentialContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#droplet_potential.
    def exitDroplet_potential(self, ctx: CharmmMRParser.Droplet_potentialContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_atom_constraint.
    def enterFix_atom_constraint(self, ctx: CharmmMRParser.Fix_atom_constraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#fix_atom_constraint.
    def exitFix_atom_constraint(self, ctx: CharmmMRParser.Fix_atom_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#center_of_mass_constraint.
    def enterCenter_of_mass_constraint(self, ctx: CharmmMRParser.Center_of_mass_constraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#center_of_mass_constraint.
    def exitCenter_of_mass_constraint(self, ctx: CharmmMRParser.Center_of_mass_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_bond_or_angle_constraint.
    def enterFix_bond_or_angle_constraint(self, ctx: CharmmMRParser.Fix_bond_or_angle_constraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#fix_bond_or_angle_constraint.
    def exitFix_bond_or_angle_constraint(self, ctx: CharmmMRParser.Fix_bond_or_angle_constraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#restrained_distance.
    def enterRestrained_distance(self, ctx: CharmmMRParser.Restrained_distanceContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#restrained_distance.
    def exitRestrained_distance(self, ctx: CharmmMRParser.Restrained_distanceContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#external_force.
    def enterExternal_force(self, ctx: CharmmMRParser.External_forceContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#external_force.
    def exitExternal_force(self, ctx: CharmmMRParser.External_forceContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_restraint.
    def enterRmsd_restraint(self, ctx: CharmmMRParser.Rmsd_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#rmsd_restraint.
    def exitRmsd_restraint(self, ctx: CharmmMRParser.Rmsd_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#gyration_restraint.
    def enterGyration_restraint(self, ctx: CharmmMRParser.Gyration_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#gyration_restraint.
    def exitGyration_restraint(self, ctx: CharmmMRParser.Gyration_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#distance_matrix_restraint.
    def enterDistance_matrix_restraint(self, ctx: CharmmMRParser.Distance_matrix_restraintContext):  # pylint: disable=unused-argument
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CharmmMRParser#distance_matrix_restraint.
    def exitDistance_matrix_restraint(self, ctx: CharmmMRParser.Distance_matrix_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#noe_statement.
    def enterNoe_statement(self, ctx: CharmmMRParser.Noe_statementContext):
        if ctx.MinDist():
            self.noeAverage = 'min'

        elif ctx.SumR():
            self.noeAverage = 'sum'

        elif ctx.SExp():
            self.squareExponent = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.squareExponent, str):
                if self.squareExponent in self.evaluate:
                    self.squareExponent = self.evaluate[self.squareExponent]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.squareExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareExponent = 1.0
            if self.squareExponent is None or self.squareExponent <= 0.0:
                self.f.append("[Invalid data] "
                              "The exponent value of square-well or soft-square function "
                              f"'NOE {str(ctx.SExp())} {self.squareExponent} END' must be a positive value.")

        elif ctx.RSwi():
            self.rSwitch = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rSwitch, str):
                if self.rSwitch in self.evaluate:
                    self.rSwitch = self.evaluate[self.rSwitch]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.rSwitch!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rSwitch = 1.0
            if self.rSwitch is None or self.rSwitch < 0.0:
                self.f.append("[Invalid data] "
                              "The smoothing parameter of soft-square function "
                              f"'NOE {str(ctx.RSwi())} {self.rSwitch} END' must not be a negative value.")

        elif ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.scale!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale is None or self.scale == 0.0:
                self.f.append("[Range value warning] "
                              f"The scale value 'NOE {str(ctx.Scale())} {self.scale} END' should be a positive value.")
            elif self.scale < 0.0:
                self.f.append("[Invalid data] "
                              f"The scale value 'NOE {str(ctx.Scale())} {self.scale} END' must not be a negative value.")

        elif ctx.KMin():
            self.kMin = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.kMin, str):
                if self.kMin in self.evaluate:
                    self.kMin = self.evaluate[self.kMin]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.kMin!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.kMin = 0.0
            if self.kMin is None or self.kMin < 0.0:
                self.f.append("[Invalid data] "
                              "The kinetic parameter of soft-square function "
                              f"'NOE {str(ctx.KMin())} {self.kMin} END' must not be a negative value.")

        elif ctx.KMax():
            self.kMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.kMax, str):
                if self.kMax in self.evaluate:
                    self.kMax = self.evaluate[self.kMax]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.kMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.kMax = 0.0
            if self.kMax is None or self.kMax < 0.0:
                self.f.append("[Invalid data] "
                              "The kinetic parameter of soft-square function "
                              f"'NOE {str(ctx.KMax())} {self.kMax} END' must not be a negative value.")

        elif ctx.RMin():
            self.rMin = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rMin, str):
                if self.rMin in self.evaluate:
                    self.rMin = self.evaluate[self.rMin]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.rMin!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rMin = 0.0
            if self.rMin is None or self.rMin < 0.0:
                self.f.append("[Invalid data] "
                              "The lower limit of distance restraint "
                              f"'NOE {str(ctx.RMin())} {self.rMin} END' must not be a negative value.")

        elif ctx.RMax():
            self.rMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rMax, str):
                if self.rMax in self.evaluate:
                    self.rMax = self.evaluate[self.rMax]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.rMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rMax = None
            if self.rMax is not None and self.rMax < 0.0:
                self.f.append("[Invalid data] "
                              "The upper limit of distance restraint "
                              f"'NOE {str(ctx.RMax())} {self.rMax} END' must not be a negative value.")

        elif ctx.FMax():
            self.fMax = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.fMax, str):
                if self.fMax in self.evaluate:
                    self.fMax = self.evaluate[self.fMax]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.fMax!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.fMax = None
            if self.fMax is not None and self.fMax < 0.0:
                self.f.append("[Invalid data] "
                              "The kinetic parameter of smoothing function "
                              f"'NOE {str(ctx.FMax())} {self.fMax} END' must not be a negative value.")

        elif ctx.RExp():
            self.rExp = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rExp, str):
                if self.rExp in self.evaluate:
                    self.rExp = self.evaluate[self.rExp]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.rExp!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rExp = -1.0 / 6.0
            if abs(self.rExp + 1.0 / 6.0) < 0.001 or abs(self.rExp - 6.0) < 0.001:
                self.noeAverage = 'r-6'
            elif abs(self.rExp - 3.0) < 0.001:
                self.noeAverage = 'r-3'
            elif abs(self.rExp - 1.0) < 0.001:
                self.noeAverage = 'center'

        elif ctx.Reset():
            self.noeAverage = 'r-6'
            self.squareExponent = 1.0
            self.rSwitch = None
            self.scale = 1.0
            self.kMin = 0.0
            self.kMax = 0.0
            self.rMin = 0.0
            self.rMax = None
            self.fMax = None
            # self.tCon = 0.0
            self.rExp = -1.0 / 6.0

    # Exit a parse tree produced by CharmmMRParser#noe_statement.
    def exitNoe_statement(self, ctx: CharmmMRParser.Noe_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#noe_assign.
    def enterNoe_assign(self, ctx: CharmmMRParser.Noe_assignContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#noe_assign.
    def exitNoe_assign(self, ctx: CharmmMRParser.Noe_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#pnoe_statement.
    def enterPnoe_statement(self, ctx: CharmmMRParser.Pnoe_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#pnoe_statement.
    def exitPnoe_statement(self, ctx: CharmmMRParser.Pnoe_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#pnoe_assign.
    def enterPnoe_assign(self, ctx: CharmmMRParser.Pnoe_assignContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#pnoe_assign.
    def exitPnoe_assign(self, ctx: CharmmMRParser.Pnoe_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_statement.
    def enterDihedral_statement(self, ctx: CharmmMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        if ctx.Force():
            self.force = float(str(ctx.Force()))

        elif ctx.Min():
            self.min = float(str(ctx.Min()))

        elif ctx.Width():
            self.width = float(str(ctx.Width()))

        elif ctx.Period():
            self.period = int(str(ctx.Period()))

    # Exit a parse tree produced by CharmmMRParser#dihedral_statement.
    def exitDihedral_statement(self, ctx: CharmmMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#dihedral_assign.
    def enterDihedral_assign(self, ctx: CharmmMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#dihedral_assign.
    def exitDihedral_assign(self, ctx: CharmmMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        if ctx.selection(0):
            pass

        elif ctx.ByNumber():
            if len(self.__atomNumberDict) == 0:
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'bynumber' clause has no effect "
                              "because CHARMM CRD file is not provided.")
            else:
                for col in range(4):
                    ai = int(str(ctx.Integer(col)))
                    if ai in self.__atomNumberDict:
                        atomSelection = [copy.copy(self.__atomNumberDict[ai])]
                        self.atomSelectionSet.append(atomSelection)
                    else:
                        self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                      f"'{ai}' is not defined in the CHARMM CRD file.")

        elif ctx.Simple_name(0) and ctx.Integer(0):
            if ctx.Simple_name(4):
                for col in range(4):
                    self.factor = {'chain_id': [str(ctx.Simple_name(col * 2))],
                                   'seq_id': [int(str(ctx.Integer(col)))],
                                   'atom_id': [str(ctx.Simple_name(col * 2 + 1))]}
                    self.factor = self.doConsumeFactor_expressions(self.factor, 'atom-spec', True)
                    atomSelection = self.factor['atom_selection'] if 'atom_selection' in self.factor else []
                    self.atomSelectionSet.append(atomSelection)
            else:
                for col in range(4):
                    self.factor = {'seq_id': [int(str(ctx.Integer(col)))],
                                   'atom_id': [str(ctx.Simple_name(col))]}
                    atomSelection = self.factor['atom_selection'] if 'atom_selection' in self.factor else []
                    self.atomSelectionSet.append(atomSelection)

    # Enter a parse tree produced by CharmmMRParser#harmonic_statement.
    def enterHarmonic_statement(self, ctx: CharmmMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#harmonic_statement.
    def exitHarmonic_statement(self, ctx: CharmmMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#absolute_spec.
    def enterAbsolute_spec(self, ctx: CharmmMRParser.Absolute_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#absolute_spec.
    def exitAbsolute_spec(self, ctx: CharmmMRParser.Absolute_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#force_const_spec.
    def enterForce_const_spec(self, ctx: CharmmMRParser.Force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#force_const_spec.
    def exitForce_const_spec(self, ctx: CharmmMRParser.Force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#bestfit_spec.
    def enterBestfit_spec(self, ctx: CharmmMRParser.Bestfit_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#bestfit_spec.
    def exitBestfit_spec(self, ctx: CharmmMRParser.Bestfit_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#coordinate_spec.
    def enterCoordinate_spec(self, ctx: CharmmMRParser.Coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#coordinate_spec.
    def exitCoordinate_spec(self, ctx: CharmmMRParser.Coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#ic_statement.
    def enterIc_statement(self, ctx: CharmmMRParser.Ic_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#ic_statement.
    def exitIc_statement(self, ctx: CharmmMRParser.Ic_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#droplet_statement.
    def enterDroplet_statement(self, ctx: CharmmMRParser.Droplet_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#droplet_statement.
    def exitDroplet_statement(self, ctx: CharmmMRParser.Droplet_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_atom_statement.
    def enterFix_atom_statement(self, ctx: CharmmMRParser.Fix_atom_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#fix_atom_statement.
    def exitFix_atom_statement(self, ctx: CharmmMRParser.Fix_atom_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#center_of_mass_statement.
    def enterCenter_of_mass_statement(self, ctx: CharmmMRParser.Center_of_mass_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#center_of_mass_statement.
    def exitCenter_of_mass_statement(self, ctx: CharmmMRParser.Center_of_mass_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fix_bond_or_angle_statement.
    def enterFix_bond_or_angle_statement(self, ctx: CharmmMRParser.Fix_bond_or_angle_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#fix_bond_or_angle_statement.
    def exitFix_bond_or_angle_statement(self, ctx: CharmmMRParser.Fix_bond_or_angle_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#shake_opt.
    def enterShake_opt(self, ctx: CharmmMRParser.Shake_optContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#shake_opt.
    def exitShake_opt(self, ctx: CharmmMRParser.Shake_optContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#fast_opt.
    def enterFast_opt(self, ctx: CharmmMRParser.Fast_optContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#fast_opt.
    def exitFast_opt(self, ctx: CharmmMRParser.Fast_optContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#restrained_distance_statement.
    def enterRestrained_distance_statement(self, ctx: CharmmMRParser.Restrained_distance_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#restrained_distance_statement.
    def exitRestrained_distance_statement(self, ctx: CharmmMRParser.Restrained_distance_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#external_force_statement.
    def enterExternal_force_statement(self, ctx: CharmmMRParser.External_force_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#external_force_statement.
    def exitExternal_force_statement(self, ctx: CharmmMRParser.External_force_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_statement.
    def enterRmsd_statement(self, ctx: CharmmMRParser.Rmsd_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#rmsd_statement.
    def exitRmsd_statement(self, ctx: CharmmMRParser.Rmsd_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_orient_spec.
    def enterRmsd_orient_spec(self, ctx: CharmmMRParser.Rmsd_orient_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_orient_spec.
    def exitRmsd_orient_spec(self, ctx: CharmmMRParser.Rmsd_orient_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_force_const_spec.
    def enterRmsd_force_const_spec(self, ctx: CharmmMRParser.Rmsd_force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_force_const_spec.
    def exitRmsd_force_const_spec(self, ctx: CharmmMRParser.Rmsd_force_const_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#rmsd_coordinate_spec.
    def enterRmsd_coordinate_spec(self, ctx: CharmmMRParser.Rmsd_coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#rmsd_coordinate_spec.
    def exitRmsd_coordinate_spec(self, ctx: CharmmMRParser.Rmsd_coordinate_specContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#gyration_statement.
    def enterGyration_statement(self, ctx: CharmmMRParser.Gyration_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#gyration_statement.
    def exitGyration_statement(self, ctx: CharmmMRParser.Gyration_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#distance_matrix_statement.
    def enterDistance_matrix_statement(self, ctx: CharmmMRParser.Distance_matrix_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CharmmMRParser#distance_matrix_statement.
    def exitDistance_matrix_statement(self, ctx: CharmmMRParser.Distance_matrix_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmMRParser#selection.
    def enterSelection(self, ctx: CharmmMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.verbose_debug:
            print("  " * self.depth + "enter_selection")

        if self.depth == 0:
            self.stackSelections = []
            self.stackTerms = []
            self.factor = {}

    # Exit a parse tree produced by CharmmMRParser#selection.
    def exitSelection(self, ctx: CharmmMRParser.SelectionContext):  # pylint: disable=unused-argument
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
                atomSelection = self.intersectionAtom_selections(blockSelections.pop(), atomSelection)

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

    # Enter a parse tree produced by CharmmMRParser#selection_expression.
    def enterSelection_expression(self, ctx: CharmmMRParser.Selection_expressionContext):
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

    # Exit a parse tree produced by CharmmMRParser#selection_expression.
    def exitSelection_expression(self, ctx: CharmmMRParser.Selection_expressionContext):  # pylint: disable=unused-argument
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

    # Enter a parse tree produced by CharmmMRParser#term.
    def enterTerm(self, ctx: CharmmMRParser.TermContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_term, intersection: {bool(ctx.And_op(0))}")

        self.stackFactors = []
        self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by CharmmMRParser#term.
    def exitTerm(self, ctx: CharmmMRParser.TermContext):  # pylint: disable=unused-argument
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
                _factor = self.doConsumeFactor_expressions(self.stackFactors.pop(), cifCheck=True)
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

    # Enter a parse tree produced by CharmmMRParser#factor.
    def enterFactor(self, ctx: CharmmMRParser.FactorContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_factor, concatenation: {bool(ctx.factor())}")

        if ctx.Not_op():
            if len(self.factor) > 0:
                self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)
                if 'atom_selection' in self.factor:
                    self.stackFactors.append(self.factor)
                self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by CharmmMRParser#factor.
    def exitFactor(self, ctx: CharmmMRParser.FactorContext):
        self.depth -= 1
        if self.verbose_debug:
            print("  " * self.depth + "exit_factor")

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

            if ctx.All() or ctx.Initial():
                clauseName = 'all' if ctx.All() else 'initial'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                try:

                    atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [{'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    self.intersectionFactor_expressions(atomSelection)

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName!r} clause has no effect.")

                    else:
                        if 'chain_id' in self.factor:
                            del self.factor['chain_id']
                        if 'comp_id' in self.factor:
                            del self.factor['comp_id']
                        if 'seq_id' in self.factor:
                            del self.factor['seq_id']
                        if 'type_symbol' in self.factor:
                            del self.factor['type_symbol']
                        if 'atom_id' in self.factor:
                            del self.factor['atom_id']
                        if 'comp_ids' in self.factor:
                            del self.factor['comp_ids']
                        if 'seq_ids' in self.factor:
                            del self.factor['seq_ids']
                        if 'type_symbols' in self.factor:
                            del self.factor['type_symbols']
                        if 'atom_ids' in self.factor:
                            del self.factor['atom_ids']
                        if 'alt_chain_id' in self.factor:
                            del self.factor['alt_chain_id']
                        if 'alt_atom_id' in self.factor:
                            del self.factor['alt_atom_id']

                except Exception as e:
                    if self.verbose:
                        self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

            elif ctx.Around():
                clauseName = 'around'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                around = self.numberFSelection[0]
                _atomSelection = []

                self.consumeFactor_expressions(f"atom selection expression before the {clauseName!r} clause")

                if 'atom_selection' in self.factor:

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
                                self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                    if len(self.factor['atom_selection']) > 0:
                        self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items())
                                                                              for atom in _atomSelection
                                                                              if isinstance(atom, dict))]

                        if len(self.factor['atom_selection']) == 0:
                            self.factor['atom_id'] = [None]
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName!r} clause has no effect.")

            elif ctx.Atom():
                if self.verbose_debug:
                    print("  " * self.depth + "--> atom")
                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                simpleNameIndex = simpleNamesIndex = 0  # these indices are necessary to deal with mixing case of 'Simple_name' and 'Simple_names'
                if ctx.Simple_name(0):
                    chainId = str(ctx.Simple_name(0))
                    self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                               if ps['auth_chain_id'] == self.getRealChainId(chainId, ps['auth_chain_id'])]
                    if self.hasNonPolySeq:
                        for np in self.nonPolySeq:
                            _chainId = np['auth_chain_id']
                            if _chainId == self.getRealChainId(chainId, _chainId) and _chainId not in self.factor['chain_id']:
                                self.factor['chain_id'].append(_chainId)
                    if len(self.factor['chain_id']) > 0:
                        simpleNameIndex += 1

                if simpleNameIndex == 0 and ctx.Simple_names(0):
                    chainId = str(ctx.Simple_names(0))
                    if self.reasons is not None and 'segment_id_mismatch' in self.reasons and chainId in self.reasons['segment_id_mismatch']\
                       and self.reasons['segment_id_mismatch'][chainId] in self.reasons['segment_id_match_stats'][chainId]:
                        _chainId = self.reasons['segment_id_mismatch'][chainId]
                        _stats = self.reasons['segment_id_match_stats'][chainId]
                        self.factor['chain_id'] = sorted([k for k, v in _stats.items() if v == _stats[_chainId]])
                        self.factor['alt_chain_id'] = chainId
                    else:
                        chainId_ex = toRegEx(chainId)
                        self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                                   if re.match(chainId_ex, ps['auth_chain_id'])]
                        if self.hasNonPolySeq:
                            for np in self.nonPolySeq:
                                __chainId = np['auth_chain_id']
                                if re.match(chainId_ex, __chainId) and __chainId not in self.factor['chain_id']:
                                    self.factor['chain_id'].append(__chainId)
                    simpleNamesIndex += 1

                if len(self.factor['chain_id']) == 0:
                    if self.monoPolymer and not self.hasBranched and not self.hasNonPoly:
                        self.factor['chain_id'] = self.polySeq[0]['chain_id']
                        self.factor['auth_chain_id'] = chainId
                    elif self.reasons is not None:
                        self.factor['atom_id'] = [None]
                        if 'segment_id_mismatch' in self.reasons\
                           and (chainId not in self.reasons['segment_id_mismatch']
                                or self.reasons['segment_id_mismatch'][chainId] is not None):
                            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                          "Couldn't specify segment name "
                                          f"'{chainId}' the coordinates.")  # do not use 'chainId!r' expression, '%' code throws ValueError
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

                if ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                if ctx.Integers():
                    seqId = str(ctx.Integers())
                    seqId_ex = toRegEx(seqId)
                    _seqIdSelect = set()
                    for chainId in self.factor['chain_id']:
                        psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                        for ps in psList:
                            isPolySeq = ps in self.polySeq
                            found = False
                            for realSeqId in ps['auth_seq_id']:
                                if realSeqId is None:
                                    continue
                                realSeqId = self.getRealSeqId(ps, realSeqId, isPolySeq)[0]
                                if re.match(seqId_ex, str(realSeqId)):
                                    _seqIdSelect.add(realSeqId)
                                    found = True
                            if not found:
                                for realSeqId in ps['auth_seq_id']:
                                    if realSeqId is None:
                                        continue
                                    realSeqId = self.getRealSeqId(ps, realSeqId, isPolySeq)[0]
                                    seqKey = (chainId, realSeqId)
                                    if seqKey in self.authToLabelSeq:
                                        _, realSeqId = self.authToLabelSeq[seqKey]
                                        if re.match(seqId_ex, str(realSeqId)):
                                            _seqIdSelect.add(realSeqId)
                    self.factor['seq_id'] = list(_seqIdSelect)

                _atomIdSelect = set()
                if ctx.Simple_name(simpleNameIndex):
                    atomId = str(ctx.Simple_name(simpleNameIndex))
                    for chainId in self.factor['chain_id']:
                        psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                        for ps in psList:
                            isPolySeq = ps in self.polySeq
                            for seqId in self.factor['seq_id']:
                                if seqId in ps['auth_seq_id']:
                                    seqId, compId, _ = self.getRealSeqId(ps, seqId, isPolySeq)
                                    # compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                                    if self.ccU.updateChemCompDict(compId):
                                        if any(True for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId):
                                            _atomIdSelect.add(atomId)

                elif ctx.Simple_names(simpleNamesIndex):
                    atomId = translateToStdAtomName(str(ctx.Simple_names(simpleNamesIndex)),
                                                    None if 'comp_id' not in self.factor else self.factor['comp_id'][0],
                                                    ccU=self.ccU)
                    atomId_ex = toRegEx(atomId)
                    for chainId in self.factor['chain_id']:
                        psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                        for ps in psList:
                            isPolySeq = ps in self.polySeq
                            for seqId in self.factor['seq_id']:
                                if seqId in ps['auth_seq_id']:
                                    seqId, compId, _ = self.getRealSeqId(ps, seqId, isPolySeq)
                                    # compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                                    if self.ccU.updateChemCompDict(compId):
                                        for cca in self.ccU.lastAtomList:
                                            if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                                realAtomId = cca[self.ccU.ccaAtomId]
                                                if re.match(atomId_ex, realAtomId):
                                                    _atomIdSelect.add(realAtomId)

                self.factor['atom_id'] = list(_atomIdSelect)

                self.consumeFactor_expressions("'atom' clause", False)

            elif ctx.Property():
                if self.verbose_debug:
                    print("  " * self.depth + "--> property")
                if not self.hasCoord:
                    return
                absolute = bool(ctx.Abs())
                _attr_prop = str(ctx.Attr_properties())
                attr_prop = _attr_prop.lower()
                opCode = str(ctx.Comparison_ops()).lower()
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                attr_value = self.numberFSelection[0]

                validProp = True

                if attr_prop.startswith('xcom')\
                        or attr_prop.startswith('ycom')\
                        or attr_prop.startswith('zcom')\
                        or attr_prop.startswith('wcom')\
                        or attr_prop.startswith('wmai'):  # XCOMP, YCOMP, ZCOMP, WCOMP, WMAI
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "requires a comparison coordinate set.")
                    validProp = False

                elif attr_prop.startswith('char'):  # CAHRGE
                    valueType = {'name': 'pdbx_formal_charge'}
                    if opCode in ('.eq.', '.ae.'):
                        valueType['type'] = 'int' if not absolute else 'abs-int'
                        valueType['value'] = attr_value
                    elif opCode == '.lt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '.le.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '.ne.':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'not_equal_to': attr_value}
                    atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [valueType,
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop in ('dx', 'dy', 'dz'):
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "related to atomic force of each atom is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop.startswith('fbet'):  # FBETA
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "related to the Langevin dynamics (nonzero friction coefficient) is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop == 'mass':
                    _typeSymbolSelect = set()
                    atomTypes = self.cR.getDictList('atom_type')
                    if len(atomTypes) > 0 and 'symbol' in atomTypes[0]:
                        for atomType in atomTypes:
                            typeSymbol = atomType['symbol']
                            atomicNumber = int_atom(typeSymbol)
                            atomicWeight = ELEMENT_WEIGHTS[atomicNumber]

                            if (opCode == '.eq.' and atomicWeight == attr_value)\
                               or (opCode == '.lt.' and atomicWeight < attr_value)\
                               or (opCode == '.gt.' and atomicWeight > attr_value)\
                               or (opCode == '.le.' and atomicWeight <= attr_value)\
                               or (opCode == '.ge.' and atomicWeight >= attr_value)\
                               or (opCode == '.ne.' and atomicWeight != attr_value)\
                               or (opCode == '.ae.' and abs(atomicWeight - attr_value) < 0.001):
                                _typeSymbolSelect.add(typeSymbol)

                    atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [{'name': 'type_symbol', 'type': 'enum',
                                                        'enum': _typeSymbolSelect},
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop in ('xref', 'yref', 'zref'):
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "requires a reference coordinate set.")
                    validProp = False

                elif attr_prop in ('vx', 'vy', 'vz'):
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "related to current velocities of each atom is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop in ('x', 'y', 'z'):
                    valueType = {'name': f"Cartn_{attr_prop}"}
                    if opCode == '.eq.':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '.lt.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '.gt.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '.le.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '.ge.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '.ne.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'not_equal_to': attr_value}
                    elif opCode == '.ae.':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value - 0.001, 'max_inclusive': attr_value + 0.001}
                    atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [valueType,
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    self.intersectionFactor_expressions(atomSelection)

                elif attr_prop.startswith('sca') or attr_prop in ('zero', 'one'):
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The '{_attr_prop}' clause has no effect "
                                  "because the internal vector statement is not set.")
                    validProp = False

                elif attr_prop.startswith('econ') or attr_prop.startswith('epco') or attr_prop.startswith('cons')\
                        or attr_prop.startswith('igno') or attr_prop.startswith('aspv') or attr_prop.startswith('vdws')\
                        or attr_prop.startswith('alph') or attr_prop.startswith('effe') or attr_prop.startswith('radi')\
                        or attr_prop.startswith('rsca') or attr_prop.startswith('fdco')\
                        or attr_prop in ('move', 'type', 'fdim', 'fdep'):
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "related to software specific parameters of each atom is not possessed in the static coordinate file.")
                    validProp = False

                if validProp and len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    _absolute = ' abs' if absolute else ''
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  f"The 'attribute' clause ('{_attr_prop}{_absolute} {opCode} {attr_value}') has no effect.")

            elif ctx.Bonded():
                if self.verbose_debug:
                    print("  " * self.depth + "--> bonded")
                if not self.hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        compId = _atom['comp_id']
                        seqId = _atom['seq_id']
                        atomId = _atom['atom_id']

                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)

                        # intra
                        if self.ccU.updateChemCompDict(compId):
                            leavingAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] == 'Y']

                            _atomIdSelect = set()
                            for ccb in self.ccU.lastBonds:
                                if ccb[self.ccU.ccbAtomId1] == atomId:
                                    _atomIdSelect.add(ccb[self.ccU.ccbAtomId2])
                                elif ccb[self.ccU.ccbAtomId2] == atomId:
                                    _atomIdSelect.add(ccb[self.ccU.ccbAtomId1])

                            hasLeaavindAtomId = False

                            for _atomId in _atomIdSelect:

                                if _atomId in leavingAtomIds:
                                    hasLeaavindAtomId = True
                                    continue

                                _atom = None
                                if coordAtomSite is not None:
                                    if _atomId in coordAtomSite['atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                    elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in coordAtomSite['atom_id']
                                                                               or ('H' + _atomId[-1] in coordAtomSite['atom_id'])):
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                    elif 'alt_atom_id' in coordAtomSite and _atomId in coordAtomSite['alt_atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']

                                if _atom is not None and _atom['comp_id'] == compId:
                                    _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                                else:
                                    psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                                    for ps in psList:
                                        isPolySeq = ps in self.polySeq
                                        if seqId in ps['auth_seq_id'] and ps['comp_id'][ps['auth_seq_id'].index(seqId)] == compId:
                                            seqId = self.getRealSeqId(ps, seqId, isPolySeq)[0]
                                            if any(True for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId):
                                                _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                            # sequential
                            if hasLeaavindAtomId:
                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': chainId},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': seqId},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': atomId},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) == 1:
                                    origin = to_np_array(_origin[0])

                                    psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                                    for ps in psList:
                                        isPolySeq = ps in self.polySeq
                                        for _seqId in [seqId - 1, seqId + 1]:
                                            if _seqId in ps['auth_seq_id']:
                                                _seqId, _compId, _ = self.getRealSeqId(ps, _seqId, isPolySeq)
                                                # _compId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                                                if self.ccU.updateChemCompDict(_compId):
                                                    leavingAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] == 'Y']

                                                    _atomIdSelect = set()
                                                    for ccb in self.ccU.lastBonds:
                                                        if ccb[self.ccU.ccbAtomId1] in leavingAtomIds:
                                                            _atomId = ccb[self.ccU.ccbAtomId2]
                                                            if _atomId not in leavingAtomIds:
                                                                _atomIdSelect.add(_atomId)
                                                        if ccb[self.ccU.ccbAtomId2] in leavingAtomIds:
                                                            _atomId = ccb[self.ccU.ccbAtomId1]
                                                            if _atomId not in leavingAtomIds:
                                                                _atomIdSelect.add(_atomId)

                                                    for _atomId in _atomIdSelect:
                                                        _neighbor =\
                                                            self.cR.getDictListWithFilter('atom_site',
                                                                                          CARTN_DATA_ITEMS,
                                                                                          [{'name': self.authAsymId, 'type': 'str', 'value': chainId},
                                                                                           {'name': self.authSeqId, 'type': 'int', 'value': _seqId},
                                                                                           {'name': self.authAtomId, 'type': 'str', 'value': _atomId},
                                                                                           {'name': self.modelNumName, 'type': 'int',
                                                                                            'value': self.representativeModelId},
                                                                                           {'name': 'label_alt_id', 'type': 'enum',
                                                                                            'enum': (self.representativeAltId,)}
                                                                                           ])

                                                        if len(_neighbor) != 1:
                                                            continue

                                                        if distance(to_np_array(_neighbor[0]), origin) < 2.5:
                                                            _atomSelection.append({'chain_id': chainId, 'seq_id': _seqId, 'comp_id': _compId, 'atom_id': _atomId})

                        # struct_conn category
                        _atom = self.cR.getDictListWithFilter('struct_conn',
                                                              PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                              [{'name': 'ptnr2_auth_asym_id', 'type': 'str', 'value': chainId},
                                                               {'name': 'ptnr2_auth_seq_id', 'type': 'int', 'value': seqId},
                                                               {'name': 'ptnr2_label_atom_id', 'type': 'str', 'value': atomId},
                                                               {'name': self.modelNumName, 'type': 'int',
                                                                'value': self.representativeModelId}
                                                               ])

                        if len(_atom) == 1:
                            _atomSelection.append(_atom[0])

                        _atom = self.cR.getDictListWithFilter('struct_conn',
                                                              PTNR2_AUTH_ATOM_DATA_ITEMS,
                                                              [{'name': 'ptnr1_auth_asym_id', 'type': 'str', 'value': chainId},
                                                               {'name': 'ptnr1_auth_seq_id', 'type': 'int', 'value': seqId},
                                                               {'name': 'ptnr1_label_atom_id', 'type': 'str', 'value': atomId},
                                                               {'name': self.modelNumName, 'type': 'int',
                                                                'value': self.representativeModelId}
                                                               ])

                        if len(_atom) == 1:
                            _atomSelection.append(_atom[0])

                    self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items())
                                                                          for atom in _atomSelection
                                                                          if isinstance(atom, dict))]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      "The 'bondedto' clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'bondedto' clause has no effect because no atom is selected.")

            elif ctx.ByGroup():
                if self.verbose_debug:
                    print("  " * self.depth + "--> bygroup")
                if not self.hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        compId = _atom['comp_id']
                        seqId = _atom['seq_id']
                        atomId = _atom['atom_id']

                        _atomSelection.append(_atom)  # self atom

                        if self.ccU.updateChemCompDict(compId):
                            _bondedAtomIdSelect = set()
                            for ccb in self.ccU.lastBonds:
                                if ccb[self.ccU.ccbAtomId1] == atomId:
                                    _bondedAtomIdSelect.add(ccb[self.ccU.ccbAtomId2])
                                elif ccb[self.ccU.ccbAtomId2] == atomId:
                                    _bondedAtomIdSelect.add(ccb[self.ccU.ccbAtomId1])

                            _nonBondedAtomIdSelect = set()
                            for _atomId in _bondedAtomIdSelect:
                                for ccb in self.ccU.lastBonds:
                                    if ccb[self.ccU.ccbAtomId1] == _atomId:
                                        _nonBondedAtomIdSelect.add(ccb[self.ccU.ccbAtomId2])
                                    elif ccb[self.ccU.ccbAtomId2] == _atomId:
                                        _nonBondedAtomIdSelect.add(ccb[self.ccU.ccbAtomId1])

                            if atomId in _nonBondedAtomIdSelect:
                                _nonBondedAtomIdSelect.remove(atomId)

                            for _atomId in _bondedAtomIdSelect:
                                if _atomId in _nonBondedAtomIdSelect:
                                    _nonBondedAtomIdSelect.remove(_atomId)

                            if len(_nonBondedAtomIdSelect) > 0:
                                _origin =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  CARTN_DATA_ITEMS,
                                                                  [{'name': self.authAsymId, 'type': 'str', 'value': chainId},
                                                                   {'name': self.authSeqId, 'type': 'int', 'value': seqId},
                                                                   {'name': self.authAtomId, 'type': 'str', 'value': atomId},
                                                                   {'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                if len(_origin) == 1:
                                    origin = to_np_array(_origin[0])

                                    for _atomId in _nonBondedAtomIdSelect:
                                        _neighbor =\
                                            self.cR.getDictListWithFilter('atom_site',
                                                                          CARTN_DATA_ITEMS,
                                                                          [{'name': self.authAsymId, 'type': 'str', 'value': chainId},
                                                                           {'name': self.authSeqId, 'type': 'int', 'value': seqId},
                                                                           {'name': self.authAtomId, 'type': 'str', 'value': _atomId},
                                                                           {'name': self.modelNumName, 'type': 'int',
                                                                            'value': self.representativeModelId},
                                                                           {'name': 'label_alt_id', 'type': 'enum',
                                                                            'enum': (self.representativeAltId,)}
                                                                           ])

                                        if len(_neighbor) != 1:
                                            continue

                                        if distance(to_np_array(_neighbor[0]), origin) < 2.0:
                                            _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                                else:
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)
                                    if cca is not None:
                                        _origin = {'x': float(cca[self.ccU.ccaCartnX]), 'y': float(cca[self.ccU.ccaCartnY]), 'z': float(cca[self.ccU.ccaCartnZ])}
                                        origin = to_np_array(_origin)

                                        for _atomId in _nonBondedAtomIdSelect:
                                            _cca = next((_cca for _cca in self.ccU.lastAtomList if _cca[self.ccU.ccaAtomId] == _atomId), None)
                                            if _cca is not None:
                                                _neighbor = {'x': float(_cca[self.ccU.ccaCartnX]), 'y': float(_cca[self.ccU.ccaCartnY]), 'z': float(_cca[self.ccU.ccaCartnZ])}

                                                if distance(to_np_array(_neighbor), origin) < 2.0:
                                                    _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId})

                    atomSelection = [dict(s) for s in set(frozenset(atom.items())
                                                          for atom in _atomSelection
                                                          if isinstance(atom, dict))]

                    if len(atomSelection) <= len(self.factor['atom_selection']):
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      "The 'bygroup' clause has no effect.")

                    self.factor['atom_selection'] = atomSelection

                else:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'bygroup' clause has no effect because no atom is selected.")

            elif ctx.ByRes():
                if self.verbose_debug:
                    print("  " * self.depth + "--> byres")
                if not self.hasCoord:
                    return
                if 'atom_selection' in self.factor and len(self.factor['atom_selection']) > 0:
                    _atomSelection = []

                    _sequenceSelect = set()

                    for _atom in self.factor['atom_selection']:
                        chainId = _atom['chain_id']
                        seqId = _atom['seq_id']

                        _sequenceSelect.add((chainId, seqId))

                    for (chainId, seqId) in _sequenceSelect:
                        _atom = next(_atom for _atom in self.factor['atom_selection'] if _atom['chain_id'] == chainId and _atom['seq_id'] == seqId)
                        compId = _atom['comp_id']

                        _atomByRes =\
                            self.cR.getDictListWithFilter('atom_site',
                                                          ATOM_NAME_DATA_ITEMS,
                                                          [{'name': self.authAsymId, 'type': 'str', 'value': chainId},
                                                           {'name': self.authSeqId, 'type': 'int', 'value': seqId},
                                                           {'name': self.modelNumName, 'type': 'int',
                                                            'value': self.representativeModelId},
                                                           {'name': 'label_alt_id', 'type': 'enum',
                                                            'enum': (self.representativeAltId,)}
                                                           ])

                        if len(_atomByRes) > 0 and _atomByRes[0]['comp_id'] == compId:
                            for _atom in _atomByRes:
                                _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': _atom['comp_id'], 'atom_id': _atom['atom_id']})

                        else:
                            psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                            for ps in psList:
                                isPolySeq = ps in self.polySeq
                                if seqId in ps['auth_seq_id'] and ps['comp_id'][ps['auth_seq_id'].index(seqId)] == compId:
                                    seqId = self.getRealSeqId(ps, seqId, isPolySeq)[0]
                                    if self.ccU.updateChemCompDict(compId):
                                        atomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                                        for atomId in atomIds:
                                            _atomSelection.append({'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': atomId})

                    self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items())
                                                                          for atom in _atomSelection
                                                                          if isinstance(atom, dict))]

                    if len(self.factor['atom_selection']) == 0:
                        self.factor['atom_id'] = [None]
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      "The 'byres' clause has no effect.")

                else:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'byres' clause has no effect because no atom is selected.")

            elif ctx.Chemical():
                if self.verbose_debug:
                    print("  " * self.depth + "--> chemical")
                if ctx.Colon():  # range expression
                    self.factor['type_symbols'] = [str(ctx.Simple_name(0)).upper(), str(ctx.Simple_name(1)).upper()]

                elif ctx.Simple_name(0):
                    self.factor['type_symbol'] = [str(ctx.Simple_name(0)).upper()]

                elif ctx.Simple_names(0):
                    self.factor['type_symbols'] = [str(ctx.Simple_names(0)).upper()]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['type_symbol'] = [v.upper() for v in val]
                        else:
                            self.factor['type_symbol'] = [val.upper()]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                self.consumeFactor_expressions("'chemical' clause", False)

            elif ctx.Hydrogen():
                if self.verbose_debug:
                    print("  " * self.depth + "--> hydrogen")
                if not self.hasCoord:
                    return
                _typeSymbolSelect = set()
                atomTypes = self.cR.getDictList('atom_type')
                if len(atomTypes) > 0 and 'symbol' in atomTypes[0]:
                    for atomType in atomTypes:
                        typeSymbol = atomType['symbol']
                        atomicNumber = int_atom(typeSymbol)
                        atomicWeight = ELEMENT_WEIGHTS[atomicNumber]
                        if atomicWeight < 3.5:
                            _typeSymbolSelect.add(typeSymbol)

                self.factor['type_symbol'] = list(_typeSymbolSelect)

                self.consumeFactor_expressions("'hydrogen' clause", False)

            elif ctx.NONE():
                if self.verbose_debug:
                    print("  " * self.depth + "--> none")
                self.factor['atom_selection'] = []

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
                                    self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

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
                            self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

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

            elif ctx.Point():
                if self.verbose_debug:
                    print("  " * self.depth + "--> point")
                if not self.hasCoord:
                    return
                vector3D = [self.numberFSelection[0], self.numberFSelection[1], self.numberFSelection[2]]
                cut = self.numberFSelection[3]

                atomSelection = []

                try:

                    _neighbor =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_CARTN_DATA_ITEMS,
                                                      [{'name': 'Cartn_x', 'type': 'range-float',
                                                        'range': {'min_exclusive': (vector3D[0] - cut),
                                                                  'max_exclusive': (vector3D[0] + cut)}},
                                                       {'name': 'Cartn_y', 'type': 'range-float',
                                                        'range': {'min_exclusive': (vector3D[1] - cut),
                                                                  'max_exclusive': (vector3D[1] + cut)}},
                                                       {'name': 'Cartn_z', 'type': 'range-float',
                                                        'range': {'min_exclusive': (vector3D[2] - cut),
                                                                  'max_exclusive': (vector3D[2] + cut)}},
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    if len(_neighbor) > 0:
                        neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), vector3D) < cut]

                        for atom in neighbor:
                            del atom['x']
                            del atom['y']
                            del atom['z']
                            atomSelection.append(atom)

                except Exception as e:
                    if self.verbose:
                        self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                self.factor['atom_selection'] = atomSelection

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'cut' clause has no effect.")

            elif ctx.Lone():
                if self.verbose_debug:
                    print("  " * self.depth + "--> lone")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'lone' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Previous():
                if self.verbose_debug:
                    print("  " * self.depth + "--> previous")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'previous' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.User():
                if self.verbose_debug:
                    print("  " * self.depth + "--> user")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'user' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Recall():
                if self.verbose_debug:
                    print("  " * self.depth + "--> recall")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'recall' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.IGroup():
                if self.verbose_debug:
                    print("  " * self.depth + "--> igroup")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'igroup' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Subset():
                if self.verbose_debug:
                    print("  " * self.depth + "--> subset")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'subset' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.ByNumber():
                if self.verbose_debug:
                    print("  " * self.depth + "--> bynumber")

                if ctx.Colon():  # range expression
                    self.factor['atom_num'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['atom_num'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['atom_nums'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_num'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['atom_num'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                if 'atom_num' in self.factor and len(self.__atomNumberDict) > 0:
                    for ai in self.factor['atom_num']:
                        if ai in self.__atomNumberDict:
                            _factor = copy.copy(self.__atomNumberDict[ai])
                            if 'chain_id' not in self.factor:
                                self.factor['chain_id'] = []
                            if _factor['chain_id'] not in self.factor['chain_id']:
                                self.factor['chain_id'].append(_factor['chain_id'])
                            if 'seq_id' not in self.factor:
                                self.factor['seq_id'] = []
                            if _factor['seq_id'] not in self.factor['seq_id']:
                                self.factor['seq_id'].append(_factor['seq_id'])
                            if 'comp_id' not in self.factor:
                                self.factor['comp_id'] = []
                            if 'comp_id' in _factor and _factor['comp_id'] not in self.factor['comp_id']:
                                self.factor['comp_id'].append(_factor['comp_id'])
                            if 'atom_id' not in self.factor:
                                self.factor['atom_id'] = []
                            if 'atom_id' in _factor and _factor['atom_id'] not in self.factor['atom_id']:
                                self.factor['atom_id'].append(_factor['atom_id'])
                            self.factor['atom_num'].remove(ai)
                            if len(self.factor['atom_num']) == 0:
                                del self.factor['atom_num']
                        else:
                            self.f.append(f"[Missing data] {self.getCurrentRestraint()}"
                                          f"'{ai}' is not defined in the CHARMM CRD file.")

            elif ctx.IRes():
                if self.verbose_debug:
                    print("  " * self.depth + "--> ires")

                if ctx.Colon():  # range expression
                    self.factor['seq_id'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['seq_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

            elif ctx.Residue():
                if self.verbose_debug:
                    print("  " * self.depth + "--> residue")

                eval_factor = False
                __factor = None
                if 'seq_id' in self.factor or 'seq_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'residue' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                if ctx.Colon():  # range expression
                    self.factor['seq_id'] = list(range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1))

                elif ctx.Integer(0):
                    self.factor['seq_id'] = [int(str(ctx.Integer(0)))]

                elif ctx.Integers():
                    self.factor['seq_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The 'residue' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                      f"and {self.getReadableFactor(_factor)}.")

            elif ctx.Resname():
                if self.verbose_debug:
                    print("  " * self.depth + "--> resname")

                eval_factor = False
                if 'comp_id' in self.factor or 'comp_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'resname' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                if ctx.Colon():  # range expression
                    self.factor['comp_ids'] = [str(ctx.Simple_name(0)).upper(), str(ctx.Simple_name(1)).upper()]

                elif ctx.Simple_name(0):
                    self.factor['comp_id'] = [str(ctx.Simple_name(0)).upper()]

                elif ctx.Simple_names(0):
                    self.factor['comp_ids'] = [str(ctx.Simple_names(0)).upper()]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['comp_id'] = [v.upper() for v in val]
                        else:
                            self.factor['comp_id'] = [val.upper()]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The 'resname' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                      f"and {self.getReadableFactor(_factor)}.")

            elif ctx.ISeg():
                if self.verbose_debug:
                    print("  " * self.depth + "--> iseg")

                if ctx.Colon():  # range expression
                    self.factor['chain_id'] = [str(id) for id in range(int(str(ctx.Integer(0))), int(str(ctx.Integer(0))) + 1)]

                elif ctx.Integer(0):
                    self.factor['chain_id'] = [str(ctx.Integer(0))]

                elif ctx.Integers():
                    self.factor['chain_ids'] = [str(ctx.Integers())]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['chain_id'] = [str(v) if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['chain_id'] = [str(val) if isinstance(val, int) else int(val)]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

            elif ctx.SegIdentifier():
                if self.verbose_debug:
                    print("  " * self.depth + "--> segidentifier")
                if not self.hasPolySeq and not self.hasNonPolySeq:
                    return

                eval_factor = False
                if 'chain_id' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'segidentifier' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                if ctx.Colon():  # range expression
                    if ctx.Simple_name(0):
                        begChainId = str(ctx.Simple_name(0))
                    elif ctx.Double_quote_string(0):
                        begChainId = str(ctx.Double_quote_string(0)).strip('"').strip()
                        if len(begChainId) == 0:
                            return
                    if ctx.Simple_name(1):
                        endChainId = str(ctx.Simple_name(1))
                    elif ctx.Double_quote_string(1):
                        endChainId = str(ctx.Double_quote_string(1)).strip('"').strip()
                        if len(endChainId) == 0:
                            return
                    self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                               if begChainId <= ps['auth_chain_id'] <= endChainId]
                    if self.hasNonPolySeq:
                        for np in self.nonPolySeq:
                            _chainId = np['auth_chain_id']
                            if begChainId <= _chainId <= endChainId and _chainId not in self.factor['chain_id']:
                                self.factor['chain_id'].append(_chainId)

                    if len(self.factor['chain_id']) == 0:
                        if self.monoPolymer:
                            self.factor['chain_id'] = self.polySeq[0]['auth_chain_id']
                            self.factor['auth_chain_id'] = [begChainId, endChainId]
                        elif self.reasons is not None:
                            self.factor['atom_id'] = [None]
                            if 'segment_id_mismatch' in self.reasons\
                               and (chainId not in self.reasons['segment_id_mismatch']
                                    or self.reasons['segment_id_mismatch'][chainId] is not None):
                                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                              "Couldn't specify segment name "
                                              f"{begChainId:!r}:{endChainId:!r} in the coordinates.")

                else:
                    if ctx.Simple_name(0) or ctx.Double_quote_string(0):
                        if ctx.Simple_name(0):
                            chainId = str(ctx.Simple_name(0))
                        elif ctx.Double_quote_string(0):
                            chainId = str(ctx.Double_quote_string(0)).strip('"').strip()
                            if len(chainId) == 0:
                                return
                        self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                                   if ps['auth_chain_id'] == self.getRealChainId(chainId, ps['auth_chain_id'])]
                        if self.hasNonPolySeq:
                            for np in self.nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId == self.getRealChainId(chainId, _chainId) and _chainId not in self.factor['chain_id']:
                                    self.factor['chain_id'].append(_chainId)
                        self.factor['segment_id'] = chainId
                        if self.factor['chain_id'] != [chainId]:
                            self.factor['alt_chain_id'] = chainId
                    if ctx.Simple_names(0):
                        chainId = str(ctx.Simple_names(0))
                        if self.reasons is not None and 'segment_id_mismatch' in self.reasons and chainId in self.reasons['segment_id_mismatch']\
                           and self.reasons['segment_id_mismatch'][chainId] in self.reasons['segment_id_match_stats'][chainId]:
                            _chainId = self.reasons['segment_id_mismatch'][chainId]
                            _stats = self.reasons['segment_id_match_stats'][chainId]
                            self.factor['chain_id'] = sorted([k for k, v in _stats.items() if v == _stats[_chainId]])
                            self.factor['alt_chain_id'] = chainId
                        else:
                            chainId_ex = toRegEx(chainId)
                            self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                                       if re.match(chainId_ex, ps['auth_chain_id'])]
                            if self.hasNonPolySeq:
                                for np in self.nonPolySeq:
                                    __chainId = np['auth_chain_id']
                                    if re.match(chainId_ex, __chainId) and __chainId not in self.factor['chain_id']:
                                        self.factor['chain_id'].append(__chainId)
                    if ctx.Symbol_name():
                        symbol_name = chainId = str(ctx.Symbol_name())
                        if symbol_name in self.evaluate:
                            val = self.evaluate[symbol_name]
                            if isinstance(val, list):
                                self.factor['chain_id'] = val
                                self.factor['segment_id'] = val
                            else:
                                self.factor['chain_id'] = [val]
                        else:
                            self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                          f"The symbol {symbol_name!r} is not defined.")
                    if ctx.Integer(0):
                        chainId = str(ctx.Integer(0))
                        self.factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq
                                                   if ps['auth_chain_id'] == self.getRealChainId(chainId, ps['auth_chain_id'])]
                        if self.hasNonPolySeq:
                            for np in self.nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId == self.getRealChainId(chainId, _chainId) and _chainId not in self.factor['chain_id']:
                                    self.factor['chain_id'].append(_chainId)
                        self.factor['segment_id'] = chainId
                        if self.factor['chain_id'] != [chainId]:
                            self.factor['alt_chain_id'] = chainId
                    if len(self.factor['chain_id']) == 0:
                        if self.monoPolymer and not self.hasBranched and not self.hasNonPoly:
                            self.factor['chain_id'] = self.polySeq[0]['auth_chain_id']
                            self.factor['auth_chain_id'] = chainId
                        elif self.reasons is not None:
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
                                                  "Couldn't specify segment name "
                                                  f"'{chainId}' in the coordinates.")  # do not use 'chainId!r' expression, '%' code throws ValueError
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

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0:
                        _factor = copy.copy(self.factor)
                        if 'atom_selection' in __factor:
                            del __factor['atom_selection']
                        del _factor['atom_selection']
                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The 'segidentifier' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                      f"and {self.getReadableFactor(_factor)}.")

            if self.depth > 0 and self.cur_union_expr:
                self.unionFactor = self.factor
            else:
                self.stackFactors.append(self.factor)

        finally:
            self.numberFSelection.clear()

    # Enter a parse tree produced by CharmmMRParser#number.
    def enterNumber(self, ctx: CharmmMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number.
    def exitNumber(self, ctx: CharmmMRParser.NumberContext):
        if ctx.Real():
            self.numberSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        elif ctx.Symbol_name():
            symbol_name = str(ctx.Symbol_name())
            if symbol_name in self.evaluate:
                self.numberSelection.append(float(self.evaluate[symbol_name]))
            else:
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The symbol {symbol_name!r} is not defined.")
                self.numberSelection.append(None)

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by CharmmMRParser#number_f.
    def enterNumber_f(self, ctx: CharmmMRParser.Number_fContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number_f.
    def exitNumber_f(self, ctx: CharmmMRParser.Number_fContext):
        if ctx.Real():
            self.numberFSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberFSelection.append(float(str(ctx.Integer())))

        else:
            self.numberFSelection.append(None)

    # Enter a parse tree produced by CharmmMRParser#number_s.
    def enterNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#number_s.
    def exitNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    def getNumber_s(self, ctx: CharmmMRParser.Number_sContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        if ctx.Symbol_name():
            return str(ctx.Symbol_name())

        return None

    # Enter a parse tree produced by CharmmMRParser#set_statement.
    def enterSet_statement(self, ctx: CharmmMRParser.Set_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmMRParser#set_statement.
    def exitSet_statement(self, ctx: CharmmMRParser.Set_statementContext):
        if ctx.Simple_name_VE(0):

            if ctx.Real_VE():
                self.evaluate[str(ctx.Simple_name_VE(0))] = float(str(ctx.Real_VE()))

            elif ctx.Integer_VE():
                self.evaluate[str(ctx.Simple_name_VE(0))] = int(str(ctx.Integer_VE()))

            elif ctx.Simple_name_VE(1):
                self.evaluate[str(ctx.Simple_name_VE(0))] = str(ctx.Simple_name_VE(1))

# del CharmmMRParser
