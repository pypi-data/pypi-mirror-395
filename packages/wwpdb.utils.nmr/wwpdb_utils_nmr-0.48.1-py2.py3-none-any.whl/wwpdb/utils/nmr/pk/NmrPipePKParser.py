# Generated from NmrPipePKParser.g4 by ANTLR 4.13.0
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
        4,1,115,729,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,
        7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,
        13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,
        20,7,20,2,21,7,21,2,22,7,22,1,0,3,0,48,8,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,62,8,0,10,0,12,0,65,9,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,3,2,102,8,2,1,2,1,2,1,2,3,2,107,8,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,3,2,134,8,2,1,2,1,2,1,2,3,2,139,8,2,1,2,1,2,1,2,1,2,3,
        2,145,8,2,1,2,1,2,1,2,3,2,150,8,2,1,2,4,2,153,8,2,11,2,12,2,154,
        1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,
        1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,180,8,3,1,3,1,3,1,3,3,3,185,8,3,
        1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,3,4,221,8,4,1,4,1,4,1,4,3,4,226,8,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,261,8,4,1,4,
        1,4,1,4,3,4,266,8,4,1,4,1,4,1,4,1,4,3,4,272,8,4,1,4,1,4,1,4,3,4,
        277,8,4,1,4,4,4,280,8,4,11,4,12,4,281,1,5,1,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,315,8,5,1,5,1,5,1,5,3,5,320,
        8,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,364,8,6,1,6,1,6,
        1,6,3,6,369,8,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,412,8,6,
        1,6,1,6,1,6,3,6,417,8,6,1,6,1,6,1,6,1,6,3,6,423,8,6,1,6,1,6,1,6,
        3,6,428,8,6,1,6,4,6,431,8,6,11,6,12,6,432,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,3,7,474,8,7,1,7,1,7,1,7,3,7,479,8,7,1,7,1,7,1,8,1,8,1,8,1,
        8,1,8,4,8,488,8,8,11,8,12,8,489,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,
        1,9,1,9,1,10,1,10,4,10,504,8,10,11,10,12,10,505,1,10,1,10,1,10,1,
        10,1,10,1,10,1,10,1,10,1,10,3,10,517,8,10,1,10,1,10,4,10,521,8,10,
        11,10,12,10,522,1,11,1,11,1,11,1,11,4,11,529,8,11,11,11,12,11,530,
        1,11,1,11,1,12,1,12,4,12,537,8,12,11,12,12,12,538,1,12,1,12,1,12,
        1,12,3,12,545,8,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,3,12,554,8,
        12,1,12,1,12,4,12,558,8,12,11,12,12,12,559,1,13,1,13,3,13,564,8,
        13,1,13,1,13,1,13,1,13,4,13,570,8,13,11,13,12,13,571,1,13,1,13,1,
        14,1,14,4,14,578,8,14,11,14,12,14,579,1,14,1,14,1,14,1,14,3,14,586,
        8,14,1,14,3,14,589,8,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,
        3,14,599,8,14,1,14,1,14,4,14,603,8,14,11,14,12,14,604,1,15,1,15,
        3,15,609,8,15,1,15,3,15,612,8,15,1,15,1,15,1,15,1,15,1,15,4,15,619,
        8,15,11,15,12,15,620,1,15,1,15,1,16,4,16,626,8,16,11,16,12,16,627,
        1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,3,17,644,8,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,18,4,18,656,8,18,11,18,12,18,657,1,19,1,19,1,19,1,19,1,19,1,19,
        1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,3,19,
        678,8,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,20,4,20,
        690,8,20,11,20,12,20,691,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,
        1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,
        1,21,3,21,716,8,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,
        1,22,1,22,1,22,0,0,23,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,42,44,0,5,1,0,17,20,1,1,14,14,1,0,23,24,1,1,115,115,
        2,0,7,9,12,12,773,0,47,1,0,0,0,2,68,1,0,0,0,4,77,1,0,0,0,6,156,1,
        0,0,0,8,188,1,0,0,0,10,283,1,0,0,0,12,323,1,0,0,0,14,434,1,0,0,0,
        16,482,1,0,0,0,18,491,1,0,0,0,20,501,1,0,0,0,22,524,1,0,0,0,24,534,
        1,0,0,0,26,561,1,0,0,0,28,575,1,0,0,0,30,606,1,0,0,0,32,625,1,0,
        0,0,34,629,1,0,0,0,36,655,1,0,0,0,38,659,1,0,0,0,40,689,1,0,0,0,
        42,693,1,0,0,0,44,726,1,0,0,0,46,48,5,14,0,0,47,46,1,0,0,0,47,48,
        1,0,0,0,48,63,1,0,0,0,49,62,3,2,1,0,50,62,3,4,2,0,51,62,3,8,4,0,
        52,62,3,12,6,0,53,62,3,16,8,0,54,62,3,20,10,0,55,62,3,24,12,0,56,
        62,3,28,14,0,57,62,3,32,16,0,58,62,3,36,18,0,59,62,3,40,20,0,60,
        62,5,14,0,0,61,49,1,0,0,0,61,50,1,0,0,0,61,51,1,0,0,0,61,52,1,0,
        0,0,61,53,1,0,0,0,61,54,1,0,0,0,61,55,1,0,0,0,61,56,1,0,0,0,61,57,
        1,0,0,0,61,58,1,0,0,0,61,59,1,0,0,0,61,60,1,0,0,0,62,65,1,0,0,0,
        63,61,1,0,0,0,63,64,1,0,0,0,64,66,1,0,0,0,65,63,1,0,0,0,66,67,5,
        0,0,1,67,1,1,0,0,0,68,69,5,1,0,0,69,70,7,0,0,0,70,71,5,28,0,0,71,
        72,5,25,0,0,72,73,5,25,0,0,73,74,5,21,0,0,74,75,5,21,0,0,75,76,5,
        30,0,0,76,3,1,0,0,0,77,78,5,2,0,0,78,79,5,32,0,0,79,80,5,33,0,0,
        80,81,5,34,0,0,81,82,5,37,0,0,82,83,5,38,0,0,83,84,5,41,0,0,84,85,
        5,42,0,0,85,86,5,45,0,0,86,87,5,46,0,0,87,88,5,49,0,0,88,89,5,50,
        0,0,89,90,5,53,0,0,90,91,5,54,0,0,91,92,5,57,0,0,92,93,5,58,0,0,
        93,94,5,59,0,0,94,95,5,60,0,0,95,96,5,65,0,0,96,97,5,66,0,0,97,98,
        5,67,0,0,98,99,5,68,0,0,99,101,5,69,0,0,100,102,5,70,0,0,101,100,
        1,0,0,0,101,102,1,0,0,0,102,103,1,0,0,0,103,104,5,71,0,0,104,106,
        5,72,0,0,105,107,5,73,0,0,106,105,1,0,0,0,106,107,1,0,0,0,107,108,
        1,0,0,0,108,109,5,90,0,0,109,110,5,3,0,0,110,111,5,92,0,0,111,112,
        5,92,0,0,112,113,5,92,0,0,113,114,5,92,0,0,114,115,5,92,0,0,115,
        116,5,92,0,0,116,117,5,92,0,0,117,118,5,92,0,0,118,119,5,92,0,0,
        119,120,5,92,0,0,120,121,5,92,0,0,121,122,5,92,0,0,122,123,5,92,
        0,0,123,124,5,92,0,0,124,125,5,92,0,0,125,126,5,92,0,0,126,127,5,
        92,0,0,127,128,5,92,0,0,128,129,5,92,0,0,129,130,5,92,0,0,130,131,
        5,92,0,0,131,133,5,92,0,0,132,134,5,92,0,0,133,132,1,0,0,0,133,134,
        1,0,0,0,134,135,1,0,0,0,135,136,5,92,0,0,136,138,5,92,0,0,137,139,
        5,92,0,0,138,137,1,0,0,0,138,139,1,0,0,0,139,140,1,0,0,0,140,144,
        5,94,0,0,141,142,5,4,0,0,142,143,5,96,0,0,143,145,5,98,0,0,144,141,
        1,0,0,0,144,145,1,0,0,0,145,149,1,0,0,0,146,147,5,5,0,0,147,148,
        5,99,0,0,148,150,5,101,0,0,149,146,1,0,0,0,149,150,1,0,0,0,150,152,
        1,0,0,0,151,153,3,6,3,0,152,151,1,0,0,0,153,154,1,0,0,0,154,152,
        1,0,0,0,154,155,1,0,0,0,155,5,1,0,0,0,156,157,5,7,0,0,157,158,3,
        44,22,0,158,159,3,44,22,0,159,160,3,44,22,0,160,161,3,44,22,0,161,
        162,3,44,22,0,162,163,3,44,22,0,163,164,3,44,22,0,164,165,3,44,22,
        0,165,166,3,44,22,0,166,167,3,44,22,0,167,168,3,44,22,0,168,169,
        3,44,22,0,169,170,5,7,0,0,170,171,5,7,0,0,171,172,5,7,0,0,172,173,
        5,7,0,0,173,174,3,44,22,0,174,175,3,44,22,0,175,176,3,44,22,0,176,
        177,3,44,22,0,177,179,5,7,0,0,178,180,5,12,0,0,179,178,1,0,0,0,179,
        180,1,0,0,0,180,181,1,0,0,0,181,182,5,7,0,0,182,184,5,7,0,0,183,
        185,5,7,0,0,184,183,1,0,0,0,184,185,1,0,0,0,185,186,1,0,0,0,186,
        187,7,1,0,0,187,7,1,0,0,0,188,189,5,2,0,0,189,190,5,32,0,0,190,191,
        5,33,0,0,191,192,5,34,0,0,192,193,5,35,0,0,193,194,5,37,0,0,194,
        195,5,38,0,0,195,196,5,39,0,0,196,197,5,41,0,0,197,198,5,42,0,0,
        198,199,5,43,0,0,199,200,5,45,0,0,200,201,5,46,0,0,201,202,5,47,
        0,0,202,203,5,49,0,0,203,204,5,50,0,0,204,205,5,51,0,0,205,206,5,
        53,0,0,206,207,5,54,0,0,207,208,5,55,0,0,208,209,5,57,0,0,209,210,
        5,58,0,0,210,211,5,59,0,0,211,212,5,60,0,0,212,213,5,61,0,0,213,
        214,5,62,0,0,214,215,5,65,0,0,215,216,5,66,0,0,216,217,5,67,0,0,
        217,218,5,68,0,0,218,220,5,69,0,0,219,221,5,70,0,0,220,219,1,0,0,
        0,220,221,1,0,0,0,221,222,1,0,0,0,222,223,5,71,0,0,223,225,5,72,
        0,0,224,226,5,73,0,0,225,224,1,0,0,0,225,226,1,0,0,0,226,227,1,0,
        0,0,227,228,5,90,0,0,228,229,5,3,0,0,229,230,5,92,0,0,230,231,5,
        92,0,0,231,232,5,92,0,0,232,233,5,92,0,0,233,234,5,92,0,0,234,235,
        5,92,0,0,235,236,5,92,0,0,236,237,5,92,0,0,237,238,5,92,0,0,238,
        239,5,92,0,0,239,240,5,92,0,0,240,241,5,92,0,0,241,242,5,92,0,0,
        242,243,5,92,0,0,243,244,5,92,0,0,244,245,5,92,0,0,245,246,5,92,
        0,0,246,247,5,92,0,0,247,248,5,92,0,0,248,249,5,92,0,0,249,250,5,
        92,0,0,250,251,5,92,0,0,251,252,5,92,0,0,252,253,5,92,0,0,253,254,
        5,92,0,0,254,255,5,92,0,0,255,256,5,92,0,0,256,257,5,92,0,0,257,
        258,5,92,0,0,258,260,5,92,0,0,259,261,5,92,0,0,260,259,1,0,0,0,260,
        261,1,0,0,0,261,262,1,0,0,0,262,263,5,92,0,0,263,265,5,92,0,0,264,
        266,5,92,0,0,265,264,1,0,0,0,265,266,1,0,0,0,266,267,1,0,0,0,267,
        271,5,94,0,0,268,269,5,4,0,0,269,270,5,96,0,0,270,272,5,98,0,0,271,
        268,1,0,0,0,271,272,1,0,0,0,272,276,1,0,0,0,273,274,5,5,0,0,274,
        275,5,99,0,0,275,277,5,101,0,0,276,273,1,0,0,0,276,277,1,0,0,0,277,
        279,1,0,0,0,278,280,3,10,5,0,279,278,1,0,0,0,280,281,1,0,0,0,281,
        279,1,0,0,0,281,282,1,0,0,0,282,9,1,0,0,0,283,284,5,7,0,0,284,285,
        3,44,22,0,285,286,3,44,22,0,286,287,3,44,22,0,287,288,3,44,22,0,
        288,289,3,44,22,0,289,290,3,44,22,0,290,291,3,44,22,0,291,292,3,
        44,22,0,292,293,3,44,22,0,293,294,3,44,22,0,294,295,3,44,22,0,295,
        296,3,44,22,0,296,297,3,44,22,0,297,298,3,44,22,0,298,299,3,44,22,
        0,299,300,3,44,22,0,300,301,3,44,22,0,301,302,3,44,22,0,302,303,
        5,7,0,0,303,304,5,7,0,0,304,305,5,7,0,0,305,306,5,7,0,0,306,307,
        5,7,0,0,307,308,5,7,0,0,308,309,3,44,22,0,309,310,3,44,22,0,310,
        311,3,44,22,0,311,312,3,44,22,0,312,314,5,7,0,0,313,315,5,12,0,0,
        314,313,1,0,0,0,314,315,1,0,0,0,315,316,1,0,0,0,316,317,5,7,0,0,
        317,319,5,7,0,0,318,320,5,7,0,0,319,318,1,0,0,0,319,320,1,0,0,0,
        320,321,1,0,0,0,321,322,7,1,0,0,322,11,1,0,0,0,323,324,5,2,0,0,324,
        325,5,32,0,0,325,326,5,33,0,0,326,327,5,34,0,0,327,328,5,35,0,0,
        328,329,5,36,0,0,329,330,5,37,0,0,330,331,5,38,0,0,331,332,5,39,
        0,0,332,333,5,39,0,0,333,334,5,41,0,0,334,335,5,42,0,0,335,336,5,
        43,0,0,336,337,5,44,0,0,337,338,5,45,0,0,338,339,5,46,0,0,339,340,
        5,47,0,0,340,341,5,48,0,0,341,342,5,49,0,0,342,343,5,50,0,0,343,
        344,5,51,0,0,344,345,5,52,0,0,345,346,5,53,0,0,346,347,5,54,0,0,
        347,348,5,55,0,0,348,349,5,56,0,0,349,350,5,57,0,0,350,351,5,58,
        0,0,351,352,5,59,0,0,352,353,5,60,0,0,353,354,5,61,0,0,354,355,5,
        62,0,0,355,356,5,63,0,0,356,357,5,64,0,0,357,358,5,65,0,0,358,359,
        5,66,0,0,359,360,5,67,0,0,360,361,5,68,0,0,361,363,5,69,0,0,362,
        364,5,70,0,0,363,362,1,0,0,0,363,364,1,0,0,0,364,365,1,0,0,0,365,
        366,5,71,0,0,366,368,5,72,0,0,367,369,5,73,0,0,368,367,1,0,0,0,368,
        369,1,0,0,0,369,370,1,0,0,0,370,371,5,90,0,0,371,372,5,3,0,0,372,
        373,5,92,0,0,373,374,5,92,0,0,374,375,5,92,0,0,375,376,5,92,0,0,
        376,377,5,92,0,0,377,378,5,92,0,0,378,379,5,92,0,0,379,380,5,92,
        0,0,380,381,5,92,0,0,381,382,5,92,0,0,382,383,5,92,0,0,383,384,5,
        92,0,0,384,385,5,92,0,0,385,386,5,92,0,0,386,387,5,92,0,0,387,388,
        5,92,0,0,388,389,5,92,0,0,389,390,5,92,0,0,390,391,5,92,0,0,391,
        392,5,92,0,0,392,393,5,92,0,0,393,394,5,92,0,0,394,395,5,92,0,0,
        395,396,5,92,0,0,396,397,5,92,0,0,397,398,5,92,0,0,398,399,5,92,
        0,0,399,400,5,92,0,0,400,401,5,92,0,0,401,402,5,92,0,0,402,403,5,
        92,0,0,403,404,5,92,0,0,404,405,5,92,0,0,405,406,5,92,0,0,406,407,
        5,92,0,0,407,408,5,92,0,0,408,409,5,92,0,0,409,411,5,92,0,0,410,
        412,5,92,0,0,411,410,1,0,0,0,411,412,1,0,0,0,412,413,1,0,0,0,413,
        414,5,92,0,0,414,416,5,92,0,0,415,417,5,92,0,0,416,415,1,0,0,0,416,
        417,1,0,0,0,417,418,1,0,0,0,418,422,5,94,0,0,419,420,5,4,0,0,420,
        421,5,96,0,0,421,423,5,98,0,0,422,419,1,0,0,0,422,423,1,0,0,0,423,
        427,1,0,0,0,424,425,5,5,0,0,425,426,5,99,0,0,426,428,5,101,0,0,427,
        424,1,0,0,0,427,428,1,0,0,0,428,430,1,0,0,0,429,431,3,14,7,0,430,
        429,1,0,0,0,431,432,1,0,0,0,432,430,1,0,0,0,432,433,1,0,0,0,433,
        13,1,0,0,0,434,435,5,7,0,0,435,436,3,44,22,0,436,437,3,44,22,0,437,
        438,3,44,22,0,438,439,3,44,22,0,439,440,3,44,22,0,440,441,3,44,22,
        0,441,442,3,44,22,0,442,443,3,44,22,0,443,444,3,44,22,0,444,445,
        3,44,22,0,445,446,3,44,22,0,446,447,3,44,22,0,447,448,3,44,22,0,
        448,449,3,44,22,0,449,450,3,44,22,0,450,451,3,44,22,0,451,452,3,
        44,22,0,452,453,3,44,22,0,453,454,3,44,22,0,454,455,3,44,22,0,455,
        456,3,44,22,0,456,457,3,44,22,0,457,458,3,44,22,0,458,459,3,44,22,
        0,459,460,5,7,0,0,460,461,5,7,0,0,461,462,5,7,0,0,462,463,5,7,0,
        0,463,464,5,7,0,0,464,465,5,7,0,0,465,466,5,7,0,0,466,467,5,7,0,
        0,467,468,3,44,22,0,468,469,3,44,22,0,469,470,3,44,22,0,470,471,
        3,44,22,0,471,473,5,7,0,0,472,474,5,12,0,0,473,472,1,0,0,0,473,474,
        1,0,0,0,474,475,1,0,0,0,475,476,5,7,0,0,476,478,5,7,0,0,477,479,
        5,7,0,0,478,477,1,0,0,0,478,479,1,0,0,0,479,480,1,0,0,0,480,481,
        7,1,0,0,481,15,1,0,0,0,482,483,5,1,0,0,483,484,5,22,0,0,484,485,
        5,25,0,0,485,487,5,30,0,0,486,488,3,18,9,0,487,486,1,0,0,0,488,489,
        1,0,0,0,489,487,1,0,0,0,489,490,1,0,0,0,490,17,1,0,0,0,491,492,5,
        1,0,0,492,493,7,0,0,0,493,494,5,25,0,0,494,495,5,26,0,0,495,496,
        5,26,0,0,496,497,5,26,0,0,497,498,7,2,0,0,498,499,5,26,0,0,499,500,
        5,30,0,0,500,19,1,0,0,0,501,503,5,3,0,0,502,504,5,92,0,0,503,502,
        1,0,0,0,504,505,1,0,0,0,505,503,1,0,0,0,505,506,1,0,0,0,506,507,
        1,0,0,0,507,508,5,94,0,0,508,509,5,2,0,0,509,510,5,74,0,0,510,511,
        5,77,0,0,511,512,5,78,0,0,512,516,5,81,0,0,513,517,5,82,0,0,514,
        515,5,83,0,0,515,517,5,84,0,0,516,513,1,0,0,0,516,514,1,0,0,0,516,
        517,1,0,0,0,517,518,1,0,0,0,518,520,5,90,0,0,519,521,3,22,11,0,520,
        519,1,0,0,0,521,522,1,0,0,0,522,520,1,0,0,0,522,523,1,0,0,0,523,
        21,1,0,0,0,524,525,5,7,0,0,525,526,3,44,22,0,526,528,3,44,22,0,527,
        529,3,44,22,0,528,527,1,0,0,0,529,530,1,0,0,0,530,528,1,0,0,0,530,
        531,1,0,0,0,531,532,1,0,0,0,532,533,7,1,0,0,533,23,1,0,0,0,534,536,
        5,3,0,0,535,537,5,92,0,0,536,535,1,0,0,0,537,538,1,0,0,0,538,536,
        1,0,0,0,538,539,1,0,0,0,539,540,1,0,0,0,540,541,5,94,0,0,541,542,
        5,2,0,0,542,544,5,74,0,0,543,545,5,75,0,0,544,543,1,0,0,0,544,545,
        1,0,0,0,545,546,1,0,0,0,546,547,5,77,0,0,547,548,5,78,0,0,548,549,
        5,79,0,0,549,553,5,81,0,0,550,554,5,82,0,0,551,552,5,83,0,0,552,
        554,5,84,0,0,553,550,1,0,0,0,553,551,1,0,0,0,553,554,1,0,0,0,554,
        555,1,0,0,0,555,557,5,90,0,0,556,558,3,26,13,0,557,556,1,0,0,0,558,
        559,1,0,0,0,559,557,1,0,0,0,559,560,1,0,0,0,560,25,1,0,0,0,561,563,
        5,7,0,0,562,564,5,7,0,0,563,562,1,0,0,0,563,564,1,0,0,0,564,565,
        1,0,0,0,565,566,3,44,22,0,566,567,3,44,22,0,567,569,3,44,22,0,568,
        570,3,44,22,0,569,568,1,0,0,0,570,571,1,0,0,0,571,569,1,0,0,0,571,
        572,1,0,0,0,572,573,1,0,0,0,573,574,7,1,0,0,574,27,1,0,0,0,575,577,
        5,3,0,0,576,578,5,92,0,0,577,576,1,0,0,0,578,579,1,0,0,0,579,577,
        1,0,0,0,579,580,1,0,0,0,580,581,1,0,0,0,581,582,5,94,0,0,582,583,
        5,2,0,0,583,585,5,74,0,0,584,586,5,76,0,0,585,584,1,0,0,0,585,586,
        1,0,0,0,586,588,1,0,0,0,587,589,5,75,0,0,588,587,1,0,0,0,588,589,
        1,0,0,0,589,590,1,0,0,0,590,591,5,77,0,0,591,592,5,78,0,0,592,593,
        5,79,0,0,593,594,5,80,0,0,594,598,5,81,0,0,595,599,5,82,0,0,596,
        597,5,83,0,0,597,599,5,84,0,0,598,595,1,0,0,0,598,596,1,0,0,0,598,
        599,1,0,0,0,599,600,1,0,0,0,600,602,5,90,0,0,601,603,3,30,15,0,602,
        601,1,0,0,0,603,604,1,0,0,0,604,602,1,0,0,0,604,605,1,0,0,0,605,
        29,1,0,0,0,606,608,5,7,0,0,607,609,5,7,0,0,608,607,1,0,0,0,608,609,
        1,0,0,0,609,611,1,0,0,0,610,612,5,7,0,0,611,610,1,0,0,0,611,612,
        1,0,0,0,612,613,1,0,0,0,613,614,3,44,22,0,614,615,3,44,22,0,615,
        616,3,44,22,0,616,618,3,44,22,0,617,619,3,44,22,0,618,617,1,0,0,
        0,619,620,1,0,0,0,620,618,1,0,0,0,620,621,1,0,0,0,621,622,1,0,0,
        0,622,623,7,1,0,0,623,31,1,0,0,0,624,626,3,34,17,0,625,624,1,0,0,
        0,626,627,1,0,0,0,627,625,1,0,0,0,627,628,1,0,0,0,628,33,1,0,0,0,
        629,630,5,6,0,0,630,631,5,111,0,0,631,632,5,105,0,0,632,633,5,111,
        0,0,633,634,5,106,0,0,634,635,5,107,0,0,635,636,5,110,0,0,636,643,
        5,106,0,0,637,644,5,113,0,0,638,639,5,103,0,0,639,640,5,111,0,0,
        640,641,5,105,0,0,641,642,5,111,0,0,642,644,5,104,0,0,643,637,1,
        0,0,0,643,638,1,0,0,0,644,645,1,0,0,0,645,646,5,109,0,0,646,647,
        5,112,0,0,647,648,5,106,0,0,648,649,5,108,0,0,649,650,5,110,0,0,
        650,651,5,106,0,0,651,652,5,102,0,0,652,653,7,3,0,0,653,35,1,0,0,
        0,654,656,3,38,19,0,655,654,1,0,0,0,656,657,1,0,0,0,657,655,1,0,
        0,0,657,658,1,0,0,0,658,37,1,0,0,0,659,660,5,6,0,0,660,661,5,111,
        0,0,661,662,5,105,0,0,662,663,5,111,0,0,663,664,5,105,0,0,664,665,
        5,111,0,0,665,666,5,106,0,0,666,667,5,107,0,0,667,668,5,110,0,0,
        668,677,5,106,0,0,669,678,5,113,0,0,670,671,5,103,0,0,671,672,5,
        111,0,0,672,673,5,105,0,0,673,674,5,111,0,0,674,675,5,105,0,0,675,
        676,5,111,0,0,676,678,5,104,0,0,677,669,1,0,0,0,677,670,1,0,0,0,
        678,679,1,0,0,0,679,680,5,109,0,0,680,681,5,112,0,0,681,682,5,106,
        0,0,682,683,5,108,0,0,683,684,5,110,0,0,684,685,5,106,0,0,685,686,
        5,102,0,0,686,687,7,3,0,0,687,39,1,0,0,0,688,690,3,42,21,0,689,688,
        1,0,0,0,690,691,1,0,0,0,691,689,1,0,0,0,691,692,1,0,0,0,692,41,1,
        0,0,0,693,694,5,6,0,0,694,695,5,111,0,0,695,696,5,105,0,0,696,697,
        5,111,0,0,697,698,5,105,0,0,698,699,5,111,0,0,699,700,5,105,0,0,
        700,701,5,111,0,0,701,702,5,106,0,0,702,703,5,107,0,0,703,704,5,
        110,0,0,704,715,5,106,0,0,705,716,5,113,0,0,706,707,5,103,0,0,707,
        708,5,111,0,0,708,709,5,105,0,0,709,710,5,111,0,0,710,711,5,105,
        0,0,711,712,5,111,0,0,712,713,5,105,0,0,713,714,5,111,0,0,714,716,
        5,104,0,0,715,705,1,0,0,0,715,706,1,0,0,0,716,717,1,0,0,0,717,718,
        5,109,0,0,718,719,5,112,0,0,719,720,5,106,0,0,720,721,5,108,0,0,
        721,722,5,110,0,0,722,723,5,106,0,0,723,724,5,102,0,0,724,725,7,
        3,0,0,725,43,1,0,0,0,726,727,7,4,0,0,727,45,1,0,0,0,55,47,61,63,
        101,106,133,138,144,149,154,179,184,220,225,260,265,271,276,281,
        314,319,363,368,411,416,422,427,432,473,478,489,505,516,522,530,
        538,544,553,559,563,571,579,585,588,598,604,608,611,620,627,643,
        657,677,691,715
    ]

