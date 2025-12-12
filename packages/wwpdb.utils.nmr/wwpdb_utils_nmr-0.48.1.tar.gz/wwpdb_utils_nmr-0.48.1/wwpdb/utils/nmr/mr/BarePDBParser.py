# Generated from BarePDBParser.g4 by ANTLR 4.13.0
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
        4,1,20,133,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,1,0,1,0,1,0,5,0,33,8,0,10,0,12,0,36,9,0,1,0,1,0,1,1,1,1,5,1,
        42,8,1,10,1,12,1,45,9,1,1,1,1,1,1,2,4,2,50,8,2,11,2,12,2,51,1,3,
        1,3,1,3,1,3,1,3,1,3,3,3,60,8,3,1,3,1,3,3,3,64,8,3,1,3,1,3,1,3,1,
        3,1,3,3,3,71,8,3,1,3,3,3,74,8,3,1,3,3,3,77,8,3,1,4,1,4,1,4,1,4,1,
        4,3,4,84,8,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,95,8,6,1,7,
        1,7,1,7,1,8,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,3,12,110,8,
        12,1,12,3,12,113,8,12,1,12,1,12,5,12,117,8,12,10,12,12,12,120,9,
        12,1,12,1,12,1,13,1,13,5,13,126,8,13,10,13,12,13,129,9,13,1,13,1,
        13,1,13,0,0,14,0,2,4,6,8,10,12,14,16,18,20,22,24,26,0,5,1,1,20,20,
        2,0,1,1,5,5,2,0,5,5,12,12,2,0,1,2,12,13,1,0,1,2,140,0,34,1,0,0,0,
        2,39,1,0,0,0,4,49,1,0,0,0,6,53,1,0,0,0,8,83,1,0,0,0,10,85,1,0,0,
        0,12,94,1,0,0,0,14,96,1,0,0,0,16,99,1,0,0,0,18,102,1,0,0,0,20,104,
        1,0,0,0,22,106,1,0,0,0,24,109,1,0,0,0,26,123,1,0,0,0,28,33,3,2,1,
        0,29,33,3,4,2,0,30,33,3,24,12,0,31,33,3,26,13,0,32,28,1,0,0,0,32,
        29,1,0,0,0,32,30,1,0,0,0,32,31,1,0,0,0,33,36,1,0,0,0,34,32,1,0,0,
        0,34,35,1,0,0,0,35,37,1,0,0,0,36,34,1,0,0,0,37,38,5,0,0,1,38,1,1,
        0,0,0,39,43,5,3,0,0,40,42,5,18,0,0,41,40,1,0,0,0,42,45,1,0,0,0,43,
        41,1,0,0,0,43,44,1,0,0,0,44,46,1,0,0,0,45,43,1,0,0,0,46,47,7,0,0,
        0,47,3,1,0,0,0,48,50,3,6,3,0,49,48,1,0,0,0,50,51,1,0,0,0,51,49,1,
        0,0,0,51,52,1,0,0,0,52,5,1,0,0,0,53,54,3,8,4,0,54,55,3,10,5,0,55,
        63,3,10,5,0,56,57,5,1,0,0,57,64,5,1,0,0,58,60,5,12,0,0,59,58,1,0,
        0,0,59,60,1,0,0,0,60,61,1,0,0,0,61,64,7,1,0,0,62,64,5,12,0,0,63,
        56,1,0,0,0,63,59,1,0,0,0,63,62,1,0,0,0,64,65,1,0,0,0,65,70,3,12,
        6,0,66,67,3,22,11,0,67,68,3,22,11,0,68,71,1,0,0,0,69,71,5,6,0,0,
        70,66,1,0,0,0,70,69,1,0,0,0,70,71,1,0,0,0,71,73,1,0,0,0,72,74,3,
        20,10,0,73,72,1,0,0,0,73,74,1,0,0,0,74,76,1,0,0,0,75,77,3,20,10,
        0,76,75,1,0,0,0,76,77,1,0,0,0,77,7,1,0,0,0,78,79,5,8,0,0,79,84,5,
        1,0,0,80,81,5,9,0,0,81,84,5,1,0,0,82,84,5,4,0,0,83,78,1,0,0,0,83,
        80,1,0,0,0,83,82,1,0,0,0,84,9,1,0,0,0,85,86,7,2,0,0,86,11,1,0,0,
        0,87,88,3,22,11,0,88,89,3,22,11,0,89,90,3,22,11,0,90,95,1,0,0,0,
        91,95,3,14,7,0,92,95,3,16,8,0,93,95,3,18,9,0,94,87,1,0,0,0,94,91,
        1,0,0,0,94,92,1,0,0,0,94,93,1,0,0,0,95,13,1,0,0,0,96,97,3,22,11,
        0,97,98,5,6,0,0,98,15,1,0,0,0,99,100,5,6,0,0,100,101,3,22,11,0,101,
        17,1,0,0,0,102,103,5,7,0,0,103,19,1,0,0,0,104,105,7,3,0,0,105,21,
        1,0,0,0,106,107,7,4,0,0,107,23,1,0,0,0,108,110,5,8,0,0,109,108,1,
        0,0,0,109,110,1,0,0,0,110,112,1,0,0,0,111,113,5,9,0,0,112,111,1,
        0,0,0,112,113,1,0,0,0,113,114,1,0,0,0,114,118,5,10,0,0,115,117,5,
        18,0,0,116,115,1,0,0,0,117,120,1,0,0,0,118,116,1,0,0,0,118,119,1,
        0,0,0,119,121,1,0,0,0,120,118,1,0,0,0,121,122,7,0,0,0,122,25,1,0,
        0,0,123,127,5,11,0,0,124,126,5,18,0,0,125,124,1,0,0,0,126,129,1,
        0,0,0,127,125,1,0,0,0,127,128,1,0,0,0,128,130,1,0,0,0,129,127,1,
        0,0,0,130,131,7,0,0,0,131,27,1,0,0,0,15,32,34,43,51,59,63,70,73,
        76,83,94,109,112,118,127
    ]

