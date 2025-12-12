# Generated from BiosymMRParser.g4 by ANTLR 4.13.0
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
        4,1,25,204,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,49,8,0,10,0,12,0,52,9,0,1,0,1,0,
        1,1,4,1,57,8,1,11,1,12,1,58,1,2,3,2,62,8,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,3,2,73,8,2,1,3,4,3,76,8,3,11,3,12,3,77,1,4,3,4,81,
        8,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,5,4,5,92,8,5,11,5,12,5,93,
        1,6,3,6,97,8,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,
        6,1,6,3,6,113,8,6,1,6,1,6,1,6,3,6,118,8,6,1,6,1,6,1,6,3,6,123,8,
        6,1,7,4,7,126,8,7,11,7,12,7,127,1,8,3,8,131,8,8,1,8,1,8,1,8,1,8,
        1,8,1,8,1,8,1,8,1,8,1,8,1,9,4,9,144,8,9,11,9,12,9,145,1,10,3,10,
        149,8,10,1,10,1,10,1,10,1,11,4,11,155,8,11,11,11,12,11,156,1,12,
        3,12,160,8,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,14,1,14,
        1,15,1,15,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,193,8,18,1,18,1,18,
        1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,0,0,20,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,36,38,0,3,1,0,1,3,1,0,21,22,2,0,16,
        16,23,23,208,0,50,1,0,0,0,2,56,1,0,0,0,4,61,1,0,0,0,6,75,1,0,0,0,
        8,80,1,0,0,0,10,91,1,0,0,0,12,96,1,0,0,0,14,125,1,0,0,0,16,130,1,
        0,0,0,18,143,1,0,0,0,20,148,1,0,0,0,22,154,1,0,0,0,24,159,1,0,0,
        0,26,167,1,0,0,0,28,169,1,0,0,0,30,171,1,0,0,0,32,173,1,0,0,0,34,
        177,1,0,0,0,36,185,1,0,0,0,38,196,1,0,0,0,40,49,3,2,1,0,41,49,3,
        6,3,0,42,49,3,10,5,0,43,49,3,14,7,0,44,49,3,18,9,0,45,49,3,22,11,
        0,46,49,3,26,13,0,47,49,3,30,15,0,48,40,1,0,0,0,48,41,1,0,0,0,48,
        42,1,0,0,0,48,43,1,0,0,0,48,44,1,0,0,0,48,45,1,0,0,0,48,46,1,0,0,
        0,48,47,1,0,0,0,49,52,1,0,0,0,50,48,1,0,0,0,50,51,1,0,0,0,51,53,
        1,0,0,0,52,50,1,0,0,0,53,54,5,0,0,1,54,1,1,0,0,0,55,57,3,4,2,0,56,
        55,1,0,0,0,57,58,1,0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,3,1,0,0,
        0,60,62,5,10,0,0,61,60,1,0,0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,64,
        5,9,0,0,64,65,5,9,0,0,65,66,3,28,14,0,66,67,3,28,14,0,67,68,3,28,
        14,0,68,69,3,28,14,0,69,70,3,28,14,0,70,72,3,28,14,0,71,73,3,28,
        14,0,72,71,1,0,0,0,72,73,1,0,0,0,73,5,1,0,0,0,74,76,3,8,4,0,75,74,
        1,0,0,0,76,77,1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,0,78,7,1,0,0,0,79,
        81,5,10,0,0,80,79,1,0,0,0,80,81,1,0,0,0,81,82,1,0,0,0,82,83,5,9,
        0,0,83,84,5,9,0,0,84,85,3,28,14,0,85,86,3,28,14,0,86,87,3,28,14,
        0,87,88,3,28,14,0,88,89,3,28,14,0,89,9,1,0,0,0,90,92,3,12,6,0,91,
        90,1,0,0,0,92,93,1,0,0,0,93,91,1,0,0,0,93,94,1,0,0,0,94,11,1,0,0,
        0,95,97,5,10,0,0,96,95,1,0,0,0,96,97,1,0,0,0,97,98,1,0,0,0,98,99,
        5,9,0,0,99,100,5,9,0,0,100,101,5,9,0,0,101,102,5,9,0,0,102,103,3,
        28,14,0,103,104,3,28,14,0,104,105,3,28,14,0,105,106,3,28,14,0,106,
        107,3,28,14,0,107,108,3,28,14,0,108,112,3,28,14,0,109,110,3,28,14,
        0,110,111,3,28,14,0,111,113,1,0,0,0,112,109,1,0,0,0,112,113,1,0,
        0,0,113,117,1,0,0,0,114,115,3,28,14,0,115,116,3,28,14,0,116,118,
        1,0,0,0,117,114,1,0,0,0,117,118,1,0,0,0,118,122,1,0,0,0,119,120,
        3,28,14,0,120,121,3,28,14,0,121,123,1,0,0,0,122,119,1,0,0,0,122,
        123,1,0,0,0,123,13,1,0,0,0,124,126,3,16,8,0,125,124,1,0,0,0,126,
        127,1,0,0,0,127,125,1,0,0,0,127,128,1,0,0,0,128,15,1,0,0,0,129,131,
        5,10,0,0,130,129,1,0,0,0,130,131,1,0,0,0,131,132,1,0,0,0,132,133,
        5,9,0,0,133,134,5,9,0,0,134,135,5,9,0,0,135,136,5,9,0,0,136,137,
        3,28,14,0,137,138,3,28,14,0,138,139,3,28,14,0,139,140,3,28,14,0,
        140,141,3,28,14,0,141,17,1,0,0,0,142,144,3,20,10,0,143,142,1,0,0,
        0,144,145,1,0,0,0,145,143,1,0,0,0,145,146,1,0,0,0,146,19,1,0,0,0,
        147,149,5,10,0,0,148,147,1,0,0,0,148,149,1,0,0,0,149,150,1,0,0,0,
        150,151,5,9,0,0,151,152,5,8,0,0,152,21,1,0,0,0,153,155,3,24,12,0,
        154,153,1,0,0,0,155,156,1,0,0,0,156,154,1,0,0,0,156,157,1,0,0,0,
        157,23,1,0,0,0,158,160,5,10,0,0,159,158,1,0,0,0,159,160,1,0,0,0,
        160,161,1,0,0,0,161,162,5,9,0,0,162,163,5,9,0,0,163,164,5,9,0,0,
        164,165,5,9,0,0,165,166,5,9,0,0,166,25,1,0,0,0,167,168,5,4,0,0,168,
        27,1,0,0,0,169,170,7,0,0,0,170,29,1,0,0,0,171,172,3,32,16,0,172,
        31,1,0,0,0,173,174,3,34,17,0,174,175,3,36,18,0,175,176,3,38,19,0,
        176,33,1,0,0,0,177,178,5,11,0,0,178,179,5,17,0,0,179,180,5,16,0,
        0,180,181,5,20,0,0,181,182,5,16,0,0,182,183,5,16,0,0,183,184,5,25,
        0,0,184,35,1,0,0,0,185,186,5,11,0,0,186,187,5,18,0,0,187,188,5,16,
        0,0,188,189,7,1,0,0,189,190,5,16,0,0,190,192,5,16,0,0,191,193,5,
        16,0,0,192,191,1,0,0,0,192,193,1,0,0,0,193,194,1,0,0,0,194,195,5,
        25,0,0,195,37,1,0,0,0,196,197,5,11,0,0,197,198,5,19,0,0,198,199,
        5,16,0,0,199,200,7,2,0,0,200,201,5,16,0,0,201,202,5,25,0,0,202,39,
        1,0,0,0,19,48,50,58,61,72,77,80,93,96,112,117,122,127,130,145,148,
        156,159,192
    ]