class NmrPipePKParser ( Parser ):

    grammarFileName = "NmrPipePKParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'DATA'", "'VARS'", "'FORMAT'", "'NULLVALUE'", 
                     "'NULLSTRING'", "'('", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'DIMCOUNT'", "'PPM'", "'HZ'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'INDEX'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'DX'", "'DY'", "'DZ'", "'DA'", "'X_PPM'", 
                     "'Y_PPM'", "'Z_PPM'", "'A_PPM'", "'X_HZ'", "'Y_HZ'", 
                     "'Z_HZ'", "'A_HZ'", "'XW'", "'YW'", "'ZW'", "'AW'", 
                     "'XW_HZ'", "'YW_HZ'", "'ZW_HZ'", "'AW_HZ'", "'X1'", 
                     "'X3'", "'Y1'", "'Y3'", "'Z1'", "'Z3'", "'A1'", "'A3'", 
                     "'HEIGHT'", "'DHEIGHT'", "'VOL'", "'PCHI2'", "'TYPE'", 
                     "'ASS'", "'CLUSTID'", "'MEMCNT'", "'TROUBLE'", "'PkID'", 
                     "'Sl.Z'", "'Sl.A'", "'X'", "'Y'", "'Z'", "'A'", "'Intensity'", 
                     "'Assign'", "'Assign1'", "'Assign2'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "')'", "'['", "']'", "','", "';'", "'#'", "'%'", "'^'" ]

    symbolicNames = [ "<INVALID>", "Data", "Vars", "Format", "Null_value", 
                      "Null_string", "L_paren", "Integer", "Float", "Real", 
                      "SHARP_COMMENT", "EXCLM_COMMENT", "Any_name", "SPACE", 
                      "RETURN", "SECTION_COMMENT", "LINE_COMMENT", "X_axis_DA", 
                      "Y_axis_DA", "Z_axis_DA", "A_axis_DA", "Ppm_value_DA", 
                      "Dim_count_DA", "Ppm_DA", "Hz_DA", "Integer_DA", "Float_DA", 
                      "Real_DA", "Simple_name_DA", "SPACE_DA", "RETURN_DA", 
                      "LINE_COMMENT_DA", "Index", "X_axis", "Y_axis", "Z_axis", 
                      "A_axis", "Dx", "Dy", "Dz", "Da", "X_ppm", "Y_ppm", 
                      "Z_ppm", "A_ppm", "X_hz", "Y_hz", "Z_hz", "A_hz", 
                      "Xw", "Yw", "Zw", "Aw", "Xw_hz", "Yw_hz", "Zw_hz", 
                      "Aw_hz", "X1", "X3", "Y1", "Y3", "Z1", "Z3", "A1", 
                      "A3", "Height", "DHeight", "Vol", "Pchi2", "Type", 
                      "Ass", "ClustId", "Memcnt", "Trouble", "PkID", "Sl_Z", 
                      "Sl_A", "X", "Y", "Z", "A", "Intensity", "Assign", 
                      "Assign1", "Assign2", "Integer_VA", "Float_VA", "Real_VA", 
                      "Simple_name_VA", "SPACE_VA", "RETURN_VA", "LINE_COMMENT_VA", 
                      "Format_code", "SPACE_FO", "RETURN_FO", "LINE_COMMENT_FO", 
                      "Any_name_NV", "SPACE_NV", "RETURN_NV", "Any_name_NS", 
                      "SPACE_NS", "RETURN_NS", "R_paren", "L_brkt", "R_brkt", 
                      "Comma", "Semicolon", "Number_sign", "Percent_sign", 
                      "Caret", "Integer_PR", "Float_PR", "Real_PR", "Assignments_PR", 
                      "SPACE_PR", "RETURN_PR" ]

    RULE_nmrpipe_pk = 0
    RULE_data_label = 1
    RULE_peak_list_2d = 2
    RULE_peak_2d = 3
    RULE_peak_list_3d = 4
    RULE_peak_3d = 5
    RULE_peak_list_4d = 6
    RULE_peak_4d = 7
    RULE_pipp_label = 8
    RULE_pipp_axis = 9
    RULE_pipp_peak_list_2d = 10
    RULE_pipp_peak_2d = 11
    RULE_pipp_peak_list_3d = 12
    RULE_pipp_peak_3d = 13
    RULE_pipp_peak_list_4d = 14
    RULE_pipp_peak_4d = 15
    RULE_pipp_row_peak_list_2d = 16
    RULE_pipp_row_peak_2d = 17
    RULE_pipp_row_peak_list_3d = 18
    RULE_pipp_row_peak_3d = 19
    RULE_pipp_row_peak_list_4d = 20
    RULE_pipp_row_peak_4d = 21
    RULE_number = 22

    ruleNames =  [ "nmrpipe_pk", "data_label", "peak_list_2d", "peak_2d", 
                   "peak_list_3d", "peak_3d", "peak_list_4d", "peak_4d", 
                   "pipp_label", "pipp_axis", "pipp_peak_list_2d", "pipp_peak_2d", 
                   "pipp_peak_list_3d", "pipp_peak_3d", "pipp_peak_list_4d", 
                   "pipp_peak_4d", "pipp_row_peak_list_2d", "pipp_row_peak_2d", 
                   "pipp_row_peak_list_3d", "pipp_row_peak_3d", "pipp_row_peak_list_4d", 
                   "pipp_row_peak_4d", "number" ]

    EOF = Token.EOF
    Data=1
    Vars=2
    Format=3
    Null_value=4
    Null_string=5
    L_paren=6
    Integer=7
    Float=8
    Real=9
    SHARP_COMMENT=10
    EXCLM_COMMENT=11
    Any_name=12
    SPACE=13
    RETURN=14
    SECTION_COMMENT=15
    LINE_COMMENT=16
    X_axis_DA=17
    Y_axis_DA=18
    Z_axis_DA=19
    A_axis_DA=20
    Ppm_value_DA=21
    Dim_count_DA=22
    Ppm_DA=23
    Hz_DA=24
    Integer_DA=25
    Float_DA=26
    Real_DA=27
    Simple_name_DA=28
    SPACE_DA=29
    RETURN_DA=30
    LINE_COMMENT_DA=31
    Index=32
    X_axis=33
    Y_axis=34
    Z_axis=35
    A_axis=36
    Dx=37
    Dy=38
    Dz=39
    Da=40
    X_ppm=41
    Y_ppm=42
    Z_ppm=43
    A_ppm=44
    X_hz=45
    Y_hz=46
    Z_hz=47
    A_hz=48
    Xw=49
    Yw=50
    Zw=51
    Aw=52
    Xw_hz=53
    Yw_hz=54
    Zw_hz=55
    Aw_hz=56
    X1=57
    X3=58
    Y1=59
    Y3=60
    Z1=61
    Z3=62
    A1=63
    A3=64
    Height=65
    DHeight=66
    Vol=67
    Pchi2=68
    Type=69
    Ass=70
    ClustId=71
    Memcnt=72
    Trouble=73
    PkID=74
    Sl_Z=75
    Sl_A=76
    X=77
    Y=78
    Z=79
    A=80
    Intensity=81
    Assign=82
    Assign1=83
    Assign2=84
    Integer_VA=85
    Float_VA=86
    Real_VA=87
    Simple_name_VA=88
    SPACE_VA=89
    RETURN_VA=90
    LINE_COMMENT_VA=91
    Format_code=92
    SPACE_FO=93
    RETURN_FO=94
    LINE_COMMENT_FO=95
    Any_name_NV=96
    SPACE_NV=97
    RETURN_NV=98
    Any_name_NS=99
    SPACE_NS=100
    RETURN_NS=101
    R_paren=102
    L_brkt=103
    R_brkt=104
    Comma=105
    Semicolon=106
    Number_sign=107
    Percent_sign=108
    Caret=109
    Integer_PR=110
    Float_PR=111
    Real_PR=112
    Assignments_PR=113
    SPACE_PR=114
    RETURN_PR=115

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Nmrpipe_pkContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def RETURN(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.RETURN)
            else:
                return self.getToken(NmrPipePKParser.RETURN, i)

        def data_label(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Data_labelContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Data_labelContext,i)


        def peak_list_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_list_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_list_2dContext,i)


        def peak_list_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_list_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_list_3dContext,i)


        def peak_list_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_list_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_list_4dContext,i)


        def pipp_label(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_labelContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_labelContext,i)


        def pipp_peak_list_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_list_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_list_2dContext,i)


        def pipp_peak_list_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_list_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_list_3dContext,i)


        def pipp_peak_list_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_list_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_list_4dContext,i)


        def pipp_row_peak_list_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_list_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_list_2dContext,i)


        def pipp_row_peak_list_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_list_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_list_3dContext,i)


        def pipp_row_peak_list_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_list_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_list_4dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_nmrpipe_pk

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNmrpipe_pk" ):
                listener.enterNmrpipe_pk(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNmrpipe_pk" ):
                listener.exitNmrpipe_pk(self)




    def nmrpipe_pk(self):

        localctx = NmrPipePKParser.Nmrpipe_pkContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_nmrpipe_pk)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 46
                self.match(NmrPipePKParser.RETURN)


            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 16462) != 0):
                self.state = 61
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 49
                    self.data_label()
                    pass

                elif la_ == 2:
                    self.state = 50
                    self.peak_list_2d()
                    pass

                elif la_ == 3:
                    self.state = 51
                    self.peak_list_3d()
                    pass

                elif la_ == 4:
                    self.state = 52
                    self.peak_list_4d()
                    pass

                elif la_ == 5:
                    self.state = 53
                    self.pipp_label()
                    pass

                elif la_ == 6:
                    self.state = 54
                    self.pipp_peak_list_2d()
                    pass

                elif la_ == 7:
                    self.state = 55
                    self.pipp_peak_list_3d()
                    pass

                elif la_ == 8:
                    self.state = 56
                    self.pipp_peak_list_4d()
                    pass

                elif la_ == 9:
                    self.state = 57
                    self.pipp_row_peak_list_2d()
                    pass

                elif la_ == 10:
                    self.state = 58
                    self.pipp_row_peak_list_3d()
                    pass

                elif la_ == 11:
                    self.state = 59
                    self.pipp_row_peak_list_4d()
                    pass

                elif la_ == 12:
                    self.state = 60
                    self.match(NmrPipePKParser.RETURN)
                    pass


                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 66
            self.match(NmrPipePKParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Data_labelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Data(self):
            return self.getToken(NmrPipePKParser.Data, 0)

        def Simple_name_DA(self):
            return self.getToken(NmrPipePKParser.Simple_name_DA, 0)

        def Integer_DA(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer_DA)
            else:
                return self.getToken(NmrPipePKParser.Integer_DA, i)

        def Ppm_value_DA(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Ppm_value_DA)
            else:
                return self.getToken(NmrPipePKParser.Ppm_value_DA, i)

        def RETURN_DA(self):
            return self.getToken(NmrPipePKParser.RETURN_DA, 0)

        def X_axis_DA(self):
            return self.getToken(NmrPipePKParser.X_axis_DA, 0)

        def Y_axis_DA(self):
            return self.getToken(NmrPipePKParser.Y_axis_DA, 0)

        def Z_axis_DA(self):
            return self.getToken(NmrPipePKParser.Z_axis_DA, 0)

        def A_axis_DA(self):
            return self.getToken(NmrPipePKParser.A_axis_DA, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_data_label

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterData_label" ):
                listener.enterData_label(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitData_label" ):
                listener.exitData_label(self)




    def data_label(self):

        localctx = NmrPipePKParser.Data_labelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_data_label)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(NmrPipePKParser.Data)
            self.state = 69
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1966080) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 70
            self.match(NmrPipePKParser.Simple_name_DA)
            self.state = 71
            self.match(NmrPipePKParser.Integer_DA)
            self.state = 72
            self.match(NmrPipePKParser.Integer_DA)
            self.state = 73
            self.match(NmrPipePKParser.Ppm_value_DA)
            self.state = 74
            self.match(NmrPipePKParser.Ppm_value_DA)
            self.state = 75
            self.match(NmrPipePKParser.RETURN_DA)
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

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def Index(self):
            return self.getToken(NmrPipePKParser.Index, 0)

        def X_axis(self):
            return self.getToken(NmrPipePKParser.X_axis, 0)

        def Y_axis(self):
            return self.getToken(NmrPipePKParser.Y_axis, 0)

        def Dx(self):
            return self.getToken(NmrPipePKParser.Dx, 0)

        def Dy(self):
            return self.getToken(NmrPipePKParser.Dy, 0)

        def X_ppm(self):
            return self.getToken(NmrPipePKParser.X_ppm, 0)

        def Y_ppm(self):
            return self.getToken(NmrPipePKParser.Y_ppm, 0)

        def X_hz(self):
            return self.getToken(NmrPipePKParser.X_hz, 0)

        def Y_hz(self):
            return self.getToken(NmrPipePKParser.Y_hz, 0)

        def Xw(self):
            return self.getToken(NmrPipePKParser.Xw, 0)

        def Yw(self):
            return self.getToken(NmrPipePKParser.Yw, 0)

        def Xw_hz(self):
            return self.getToken(NmrPipePKParser.Xw_hz, 0)

        def Yw_hz(self):
            return self.getToken(NmrPipePKParser.Yw_hz, 0)

        def X1(self):
            return self.getToken(NmrPipePKParser.X1, 0)

        def X3(self):
            return self.getToken(NmrPipePKParser.X3, 0)

        def Y1(self):
            return self.getToken(NmrPipePKParser.Y1, 0)

        def Y3(self):
            return self.getToken(NmrPipePKParser.Y3, 0)

        def Height(self):
            return self.getToken(NmrPipePKParser.Height, 0)

        def DHeight(self):
            return self.getToken(NmrPipePKParser.DHeight, 0)

        def Vol(self):
            return self.getToken(NmrPipePKParser.Vol, 0)

        def Pchi2(self):
            return self.getToken(NmrPipePKParser.Pchi2, 0)

        def Type(self):
            return self.getToken(NmrPipePKParser.Type, 0)

        def ClustId(self):
            return self.getToken(NmrPipePKParser.ClustId, 0)

        def Memcnt(self):
            return self.getToken(NmrPipePKParser.Memcnt, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Ass(self):
            return self.getToken(NmrPipePKParser.Ass, 0)

        def Trouble(self):
            return self.getToken(NmrPipePKParser.Trouble, 0)

        def Null_value(self):
            return self.getToken(NmrPipePKParser.Null_value, 0)

        def Any_name_NV(self):
            return self.getToken(NmrPipePKParser.Any_name_NV, 0)

        def RETURN_NV(self):
            return self.getToken(NmrPipePKParser.RETURN_NV, 0)

        def Null_string(self):
            return self.getToken(NmrPipePKParser.Null_string, 0)

        def Any_name_NS(self):
            return self.getToken(NmrPipePKParser.Any_name_NS, 0)

        def RETURN_NS(self):
            return self.getToken(NmrPipePKParser.RETURN_NS, 0)

        def peak_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_2dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_list_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_2d" ):
                listener.enterPeak_list_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_2d" ):
                listener.exitPeak_list_2d(self)




    def peak_list_2d(self):

        localctx = NmrPipePKParser.Peak_list_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_peak_list_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(NmrPipePKParser.Vars)
            self.state = 78
            self.match(NmrPipePKParser.Index)
            self.state = 79
            self.match(NmrPipePKParser.X_axis)
            self.state = 80
            self.match(NmrPipePKParser.Y_axis)
            self.state = 81
            self.match(NmrPipePKParser.Dx)
            self.state = 82
            self.match(NmrPipePKParser.Dy)
            self.state = 83
            self.match(NmrPipePKParser.X_ppm)
            self.state = 84
            self.match(NmrPipePKParser.Y_ppm)
            self.state = 85
            self.match(NmrPipePKParser.X_hz)
            self.state = 86
            self.match(NmrPipePKParser.Y_hz)
            self.state = 87
            self.match(NmrPipePKParser.Xw)
            self.state = 88
            self.match(NmrPipePKParser.Yw)
            self.state = 89
            self.match(NmrPipePKParser.Xw_hz)
            self.state = 90
            self.match(NmrPipePKParser.Yw_hz)
            self.state = 91
            self.match(NmrPipePKParser.X1)
            self.state = 92
            self.match(NmrPipePKParser.X3)
            self.state = 93
            self.match(NmrPipePKParser.Y1)
            self.state = 94
            self.match(NmrPipePKParser.Y3)
            self.state = 95
            self.match(NmrPipePKParser.Height)
            self.state = 96
            self.match(NmrPipePKParser.DHeight)
            self.state = 97
            self.match(NmrPipePKParser.Vol)
            self.state = 98
            self.match(NmrPipePKParser.Pchi2)
            self.state = 99
            self.match(NmrPipePKParser.Type)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==70:
                self.state = 100
                self.match(NmrPipePKParser.Ass)


            self.state = 103
            self.match(NmrPipePKParser.ClustId)
            self.state = 104
            self.match(NmrPipePKParser.Memcnt)
            self.state = 106
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==73:
                self.state = 105
                self.match(NmrPipePKParser.Trouble)


            self.state = 108
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 109
            self.match(NmrPipePKParser.Format)
            self.state = 110
            self.match(NmrPipePKParser.Format_code)
            self.state = 111
            self.match(NmrPipePKParser.Format_code)
            self.state = 112
            self.match(NmrPipePKParser.Format_code)
            self.state = 113
            self.match(NmrPipePKParser.Format_code)
            self.state = 114
            self.match(NmrPipePKParser.Format_code)
            self.state = 115
            self.match(NmrPipePKParser.Format_code)
            self.state = 116
            self.match(NmrPipePKParser.Format_code)
            self.state = 117
            self.match(NmrPipePKParser.Format_code)
            self.state = 118
            self.match(NmrPipePKParser.Format_code)
            self.state = 119
            self.match(NmrPipePKParser.Format_code)
            self.state = 120
            self.match(NmrPipePKParser.Format_code)
            self.state = 121
            self.match(NmrPipePKParser.Format_code)
            self.state = 122
            self.match(NmrPipePKParser.Format_code)
            self.state = 123
            self.match(NmrPipePKParser.Format_code)
            self.state = 124
            self.match(NmrPipePKParser.Format_code)
            self.state = 125
            self.match(NmrPipePKParser.Format_code)
            self.state = 126
            self.match(NmrPipePKParser.Format_code)
            self.state = 127
            self.match(NmrPipePKParser.Format_code)
            self.state = 128
            self.match(NmrPipePKParser.Format_code)
            self.state = 129
            self.match(NmrPipePKParser.Format_code)
            self.state = 130
            self.match(NmrPipePKParser.Format_code)
            self.state = 131
            self.match(NmrPipePKParser.Format_code)
            self.state = 133
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 132
                self.match(NmrPipePKParser.Format_code)


            self.state = 135
            self.match(NmrPipePKParser.Format_code)
            self.state = 136
            self.match(NmrPipePKParser.Format_code)
            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==92:
                self.state = 137
                self.match(NmrPipePKParser.Format_code)


            self.state = 140
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 141
                self.match(NmrPipePKParser.Null_value)
                self.state = 142
                self.match(NmrPipePKParser.Any_name_NV)
                self.state = 143
                self.match(NmrPipePKParser.RETURN_NV)


            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 146
                self.match(NmrPipePKParser.Null_string)
                self.state = 147
                self.match(NmrPipePKParser.Any_name_NS)
                self.state = 148
                self.match(NmrPipePKParser.RETURN_NS)


            self.state = 152 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 151
                self.peak_2d()
                self.state = 154 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

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
                return self.getTokens(NmrPipePKParser.Integer)
            else:
                return self.getToken(NmrPipePKParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Any_name(self):
            return self.getToken(NmrPipePKParser.Any_name, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_2d" ):
                listener.enterPeak_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_2d" ):
                listener.exitPeak_2d(self)




    def peak_2d(self):

        localctx = NmrPipePKParser.Peak_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_peak_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(NmrPipePKParser.Integer)
            self.state = 157
            self.number()
            self.state = 158
            self.number()
            self.state = 159
            self.number()
            self.state = 160
            self.number()
            self.state = 161
            self.number()
            self.state = 162
            self.number()
            self.state = 163
            self.number()
            self.state = 164
            self.number()
            self.state = 165
            self.number()
            self.state = 166
            self.number()
            self.state = 167
            self.number()
            self.state = 168
            self.number()
            self.state = 169
            self.match(NmrPipePKParser.Integer)
            self.state = 170
            self.match(NmrPipePKParser.Integer)
            self.state = 171
            self.match(NmrPipePKParser.Integer)
            self.state = 172
            self.match(NmrPipePKParser.Integer)
            self.state = 173
            self.number()
            self.state = 174
            self.number()
            self.state = 175
            self.number()
            self.state = 176
            self.number()
            self.state = 177
            self.match(NmrPipePKParser.Integer)
            self.state = 179
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 178
                self.match(NmrPipePKParser.Any_name)


            self.state = 181
            self.match(NmrPipePKParser.Integer)
            self.state = 182
            self.match(NmrPipePKParser.Integer)
            self.state = 184
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 183
                self.match(NmrPipePKParser.Integer)


            self.state = 186
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Peak_list_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def Index(self):
            return self.getToken(NmrPipePKParser.Index, 0)

        def X_axis(self):
            return self.getToken(NmrPipePKParser.X_axis, 0)

        def Y_axis(self):
            return self.getToken(NmrPipePKParser.Y_axis, 0)

        def Z_axis(self):
            return self.getToken(NmrPipePKParser.Z_axis, 0)

        def Dx(self):
            return self.getToken(NmrPipePKParser.Dx, 0)

        def Dy(self):
            return self.getToken(NmrPipePKParser.Dy, 0)

        def Dz(self):
            return self.getToken(NmrPipePKParser.Dz, 0)

        def X_ppm(self):
            return self.getToken(NmrPipePKParser.X_ppm, 0)

        def Y_ppm(self):
            return self.getToken(NmrPipePKParser.Y_ppm, 0)

        def Z_ppm(self):
            return self.getToken(NmrPipePKParser.Z_ppm, 0)

        def X_hz(self):
            return self.getToken(NmrPipePKParser.X_hz, 0)

        def Y_hz(self):
            return self.getToken(NmrPipePKParser.Y_hz, 0)

        def Z_hz(self):
            return self.getToken(NmrPipePKParser.Z_hz, 0)

        def Xw(self):
            return self.getToken(NmrPipePKParser.Xw, 0)

        def Yw(self):
            return self.getToken(NmrPipePKParser.Yw, 0)

        def Zw(self):
            return self.getToken(NmrPipePKParser.Zw, 0)

        def Xw_hz(self):
            return self.getToken(NmrPipePKParser.Xw_hz, 0)

        def Yw_hz(self):
            return self.getToken(NmrPipePKParser.Yw_hz, 0)

        def Zw_hz(self):
            return self.getToken(NmrPipePKParser.Zw_hz, 0)

        def X1(self):
            return self.getToken(NmrPipePKParser.X1, 0)

        def X3(self):
            return self.getToken(NmrPipePKParser.X3, 0)

        def Y1(self):
            return self.getToken(NmrPipePKParser.Y1, 0)

        def Y3(self):
            return self.getToken(NmrPipePKParser.Y3, 0)

        def Z1(self):
            return self.getToken(NmrPipePKParser.Z1, 0)

        def Z3(self):
            return self.getToken(NmrPipePKParser.Z3, 0)

        def Height(self):
            return self.getToken(NmrPipePKParser.Height, 0)

        def DHeight(self):
            return self.getToken(NmrPipePKParser.DHeight, 0)

        def Vol(self):
            return self.getToken(NmrPipePKParser.Vol, 0)

        def Pchi2(self):
            return self.getToken(NmrPipePKParser.Pchi2, 0)

        def Type(self):
            return self.getToken(NmrPipePKParser.Type, 0)

        def ClustId(self):
            return self.getToken(NmrPipePKParser.ClustId, 0)

        def Memcnt(self):
            return self.getToken(NmrPipePKParser.Memcnt, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Ass(self):
            return self.getToken(NmrPipePKParser.Ass, 0)

        def Trouble(self):
            return self.getToken(NmrPipePKParser.Trouble, 0)

        def Null_value(self):
            return self.getToken(NmrPipePKParser.Null_value, 0)

        def Any_name_NV(self):
            return self.getToken(NmrPipePKParser.Any_name_NV, 0)

        def RETURN_NV(self):
            return self.getToken(NmrPipePKParser.RETURN_NV, 0)

        def Null_string(self):
            return self.getToken(NmrPipePKParser.Null_string, 0)

        def Any_name_NS(self):
            return self.getToken(NmrPipePKParser.Any_name_NS, 0)

        def RETURN_NS(self):
            return self.getToken(NmrPipePKParser.RETURN_NS, 0)

        def peak_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_3dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_list_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_3d" ):
                listener.enterPeak_list_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_3d" ):
                listener.exitPeak_list_3d(self)




    def peak_list_3d(self):

        localctx = NmrPipePKParser.Peak_list_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_peak_list_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(NmrPipePKParser.Vars)
            self.state = 189
            self.match(NmrPipePKParser.Index)
            self.state = 190
            self.match(NmrPipePKParser.X_axis)
            self.state = 191
            self.match(NmrPipePKParser.Y_axis)
            self.state = 192
            self.match(NmrPipePKParser.Z_axis)
            self.state = 193
            self.match(NmrPipePKParser.Dx)
            self.state = 194
            self.match(NmrPipePKParser.Dy)
            self.state = 195
            self.match(NmrPipePKParser.Dz)
            self.state = 196
            self.match(NmrPipePKParser.X_ppm)
            self.state = 197
            self.match(NmrPipePKParser.Y_ppm)
            self.state = 198
            self.match(NmrPipePKParser.Z_ppm)
            self.state = 199
            self.match(NmrPipePKParser.X_hz)
            self.state = 200
            self.match(NmrPipePKParser.Y_hz)
            self.state = 201
            self.match(NmrPipePKParser.Z_hz)
            self.state = 202
            self.match(NmrPipePKParser.Xw)
            self.state = 203
            self.match(NmrPipePKParser.Yw)
            self.state = 204
            self.match(NmrPipePKParser.Zw)
            self.state = 205
            self.match(NmrPipePKParser.Xw_hz)
            self.state = 206
            self.match(NmrPipePKParser.Yw_hz)
            self.state = 207
            self.match(NmrPipePKParser.Zw_hz)
            self.state = 208
            self.match(NmrPipePKParser.X1)
            self.state = 209
            self.match(NmrPipePKParser.X3)
            self.state = 210
            self.match(NmrPipePKParser.Y1)
            self.state = 211
            self.match(NmrPipePKParser.Y3)
            self.state = 212
            self.match(NmrPipePKParser.Z1)
            self.state = 213
            self.match(NmrPipePKParser.Z3)
            self.state = 214
            self.match(NmrPipePKParser.Height)
            self.state = 215
            self.match(NmrPipePKParser.DHeight)
            self.state = 216
            self.match(NmrPipePKParser.Vol)
            self.state = 217
            self.match(NmrPipePKParser.Pchi2)
            self.state = 218
            self.match(NmrPipePKParser.Type)
            self.state = 220
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==70:
                self.state = 219
                self.match(NmrPipePKParser.Ass)


            self.state = 222
            self.match(NmrPipePKParser.ClustId)
            self.state = 223
            self.match(NmrPipePKParser.Memcnt)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==73:
                self.state = 224
                self.match(NmrPipePKParser.Trouble)


            self.state = 227
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 228
            self.match(NmrPipePKParser.Format)
            self.state = 229
            self.match(NmrPipePKParser.Format_code)
            self.state = 230
            self.match(NmrPipePKParser.Format_code)
            self.state = 231
            self.match(NmrPipePKParser.Format_code)
            self.state = 232
            self.match(NmrPipePKParser.Format_code)
            self.state = 233
            self.match(NmrPipePKParser.Format_code)
            self.state = 234
            self.match(NmrPipePKParser.Format_code)
            self.state = 235
            self.match(NmrPipePKParser.Format_code)
            self.state = 236
            self.match(NmrPipePKParser.Format_code)
            self.state = 237
            self.match(NmrPipePKParser.Format_code)
            self.state = 238
            self.match(NmrPipePKParser.Format_code)
            self.state = 239
            self.match(NmrPipePKParser.Format_code)
            self.state = 240
            self.match(NmrPipePKParser.Format_code)
            self.state = 241
            self.match(NmrPipePKParser.Format_code)
            self.state = 242
            self.match(NmrPipePKParser.Format_code)
            self.state = 243
            self.match(NmrPipePKParser.Format_code)
            self.state = 244
            self.match(NmrPipePKParser.Format_code)
            self.state = 245
            self.match(NmrPipePKParser.Format_code)
            self.state = 246
            self.match(NmrPipePKParser.Format_code)
            self.state = 247
            self.match(NmrPipePKParser.Format_code)
            self.state = 248
            self.match(NmrPipePKParser.Format_code)
            self.state = 249
            self.match(NmrPipePKParser.Format_code)
            self.state = 250
            self.match(NmrPipePKParser.Format_code)
            self.state = 251
            self.match(NmrPipePKParser.Format_code)
            self.state = 252
            self.match(NmrPipePKParser.Format_code)
            self.state = 253
            self.match(NmrPipePKParser.Format_code)
            self.state = 254
            self.match(NmrPipePKParser.Format_code)
            self.state = 255
            self.match(NmrPipePKParser.Format_code)
            self.state = 256
            self.match(NmrPipePKParser.Format_code)
            self.state = 257
            self.match(NmrPipePKParser.Format_code)
            self.state = 258
            self.match(NmrPipePKParser.Format_code)
            self.state = 260
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 259
                self.match(NmrPipePKParser.Format_code)


            self.state = 262
            self.match(NmrPipePKParser.Format_code)
            self.state = 263
            self.match(NmrPipePKParser.Format_code)
            self.state = 265
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==92:
                self.state = 264
                self.match(NmrPipePKParser.Format_code)


            self.state = 267
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 271
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 268
                self.match(NmrPipePKParser.Null_value)
                self.state = 269
                self.match(NmrPipePKParser.Any_name_NV)
                self.state = 270
                self.match(NmrPipePKParser.RETURN_NV)


            self.state = 276
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 273
                self.match(NmrPipePKParser.Null_string)
                self.state = 274
                self.match(NmrPipePKParser.Any_name_NS)
                self.state = 275
                self.match(NmrPipePKParser.RETURN_NS)


            self.state = 279 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 278
                self.peak_3d()
                self.state = 281 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

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
                return self.getTokens(NmrPipePKParser.Integer)
            else:
                return self.getToken(NmrPipePKParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Any_name(self):
            return self.getToken(NmrPipePKParser.Any_name, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_3d" ):
                listener.enterPeak_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_3d" ):
                listener.exitPeak_3d(self)




    def peak_3d(self):

        localctx = NmrPipePKParser.Peak_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_peak_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 283
            self.match(NmrPipePKParser.Integer)
            self.state = 284
            self.number()
            self.state = 285
            self.number()
            self.state = 286
            self.number()
            self.state = 287
            self.number()
            self.state = 288
            self.number()
            self.state = 289
            self.number()
            self.state = 290
            self.number()
            self.state = 291
            self.number()
            self.state = 292
            self.number()
            self.state = 293
            self.number()
            self.state = 294
            self.number()
            self.state = 295
            self.number()
            self.state = 296
            self.number()
            self.state = 297
            self.number()
            self.state = 298
            self.number()
            self.state = 299
            self.number()
            self.state = 300
            self.number()
            self.state = 301
            self.number()
            self.state = 302
            self.match(NmrPipePKParser.Integer)
            self.state = 303
            self.match(NmrPipePKParser.Integer)
            self.state = 304
            self.match(NmrPipePKParser.Integer)
            self.state = 305
            self.match(NmrPipePKParser.Integer)
            self.state = 306
            self.match(NmrPipePKParser.Integer)
            self.state = 307
            self.match(NmrPipePKParser.Integer)
            self.state = 308
            self.number()
            self.state = 309
            self.number()
            self.state = 310
            self.number()
            self.state = 311
            self.number()
            self.state = 312
            self.match(NmrPipePKParser.Integer)
            self.state = 314
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 313
                self.match(NmrPipePKParser.Any_name)


            self.state = 316
            self.match(NmrPipePKParser.Integer)
            self.state = 317
            self.match(NmrPipePKParser.Integer)
            self.state = 319
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 318
                self.match(NmrPipePKParser.Integer)


            self.state = 321
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Peak_list_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def Index(self):
            return self.getToken(NmrPipePKParser.Index, 0)

        def X_axis(self):
            return self.getToken(NmrPipePKParser.X_axis, 0)

        def Y_axis(self):
            return self.getToken(NmrPipePKParser.Y_axis, 0)

        def Z_axis(self):
            return self.getToken(NmrPipePKParser.Z_axis, 0)

        def A_axis(self):
            return self.getToken(NmrPipePKParser.A_axis, 0)

        def Dx(self):
            return self.getToken(NmrPipePKParser.Dx, 0)

        def Dy(self):
            return self.getToken(NmrPipePKParser.Dy, 0)

        def Dz(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Dz)
            else:
                return self.getToken(NmrPipePKParser.Dz, i)

        def X_ppm(self):
            return self.getToken(NmrPipePKParser.X_ppm, 0)

        def Y_ppm(self):
            return self.getToken(NmrPipePKParser.Y_ppm, 0)

        def Z_ppm(self):
            return self.getToken(NmrPipePKParser.Z_ppm, 0)

        def A_ppm(self):
            return self.getToken(NmrPipePKParser.A_ppm, 0)

        def X_hz(self):
            return self.getToken(NmrPipePKParser.X_hz, 0)

        def Y_hz(self):
            return self.getToken(NmrPipePKParser.Y_hz, 0)

        def Z_hz(self):
            return self.getToken(NmrPipePKParser.Z_hz, 0)

        def A_hz(self):
            return self.getToken(NmrPipePKParser.A_hz, 0)

        def Xw(self):
            return self.getToken(NmrPipePKParser.Xw, 0)

        def Yw(self):
            return self.getToken(NmrPipePKParser.Yw, 0)

        def Zw(self):
            return self.getToken(NmrPipePKParser.Zw, 0)

        def Aw(self):
            return self.getToken(NmrPipePKParser.Aw, 0)

        def Xw_hz(self):
            return self.getToken(NmrPipePKParser.Xw_hz, 0)

        def Yw_hz(self):
            return self.getToken(NmrPipePKParser.Yw_hz, 0)

        def Zw_hz(self):
            return self.getToken(NmrPipePKParser.Zw_hz, 0)

        def Aw_hz(self):
            return self.getToken(NmrPipePKParser.Aw_hz, 0)

        def X1(self):
            return self.getToken(NmrPipePKParser.X1, 0)

        def X3(self):
            return self.getToken(NmrPipePKParser.X3, 0)

        def Y1(self):
            return self.getToken(NmrPipePKParser.Y1, 0)

        def Y3(self):
            return self.getToken(NmrPipePKParser.Y3, 0)

        def Z1(self):
            return self.getToken(NmrPipePKParser.Z1, 0)

        def Z3(self):
            return self.getToken(NmrPipePKParser.Z3, 0)

        def A1(self):
            return self.getToken(NmrPipePKParser.A1, 0)

        def A3(self):
            return self.getToken(NmrPipePKParser.A3, 0)

        def Height(self):
            return self.getToken(NmrPipePKParser.Height, 0)

        def DHeight(self):
            return self.getToken(NmrPipePKParser.DHeight, 0)

        def Vol(self):
            return self.getToken(NmrPipePKParser.Vol, 0)

        def Pchi2(self):
            return self.getToken(NmrPipePKParser.Pchi2, 0)

        def Type(self):
            return self.getToken(NmrPipePKParser.Type, 0)

        def ClustId(self):
            return self.getToken(NmrPipePKParser.ClustId, 0)

        def Memcnt(self):
            return self.getToken(NmrPipePKParser.Memcnt, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Ass(self):
            return self.getToken(NmrPipePKParser.Ass, 0)

        def Trouble(self):
            return self.getToken(NmrPipePKParser.Trouble, 0)

        def Null_value(self):
            return self.getToken(NmrPipePKParser.Null_value, 0)

        def Any_name_NV(self):
            return self.getToken(NmrPipePKParser.Any_name_NV, 0)

        def RETURN_NV(self):
            return self.getToken(NmrPipePKParser.RETURN_NV, 0)

        def Null_string(self):
            return self.getToken(NmrPipePKParser.Null_string, 0)

        def Any_name_NS(self):
            return self.getToken(NmrPipePKParser.Any_name_NS, 0)

        def RETURN_NS(self):
            return self.getToken(NmrPipePKParser.RETURN_NS, 0)

        def peak_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Peak_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Peak_4dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_list_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_list_4d" ):
                listener.enterPeak_list_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_list_4d" ):
                listener.exitPeak_list_4d(self)




    def peak_list_4d(self):

        localctx = NmrPipePKParser.Peak_list_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_peak_list_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 323
            self.match(NmrPipePKParser.Vars)
            self.state = 324
            self.match(NmrPipePKParser.Index)
            self.state = 325
            self.match(NmrPipePKParser.X_axis)
            self.state = 326
            self.match(NmrPipePKParser.Y_axis)
            self.state = 327
            self.match(NmrPipePKParser.Z_axis)
            self.state = 328
            self.match(NmrPipePKParser.A_axis)
            self.state = 329
            self.match(NmrPipePKParser.Dx)
            self.state = 330
            self.match(NmrPipePKParser.Dy)
            self.state = 331
            self.match(NmrPipePKParser.Dz)
            self.state = 332
            self.match(NmrPipePKParser.Dz)
            self.state = 333
            self.match(NmrPipePKParser.X_ppm)
            self.state = 334
            self.match(NmrPipePKParser.Y_ppm)
            self.state = 335
            self.match(NmrPipePKParser.Z_ppm)
            self.state = 336
            self.match(NmrPipePKParser.A_ppm)
            self.state = 337
            self.match(NmrPipePKParser.X_hz)
            self.state = 338
            self.match(NmrPipePKParser.Y_hz)
            self.state = 339
            self.match(NmrPipePKParser.Z_hz)
            self.state = 340
            self.match(NmrPipePKParser.A_hz)
            self.state = 341
            self.match(NmrPipePKParser.Xw)
            self.state = 342
            self.match(NmrPipePKParser.Yw)
            self.state = 343
            self.match(NmrPipePKParser.Zw)
            self.state = 344
            self.match(NmrPipePKParser.Aw)
            self.state = 345
            self.match(NmrPipePKParser.Xw_hz)
            self.state = 346
            self.match(NmrPipePKParser.Yw_hz)
            self.state = 347
            self.match(NmrPipePKParser.Zw_hz)
            self.state = 348
            self.match(NmrPipePKParser.Aw_hz)
            self.state = 349
            self.match(NmrPipePKParser.X1)
            self.state = 350
            self.match(NmrPipePKParser.X3)
            self.state = 351
            self.match(NmrPipePKParser.Y1)
            self.state = 352
            self.match(NmrPipePKParser.Y3)
            self.state = 353
            self.match(NmrPipePKParser.Z1)
            self.state = 354
            self.match(NmrPipePKParser.Z3)
            self.state = 355
            self.match(NmrPipePKParser.A1)
            self.state = 356
            self.match(NmrPipePKParser.A3)
            self.state = 357
            self.match(NmrPipePKParser.Height)
            self.state = 358
            self.match(NmrPipePKParser.DHeight)
            self.state = 359
            self.match(NmrPipePKParser.Vol)
            self.state = 360
            self.match(NmrPipePKParser.Pchi2)
            self.state = 361
            self.match(NmrPipePKParser.Type)
            self.state = 363
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==70:
                self.state = 362
                self.match(NmrPipePKParser.Ass)


            self.state = 365
            self.match(NmrPipePKParser.ClustId)
            self.state = 366
            self.match(NmrPipePKParser.Memcnt)
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==73:
                self.state = 367
                self.match(NmrPipePKParser.Trouble)


            self.state = 370
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 371
            self.match(NmrPipePKParser.Format)
            self.state = 372
            self.match(NmrPipePKParser.Format_code)
            self.state = 373
            self.match(NmrPipePKParser.Format_code)
            self.state = 374
            self.match(NmrPipePKParser.Format_code)
            self.state = 375
            self.match(NmrPipePKParser.Format_code)
            self.state = 376
            self.match(NmrPipePKParser.Format_code)
            self.state = 377
            self.match(NmrPipePKParser.Format_code)
            self.state = 378
            self.match(NmrPipePKParser.Format_code)
            self.state = 379
            self.match(NmrPipePKParser.Format_code)
            self.state = 380
            self.match(NmrPipePKParser.Format_code)
            self.state = 381
            self.match(NmrPipePKParser.Format_code)
            self.state = 382
            self.match(NmrPipePKParser.Format_code)
            self.state = 383
            self.match(NmrPipePKParser.Format_code)
            self.state = 384
            self.match(NmrPipePKParser.Format_code)
            self.state = 385
            self.match(NmrPipePKParser.Format_code)
            self.state = 386
            self.match(NmrPipePKParser.Format_code)
            self.state = 387
            self.match(NmrPipePKParser.Format_code)
            self.state = 388
            self.match(NmrPipePKParser.Format_code)
            self.state = 389
            self.match(NmrPipePKParser.Format_code)
            self.state = 390
            self.match(NmrPipePKParser.Format_code)
            self.state = 391
            self.match(NmrPipePKParser.Format_code)
            self.state = 392
            self.match(NmrPipePKParser.Format_code)
            self.state = 393
            self.match(NmrPipePKParser.Format_code)
            self.state = 394
            self.match(NmrPipePKParser.Format_code)
            self.state = 395
            self.match(NmrPipePKParser.Format_code)
            self.state = 396
            self.match(NmrPipePKParser.Format_code)
            self.state = 397
            self.match(NmrPipePKParser.Format_code)
            self.state = 398
            self.match(NmrPipePKParser.Format_code)
            self.state = 399
            self.match(NmrPipePKParser.Format_code)
            self.state = 400
            self.match(NmrPipePKParser.Format_code)
            self.state = 401
            self.match(NmrPipePKParser.Format_code)
            self.state = 402
            self.match(NmrPipePKParser.Format_code)
            self.state = 403
            self.match(NmrPipePKParser.Format_code)
            self.state = 404
            self.match(NmrPipePKParser.Format_code)
            self.state = 405
            self.match(NmrPipePKParser.Format_code)
            self.state = 406
            self.match(NmrPipePKParser.Format_code)
            self.state = 407
            self.match(NmrPipePKParser.Format_code)
            self.state = 408
            self.match(NmrPipePKParser.Format_code)
            self.state = 409
            self.match(NmrPipePKParser.Format_code)
            self.state = 411
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 410
                self.match(NmrPipePKParser.Format_code)


            self.state = 413
            self.match(NmrPipePKParser.Format_code)
            self.state = 414
            self.match(NmrPipePKParser.Format_code)
            self.state = 416
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==92:
                self.state = 415
                self.match(NmrPipePKParser.Format_code)


            self.state = 418
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 422
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 419
                self.match(NmrPipePKParser.Null_value)
                self.state = 420
                self.match(NmrPipePKParser.Any_name_NV)
                self.state = 421
                self.match(NmrPipePKParser.RETURN_NV)


            self.state = 427
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 424
                self.match(NmrPipePKParser.Null_string)
                self.state = 425
                self.match(NmrPipePKParser.Any_name_NS)
                self.state = 426
                self.match(NmrPipePKParser.RETURN_NS)


            self.state = 430 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 429
                self.peak_4d()
                self.state = 432 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

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
                return self.getTokens(NmrPipePKParser.Integer)
            else:
                return self.getToken(NmrPipePKParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Any_name(self):
            return self.getToken(NmrPipePKParser.Any_name, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_peak_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeak_4d" ):
                listener.enterPeak_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeak_4d" ):
                listener.exitPeak_4d(self)




    def peak_4d(self):

        localctx = NmrPipePKParser.Peak_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_peak_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self.match(NmrPipePKParser.Integer)
            self.state = 435
            self.number()
            self.state = 436
            self.number()
            self.state = 437
            self.number()
            self.state = 438
            self.number()
            self.state = 439
            self.number()
            self.state = 440
            self.number()
            self.state = 441
            self.number()
            self.state = 442
            self.number()
            self.state = 443
            self.number()
            self.state = 444
            self.number()
            self.state = 445
            self.number()
            self.state = 446
            self.number()
            self.state = 447
            self.number()
            self.state = 448
            self.number()
            self.state = 449
            self.number()
            self.state = 450
            self.number()
            self.state = 451
            self.number()
            self.state = 452
            self.number()
            self.state = 453
            self.number()
            self.state = 454
            self.number()
            self.state = 455
            self.number()
            self.state = 456
            self.number()
            self.state = 457
            self.number()
            self.state = 458
            self.number()
            self.state = 459
            self.match(NmrPipePKParser.Integer)
            self.state = 460
            self.match(NmrPipePKParser.Integer)
            self.state = 461
            self.match(NmrPipePKParser.Integer)
            self.state = 462
            self.match(NmrPipePKParser.Integer)
            self.state = 463
            self.match(NmrPipePKParser.Integer)
            self.state = 464
            self.match(NmrPipePKParser.Integer)
            self.state = 465
            self.match(NmrPipePKParser.Integer)
            self.state = 466
            self.match(NmrPipePKParser.Integer)
            self.state = 467
            self.number()
            self.state = 468
            self.number()
            self.state = 469
            self.number()
            self.state = 470
            self.number()
            self.state = 471
            self.match(NmrPipePKParser.Integer)
            self.state = 473
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 472
                self.match(NmrPipePKParser.Any_name)


            self.state = 475
            self.match(NmrPipePKParser.Integer)
            self.state = 476
            self.match(NmrPipePKParser.Integer)
            self.state = 478
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 477
                self.match(NmrPipePKParser.Integer)


            self.state = 480
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Pipp_labelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Data(self):
            return self.getToken(NmrPipePKParser.Data, 0)

        def Dim_count_DA(self):
            return self.getToken(NmrPipePKParser.Dim_count_DA, 0)

        def Integer_DA(self):
            return self.getToken(NmrPipePKParser.Integer_DA, 0)

        def RETURN_DA(self):
            return self.getToken(NmrPipePKParser.RETURN_DA, 0)

        def pipp_axis(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_axisContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_axisContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_label

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_label" ):
                listener.enterPipp_label(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_label" ):
                listener.exitPipp_label(self)




    def pipp_label(self):

        localctx = NmrPipePKParser.Pipp_labelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_pipp_label)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 482
            self.match(NmrPipePKParser.Data)
            self.state = 483
            self.match(NmrPipePKParser.Dim_count_DA)
            self.state = 484
            self.match(NmrPipePKParser.Integer_DA)
            self.state = 485
            self.match(NmrPipePKParser.RETURN_DA)
            self.state = 487 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 486
                    self.pipp_axis()

                else:
                    raise NoViableAltException(self)
                self.state = 489 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,30,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_axisContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Data(self):
            return self.getToken(NmrPipePKParser.Data, 0)

        def Integer_DA(self):
            return self.getToken(NmrPipePKParser.Integer_DA, 0)

        def Float_DA(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Float_DA)
            else:
                return self.getToken(NmrPipePKParser.Float_DA, i)

        def RETURN_DA(self):
            return self.getToken(NmrPipePKParser.RETURN_DA, 0)

        def X_axis_DA(self):
            return self.getToken(NmrPipePKParser.X_axis_DA, 0)

        def Y_axis_DA(self):
            return self.getToken(NmrPipePKParser.Y_axis_DA, 0)

        def Z_axis_DA(self):
            return self.getToken(NmrPipePKParser.Z_axis_DA, 0)

        def A_axis_DA(self):
            return self.getToken(NmrPipePKParser.A_axis_DA, 0)

        def Ppm_DA(self):
            return self.getToken(NmrPipePKParser.Ppm_DA, 0)

        def Hz_DA(self):
            return self.getToken(NmrPipePKParser.Hz_DA, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_axis

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_axis" ):
                listener.enterPipp_axis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_axis" ):
                listener.exitPipp_axis(self)




    def pipp_axis(self):

        localctx = NmrPipePKParser.Pipp_axisContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_pipp_axis)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 491
            self.match(NmrPipePKParser.Data)
            self.state = 492
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1966080) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 493
            self.match(NmrPipePKParser.Integer_DA)
            self.state = 494
            self.match(NmrPipePKParser.Float_DA)
            self.state = 495
            self.match(NmrPipePKParser.Float_DA)
            self.state = 496
            self.match(NmrPipePKParser.Float_DA)
            self.state = 497
            _la = self._input.LA(1)
            if not(_la==23 or _la==24):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 498
            self.match(NmrPipePKParser.Float_DA)
            self.state = 499
            self.match(NmrPipePKParser.RETURN_DA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_peak_list_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def PkID(self):
            return self.getToken(NmrPipePKParser.PkID, 0)

        def X(self):
            return self.getToken(NmrPipePKParser.X, 0)

        def Y(self):
            return self.getToken(NmrPipePKParser.Y, 0)

        def Intensity(self):
            return self.getToken(NmrPipePKParser.Intensity, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def Assign(self):
            return self.getToken(NmrPipePKParser.Assign, 0)

        def Assign1(self):
            return self.getToken(NmrPipePKParser.Assign1, 0)

        def Assign2(self):
            return self.getToken(NmrPipePKParser.Assign2, 0)

        def pipp_peak_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_2dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_list_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_list_2d" ):
                listener.enterPipp_peak_list_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_list_2d" ):
                listener.exitPipp_peak_list_2d(self)




    def pipp_peak_list_2d(self):

        localctx = NmrPipePKParser.Pipp_peak_list_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_pipp_peak_list_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 501
            self.match(NmrPipePKParser.Format)
            self.state = 503 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 502
                self.match(NmrPipePKParser.Format_code)
                self.state = 505 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==92):
                    break

            self.state = 507
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 508
            self.match(NmrPipePKParser.Vars)
            self.state = 509
            self.match(NmrPipePKParser.PkID)
            self.state = 510
            self.match(NmrPipePKParser.X)
            self.state = 511
            self.match(NmrPipePKParser.Y)
            self.state = 512
            self.match(NmrPipePKParser.Intensity)
            self.state = 516
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [82]:
                self.state = 513
                self.match(NmrPipePKParser.Assign)
                pass
            elif token in [83]:
                self.state = 514
                self.match(NmrPipePKParser.Assign1)
                self.state = 515
                self.match(NmrPipePKParser.Assign2)
                pass
            elif token in [90]:
                pass
            else:
                pass
            self.state = 518
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 520 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 519
                self.pipp_peak_2d()
                self.state = 522 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_peak_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self):
            return self.getToken(NmrPipePKParser.Integer, 0)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_2d" ):
                listener.enterPipp_peak_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_2d" ):
                listener.exitPipp_peak_2d(self)




    def pipp_peak_2d(self):

        localctx = NmrPipePKParser.Pipp_peak_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_pipp_peak_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 524
            self.match(NmrPipePKParser.Integer)
            self.state = 525
            self.number()
            self.state = 526
            self.number()
            self.state = 528 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 527
                self.number()
                self.state = 530 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4992) != 0)):
                    break

            self.state = 532
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Pipp_peak_list_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def PkID(self):
            return self.getToken(NmrPipePKParser.PkID, 0)

        def X(self):
            return self.getToken(NmrPipePKParser.X, 0)

        def Y(self):
            return self.getToken(NmrPipePKParser.Y, 0)

        def Z(self):
            return self.getToken(NmrPipePKParser.Z, 0)

        def Intensity(self):
            return self.getToken(NmrPipePKParser.Intensity, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def Sl_Z(self):
            return self.getToken(NmrPipePKParser.Sl_Z, 0)

        def Assign(self):
            return self.getToken(NmrPipePKParser.Assign, 0)

        def Assign1(self):
            return self.getToken(NmrPipePKParser.Assign1, 0)

        def Assign2(self):
            return self.getToken(NmrPipePKParser.Assign2, 0)

        def pipp_peak_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_3dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_list_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_list_3d" ):
                listener.enterPipp_peak_list_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_list_3d" ):
                listener.exitPipp_peak_list_3d(self)




    def pipp_peak_list_3d(self):

        localctx = NmrPipePKParser.Pipp_peak_list_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_pipp_peak_list_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 534
            self.match(NmrPipePKParser.Format)
            self.state = 536 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 535
                self.match(NmrPipePKParser.Format_code)
                self.state = 538 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==92):
                    break

            self.state = 540
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 541
            self.match(NmrPipePKParser.Vars)
            self.state = 542
            self.match(NmrPipePKParser.PkID)
            self.state = 544
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==75:
                self.state = 543
                self.match(NmrPipePKParser.Sl_Z)


            self.state = 546
            self.match(NmrPipePKParser.X)
            self.state = 547
            self.match(NmrPipePKParser.Y)
            self.state = 548
            self.match(NmrPipePKParser.Z)
            self.state = 549
            self.match(NmrPipePKParser.Intensity)
            self.state = 553
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [82]:
                self.state = 550
                self.match(NmrPipePKParser.Assign)
                pass
            elif token in [83]:
                self.state = 551
                self.match(NmrPipePKParser.Assign1)
                self.state = 552
                self.match(NmrPipePKParser.Assign2)
                pass
            elif token in [90]:
                pass
            else:
                pass
            self.state = 555
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 557 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 556
                self.pipp_peak_3d()
                self.state = 559 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_peak_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer)
            else:
                return self.getToken(NmrPipePKParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_3d" ):
                listener.enterPipp_peak_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_3d" ):
                listener.exitPipp_peak_3d(self)




    def pipp_peak_3d(self):

        localctx = NmrPipePKParser.Pipp_peak_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_pipp_peak_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 561
            self.match(NmrPipePKParser.Integer)
            self.state = 563
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.state = 562
                self.match(NmrPipePKParser.Integer)


            self.state = 565
            self.number()
            self.state = 566
            self.number()
            self.state = 567
            self.number()
            self.state = 569 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 568
                self.number()
                self.state = 571 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4992) != 0)):
                    break

            self.state = 573
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Pipp_peak_list_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Format(self):
            return self.getToken(NmrPipePKParser.Format, 0)

        def RETURN_FO(self):
            return self.getToken(NmrPipePKParser.RETURN_FO, 0)

        def Vars(self):
            return self.getToken(NmrPipePKParser.Vars, 0)

        def PkID(self):
            return self.getToken(NmrPipePKParser.PkID, 0)

        def X(self):
            return self.getToken(NmrPipePKParser.X, 0)

        def Y(self):
            return self.getToken(NmrPipePKParser.Y, 0)

        def Z(self):
            return self.getToken(NmrPipePKParser.Z, 0)

        def A(self):
            return self.getToken(NmrPipePKParser.A, 0)

        def Intensity(self):
            return self.getToken(NmrPipePKParser.Intensity, 0)

        def RETURN_VA(self):
            return self.getToken(NmrPipePKParser.RETURN_VA, 0)

        def Format_code(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Format_code)
            else:
                return self.getToken(NmrPipePKParser.Format_code, i)

        def Sl_A(self):
            return self.getToken(NmrPipePKParser.Sl_A, 0)

        def Sl_Z(self):
            return self.getToken(NmrPipePKParser.Sl_Z, 0)

        def Assign(self):
            return self.getToken(NmrPipePKParser.Assign, 0)

        def Assign1(self):
            return self.getToken(NmrPipePKParser.Assign1, 0)

        def Assign2(self):
            return self.getToken(NmrPipePKParser.Assign2, 0)

        def pipp_peak_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_peak_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_peak_4dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_list_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_list_4d" ):
                listener.enterPipp_peak_list_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_list_4d" ):
                listener.exitPipp_peak_list_4d(self)




    def pipp_peak_list_4d(self):

        localctx = NmrPipePKParser.Pipp_peak_list_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_pipp_peak_list_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 575
            self.match(NmrPipePKParser.Format)
            self.state = 577 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 576
                self.match(NmrPipePKParser.Format_code)
                self.state = 579 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==92):
                    break

            self.state = 581
            self.match(NmrPipePKParser.RETURN_FO)
            self.state = 582
            self.match(NmrPipePKParser.Vars)
            self.state = 583
            self.match(NmrPipePKParser.PkID)
            self.state = 585
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==76:
                self.state = 584
                self.match(NmrPipePKParser.Sl_A)


            self.state = 588
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==75:
                self.state = 587
                self.match(NmrPipePKParser.Sl_Z)


            self.state = 590
            self.match(NmrPipePKParser.X)
            self.state = 591
            self.match(NmrPipePKParser.Y)
            self.state = 592
            self.match(NmrPipePKParser.Z)
            self.state = 593
            self.match(NmrPipePKParser.A)
            self.state = 594
            self.match(NmrPipePKParser.Intensity)
            self.state = 598
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [82]:
                self.state = 595
                self.match(NmrPipePKParser.Assign)
                pass
            elif token in [83]:
                self.state = 596
                self.match(NmrPipePKParser.Assign1)
                self.state = 597
                self.match(NmrPipePKParser.Assign2)
                pass
            elif token in [90]:
                pass
            else:
                pass
            self.state = 600
            self.match(NmrPipePKParser.RETURN_VA)
            self.state = 602 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 601
                self.pipp_peak_4d()
                self.state = 604 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==7):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_peak_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer)
            else:
                return self.getToken(NmrPipePKParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.NumberContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.NumberContext,i)


        def RETURN(self):
            return self.getToken(NmrPipePKParser.RETURN, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_peak_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_peak_4d" ):
                listener.enterPipp_peak_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_peak_4d" ):
                listener.exitPipp_peak_4d(self)




    def pipp_peak_4d(self):

        localctx = NmrPipePKParser.Pipp_peak_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_pipp_peak_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 606
            self.match(NmrPipePKParser.Integer)
            self.state = 608
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
            if la_ == 1:
                self.state = 607
                self.match(NmrPipePKParser.Integer)


            self.state = 611
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.state = 610
                self.match(NmrPipePKParser.Integer)


            self.state = 613
            self.number()
            self.state = 614
            self.number()
            self.state = 615
            self.number()
            self.state = 616
            self.number()
            self.state = 618 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 617
                self.number()
                self.state = 620 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4992) != 0)):
                    break

            self.state = 622
            _la = self._input.LA(1)
            if not(_la==-1 or _la==14):
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


    class Pipp_row_peak_list_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pipp_row_peak_2d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_2dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_2dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_list_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_list_2d" ):
                listener.enterPipp_row_peak_list_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_list_2d" ):
                listener.exitPipp_row_peak_list_2d(self)




    def pipp_row_peak_list_2d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_list_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_pipp_row_peak_list_2d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 625 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 624
                    self.pipp_row_peak_2d()

                else:
                    raise NoViableAltException(self)
                self.state = 627 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,49,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_row_peak_2dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_paren(self):
            return self.getToken(NmrPipePKParser.L_paren, 0)

        def Float_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Float_PR)
            else:
                return self.getToken(NmrPipePKParser.Float_PR, i)

        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Comma)
            else:
                return self.getToken(NmrPipePKParser.Comma, i)

        def Semicolon(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Semicolon)
            else:
                return self.getToken(NmrPipePKParser.Semicolon, i)

        def Number_sign(self):
            return self.getToken(NmrPipePKParser.Number_sign, 0)

        def Integer_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer_PR)
            else:
                return self.getToken(NmrPipePKParser.Integer_PR, i)

        def Caret(self):
            return self.getToken(NmrPipePKParser.Caret, 0)

        def Real_PR(self):
            return self.getToken(NmrPipePKParser.Real_PR, 0)

        def Percent_sign(self):
            return self.getToken(NmrPipePKParser.Percent_sign, 0)

        def R_paren(self):
            return self.getToken(NmrPipePKParser.R_paren, 0)

        def RETURN_PR(self):
            return self.getToken(NmrPipePKParser.RETURN_PR, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Assignments_PR(self):
            return self.getToken(NmrPipePKParser.Assignments_PR, 0)

        def L_brkt(self):
            return self.getToken(NmrPipePKParser.L_brkt, 0)

        def R_brkt(self):
            return self.getToken(NmrPipePKParser.R_brkt, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_2d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_2d" ):
                listener.enterPipp_row_peak_2d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_2d" ):
                listener.exitPipp_row_peak_2d(self)




    def pipp_row_peak_2d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_2dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_pipp_row_peak_2d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 629
            self.match(NmrPipePKParser.L_paren)
            self.state = 630
            self.match(NmrPipePKParser.Float_PR)
            self.state = 631
            self.match(NmrPipePKParser.Comma)
            self.state = 632
            self.match(NmrPipePKParser.Float_PR)
            self.state = 633
            self.match(NmrPipePKParser.Semicolon)
            self.state = 634
            self.match(NmrPipePKParser.Number_sign)
            self.state = 635
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 636
            self.match(NmrPipePKParser.Semicolon)
            self.state = 643
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [113]:
                self.state = 637
                self.match(NmrPipePKParser.Assignments_PR)
                pass
            elif token in [103]:
                self.state = 638
                self.match(NmrPipePKParser.L_brkt)
                self.state = 639
                self.match(NmrPipePKParser.Float_PR)
                self.state = 640
                self.match(NmrPipePKParser.Comma)
                self.state = 641
                self.match(NmrPipePKParser.Float_PR)
                self.state = 642
                self.match(NmrPipePKParser.R_brkt)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 645
            self.match(NmrPipePKParser.Caret)
            self.state = 646
            self.match(NmrPipePKParser.Real_PR)
            self.state = 647
            self.match(NmrPipePKParser.Semicolon)
            self.state = 648
            self.match(NmrPipePKParser.Percent_sign)
            self.state = 649
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 650
            self.match(NmrPipePKParser.Semicolon)
            self.state = 651
            self.match(NmrPipePKParser.R_paren)
            self.state = 652
            _la = self._input.LA(1)
            if not(_la==-1 or _la==115):
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


    class Pipp_row_peak_list_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pipp_row_peak_3d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_3dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_3dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_list_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_list_3d" ):
                listener.enterPipp_row_peak_list_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_list_3d" ):
                listener.exitPipp_row_peak_list_3d(self)




    def pipp_row_peak_list_3d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_list_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_pipp_row_peak_list_3d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 655 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 654
                    self.pipp_row_peak_3d()

                else:
                    raise NoViableAltException(self)
                self.state = 657 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,51,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_row_peak_3dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_paren(self):
            return self.getToken(NmrPipePKParser.L_paren, 0)

        def Float_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Float_PR)
            else:
                return self.getToken(NmrPipePKParser.Float_PR, i)

        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Comma)
            else:
                return self.getToken(NmrPipePKParser.Comma, i)

        def Semicolon(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Semicolon)
            else:
                return self.getToken(NmrPipePKParser.Semicolon, i)

        def Number_sign(self):
            return self.getToken(NmrPipePKParser.Number_sign, 0)

        def Integer_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer_PR)
            else:
                return self.getToken(NmrPipePKParser.Integer_PR, i)

        def Caret(self):
            return self.getToken(NmrPipePKParser.Caret, 0)

        def Real_PR(self):
            return self.getToken(NmrPipePKParser.Real_PR, 0)

        def Percent_sign(self):
            return self.getToken(NmrPipePKParser.Percent_sign, 0)

        def R_paren(self):
            return self.getToken(NmrPipePKParser.R_paren, 0)

        def RETURN_PR(self):
            return self.getToken(NmrPipePKParser.RETURN_PR, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Assignments_PR(self):
            return self.getToken(NmrPipePKParser.Assignments_PR, 0)

        def L_brkt(self):
            return self.getToken(NmrPipePKParser.L_brkt, 0)

        def R_brkt(self):
            return self.getToken(NmrPipePKParser.R_brkt, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_3d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_3d" ):
                listener.enterPipp_row_peak_3d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_3d" ):
                listener.exitPipp_row_peak_3d(self)




    def pipp_row_peak_3d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_3dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_pipp_row_peak_3d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 659
            self.match(NmrPipePKParser.L_paren)
            self.state = 660
            self.match(NmrPipePKParser.Float_PR)
            self.state = 661
            self.match(NmrPipePKParser.Comma)
            self.state = 662
            self.match(NmrPipePKParser.Float_PR)
            self.state = 663
            self.match(NmrPipePKParser.Comma)
            self.state = 664
            self.match(NmrPipePKParser.Float_PR)
            self.state = 665
            self.match(NmrPipePKParser.Semicolon)
            self.state = 666
            self.match(NmrPipePKParser.Number_sign)
            self.state = 667
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 668
            self.match(NmrPipePKParser.Semicolon)
            self.state = 677
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [113]:
                self.state = 669
                self.match(NmrPipePKParser.Assignments_PR)
                pass
            elif token in [103]:
                self.state = 670
                self.match(NmrPipePKParser.L_brkt)
                self.state = 671
                self.match(NmrPipePKParser.Float_PR)
                self.state = 672
                self.match(NmrPipePKParser.Comma)
                self.state = 673
                self.match(NmrPipePKParser.Float_PR)
                self.state = 674
                self.match(NmrPipePKParser.Comma)
                self.state = 675
                self.match(NmrPipePKParser.Float_PR)
                self.state = 676
                self.match(NmrPipePKParser.R_brkt)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 679
            self.match(NmrPipePKParser.Caret)
            self.state = 680
            self.match(NmrPipePKParser.Real_PR)
            self.state = 681
            self.match(NmrPipePKParser.Semicolon)
            self.state = 682
            self.match(NmrPipePKParser.Percent_sign)
            self.state = 683
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 684
            self.match(NmrPipePKParser.Semicolon)
            self.state = 685
            self.match(NmrPipePKParser.R_paren)
            self.state = 686
            _la = self._input.LA(1)
            if not(_la==-1 or _la==115):
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


    class Pipp_row_peak_list_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pipp_row_peak_4d(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NmrPipePKParser.Pipp_row_peak_4dContext)
            else:
                return self.getTypedRuleContext(NmrPipePKParser.Pipp_row_peak_4dContext,i)


        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_list_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_list_4d" ):
                listener.enterPipp_row_peak_list_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_list_4d" ):
                listener.exitPipp_row_peak_list_4d(self)




    def pipp_row_peak_list_4d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_list_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_pipp_row_peak_list_4d)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 689 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 688
                    self.pipp_row_peak_4d()

                else:
                    raise NoViableAltException(self)
                self.state = 691 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,53,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pipp_row_peak_4dContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_paren(self):
            return self.getToken(NmrPipePKParser.L_paren, 0)

        def Float_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Float_PR)
            else:
                return self.getToken(NmrPipePKParser.Float_PR, i)

        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Comma)
            else:
                return self.getToken(NmrPipePKParser.Comma, i)

        def Semicolon(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Semicolon)
            else:
                return self.getToken(NmrPipePKParser.Semicolon, i)

        def Number_sign(self):
            return self.getToken(NmrPipePKParser.Number_sign, 0)

        def Integer_PR(self, i:int=None):
            if i is None:
                return self.getTokens(NmrPipePKParser.Integer_PR)
            else:
                return self.getToken(NmrPipePKParser.Integer_PR, i)

        def Caret(self):
            return self.getToken(NmrPipePKParser.Caret, 0)

        def Real_PR(self):
            return self.getToken(NmrPipePKParser.Real_PR, 0)

        def Percent_sign(self):
            return self.getToken(NmrPipePKParser.Percent_sign, 0)

        def R_paren(self):
            return self.getToken(NmrPipePKParser.R_paren, 0)

        def RETURN_PR(self):
            return self.getToken(NmrPipePKParser.RETURN_PR, 0)

        def EOF(self):
            return self.getToken(NmrPipePKParser.EOF, 0)

        def Assignments_PR(self):
            return self.getToken(NmrPipePKParser.Assignments_PR, 0)

        def L_brkt(self):
            return self.getToken(NmrPipePKParser.L_brkt, 0)

        def R_brkt(self):
            return self.getToken(NmrPipePKParser.R_brkt, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_pipp_row_peak_4d

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipp_row_peak_4d" ):
                listener.enterPipp_row_peak_4d(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipp_row_peak_4d" ):
                listener.exitPipp_row_peak_4d(self)




    def pipp_row_peak_4d(self):

        localctx = NmrPipePKParser.Pipp_row_peak_4dContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_pipp_row_peak_4d)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 693
            self.match(NmrPipePKParser.L_paren)
            self.state = 694
            self.match(NmrPipePKParser.Float_PR)
            self.state = 695
            self.match(NmrPipePKParser.Comma)
            self.state = 696
            self.match(NmrPipePKParser.Float_PR)
            self.state = 697
            self.match(NmrPipePKParser.Comma)
            self.state = 698
            self.match(NmrPipePKParser.Float_PR)
            self.state = 699
            self.match(NmrPipePKParser.Comma)
            self.state = 700
            self.match(NmrPipePKParser.Float_PR)
            self.state = 701
            self.match(NmrPipePKParser.Semicolon)
            self.state = 702
            self.match(NmrPipePKParser.Number_sign)
            self.state = 703
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 704
            self.match(NmrPipePKParser.Semicolon)
            self.state = 715
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [113]:
                self.state = 705
                self.match(NmrPipePKParser.Assignments_PR)
                pass
            elif token in [103]:
                self.state = 706
                self.match(NmrPipePKParser.L_brkt)
                self.state = 707
                self.match(NmrPipePKParser.Float_PR)
                self.state = 708
                self.match(NmrPipePKParser.Comma)
                self.state = 709
                self.match(NmrPipePKParser.Float_PR)
                self.state = 710
                self.match(NmrPipePKParser.Comma)
                self.state = 711
                self.match(NmrPipePKParser.Float_PR)
                self.state = 712
                self.match(NmrPipePKParser.Comma)
                self.state = 713
                self.match(NmrPipePKParser.Float_PR)
                self.state = 714
                self.match(NmrPipePKParser.R_brkt)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 717
            self.match(NmrPipePKParser.Caret)
            self.state = 718
            self.match(NmrPipePKParser.Real_PR)
            self.state = 719
            self.match(NmrPipePKParser.Semicolon)
            self.state = 720
            self.match(NmrPipePKParser.Percent_sign)
            self.state = 721
            self.match(NmrPipePKParser.Integer_PR)
            self.state = 722
            self.match(NmrPipePKParser.Semicolon)
            self.state = 723
            self.match(NmrPipePKParser.R_paren)
            self.state = 724
            _la = self._input.LA(1)
            if not(_la==-1 or _la==115):
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

        def Integer(self):
            return self.getToken(NmrPipePKParser.Integer, 0)

        def Float(self):
            return self.getToken(NmrPipePKParser.Float, 0)

        def Real(self):
            return self.getToken(NmrPipePKParser.Real, 0)

        def Any_name(self):
            return self.getToken(NmrPipePKParser.Any_name, 0)

        def getRuleIndex(self):
            return NmrPipePKParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = NmrPipePKParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 726
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4992) != 0)):
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





