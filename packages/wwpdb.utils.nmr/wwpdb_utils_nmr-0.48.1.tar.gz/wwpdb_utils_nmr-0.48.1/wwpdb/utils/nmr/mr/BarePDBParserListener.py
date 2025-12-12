##
# File: BarePDBParserListener.py
# Date: 19-Sep-2025
#
# Updates:
""" ParserLister class for Bare PDB files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import re

from antlr4 import ParseTreeListener
from rmsd.calculate_rmsd import NAMES_ELEMENT  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.BarePDBParser import BarePDBParser
    from wwpdb.utils.nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (translateToStdResName,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           protonBeginCode,
                                           letterToDigit,
                                           indexToLetter,
                                           retrieveAtomIdentFromMRMap)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.BarePDBParser import BarePDBParser
    from nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from nmr.mr.ParserListenerUtil import (translateToStdResName,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode,
                               letterToDigit,
                               indexToLetter,
                               retrieveAtomIdentFromMRMap)


# This class defines a complete listener for a parse tree produced by BarePDBParser.
class BarePDBParserListener(ParseTreeListener, BaseTopologyParserListener):
    __slots__ = ('coordinatesStatements', )

    # total appearances of TER clause
    __ter_count = 0
    # offset value for atom number due to TER clause
    __ter_offset = 0
    # END clause
    __end = False

    # collection of atom name selection
    atomNameSelection = []

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

        self.file_type = 'nm-aux-pdb'

        self.coordinatesStatements = 0

    # Enter a parse tree produced by BarePDBParser#bare_pdb.
    def enterBare_pdb(self, ctx: BarePDBParser.Bare_pdbContext):  # pylint: disable=unused-argument
        self.__ter_count = 0
        self.__ter_offset = 0
        self.__end = False

    # Exit a parse tree produced by BarePDBParser#bare_pdb.
    def exitBare_pdb(self, ctx: BarePDBParser.Bare_pdbContext):  # pylint: disable=unused-argument

        if not self.hasPolySeqModel:
            return

        if len(self.atoms) == 0:
            return

        chainIndex = letterToDigit(self.polySeqModel[0]['chain_id']) - 1  # set tentative chain_id from label_asym_id, which will be assigned to coordinate auth_asym_id
        chainId = indexToLetter(chainIndex)

        terminus = [atom['auth_atom_id'].endswith('T') for atom in self.atoms if isinstance(atom, dict)]

        atomTotal = len(terminus)

        if atomTotal == 0:
            return

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
        prevAsymId = prevSeqId = prevCompId = None
        offset = 0
        for atom in self.atoms:

            if isinstance(atom, str):
                self.polySeqPrmTop.append({'chain_id': chainId,
                                           'seq_id': seqIdList,
                                           'auth_comp_id': compIdList})
                seqIdList, compIdList = [], []
                chainIndex += 1
                chainId = indexToLetter(chainIndex)
                offset = 0
                continue

            atomNum = atom['atom_number']
            atomName = atom['auth_atom_id']
            asymId = atom['auth_chain_id']
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

            if (offset > 0 or self.__ter_count == 0)\
               and ((0 < atomNum < len(terminus) + 1
                     and ((terminus[atomNum - 1] and ancAtomName.endswith('T'))
                          or (terminus[atomNum - 2] and prevAtomName.endswith('T')
                              and self.csStat.getTypeOfCompId(prevCompId) != self.csStat.getTypeOfCompId(compId))))
                    or self.isSegmentWithAsymHint(prevAsymId, prevCompId, prevAtomName, asymId, compId, atomName)
                    or self.isLigand(prevCompId, compId)
                    or self.isMetalIon(compId, atomName)
                    or self.isMetalIon(prevCompId, prevAtomName)
                    or self.isMetalElem(prevAtomName, prevSeqId, _seqId)):

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
                                            'auth_atom_id': atomName}
            ancAtomName = prevAtomName
            prevAtomName = atomName
            prevAsymId = asymId
            prevSeqId = _seqId
            prevCompId = compId

        if len(self.polySeqPrmTop) == 0:
            if len(seqIdList) > 0:
                self.polySeqPrmTop.append({'chain_id': chainId,
                                           'seq_id': seqIdList,
                                           'auth_comp_id': compIdList})

        self.exit(retrievedAtomNumList)

    # Enter a parse tree produced by BarePDBParser#comment.
    def enterComment(self, ctx: BarePDBParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#comment.
    def exitComment(self, ctx: BarePDBParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#coordinates.
    def enterCoordinates(self, ctx: BarePDBParser.CoordinatesContext):  # pylint: disable=unused-argument
        self.coordinatesStatements += 1

    # Exit a parse tree produced by BarePDBParser#coordinates.
    def exitCoordinates(self, ctx: BarePDBParser.CoordinatesContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#atom_coordinate.
    def enterAtom_coordinate(self, ctx: BarePDBParser.Atom_coordinateContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#atom_coordinate.
    def exitAtom_coordinate(self, ctx: BarePDBParser.Atom_coordinateContext):

        try:

            if self.__end:
                return

            nr = self.cur_nr

            if nr < 0 or nr <= self.prev_nr:
                return

            self.prev_nr = nr

            if ctx.Integer(1):
                chainId = str(ctx.Integer(0))
                seqId = int(str(ctx.Integer(1)))
            elif ctx.Integer(0):
                seqId = int(str(ctx.Integer(0)))
                chainId = str(ctx.Simple_name()) if ctx.Simple_name() else None
            elif ctx.Integer_concat_alt():
                seqId = int(str(ctx.Integer_concat_alt())[:-1])
                chainId = str(ctx.Simple_name()) if ctx.Simple_name() else None
            else:
                concat_string = str(ctx.Simple_name())
                integers = re.findall(r'\d+', concat_string)
                seqId = int(integers[0])
                chainId = concat_string[:concat_string.index(integers[0])]

            atomId = self.atomNameSelection[0]

            if atomId is None:
                return

            compId = self.atomNameSelection[1]

            if atomId.endswith('*'):
                _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

            atom = {'atom_number': nr + self.__ter_offset,
                    'auth_chain_id': chainId,
                    'auth_seq_id': seqId,
                    'auth_comp_id': compId,
                    'auth_atom_id': atomId}

            if atom not in self.atoms:
                self.atoms.append(atom)

        except (ValueError, IndexError):
            pass

        finally:
            self.atomNameSelection.clear()

    # Enter a parse tree produced by BarePDBParser#atom_num.
    def enterAtom_num(self, ctx: BarePDBParser.Atom_numContext):
        if ctx.Atom() and ctx.Integer():
            self.cur_nr = int(str(ctx.Integer()))
        elif ctx.Hetatm() and ctx.Integer():
            self.cur_nr = int(str(ctx.Integer()))
        elif ctx.Hetatm_decimal():
            concat_string = str(ctx.Hetatm_decimal())
            self.cur_nr = int(concat_string[6:])
        else:
            self.cur_nr = -1

    # Exit a parse tree produced by BarePDBParser#atom_num.
    def exitAtom_num(self, ctx: BarePDBParser.Atom_numContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#atom_name.
    def enterAtom_name(self, ctx: BarePDBParser.Atom_nameContext):
        if ctx.Simple_name():
            self.atomNameSelection.append(str(ctx.Simple_name()))
        else:
            self.atomNameSelection.append(str(ctx.Integer_concat_alt()))

    # Exit a parse tree produced by BarePDBParser#atom_name.
    def exitAtom_name(self, ctx: BarePDBParser.Atom_nameContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#xyz.
    def enterXyz(self, ctx: BarePDBParser.XyzContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#xyz.
    def exitXyz(self, ctx: BarePDBParser.XyzContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#x_yz.
    def enterX_yz(self, ctx: BarePDBParser.X_yzContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#x_yz.
    def exitX_yz(self, ctx: BarePDBParser.X_yzContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#xy_z.
    def enterXy_z(self, ctx: BarePDBParser.Xy_zContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#xy_z.
    def exitXy_z(self, ctx: BarePDBParser.Xy_zContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#x_y_z.
    def enterX_y_z(self, ctx: BarePDBParser.X_y_zContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#x_y_z.
    def exitX_y_z(self, ctx: BarePDBParser.X_y_zContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#undefined.
    def enterUndefined(self, ctx: BarePDBParser.UndefinedContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#undefined.
    def exitUndefined(self, ctx: BarePDBParser.UndefinedContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#number.
    def enterNumber(self, ctx: BarePDBParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#number.
    def exitNumber(self, ctx: BarePDBParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BarePDBParser#terminal.
    def enterTerminal(self, ctx: BarePDBParser.TerminalContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BarePDBParser#terminal.
    def exitTerminal(self, ctx: BarePDBParser.TerminalContext):
        self.atoms.append('TER')
        self.__ter_count += 1

        if ctx.Any_name(0):
            try:
                if int(str(ctx.Any_name(0))) == self.cur_nr + 1:
                    self.__ter_offset -= 1
            except ValueError:
                pass

    # Enter a parse tree produced by BarePDBParser#end.
    def enterEnd(self, ctx: BarePDBParser.EndContext):  # pylint: disable=unused-argument
        self.__end = True

    # Exit a parse tree produced by BarePDBParser#end.
    def exitEnd(self, ctx: BarePDBParser.EndContext):  # pylint: disable=unused-argument
        pass

    def getContentSubtype(self) -> dict:
        """ Return content subtype of Bare PDB file.
        """

        contentSubtype = {'coordinates': self.coordinatesStatements}

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

# del BarePDBParser
