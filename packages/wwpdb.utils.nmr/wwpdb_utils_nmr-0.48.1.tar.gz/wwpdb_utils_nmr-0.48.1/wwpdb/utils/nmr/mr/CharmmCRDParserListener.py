##
# File: CharmmCRDParserListener.py
# Date: 14-Nov-2024
#
# Updates:
""" ParserLister class for CHARMM CRD files.
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
    from wwpdb.utils.nmr.mr.CharmmCRDParser import CharmmCRDParser
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
    from nmr.mr.CharmmCRDParser import CharmmCRDParser
    from nmr.mr.BaseTopologyParserListener import BaseTopologyParserListener
    from nmr.mr.ParserListenerUtil import (REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode,
                               letterToDigit,
                               indexToLetter,
                               retrieveAtomIdentFromMRMap)


# This class defines a complete listener for a parse tree produced by CharmmCRDParser.
class CharmmCRDParserListener(ParseTreeListener, BaseTopologyParserListener):
    __slots__ = ('coordinatesStatements', )

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

        self.file_type = 'nm-aux-cha'

        self.coordinatesStatements = 0

    # Enter a parse tree produced by CharmmCRDParser#charmm_crd.
    def enterCharmm_crd(self, ctx: CharmmCRDParser.Charmm_crdContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmCRDParser#charmm_crd.
    def exitCharmm_crd(self, ctx: CharmmCRDParser.Charmm_crdContext):  # pylint: disable=unused-argument

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
        prevAsymId = prevSeqId = prevCompId = None
        offset = 0
        for atom in self.atoms:
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

            if (0 < atomNum < len(terminus) + 1
                and ((terminus[atomNum - 1] and ancAtomName.endswith('T'))
                     or (terminus[atomNum - 2] and prevAtomName.endswith('T')
                         and self.csStat.getTypeOfCompId(prevCompId) != self.csStat.getTypeOfCompId(compId))))\
               or self.isSegmentWithAsymHint(prevAsymId, prevCompId, prevAtomName, asymId, compId, atomName)\
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
                                            'auth_atom_id': atomName}
            ancAtomName = prevAtomName
            prevAtomName = atomName
            prevAsymId = asymId
            prevSeqId = _seqId
            prevCompId = compId

        self.polySeqPrmTop.append({'chain_id': chainId,
                                   'seq_id': seqIdList,
                                   'auth_comp_id': compIdList})

        self.exit(retrievedAtomNumList)

    # Enter a parse tree produced by CharmmCRDParser#comment.
    def enterComment(self, ctx: CharmmCRDParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmCRDParser#comment.
    def exitComment(self, ctx: CharmmCRDParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CharmmCRDParser#coordinates.
    def enterCoordinates(self, ctx: CharmmCRDParser.CoordinatesContext):  # pylint: disable=unused-argument
        self.coordinatesStatements += 1

    # Exit a parse tree produced by CharmmCRDParser#coordinates.
    def exitCoordinates(self, ctx: CharmmCRDParser.CoordinatesContext):
        if ctx.Integer():
            return
        self.coordinatesStatements -= -1

    # Enter a parse tree produced by CharmmCRDParser#atom_coordinate.
    def enterAtom_coordinate(self, ctx: CharmmCRDParser.Atom_coordinateContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CharmmCRDParser#atom_coordinate.
    def exitAtom_coordinate(self, ctx: CharmmCRDParser.Atom_coordinateContext):

        try:

            nr = int(str(ctx.Integer(0)))

            if nr < 0 or nr <= self.prev_nr:
                return

            self.prev_nr = nr

            seqId = int(str(ctx.Integer(1)))

            compId = str(ctx.Simple_name(0))
            atomId = str(ctx.Simple_name(1))
            chainId = str(ctx.Simple_name(2))
            authSeqId = int(str(ctx.Integer(2)))

            atom = {'atom_number': nr,
                    'seq_id': seqId,
                    'auth_chain_id': chainId,
                    'auth_seq_id': authSeqId,
                    'auth_comp_id': compId,
                    'auth_atom_id': atomId}

            if atom not in self.atoms:
                self.atoms.append(atom)

        except ValueError:
            pass

    def getContentSubtype(self) -> dict:
        """ Return content subtype of CHARMM CRD file.
        """

        contentSubtype = {'coordinates': self.coordinatesStatements}

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

# del CharmmCRDParser
