# Generated from XeasyPKParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,44,311,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,1,0,3,0,40,8,0,
        1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,54,8,0,10,0,
        12,0,57,9,0,1,0,1,0,3,0,61,8,0,1,0,1,0,1,1,1,1,1,1,1,1,1,2,1,2,1,
        2,1,2,1,3,1,3,4,3,75,8,3,11,3,12,3,76,1,3,1,3,1,4,1,4,1,4,1,4,1,
        4,1,5,1,5,1,5,1,5,1,6,1,6,4,6,92,8,6,11,6,12,6,93,1,6,1,6,1,7,1,
        7,4,7,100,8,7,11,7,12,7,101,1,7,1,7,1,8,1,8,5,8,108,8,8,10,8,12,
        8,111,9,8,4,8,113,8,8,11,8,12,8,114,1,9,1,9,1,9,1,9,1,9,3,9,122,
        8,9,1,9,1,9,1,9,3,9,127,8,9,1,9,1,9,1,9,1,9,1,9,3,9,134,8,9,1,9,
        3,9,137,8,9,1,9,1,9,1,9,3,9,142,8,9,3,9,144,8,9,1,9,1,9,1,9,3,9,
        149,8,9,1,9,3,9,152,8,9,1,9,1,9,1,9,3,9,157,8,9,5,9,159,8,9,10,9,
        12,9,162,9,9,1,10,1,10,5,10,166,8,10,10,10,12,10,169,9,10,4,10,171,
        8,10,11,10,12,10,172,1,11,1,11,1,11,1,11,1,11,1,11,3,11,181,8,11,
        1,11,1,11,1,11,3,11,186,8,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,
        194,8,11,1,11,3,11,197,8,11,1,11,1,11,1,11,3,11,202,8,11,3,11,204,
        8,11,1,11,1,11,1,11,1,11,3,11,210,8,11,1,11,3,11,213,8,11,1,11,1,
        11,1,11,3,11,218,8,11,5,11,220,8,11,10,11,12,11,223,9,11,1,12,1,
        12,5,12,227,8,12,10,12,12,12,230,9,12,4,12,232,8,12,11,12,12,12,
        233,1,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,243,8,13,1,13,1,13,1,
        13,3,13,248,8,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,257,8,13,
        1,13,3,13,260,8,13,1,13,1,13,1,13,3,13,265,8,13,3,13,267,8,13,1,
        13,1,13,1,13,1,13,1,13,3,13,274,8,13,1,13,3,13,277,8,13,1,13,1,13,
        1,13,3,13,282,8,13,5,13,284,8,13,10,13,12,13,287,9,13,1,14,1,14,
        1,15,1,15,1,16,1,16,1,17,1,17,1,17,3,17,298,8,17,3,17,300,8,17,1,
        18,1,18,5,18,304,8,18,10,18,12,18,307,9,18,1,18,1,18,1,18,0,0,19,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,0,5,1,1,17,17,
        1,0,9,10,2,0,9,11,15,15,2,0,9,9,15,15,1,1,44,44,354,0,39,1,0,0,0,
        2,64,1,0,0,0,4,68,1,0,0,0,6,72,1,0,0,0,8,80,1,0,0,0,10,85,1,0,0,
        0,12,89,1,0,0,0,14,97,1,0,0,0,16,112,1,0,0,0,18,116,1,0,0,0,20,170,
        1,0,0,0,22,174,1,0,0,0,24,231,1,0,0,0,26,235,1,0,0,0,28,288,1,0,
        0,0,30,290,1,0,0,0,32,292,1,0,0,0,34,299,1,0,0,0,36,301,1,0,0,0,
        38,40,5,17,0,0,39,38,1,0,0,0,39,40,1,0,0,0,40,55,1,0,0,0,41,54,3,
        2,1,0,42,54,3,4,2,0,43,54,3,6,3,0,44,54,3,8,4,0,45,54,3,10,5,0,46,
        54,3,12,6,0,47,54,3,14,7,0,48,54,3,36,18,0,49,54,3,16,8,0,50,54,
        3,20,10,0,51,54,3,24,12,0,52,54,5,17,0,0,53,41,1,0,0,0,53,42,1,0,
        0,0,53,43,1,0,0,0,53,44,1,0,0,0,53,45,1,0,0,0,53,46,1,0,0,0,53,47,
        1,0,0,0,53,48,1,0,0,0,53,49,1,0,0,0,53,50,1,0,0,0,53,51,1,0,0,0,
        53,52,1,0,0,0,54,57,1,0,0,0,55,53,1,0,0,0,55,56,1,0,0,0,56,60,1,
        0,0,0,57,55,1,0,0,0,58,61,5,17,0,0,59,61,3,36,18,0,60,58,1,0,0,0,
        60,59,1,0,0,0,60,61,1,0,0,0,61,62,1,0,0,0,62,63,5,0,0,1,63,1,1,0,
        0,0,64,65,5,1,0,0,65,66,5,20,0,0,66,67,5,22,0,0,67,3,1,0,0,0,68,
        69,5,2,0,0,69,70,5,23,0,0,70,71,5,25,0,0,71,5,1,0,0,0,72,74,5,3,
        0,0,73,75,5,26,0,0,74,73,1,0,0,0,75,76,1,0,0,0,76,74,1,0,0,0,76,
        77,1,0,0,0,77,78,1,0,0,0,78,79,5,28,0,0,79,7,1,0,0,0,80,81,5,5,0,
        0,81,82,5,29,0,0,82,83,5,30,0,0,83,84,5,32,0,0,84,9,1,0,0,0,85,86,
        5,6,0,0,86,87,5,33,0,0,87,88,5,35,0,0,88,11,1,0,0,0,89,91,5,7,0,
        0,90,92,5,36,0,0,91,90,1,0,0,0,92,93,1,0,0,0,93,91,1,0,0,0,93,94,
        1,0,0,0,94,95,1,0,0,0,95,96,5,38,0,0,96,13,1,0,0,0,97,99,5,8,0,0,
        98,100,5,39,0,0,99,98,1,0,0,0,100,101,1,0,0,0,101,99,1,0,0,0,101,
        102,1,0,0,0,102,103,1,0,0,0,103,104,5,41,0,0,104,15,1,0,0,0,105,
        109,3,18,9,0,106,108,3,36,18,0,107,106,1,0,0,0,108,111,1,0,0,0,109,
        107,1,0,0,0,109,110,1,0,0,0,110,113,1,0,0,0,111,109,1,0,0,0,112,
        105,1,0,0,0,113,114,1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,115,
        17,1,0,0,0,116,117,5,9,0,0,117,118,3,28,14,0,118,119,3,28,14,0,119,
        121,5,9,0,0,120,122,5,15,0,0,121,120,1,0,0,0,121,122,1,0,0,0,122,
        123,1,0,0,0,123,124,3,30,15,0,124,126,3,30,15,0,125,127,5,15,0,0,
        126,125,1,0,0,0,126,127,1,0,0,0,127,128,1,0,0,0,128,143,3,32,16,
        0,129,144,7,0,0,0,130,131,3,34,17,0,131,133,3,34,17,0,132,134,5,
        9,0,0,133,132,1,0,0,0,133,134,1,0,0,0,134,136,1,0,0,0,135,137,5,
        9,0,0,136,135,1,0,0,0,136,137,1,0,0,0,137,141,1,0,0,0,138,142,5,
        17,0,0,139,142,3,36,18,0,140,142,5,0,0,1,141,138,1,0,0,0,141,139,
        1,0,0,0,141,140,1,0,0,0,142,144,1,0,0,0,143,129,1,0,0,0,143,130,
        1,0,0,0,144,160,1,0,0,0,145,146,3,34,17,0,146,148,3,34,17,0,147,
        149,5,9,0,0,148,147,1,0,0,0,148,149,1,0,0,0,149,151,1,0,0,0,150,
        152,5,9,0,0,151,150,1,0,0,0,151,152,1,0,0,0,152,156,1,0,0,0,153,
        157,5,17,0,0,154,157,3,36,18,0,155,157,5,0,0,1,156,153,1,0,0,0,156,
        154,1,0,0,0,156,155,1,0,0,0,157,159,1,0,0,0,158,145,1,0,0,0,159,
        162,1,0,0,0,160,158,1,0,0,0,160,161,1,0,0,0,161,19,1,0,0,0,162,160,
        1,0,0,0,163,167,3,22,11,0,164,166,3,36,18,0,165,164,1,0,0,0,166,
        169,1,0,0,0,167,165,1,0,0,0,167,168,1,0,0,0,168,171,1,0,0,0,169,
        167,1,0,0,0,170,163,1,0,0,0,171,172,1,0,0,0,172,170,1,0,0,0,172,
        173,1,0,0,0,173,21,1,0,0,0,174,175,5,9,0,0,175,176,3,28,14,0,176,
        177,3,28,14,0,177,178,3,28,14,0,178,180,5,9,0,0,179,181,5,15,0,0,
        180,179,1,0,0,0,180,181,1,0,0,0,181,182,1,0,0,0,182,183,3,30,15,
        0,183,185,3,30,15,0,184,186,5,15,0,0,185,184,1,0,0,0,185,186,1,0,
        0,0,186,187,1,0,0,0,187,203,3,32,16,0,188,204,7,0,0,0,189,190,3,
        34,17,0,190,191,3,34,17,0,191,193,3,34,17,0,192,194,5,9,0,0,193,
        192,1,0,0,0,193,194,1,0,0,0,194,196,1,0,0,0,195,197,5,9,0,0,196,
        195,1,0,0,0,196,197,1,0,0,0,197,201,1,0,0,0,198,202,5,17,0,0,199,
        202,3,36,18,0,200,202,5,0,0,1,201,198,1,0,0,0,201,199,1,0,0,0,201,
        200,1,0,0,0,202,204,1,0,0,0,203,188,1,0,0,0,203,189,1,0,0,0,204,
        221,1,0,0,0,205,206,3,34,17,0,206,207,3,34,17,0,207,209,3,34,17,
        0,208,210,5,9,0,0,209,208,1,0,0,0,209,210,1,0,0,0,210,212,1,0,0,
        0,211,213,5,9,0,0,212,211,1,0,0,0,212,213,1,0,0,0,213,217,1,0,0,
        0,214,218,5,17,0,0,215,218,3,36,18,0,216,218,5,0,0,1,217,214,1,0,
        0,0,217,215,1,0,0,0,217,216,1,0,0,0,218,220,1,0,0,0,219,205,1,0,
        0,0,220,223,1,0,0,0,221,219,1,0,0,0,221,222,1,0,0,0,222,23,1,0,0,
        0,223,221,1,0,0,0,224,228,3,26,13,0,225,227,3,36,18,0,226,225,1,
        0,0,0,227,230,1,0,0,0,228,226,1,0,0,0,228,229,1,0,0,0,229,232,1,
        0,0,0,230,228,1,0,0,0,231,224,1,0,0,0,232,233,1,0,0,0,233,231,1,
        0,0,0,233,234,1,0,0,0,234,25,1,0,0,0,235,236,5,9,0,0,236,237,3,28,
        14,0,237,238,3,28,14,0,238,239,3,28,14,0,239,240,3,28,14,0,240,242,
        5,9,0,0,241,243,5,15,0,0,242,241,1,0,0,0,242,243,1,0,0,0,243,244,
        1,0,0,0,244,245,3,30,15,0,245,247,3,30,15,0,246,248,5,15,0,0,247,
        246,1,0,0,0,247,248,1,0,0,0,248,249,1,0,0,0,249,266,3,32,16,0,250,
        267,7,0,0,0,251,252,3,34,17,0,252,253,3,34,17,0,253,254,3,34,17,
        0,254,256,3,34,17,0,255,257,5,9,0,0,256,255,1,0,0,0,256,257,1,0,
        0,0,257,259,1,0,0,0,258,260,5,9,0,0,259,258,1,0,0,0,259,260,1,0,
        0,0,260,264,1,0,0,0,261,265,5,17,0,0,262,265,3,36,18,0,263,265,5,
        0,0,1,264,261,1,0,0,0,264,262,1,0,0,0,264,263,1,0,0,0,265,267,1,
        0,0,0,266,250,1,0,0,0,266,251,1,0,0,0,267,285,1,0,0,0,268,269,3,
        34,17,0,269,270,3,34,17,0,270,271,3,34,17,0,271,273,3,34,17,0,272,
        274,5,9,0,0,273,272,1,0,0,0,273,274,1,0,0,0,274,276,1,0,0,0,275,
        277,5,9,0,0,276,275,1,0,0,0,276,277,1,0,0,0,277,281,1,0,0,0,278,
        282,5,17,0,0,279,282,3,36,18,0,280,282,5,0,0,1,281,278,1,0,0,0,281,
        279,1,0,0,0,281,280,1,0,0,0,282,284,1,0,0,0,283,268,1,0,0,0,284,
        287,1,0,0,0,285,283,1,0,0,0,285,286,1,0,0,0,286,27,1,0,0,0,287,285,
        1,0,0,0,288,289,7,1,0,0,289,29,1,0,0,0,290,291,7,2,0,0,291,31,1,
        0,0,0,292,293,7,3,0,0,293,33,1,0,0,0,294,300,5,9,0,0,295,297,5,15,
        0,0,296,298,5,9,0,0,297,296,1,0,0,0,297,298,1,0,0,0,298,300,1,0,
        0,0,299,294,1,0,0,0,299,295,1,0,0,0,300,35,1,0,0,0,301,305,5,12,
        0,0,302,304,5,42,0,0,303,302,1,0,0,0,304,307,1,0,0,0,305,303,1,0,
        0,0,305,306,1,0,0,0,306,308,1,0,0,0,307,305,1,0,0,0,308,309,7,4,
        0,0,309,37,1,0,0,0,46,39,53,55,60,76,93,101,109,114,121,126,133,
        136,141,143,148,151,156,160,167,172,180,185,193,196,201,203,209,
        212,217,221,228,233,242,247,256,259,264,266,273,276,281,285,297,
        299,305
    ]

