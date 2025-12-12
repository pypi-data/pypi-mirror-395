##
# File: CnsMRParserListener.py
# Date: 09-Feb-2022
#
# Updates:
""" ParserLister class for CNS MR files.
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
import numpy

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import (int_atom, ELEMENT_WEIGHTS)  # noqa: F401 pylint: disable=no-name-in-module, import-error
from operator import itemgetter
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.CnsMRParser import CnsMRParser
    from wwpdb.utils.nmr.mr.BaseStackedMRParserListener import (BaseStackedMRParserListener,
                                                                CS_ERROR_MIN,
                                                                CS_ERROR_MAX)
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx,
                                                       translateToStdAtomName,
                                                       hasInterChainRestraint,
                                                       isIdenticalRestraint,
                                                       isLongRangeRestraint,
                                                       isDefinedSegmentRestraint,
                                                       isAsymmetricRangeRestraint,
                                                       isAmbigAtomSelection,
                                                       getAltProtonIdInBondConstraint,
                                                       getTypeOfDihedralRestraint,
                                                       fixBackboneAtomsOfDihedralRestraint,
                                                       isLikePheOrTyr,
                                                       getRdcCode,
                                                       getAuxLoops,
                                                       getRow,
                                                       getAuxRow,
                                                       getStarAtom,
                                                       resetCombinationId,
                                                       resetMemberId,
                                                       getDistConstraintType,
                                                       getPotentialType,
                                                       ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       CS_RESTRAINT_ERROR,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                                       XPLOR_NITROXIDE_NAMES,
                                                       XPLOR_ORIGIN_AXIS_COLS,
                                                       CARTN_DATA_ITEMS,
                                                       AUTH_ATOM_DATA_ITEMS,
                                                       ATOM_NAME_DATA_ITEMS,
                                                       AUTH_ATOM_CARTN_DATA_ITEMS,
                                                       PTNR1_AUTH_ATOM_DATA_ITEMS,
                                                       PTNR2_AUTH_ATOM_DATA_ITEMS)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (MAX_MAG_IDENT_ASYM_ID,
                                           emptyValue,
                                           protonBeginCode,
                                           jcoupBbPairCode,
                                           rdcBbPairCode,
                                           deepcopy)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.CnsMRParser import CnsMRParser
    from nmr.mr.BaseStackedMRParserListener import (BaseStackedMRParserListener,
                                                    CS_ERROR_MIN,
                                                    CS_ERROR_MAX)
    from nmr.mr.ParserListenerUtil import (toRegEx,
                                           hasInterChainRestraint,
                                           isIdenticalRestraint,
                                           isLongRangeRestraint,
                                           isDefinedSegmentRestraint,
                                           isAsymmetricRangeRestraint,
                                           isAmbigAtomSelection,
                                           getAltProtonIdInBondConstraint,
                                           getTypeOfDihedralRestraint,
                                           fixBackboneAtomsOfDihedralRestraint,
                                           isLikePheOrTyr,
                                           getRdcCode,
                                           getAuxLoops,
                                           getRow,
                                           getAuxRow,
                                           getStarAtom,
                                           resetCombinationId,
                                           resetMemberId,
                                           getDistConstraintType,
                                           getPotentialType,
                                           ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           CS_RESTRAINT_ERROR,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                           XPLOR_NITROXIDE_NAMES,
                                           XPLOR_ORIGIN_AXIS_COLS,
                                           CARTN_DATA_ITEMS,
                                           AUTH_ATOM_DATA_ITEMS,
                                           ATOM_NAME_DATA_ITEMS,
                                           AUTH_ATOM_CARTN_DATA_ITEMS,
                                           PTNR1_AUTH_ATOM_DATA_ITEMS,
                                           PTNR2_AUTH_ATOM_DATA_ITEMS)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (MAX_MAG_IDENT_ASYM_ID,
                               emptyValue,
                               protonBeginCode,
                               jcoupBbPairCode,
                               rdcBbPairCode,
                               deepcopy)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance)


# This class defines a complete listener for a parse tree produced by CnsMRParser.
class CnsMRParserListener(ParseTreeListener, BaseStackedMRParserListener):
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

        self.file_type = 'nm-res-cns'
        self.software_name = 'CNS'

    # Enter a parse tree produced by CnsMRParser#cns_mr.
    def enterCns_mr(self, ctx: CnsMRParser.Cns_mrContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#cns_mr.
    def exitCns_mr(self, ctx: CnsMRParser.Cns_mrContext):  # pylint: disable=unused-argument
        self.exit()

    # Enter a parse tree produced by CnsMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CnsMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.distStatements += 1
        self.cur_subtype_altered = self.cur_subtype != 'dist' and len(self.cur_subtype) > 0
        self.cur_subtype = 'dist'

        if self.cur_subtype_altered and not self.preferAuthSeq:
            self.preferAuthSeq = True
            self.authSeqId = 'auth_seq_id'

        self.noePotential = 'biharmonic'  # default potential
        self.noeAverage = 'r-6'  # default averaging method
        self.squareExponent = 2.0
        self.softExponent = 2.0
        self.squareConstant = 20.0
        self.squareOffset = 0.0
        self.rSwitch = 10.0
        self.scale = 1.0
        self.asymptote = 0.0
        self.B_high = 0.01
        self.ceiling = 30.0
        self.temperature = 300.0
        self.monomers = 1
        self.ncount = 2
        self.symmTarget = None
        self.symmDminus = None
        self.symmDplus = None

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CnsMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict and self.cur_subtype == 'dist':
            if self.cur_subtype not in self.lastSfDict:
                return

            sf = self.lastSfDict[self.cur_subtype]

            if 'aux_loops' in sf:
                return

            sf['aux_loops'] = getAuxLoops(self.cur_subtype)

            aux_lp = next((aux_lp for aux_lp in sf['aux_loops'] if aux_lp.category == '_Gen_dist_constraint_software_param'), None)

            if aux_lp is None:
                return

            aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                      {'Type': 'class name', 'Value': self.classification}))
            aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                      {'Type': 'potential function', 'Value': self.noePotential}))
            aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                      {'Type': 'averaging method', 'Value': self.noeAverage}))
            aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                      {'Type': 'scaling constant', 'Value': self.scale}))
            aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                      {'Type': 'ceiling', 'Value': self.ceiling}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'exponent', 'Value': self.squareExponent}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'soft exponent', 'Value': self.softExponent}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'auxiliary scaling constant', 'Value': self.squareConstant}))
            if self.noePotential in ('square', 'softsquare'):
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'negative offset', 'Value': self.squareOffset}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'switch distance', 'Value': self.rSwitch}))
            if self.noePotential == 'softsquare':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'asymptote slope', 'Value': self.asymptote}))
            if self.noePotential == 'high':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'B_high', 'Value': self.B_high}))
            if self.noePotential == 'biharmonic':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'temperature', 'Value': self.temperature}))
            if self.noeAverage == 'sum':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'number monomers', 'Value': self.monomers}))
            if self.noePotential == 'high':
                aux_lp.add_data(getAuxRow(self.cur_subtype, aux_lp.category, sf['list_id'], self.entryId,
                                          {'Type': 'number assign statements', 'Value': self.ncount}))

            sf['saveframe'].add_loop(aux_lp)

        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: CnsMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        self.scale = 1.0

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: CnsMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#plane_restraint.
    def enterPlane_restraint(self, ctx: CnsMRParser.Plane_restraintContext):  # pylint: disable=unused-argument
        self.planeStatements += 1
        self.cur_subtype = 'plane'

        if self.createSfDict:
            self.addSf('planarity restraint')

    # Exit a parse tree produced by CnsMRParser#plane_restraint.
    def exitPlane_restraint(self, ctx: CnsMRParser.Plane_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#harmonic_restraint.
    def enterHarmonic_restraint(self, ctx: CnsMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        self.geoStatements += 1
        self.cur_subtype = 'geo'

        self.squareExponent = 2.0
        self.vector3D = [0.0] * 3

        if self.createSfDict:
            self.addSf('NCS restraint')

    # Exit a parse tree produced by CnsMRParser#harmonic_restraint.
    def exitHarmonic_restraint(self, ctx: CnsMRParser.Harmonic_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: CnsMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.rdcStatements += 1
        self.cur_subtype = 'rdc'

        self.potential = 'square'  # default potential
        self.scale = 1.0

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: CnsMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#coupling_restraint.
    def enterCoupling_restraint(self, ctx: CnsMRParser.Coupling_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.jcoupStatements += 1
        self.cur_subtype = 'jcoup'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#coupling_restraint.
    def exitCoupling_restraint(self, ctx: CnsMRParser.Coupling_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#carbon_shift_restraint.
    def enterCarbon_shift_restraint(self, ctx: CnsMRParser.Carbon_shift_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.hvycsStatements += 1
        self.cur_subtype = 'hvycs'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#carbon_shift_restraint.
    def exitCarbon_shift_restraint(self, ctx: CnsMRParser.Carbon_shift_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#proton_shift_restraint.
    def enterProton_shift_restraint(self, ctx: CnsMRParser.Proton_shift_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.procsStatements += 1
        self.cur_subtype = 'procs'

        if self.createSfDict:
            self.addSf()

    # Exit a parse tree produced by CnsMRParser#proton_shift_restraint.
    def exitProton_shift_restraint(self, ctx: CnsMRParser.Proton_shift_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#conformation_db_restraint.
    def enterConformation_db_restraint(self, ctx: CnsMRParser.Conformation_db_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.ramaStatements += 1
        self.cur_subtype = 'rama'

        if self.createSfDict:
            self.addSf('dihedral angle database restraint')

    # Exit a parse tree produced by CnsMRParser#conformation_db_restraint.
    def exitConformation_db_restraint(self, ctx: CnsMRParser.Conformation_db_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#diffusion_anisotropy_restraint.
    def enterDiffusion_anisotropy_restraint(self, ctx: CnsMRParser.Diffusion_anisotropy_restraintContext):  # pylint: disable=unused-argument
        self.classification = '.'

        self.diffStatements += 1
        self.cur_subtype = 'diff'

        if self.createSfDict:
            self.addSf('diffusion anisotropy restraint')

    # Exit a parse tree produced by CnsMRParser#diffusion_anisotropy_restraint.
    def exitDiffusion_anisotropy_restraint(self, ctx: CnsMRParser.Diffusion_anisotropy_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#one_bond_coupling_restraint.
    def enterOne_bond_coupling_restraint(self, ctx: CnsMRParser.One_bond_coupling_restraintContext):  # pylint: disable=unused-argument
        """
        @deprecated: This restraint has not been useful in practice, but has been preserved for historical reasons.
        """

    # Exit a parse tree produced by CnsMRParser#one_bond_coupling_restraint.
    def exitOne_bond_coupling_restraint(self, ctx: CnsMRParser.One_bond_coupling_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#angle_db_restraint.
    def enterAngle_db_restraint(self, ctx: CnsMRParser.Angle_db_restraintContext):  # pylint: disable=unused-argument
        """
        @deprecated:  This term has not proved useful in practice and is only here for historical reasons.
        """

    # Exit a parse tree produced by CnsMRParser#angle_db_restraint.
    def exitAngle_db_restraint(self, ctx: CnsMRParser.Angle_db_restraintContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#noe_statement.
    def enterNoe_statement(self, ctx: CnsMRParser.Noe_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('BIHA'):
                self.noePotential = 'biharmonic'
            elif code.startswith('LOGN'):
                self.noePotential = 'lognormal'
            elif code.startswith('SQUA'):
                self.noePotential = 'square'
            elif code.startswith('SOFT'):
                self.noePotential = 'softsquare'
            elif code.startswith('SYMM'):
                self.noePotential = 'symmetry'
            elif code.startswith('HIGH'):
                self.noePotential = 'high'
            elif code.startswith('3DPO'):
                self.noePotential = '3dpo'
            else:
                self.noePotential = 'biharmonic'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'NOE' statements. "
                              f"Instead, set the default potential {self.noePotential!r}.")

        elif ctx.Averaging_methods():
            code = str(ctx.Averaging_methods()).upper()
            if code == 'R-6':
                self.noeAverage = 'r-6'
            elif code == 'R-3':
                self.noeAverage = 'r-3'
            elif code == 'SUM':
                self.noeAverage = 'sum'
            elif code.startswith('CENT'):
                self.noeAverage = 'center'
            else:
                self.noeAverage = 'r-6'
                self.f.append("[Enum mismatch ignorable] "
                              f"The averaging method {str(ctx.Averaging_methods())!r} is unknown method for the 'NOE' statements. "
                              f"Instead, set the default method {self.noeAverage!r}.")

        elif ctx.SqExponent():
            self.squareExponent = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.squareExponent, str):
                if self.squareExponent in self.evaluate:
                    self.squareExponent = self.evaluate[self.squareExponent]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.squareExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareExponent = 2.0
            if self.squareExponent is None or self.squareExponent <= 0.0:
                self.f.append("[Invalid data] "
                              "The exponent value of square-well or soft-square function "
                              f"'NOE {str(ctx.SqExponent())} {self.getClass_name(ctx.class_name(0))} {self.squareExponent} END' must be a positive value.")

        elif ctx.SoExponent():
            self.softExponent = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.softExponent, str):
                if self.softExponent in self.evaluate:
                    self.softExponent = self.evaluate[self.softExponent]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.softExponent!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.softExponent = 2.0
            if self.softExponent is None or self.softExponent <= 0.0:
                self.f.append("[Invalid data] "
                              "The exponent value for soft-square function only "
                              f"'NOE {str(ctx.SoExponent())} {self.getClass_name(ctx.class_name(0))} {self.softExponent} END' must be a positive value.")

        elif ctx.SqConstant():
            self.squareConstant = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.squareConstant, str):
                if self.squareConstant in self.evaluate:
                    self.squareConstant = self.evaluate[self.squareConstant]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.squareConstant!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareConstant = 20.0
            if self.squareConstant is None or self.squareConstant <= 0.0:
                self.f.append("[Invalid data] "
                              "The auxiliary scaling constant of square-well or soft-square function "
                              f"'NOE {str(ctx.SqConstant())} {self.getClass_name(ctx.class_name(0))} {self.squareConstant} END' must be a positive value.")

        elif ctx.SqOffset():
            self.squareOffset = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.squareOffset, str):
                if self.squareOffset in self.evaluate:
                    self.squareOffset = self.evaluate[self.squareOffset]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.squareOffset!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.squareOffset = 0.0
            if self.squareOffset is None or self.squareOffset < 0.0:
                self.f.append("[Invalid data] "
                              "The negative offset value to all upper bounds of square-well or soft-square function "
                              f"'NOE {str(ctx.SqOffset())} {self.getClass_name(ctx.class_name(0))} {self.squareOffset} END' must not be a negative value.")

        elif ctx.Rswitch():
            self.rSwitch = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.rSwitch, str):
                if self.rSwitch in self.evaluate:
                    self.rSwitch = self.evaluate[self.rSwitch]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.rSwitch!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.rSwitch = 10.0
            if self.rSwitch is None or self.rSwitch < 0.0:
                self.f.append("[Invalid data] "
                              "The smoothing parameter of soft-square function "
                              f"'NOE {str(ctx.Rswitch())} {self.getClass_name(ctx.class_name(0))} {self.rSwitch} END' must not be a negative value.")

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
                              f"The scale value 'NOE {str(ctx.Scale())} {self.getClass_name(ctx.class_name(0))} {self.scale} END' should be a positive value.")
            elif self.scale < 0.0:
                self.f.append("[Invalid data] "
                              f"The scale value 'NOE {str(ctx.Scale())} {self.getClass_name(ctx.class_name(0))} {self.scale} END' must not be a negative value.")

        elif ctx.Asymptote():
            self.asymptote = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.asymptote, str):
                if self.asymptote in self.evaluate:
                    self.asymptote = self.evaluate[self.asymptote]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.asymptote!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.asymptote = 0.0
            if self.asymptote is None:
                self.f.append("[Range value warning] "
                              "The asymptote slope value "
                              f"'NOE {str(ctx.Asymptote())} {self.getClass_name(ctx.class_name(0))} {self.asymptote} END' should be a non-negative value.")
            elif self.asymptote < 0.0:
                self.f.append("[Invalid data] "
                              "The asymptote slope value "
                              f"'NOE {str(ctx.Asymptote())} {self.getClass_name(ctx.class_name(0))} {self.asymptote} END' must not be a negative value.")

        elif ctx.Bhig():
            self.B_high = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.B_high, str):
                if self.B_high in self.evaluate:
                    self.B_high = self.evaluate[self.B_high]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.B_high!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.B_high = 0.01
            if self.B_high is None:
                self.f.append("[Range value warning] "
                              "The potential barrier value "
                              f"'NOE {str(ctx.Bhig())} {self.getClass_name(ctx.class_name(0))} {self.B_high} END' should be a non-negative value.")
            elif self.B_high < 0.0:
                self.f.append("[Invalid data] "
                              "The potential barrier value "
                              f"'NOE {str(ctx.Bhig())} {self.getClass_name(ctx.class_name(0))} {self.B_high} END' must not be a negative value.")

        elif ctx.Ceiling():
            self.ceiling = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.ceiling, str):
                if self.ceiling in self.evaluate:
                    self.ceiling = self.evaluate[self.ceiling]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.ceiling!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.ceiling = 30.0
            if self.ceiling is None:
                self.f.append("[Range value warning] "
                              "The ceiling value for energy constant "
                              f"'NOE {str(ctx.Ceiling())} {self.ceiling} END' should be a non-negative value.")
            elif self.ceiling < 0.0:
                self.f.append("[Invalid data] "
                              "The ceiling value for energy constant "
                              f"'NOE {str(ctx.Ceiling())} {self.ceiling} END' must not be a negative value.")

        elif ctx.Temperature():
            self.temperature = self.getNumber_s(ctx.number_s(0))
            if isinstance(self.temperature, str):
                if self.temperature in self.evaluate:
                    self.temperature = self.evaluate[self.temperature]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The symbol {self.temperature!r} in the 'NOE' statement is not defined so that set the default value.")
                    self.temperature = 300.0
            if self.temperature is None:
                self.f.append("[Range value warning] "
                              f"The temperature 'NOE {str(ctx.Temparature())} {self.temperature} END' should be a non-negative value.")
            elif self.temperature < 0.0:
                self.f.append("[Invalid data] "
                              f"The temperature 'NOE {str(ctx.Temparature())} {self.temperature} END' must not be a negative value.")

        elif ctx.Monomers():
            self.monomers = int(str(ctx.Integer()))
            if self.monomers is None or self.monomers == 0:
                self.f.append("[Range value warning] "
                              "The number of monomers "
                              f"'NOE {str(ctx.Monomers())} {self.getClass_name(ctx.class_name(0))} {self.monomers} END' should be a positive value.")
            elif self.monomers < 0:
                self.f.append("[Invalid data] "
                              "The number of monomers "
                              f"'NOE {str(ctx.Monomers())} {self.getClass_name(ctx.class_name(0))} {self.monomers} END' must not be a negative value.")

        elif ctx.Ncount():
            self.ncount = int(str(ctx.Integer()))
            if self.ncount is None or self.ncount == 0:
                self.f.append("[Range value warning] "
                              "The number of assign statements "
                              f"'NOE {str(ctx.Ncount())} {self.getClass_name(ctx.class_name(0))} {self.ncount} END' should be a positive value.")
            elif self.ncount < 0:
                self.f.append("[Invalid data] "
                              "The number of assign statements "
                              f"'NOE {str(ctx.Ncount())} {self.getClass_name(ctx.class_name(0))} {self.ncount} END' must not be a negative value.")

        elif ctx.Reset():
            self.noePotential = 'biharmonic'  # default potential
            self.squareExponent = 2.0
            self.softExponent = 2.0
            self.squareConstant = 20.0
            self.squareOffset = 0.0
            self.rSwitch = 10.0
            self.scale = 1.0
            self.asymptote = 0.0
            self.B_high = 0.01
            self.ceiling = 30.0
            self.temperature = 300.0
            self.monomers = 1
            self.ncount = 2
            self.symmTarget = None
            self.symmDminus = None
            self.symmDplus = None

    # Exit a parse tree produced by CnsMRParser#noe_statement.
    def exitNoe_statement(self, ctx: CnsMRParser.Noe_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (NOE) classification={self.classification!r}")

    # Enter a parse tree produced by CnsMRParser#noe_assign.
    def enterNoe_assign(self, ctx: CnsMRParser.Noe_assignContext):  # pylint: disable=unused-argument
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

        self.scale_a = None
        self.has_nx = False

    # Exit a parse tree produced by CnsMRParser#noe_assign.
    def exitNoe_assign(self, ctx: CnsMRParser.Noe_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.distRestraints -= 1
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 2:
                dminus = self.numberSelection[1]
                dplus = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                dminus = dplus = self.numberSelection[1]

            else:
                dminus = dplus = 0.0

            scale = self.scale if self.scale_a is None else self.scale_a

            if scale < 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The weight value '{scale}' must not be a negative value.")
                return
            if scale == 0.0:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The weight value '{scale}' should be a positive value.")

            target_value = target
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            if self.noePotential == 'biharmonic':
                lower_limit = target - dminus
                upper_limit = target + dplus
            elif self.noePotential == 'lognormal':
                pass
            elif self.noePotential == 'square':
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'softsquare':
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                    upper_linear_limit = target + dplus - self.squareOffset + self.rSwitch
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'symmetry':
                if target == 0.0:
                    target = self.symmTarget
                    dminus = self.symmDminus
                    dplus = self.symmDplus
                else:
                    self.symmTarget = target
                    self.symmDminus = dminus
                    self.symmDplus = dplus
                target_value = target
                if abs(self.squareExponent - 2.0) < abs(self.squareExponent - 1.0):
                    lower_linear = target - dminus
                    upper_linear = target + dplus - self.squareOffset
                    upper_linear_limit = target + dplus - self.squareOffset + self.rSwitch
                else:
                    lower_linear_limit = target - dminus
                    upper_linear_limit = target + dplus - self.squareOffset
            elif self.noePotential == 'high':
                lower_linear = target - dminus
                upper_linear = target + dplus
                lower_linear_limit = lower_linear - 0.1
                upper_linear_limit = upper_linear + 0.1
            else:  # 3dpo
                if target == 0.0:
                    target = self.symmTarget
                    dminus = self.symmDminus
                    dplus = self.symmDplus
                else:
                    self.symmTarget = target
                    self.symmDminus = dminus
                    self.symmDplus = dplus
                target_value = target
                lower_limit = target - dminus
                upper_limit = target + dplus

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

            dstFunc = self.validateDistanceRange(scale,
                                                 target_value, lower_limit, upper_limit,
                                                 lower_linear_limit, upper_linear_limit)

            if dstFunc is None:
                return

            if 0 in (len(self.atomSelectionSet[0]), len(self.atomSelectionSet[1])):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            combinationId = memberId = memberLogicCode = '.'
            if self.createSfDict:
                sf = self.getSf(constraintType=getDistConstraintType(self.atomSelectionSet, dstFunc,
                                                                     self.csStat, self.originalFileName),
                                potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))
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
                for atom1, atom2 in (itertools.product(self.atomSelectionSet[i],
                                                       self.atomSelectionSet[i + 1])
                                     if not self.in_loop else
                                     zip(self.atomSelectionSet[i],
                                         self.atomSelectionSet[i + 1])):
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

    # Enter a parse tree produced by CnsMRParser#predict_statement.
    def enterPredict_statement(self, ctx: CnsMRParser.Predict_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#predict_statement.
    def exitPredict_statement(self, ctx: CnsMRParser.Predict_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#noe_annotation.
    def enterNoe_annotation(self, ctx: CnsMRParser.Noe_annotationContext):
        if ctx.Weight():
            self.scale_a = self.getNumber_a(ctx.number_a())

    # Exit a parse tree produced by CnsMRParser#noe_annotation.
    def exitNoe_annotation(self, ctx: CnsMRParser.Noe_annotationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#dihedral_statement.
    def enterDihedral_statement(self, ctx: CnsMRParser.Dihedral_statementContext):
        if ctx.Scale():
            self.scale = self.getNumber_s(ctx.number_s())
            if isinstance(self.scale, str):
                if self.scale in self.evaluate:
                    self.scale = self.evaluate[self.scale]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' "
                                  f"where the symbol {self.scale!r} is not defined so that set the default value.")
                    self.scale = 1.0
            if self.scale < 0.0:
                self.f.append("[Invalid data] "
                              f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' must not be a negative value.")
            elif self.scale == 0.0:
                self.f.append("[Range value warning] "
                              f"The scale value 'RESTRAINTS DIHEDRAL {str(ctx.Scale())}={self.scale} END' should be a positive value.")

        elif ctx.Reset():
            self.scale = 1.0

    # Exit a parse tree produced by CnsMRParser#dihedral_statement.
    def exitDihedral_statement(self, ctx: CnsMRParser.Dihedral_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#dihedral_assign.
    def enterDihedral_assign(self, ctx: CnsMRParser.Dihedral_assignContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1
        if self.cur_subtype != 'dihed':
            self.dihedStatements += 1
        self.cur_subtype = 'dihed'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#dihedral_assign.
    def exitDihedral_assign(self, ctx: CnsMRParser.Dihedral_assignContext):

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            energyConst = self.numberSelection[0]
            target = self.numberSelection[1]
            delta = abs(self.numberSelection[2])
            exponent = int(str(ctx.Integer()))

            if energyConst <= 0.0:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"The energy constant value {energyConst} must be a positive value.")
                return

            if exponent not in (0, 1, 2, 4):
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The exponent value of dihedral angle restraint 'ed={exponent}' should be 1 (linear well), 2 (square well) or 4 (quartic well) "
                              "so that set the default exponent value (square well).")
                exponent = 2

            target_value = target
            lower_limit = None
            upper_limit = None
            lower_linear_limit = None
            upper_linear_limit = None

            if delta > 0.0:
                if exponent in (2, 4):
                    lower_limit = target - delta
                    upper_limit = target + delta
                else:
                    lower_linear_limit = target - delta
                    upper_linear_limit = target + delta

            dstFunc = self.validateAngleRange(self.scale if exponent > 0 else 0.0, {'energy_const': energyConst, 'exponent': exponent},
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
                if not self.areUniqueCoordAtoms('a dihedral angle (DIHE)'):
                    if len(self.g) > 0:
                        self.f.extend(self.g)
                return

            len_f = len(self.f)
            self.areUniqueCoordAtoms('a dihedral angle (DIHE)',
                                     allow_ambig=True, allow_ambig_warn_title='Ambiguous dihedral angle')
            combinationId = '.' if len_f == len(self.f) else 0

            atomSelTotal = sum(len(s) for s in self.atomSelectionSet)

            in_loop = self.in_loop and atomSelTotal > 4\
                and atomSelTotal % 4 == 0 and all(len(s) == atomSelTotal / 4 for s in self.atomSelectionSet)

            if isinstance(combinationId, int):
                fixedAngleName = '.'
                for atom1, atom2, atom3, atom4 in (itertools.product(self.atomSelectionSet[0],
                                                                     self.atomSelectionSet[1],
                                                                     self.atomSelectionSet[2],
                                                                     self.atomSelectionSet[3])
                                                   if not in_loop else
                                                   zip(self.atomSelectionSet[0],
                                                       self.atomSelectionSet[1],
                                                       self.atomSelectionSet[2],
                                                       self.atomSelectionSet[3])):
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

                    if angleName in emptyValue and atomSelTotal != 4 and not in_loop:
                        continue

                    fixedAngleName = angleName
                    break

            sf = None
            if self.createSfDict:
                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc))

            first_item = True

            for atom1, atom2, atom3, atom4 in (itertools.product(self.atomSelectionSet[0],
                                                                 self.atomSelectionSet[1],
                                                                 self.atomSelectionSet[2],
                                                                 self.atomSelectionSet[3])
                                               if not in_loop else
                                               zip(self.atomSelectionSet[0],
                                                   self.atomSelectionSet[1],
                                                   self.atomSelectionSet[2],
                                                   self.atomSelectionSet[3])):
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

                if angleName in emptyValue and atomSelTotal != 4 and not in_loop:
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
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#plane_statement.
    def enterPlane_statement(self, ctx: CnsMRParser.Plane_statementContext):
        if ctx.Initialize():
            self.planeWeight = 300.0

    # Exit a parse tree produced by CnsMRParser#plane_statement.
    def exitPlane_statement(self, ctx: CnsMRParser.Plane_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#plane_group.
    def enterPlane_group(self, ctx: CnsMRParser.Plane_groupContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#plane_group.
    def exitPlane_group(self, ctx: CnsMRParser.Plane_groupContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#group_statement.
    def enterGroup_statement(self, ctx: CnsMRParser.Group_statementContext):
        self.planeRestraints += 1
        if self.cur_subtype != 'plane':
            self.planeStatements += 1
        self.cur_subtype = 'plane'

        self.atomSelectionSet.clear()
        self.g.clear()

        if ctx.Weight():
            self.planeWeight = self.getNumber_s(ctx.number_s())
            if isinstance(self.planeWeight, str):
                if self.planeWeight in self.evaluate:
                    self.planeWeight = self.evaluate[self.planeWeight]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' "
                                  f"where the symbol {self.planeWeight!r} is not defined so that set the default value.")
                    self.planeWeight = 300.0
            if self.planeWeight < 0.0:
                self.f.append("[Invalid data] "
                              f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' must not be a negative value.")
            elif self.planeWeight == 0.0:
                self.f.append("[Range value warning] "
                              f"The weight value 'GROUP {str(ctx.Weight())}={self.planeWeight} END' should be a positive value.")

    # Exit a parse tree produced by CnsMRParser#group_statement.
    def exitGroup_statement(self, ctx: CnsMRParser.Group_statementContext):  # pylint: disable=unused-argument
        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        if len(self.atomSelectionSet) == 0:
            return

        if self.createSfDict:
            sf = self.getSf('planarity restraint')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'list_id']
                sf['tags'].append(['weight', self.planeWeight])

        for atom1 in self.atomSelectionSet[0]:
            if self.debug:
                print(f"subtype={self.cur_subtype} (PLANE/GROUP) id={self.planeRestraints} "
                      f"atom={atom1} weight={self.planeWeight}")
            if self.createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           sf['list_id']])

    # Enter a parse tree produced by CnsMRParser#harmonic_statement.
    def enterHarmonic_statement(self, ctx: CnsMRParser.Harmonic_statementContext):
        if ctx.Exponent():
            self.squareExponent = int(str(ctx.Integer()))
            if self.squareExponent <= 0.0:
                self.f.append("[Invalid data] "
                              "The exponent value  "
                              f"'RESTRAINTS HARMONIC {str(ctx.Exponent())}={self.squareExponent} END' must be a positive value.")

        elif ctx.Normal():
            if ctx.number_s(0):
                self.vector3D = [self.getNumber_s(ctx.number_s(0)),
                                 self.getNumber_s(ctx.number_s(1)),
                                 self.getNumber_s(ctx.number_s(2))]

            elif ctx.Tail():
                self.inVector3D = True
                self.inVector3D_columnSel = -1
                self.inVector3D_tail = None
                self.inVector3D_head = None
                self.vector3D = None

    # Exit a parse tree produced by CnsMRParser#harmonic_statement.
    def exitHarmonic_statement(self, ctx: CnsMRParser.Harmonic_statementContext):  # pylint: disable=unused-argument
        if self.vector3D is None:
            self.vector3D = [0.0] * 3  # set default vector if not available

        if 'harm' not in self.vectorDo or len(self.vector3D['harm']) == 0:
            self.f.append("[Invalid data] "
                          "No vector statement for harmonic coordinate restraints exists.")
            return

        for col, vector in enumerate(self.vector3D['harm'], start=1):
            dstFunc = {}
            if 'value' in vector:
                dstFunc['energy_const'] = vector['value']
            dstFunc['exponent'] = self.squareExponent
            for atom1 in vector['atom_selection']:
                if self.debug:
                    print(f"subtype={self.cur_subtype} (HARM) id={col} "
                          f"atom={atom1} {dstFunc} normal_vector={self.vector3D}")

        self.vector3D['harm'] = []

    # Enter a parse tree produced by CnsMRParser#harmonic_assign.
    def enterHarmonic_assign(self, ctx: CnsMRParser.Harmonic_assignContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        if self.cur_subtype != 'geo':
            self.geoStatements += 1
        self.cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#harmonic_assign.
    def exitHarmonic_assign(self, ctx: CnsMRParser.Harmonic_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.geoRestraints -= 1
                return

            self.vector3D = [self.numberSelection[0], self.numberSelection[1], self.numberSelection[2]]

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            for atom1 in self.atomSelectionSet[0]:
                if self.debug:
                    print(f"subtype={self.cur_subtype} (HARM) id={self.geoRestraints} "
                          f"atom={atom1} normal_vector={self.vector3D}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#sani_statement.
    def enterSani_statement(self, ctx: CnsMRParser.Sani_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'SANIsotropy' statements. "
                              f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'DFS': self.getNumber_s(ctx.number_s(0)),
                                 'anisotropy': self.getNumber_s(ctx.number_s(1)),
                                 'rhombicity': self.getNumber_s(ctx.number_s(2))
                                 }

    # Exit a parse tree produced by CnsMRParser#sani_statement.
    def exitSani_statement(self, ctx: CnsMRParser.Sani_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (SANI) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by CnsMRParser#sani_assign.
    def enterSani_assign(self, ctx: CnsMRParser.Sani_assignContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1
        if self.cur_subtype != 'rdc':
            self.rdcStatements += 1
        self.cur_subtype = 'rdc'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#sani_assign.
    def exitSani_assign(self, ctx: CnsMRParser.Sani_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta
                if len(self.numberSelection) > 2:
                    error_less = delta
                    error_greater = abs(self.numberSelection[2])
                    lower_limit = target - error_less
                    upper_limit = target + error_greater

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return
            """
            if not self.areUniqueCoordAtoms('an RDC (SANI)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return
            """
            try:
                chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[5][0]['atom_id']
            except IndexError:
                if not self.areUniqueCoordAtoms('an RDC (SANI)', XPLOR_ORIGIN_AXIS_COLS):
                    if len(self.g) > 0:
                        self.f.extend(self.g)
                return

            chain_id_set = None
            if self.exptlMethod == 'SOLID-STATE NMR':
                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                if ps is not None:
                    chain_id_set = [chain_id_1]
                    chain_id_set.extend(ps['identical_auth_chain_id'])
                    chain_id_set.sort()
                    if self.symmetric != 'no':
                        pass
                    elif len(chain_id_set) > MAX_MAG_IDENT_ASYM_ID and chain_id_2 in chain_id_set:
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
                                self.log.write(f"+{self.__class_name__}.exitSani_assign() ++ Error  - {str(e)}")

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in RDC vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                if self.symmetric == 'no':
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
                    warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Anomalous RDC vector'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
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
                    warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Anomalous RDC vector'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                  "Found inter-residue RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                if self.symmetric == 'no':
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found zero RDC vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        if atom_id_1[0] in protonBeginCode and atom_id_2[0] in protonBeginCode:
                            self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                          "Found an RDC vector over multiple covalent bonds in the 'SANIsotropy' statement; "
                                          f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}). "
                                          "Did you accidentally select 'SANIsotropy' statement, instead of 'XDIPolar' statement of XPLOR-NIH?")
                        else:
                            self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                          "Found an RDC vector over multiple covalent bonds in the 'SANIsotropy' statement; "
                                          f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")

            combinationId = '.'
            if self.createSfDict:
                sf = self.getSf(potentialType=getPotentialType(self.file_type, self.cur_subtype, dstFunc),
                                rdcCode=getRdcCode([self.atomSelectionSet[4][0], self.atomSelectionSet[5][0]]))
                sf['id'] += 1
                if len(self.atomSelectionSet[4]) > 1 or len(self.atomSelectionSet[5]) > 1:
                    combinationId = 0

            for atom1, atom2 in (itertools.product(self.atomSelectionSet[4],
                                                   self.atomSelectionSet[5])
                                 if not self.in_loop else
                                 zip(self.atomSelectionSet[4],
                                     self.atomSelectionSet[5])):
                atoms = [atom1, atom2]
                if isDefinedSegmentRestraint(atoms):
                    continue
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if self.symmetric == 'no':
                    if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                        continue
                else:
                    if isAsymmetricRangeRestraint(atoms, chain_id_set, self.symmetric):
                        continue
                    if atom1['chain_id'] != atom2['chain_id']:
                        self.f.append(f"[Anomalous RDC vector] {self.getCurrentRestraint()}"
                                      "Found inter-chain RDC vector; "
                                      f"({atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']}, "
                                      f"{atom2['chain_id']}:{atom2['seq_id']}:{atom2['comp_id']}:{atom2['atom_id']}). "
                                      "However, it might be an artificial RDC constraint on solid-state NMR applied to symmetric samples such as fibrils.")
                if isinstance(combinationId, int):
                    combinationId += 1
                if self.debug:
                    print(f"subtype={self.cur_subtype} (SANI) id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 combinationId, None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2)
                    sf['loop'].add_data(row)

            if self.createSfDict and sf is not None and isinstance(combinationId, int) and combinationId == 1:
                sf['loop'].data[-1] = resetCombinationId(self.cur_subtype, sf['loop'].data[-1])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#coupling_statement.
    def enterCoupling_statement(self, ctx: CnsMRParser.Coupling_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            elif code.startswith('MULT'):
                self.potential = 'multiple'
            else:
                self.potential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'COUPling' statements. "
                              f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

        elif ctx.Coefficients():
            self.coefficients = {'Karplus_coef_a': self.getNumber_s(ctx.number_s(0)),
                                 'Karplus_coef_b': self.getNumber_s(ctx.number_s(1)),
                                 'Karplus_coef_c': self.getNumber_s(ctx.number_s(2)),
                                 'Karplus_phase': self.getNumber_s(ctx.number_s(3))
                                 }

    # Exit a parse tree produced by CnsMRParser#coupling_statement.
    def exitCoupling_statement(self, ctx: CnsMRParser.Coupling_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (COUP) classification={self.classification!r} "
                  f"coefficients={self.coefficients}")

    # Enter a parse tree produced by CnsMRParser#coup_assign.
    def enterCoup_assign(self, ctx: CnsMRParser.Coup_assignContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1
        if self.cur_subtype != 'jcoup':
            self.jcoupStatements += 1
        self.cur_subtype = 'jcoup'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#coup_assign.
    def exitCoup_assign(self, ctx: CnsMRParser.Coup_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            target = self.numberSelection[0]
            delta = abs(self.numberSelection[1])

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential != 'harmonic' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateRdcRange(1.0, {'potential': self.potential},
                                            target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            dstFunc2 = None

            if len(self.numberSelection) > 3:
                target = self.numberSelection[2]
                delta = abs(self.numberSelection[3])

                target_value = target
                lower_limit = None
                upper_limit = None

                if self.potential != 'harmonic' and delta > 0.0:
                    lower_limit = target - delta
                    upper_limit = target + delta

                dstFunc2 = self.validateRdcRange(1.0, {'potential': self.potential},
                                                 target_value, lower_limit, upper_limit)

                if dstFunc2 is None:
                    return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a J-coupling (COUP)'):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            for i in range(0, len(self.atomSelectionSet), 4):
                chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[i + 3][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[i + 3][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[i + 3][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[i + 3][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Non-magnetic susceptible spin appears in J-coupling vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                                  f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found inter-chain J-coupling vector; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:
                    if abs(seq_id_1 - seq_id_2) > 2 or {atom_id_1, atom_id_2} != {'H', 'N'}:
                        warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                        self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                      "Found inter-residue J-coupling vector; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.csStat.peptideLike(comp_id_1) and self.csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in jcoupBbPairCode)
                             or (seq_id_1 > seq_id_2 and atom_id_1 in jcoupBbPairCode and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 in ('H', 'N'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('H', 'N') and atom_id_2.startswith('HA'))
                             or {atom_id_1, atom_id_2} == {'H', 'N'}):
                        pass

                    elif self.csStat.getTypeOfCompId(comp_id_1)[1] and self.csStat.getTypeOfCompId(comp_id_1)[1]\
                            and seq_id_1 < seq_id_2 and atom_id_2 == 'P':
                        pass

                    else:
                        warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                        self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                      "Found inter-residue J-coupling vector; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

                elif atom_id_1 == atom_id_2:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found zero J-coupling vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            if self.createSfDict:
                sf = self.getSf(self.classification)
                sf['id'] += 1

            if len(self.atomSelectionSet) == 4:
                for atom1, atom2, atom3, atom4 in (itertools.product(self.atomSelectionSet[0],
                                                                     self.atomSelectionSet[1],
                                                                     self.atomSelectionSet[2],
                                                                     self.atomSelectionSet[3])
                                                   if not self.in_loop else
                                                   zip(self.atomSelectionSet[0],
                                                       self.atomSelectionSet[1],
                                                       self.atomSelectionSet[2],
                                                       self.atomSelectionSet[3])):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (COUP) id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

            else:
                for atom1, atom2, atom3, atom4 in (itertools.product(self.atomSelectionSet[0],
                                                                     self.atomSelectionSet[1],
                                                                     self.atomSelectionSet[2],
                                                                     self.atomSelectionSet[3])
                                                   if not self.in_loop else
                                                   zip(self.atomSelectionSet[0],
                                                       self.atomSelectionSet[1],
                                                       self.atomSelectionSet[2],
                                                       self.atomSelectionSet[3])):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (COUP) id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

                for atom1, atom2, atom3, atom4 in (itertools.product(self.atomSelectionSet[4],
                                                                     self.atomSelectionSet[5],
                                                                     self.atomSelectionSet[6],
                                                                     self.atomSelectionSet[7])
                                                   if not self.in_loop else
                                                   zip(self.atomSelectionSet[4],
                                                       self.atomSelectionSet[5],
                                                       self.atomSelectionSet[6],
                                                       self.atomSelectionSet[7])):
                    if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                        if {atom1['atom_id'], atom4['atom_id']} != {'H', 'N'}:
                            continue
                    if self.debug:
                        if dstFunc2 is None:
                            print(f"subtype={self.cur_subtype} (COUP) id={self.jcoupRestraints} "
                                  f"atom4={atom1} atom5={atom2} atom6={atom3} atom7={atom4} {dstFunc}")
                        else:
                            print(f"subtype={self.cur_subtype} (COUP) id={self.jcoupRestraints} "
                                  f"atom4={atom1} atom5={atom2} atom6={atom3} atom7={atom4} {dstFunc2}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     '.', None, None,
                                     sf['list_id'], self.entryId, dstFunc if dstFunc2 is None else dstFunc2,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#carbon_shift_statement.
    def enterCarbon_shift_statement(self, ctx: CnsMRParser.Carbon_shift_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            else:
                self.potential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'CARBon' statements. "
                              f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'

        elif ctx.Expectation():
            self.csExpect = {'psi_position': int(str(ctx.Integer(0))),
                             'phi_poistion': int(str(ctx.Integer(1))),
                             'ca_shift': self.getNumber_s(ctx.number_s(0)),
                             'ca_shift_error': self.getNumber_s(ctx.number_s(1)),
                             'cb_shift': self.getNumber_s(ctx.number_s(2)),
                             'cb_shift_error': self.getNumber_s(ctx.number_s(3))
                             }

    # Exit a parse tree produced by CnsMRParser#carbon_shift_statement.
    def exitCarbon_shift_statement(self, ctx: CnsMRParser.Carbon_shift_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (CARB) classification={self.classification!r} "
                  f"expectation={self.csExpect}")

    # Enter a parse tree produced by CnsMRParser#carbon_shift_assign.
    def enterCarbon_shift_assign(self, ctx: CnsMRParser.Carbon_shift_assignContext):  # pylint: disable=unused-argument
        self.hvycsRestraints += 1
        self.cur_subtype = 'hvycs'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#carbon_shift_assign.
    def exitCarbon_shift_assign(self, ctx: CnsMRParser.Carbon_shift_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.hvycsRestraints -= 1
                return

            ca_shift = self.numberSelection[0]
            cb_shift = self.numberSelection[1]

            if CS_ERROR_MIN < ca_shift < CS_ERROR_MAX:
                pass
            else:
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"CA chemical shift value '{ca_shift}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a carbon chemical shift (CARB)'):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            dstFunc = {'ca_shift': ca_shift, 'cb_shift': cb_shift, 'weight': 1.0, 'potential': self.potential}

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
            seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
            atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

            chain_id_4 = self.atomSelectionSet[3][0]['chain_id']
            seq_id_4 = self.atomSelectionSet[3][0]['seq_id']
            atom_id_4 = self.atomSelectionSet[3][0]['atom_id']

            chain_id_5 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_5 = self.atomSelectionSet[4][0]['seq_id']
            atom_id_5 = self.atomSelectionSet[4][0]['atom_id']

            chain_ids = [chain_id_1, chain_id_2, chain_id_3, chain_id_4, chain_id_5]
            seq_ids = [seq_id_1, seq_id_2, seq_id_3, seq_id_4, seq_id_5]
            offsets = [seq_id - seq_id_3 for seq_id in seq_ids]
            atom_ids = [atom_id_1, atom_id_2, atom_id_3, atom_id_4, atom_id_5]

            ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_3), None)

            if ps is not None and chain_ids == [chain_id_1] * 5 and atom_ids == ['C', 'N', 'CA', 'C', 'N']\
               and offsets != [-1, 0, 0, 0, 1]:

                try:
                    _seq_ids = [ps['seq_id'][ps['auth_seq_id'].index(seq_id)] for seq_id in seq_ids]
                    _seq_id_3 = _seq_ids[2]
                    offsets = [seq_id - _seq_id_3 for seq_id in _seq_ids]
                except (IndexError, ValueError):
                    pass

            if chain_ids != [chain_id_1] * 5 or offsets != [-1, 0, 0, 0, 1] or atom_ids != ['C', 'N', 'CA', 'C', 'N']:

                if ps is not None:

                    if ps['auth_seq_id'][0] == seq_id_3 and atom_ids[0] == 'C':
                        hint = f"'{seq_id_3 - 1}'"
                        if ps['seq_id'][0] != seq_id_3:
                            hint += f" (or '{ps['seq_id'][0] - 1}' in label sequence scheme)"
                        self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                      f"The residue number {hint} is not present in polymer sequence "
                                      f"of chain {chain_id_3} of the coordinates. "
                                      "Please update the sequence in the Macromolecules page.")
                        return

                    if ps['auth_seq_id'][-1] == seq_id_3 and atom_ids[-1] == 'N':
                        hint = f"'{seq_id_3 + 1}'"
                        if ps['seq_id'][-1] != seq_id_3:
                            hint += f" (or '{ps['seq_id'][-1] + 1}' in label sequence scheme)"
                        self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                      f"The residue number {hint} is not present in polymer sequence "
                                      f"of chain {chain_id_3} of the coordinates. "
                                      "Please update the sequence in the Macromolecules page.")
                        return

                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "The atom selection order must be [C(i-1), N(i), CA(i), C(i), N(i+1)].")
                return

            comp_id = self.atomSelectionSet[2][0]['comp_id']

            if comp_id == 'GLY':
                del dstFunc['cb_shift']

            else:

                if CS_ERROR_MIN < cb_shift < CS_ERROR_MAX:
                    pass
                else:
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"CB chemical shift value '{ca_shift}' must be within range {CS_RESTRAINT_ERROR}.")
                    return

            if self.createSfDict:
                sf = self.getSf(self.classification)
                sf['id'] += 1

            for atom1, atom2, atom3, atom4, atom5 in (itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3],
                                                                        self.atomSelectionSet[4])
                                                      if not self.in_loop else
                                                      zip(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1],
                                                          self.atomSelectionSet[2],
                                                          self.atomSelectionSet[3],
                                                          self.atomSelectionSet[4])):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if isLongRangeRestraint([atom2, atom3, atom4, atom5], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CARB) id={self.hvycsRestraints} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom1, atom2, atom3, atom4, atom5)
                    sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#carbon_shift_rcoil.
    def enterCarbon_shift_rcoil(self, ctx: CnsMRParser.Carbon_shift_rcoilContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#carbon_shift_rcoil.
    def exitCarbon_shift_rcoil(self, ctx: CnsMRParser.Carbon_shift_rcoilContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            rcoil_a = self.numberSelection[0]
            rcoil_b = self.numberSelection[1]

            if CS_ERROR_MIN < rcoil_a < CS_ERROR_MAX:
                pass
            else:
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"Random coil 'a' chemical shift value '{rcoil_a}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if CS_ERROR_MIN < rcoil_b < CS_ERROR_MAX:
                pass
            else:
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"Random coil 'b' chemical shift value '{rcoil_b}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            dstFunc = {'rcoil_a': rcoil_a, 'rcoil_b': rcoil_b}

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] != 'C':
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"Not a carbon; {atom1}.")
                    return

            for atom1 in self.atomSelectionSet[0]:
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CARB/RCOI) id={self.hvycsRestraints} "
                          f"atom={atom1} {dstFunc}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#proton_shift_statement.
    def enterProton_shift_statement(self, ctx: CnsMRParser.Proton_shift_statementContext):
        if ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.potential = 'square'
            elif code.startswith('HARM'):
                self.potential = 'harmonic'
            elif code.startswith('MULT'):
                self.potential = 'multiple'
            else:
                self.potential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'PROTONshift' statements. "
                              f"Instead, set the default potential {self.potential!r}.")

        elif ctx.Reset():
            self.potential = 'square'
            self.coefficients = None

    # Exit a parse tree produced by CnsMRParser#proton_shift_statement.
    def exitProton_shift_statement(self, ctx: CnsMRParser.Proton_shift_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (PROTON) classification={self.classification!r}")

    # Enter a parse tree produced by CnsMRParser#observed.
    def enterObserved(self, ctx: CnsMRParser.ObservedContext):  # pylint: disable=unused-argument
        self.procsRestraints += 1
        self.cur_subtype = 'procs'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#observed.
    def exitObserved(self, ctx: CnsMRParser.ObservedContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.procsRestraints -= 1
                return

            obs_value = self.numberSelection[0]

            obs_value_2 = None
            if len(self.numberSelection) > 1:
                obs_value_2 = self.numberSelection[1]

            if CS_ERROR_MIN < obs_value < CS_ERROR_MAX:
                pass
            else:
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The observed chemical shift value '{obs_value}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            if obs_value_2 is not None:
                if CS_ERROR_MIN < obs_value_2 < CS_ERROR_MAX:
                    pass
                else:
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The 2nd observed chemical shift value '{obs_value_2}' must be within range {CS_RESTRAINT_ERROR}.")
                    return

            if obs_value_2 is None:
                dstFunc = {'obs_value': obs_value}
            else:
                dstFunc = {'obs_value': obs_value, 'obs_value_2': obs_value_2}

            lenAtomSelectionSet = len(self.atomSelectionSet)

            if obs_value_2 is None and lenAtomSelectionSet == 2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Missing observed chemical shift value for the 2nd atom selection.")
                return

            if obs_value_2 is not None and lenAtomSelectionSet == 1:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Missing 2nd atom selection for the observed chemical shift value '{obs_value_2}'.")
                return

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] not in protonBeginCode:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"Not a proton; {atom1}.")
                    return

            if self.createSfDict:
                sf = self.getSf(self.classification)
                sf['id'] += 1

            for atom in self.atomSelectionSet[0]:
                if self.debug:
                    print(f"subtype={self.cur_subtype} (PROTON/OBSE) id={self.procsRestraints} "
                          f"atom={atom} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                 '.', None, None,
                                 sf['list_id'], self.entryId, dstFunc,
                                 self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                 atom)
                    sf['loop'].add_data(row)

            if lenAtomSelectionSet > 1:
                for atom in self.atomSelectionSet[1]:
                    if self.debug:
                        print(f"subtype={self.cur_subtype} (PROTON/OBSE) id={self.procsRestraints} "
                              f"atom={atom} {dstFunc}")
                    if self.createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.cur_subtype, sf['id'], sf['index_id'],
                                     2, None, '.',
                                     sf['list_id'], self.entryId, dstFunc,
                                     self.authToStarSeq, self.authToOrigSeq, self.authToInsCode, self.offsetHolder,
                                     None, atom)
                        sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#proton_shift_rcoil.
    def enterProton_shift_rcoil(self, ctx: CnsMRParser.Proton_shift_rcoilContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_rcoil.
    def exitProton_shift_rcoil(self, ctx: CnsMRParser.Proton_shift_rcoilContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                return

            rcoil = self.numberSelection[0]

            if CS_ERROR_MIN < rcoil < CS_ERROR_MAX:
                pass
            else:
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"Random coil chemical shift value '{rcoil}' must be within range {CS_RESTRAINT_ERROR}.")
                return

            dstFunc = {'rcoil': rcoil}

            for atom1 in self.atomSelectionSet[0]:
                if atom1['atom_id'][0] not in protonBeginCode:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  f"Not a proton; {atom1}.")
                    return

            for atom1 in self.atomSelectionSet[0]:
                if self.debug:
                    print(f"subtype={self.cur_subtype} (PROTON/RCOI) id={self.procsRestraints} "
                          f"atom={atom1} {dstFunc}")

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#proton_shift_anisotropy.
    def enterProton_shift_anisotropy(self, ctx: CnsMRParser.Proton_shift_anisotropyContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_anisotropy.
    def exitProton_shift_anisotropy(self, ctx: CnsMRParser.Proton_shift_anisotropyContext):
        co_or_cn = str(ctx.Simple_name(0))
        is_cooh = None
        if ctx.Logical():
            is_cooh = str(ctx.Logical()) in ('TRUE', 'ON')
        sc_or_bb = str(ctx.Simple_name(1))

        if not self.areUniqueCoordAtoms('a proton chemical shift (PROTON/ANIS)'):
            if len(self.g) > 0:
                self.f.extend(self.g)
            return

        dstFunc = {'co_or_cn': co_or_cn.lower(), 'is_cooh': is_cooh, 'sc_or_bb': sc_or_bb.lower()}

        chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
        seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
        atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

        chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
        seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
        atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

        chain_id_3 = self.atomSelectionSet[2][0]['chain_id']
        seq_id_3 = self.atomSelectionSet[2][0]['seq_id']
        atom_id_3 = self.atomSelectionSet[2][0]['atom_id']

        chain_ids = [chain_id_1, chain_id_2, chain_id_3]
        seq_ids = [seq_id_1, seq_id_2, seq_id_3]
        offsets = [seq_id - seq_id_2 for seq_id in seq_ids]
        atom_ids = [atom_id_1, atom_id_2, atom_id_3]

        if chain_ids != [chain_id_1] * 3 or offsets != [0] * 3 or atom_ids != ['CA', 'C', 'O']:
            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                          "The atom selection order must be [CA(i), C(i), O(i)].")
            return

        for atom1, atom2, atom3 in itertools.product(self.atomSelectionSet[0],
                                                     self.atomSelectionSet[1],
                                                     self.atomSelectionSet[2]):
            if isLongRangeRestraint([atom1, atom2, atom3], self.polySeq if self.gapInAuthSeq else None):
                continue
            if self.debug:
                print(f"subtype={self.cur_subtype} (PROTON/ANIS) id={self.procsRestraints} "
                      f"atom1={atom1} atom2={atom2} atom3={atom3} {dstFunc}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_amides.
    def enterProton_shift_amides(self, ctx: CnsMRParser.Proton_shift_amidesContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_amides.
    def exitProton_shift_amides(self, ctx: CnsMRParser.Proton_shift_amidesContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'H':
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Not a backbone amide proton; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.cur_subtype} (PROTON/AMID) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_carbons.
    def enterProton_shift_carbons(self, ctx: CnsMRParser.Proton_shift_carbonsContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_carbons.
    def exitProton_shift_carbons(self, ctx: CnsMRParser.Proton_shift_carbonsContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'C':
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Not a backbone carbonyl carbon; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.cur_subtype} (PROTON/CARB) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_nitrogens.
    def enterProton_shift_nitrogens(self, ctx: CnsMRParser.Proton_shift_nitrogensContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_nitrogens.
    def exitProton_shift_nitrogens(self, ctx: CnsMRParser.Proton_shift_nitrogensContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'N':
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Not a backbone nitrogen; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.cur_subtype} (PROTON/NITR) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_oxygens.
    def enterProton_shift_oxygens(self, ctx: CnsMRParser.Proton_shift_oxygensContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_oxygens.
    def exitProton_shift_oxygens(self, ctx: CnsMRParser.Proton_shift_oxygensContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] != 'O':
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Not a backbone oxygen; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.cur_subtype} (PROTON/OXYG) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_ring_atoms.
    def enterProton_shift_ring_atoms(self, ctx: CnsMRParser.Proton_shift_ring_atomsContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_ring_atoms.
    def exitProton_shift_ring_atoms(self, ctx: CnsMRParser.Proton_shift_ring_atomsContext):
        ring_name = str(ctx.Simple_name())

        ringNames = ('PHE', 'TYR', 'HIS', 'TRP5', 'TRP6', 'ADE6', 'ADE5', 'GUA6', 'GUA5', 'THY', 'CYT', 'URA')

        if ring_name not in ringNames:
            self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                          f"{ring_name!r} must be one of {ringNames}.")
            return

        if not self.areUniqueCoordAtoms('a proton chemical shift (PROTON/RING)'):
            if len(self.g) > 0:
                self.f.extend(self.g)
            return

        if len(self.atomSelectionSet) == 5:
            for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                       self.atomSelectionSet[1],
                                                                       self.atomSelectionSet[2],
                                                                       self.atomSelectionSet[3],
                                                                       self.atomSelectionSet[4]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (PROTON/RING) id={self.procsRestraints} "
                          f"ring_name={ring_name} atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5}")

        else:
            for atom1, atom2, atom3, atom4, atom5, atom6 in itertools.product(self.atomSelectionSet[0],
                                                                              self.atomSelectionSet[1],
                                                                              self.atomSelectionSet[2],
                                                                              self.atomSelectionSet[3],
                                                                              self.atomSelectionSet[4],
                                                                              self.atomSelectionSet[5]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5, atom6], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (PROTON/RING) id={self.procsRestraints} "
                          f"ring_name={ring_name} atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} atom6={atom6}")

    # Enter a parse tree produced by CnsMRParser#proton_shift_alphas_and_amides.
    def enterProton_shift_alphas_and_amides(self, ctx: CnsMRParser.Proton_shift_alphas_and_amidesContext):  # pylint: disable=unused-argument
        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#proton_shift_alphas_and_amides.
    def exitProton_shift_alphas_and_amides(self, ctx: CnsMRParser.Proton_shift_alphas_and_amidesContext):  # pylint: disable=unused-argument
        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'] == 'H' or atom1['atom_id'].startswith('HA'):
                pass
            else:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Neither alpha protons nor amide proton; {atom1}.")
                return

        for atom1 in self.atomSelectionSet[0]:
            print(f"subtype={self.cur_subtype} (PROTON/ALPH) id={self.procsRestraints} "
                  f"atom={atom1}")

    # Enter a parse tree produced by CnsMRParser#conformation_statement.
    def enterConformation_statement(self, ctx: CnsMRParser.Conformation_statementContext):
        if ctx.Error():
            self.ramaError = self.getNumber_s(ctx.number_s())
            if isinstance(self.ramaError, str):
                if self.ramaError in self.evaluate:
                    self.ramaError = self.evaluate[self.ramaError]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The error value 'CONF {str(ctx.Error())} {self.ramaError} END'")

        elif ctx.ForceConstant():
            self.ramaForceConst = self.getNumber_s(ctx.number_s())

        elif ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.ramaPotential = 'square'
            elif code.startswith('HARM'):
                self.ramaPotential = 'harmonic'
            else:
                self.ramaPotential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'CONFormation' statements. "
                              f"Instead, set the default potential {self.ramaPotential!r}.")

        elif ctx.Size():
            self.ramaSize = []
            dim = str(ctx.Dimensions()).lower()
            self.ramaSize.append(int(str(ctx.Integer(0))))
            if dim in ('twod', 'threed', 'fourd'):
                self.ramaSize.append(int(str(ctx.Integer(1))))
            if dim in ('threed', 'fourd'):
                self.ramaSize.append(int(str(ctx.Integer(2))))
            if dim == 'fourd':
                self.ramaSize.append(int(str(ctx.Integer(3))))

        elif ctx.Phase():
            self.ramaPhase = []
            for d in range(4):
                offset = d * 3
                if ctx.Integer(offset):
                    phase = []
                    for i in range(3):
                        if ctx.Integer(offset + i):
                            phase.append(int(str(ctx.Integer(offset + i))))
                        else:
                            break
                    self.ramaPhase.append(phase)
                else:
                    break

        elif ctx.Expectation():
            self.ramaExpectValue = self.getNumber_s(ctx.number_s())

            self.ramaExpectGrid = []
            for d in range(4):
                if ctx.Integer(d):
                    self.ramaExpectGrid.append(int(str(ctx.Integer(d))))
                else:
                    break

        elif ctx.Reset():
            self.ramaError = None
            self.ramaForceConst = 1.0
            self.ramaPotential = 'square'
            self.ramaSize = None
            self.ramaPhase = None
            self.ramaExpectGrid = None
            self.ramaExpectValue = None

        elif ctx.Zero():
            self.ramaExpectGrid = None
            self.ramaExpectValue = None

    # Exit a parse tree produced by CnsMRParser#conformation_statement.
    def exitConformation_statement(self, ctx: CnsMRParser.Conformation_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (CONF) classification={self.classification!r} "
                  f"error={self.ramaError} force_constant={self.ramaForceConst} potential={self.ramaPotential} "
                  f"size={self.ramaSize} phase={self.ramaSize} expectation={self.ramaExpectGrid} {self.ramaExpectValue}")

    # Enter a parse tree produced by CnsMRParser#conf_assign.
    def enterConf_assign(self, ctx: CnsMRParser.Conf_assignContext):  # pylint: disable=unused-argument
        self.ramaRestraints += 1
        self.cur_subtype = 'rama'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#conf_assign.
    def exitConf_assign(self, ctx: CnsMRParser.Conf_assignContext):  # pylint: disable=unused-argument
        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        if not self.areUniqueCoordAtoms('a conformation database (CONF)'):
            if len(self.g) > 0:
                self.f.extend(self.g)
            return

        for i in range(0, len(self.atomSelectionSet), 2):
            chain_id_1 = self.atomSelectionSet[i][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[i][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[i][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[i][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[i + 1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[i + 1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[i + 1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[i + 1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in dihedral angle vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found inter-chain dihedral angle vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                              "Found inter-residue dihedral angle vector; "
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
                    warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                  "Found inter-residue dihedral angle vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero dihedral angle vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found an dihedral angle vector over multiple covalent bonds in the 'CONFormation' statement; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

        if self.createSfDict:
            sf = self.getSf('dihedral angle database restraint')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id', 'combination_id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                      'auth_asym_id_4', 'auth_seq_id_4', 'auth_comp_id_4', 'auth_atom_id_4',
                                      'list_id']
                sf['tags'].append(['classification', self.classification])
                sf['tags'].append(['error', self.ramaError])
                sf['tags'].append(['force_constant', self.ramaForceConst])
                sf['tags'].append(['potential', self.ramaPotential])
                sf['tags'].append(['size', self.ramaSize])
                sf['tags'].append(['phase', self.ramaPhase])
                sf['tags'].append(['expect_grid', self.ramaExpectGrid])
                sf['tags'].append(['expect_value', self.ramaExpectValue])

        for i in range(0, len(self.atomSelectionSet), 4):
            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[i],
                                                                self.atomSelectionSet[i + 1],
                                                                self.atomSelectionSet[i + 2],
                                                                self.atomSelectionSet[i + 3]):
                if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (CONF) id={self.ramaRestraints} "
                          f"atom{i+1}={atom1} atom{i+2}={atom2} atom{i+3}={atom3} atom{i+4}={atom4}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'], '.' if len(self.atomSelectionSet) == 4 else (i + 1),
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                               atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id'],
                                               sf['list_id']])

    # Enter a parse tree produced by CnsMRParser#diffusion_statement.
    def enterDiffusion_statement(self, ctx: CnsMRParser.Diffusion_statementContext):
        if ctx.Coefficients():
            self.diffCoef = {'Tc': self.getNumber_s(ctx.number_s(0)),
                             'anisotropy': self.getNumber_s(ctx.number_s(1)),
                             'rhombicity': self.getNumber_s(ctx.number_s(2)),
                             'frequency_1h': self.getNumber_s(ctx.number_s(3)),
                             'frequency_15n': self.getNumber_s(ctx.number_s(4))
                             }

        elif ctx.ForceConstant():
            self.diffForceConst = self.getNumber_s(ctx.number_s(0))

        elif ctx.Potential_types():
            code = str(ctx.Potential_types()).upper()
            if code.startswith('SQUA'):
                self.diffPotential = 'square'
            elif code.startswith('HARM'):
                self.diffPotential = 'harmonic'
            else:
                self.diffPotential = 'square'
                self.f.append("[Enum mismatch ignorable] "
                              f"The potential type {str(ctx.Potential_types())!r} is unknown potential type for the 'DANIsotropy' statements. "
                              f"Instead, set the default potential {self.diffPotential!r}.")

        elif ctx.Reset():
            self.diffCoef = None
            self.diffForceConst = 1.0
            self.diffPotential = 'square'

    # Exit a parse tree produced by CnsMRParser#diffusion_statement.
    def exitDiffusion_statement(self, ctx: CnsMRParser.Diffusion_statementContext):  # pylint: disable=unused-argument
        if self.debug:
            print(f"subtype={self.cur_subtype} (DANI) classification={self.classification!r} "
                  f"coefficients={self.diffCoef} force_constant={self.diffForceConst} "
                  f"potential={self.diffPotential}")

    # Enter a parse tree produced by CnsMRParser#dani_assign.
    def enterDani_assign(self, ctx: CnsMRParser.Dani_assignContext):  # pylint: disable=unused-argument
        self.diffRestraints += 1
        self.cur_subtype = 'diff'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#dani_assign.
    def exitDani_assign(self, ctx: CnsMRParser.Dani_assignContext):  # pylint: disable=unused-argument

        try:

            if len(self.numberSelection) == 0 or None in self.numberSelection:
                self.diffRestraints -= 1
                return

            target = self.numberSelection[0]

            if len(self.numberSelection) > 1:
                delta = abs(self.numberSelection[1])
            else:
                delta = 0.0

            target_value = target
            lower_limit = None
            upper_limit = None

            if self.potential == 'square' and delta > 0.0:
                lower_limit = target - delta
                upper_limit = target + delta

            dstFunc = self.validateT1T2Range(1.0,
                                             target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.hasPolySeq and not self.hasNonPolySeq:
                return

            if not self.areUniqueCoordAtoms('a diffusion anisotropy (DANI)', XPLOR_ORIGIN_AXIS_COLS):
                if len(self.g) > 0:
                    self.f.extend(self.g)
                return

            chain_id_1 = self.atomSelectionSet[4][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[4][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[4][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[4][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[5][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[5][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[5][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[5][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Non-magnetic susceptible spin appears in diffusion anisotropy vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "
                              f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Found inter-chain diffusion anisotropy vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                              "Found inter-residue diffusion anisotropy vector; "
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
                    warn_title = 'Anomalous data' if self.preferAuthSeq and 'PRO' in (comp_id_1, comp_id_2) else 'Invalid data'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                  "Found inter-residue diffusion anisotropy vector; "
                                  f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                    return

            elif atom_id_1 == atom_id_2:
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              "Found zero diffusion anisotropy vector; "
                              f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                return

            elif self.ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not self.ccU.hasBond(comp_id_1, atom_id_1, atom_id_2):

                    if self.nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                      "Found a diffusion anisotropy vector over multiple covalent bonds in the 'DANIsotropy' statement; "
                                      f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).")
                        return

            if self.createSfDict:
                sf = self.getSf('diffusion anisotropy restraint')
                sf['id'] += 1
                if len(sf['loop']['tags']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          't1/t2_ratio', 't1/t2_ratio_err',
                                          'list_id']
                    sf['tags'].append(['classification', self.classification])
                    sf['tags'].append(['coefficients', self.diffCoef])
                    sf['tags'].append(['force_constant', self.diffForceConst])
                    sf['tags'].append(['potential', self.diffPotential])

            for atom1, atom2 in itertools.product(self.atomSelectionSet[4],
                                                  self.atomSelectionSet[5]):
                atoms = [atom1, atom2]
                if isDefinedSegmentRestraint(atoms):
                    continue
                if isIdenticalRestraint(atoms, self.nefT):
                    continue
                if isLongRangeRestraint(atoms, self.polySeq if self.gapInAuthSeq else None):
                    continue
                if self.debug:
                    print(f"subtype={self.cur_subtype} (DANI) id={self.diffRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               target, delta,
                                               sf['list_id']])

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CnsMRParser#one_bond_coupling_statement.
    def enterOne_bond_coupling_statement(self, ctx: CnsMRParser.One_bond_coupling_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#one_bond_coupling_statement.
    def exitOne_bond_coupling_statement(self, ctx: CnsMRParser.One_bond_coupling_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#one_bond_assign.
    def enterOne_bond_assign(self, ctx: CnsMRParser.One_bond_assignContext):  # pylint: disable=unused-argument
        """
        @deprecated: This restraint has not been useful in practice, but has been preserved for historical reasons.
        """

    # Exit a parse tree produced by CnsMRParser#one_bond_assign.
    def exitOne_bond_assign(self, ctx: CnsMRParser.One_bond_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#angle_db_statement.
    def enterAngle_db_statement(self, ctx: CnsMRParser.Angle_db_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#angle_db_statement.
    def exitAngle_db_statement(self, ctx: CnsMRParser.Angle_db_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#angle_db_assign.
    def enterAngle_db_assign(self, ctx: CnsMRParser.Angle_db_assignContext):  # pylint: disable=unused-argument
        """
        @deprecated:  This term has not proved useful in practice and is only here for historical reasons.
        """

    # Exit a parse tree produced by CnsMRParser#angle_db_assign.
    def exitAngle_db_assign(self, ctx: CnsMRParser.Angle_db_assignContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#ncs_restraint.
    def enterNcs_restraint(self, ctx: CnsMRParser.Ncs_restraintContext):  # pylint: disable=unused-argument
        self.geoStatements += 1
        self.cur_subtype = 'geo'

        if self.createSfDict:
            self.addSf('NCS restraint')

    # Exit a parse tree produced by CnsMRParser#ncs_restraint.
    def exitNcs_restraint(self, ctx: CnsMRParser.Ncs_restraintContext):  # pylint: disable=unused-argument
        if self.createSfDict:
            self.trimSfWoLp()

    # Enter a parse tree produced by CnsMRParser#ncs_statement.
    def enterNcs_statement(self, ctx: CnsMRParser.Ncs_statementContext):
        if ctx.Initialize():
            self.ncsSigb = 2.0
            self.ncsWeight = 300.0

    # Exit a parse tree produced by CnsMRParser#ncs_statement.
    def exitNcs_statement(self, ctx: CnsMRParser.Ncs_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#ncs_group_statement.
    def enterNcs_group_statement(self, ctx: CnsMRParser.Ncs_group_statementContext):
        self.geoRestraints += 1
        if self.cur_subtype != 'geo':
            self.geoStatements += 1
        self.cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.g.clear()

        if ctx.Sigb():
            self.ncsSigb = self.getNumber_s(ctx.number_s())
            if isinstance(self.ncsSigb, str):
                if self.ncsSigb in self.evaluate:
                    self.ncsSigb = self.evaluate[self.ncsSigb]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The B-factor value 'GROUP {str(ctx.Sigb())}={self.ncsSigb} END' "
                                  f"where the symbol {self.ncsSigb!r} is not defined so that set the default value.")
                    self.ncsSigb = 2.0
            if self.ncsSigb <= 0.0:
                self.f.append("[Invalid data] "
                              f"The B-factor value 'GROUP {str(ctx.Sigb())}={self.ncsSigb} END' must be a positive value.")

        elif ctx.Weight():
            self.ncsWeight = self.getNumber_s(ctx.number_s())
            if isinstance(self.ncsWeight, str):
                if self.ncsWeight in self.evaluate:
                    self.ncsWeight = self.evaluate[self.ncsWeight]
                else:
                    self.f.append("[Unsupported data] "
                                  f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' "
                                  f"where the symbol {self.ncsWeight!r} is not defined so that set the default value.")
                    self.ncsWeight = 300.0
            if self.ncsWeight < 0.0:
                self.f.append("[Invalid data] "
                              f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' must not be a negative value.")
            elif self.ncsWeight == 0.0:
                self.f.append("[Range value warning] "
                              f"The weight value 'GROUP {str(ctx.Weight())}={self.ncsWeight} END' should be a positive value.")

    # Exit a parse tree produced by CnsMRParser#ncs_group_statement.
    def exitNcs_group_statement(self, ctx: CnsMRParser.Ncs_group_statementContext):  # pylint: disable=unused-argument
        if not self.hasPolySeq and not self.hasNonPolySeq:
            return

        if len(self.atomSelectionSet) == 0:
            return

        if self.createSfDict:
            sf = self.getSf('NCS restraint')
            sf['id'] += 1
            if len(sf['loop']['tags']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'list_id']
                sf['tags'].append(['sigma_b', self.ncsSigb])
                sf['tags'].append(['weight', self.ncsWeight])

        for atom1 in self.atomSelectionSet[0]:
            if atom1['atom_id'][0] in protonBeginCode:
                continue
            if self.debug:
                print(f"subtype={self.cur_subtype} (NCS/GROUP) id={self.geoRestraints} "
                      f"atom={atom1} sigb={self.ncsSigb} weight={self.ncsWeight}")
            if self.createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           sf['list_id']])

    # Enter a parse tree produced by CnsMRParser#selection.
    def enterSelection(self, ctx: CnsMRParser.SelectionContext):  # pylint: disable=unused-argument
        if self.verbose_debug:
            print("  " * self.depth + "enter_selection")

        if self.inVector3D:
            self.inVector3D_columnSel += 1

        elif self.depth == 0:
            self.stackSelections = []
            self.stackTerms = []
            self.factor = {}

    # Exit a parse tree produced by CnsMRParser#selection.
    def exitSelection(self, ctx: CnsMRParser.SelectionContext):  # pylint: disable=unused-argument
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

        if self.inVector3D:
            if self.inVector3D_columnSel == 0:
                self.inVector3D_tail = atomSelection[0]
                if len(atomSelection) > 1:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Ambiguous atoms have been selected to create a 3d-vector in the 'tail' clause.")
            else:
                self.inVector3D_head = atomSelection[0]
                if len(atomSelection) > 1:
                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                  "Ambiguous atoms have been selected to create a 3d-vector in the 'head' clause.")

        else:
            self.atomSelectionSet.append(atomSelection)

    # Enter a parse tree produced by CnsMRParser#selection_expression.
    def enterSelection_expression(self, ctx: CnsMRParser.Selection_expressionContext):
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

    # Exit a parse tree produced by CnsMRParser#selection_expression.
    def exitSelection_expression(self, ctx: CnsMRParser.Selection_expressionContext):  # pylint: disable=unused-argument
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

    # Enter a parse tree produced by CnsMRParser#term.
    def enterTerm(self, ctx: CnsMRParser.TermContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_term, intersection: {bool(ctx.And_op(0))}")

        self.stackFactors = []
        self.factor = {}

        self.depth += 1

    # Exit a parse tree produced by CnsMRParser#term.
    def exitTerm(self, ctx: CnsMRParser.TermContext):  # pylint: disable=unused-argument
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

    # Enter a parse tree produced by CnsMRParser#factor.
    def enterFactor(self, ctx: CnsMRParser.FactorContext):
        if self.verbose_debug:
            print("  " * self.depth + f"enter_factor, concatenation: {bool(ctx.factor())}")

        if ctx.Not_op():
            if len(self.factor) > 0:
                self.factor = self.doConsumeFactor_expressions(self.factor, cifCheck=True)
                if 'atom_selection' in self.factor:
                    self.stackFactors.append(self.factor)
                self.factor = {}

        elif ctx.Point():
            self.inVector3D = True
            self.inVector3D_columnSel = -1
            self.inVector3D_tail = None
            self.inVector3D_head = None
            self.vector3D = None

        self.depth += 1

    # Exit a parse tree produced by CnsMRParser#factor.
    def exitFactor(self, ctx: CnsMRParser.FactorContext):
        self.depth -= 1
        if self.verbose_debug:
            print("  " * self.depth + "exit_factor")

        def set_store(num):
            if self.verbose_debug:
                print("  " * self.depth + f"--> store{num}")
            if len(self.storeSet[num]) == 0:
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The 'store{num}' clause has no effect "
                              "because the internal vector statement is not set yet.")
            else:
                self.factor = deepcopy(self.storeSet[num])

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

            if ctx.All() or ctx.Known():
                clauseName = 'all' if ctx.All() else 'known'
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

            elif ctx.Around() or ctx.Saround():
                clauseName = 'around' if ctx.Around() else 'saround'
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

                    if ctx.Saround():
                        identity = numpy.identity(3, dtype=float)
                        zero = numpy.zeros(3, dtype=float)

                        oper_list = self.cR.getDictList('pdbx_struct_oper_list')
                        if len(oper_list) > 0:
                            for oper in oper_list:
                                matrix = numpy.array([[float(oper['matrix[1][1]']), float(oper['matrix[1][2]']), float(oper['matrix[1][3]'])],
                                                     [float(oper['matrix[2][1]']), float(oper['matrix[2][2]']), float(oper['matrix[2][3]'])],
                                                     [float(oper['matrix[3][1]']), float(oper['matrix[3][2]']), float(oper['matrix[3][3]'])]], dtype=float)
                                vector = numpy.array([float(oper['vector[1]']), float(oper['vector[2]']), float(oper['vector[3]'])], dtype=float)

                                if numpy.array_equal(matrix, identity) and numpy.array_equal(vector, zero):
                                    continue

                                inv_matrix = numpy.linalg.inv(matrix)

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

                                        origin = numpy.dot(inv_matrix, numpy.subtract(to_np_array(_origin[0]), vector))

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
                    if len(self.fibril_chain_ids) > 0 and not self.hasNonPoly:
                        if chainId[0] in self.fibril_chain_ids:
                            self.factor['chain_id'] = [chainId[0]]
                    elif self.monoPolymer and not self.hasBranched and not self.hasNonPoly:
                        self.factor['chain_id'] = self.polySeq[0]['chain_id']
                        self.factor['auth_chain_id'] = chainId
                    elif self.reasons is not None:
                        if 'atom_id' not in self.factor or not any(a in XPLOR_RDC_PRINCIPAL_AXIS_NAMES for a in self.factor['atom_id']):
                            self.factor['atom_id'] = [None]
                            if not self.with_axis\
                               and 'segment_id_mismatch' in self.reasons\
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
                if ctx.Logical():  # 7rno: ON
                    atomId = str(ctx.Logical())
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

            elif ctx.Attribute():
                if self.verbose_debug:
                    print("  " * self.depth + "--> attribute")
                if not self.hasCoord:
                    return
                absolute = bool(ctx.Abs())
                _attr_prop = str(ctx.Attr_properties())
                attr_prop = _attr_prop.lower()
                opCode = str(ctx.Comparison_ops())
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                attr_value = self.numberFSelection[0]

                validProp = True

                if attr_prop == 'b':
                    valueType = {'name': 'B_iso_or_equiv'}
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop.startswith('bcom')\
                        or attr_prop.startswith('qcom')\
                        or attr_prop.startswith('xcom')\
                        or attr_prop.startswith('ycom')\
                        or attr_prop.startswith('zcom'):  # BCOMP, QCOMP, XCOMP, YCOMP, ZCOM`
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "requires a comparison coordinate set.")
                    validProp = False

                elif attr_prop.startswith('char'):  # CAHRGE
                    valueType = {'name': 'pdbx_formal_charge'}
                    if opCode == '=':
                        valueType['type'] = 'int' if not absolute else 'abs-int'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-int' if not absolute else 'range-abs-int'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
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

                elif attr_prop in ('dx', 'dy', 'dz', 'harm'):
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

                            if (opCode == '=' and atomicWeight == attr_value)\
                               or (opCode == '<' and atomicWeight < attr_value)\
                               or (opCode == '>' and atomicWeight > attr_value)\
                               or (opCode == '<=' and atomicWeight <= attr_value)\
                               or (opCode == '>=' and atomicWeight >= attr_value)\
                               or (opCode == '#' and atomicWeight != attr_value):
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

                elif attr_prop == 'q':
                    valueType = {'name': 'occupancy'}
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop.startswith('scatter'):  # scatter_[ab][1-4], scatter_c, scatter_fp, scatter_fdp
                    self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                  f"The attribute property {_attr_prop!r} "
                                  "related to X-ray scattering power of each atom is not possessed in the static coordinate file.")
                    validProp = False

                elif attr_prop in ('refx', 'refy', 'refz', 'rmsd'):
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
                    if opCode == '=':
                        valueType['type'] = 'float' if not absolute else 'abs-float'
                        valueType['value'] = attr_value
                    elif opCode == '<':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_exclusive': attr_value}
                    elif opCode == '>':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_exclusive': attr_value}
                    elif opCode == '<=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'max_inclusive': attr_value}
                    elif opCode == '>=':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
                        valueType['range'] = {'min_inclusive': attr_value}
                    elif opCode == '#':
                        valueType['type'] = 'range-float' if not absolute else 'range-abs-float'
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

                elif attr_prop.startswith('store'):
                    store_id = int(attr_prop[-1])
                    self.factor['atom_id'] = [None]
                    if len(self.storeSet[store_id]) == 0:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The 'store{store_id}' clause has no effect "
                                      "because the internal vector statement is not set.")
                        validProp = False

                if validProp and 'atom_selection' in self.factor and len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    _absolute = ' abs' if absolute else ''
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  f"The 'attribute' clause ('{_attr_prop}{_absolute} {opCode} {attr_value}') has no effect.")

            elif ctx.BondedTo():
                if self.verbose_debug:
                    print("  " * self.depth + "--> bondedto")
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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
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

            elif ctx.Fbox() or ctx.Sfbox():
                clauseName = 'fbox' if ctx.Fbox() else 'sfbox'
                if self.verbose_debug:
                    print("  " * self.depth + f"--> {clauseName}")
                if not self.hasCoord:
                    return
                if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                    return
                xmin = self.numberFSelection[0]
                xmax = self.numberFSelection[1]
                ymin = self.numberFSelection[2]
                ymax = self.numberFSelection[3]
                zmin = self.numberFSelection[4]
                zmax = self.numberFSelection[5]

                try:

                    _atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [{'name': 'Cartn_x', 'type': 'range-float',
                                                        'range': {'min_exclusive': xmin,
                                                                  'max_exclusive': xmax}},
                                                       {'name': 'Cartn_y', 'type': 'range-float',
                                                        'range': {'min_exclusive': ymin,
                                                                  'max_exclusive': ymax}},
                                                       {'name': 'Cartn_z', 'type': 'range-float',
                                                        'range': {'min_exclusive': zmin,
                                                                  'max_exclusive': zmax}},
                                                       {'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                except Exception as e:
                    if self.verbose:
                        self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                if ctx.Sfbox():
                    identity = numpy.identity(3, dtype=float)
                    zero = numpy.zeros(3, dtype=float)

                    oper_list = self.cR.getDictList('pdbx_struct_oper_list')
                    if len(oper_list) > 0:
                        for oper in oper_list:
                            matrix = numpy.array([[float(oper['matrix[1][1]']), float(oper['matrix[1][2]']), float(oper['matrix[1][3]'])],
                                                 [float(oper['matrix[2][1]']), float(oper['matrix[2][2]']), float(oper['matrix[2][3]'])],
                                                 [float(oper['matrix[3][1]']), float(oper['matrix[3][2]']), float(oper['matrix[3][3]'])]], dtype=float)
                            vector = numpy.array([float(oper['vector[1]']), float(oper['vector[2]']), float(oper['vector[3]'])], dtype=float)

                            if numpy.array_equal(matrix, identity) and numpy.array_equal(vector, zero):
                                continue

                            try:

                                __atomSelection =\
                                    self.cR.getDictListWithFilter('atom_site',
                                                                  AUTH_ATOM_CARTN_DATA_ITEMS,
                                                                  [{'name': self.modelNumName, 'type': 'int',
                                                                    'value': self.representativeModelId},
                                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                                    'enum': (self.representativeAltId,)}
                                                                   ])

                                for atom in __atomSelection:
                                    origin = to_np_array(atom)
                                    mv = numpy.dot(matrix, numpy.add(origin, vector))

                                    if xmin < mv[0] < xmax\
                                       and ymin < mv[1] < ymax\
                                       and zmin < mv[2] < zmax:
                                        del atom['x']
                                        del atom['y']
                                        del atom['z']
                                        _atomSelection.append(atom)

                            except Exception as e:
                                if self.verbose:
                                    self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                self.factor['atom_selection'] = [dict(s) for s in set(frozenset(atom.items())
                                                                      for atom in _atomSelection
                                                                      if isinstance(atom, dict))]

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  f"The {clauseName!r} clause has no effect.")

            elif ctx.Id():
                if self.verbose_debug:
                    print("  " * self.depth + "--> id")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'id' clause has no effect "
                              "because the internal atom number is not included in the coordinate file.")

            elif ctx.Name():
                if self.verbose_debug:
                    print("  " * self.depth + "--> name")

                eval_factor = False
                __factor = None
                if 'atom_id' in self.factor or 'atom_ids' in self.factor:
                    __factor = copy.copy(self.factor)
                    self.consumeFactor_expressions("'name' clause", False)
                    eval_factor = True

                if not eval_factor and 'atom_selection' in self.factor:
                    self.factor = {}

                if ctx.Colon():  # range expression
                    if ctx.Simple_name(0):
                        begAtomId = str(ctx.Simple_name(0))
                    elif ctx.Double_quote_string(0):
                        begAtomId = str(ctx.Double_quote_string(0)).strip('"').strip()
                        if len(begAtomId) == 0:
                            return
                    if ctx.Simple_name(1):
                        endAtomId = str(ctx.Simple_name(1))
                    elif ctx.Double_quote_string(1):
                        endAtomId = str(ctx.Double_quote_string(1)).strip('"').strip()
                        if len(endAtomId) == 0:
                            return
                    self.factor['atom_ids'] = [begAtomId, endAtomId]

                elif ctx.Simple_name(0) or ctx.Double_quote_string(0):
                    if ctx.Simple_name(0):
                        self.factor['atom_id'] = [str(ctx.Simple_name(0))]
                    elif ctx.Double_quote_string(0):
                        self.factor['atom_id'] = [str(ctx.Double_quote_string(0)).strip('"').strip()]

                elif ctx.Simple_names(0):
                    self.factor['atom_ids'] = [str(ctx.Simple_names(0))]

                elif ctx.Symbol_name():
                    symbol_name = str(ctx.Symbol_name())
                    if symbol_name in self.evaluate:
                        val = self.evaluate[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_id'] = val
                        else:
                            self.factor['atom_id'] = [val]
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['atom_id'] = val
                        else:
                            self.factor['atom_id'] = [val]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                elif ctx.Logical():  # 7rno: ON
                    self.factor['atom_id'] = [str(ctx.Logical())]

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor and __factor['atom_id'][0] is not None:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.cur_subtype == 'plane':
                            pass
                        elif self.cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The 'name' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                          f"and {self.getReadableFactor(_factor)}.")

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
                if ctx.Tail():

                    if self.inVector3D_tail is not None:

                        try:

                            _tail =\
                                self.cR.getDictListWithFilter('atom_site',
                                                              CARTN_DATA_ITEMS,
                                                              [{'name': self.authAsymId, 'type': 'str', 'value': self.inVector3D_tail['chain_id']},
                                                               {'name': self.authSeqId, 'type': 'int', 'value': self.inVector3D_tail['seq_id']},
                                                               {'name': self.authAtomId, 'type': 'str', 'value': self.inVector3D_tail['atom_id']},
                                                               {'name': self.modelNumName, 'type': 'int',
                                                                'value': self.representativeModelId},
                                                               {'name': 'label_alt_id', 'type': 'enum',
                                                                'enum': (self.representativeAltId,)}
                                                               ])

                            if len(_tail) == 1:
                                tail = to_np_array(_tail[0])

                                if self.inVector3D_head is None:
                                    self.vector3D = tail

                                else:

                                    _head =\
                                        self.cR.getDictListWithFilter('atom_site',
                                                                      CARTN_DATA_ITEMS,
                                                                      [{'name': self.authAsymId, 'type': 'str', 'value': self.inVector3D_head['chain_id']},
                                                                       {'name': self.authSeqId, 'type': 'int', 'value': self.inVector3D_head['seq_id']},
                                                                       {'name': self.authAtomId, 'type': 'str', 'value': self.inVector3D_head['atom_id']},
                                                                       {'name': self.modelNumName, 'type': 'int',
                                                                        'value': self.representativeModelId},
                                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                                        'enum': (self.representativeAltId,)}
                                                                       ])

                                    if len(_head) == 1:
                                        head = to_np_array(_head[0])
                                        self.vector3D = numpy.subtract(tail, head, dtype=float)

                        except Exception as e:
                            if self.verbose:
                                self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                    self.inVector3D_tail = self.inVector3D_head = None
                    if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                        return
                    cut = self.numberFSelection[0]

                else:
                    if len(self.numberFSelection) == 0 or None in self.numberFSelection:
                        return
                    self.vector3D = [self.numberFSelection[0], self.numberFSelection[1], self.numberFSelection[2]]
                    cut = self.numberFSelection[3]

                if self.vector3D is None:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'point' clause has no effect because no 3d-vector is specified.")

                else:
                    atomSelection = []

                    try:

                        _neighbor =\
                            self.cR.getDictListWithFilter('atom_site',
                                                          AUTH_ATOM_CARTN_DATA_ITEMS,
                                                          [{'name': 'Cartn_x', 'type': 'range-float',
                                                            'range': {'min_exclusive': (self.vector3D[0] - cut),
                                                                      'max_exclusive': (self.vector3D[0] + cut)}},
                                                           {'name': 'Cartn_y', 'type': 'range-float',
                                                            'range': {'min_exclusive': (self.vector3D[1] - cut),
                                                                      'max_exclusive': (self.vector3D[1] + cut)}},
                                                           {'name': 'Cartn_z', 'type': 'range-float',
                                                            'range': {'min_exclusive': (self.vector3D[2] - cut),
                                                                      'max_exclusive': (self.vector3D[2] + cut)}},
                                                           {'name': self.modelNumName, 'type': 'int',
                                                            'value': self.representativeModelId},
                                                           {'name': 'label_alt_id', 'type': 'enum',
                                                            'enum': (self.representativeAltId,)}
                                                           ])

                        if len(_neighbor) > 0:
                            neighbor = [atom for atom in _neighbor if distance(to_np_array(atom), self.vector3D) < cut]

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

                self.inVector3D = False
                self.vector3D = None

            elif ctx.Previous():
                if self.verbose_debug:
                    print("  " * self.depth + "--> previous")
                self.factor['atom_id'] = [None]
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'previous' clause has no effect "
                              "because the internal atom selection is fragile in the restraint file.")

            elif ctx.Pseudo():
                if self.verbose_debug:
                    print("  " * self.depth + "--> pseudo")
                if not self.hasCoord:
                    return
                atomSelection = []

                try:

                    _atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [{'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    lastCompId = None
                    pseudoAtoms = None

                    for _atom in _atomSelection:
                        compId = _atom['comp_id']
                        atomId = _atom['atom_id']

                        if compId is not lastCompId:
                            pseudoAtoms = self.csStat.getPseudoAtoms(compId)
                            lastCompId = compId

                        if atomId in pseudoAtoms:
                            atomSelection.append(_atom)

                except Exception as e:
                    if self.verbose:
                        self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                self.intersectionFactor_expressions(atomSelection)

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'pseudo' clause has no effect.")

            elif ctx.Residue():
                if self.verbose_debug:
                    print("  " * self.depth + "--> residue")

                eval_factor = False
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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['seq_id'] = [v if isinstance(v, int) else int(v) for v in val]
                        else:
                            self.factor['seq_id'] = [val if isinstance(val, int) else int(val)]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.cur_subtype == 'plane':
                            pass
                        elif self.cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
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
                    elif symbol_name in self.evaluateFor:
                        val = self.evaluateFor[symbol_name]
                        if isinstance(val, list):
                            self.factor['comp_id'] = [v.upper() for v in val]
                        else:
                            self.factor['comp_id'] = [val.upper()]
                    else:
                        self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                                      f"The symbol {symbol_name!r} is not defined.")

                if eval_factor and 'atom_selection' in self.factor:
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.cur_subtype == 'plane':
                            pass
                        elif self.cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The 'resname' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                          f"and {self.getReadableFactor(_factor)}.")

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
                            if 'atom_id' not in self.factor or not any(a in XPLOR_RDC_PRINCIPAL_AXIS_NAMES for a in self.factor['atom_id']):
                                self.factor['atom_id'] = [None]
                                if not self.with_axis\
                                   and 'segment_id_mismatch' in self.reasons\
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
                        elif symbol_name in self.evaluateFor:
                            val = self.evaluateFor[symbol_name]
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
                        if len(self.fibril_chain_ids) > 0 and not self.hasNonPoly:
                            if chainId[0] in self.fibril_chain_ids:
                                self.factor['chain_id'] = [chainId[0]]
                        elif self.monoPolymer and not self.hasBranched and not self.hasNonPoly:
                            self.factor['chain_id'] = self.polySeq[0]['auth_chain_id']
                            self.factor['auth_chain_id'] = chainId
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
                                    if not self.with_axis\
                                       and 'segment_id_mismatch' in self.reasons\
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
                    if len(self.factor['atom_selection']) == 0 and 'atom_id' in __factor:
                        __atomId = __factor['atom_id'][0].upper() if len(__factor['atom_id'][0]) <= 2 else __factor['atom_id'][0][:2].upper()
                        if self.with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                            pass
                        elif self.cur_subtype == 'plane':
                            pass
                        elif self.cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                            pass
                        else:
                            _factor = copy.copy(self.factor)
                            if 'atom_selection' in __factor:
                                del __factor['atom_selection']
                            del _factor['atom_selection']
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The 'segidentifier' clause has no effect for a conjunction of factor {self.getReadableFactor(__factor)} "
                                          f"and {self.getReadableFactor(_factor)}.")

            elif ctx.Sfbox():
                pass

            elif ctx.Store1():
                set_store(1)

            elif ctx.Store2():
                set_store(2)

            elif ctx.Store3():
                set_store(3)

            elif ctx.Store4():
                set_store(4)

            elif ctx.Store5():
                set_store(5)

            elif ctx.Store6():
                set_store(6)

            elif ctx.Store7():
                set_store(7)

            elif ctx.Store8():
                set_store(8)

            elif ctx.Store9():
                set_store(9)

            elif ctx.Tag():
                if self.verbose_debug:
                    print("  " * self.depth + "--> tag")
                if not self.hasCoord:
                    return
                atomSelection = []
                _sequenceSelect = []

                try:

                    _atomSelection =\
                        self.cR.getDictListWithFilter('atom_site',
                                                      AUTH_ATOM_DATA_ITEMS,
                                                      [{'name': self.modelNumName, 'type': 'int',
                                                        'value': self.representativeModelId},
                                                       {'name': 'label_alt_id', 'type': 'enum',
                                                        'enum': (self.representativeAltId,)}
                                                       ])

                    for _atom in _atomSelection:
                        _sequence = (_atom['chain_id'], _atom['seq_id'])

                        if _sequence in _sequenceSelect:
                            continue

                        atomSelection.append(_atom)
                        _sequenceSelect.append(_sequence)

                except Exception as e:
                    if self.verbose:
                        self.log.write(f"+{self.__class_name__}.exitFactor() ++ Error  - {str(e)}")

                self.intersectionFactor_expressions(atomSelection)

                if len(self.factor['atom_selection']) == 0:
                    self.factor['atom_id'] = [None]
                    self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                  "The 'tag' clause has no effect.")

            if self.depth > 0 and self.cur_union_expr:
                self.unionFactor = self.factor
            else:
                self.stackFactors.append(self.factor)

        finally:
            self.numberFSelection.clear()

    # Enter a parse tree produced by CnsMRParser#number.
    def enterNumber(self, ctx: CnsMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#number.
    def exitNumber(self, ctx: CnsMRParser.NumberContext):
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

    # Enter a parse tree produced by CnsMRParser#number_f.
    def enterNumber_f(self, ctx: CnsMRParser.Number_fContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#number_f.
    def exitNumber_f(self, ctx: CnsMRParser.Number_fContext):
        if ctx.Real():
            self.numberFSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberFSelection.append(float(str(ctx.Integer())))

        else:
            self.numberFSelection.append(None)

    # Enter a parse tree produced by CnsMRParser#number_s.
    def enterNumber_s(self, ctx: CnsMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#number_s.
    def exitNumber_s(self, ctx: CnsMRParser.Number_sContext):  # pylint: disable=unused-argument
        pass

    def getNumber_s(self, ctx: CnsMRParser.Number_sContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        if ctx.Symbol_name():
            return str(ctx.Symbol_name())

        return None

    # Enter a parse tree produced by CnsMRParser#number_a.
    def enterNumber_a(self, ctx: CnsMRParser.Number_aContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#number_a.
    def exitNumber_a(self, ctx: CnsMRParser.Number_aContext):  # pylint: disable=unused-argument
        pass

    def getNumber_a(self, ctx: CnsMRParser.Number_aContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Real():
            return float(str(ctx.Real()))

        if ctx.Integer():
            return float(str(ctx.Integer()))

        return None

    # Enter a parse tree produced by CnsMRParser#classification.
    def enterClassification(self, ctx: CnsMRParser.ClassificationContext):
        self.classification = self.getClass_name(ctx.class_name())

    # Exit a parse tree produced by CnsMRParser#classification.
    def exitClassification(self, ctx: CnsMRParser.ClassificationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#class_name.
    def enterClass_name(self, ctx: CnsMRParser.Class_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#class_name.
    def exitClass_name(self, ctx: CnsMRParser.Class_nameContext):  # pylint: disable=unused-argument
        pass

    def getClass_name(self, ctx: CnsMRParser.Class_nameContext):  # pylint: disable=no-self-use
        if ctx is None:
            return None

        if ctx.Simple_name():
            return str(ctx.Simple_name())

        if ctx.Noe():
            return str(ctx.Noe())

        if ctx.Restraints():
            return str(ctx.Restraints())

        if ctx.AngleDb():
            return str(ctx.AngleDb())

        if ctx.HBonded():
            return str(ctx.HBonded())

        if ctx.Dihedral():
            return str(ctx.Dihedral())

        if ctx.Improper():
            return str(ctx.Improper())

        return None

    # Enter a parse tree produced by CnsMRParser#flag_statement.
    def enterFlag_statement(self, ctx: CnsMRParser.Flag_statementContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#flag_statement.
    def exitFlag_statement(self, ctx: CnsMRParser.Flag_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#vector_statement.
    def enterVector_statement(self, ctx: CnsMRParser.Vector_statementContext):  # pylint: disable=unused-argument
        self.cur_vector_mode = ''
        self.cur_vector_atom_prop_type = ''

        self.cur_vflc_op_code = ''
        self.stackVflc = []

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#vector_statement.
    def exitVector_statement(self, ctx: CnsMRParser.Vector_statementContext):  # pylint: disable=unused-argument
        if self.cur_vector_mode == 'identity':
            if self.cur_vector_atom_prop_type.startswith('store'):
                self.storeSet[int(self.cur_vector_atom_prop_type[-1])] = {'atom_selection': copy.copy(self.atomSelectionSet[0])}

        elif self.cur_vector_mode == 'do':
            if len(self.cur_vector_atom_prop_type) > 0:
                vector_name = self.cur_vector_atom_prop_type
                if len(vector_name) > 4:
                    vector_name = vector_name[:4]
                if vector_name not in self.vectorDo:
                    self.vectorDo[vector_name] = []
                vector = {'atom_selection': copy.copy(self.atomSelectionSet[0])}
                while self.stackVflc:
                    vector['value'] = self.stackVflc.pop()
                self.vectorDo[vector_name].append(vector)

    # Enter a parse tree produced by CnsMRParser#vector_mode.
    def enterVector_mode(self, ctx: CnsMRParser.Vector_modeContext):
        if ctx.Identity_Lp():
            self.cur_vector_mode = 'identity'

        elif ctx.Do_Lp():
            self.cur_vector_mode = 'do'

        elif ctx.Show():
            self.cur_vector_mode = 'show'

    # Exit a parse tree produced by CnsMRParser#vector_mode.
    def exitVector_mode(self, ctx: CnsMRParser.Vector_modeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#vector_expression.
    def enterVector_expression(self, ctx: CnsMRParser.Vector_expressionContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#vector_expression.
    def exitVector_expression(self, ctx: CnsMRParser.Vector_expressionContext):
        if ctx.Atom_properties_VE():
            self.cur_vector_atom_prop_type = str(ctx.Atom_properties_VE()).lower()

    # Enter a parse tree produced by CnsMRParser#vector_operation.
    def enterVector_operation(self, ctx: CnsMRParser.Vector_operationContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#vector_operation.
    def exitVector_operation(self, ctx: CnsMRParser.Vector_operationContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#vflc.
    def enterVflc(self, ctx: CnsMRParser.VflcContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#vflc.
    def exitVflc(self, ctx: CnsMRParser.VflcContext):
        if ctx.Integer_VE():
            self.stackVflc.append(int(str(ctx.Integer_VE())))
        elif ctx.Real_VE():
            self.stackVflc.append(float(str(ctx.Real_VE())))
        elif ctx.Simple_name_VE():
            self.stackVflc.append(str(ctx.Simple_name_VE()))
        elif ctx.Double_quote_string_VE():
            self.stackVflc.append(str(ctx.Double_quote_string_VE()).strip('"').strip())
        elif ctx.Symbol_name_VE():
            symbol_name = str(ctx.Symbol_name_VE())
            if symbol_name in self.evaluate:
                self.stackVflc.append(self.evaluate[symbol_name])
            elif symbol_name in self.evaluateFor:
                self.stackVflc.append(self.evaluateFor[symbol_name])
            else:
                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              f"The symbol {symbol_name!r} is not defined.")
        elif ctx.Atom_properties_VE():
            pass
        elif ctx.vector_func_call():
            pass

    # Enter a parse tree produced by CnsMRParser#vector_func_call.
    def enterVector_func_call(self, ctx: CnsMRParser.Vector_func_callContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#vector_func_call.
    def exitVector_func_call(self, ctx: CnsMRParser.Vector_func_callContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#vector_show_property.
    def enterVector_show_property(self, ctx: CnsMRParser.Vector_show_propertyContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#vector_show_property.
    def exitVector_show_property(self, ctx: CnsMRParser.Vector_show_propertyContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#evaluate_statement.
    def enterEvaluate_statement(self, ctx: CnsMRParser.Evaluate_statementContext):
        if ctx.Symbol_name_VE():
            self.cur_symbol_name = str(ctx.Symbol_name_VE())

        self.cur_vflc_op_code = ''
        self.stackVflc = []

    # Exit a parse tree produced by CnsMRParser#evaluate_statement.
    def exitEvaluate_statement(self, ctx: CnsMRParser.Evaluate_statementContext):  # pylint: disable=unused-argument
        if self.stackVflc:
            self.evaluate[self.cur_symbol_name] = self.stackVflc[0]

            if self.cur_vflc_op_code in ('+', '-', '*', '/', '^'):
                s = self.stackVflc[0]
                n = self.stackVflc[1]
                if isinstance(s, list) and not isinstance(n, list):
                    if self.cur_vflc_op_code == '+':
                        self.evaluate[self.cur_symbol_name] = [_s + n for _s in s]
                    elif self.cur_vflc_op_code == '-':
                        self.evaluate[self.cur_symbol_name] = [_s - n for _s in s]
                    elif self.cur_vflc_op_code == '*':
                        self.evaluate[self.cur_symbol_name] = [_s * n for _s in s]
                    elif self.cur_vflc_op_code == '/':
                        self.evaluate[self.cur_symbol_name] = [_s / n for _s in s]
                    elif self.cur_vflc_op_code == '^':
                        self.evaluate[self.cur_symbol_name] = [_s ** n for _s in s]
                elif not isinstance(s, list) and isinstance(n, list):
                    if self.cur_vflc_op_code == '+':
                        self.evaluate[self.cur_symbol_name] = [s + _n for _n in n]
                    elif self.cur_vflc_op_code == '-':
                        self.evaluate[self.cur_symbol_name] = [s - _n for _n in n]
                    elif self.cur_vflc_op_code == '*':
                        self.evaluate[self.cur_symbol_name] = [s * _n for _n in n]
                    elif self.cur_vflc_op_code == '/':
                        self.evaluate[self.cur_symbol_name] = [s / _n for _n in n]
                    elif self.cur_vflc_op_code == '^':
                        self.evaluate[self.cur_symbol_name] = [s ** _n for _n in n]
                elif isinstance(s, list) and isinstance(n, list):
                    if self.cur_vflc_op_code == '+':
                        self.evaluate[self.cur_symbol_name] = [_s + _n for _s, _n in zip(s, n)]
                    elif self.cur_vflc_op_code == '-':
                        self.evaluate[self.cur_symbol_name] = [_s - _n for _s, _n in zip(s, n)]
                    elif self.cur_vflc_op_code == '*':
                        self.evaluate[self.cur_symbol_name] = [_s * _n for _s, _n in zip(s, n)]
                    elif self.cur_vflc_op_code == '/':
                        self.evaluate[self.cur_symbol_name] = [_s / _n for _s, _n in zip(s, n)]
                    elif self.cur_vflc_op_code == '^':
                        self.evaluate[self.cur_symbol_name] = [_s ** _n for _s, _n in zip(s, n)]
                else:
                    if self.cur_vflc_op_code == '+':
                        self.evaluate[self.cur_symbol_name] = s + n
                    elif self.cur_vflc_op_code == '-':
                        self.evaluate[self.cur_symbol_name] = s - n
                    elif self.cur_vflc_op_code == '*':
                        self.evaluate[self.cur_symbol_name] = s * n
                    elif self.cur_vflc_op_code == '/':
                        self.evaluate[self.cur_symbol_name] = s / n
                    elif self.cur_vflc_op_code == '^':
                        self.evaluate[self.cur_symbol_name] = s ** n

        self.stackVflc.clear()

    # Enter a parse tree produced by CnsMRParser#evaluate_operation.
    def enterEvaluate_operation(self, ctx: CnsMRParser.Evaluate_operationContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#evaluate_operation.
    def exitEvaluate_operation(self, ctx: CnsMRParser.Evaluate_operationContext):
        if ctx.Add_op_VE():
            self.cur_vflc_op_code = '+'
        elif ctx.Sub_op_VE():
            self.cur_vflc_op_code = '-'
        elif ctx.Mul_op_VE():
            self.cur_vflc_op_code = '*'
        elif ctx.Div_op_VE():
            self.cur_vflc_op_code = '/'
        elif ctx.Exp_op_VE():
            self.cur_vflc_op_code = '^'

    # Enter a parse tree produced by CnsMRParser#patch_statement.
    def enterPatch_statement(self, ctx: CnsMRParser.Patch_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        self.cur_subtype = 'geo'

        self.atomSelectionSet.clear()
        self.g.clear()

    # Exit a parse tree produced by CnsMRParser#patch_statement.
    def exitPatch_statement(self, ctx: CnsMRParser.Patch_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#parameter_setting.
    def enterParameter_setting(self, ctx: CnsMRParser.Parameter_settingContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CnsMRParser#parameter_setting.
    def exitParameter_setting(self, ctx: CnsMRParser.Parameter_settingContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#parameter_statement.
    def enterParameter_statement(self, ctx: CnsMRParser.Parameter_statementContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1
        self.cur_subtype = 'geo'

    # Exit a parse tree produced by CnsMRParser#parameter_statement.
    def exitParameter_statement(self, ctx: CnsMRParser.Parameter_statementContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CnsMRParser#noe_assign_loop.
    def enterNoe_assign_loop(self, ctx: CnsMRParser.Noe_assign_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#noe_assign_loop.
    def exitNoe_assign_loop(self, ctx: CnsMRParser.Noe_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

    # Enter a parse tree produced by CnsMRParser#dihedral_assign_loop.
    def enterDihedral_assign_loop(self, ctx: CnsMRParser.Dihedral_assign_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#dihedral_assign_loop.
    def exitDihedral_assign_loop(self, ctx: CnsMRParser.Dihedral_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

    # Enter a parse tree produced by CnsMRParser#sani_assign_loop.
    def enterSani_assign_loop(self, ctx: CnsMRParser.Sani_assign_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#sani_assign_loop.
    def exitSani_assign_loop(self, ctx: CnsMRParser.Sani_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

    # Enter a parse tree produced by CnsMRParser#coup_assign_loop.
    def enterCoup_assign_loop(self, ctx: CnsMRParser.Coup_assign_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#coup_assign_loop.
    def exitCoup_assign_loop(self, ctx: CnsMRParser.Coup_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

    # Enter a parse tree produced by CnsMRParser#carbon_shift_assign_loop.
    def enterCarbon_shift_assign_loop(self, ctx: CnsMRParser.Carbon_shift_assign_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#carbon_shift_assign_loop.
    def exitCarbon_shift_assign_loop(self, ctx: CnsMRParser.Carbon_shift_assign_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

    # Enter a parse tree produced by CnsMRParser#plane_group_loop.
    def enterPlane_group_loop(self, ctx: CnsMRParser.Plane_group_loopContext):
        self.in_loop = True

        symbol_name = None
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())

        if ctx.Integer_CF(0):
            int_list = []
            idx = 0
            while True:
                if ctx.Integer_CF(idx):
                    int_list.append(int(str(ctx.Integer_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = int_list

        if ctx.Real_CF(0):
            real_list = []
            idx = 0
            while True:
                if ctx.Real_CF(idx):
                    real_list.append(float(str(ctx.Real_CF(idx))))
                    idx += 1
                else:
                    break
            if symbol_name[0] is not None:
                self.evaluateFor[symbol_name] = real_list

        if ctx.Simple_name_CF(0):
            str_list = []
            idx = 0
            while True:
                if ctx.Simple_name_CF(idx):
                    str_list.append(str(ctx.Simple_name_CF(idx)))
                    idx += 1
                else:
                    break
            if symbol_name is not None:
                self.evaluateFor[symbol_name] = str_list

    # Exit a parse tree produced by CnsMRParser#plane_group_loop.
    def exitPlane_group_loop(self, ctx: CnsMRParser.Plane_group_loopContext):
        if ctx.Symbol_name_CF():
            symbol_name = str(ctx.Symbol_name_CF())
            if symbol_name in self.evaluateFor:
                del self.evaluateFor[symbol_name]

        self.in_loop = False

# del CnsMRParser