class BiosymMRParser ( Parser ):

    grammarFileName = "BiosymMRParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'restraint'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'create'", "'function'", "'target'", 
                     "'distance'", "'quadratic'", "'flatBottomed'", "'relative'" ]

    symbolicNames = [ "<INVALID>", "Integer", "Float", "Float_DecimalComma", 
                      "Real", "SHARP_COMMENT", "EXCLM_COMMENT", "SMCLN_COMMENT", 
                      "Chiral_code", "Atom_selection", "Ordinal", "Restraint", 
                      "SPACE", "ENCLOSE_COMMENT", "SECTION_COMMENT", "LINE_COMMENT", 
                      "Double_quote_string", "Create", "Function", "Target", 
                      "Distance", "Quadratic", "Flat_bottomed", "Relative", 
                      "SPACE_II", "RETURN_II" ]

    RULE_biosym_mr = 0
    RULE_distance_restraints = 1
    RULE_distance_restraint = 2
    RULE_distance_constraints = 3
    RULE_distance_constraint = 4
    RULE_dihedral_angle_restraints = 5
    RULE_dihedral_angle_restraint = 6
    RULE_dihedral_angle_constraints = 7
    RULE_dihedral_angle_constraint = 8
    RULE_chirality_constraints = 9
    RULE_chirality_constraint = 10
    RULE_prochirality_constraints = 11
    RULE_prochirality_constraint = 12
    RULE_mixing_time = 13
    RULE_number = 14
    RULE_ins_distance_restraints = 15
    RULE_ins_distance_restraint = 16
    RULE_decl_create = 17
    RULE_decl_function = 18
    RULE_decl_target = 19

    ruleNames =  [ "biosym_mr", "distance_restraints", "distance_restraint", 
                   "distance_constraints", "distance_constraint", "dihedral_angle_restraints", 
                   "dihedral_angle_restraint", "dihedral_angle_constraints", 
                   "dihedral_angle_constraint", "chirality_constraints", 
                   "chirality_constraint", "prochirality_constraints", "prochirality_constraint", 
                   "mixing_time", "number", "ins_distance_restraints", "ins_distance_restraint", 
                   "decl_create", "decl_function", "decl_target" ]

    EOF = Token.EOF
    Integer=1
    Float=2
    Float_DecimalComma=3
    Real=4
    SHARP_COMMENT=5
    EXCLM_COMMENT=6
    SMCLN_COMMENT=7
    Chiral_code=8
    Atom_selection=9
    Ordinal=10
    Restraint=11
    SPACE=12
    ENCLOSE_COMMENT=13
    SECTION_COMMENT=14
    LINE_COMMENT=15
    Double_quote_string=16
    Create=17
    Function=18
    Target=19
    Distance=20
    Quadratic=21
    Flat_bottomed=22
    Relative=23
    SPACE_II=24
    RETURN_II=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Biosym_mrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(BiosymMRParser.EOF, 0)

        def distance_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Distance_restraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Distance_restraintsContext,i)


        def distance_constraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Distance_constraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Distance_constraintsContext,i)


        def dihedral_angle_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Dihedral_angle_restraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Dihedral_angle_restraintsContext,i)


        def dihedral_angle_constraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Dihedral_angle_constraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Dihedral_angle_constraintsContext,i)


        def chirality_constraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Chirality_constraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Chirality_constraintsContext,i)


        def prochirality_constraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Prochirality_constraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Prochirality_constraintsContext,i)


        def mixing_time(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Mixing_timeContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Mixing_timeContext,i)


        def ins_distance_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Ins_distance_restraintsContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Ins_distance_restraintsContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_biosym_mr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBiosym_mr" ):
                listener.enterBiosym_mr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBiosym_mr" ):
                listener.exitBiosym_mr(self)




    def biosym_mr(self):

        localctx = BiosymMRParser.Biosym_mrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_biosym_mr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3600) != 0):
                self.state = 48
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 40
                    self.distance_restraints()
                    pass

                elif la_ == 2:
                    self.state = 41
                    self.distance_constraints()
                    pass

                elif la_ == 3:
                    self.state = 42
                    self.dihedral_angle_restraints()
                    pass

                elif la_ == 4:
                    self.state = 43
                    self.dihedral_angle_constraints()
                    pass

                elif la_ == 5:
                    self.state = 44
                    self.chirality_constraints()
                    pass

                elif la_ == 6:
                    self.state = 45
                    self.prochirality_constraints()
                    pass

                elif la_ == 7:
                    self.state = 46
                    self.mixing_time()
                    pass

                elif la_ == 8:
                    self.state = 47
                    self.ins_distance_restraints()
                    pass


                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 53
            self.match(BiosymMRParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def distance_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Distance_restraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Distance_restraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_distance_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraints" ):
                listener.enterDistance_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraints" ):
                listener.exitDistance_restraints(self)




    def distance_restraints(self):

        localctx = BiosymMRParser.Distance_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_distance_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 55
                    self.distance_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 58 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Atom_selection)
            else:
                return self.getToken(BiosymMRParser.Atom_selection, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.NumberContext,i)


        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_distance_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraint" ):
                listener.enterDistance_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraint" ):
                listener.exitDistance_restraint(self)




    def distance_restraint(self):

        localctx = BiosymMRParser.Distance_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_distance_restraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 60
                self.match(BiosymMRParser.Ordinal)


            self.state = 63
            self.match(BiosymMRParser.Atom_selection)
            self.state = 64
            self.match(BiosymMRParser.Atom_selection)
            self.state = 65
            self.number()
            self.state = 66
            self.number()
            self.state = 67
            self.number()
            self.state = 68
            self.number()
            self.state = 69
            self.number()
            self.state = 70
            self.number()
            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 14) != 0):
                self.state = 71
                self.number()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_constraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def distance_constraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Distance_constraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Distance_constraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_distance_constraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_constraints" ):
                listener.enterDistance_constraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_constraints" ):
                listener.exitDistance_constraints(self)




    def distance_constraints(self):

        localctx = BiosymMRParser.Distance_constraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_distance_constraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 74
                    self.distance_constraint()

                else:
                    raise NoViableAltException(self)
                self.state = 77 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_constraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Atom_selection)
            else:
                return self.getToken(BiosymMRParser.Atom_selection, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.NumberContext,i)


        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_distance_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_constraint" ):
                listener.enterDistance_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_constraint" ):
                listener.exitDistance_constraint(self)




    def distance_constraint(self):

        localctx = BiosymMRParser.Distance_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_distance_constraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 79
                self.match(BiosymMRParser.Ordinal)


            self.state = 82
            self.match(BiosymMRParser.Atom_selection)
            self.state = 83
            self.match(BiosymMRParser.Atom_selection)
            self.state = 84
            self.number()
            self.state = 85
            self.number()
            self.state = 86
            self.number()
            self.state = 87
            self.number()
            self.state = 88
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_angle_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dihedral_angle_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Dihedral_angle_restraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Dihedral_angle_restraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_dihedral_angle_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_restraints" ):
                listener.enterDihedral_angle_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_restraints" ):
                listener.exitDihedral_angle_restraints(self)




    def dihedral_angle_restraints(self):

        localctx = BiosymMRParser.Dihedral_angle_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_dihedral_angle_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 90
                    self.dihedral_angle_restraint()

                else:
                    raise NoViableAltException(self)
                self.state = 93 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_angle_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Atom_selection)
            else:
                return self.getToken(BiosymMRParser.Atom_selection, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.NumberContext,i)


        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_dihedral_angle_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_restraint" ):
                listener.enterDihedral_angle_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_restraint" ):
                listener.exitDihedral_angle_restraint(self)




    def dihedral_angle_restraint(self):

        localctx = BiosymMRParser.Dihedral_angle_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_dihedral_angle_restraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 95
                self.match(BiosymMRParser.Ordinal)


            self.state = 98
            self.match(BiosymMRParser.Atom_selection)
            self.state = 99
            self.match(BiosymMRParser.Atom_selection)
            self.state = 100
            self.match(BiosymMRParser.Atom_selection)
            self.state = 101
            self.match(BiosymMRParser.Atom_selection)
            self.state = 102
            self.number()
            self.state = 103
            self.number()
            self.state = 104
            self.number()
            self.state = 105
            self.number()
            self.state = 106
            self.number()
            self.state = 107
            self.number()
            self.state = 108
            self.number()
            self.state = 112
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 109
                self.number()
                self.state = 110
                self.number()


            self.state = 117
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 114
                self.number()
                self.state = 115
                self.number()


            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 14) != 0):
                self.state = 119
                self.number()
                self.state = 120
                self.number()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_angle_constraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dihedral_angle_constraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Dihedral_angle_constraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Dihedral_angle_constraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_dihedral_angle_constraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_constraints" ):
                listener.enterDihedral_angle_constraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_constraints" ):
                listener.exitDihedral_angle_constraints(self)




    def dihedral_angle_constraints(self):

        localctx = BiosymMRParser.Dihedral_angle_constraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_dihedral_angle_constraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 124
                    self.dihedral_angle_constraint()

                else:
                    raise NoViableAltException(self)
                self.state = 127 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_angle_constraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Atom_selection)
            else:
                return self.getToken(BiosymMRParser.Atom_selection, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.NumberContext,i)


        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_dihedral_angle_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_constraint" ):
                listener.enterDihedral_angle_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_constraint" ):
                listener.exitDihedral_angle_constraint(self)




    def dihedral_angle_constraint(self):

        localctx = BiosymMRParser.Dihedral_angle_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_dihedral_angle_constraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 129
                self.match(BiosymMRParser.Ordinal)


            self.state = 132
            self.match(BiosymMRParser.Atom_selection)
            self.state = 133
            self.match(BiosymMRParser.Atom_selection)
            self.state = 134
            self.match(BiosymMRParser.Atom_selection)
            self.state = 135
            self.match(BiosymMRParser.Atom_selection)
            self.state = 136
            self.number()
            self.state = 137
            self.number()
            self.state = 138
            self.number()
            self.state = 139
            self.number()
            self.state = 140
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Chirality_constraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def chirality_constraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Chirality_constraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Chirality_constraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_chirality_constraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChirality_constraints" ):
                listener.enterChirality_constraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChirality_constraints" ):
                listener.exitChirality_constraints(self)




    def chirality_constraints(self):

        localctx = BiosymMRParser.Chirality_constraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_chirality_constraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 142
                    self.chirality_constraint()

                else:
                    raise NoViableAltException(self)
                self.state = 145 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Chirality_constraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self):
            return self.getToken(BiosymMRParser.Atom_selection, 0)

        def Chiral_code(self):
            return self.getToken(BiosymMRParser.Chiral_code, 0)

        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_chirality_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChirality_constraint" ):
                listener.enterChirality_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChirality_constraint" ):
                listener.exitChirality_constraint(self)




    def chirality_constraint(self):

        localctx = BiosymMRParser.Chirality_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_chirality_constraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 147
                self.match(BiosymMRParser.Ordinal)


            self.state = 150
            self.match(BiosymMRParser.Atom_selection)
            self.state = 151
            self.match(BiosymMRParser.Chiral_code)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Prochirality_constraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def prochirality_constraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BiosymMRParser.Prochirality_constraintContext)
            else:
                return self.getTypedRuleContext(BiosymMRParser.Prochirality_constraintContext,i)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_prochirality_constraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProchirality_constraints" ):
                listener.enterProchirality_constraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProchirality_constraints" ):
                listener.exitProchirality_constraints(self)




    def prochirality_constraints(self):

        localctx = BiosymMRParser.Prochirality_constraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_prochirality_constraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 153
                    self.prochirality_constraint()

                else:
                    raise NoViableAltException(self)
                self.state = 156 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Prochirality_constraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom_selection(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Atom_selection)
            else:
                return self.getToken(BiosymMRParser.Atom_selection, i)

        def Ordinal(self):
            return self.getToken(BiosymMRParser.Ordinal, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_prochirality_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProchirality_constraint" ):
                listener.enterProchirality_constraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProchirality_constraint" ):
                listener.exitProchirality_constraint(self)




    def prochirality_constraint(self):

        localctx = BiosymMRParser.Prochirality_constraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_prochirality_constraint)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 158
                self.match(BiosymMRParser.Ordinal)


            self.state = 161
            self.match(BiosymMRParser.Atom_selection)
            self.state = 162
            self.match(BiosymMRParser.Atom_selection)
            self.state = 163
            self.match(BiosymMRParser.Atom_selection)
            self.state = 164
            self.match(BiosymMRParser.Atom_selection)
            self.state = 165
            self.match(BiosymMRParser.Atom_selection)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mixing_timeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Real(self):
            return self.getToken(BiosymMRParser.Real, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_mixing_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMixing_time" ):
                listener.enterMixing_time(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMixing_time" ):
                listener.exitMixing_time(self)




    def mixing_time(self):

        localctx = BiosymMRParser.Mixing_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_mixing_time)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            self.match(BiosymMRParser.Real)
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
            return self.getToken(BiosymMRParser.Float, 0)

        def Float_DecimalComma(self):
            return self.getToken(BiosymMRParser.Float_DecimalComma, 0)

        def Integer(self):
            return self.getToken(BiosymMRParser.Integer, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = BiosymMRParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14) != 0)):
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


    class Ins_distance_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ins_distance_restraint(self):
            return self.getTypedRuleContext(BiosymMRParser.Ins_distance_restraintContext,0)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_ins_distance_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIns_distance_restraints" ):
                listener.enterIns_distance_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIns_distance_restraints" ):
                listener.exitIns_distance_restraints(self)




    def ins_distance_restraints(self):

        localctx = BiosymMRParser.Ins_distance_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_ins_distance_restraints)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.ins_distance_restraint()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ins_distance_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def decl_create(self):
            return self.getTypedRuleContext(BiosymMRParser.Decl_createContext,0)


        def decl_function(self):
            return self.getTypedRuleContext(BiosymMRParser.Decl_functionContext,0)


        def decl_target(self):
            return self.getTypedRuleContext(BiosymMRParser.Decl_targetContext,0)


        def getRuleIndex(self):
            return BiosymMRParser.RULE_ins_distance_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIns_distance_restraint" ):
                listener.enterIns_distance_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIns_distance_restraint" ):
                listener.exitIns_distance_restraint(self)




    def ins_distance_restraint(self):

        localctx = BiosymMRParser.Ins_distance_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_ins_distance_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 173
            self.decl_create()
            self.state = 174
            self.decl_function()
            self.state = 175
            self.decl_target()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Decl_createContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Restraint(self):
            return self.getToken(BiosymMRParser.Restraint, 0)

        def Create(self):
            return self.getToken(BiosymMRParser.Create, 0)

        def Double_quote_string(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Double_quote_string)
            else:
                return self.getToken(BiosymMRParser.Double_quote_string, i)

        def Distance(self):
            return self.getToken(BiosymMRParser.Distance, 0)

        def RETURN_II(self):
            return self.getToken(BiosymMRParser.RETURN_II, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_decl_create

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecl_create" ):
                listener.enterDecl_create(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecl_create" ):
                listener.exitDecl_create(self)




    def decl_create(self):

        localctx = BiosymMRParser.Decl_createContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_decl_create)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.match(BiosymMRParser.Restraint)
            self.state = 178
            self.match(BiosymMRParser.Create)
            self.state = 179
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 180
            self.match(BiosymMRParser.Distance)
            self.state = 181
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 182
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 183
            self.match(BiosymMRParser.RETURN_II)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Decl_functionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Restraint(self):
            return self.getToken(BiosymMRParser.Restraint, 0)

        def Function(self):
            return self.getToken(BiosymMRParser.Function, 0)

        def Double_quote_string(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Double_quote_string)
            else:
                return self.getToken(BiosymMRParser.Double_quote_string, i)

        def RETURN_II(self):
            return self.getToken(BiosymMRParser.RETURN_II, 0)

        def Quadratic(self):
            return self.getToken(BiosymMRParser.Quadratic, 0)

        def Flat_bottomed(self):
            return self.getToken(BiosymMRParser.Flat_bottomed, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_decl_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecl_function" ):
                listener.enterDecl_function(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecl_function" ):
                listener.exitDecl_function(self)




    def decl_function(self):

        localctx = BiosymMRParser.Decl_functionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_decl_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(BiosymMRParser.Restraint)
            self.state = 186
            self.match(BiosymMRParser.Function)
            self.state = 187
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 188
            _la = self._input.LA(1)
            if not(_la==21 or _la==22):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 189
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 190
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 192
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 191
                self.match(BiosymMRParser.Double_quote_string)


            self.state = 194
            self.match(BiosymMRParser.RETURN_II)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Decl_targetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Restraint(self):
            return self.getToken(BiosymMRParser.Restraint, 0)

        def Target(self):
            return self.getToken(BiosymMRParser.Target, 0)

        def Double_quote_string(self, i:int=None):
            if i is None:
                return self.getTokens(BiosymMRParser.Double_quote_string)
            else:
                return self.getToken(BiosymMRParser.Double_quote_string, i)

        def RETURN_II(self):
            return self.getToken(BiosymMRParser.RETURN_II, 0)

        def Relative(self):
            return self.getToken(BiosymMRParser.Relative, 0)

        def getRuleIndex(self):
            return BiosymMRParser.RULE_decl_target

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecl_target" ):
                listener.enterDecl_target(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecl_target" ):
                listener.exitDecl_target(self)




    def decl_target(self):

        localctx = BiosymMRParser.Decl_targetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_decl_target)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.match(BiosymMRParser.Restraint)
            self.state = 197
            self.match(BiosymMRParser.Target)
            self.state = 198
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 199
            _la = self._input.LA(1)
            if not(_la==16 or _la==23):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 200
            self.match(BiosymMRParser.Double_quote_string)
            self.state = 201
            self.match(BiosymMRParser.RETURN_II)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





