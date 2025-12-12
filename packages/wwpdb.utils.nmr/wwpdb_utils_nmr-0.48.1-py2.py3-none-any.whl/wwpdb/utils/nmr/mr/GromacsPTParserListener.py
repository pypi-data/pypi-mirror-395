##
# File: GromacsPTParserListener.py
# Date: 02-Jun-2022
#
# Updates:
""" ParserLister class for GROMACS PT files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import NAMES_ELEMENT  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.GromacsPTParser import GromacsPTParser
    from wwpdb.utils.nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           protonBeginCode,
                                           letterToDigit,
                                           indexToLetter,
                                           retrieveAtomIdentFromMRMap)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.GromacsPTParser import GromacsPTParser
    from nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from nmr.mr.ParserListenerUtil import (REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode,
                               letterToDigit,
                               indexToLetter,
                               retrieveAtomIdentFromMRMap)


# This class defines a complete listener for a parse tree produced by GromacsPTParser.
class GromacsPTParserListener(ParseTreeListener, BaseTopologyParserListener):
    __slots__ = ('defaultStatements',
                 'moleculetypeStatements',
                 'atomtypesStatements',
                 'pairtypesStatements',
                 'bondtypesStatements',
                 'angletypesStatements',
                 'dihedraltypesStatements',
                 'constrainttypesStatements',
                 'nonbond_paramsStatements',
                 'atomsStatements',
                 'bondsStatements',
                 'pairsStatements',
                 'pairs_nbStatements',
                 'anglesStatements',
                 'dihedralsStatements',
                 'exclusionsStatements',
                 'constraintsStatements',
                 'settlesStatements',
                 'virtual_sites1Statements',
                 'virtual_sites2Statements',
                 'virtual_sites3Statements',
                 'virtual_sites4Statements',
                 'virtual_sitesnStatements',
                 'systemStatements',
                 'moleculesStatements')

    # system
    __system = None

    # molecules
    __molecules = []

    # collection of number selection
    numberSelection = []

    # __cur_column_len = None
    __cur_word_len = None

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        super().__init__(verbose, log, representativeModelId, representativeAltId, mrAtomNameMapping,
                         cR, caC, nefT)

        self.file_type = 'nm-aux-gro'

        self.defaultStatements = 0
        self.moleculetypeStatements = 0
        self.atomtypesStatements = 0
        self.pairtypesStatements = 0
        self.bondtypesStatements = 0
        self.angletypesStatements = 0
        self.dihedraltypesStatements = 0
        self.constrainttypesStatements = 0
        self.nonbond_paramsStatements = 0
        self.atomsStatements = 0
        self.bondsStatements = 0
        self.pairsStatements = 0
        self.pairs_nbStatements = 0
        self.anglesStatements = 0
        self.dihedralsStatements = 0
        self.exclusionsStatements = 0
        self.constraintsStatements = 0
        self.settlesStatements = 0
        self.virtual_sites1Statements = 0
        self.virtual_sites2Statements = 0
        self.virtual_sites3Statements = 0
        self.virtual_sites4Statements = 0
        self.virtual_sitesnStatements = 0
        self.systemStatements = 0
        self.moleculesStatements = 0

    # Enter a parse tree produced by GromacsPTParser#gromacs_pt.
    def enterGromacs_pt(self, ctx: GromacsPTParser.Gromacs_ptContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#gromacs_pt.
    def exitGromacs_pt(self, ctx: GromacsPTParser.Gromacs_ptContext):  # pylint: disable=unused-argument

        if not self.hasPolySeqModel:
            return

        if len(self.atoms) == 0:
            return

        chainIndex = letterToDigit(self.polySeqModel[0]['chain_id']) - 1  # set tentative chain_id from label_asym_id, which will be assigned to coordinate auth_asym_id
        chainId = indexToLetter(chainIndex)

        terminus = [atom['auth_atom_id'].endswith('T') for atom in self.atoms]

        atomTotal = len(self.atoms)
        if terminus[0]:
            terminus[0] = False
        for i in range(0, atomTotal - 1):
            j = i + 1
            if terminus[i] and terminus[j]:
                terminus[i] = False
        if terminus[-1]:
            terminus[-1] = False

        seqIdList, compIdList, retrievedAtomNumList = [], [], []

        hasSegCompId = False
        ancAtomName = prevAtomName = ''
        prevSeqId = prevCompId = None
        offset = 0
        for atom in self.atoms:
            atomNum = atom['atom_number']
            atomName = atom['auth_atom_id']
            atomType = atom['atom_type']
            _seqId = atom['auth_seq_id']
            compId = atom['auth_comp_id']
            if self.noWaterMol and (compId in ('HOH', 'H2O', 'WAT') or (len(compId) > 3 and compId[:3] in ('HOH', 'H2O', 'WAT'))):
                break
            if not hasSegCompId and (compId.endswith('5') or compId.endswith('3')):
                hasSegCompId = True
            if not hasSegCompId and compId not in monDict3 and self.mrAtomNameMapping is not None and atomName[0] in protonBeginCode:
                _, compId, _atomName = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, _seqId, compId, atomName)
                if _atomName != atomName:
                    atomName = _atomName
                    retrievedAtomNumList.append(atomNum)

            if (0 < atomNum < len(terminus) + 1
                and ((terminus[atomNum - 1] and ancAtomName.endswith('T'))
                     or (terminus[atomNum - 2] and prevAtomName.endswith('T')
                         and self.csStat.getTypeOfCompId(prevCompId) != self.csStat.getTypeOfCompId(compId))))\
               or self.isSegment(prevCompId, prevAtomName, compId, atomName)\
               or self.isLigand(prevCompId, compId)\
               or self.isMetalIon(compId, atomName)\
               or self.isMetalIon(prevCompId, prevAtomName)\
               or self.isMetalElem(prevAtomName, prevSeqId, _seqId):

                self.polySeqPrmTop.append({'chain_id': chainId,
                                           'seq_id': seqIdList,
                                           'auth_comp_id': compIdList})
                seqIdList, compIdList = [], []
                chainIndex += 1
                chainId = indexToLetter(chainIndex)
                offset = 1 - _seqId

            seqId = _seqId + offset
            if seqId not in seqIdList:
                seqIdList.append(seqId)
                compIdList.append(compId)
            self.atomNumberDict[atomNum] = {'chain_id': chainId,
                                            'seq_id': seqId,
                                            'auth_comp_id': compId,
                                            'auth_atom_id': atomName,
                                            'atom_type': atomType}
            ancAtomName = prevAtomName
            prevAtomName = atomName
            prevSeqId = _seqId
            prevCompId = compId

        self.polySeqPrmTop.append({'chain_id': chainId,
                                   'seq_id': seqIdList,
                                   'auth_comp_id': compIdList})

        self.exit(retrievedAtomNumList)

    # Enter a parse tree produced by GromacsPTParser#default_statement.
    def enterDefault_statement(self, ctx: GromacsPTParser.Default_statementContext):  # pylint: disable=unused-argument
        self.defaultStatements += 1

    # Exit a parse tree produced by GromacsPTParser#default_statement.
    def exitDefault_statement(self, ctx: GromacsPTParser.Default_statementContext):
        if ctx.Integer(0):
            return
        self.defaultStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#moleculetype_statement.
    def enterMoleculetype_statement(self, ctx: GromacsPTParser.Moleculetype_statementContext):  # pylint: disable=unused-argument
        self.moleculetypeStatements += 1

    # Exit a parse tree produced by GromacsPTParser#moleculetype_statement.
    def exitMoleculetype_statement(self, ctx: GromacsPTParser.Moleculetype_statementContext):
        if ctx.moleculetype(0):
            return
        self.moleculetypeStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#moleculetype.
    def enterMoleculetype(self, ctx: GromacsPTParser.MoleculetypeContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#moleculetype.
    def exitMoleculetype(self, ctx: GromacsPTParser.MoleculetypeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#atomtypes_statement.
    def enterAtomtypes_statement(self, ctx: GromacsPTParser.Atomtypes_statementContext):  # pylint: disable=unused-argument
        self.atomtypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#atomtypes_statement.
    def exitAtomtypes_statement(self, ctx: GromacsPTParser.Atomtypes_statementContext):
        if ctx.atomtypes(0):
            return
        self.atomtypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#atomtypes.
    def enterAtomtypes(self, ctx: GromacsPTParser.AtomtypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#atomtypes.
    def exitAtomtypes(self, ctx: GromacsPTParser.AtomtypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#pairtypes_statement.
    def enterPairtypes_statement(self, ctx: GromacsPTParser.Pairtypes_statementContext):  # pylint: disable=unused-argument
        self.pairtypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#pairtypes_statement.
    def exitPairtypes_statement(self, ctx: GromacsPTParser.Pairtypes_statementContext):
        if ctx.pairtypes(0):
            return
        self.pairtypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#pairtypes.
    def enterPairtypes(self, ctx: GromacsPTParser.PairtypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#pairtypes.
    def exitPairtypes(self, ctx: GromacsPTParser.PairtypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#bondtypes_statement.
    def enterBondtypes_statement(self, ctx: GromacsPTParser.Bondtypes_statementContext):  # pylint: disable=unused-argument
        self.bondtypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#bondtypes_statement.
    def exitBondtypes_statement(self, ctx: GromacsPTParser.Bondtypes_statementContext):
        if ctx.bondtypes(0):
            return
        self.bondtypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#bondtypes.
    def enterBondtypes(self, ctx: GromacsPTParser.BondtypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#bondtypes.
    def exitBondtypes(self, ctx: GromacsPTParser.BondtypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#angletypes_statement.
    def enterAngletypes_statement(self, ctx: GromacsPTParser.Angletypes_statementContext):  # pylint: disable=unused-argument
        self.angletypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#angletypes_statement.
    def exitAngletypes_statement(self, ctx: GromacsPTParser.Angletypes_statementContext):
        if ctx.angletypes(0):
            return
        self.angletypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#angletypes.
    def enterAngletypes(self, ctx: GromacsPTParser.AngletypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#angletypes.
    def exitAngletypes(self, ctx: GromacsPTParser.AngletypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#dihedraltypes_statement.
    def enterDihedraltypes_statement(self, ctx: GromacsPTParser.Dihedraltypes_statementContext):  # pylint: disable=unused-argument
        self.dihedraltypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#dihedraltypes_statement.
    def exitDihedraltypes_statement(self, ctx: GromacsPTParser.Dihedraltypes_statementContext):
        if ctx.dihedraltypes(0):
            return
        self.dihedraltypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#dihedraltypes.
    def enterDihedraltypes(self, ctx: GromacsPTParser.DihedraltypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#dihedraltypes.
    def exitDihedraltypes(self, ctx: GromacsPTParser.DihedraltypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#constrainttypes_statement.
    def enterConstrainttypes_statement(self, ctx: GromacsPTParser.Constrainttypes_statementContext):  # pylint: disable=unused-argument
        self.constrainttypesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#constrainttypes_statement.
    def exitConstrainttypes_statement(self, ctx: GromacsPTParser.Constrainttypes_statementContext):
        if ctx.constrainttypes(0):
            return
        self.constrainttypesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#constrainttypes.
    def enterConstrainttypes(self, ctx: GromacsPTParser.ConstrainttypesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#constrainttypes.
    def exitConstrainttypes(self, ctx: GromacsPTParser.ConstrainttypesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#nonbonded_params_statement.
    def enterNonbonded_params_statement(self, ctx: GromacsPTParser.Nonbonded_params_statementContext):  # pylint: disable=unused-argument
        self.nonbond_paramsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#nonbonded_params_statement.
    def exitNonbonded_params_statement(self, ctx: GromacsPTParser.Nonbonded_params_statementContext):
        if ctx.nonbonded_params(0):
            return
        self.nonbond_paramsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#nonbonded_params.
    def enterNonbonded_params(self, ctx: GromacsPTParser.Nonbonded_paramsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#nonbonded_params.
    def exitNonbonded_params(self, ctx: GromacsPTParser.Nonbonded_paramsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#atoms_statement.
    def enterAtoms_statement(self, ctx: GromacsPTParser.Atoms_statementContext):  # pylint: disable=unused-argument
        self.atomsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#atoms_statement.
    def exitAtoms_statement(self, ctx: GromacsPTParser.Atoms_statementContext):  # pylint: disable=unused-argument
        if ctx.atoms(0):
            return
        self.atomsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#atoms.
    def enterAtoms(self, ctx: GromacsPTParser.AtomsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#atoms.
    def exitAtoms(self, ctx: GromacsPTParser.AtomsContext):

        try:

            nr = int(str(ctx.Integer(0)))

            if nr < 0 or nr <= self.prev_nr:
                return

            self.prev_nr = nr

            seqId = int(str(ctx.Integer(1)))
            # cgnr = int(str(ctx.Integer(2)))

            type = str(ctx.Simple_name(0))
            compId = str(ctx.Simple_name(1))
            atomId = str(ctx.Simple_name(2))

            atom = {'atom_number': nr,
                    'auth_seq_id': seqId,
                    'auth_comp_id': compId,
                    'auth_atom_id': atomId,
                    'atom_type': type}

            if atom not in self.atoms:
                self.atoms.append(atom)

        except ValueError:
            pass

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by GromacsPTParser#bonds_statement.
    def enterBonds_statement(self, ctx: GromacsPTParser.Bonds_statementContext):  # pylint: disable=unused-argument
        self.bondsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#bonds_statement.
    def exitBonds_statement(self, ctx: GromacsPTParser.Bonds_statementContext):
        if ctx.bonds(0):
            return
        self.bondsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#bonds.
    def enterBonds(self, ctx: GromacsPTParser.BondsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#bonds.
    def exitBonds(self, ctx: GromacsPTParser.BondsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#pairs_statement.
    def enterPairs_statement(self, ctx: GromacsPTParser.Pairs_statementContext):  # pylint: disable=unused-argument
        self.pairsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#pairs_statement.
    def exitPairs_statement(self, ctx: GromacsPTParser.Pairs_statementContext):
        if ctx.pairs(0):
            return
        self.pairsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#pairs.
    def enterPairs(self, ctx: GromacsPTParser.PairsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#pairs.
    def exitPairs(self, ctx: GromacsPTParser.PairsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#pairs_nb_statement.
    def enterPairs_nb_statement(self, ctx: GromacsPTParser.Pairs_nb_statementContext):  # pylint: disable=unused-argument
        self.pairs_nbStatements += 1

    # Exit a parse tree produced by GromacsPTParser#pairs_nb_statement.
    def exitPairs_nb_statement(self, ctx: GromacsPTParser.Pairs_nb_statementContext):
        if ctx.pairs_nb(0):
            return
        self.pairs_nbStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#pairs_nb.
    def enterPairs_nb(self, ctx: GromacsPTParser.Pairs_nbContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#pairs_nb.
    def exitPairs_nb(self, ctx: GromacsPTParser.Pairs_nbContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#angles_statement.
    def enterAngles_statement(self, ctx: GromacsPTParser.Angles_statementContext):  # pylint: disable=unused-argument
        self.anglesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#angles_statement.
    def exitAngles_statement(self, ctx: GromacsPTParser.Angles_statementContext):
        if ctx.angles(0):
            return
        self.anglesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#angles.
    def enterAngles(self, ctx: GromacsPTParser.AnglesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#angles.
    def exitAngles(self, ctx: GromacsPTParser.AnglesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#dihedrals_statement.
    def enterDihedrals_statement(self, ctx: GromacsPTParser.Dihedrals_statementContext):  # pylint: disable=unused-argument
        self.dihedralsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#dihedrals_statement.
    def exitDihedrals_statement(self, ctx: GromacsPTParser.Dihedrals_statementContext):
        if ctx.dihedrals(0):
            return
        self.dihedralsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#dihedrals.
    def enterDihedrals(self, ctx: GromacsPTParser.DihedralsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#dihedrals.
    def exitDihedrals(self, ctx: GromacsPTParser.DihedralsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#exclusions_statement.
    def enterExclusions_statement(self, ctx: GromacsPTParser.Exclusions_statementContext):  # pylint: disable=unused-argument
        self.exclusionsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#exclusions_statement.
    def exitExclusions_statement(self, ctx: GromacsPTParser.Exclusions_statementContext):
        if ctx.exclusions(0):
            return
        self.exclusionsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#exclusions.
    def enterExclusions(self, ctx: GromacsPTParser.ExclusionsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#exclusions.
    def exitExclusions(self, ctx: GromacsPTParser.ExclusionsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#constraints_statement.
    def enterConstraints_statement(self, ctx: GromacsPTParser.Constraints_statementContext):  # pylint: disable=unused-argument
        self.constraintsStatements += 1

    # Exit a parse tree produced by GromacsPTParser#constraints_statement.
    def exitConstraints_statement(self, ctx: GromacsPTParser.Constraints_statementContext):
        if ctx.constraints(0):
            return
        self.constraintsStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#constraints.
    def enterConstraints(self, ctx: GromacsPTParser.ConstraintsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#constraints.
    def exitConstraints(self, ctx: GromacsPTParser.ConstraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#settles_statement.
    def enterSettles_statement(self, ctx: GromacsPTParser.Settles_statementContext):  # pylint: disable=unused-argument
        self.settlesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#settles_statement.
    def exitSettles_statement(self, ctx: GromacsPTParser.Settles_statementContext):
        if ctx.settles(0):
            return
        self.settlesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#settles.
    def enterSettles(self, ctx: GromacsPTParser.SettlesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#settles.
    def exitSettles(self, ctx: GromacsPTParser.SettlesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#virtual_sites1_statement.
    def enterVirtual_sites1_statement(self, ctx: GromacsPTParser.Virtual_sites1_statementContext):  # pylint: disable=unused-argument
        self.virtual_sites1Statements += 1

    # Exit a parse tree produced by GromacsPTParser#virtual_sites1_statement.
    def exitVirtual_sites1_statement(self, ctx: GromacsPTParser.Virtual_sites1_statementContext):
        if ctx.virtual_sites1(0):
            return
        self.virtual_sites1Statements -= 1

    # Enter a parse tree produced by GromacsPTParser#virtual_sites1.
    def enterVirtual_sites1(self, ctx: GromacsPTParser.Virtual_sites1Context):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#virtual_sites1.
    def exitVirtual_sites1(self, ctx: GromacsPTParser.Virtual_sites1Context):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#virtual_sites2_statement.
    def enterVirtual_sites2_statement(self, ctx: GromacsPTParser.Virtual_sites2_statementContext):  # pylint: disable=unused-argument
        self.virtual_sites2Statements += 1

    # Exit a parse tree produced by GromacsPTParser#virtual_sites2_statement.
    def exitVirtual_sites2_statement(self, ctx: GromacsPTParser.Virtual_sites2_statementContext):
        if ctx.virtual_sites2(0):
            return
        self.virtual_sites2Statements -= 1

    # Enter a parse tree produced by GromacsPTParser#virtual_sites2.
    def enterVirtual_sites2(self, ctx: GromacsPTParser.Virtual_sites2Context):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#virtual_sites2.
    def exitVirtual_sites2(self, ctx: GromacsPTParser.Virtual_sites2Context):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#virtual_sites3_statement.
    def enterVirtual_sites3_statement(self, ctx: GromacsPTParser.Virtual_sites3_statementContext):  # pylint: disable=unused-argument
        self.virtual_sites3Statements += 1

    # Exit a parse tree produced by GromacsPTParser#virtual_sites3_statement.
    def exitVirtual_sites3_statement(self, ctx: GromacsPTParser.Virtual_sites3_statementContext):
        if ctx.virtual_sites3(0):
            return
        self.virtual_sites3Statements -= 1

    # Enter a parse tree produced by GromacsPTParser#virtual_sites3.
    def enterVirtual_sites3(self, ctx: GromacsPTParser.Virtual_sites3Context):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#virtual_sites3.
    def exitVirtual_sites3(self, ctx: GromacsPTParser.Virtual_sites3Context):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#virtual_sites4_statement.
    def enterVirtual_sites4_statement(self, ctx: GromacsPTParser.Virtual_sites4_statementContext):  # pylint: disable=unused-argument
        self.virtual_sites4Statements += 1

    # Exit a parse tree produced by GromacsPTParser#virtual_sites4_statement.
    def exitVirtual_sites4_statement(self, ctx: GromacsPTParser.Virtual_sites4_statementContext):
        if ctx.virtual_sites4(0):
            return
        self.virtual_sites4Statements -= 1

    # Enter a parse tree produced by GromacsPTParser#virtual_sites4.
    def enterVirtual_sites4(self, ctx: GromacsPTParser.Virtual_sites4Context):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#virtual_sites4.
    def exitVirtual_sites4(self, ctx: GromacsPTParser.Virtual_sites4Context):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#virtual_sitesn_statement.
    def enterVirtual_sitesn_statement(self, ctx: GromacsPTParser.Virtual_sitesn_statementContext):  # pylint: disable=unused-argument
        self.virtual_sitesnStatements += 1

    # Exit a parse tree produced by GromacsPTParser#virtual_sitesn_statement.
    def exitVirtual_sitesn_statement(self, ctx: GromacsPTParser.Virtual_sitesn_statementContext):
        if ctx.virtual_sitesn(0):
            return
        self.virtual_sitesnStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#virtual_sitesn.
    def enterVirtual_sitesn(self, ctx: GromacsPTParser.Virtual_sitesnContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#virtual_sitesn.
    def exitVirtual_sitesn(self, ctx: GromacsPTParser.Virtual_sitesnContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#system_statement.
    def enterSystem_statement(self, ctx: GromacsPTParser.System_statementContext):  # pylint: disable=unused-argument
        self.systemStatements += 1

    # Exit a parse tree produced by GromacsPTParser#system_statement.
    def exitSystem_statement(self, ctx: GromacsPTParser.System_statementContext):
        if ctx.Simple_name_AA(0):
            if self.hasCoord:
                title = []
                i = 0
                while ctx.Simple_name_AA(i):
                    title.append(str(ctx.Simple_name_AA(i)))
                    i += 1

                self.__system = ' '.join(title)
            return
        self.systemStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#molecules_statement.
    def enterMolecules_statement(self, ctx: GromacsPTParser.Molecules_statementContext):  # pylint: disable=unused-argument
        self.moleculesStatements += 1

    # Exit a parse tree produced by GromacsPTParser#molecules_statement.
    def exitMolecules_statement(self, ctx: GromacsPTParser.Molecules_statementContext):
        if ctx.molecules(0):
            return
        self.moleculesStatements -= 1

    # Enter a parse tree produced by GromacsPTParser#molecules.
    def enterMolecules(self, ctx: GromacsPTParser.MoleculesContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#molecules.
    def exitMolecules(self, ctx: GromacsPTParser.MoleculesContext):
        name = str(ctx.Simple_name())
        number = int(str(ctx.Integer()))
        if number > 0:
            self.__molecules.append({'molecule_name': name, 'number_of_copies': number})

    # Enter a parse tree produced by GromacsPTParser#number.
    def enterNumber(self, ctx: GromacsPTParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#number.
    def exitNumber(self, ctx: GromacsPTParser.NumberContext):
        """ not used the 'number' in the '[ atoms ]' statement so that pass through for performance
        if ctx.Real():
            self.numberSelection.append(float(str(ctx.Real())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)
        """

    # Enter a parse tree produced by GromacsPTParser#position_restraints.
    def enterPosition_restraints(self, ctx: GromacsPTParser.Position_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#position_restraints.
    def exitPosition_restraints(self, ctx: GromacsPTParser.Position_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by GromacsPTParser#position_restraint.
    def enterPosition_restraint(self, ctx: GromacsPTParser.Position_restraintContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by GromacsPTParser#position_restraint.
    def exitPosition_restraint(self, ctx: GromacsPTParser.Position_restraintContext):  # pylint: disable=unused-argument
        pass

    def getContentSubtype(self) -> dict:
        """ Return content subtype of GROMACS parameter/topology file.
        """

        contentSubtype = {'default': self.defaultStatements,
                          'moleculetype': self.moleculetypeStatements,
                          'atomtypes': self.atomtypesStatements,
                          'pairtypes': self.pairtypesStatements,
                          'bondtypes': self.bondtypesStatements,
                          'angletypes': self.angletypesStatements,
                          'dihedraltypes': self.dihedraltypesStatements,
                          'constrainttypes': self.constrainttypesStatements,
                          'nonbond_params': self.nonbond_paramsStatements,
                          'atoms': self.atomsStatements,
                          'bonds': self.bondsStatements,
                          'pairs': self.pairsStatements,
                          'pairs_nb': self.pairs_nbStatements,
                          'angles': self.anglesStatements,
                          'dihedrals': self.dihedralsStatements,
                          'exclusions': self.exclusionsStatements,
                          'constraints': self.constraintsStatements,
                          'settles': self.settlesStatements,
                          'virtual_sites1': self.virtual_sites1Statements,
                          'virtual_sites2': self.virtual_sites2Statements,
                          'virtual_sites3': self.virtual_sites3Statements,
                          'virtual_sites4': self.virtual_sites4Statements,
                          'virtual_sitesn': self.virtual_sitesnStatements,
                          'system': self.systemStatements,
                          'molecules': self.moleculesStatements
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getSystem(self) -> Optional[str]:
        """ Return system name of GROMACS parameter/topology file.
        """

        return self.__system

    def getMolecules(self) -> List[dict]:
        """ Return list of molecules and its number of copies in GROMACS parameter/topology file.
        """

        return self.__molecules

# del GromacsPTParser
