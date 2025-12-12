##
# BarePDBReader.py
#
# Update:
##
""" A collection of classes for parsing Bare PDB files.
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, PredictionMode
from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.BarePDBLexer import BarePDBLexer
    from wwpdb.utils.nmr.mr.BarePDBParser import BarePDBParser
    from wwpdb.utils.nmr.mr.BarePDBParserListener import BarePDBParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                                       MAX_ERROR_REPORT,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID)
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
except ImportError:
    from nmr.mr.LexerErrorListener import LexerErrorListener
    from nmr.mr.ParserErrorListener import ParserErrorListener
    from nmr.mr.BarePDBLexer import BarePDBLexer
    from nmr.mr.BarePDBParser import BarePDBParser
    from nmr.mr.BarePDBParserListener import BarePDBParserListener
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.nef.NEFTranslator import NEFTranslator


class BarePDBReader:
    """ Accessor methods for parsing Bare PDB files.
    """
    __slots__ = ('__class_name__',
                 '__version__',
                 '__verbose',
                 '__lfh',
                 '__debug',
                 '__maxLexerErrorReport',
                 '__maxParserErrorReport',
                 '__representativeModelId',
                 '__representativeAltId',
                 '__mrAtomNameMapping',
                 '__ccU',
                 '__cR',
                 '__caC',
                 '__csStat',
                 '__nefT')

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None, ccU: Optional[ChemCompUtil] = None,
                 csStat: Optional[BMRBChemShiftStat] = None, nefT: Optional[NEFTranslator] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False

        self.__maxLexerErrorReport = MAX_ERROR_REPORT
        self.__maxParserErrorReport = MAX_ERROR_REPORT

        self.__representativeModelId = representativeModelId
        self.__representativeAltId = representativeAltId
        self.__mrAtomNameMapping = mrAtomNameMapping

        # CCD accessing utility
        self.__ccU = ChemCompUtil(verbose, log) if ccU is None else ccU

        if cR is not None and caC is None:
            caC = coordAssemblyChecker(verbose, log, representativeModelId, representativeAltId,
                                       cR, self.__ccU, None, None, fullCheck=False)

        self.__cR = cR
        self.__caC = caC

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(verbose, log, self.__ccU) if csStat is None else csStat

        # NEFTranslator
        self.__nefT = NEFTranslator(verbose, log, self.__ccU, self.__csStat) if nefT is None else nefT
        if nefT is None:
            self.__nefT.set_remediation_mode(True)

    def setDebugMode(self, debug: bool):
        self.__debug = debug

    def setLexerMaxErrorReport(self, maxErrReport: int):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport: int):
        self.__maxParserErrorReport = maxErrReport

    def parse(self, crdFilePath: str, cifFilePath: Optional[str] = None, isFilePath: bool = True
              ) -> Tuple[Optional[BarePDBParserListener], Optional[ParserErrorListener], Optional[LexerErrorListener]]:
        """ Parse Bare PDB file.
            @return: BarePDBParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifh = None

        try:

            if isFilePath:
                crdString = None

                if not os.access(crdFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"+{self.__class_name__}.parse() {crdFilePath} is not accessible.\n")
                    return None, None, None

                ifh = open(crdFilePath, 'r', encoding='utf-8', errors='ignore')  # pylint: disable=consider-using-with
                input = InputStream(ifh.read())

            else:
                crdFilePath, crdString = None, crdFilePath

                if crdString is None or len(crdString) == 0:
                    if self.__verbose:
                        self.__lfh.write(f"+{self.__class_name__}.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(crdString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"+{self.__class_name__}.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        if self.__verbose:
                            self.__lfh.write(f"+{self.__class_name__}.parse() {cifFilePath} is not CIF file.\n")
                        return None, None, None

            lexer = BarePDBLexer(input)
            lexer.removeErrorListeners()

            lexer_error_listener = LexerErrorListener(crdFilePath, maxErrorReport=self.__maxLexerErrorReport)
            lexer.addErrorListener(lexer_error_listener)

            messageList = lexer_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            stream = CommonTokenStream(lexer)
            parser = BarePDBParser(stream)
            # try with simpler/faster SLL prediction mode
            parser._interp.predictionMode = PredictionMode.SLL  # pylint: disable=protected-access
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(crdFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.bare_pdb()

            walker = ParseTreeWalker()
            listener = BarePDBParserListener(self.__verbose, self.__lfh,
                                             self.__representativeModelId,
                                             self.__representativeAltId,
                                             self.__mrAtomNameMapping,
                                             self.__cR, self.__caC,
                                             self.__nefT)
            walker.walk(listener, tree)

            messageList = parser_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")
            elif messageList is None and cifFilePath is None:
                parser_error_listener = ParserErrorListener(crdFilePath, maxErrorReport=self.__maxParserErrorReport)

            if self.__verbose and self.__debug:
                if listener.warningMessage is not None and len(listener.warningMessage) > 0:
                    self.__lfh.write(f"+{self.__class_name__}.parse() ++ Info  -\n" + '\n'.join(listener.warningMessage) + '\n')
                if isFilePath:
                    self.__lfh.write(f"+{self.__class_name__}.parse() ++ Info  - {listener.getContentSubtype()}\n")

            return listener, parser_error_listener, lexer_error_listener

        except IOError as e:
            if self.__verbose:
                self.__lfh.write(f"+{self.__class_name__}.parse() ++ Error  - {str(e)}\n")
            return None, None, None
        finally:
            if isFilePath and ifh is not None:
                ifh.close()


if __name__ == "__main__":
    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2ly2/2ly2_model-upload_P1.pdb.V1',
                 '../../tests-nmr/mock-data-remediation/2ly2/2ly2.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2l8m/bmr17415/work/upload/rep-f.pdb',
                 '../../tests-nmr/mock-data-remediation/2l8m/2l8m.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2moa/bmr19932/work/data/all.pdb',
                 '../../tests-nmr/mock-data-remediation/2moa/2moa.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2l9h/bmr17453/work/data/x_19_13_3_xplor.pdb',
                 '../../tests-nmr/mock-data-remediation/2l9h/2l9h.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mmc/bmr19852/work/data/RANXP_Deposition5_chain.pdb',
                 '../../tests-nmr/mock-data-remediation/2mmc/2mmc.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lwg/bmr18625/work/data/freeGGCC_reference for restraints.pdb',
                 '../../tests-nmr/mock-data-remediation/2lwg/2lwg.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2miv/bmr19695/work/data/rep1.pdb',
                 '../../tests-nmr/mock-data-remediation/2miv/2miv.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2rsq/bmr11502/work/data/prm_1D.pdb',
                 '../../tests-nmr/mock-data-remediation/2rsq/2rsq.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2mal/bmr19365/work/data/lc-ltp2-deposit.pdb',
                 '../../tests-nmr/mock-data-remediation/2mal/2mal.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lqd/bmr17415/work/data/rep-f.pdb',
                 '../../tests-nmr/mock-data-remediation/2lqd/2lqd.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5tbn/bmr30177/work/data/D_1000223981_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-remediation/5tbn/5tbn.cif')

    reader = BarePDBReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5vzm/bmr30300/work/data/D_1000228147_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-remediation/5vzm/5vzm.cif')
