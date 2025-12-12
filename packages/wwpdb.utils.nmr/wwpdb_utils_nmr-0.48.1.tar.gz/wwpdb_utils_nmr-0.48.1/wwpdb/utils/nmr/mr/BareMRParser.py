# Generated from BareMRParser.g4 by ANTLR 4.13.0
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
        4,1,13,49,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,3,
        0,14,8,0,1,0,1,0,5,0,18,8,0,10,0,12,0,21,9,0,1,0,1,0,1,1,1,1,4,1,
        27,8,1,11,1,12,1,28,1,2,4,2,32,8,2,11,2,12,2,33,1,2,1,2,1,3,4,3,
        39,8,3,11,3,12,3,40,1,3,1,3,1,4,1,4,1,5,1,5,1,5,0,0,6,0,2,4,6,8,
        10,0,3,1,1,11,11,2,0,1,2,6,9,1,0,5,7,48,0,13,1,0,0,0,2,24,1,0,0,
        0,4,31,1,0,0,0,6,38,1,0,0,0,8,44,1,0,0,0,10,46,1,0,0,0,12,14,5,11,
        0,0,13,12,1,0,0,0,13,14,1,0,0,0,14,19,1,0,0,0,15,18,3,2,1,0,16,18,
        5,11,0,0,17,15,1,0,0,0,17,16,1,0,0,0,18,21,1,0,0,0,19,17,1,0,0,0,
        19,20,1,0,0,0,20,22,1,0,0,0,21,19,1,0,0,0,22,23,5,0,0,1,23,1,1,0,
        0,0,24,26,3,4,2,0,25,27,3,6,3,0,26,25,1,0,0,0,27,28,1,0,0,0,28,26,
        1,0,0,0,28,29,1,0,0,0,29,3,1,0,0,0,30,32,3,10,5,0,31,30,1,0,0,0,
        32,33,1,0,0,0,33,31,1,0,0,0,33,34,1,0,0,0,34,35,1,0,0,0,35,36,5,
        11,0,0,36,5,1,0,0,0,37,39,3,8,4,0,38,37,1,0,0,0,39,40,1,0,0,0,40,
        38,1,0,0,0,40,41,1,0,0,0,41,42,1,0,0,0,42,43,7,0,0,0,43,7,1,0,0,
        0,44,45,7,1,0,0,45,9,1,0,0,0,46,47,7,2,0,0,47,11,1,0,0,0,6,13,17,
        19,28,33,40
    ]