class BarePDBParser ( Parser ):

    grammarFileName = "BarePDBParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'ATOM'", "'HETATM'", "'TER'", "'END'" ]

    symbolicNames = [ "<INVALID>", "Integer", "Float", "COMMENT", "Hetatm_decimal", 
                      "Integer_concat_alt", "Float_concat_2", "Float_concat_3", 
                      "Atom", "Hetatm", "Ter", "End", "Simple_name", "Null_value", 
                      "SPACE", "ENCLOSE_COMMENT", "SECTION_COMMENT", "LINE_COMMENT", 
                      "Any_name", "SPACE_CM", "RETURN_CM" ]

    RULE_bare_pdb = 0
    RULE_comment = 1
    RULE_coordinates = 2
    RULE_atom_coordinate = 3
    RULE_atom_num = 4
    RULE_atom_name = 5
    RULE_xyz = 6
    RULE_x_yz = 7
    RULE_xy_z = 8
    RULE_x_y_z = 9
    RULE_undefined = 10
    RULE_number = 11
    RULE_terminal = 12
    RULE_end = 13

    ruleNames =  [ "bare_pdb", "comment", "coordinates", "atom_coordinate", 
                   "atom_num", "atom_name", "xyz", "x_yz", "xy_z", "x_y_z", 
                   "undefined", "number", "terminal", "end" ]

    EOF = Token.EOF
    Integer=1
    Float=2
    COMMENT=3
    Hetatm_decimal=4
    Integer_concat_alt=5
    Float_concat_2=6
    Float_concat_3=7
    Atom=8
    Hetatm=9
    Ter=10
    End=11
    Simple_name=12
    Null_value=13
    SPACE=14
    ENCLOSE_COMMENT=15
    SECTION_COMMENT=16
    LINE_COMMENT=17
    Any_name=18
    SPACE_CM=19
    RETURN_CM=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Bare_pdbContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(BarePDBParser.EOF, 0)

        def comment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.CommentContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.CommentContext,i)


        def coordinates(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.CoordinatesContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.CoordinatesContext,i)


        def terminal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.TerminalContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.TerminalContext,i)


        def end(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.EndContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.EndContext,i)


        def getRuleIndex(self):
            return BarePDBParser.RULE_bare_pdb

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBare_pdb" ):
                listener.enterBare_pdb(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBare_pdb" ):
                listener.exitBare_pdb(self)




    def bare_pdb(self):

        localctx = BarePDBParser.Bare_pdbContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_bare_pdb)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3864) != 0):
                self.state = 32
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 28
                    self.comment()
                    pass

                elif la_ == 2:
                    self.state = 29
                    self.coordinates()
                    pass

                elif la_ == 3:
                    self.state = 30
                    self.terminal()
                    pass

                elif la_ == 4:
                    self.state = 31
                    self.end()
                    pass


                self.state = 36
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 37
            self.match(BarePDBParser.EOF)
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
            return self.getToken(BarePDBParser.COMMENT, 0)

        def RETURN_CM(self):
            return self.getToken(BarePDBParser.RETURN_CM, 0)

        def EOF(self):
            return self.getToken(BarePDBParser.EOF, 0)

        def Any_name(self, i:int=None):
            if i is None:
                return self.getTokens(BarePDBParser.Any_name)
            else:
                return self.getToken(BarePDBParser.Any_name, i)

        def getRuleIndex(self):
            return BarePDBParser.RULE_comment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment" ):
                listener.enterComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment" ):
                listener.exitComment(self)




    def comment(self):

        localctx = BarePDBParser.CommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_comment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(BarePDBParser.COMMENT)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 40
                self.match(BarePDBParser.Any_name)
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
            _la = self._input.LA(1)
            if not(_la==-1 or _la==20):
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


    class CoordinatesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom_coordinate(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.Atom_coordinateContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.Atom_coordinateContext,i)


        def getRuleIndex(self):
            return BarePDBParser.RULE_coordinates

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordinates" ):
                listener.enterCoordinates(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordinates" ):
                listener.exitCoordinates(self)




    def coordinates(self):

        localctx = BarePDBParser.CoordinatesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_coordinates)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 48
                    self.atom_coordinate()

                else:
                    raise NoViableAltException(self)
                self.state = 51 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Atom_coordinateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom_num(self):
            return self.getTypedRuleContext(BarePDBParser.Atom_numContext,0)


        def atom_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.Atom_nameContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.Atom_nameContext,i)


        def xyz(self):
            return self.getTypedRuleContext(BarePDBParser.XyzContext,0)


        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(BarePDBParser.Integer)
            else:
                return self.getToken(BarePDBParser.Integer, i)

        def Simple_name(self):
            return self.getToken(BarePDBParser.Simple_name, 0)

        def Integer_concat_alt(self):
            return self.getToken(BarePDBParser.Integer_concat_alt, 0)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.NumberContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.NumberContext,i)


        def Float_concat_2(self):
            return self.getToken(BarePDBParser.Float_concat_2, 0)

        def undefined(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.UndefinedContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.UndefinedContext,i)


        def getRuleIndex(self):
            return BarePDBParser.RULE_atom_coordinate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom_coordinate" ):
                listener.enterAtom_coordinate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom_coordinate" ):
                listener.exitAtom_coordinate(self)




    def atom_coordinate(self):

        localctx = BarePDBParser.Atom_coordinateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_atom_coordinate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.atom_num()
            self.state = 54
            self.atom_name()
            self.state = 55
            self.atom_name()
            self.state = 63
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 56
                self.match(BarePDBParser.Integer)
                self.state = 57
                self.match(BarePDBParser.Integer)
                pass

            elif la_ == 2:
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 58
                    self.match(BarePDBParser.Simple_name)


                self.state = 61
                _la = self._input.LA(1)
                if not(_la==1 or _la==5):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 3:
                self.state = 62
                self.match(BarePDBParser.Simple_name)
                pass


            self.state = 65
            self.xyz()
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 66
                self.number()
                self.state = 67
                self.number()

            elif la_ == 2:
                self.state = 69
                self.match(BarePDBParser.Float_concat_2)


            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 72
                self.undefined()


            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 12294) != 0):
                self.state = 75
                self.undefined()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Atom_numContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Atom(self):
            return self.getToken(BarePDBParser.Atom, 0)

        def Integer(self):
            return self.getToken(BarePDBParser.Integer, 0)

        def Hetatm(self):
            return self.getToken(BarePDBParser.Hetatm, 0)

        def Hetatm_decimal(self):
            return self.getToken(BarePDBParser.Hetatm_decimal, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_atom_num

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom_num" ):
                listener.enterAtom_num(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom_num" ):
                listener.exitAtom_num(self)




    def atom_num(self):

        localctx = BarePDBParser.Atom_numContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_atom_num)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.state = 78
                self.match(BarePDBParser.Atom)
                self.state = 79
                self.match(BarePDBParser.Integer)
                pass
            elif token in [9]:
                self.state = 80
                self.match(BarePDBParser.Hetatm)
                self.state = 81
                self.match(BarePDBParser.Integer)
                pass
            elif token in [4]:
                self.state = 82
                self.match(BarePDBParser.Hetatm_decimal)
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


    class Atom_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Simple_name(self):
            return self.getToken(BarePDBParser.Simple_name, 0)

        def Integer_concat_alt(self):
            return self.getToken(BarePDBParser.Integer_concat_alt, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_atom_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom_name" ):
                listener.enterAtom_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom_name" ):
                listener.exitAtom_name(self)




    def atom_name(self):

        localctx = BarePDBParser.Atom_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_atom_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            _la = self._input.LA(1)
            if not(_la==5 or _la==12):
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


    class XyzContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BarePDBParser.NumberContext)
            else:
                return self.getTypedRuleContext(BarePDBParser.NumberContext,i)


        def x_yz(self):
            return self.getTypedRuleContext(BarePDBParser.X_yzContext,0)


        def xy_z(self):
            return self.getTypedRuleContext(BarePDBParser.Xy_zContext,0)


        def x_y_z(self):
            return self.getTypedRuleContext(BarePDBParser.X_y_zContext,0)


        def getRuleIndex(self):
            return BarePDBParser.RULE_xyz

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXyz" ):
                listener.enterXyz(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXyz" ):
                listener.exitXyz(self)




    def xyz(self):

        localctx = BarePDBParser.XyzContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_xyz)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 87
                self.number()
                self.state = 88
                self.number()
                self.state = 89
                self.number()
                pass

            elif la_ == 2:
                self.state = 91
                self.x_yz()
                pass

            elif la_ == 3:
                self.state = 92
                self.xy_z()
                pass

            elif la_ == 4:
                self.state = 93
                self.x_y_z()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class X_yzContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(BarePDBParser.NumberContext,0)


        def Float_concat_2(self):
            return self.getToken(BarePDBParser.Float_concat_2, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_x_yz

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterX_yz" ):
                listener.enterX_yz(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitX_yz" ):
                listener.exitX_yz(self)




    def x_yz(self):

        localctx = BarePDBParser.X_yzContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_x_yz)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.number()
            self.state = 97
            self.match(BarePDBParser.Float_concat_2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Xy_zContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float_concat_2(self):
            return self.getToken(BarePDBParser.Float_concat_2, 0)

        def number(self):
            return self.getTypedRuleContext(BarePDBParser.NumberContext,0)


        def getRuleIndex(self):
            return BarePDBParser.RULE_xy_z

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXy_z" ):
                listener.enterXy_z(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXy_z" ):
                listener.exitXy_z(self)




    def xy_z(self):

        localctx = BarePDBParser.Xy_zContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_xy_z)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(BarePDBParser.Float_concat_2)
            self.state = 100
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class X_y_zContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float_concat_3(self):
            return self.getToken(BarePDBParser.Float_concat_3, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_x_y_z

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterX_y_z" ):
                listener.enterX_y_z(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitX_y_z" ):
                listener.exitX_y_z(self)




    def x_y_z(self):

        localctx = BarePDBParser.X_y_zContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_x_y_z)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(BarePDBParser.Float_concat_3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UndefinedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Simple_name(self):
            return self.getToken(BarePDBParser.Simple_name, 0)

        def Integer(self):
            return self.getToken(BarePDBParser.Integer, 0)

        def Float(self):
            return self.getToken(BarePDBParser.Float, 0)

        def Null_value(self):
            return self.getToken(BarePDBParser.Null_value, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_undefined

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUndefined" ):
                listener.enterUndefined(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUndefined" ):
                listener.exitUndefined(self)




    def undefined(self):

        localctx = BarePDBParser.UndefinedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_undefined)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 12294) != 0)):
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
            return self.getToken(BarePDBParser.Float, 0)

        def Integer(self):
            return self.getToken(BarePDBParser.Integer, 0)

        def getRuleIndex(self):
            return BarePDBParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = BarePDBParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            _la = self._input.LA(1)
            if not(_la==1 or _la==2):
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


    class TerminalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Ter(self):
            return self.getToken(BarePDBParser.Ter, 0)

        def RETURN_CM(self):
            return self.getToken(BarePDBParser.RETURN_CM, 0)

        def EOF(self):
            return self.getToken(BarePDBParser.EOF, 0)

        def Atom(self):
            return self.getToken(BarePDBParser.Atom, 0)

        def Hetatm(self):
            return self.getToken(BarePDBParser.Hetatm, 0)

        def Any_name(self, i:int=None):
            if i is None:
                return self.getTokens(BarePDBParser.Any_name)
            else:
                return self.getToken(BarePDBParser.Any_name, i)

        def getRuleIndex(self):
            return BarePDBParser.RULE_terminal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminal" ):
                listener.enterTerminal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminal" ):
                listener.exitTerminal(self)




    def terminal(self):

        localctx = BarePDBParser.TerminalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_terminal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 108
                self.match(BarePDBParser.Atom)


            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 111
                self.match(BarePDBParser.Hetatm)


            self.state = 114
            self.match(BarePDBParser.Ter)
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 115
                self.match(BarePDBParser.Any_name)
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            _la = self._input.LA(1)
            if not(_la==-1 or _la==20):
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


    class EndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def End(self):
            return self.getToken(BarePDBParser.End, 0)

        def RETURN_CM(self):
            return self.getToken(BarePDBParser.RETURN_CM, 0)

        def EOF(self):
            return self.getToken(BarePDBParser.EOF, 0)

        def Any_name(self, i:int=None):
            if i is None:
                return self.getTokens(BarePDBParser.Any_name)
            else:
                return self.getToken(BarePDBParser.Any_name, i)

        def getRuleIndex(self):
            return BarePDBParser.RULE_end

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)




    def end(self):

        localctx = BarePDBParser.EndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_end)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(BarePDBParser.End)
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 124
                self.match(BarePDBParser.Any_name)
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 130
            _la = self._input.LA(1)
            if not(_la==-1 or _la==20):
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