class XeasyPKParser ( Parser ):

    grammarFileName = "XeasyPKParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'#FORMAT'", 
                     "<INVALID>", "'#INAME'", "'#CYANAFORMAT'", "'#SPECTRUM'", 
                     "'#TOLERANCE'" ]

    symbolicNames = [ "<INVALID>", "Num_of_dim", "Num_of_peaks", "Format", 
                      "XEASY_WO_FORMAT", "Iname", "Cyana_format", "Spectrum", 
                      "Tolerance", "Integer", "Float", "Real", "COMMENT", 
                      "EXCLM_COMMENT", "SMCLN_COMMENT", "Simple_name", "SPACE", 
                      "RETURN", "SECTION_COMMENT", "LINE_COMMENT", "Integer_ND", 
                      "SPACE_ND", "RETURN_ND", "Integer_NP", "SPACE_NP", 
                      "RETURN_NP", "Simple_name_FO", "SPACE_FO", "RETURN_FO", 
                      "Integer_IN", "Simple_name_IN", "SPACE_IN", "RETURN_IN", 
                      "Simple_name_CY", "SPACE_CY", "RETURN_CY", "Simple_name_SP", 
                      "SPACE_SP", "RETURN_SP", "Float_TO", "TOACE_TO", "RETURN_TO", 
                      "Any_name", "SPACE_CM", "RETURN_CM" ]

    RULE_xeasy_pk = 0
    RULE_dimension = 1
    RULE_peak = 2
    RULE_format = 3
    RULE_iname = 4
    RULE_cyana_format = 5
    RULE_spectrum = 6
    RULE_tolerance = 7
    RULE_peak_list_2d = 8
    RULE_peak_2d = 9
    RULE_peak_list_3d = 10
    RULE_peak_3d = 11
    RULE_peak_list_4d = 12
    RULE_peak_4d = 13
    RULE_position = 14
    RULE_number = 15
    RULE_type_code = 16
    RULE_assign = 17
    RULE_comment = 18

    ruleNames =  [ "xeasy_pk", "dimension", "peak", "format", "iname", "cyana_format", 
                   "spectrum", "tolerance", "peak_list_2d", "peak_2d", "peak_list_3d", 
                   "peak_3d", "peak_list_4d", "peak_4d", "position", "number", 
                   "type_code", "assign", "comment" ]

    EOF = Token.EOF
    Num_of_dim=1
    Num_of_peaks=2
    Format=3
    XEASY_WO_FORMAT=4
    Iname=5
    Cyana_format=6
    Spectrum=7
    Tolerance=8
    Integer=9
    Float=10
    Real=11
    COMMENT=12
    EXCLM_COMMENT=13
    SMCLN_COMMENT=14
    Simple_name=15
    SPACE=16
    RETURN=17
    SECTION_COMMENT=18
    LINE_COMMENT=19
    Integer_ND=20
    SPACE_ND=21
    RETURN_ND=22
    Integer_NP=23
    SPACE_NP=24
    RETURN_NP=25
    Simple_name_FO=26
    SPACE_FO=27
    RETURN_FO=28
    Integer_IN=29
    Simple_name_IN=30
    SPACE_IN=31
    RETURN_IN=32
    Simple_name_CY=33
    SPACE_CY=34
    RETURN_CY=35
    Simple_name_SP=36
    SPACE_SP=37
    RETURN_SP=38
    Float_TO=39
    TOACE_TO=40
    RETURN_TO=41
    Any_name=42
    SPACE_CM=43
    RETURN_CM=44

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Xeasy_pkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(XeasyPKParser.EOF, 0)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.RETURN)
            else:
                return self.getToken(XeasyPKParser.RETURN, i)

        def dimension(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.DimensionContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.DimensionContext,i)


        def peak(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.PeakContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.PeakContext,i)


        def format_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.FormatContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.FormatContext,i)


        def iname(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.InameContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.InameContext,i)


        def cyana_format(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Cyana_formatContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Cyana_formatContext,i)


        def spectrum(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.SpectrumContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.SpectrumContext,i)


        def tolerance(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.ToleranceContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.ToleranceContext,i)


        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def peak_list_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_list_2dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_list_2dContext,i)


        def peak_list_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_list_3dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_list_3dContext,i)


        def peak_list_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_list_4dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_list_4dContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_xeasy_pk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXeasy_pk" ):
                listener.enterXeasy_pk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXeasy_pk" ):
                listener.exitXeasy_pk(self)




    def xeasy_pk(self):

        localctx = XeasyPKParser.Xeasy_pkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_xeasy_pk)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 38
                self.match(XeasyPKParser.RETURN)


            self.state = 55
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 53
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        self.state = 41
                        self.dimension()
                        pass

                    elif la_ == 2:
                        self.state = 42
                        self.peak()
                        pass

                    elif la_ == 3:
                        self.state = 43
                        self.format_()
                        pass

                    elif la_ == 4:
                        self.state = 44
                        self.iname()
                        pass

                    elif la_ == 5:
                        self.state = 45
                        self.cyana_format()
                        pass

                    elif la_ == 6:
                        self.state = 46
                        self.spectrum()
                        pass

                    elif la_ == 7:
                        self.state = 47
                        self.tolerance()
                        pass

                    elif la_ == 8:
                        self.state = 48
                        self.comment()
                        pass

                    elif la_ == 9:
                        self.state = 49
                        self.peak_list_2d()
                        pass

                    elif la_ == 10:
                        self.state = 50
                        self.peak_list_3d()
                        pass

                    elif la_ == 11:
                        self.state = 51
                        self.peak_list_4d()
                        pass

                    elif la_ == 12:
                        self.state = 52
                        self.match(XeasyPKParser.RETURN)
                        pass

             
                self.state = 57
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 60
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.state = 58
                self.match(XeasyPKParser.RETURN)
                pass
            elif token in [12]:
                self.state = 59
                self.comment()
                pass
            elif token in [-1]:
                pass
            else:
                pass
            self.state = 62
            self.match(XeasyPKParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DimensionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Num_of_dim(self):
            return self.getToken(XeasyPKParser.Num_of_dim, 0)

        def Integer_ND(self):
            return self.getToken(XeasyPKParser.Integer_ND, 0)

        def RETURN_ND(self):
            return self.getToken(XeasyPKParser.RETURN_ND, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_dimension

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDimension" ):
                listener.enterDimension(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDimension" ):
                listener.exitDimension(self)




    def dimension(self):

        localctx = XeasyPKParser.DimensionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_dimension)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(XeasyPKParser.Num_of_dim)
            self.state = 65
            self.match(XeasyPKParser.Integer_ND)
            self.state = 66
            self.match(XeasyPKParser.RETURN_ND)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PeakContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Num_of_peaks(self):
            return self.getToken(XeasyPKParser.Num_of_peaks, 0)

        def Integer_NP(self):
            return self.getToken(XeasyPKParser.Integer_NP, 0)

        def RETURN_NP(self):
            return self.getToken(XeasyPKParser.RETURN_NP, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak" ):
                listener.enterPeak(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak" ):
                listener.exitPeak(self)




    def peak(self):

        localctx = XeasyPKParser.PeakContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_peak)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(XeasyPKParser.Num_of_peaks)
            self.state = 69
            self.match(XeasyPKParser.Integer_NP)
            self.state = 70
            self.match(XeasyPKParser.RETURN_NP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Format(self):
            return self.getToken(XeasyPKParser.Format, 0)

        def RETURN_FO(self):
            return self.getToken(XeasyPKParser.RETURN_FO, 0)

        def Simple_name_FO(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Simple_name_FO)
            else:
                return self.getToken(XeasyPKParser.Simple_name_FO, i)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_format

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormat" ):
                listener.enterFormat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormat" ):
                listener.exitFormat(self)




    def format_(self):

        localctx = XeasyPKParser.FormatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_format)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(XeasyPKParser.Format)
            self.state = 74 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 73
                self.match(XeasyPKParser.Simple_name_FO)
                self.state = 76 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==26):
                    break

            self.state = 78
            self.match(XeasyPKParser.RETURN_FO)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Iname(self):
            return self.getToken(XeasyPKParser.Iname, 0)

        def Integer_IN(self):
            return self.getToken(XeasyPKParser.Integer_IN, 0)

        def Simple_name_IN(self):
            return self.getToken(XeasyPKParser.Simple_name_IN, 0)

        def RETURN_IN(self):
            return self.getToken(XeasyPKParser.RETURN_IN, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_iname

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIname" ):
                listener.enterIname(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIname" ):
                listener.exitIname(self)




    def iname(self):

        localctx = XeasyPKParser.InameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_iname)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(XeasyPKParser.Iname)
            self.state = 81
            self.match(XeasyPKParser.Integer_IN)
            self.state = 82
            self.match(XeasyPKParser.Simple_name_IN)
            self.state = 83
            self.match(XeasyPKParser.RETURN_IN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Cyana_formatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Cyana_format(self):
            return self.getToken(XeasyPKParser.Cyana_format, 0)

        def Simple_name_CY(self):
            return self.getToken(XeasyPKParser.Simple_name_CY, 0)

        def RETURN_CY(self):
            return self.getToken(XeasyPKParser.RETURN_CY, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_cyana_format

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCyana_format" ):
                listener.enterCyana_format(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCyana_format" ):
                listener.exitCyana_format(self)




    def cyana_format(self):

        localctx = XeasyPKParser.Cyana_formatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_cyana_format)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(XeasyPKParser.Cyana_format)
            self.state = 86
            self.match(XeasyPKParser.Simple_name_CY)
            self.state = 87
            self.match(XeasyPKParser.RETURN_CY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpectrumContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Spectrum(self):
            return self.getToken(XeasyPKParser.Spectrum, 0)

        def RETURN_SP(self):
            return self.getToken(XeasyPKParser.RETURN_SP, 0)

        def Simple_name_SP(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Simple_name_SP)
            else:
                return self.getToken(XeasyPKParser.Simple_name_SP, i)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_spectrum

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpectrum" ):
                listener.enterSpectrum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpectrum" ):
                listener.exitSpectrum(self)




    def spectrum(self):

        localctx = XeasyPKParser.SpectrumContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_spectrum)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(XeasyPKParser.Spectrum)
            self.state = 91 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 90
                self.match(XeasyPKParser.Simple_name_SP)
                self.state = 93 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==36):
                    break

            self.state = 95
            self.match(XeasyPKParser.RETURN_SP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ToleranceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Tolerance(self):
            return self.getToken(XeasyPKParser.Tolerance, 0)

        def RETURN_TO(self):
            return self.getToken(XeasyPKParser.RETURN_TO, 0)

        def Float_TO(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Float_TO)
            else:
                return self.getToken(XeasyPKParser.Float_TO, i)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_tolerance

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTolerance" ):
                listener.enterTolerance(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTolerance" ):
                listener.exitTolerance(self)




    def tolerance(self):

        localctx = XeasyPKParser.ToleranceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_tolerance)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(XeasyPKParser.Tolerance)
            self.state = 99 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 98
                self.match(XeasyPKParser.Float_TO)
                self.state = 101 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==39):
                    break

            self.state = 103
            self.match(XeasyPKParser.RETURN_TO)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def peak_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_2dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_2dContext,i)


        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_list_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_2d" ):
                listener.enterPeak_list_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_2d" ):
                listener.exitPeak_list_2d(self)




    def peak_list_2d(self):

        localctx = XeasyPKParser.Peak_list_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_peak_list_2d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 105
                    self.peak_2d()
                    self.state = 109
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
                    while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                        if _alt==1:
                            self.state = 106
                            self.comment() 
                        self.state = 111
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,7,self._ctx)


                else:
                    raise NoViableAltException(self)
                self.state = 114 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Integer)
            else:
                return self.getToken(XeasyPKParser.Integer, i)

        def position(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.PositionContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.PositionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.NumberContext,i)


        def type_code(self):
            return self.getTypedRuleContext(XeasyPKParser.Type_codeContext,0)


        def assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.AssignContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.AssignContext,i)


        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Simple_name)
            else:
                return self.getToken(XeasyPKParser.Simple_name, i)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.RETURN)
            else:
                return self.getToken(XeasyPKParser.RETURN, i)

        def EOF(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.EOF)
            else:
                return self.getToken(XeasyPKParser.EOF, i)

        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_2d" ):
                listener.enterPeak_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_2d" ):
                listener.exitPeak_2d(self)




    def peak_2d(self):

        localctx = XeasyPKParser.Peak_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_peak_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(XeasyPKParser.Integer)
            self.state = 117
            self.position()
            self.state = 118
            self.position()
            self.state = 119
            self.match(XeasyPKParser.Integer)
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 120
                self.match(XeasyPKParser.Simple_name)


            self.state = 123
            self.number()
            self.state = 124
            self.number()
            self.state = 126
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 125
                self.match(XeasyPKParser.Simple_name)


            self.state = 128
            self.type_code()
            self.state = 143
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [-1, 17]:
                self.state = 129
                _la = self._input.LA(1)
                if not(_la==-1 or _la==17):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [9, 15]:
                self.state = 130
                self.assign()
                self.state = 131
                self.assign()
                self.state = 133
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                if la_ == 1:
                    self.state = 132
                    self.match(XeasyPKParser.Integer)


                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==9:
                    self.state = 135
                    self.match(XeasyPKParser.Integer)


                self.state = 141
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [17]:
                    self.state = 138
                    self.match(XeasyPKParser.RETURN)
                    pass
                elif token in [12]:
                    self.state = 139
                    self.comment()
                    pass
                elif token in [-1]:
                    self.state = 140
                    self.match(XeasyPKParser.EOF)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            else:
                raise NoViableAltException(self)

            self.state = 160
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 145
                    self.assign()
                    self.state = 146
                    self.assign()
                    self.state = 148
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
                    if la_ == 1:
                        self.state = 147
                        self.match(XeasyPKParser.Integer)


                    self.state = 151
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==9:
                        self.state = 150
                        self.match(XeasyPKParser.Integer)


                    self.state = 156
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [17]:
                        self.state = 153
                        self.match(XeasyPKParser.RETURN)
                        pass
                    elif token in [12]:
                        self.state = 154
                        self.comment()
                        pass
                    elif token in [-1]:
                        self.state = 155
                        self.match(XeasyPKParser.EOF)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 162
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def peak_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_3dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_3dContext,i)


        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_list_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_3d" ):
                listener.enterPeak_list_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_3d" ):
                listener.exitPeak_list_3d(self)




    def peak_list_3d(self):

        localctx = XeasyPKParser.Peak_list_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_peak_list_3d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 163
                    self.peak_3d()
                    self.state = 167
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
                    while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                        if _alt==1:
                            self.state = 164
                            self.comment() 
                        self.state = 169
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,19,self._ctx)


                else:
                    raise NoViableAltException(self)
                self.state = 172 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Integer)
            else:
                return self.getToken(XeasyPKParser.Integer, i)

        def position(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.PositionContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.PositionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.NumberContext,i)


        def type_code(self):
            return self.getTypedRuleContext(XeasyPKParser.Type_codeContext,0)


        def assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.AssignContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.AssignContext,i)


        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Simple_name)
            else:
                return self.getToken(XeasyPKParser.Simple_name, i)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.RETURN)
            else:
                return self.getToken(XeasyPKParser.RETURN, i)

        def EOF(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.EOF)
            else:
                return self.getToken(XeasyPKParser.EOF, i)

        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_3d" ):
                listener.enterPeak_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_3d" ):
                listener.exitPeak_3d(self)




    def peak_3d(self):

        localctx = XeasyPKParser.Peak_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_peak_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.match(XeasyPKParser.Integer)
            self.state = 175
            self.position()
            self.state = 176
            self.position()
            self.state = 177
            self.position()
            self.state = 178
            self.match(XeasyPKParser.Integer)
            self.state = 180
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 179
                self.match(XeasyPKParser.Simple_name)


            self.state = 182
            self.number()
            self.state = 183
            self.number()
            self.state = 185
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.state = 184
                self.match(XeasyPKParser.Simple_name)


            self.state = 187
            self.type_code()
            self.state = 203
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [-1, 17]:
                self.state = 188
                _la = self._input.LA(1)
                if not(_la==-1 or _la==17):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [9, 15]:
                self.state = 189
                self.assign()
                self.state = 190
                self.assign()
                self.state = 191
                self.assign()
                self.state = 193
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
                if la_ == 1:
                    self.state = 192
                    self.match(XeasyPKParser.Integer)


                self.state = 196
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==9:
                    self.state = 195
                    self.match(XeasyPKParser.Integer)


                self.state = 201
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [17]:
                    self.state = 198
                    self.match(XeasyPKParser.RETURN)
                    pass
                elif token in [12]:
                    self.state = 199
                    self.comment()
                    pass
                elif token in [-1]:
                    self.state = 200
                    self.match(XeasyPKParser.EOF)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            else:
                raise NoViableAltException(self)

            self.state = 221
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,30,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 205
                    self.assign()
                    self.state = 206
                    self.assign()
                    self.state = 207
                    self.assign()
                    self.state = 209
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
                    if la_ == 1:
                        self.state = 208
                        self.match(XeasyPKParser.Integer)


                    self.state = 212
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==9:
                        self.state = 211
                        self.match(XeasyPKParser.Integer)


                    self.state = 217
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [17]:
                        self.state = 214
                        self.match(XeasyPKParser.RETURN)
                        pass
                    elif token in [12]:
                        self.state = 215
                        self.comment()
                        pass
                    elif token in [-1]:
                        self.state = 216
                        self.match(XeasyPKParser.EOF)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 223
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,30,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_list_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def peak_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.Peak_4dContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.Peak_4dContext,i)


        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_list_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_4d" ):
                listener.enterPeak_list_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_4d" ):
                listener.exitPeak_list_4d(self)




    def peak_list_4d(self):

        localctx = XeasyPKParser.Peak_list_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_peak_list_4d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 224
                    self.peak_4d()
                    self.state = 228
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
                    while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                        if _alt==1:
                            self.state = 225
                            self.comment() 
                        self.state = 230
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,31,self._ctx)


                else:
                    raise NoViableAltException(self)
                self.state = 233 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,32,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Peak_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Integer)
            else:
                return self.getToken(XeasyPKParser.Integer, i)

        def position(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.PositionContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.PositionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.NumberContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.NumberContext,i)


        def type_code(self):
            return self.getTypedRuleContext(XeasyPKParser.Type_codeContext,0)


        def assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.AssignContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.AssignContext,i)


        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Simple_name)
            else:
                return self.getToken(XeasyPKParser.Simple_name, i)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.RETURN)
            else:
                return self.getToken(XeasyPKParser.RETURN, i)

        def EOF(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.EOF)
            else:
                return self.getToken(XeasyPKParser.EOF, i)

        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(XeasyPKParser.CommentContext)
            else:
                return self.getTypedRuleContext(XeasyPKParser.CommentContext,i)


        def getRuleIndex(self):
            return XeasyPKParser.RULE_peak_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_4d" ):
                listener.enterPeak_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_4d" ):
                listener.exitPeak_4d(self)




    def peak_4d(self):

        localctx = XeasyPKParser.Peak_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_peak_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            self.match(XeasyPKParser.Integer)
            self.state = 236
            self.position()
            self.state = 237
            self.position()
            self.state = 238
            self.position()
            self.state = 239
            self.position()
            self.state = 240
            self.match(XeasyPKParser.Integer)
            self.state = 242
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.state = 241
                self.match(XeasyPKParser.Simple_name)


            self.state = 244
            self.number()
            self.state = 245
            self.number()
            self.state = 247
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.state = 246
                self.match(XeasyPKParser.Simple_name)


            self.state = 249
            self.type_code()
            self.state = 266
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [-1, 17]:
                self.state = 250
                _la = self._input.LA(1)
                if not(_la==-1 or _la==17):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [9, 15]:
                self.state = 251
                self.assign()
                self.state = 252
                self.assign()
                self.state = 253
                self.assign()
                self.state = 254
                self.assign()
                self.state = 256
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
                if la_ == 1:
                    self.state = 255
                    self.match(XeasyPKParser.Integer)


                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==9:
                    self.state = 258
                    self.match(XeasyPKParser.Integer)


                self.state = 264
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [17]:
                    self.state = 261
                    self.match(XeasyPKParser.RETURN)
                    pass
                elif token in [12]:
                    self.state = 262
                    self.comment()
                    pass
                elif token in [-1]:
                    self.state = 263
                    self.match(XeasyPKParser.EOF)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            else:
                raise NoViableAltException(self)

            self.state = 285
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,42,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 268
                    self.assign()
                    self.state = 269
                    self.assign()
                    self.state = 270
                    self.assign()
                    self.state = 271
                    self.assign()
                    self.state = 273
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
                    if la_ == 1:
                        self.state = 272
                        self.match(XeasyPKParser.Integer)


                    self.state = 276
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==9:
                        self.state = 275
                        self.match(XeasyPKParser.Integer)


                    self.state = 281
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [17]:
                        self.state = 278
                        self.match(XeasyPKParser.RETURN)
                        pass
                    elif token in [12]:
                        self.state = 279
                        self.comment()
                        pass
                    elif token in [-1]:
                        self.state = 280
                        self.match(XeasyPKParser.EOF)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 287
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,42,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PositionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(XeasyPKParser.Float, 0)

        def Integer(self):
            return self.getToken(XeasyPKParser.Integer, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_position

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPosition" ):
                listener.enterPosition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPosition" ):
                listener.exitPosition(self)




    def position(self):

        localctx = XeasyPKParser.PositionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_position)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 288
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(XeasyPKParser.Float, 0)

        def Real(self):
            return self.getToken(XeasyPKParser.Real, 0)

        def Integer(self):
            return self.getToken(XeasyPKParser.Integer, 0)

        def Simple_name(self):
            return self.getToken(XeasyPKParser.Simple_name, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = XeasyPKParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 36352) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Type_codeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self):
            return self.getToken(XeasyPKParser.Integer, 0)

        def Simple_name(self):
            return self.getToken(XeasyPKParser.Simple_name, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_type_code

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType_code" ):
                listener.enterType_code(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType_code" ):
                listener.exitType_code(self)




    def type_code(self):

        localctx = XeasyPKParser.Type_codeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_type_code)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 292
            _la = self._input.LA(1)
            if not(_la==9 or _la==15):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self):
            return self.getToken(XeasyPKParser.Integer, 0)

        def Simple_name(self):
            return self.getToken(XeasyPKParser.Simple_name, 0)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign" ):
                listener.enterAssign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign" ):
                listener.exitAssign(self)




    def assign(self):

        localctx = XeasyPKParser.AssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_assign)
        try:
            self.state = 299
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 294
                self.match(XeasyPKParser.Integer)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 295
                self.match(XeasyPKParser.Simple_name)
                self.state = 297
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
                if la_ == 1:
                    self.state = 296
                    self.match(XeasyPKParser.Integer)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMENT(self):
            return self.getToken(XeasyPKParser.COMMENT, 0)

        def RETURN_CM(self):
            return self.getToken(XeasyPKParser.RETURN_CM, 0)

        def EOF(self):
            return self.getToken(XeasyPKParser.EOF, 0)

        def Any_name(self, i:int=None):
            if i is None:
                return self.getTokens(XeasyPKParser.Any_name)
            else:
                return self.getToken(XeasyPKParser.Any_name, i)

        def getRuleIndex(self):
            return XeasyPKParser.RULE_comment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment" ):
                listener.enterComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment" ):
                listener.exitComment(self)




    def comment(self):

        localctx = XeasyPKParser.CommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_comment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 301
            self.match(XeasyPKParser.COMMENT)
            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 302
                self.match(XeasyPKParser.Any_name)
                self.state = 307
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 308
            _la = self._input.LA(1)
            if not(_la==-1 or _la==44):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