class BareMRParser ( Parser ):

    grammarFileName = "BareMRParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "Integer", "Float", "SHARP_COMMENT", 
                      "EXCLM_COMMENT", "Number_of_name", "Simple_name", 
                      "Double_quote_string", "Double_quote_integer", "Double_quote_float", 
                      "SPACE", "RETURN", "SECTION_COMMENT", "LINE_COMMENT" ]

    RULE_bare_mr = 0
    RULE_mr_row_format = 1
    RULE_header = 2
    RULE_mr_row_list = 3
    RULE_any = 4
    RULE_column_name = 5

    ruleNames =  [ "bare_mr", "mr_row_format", "header", "mr_row_list", 
                   "any", "column_name" ]

    EOF = Token.EOF
    Integer=1
    Float=2
    SHARP_COMMENT=3
    EXCLM_COMMENT=4
    Number_of_name=5
    Simple_name=6
    Double_quote_string=7
    Double_quote_integer=8
    Double_quote_float=9
    SPACE=10
    RETURN=11
    SECTION_COMMENT=12
    LINE_COMMENT=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Bare_mrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(BareMRParser.EOF, 0)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(BareMRParser.RETURN)
            else:
                return self.getToken(BareMRParser.RETURN, i)

        def mr_row_format(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BareMRParser.Mr_row_formatContext)
            else:
                return self.getTypedRuleContext(BareMRParser.Mr_row_formatContext,i)


        def getRuleIndex(self):
            return BareMRParser.RULE_bare_mr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBare_mr" ):
                listener.enterBare_mr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBare_mr" ):
                listener.exitBare_mr(self)




    def bare_mr(self):

        localctx = BareMRParser.Bare_mrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_bare_mr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 12
                self.match(BareMRParser.RETURN)


            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2272) != 0):
                self.state = 17
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [5, 6, 7]:
                    self.state = 15
                    self.mr_row_format()
                    pass
                elif token in [11]:
                    self.state = 16
                    self.match(BareMRParser.RETURN)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 22
            self.match(BareMRParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mr_row_formatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def header(self):
            return self.getTypedRuleContext(BareMRParser.HeaderContext,0)


        def mr_row_list(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BareMRParser.Mr_row_listContext)
            else:
                return self.getTypedRuleContext(BareMRParser.Mr_row_listContext,i)


        def getRuleIndex(self):
            return BareMRParser.RULE_mr_row_format

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMr_row_format" ):
                listener.enterMr_row_format(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMr_row_format" ):
                listener.exitMr_row_format(self)




    def mr_row_format(self):

        localctx = BareMRParser.Mr_row_formatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_mr_row_format)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.header()
            self.state = 26 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 25
                    self.mr_row_list()

                else:
                    raise NoViableAltException(self)
                self.state = 28 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(BareMRParser.RETURN, 0)

        def column_name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BareMRParser.Column_nameContext)
            else:
                return self.getTypedRuleContext(BareMRParser.Column_nameContext,i)


        def getRuleIndex(self):
            return BareMRParser.RULE_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHeader" ):
                listener.enterHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHeader" ):
                listener.exitHeader(self)




    def header(self):

        localctx = BareMRParser.HeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 30
                self.column_name()
                self.state = 33 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 224) != 0)):
                    break

            self.state = 35
            self.match(BareMRParser.RETURN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mr_row_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(BareMRParser.RETURN, 0)

        def EOF(self):
            return self.getToken(BareMRParser.EOF, 0)

        def any_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BareMRParser.AnyContext)
            else:
                return self.getTypedRuleContext(BareMRParser.AnyContext,i)


        def getRuleIndex(self):
            return BareMRParser.RULE_mr_row_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMr_row_list" ):
                listener.enterMr_row_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMr_row_list" ):
                listener.exitMr_row_list(self)




    def mr_row_list(self):

        localctx = BareMRParser.Mr_row_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_mr_row_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 37
                self.any_()
                self.state = 40 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 966) != 0)):
                    break

            self.state = 42
            _la = self._input.LA(1)
            if not(_la==-1 or _la==11):
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


    class AnyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(BareMRParser.Float, 0)

        def Integer(self):
            return self.getToken(BareMRParser.Integer, 0)

        def Simple_name(self):
            return self.getToken(BareMRParser.Simple_name, 0)

        def Double_quote_float(self):
            return self.getToken(BareMRParser.Double_quote_float, 0)

        def Double_quote_integer(self):
            return self.getToken(BareMRParser.Double_quote_integer, 0)

        def Double_quote_string(self):
            return self.getToken(BareMRParser.Double_quote_string, 0)

        def getRuleIndex(self):
            return BareMRParser.RULE_any

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAny" ):
                listener.enterAny(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAny" ):
                listener.exitAny(self)




    def any_(self):

        localctx = BareMRParser.AnyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_any)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 966) != 0)):
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


    class Column_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Simple_name(self):
            return self.getToken(BareMRParser.Simple_name, 0)

        def Double_quote_string(self):
            return self.getToken(BareMRParser.Double_quote_string, 0)

        def Number_of_name(self):
            return self.getToken(BareMRParser.Number_of_name, 0)

        def getRuleIndex(self):
            return BareMRParser.RULE_column_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterColumn_name" ):
                listener.enterColumn_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitColumn_name" ):
                listener.exitColumn_name(self)




    def column_name(self):

        localctx = BareMRParser.Column_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_column_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 224) != 0)):
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





