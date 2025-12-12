# Generated from SchrodingerMRParser.g4 by ANTLR 4.13.0
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
        4,1,107,593,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,
        7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,
        13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,
        20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,
        26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,
        33,7,33,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,81,8,
        0,10,0,12,0,84,9,0,1,0,1,0,1,1,1,1,4,1,90,8,1,11,1,12,1,91,1,1,1,
        1,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,
        5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,4,6,120,8,6,11,6,12,6,121,1,6,
        4,6,125,8,6,11,6,12,6,126,3,6,129,8,6,1,7,1,7,1,7,1,7,1,7,1,7,1,
        8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,4,9,151,8,
        9,11,9,12,9,152,1,9,4,9,156,8,9,11,9,12,9,157,3,9,160,8,9,1,10,1,
        10,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,
        12,1,12,1,12,1,12,1,12,1,12,1,12,4,12,183,8,12,11,12,12,12,184,1,
        12,4,12,188,8,12,11,12,12,12,189,3,12,192,8,12,1,13,1,13,1,13,1,
        13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,14,1,15,4,15,207,8,15,11,
        15,12,15,208,1,15,4,15,212,8,15,11,15,12,15,213,3,15,216,8,15,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,18,4,18,239,8,18,11,18,12,18,
        240,1,18,4,18,244,8,18,11,18,12,18,245,3,18,248,8,18,1,19,1,19,1,
        19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,
        20,1,20,1,20,1,20,1,20,1,21,4,21,271,8,21,11,21,12,21,272,1,21,4,
        21,276,8,21,11,21,12,21,277,3,21,280,8,21,1,22,1,22,1,22,1,22,1,
        22,1,22,1,22,1,22,1,22,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,
        23,1,23,1,24,4,24,302,8,24,11,24,12,24,303,1,24,4,24,307,8,24,11,
        24,12,24,308,3,24,311,8,24,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,
        25,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,27,1,27,1,
        27,1,27,1,28,1,28,1,28,5,28,338,8,28,10,28,12,28,341,9,28,1,29,1,
        29,3,29,345,8,29,1,29,5,29,348,8,29,10,29,12,29,351,9,29,1,30,1,
        30,1,30,1,30,1,30,1,30,1,30,1,30,5,30,361,8,30,10,30,12,30,364,9,
        30,1,30,1,30,1,30,1,30,1,30,1,30,5,30,372,8,30,10,30,12,30,375,9,
        30,3,30,377,8,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,
        30,3,30,389,8,30,1,30,1,30,1,30,1,30,1,30,3,30,396,8,30,1,30,1,30,
        1,30,1,30,5,30,402,8,30,10,30,12,30,405,9,30,1,30,1,30,1,30,1,30,
        1,30,3,30,412,8,30,1,30,1,30,1,30,5,30,417,8,30,10,30,12,30,420,
        9,30,3,30,422,8,30,1,30,1,30,1,30,1,30,5,30,428,8,30,10,30,12,30,
        431,9,30,1,30,1,30,1,30,1,30,5,30,437,8,30,10,30,12,30,440,9,30,
        1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,
        1,30,5,30,456,8,30,10,30,12,30,459,9,30,1,30,1,30,1,30,1,30,5,30,
        465,8,30,10,30,12,30,468,9,30,1,30,1,30,1,30,1,30,1,30,5,30,475,
        8,30,10,30,12,30,478,9,30,3,30,480,8,30,1,30,1,30,1,30,1,30,1,30,
        5,30,487,8,30,10,30,12,30,490,9,30,3,30,492,8,30,1,30,1,30,1,30,
        1,30,1,30,5,30,499,8,30,10,30,12,30,502,9,30,3,30,504,8,30,1,30,
        1,30,1,30,1,30,5,30,510,8,30,10,30,12,30,513,9,30,1,30,1,30,1,30,
        1,30,5,30,519,8,30,10,30,12,30,522,9,30,1,30,1,30,1,30,1,30,1,30,
        3,30,529,8,30,1,30,1,30,1,30,1,30,1,30,3,30,536,8,30,1,30,1,30,1,
        30,1,30,1,30,3,30,543,8,30,1,30,1,30,1,30,1,30,1,30,3,30,550,8,30,
        1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,
        1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,
        1,30,1,30,1,30,1,30,1,30,3,30,583,8,30,1,31,1,31,1,32,1,32,1,33,
        1,33,1,33,1,33,1,33,0,0,34,0,2,4,6,8,10,12,14,16,18,20,22,24,26,
        28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,0,11,
        2,0,20,20,31,31,1,0,74,75,2,0,21,21,32,32,1,0,79,83,2,0,22,22,37,
        37,2,0,67,67,74,75,2,0,23,23,38,38,1,0,93,99,1,0,101,106,2,0,24,
        24,47,47,2,0,67,67,69,69,676,0,82,1,0,0,0,2,87,1,0,0,0,4,95,1,0,
        0,0,6,100,1,0,0,0,8,104,1,0,0,0,10,108,1,0,0,0,12,128,1,0,0,0,14,
        130,1,0,0,0,16,136,1,0,0,0,18,159,1,0,0,0,20,161,1,0,0,0,22,168,
        1,0,0,0,24,191,1,0,0,0,26,193,1,0,0,0,28,199,1,0,0,0,30,215,1,0,
        0,0,32,217,1,0,0,0,34,227,1,0,0,0,36,247,1,0,0,0,38,249,1,0,0,0,
        40,259,1,0,0,0,42,279,1,0,0,0,44,281,1,0,0,0,46,290,1,0,0,0,48,310,
        1,0,0,0,50,312,1,0,0,0,52,320,1,0,0,0,54,330,1,0,0,0,56,334,1,0,
        0,0,58,342,1,0,0,0,60,582,1,0,0,0,62,584,1,0,0,0,64,586,1,0,0,0,
        66,588,1,0,0,0,68,81,3,2,1,0,69,81,3,6,3,0,70,81,3,8,4,0,71,81,3,
        10,5,0,72,81,3,14,7,0,73,81,3,20,10,0,74,81,3,26,13,0,75,81,3,66,
        33,0,76,81,3,30,15,0,77,81,3,36,18,0,78,81,3,42,21,0,79,81,3,48,
        24,0,80,68,1,0,0,0,80,69,1,0,0,0,80,70,1,0,0,0,80,71,1,0,0,0,80,
        72,1,0,0,0,80,73,1,0,0,0,80,74,1,0,0,0,80,75,1,0,0,0,80,76,1,0,0,
        0,80,77,1,0,0,0,80,78,1,0,0,0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,
        1,0,0,0,82,83,1,0,0,0,83,85,1,0,0,0,84,82,1,0,0,0,85,86,5,0,0,1,
        86,1,1,0,0,0,87,89,5,2,0,0,88,90,3,4,2,0,89,88,1,0,0,0,90,91,1,0,
        0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,93,1,0,0,0,93,94,5,92,0,0,94,
        3,1,0,0,0,95,96,5,88,0,0,96,97,5,89,0,0,97,98,5,88,0,0,98,99,5,91,
        0,0,99,5,1,0,0,0,100,101,5,3,0,0,101,102,3,12,6,0,102,103,5,6,0,
        0,103,7,1,0,0,0,104,105,5,4,0,0,105,106,3,18,9,0,106,107,5,6,0,0,
        107,9,1,0,0,0,108,109,5,5,0,0,109,110,3,24,12,0,110,111,5,6,0,0,
        111,11,1,0,0,0,112,129,3,66,33,0,113,114,5,7,0,0,114,115,5,8,0,0,
        115,116,5,11,0,0,116,117,5,12,0,0,117,129,5,13,0,0,118,120,3,14,
        7,0,119,118,1,0,0,0,120,121,1,0,0,0,121,119,1,0,0,0,121,122,1,0,
        0,0,122,129,1,0,0,0,123,125,3,16,8,0,124,123,1,0,0,0,125,126,1,0,
        0,0,126,124,1,0,0,0,126,127,1,0,0,0,127,129,1,0,0,0,128,112,1,0,
        0,0,128,113,1,0,0,0,128,119,1,0,0,0,128,124,1,0,0,0,129,13,1,0,0,
        0,130,131,3,54,27,0,131,132,3,54,27,0,132,133,3,62,31,0,133,134,
        3,62,31,0,134,135,3,62,31,0,135,15,1,0,0,0,136,137,5,67,0,0,137,
        138,5,67,0,0,138,139,3,62,31,0,139,140,3,62,31,0,140,141,3,62,31,
        0,141,17,1,0,0,0,142,160,3,66,33,0,143,144,5,7,0,0,144,145,5,8,0,
        0,145,146,5,9,0,0,146,147,5,10,0,0,147,148,5,14,0,0,148,160,5,13,
        0,0,149,151,3,20,10,0,150,149,1,0,0,0,151,152,1,0,0,0,152,150,1,
        0,0,0,152,153,1,0,0,0,153,160,1,0,0,0,154,156,3,22,11,0,155,154,
        1,0,0,0,156,157,1,0,0,0,157,155,1,0,0,0,157,158,1,0,0,0,158,160,
        1,0,0,0,159,142,1,0,0,0,159,143,1,0,0,0,159,150,1,0,0,0,159,155,
        1,0,0,0,160,19,1,0,0,0,161,162,3,54,27,0,162,163,3,54,27,0,163,164,
        3,54,27,0,164,165,3,54,27,0,165,166,3,62,31,0,166,167,3,62,31,0,
        167,21,1,0,0,0,168,169,5,67,0,0,169,170,5,67,0,0,170,171,5,67,0,
        0,171,172,5,67,0,0,172,173,3,62,31,0,173,174,3,62,31,0,174,23,1,
        0,0,0,175,192,3,66,33,0,176,177,5,7,0,0,177,178,5,8,0,0,178,179,
        5,9,0,0,179,180,5,14,0,0,180,192,5,13,0,0,181,183,3,26,13,0,182,
        181,1,0,0,0,183,184,1,0,0,0,184,182,1,0,0,0,184,185,1,0,0,0,185,
        192,1,0,0,0,186,188,3,28,14,0,187,186,1,0,0,0,188,189,1,0,0,0,189,
        187,1,0,0,0,189,190,1,0,0,0,190,192,1,0,0,0,191,175,1,0,0,0,191,
        176,1,0,0,0,191,182,1,0,0,0,191,187,1,0,0,0,192,25,1,0,0,0,193,194,
        3,54,27,0,194,195,3,54,27,0,195,196,3,54,27,0,196,197,3,62,31,0,
        197,198,3,62,31,0,198,27,1,0,0,0,199,200,5,67,0,0,200,201,5,67,0,
        0,201,202,5,67,0,0,202,203,3,62,31,0,203,204,3,62,31,0,204,29,1,
        0,0,0,205,207,3,32,16,0,206,205,1,0,0,0,207,208,1,0,0,0,208,206,
        1,0,0,0,208,209,1,0,0,0,209,216,1,0,0,0,210,212,3,34,17,0,211,210,
        1,0,0,0,212,213,1,0,0,0,213,211,1,0,0,0,213,214,1,0,0,0,214,216,
        1,0,0,0,215,206,1,0,0,0,215,211,1,0,0,0,216,31,1,0,0,0,217,218,5,
        16,0,0,218,219,3,54,27,0,219,220,3,54,27,0,220,221,5,67,0,0,221,
        222,5,67,0,0,222,223,3,62,31,0,223,224,3,62,31,0,224,225,3,62,31,
        0,225,226,3,62,31,0,226,33,1,0,0,0,227,228,5,16,0,0,228,229,5,67,
        0,0,229,230,5,67,0,0,230,231,5,67,0,0,231,232,5,67,0,0,232,233,3,
        62,31,0,233,234,3,62,31,0,234,235,3,62,31,0,235,236,3,62,31,0,236,
        35,1,0,0,0,237,239,3,38,19,0,238,237,1,0,0,0,239,240,1,0,0,0,240,
        238,1,0,0,0,240,241,1,0,0,0,241,248,1,0,0,0,242,244,3,40,20,0,243,
        242,1,0,0,0,244,245,1,0,0,0,245,243,1,0,0,0,245,246,1,0,0,0,246,
        248,1,0,0,0,247,238,1,0,0,0,247,243,1,0,0,0,248,37,1,0,0,0,249,250,
        5,18,0,0,250,251,3,54,27,0,251,252,3,54,27,0,252,253,3,54,27,0,253,
        254,3,54,27,0,254,255,3,62,31,0,255,256,3,62,31,0,256,257,3,62,31,
        0,257,258,3,62,31,0,258,39,1,0,0,0,259,260,5,18,0,0,260,261,5,67,
        0,0,261,262,5,67,0,0,262,263,5,67,0,0,263,264,5,67,0,0,264,265,3,
        62,31,0,265,266,3,62,31,0,266,267,3,62,31,0,267,268,3,62,31,0,268,
        41,1,0,0,0,269,271,3,44,22,0,270,269,1,0,0,0,271,272,1,0,0,0,272,
        270,1,0,0,0,272,273,1,0,0,0,273,280,1,0,0,0,274,276,3,46,23,0,275,
        274,1,0,0,0,276,277,1,0,0,0,277,275,1,0,0,0,277,278,1,0,0,0,278,
        280,1,0,0,0,279,270,1,0,0,0,279,275,1,0,0,0,280,43,1,0,0,0,281,282,
        5,17,0,0,282,283,3,54,27,0,283,284,3,54,27,0,284,285,3,54,27,0,285,
        286,5,67,0,0,286,287,3,62,31,0,287,288,3,62,31,0,288,289,3,62,31,
        0,289,45,1,0,0,0,290,291,5,17,0,0,291,292,5,67,0,0,292,293,5,67,
        0,0,293,294,5,67,0,0,294,295,5,67,0,0,295,296,3,62,31,0,296,297,
        3,62,31,0,297,298,3,62,31,0,298,299,3,62,31,0,299,47,1,0,0,0,300,
        302,3,50,25,0,301,300,1,0,0,0,302,303,1,0,0,0,303,301,1,0,0,0,303,
        304,1,0,0,0,304,311,1,0,0,0,305,307,3,52,26,0,306,305,1,0,0,0,307,
        308,1,0,0,0,308,306,1,0,0,0,308,309,1,0,0,0,309,311,1,0,0,0,310,
        301,1,0,0,0,310,306,1,0,0,0,311,49,1,0,0,0,312,313,5,19,0,0,313,
        314,3,54,27,0,314,315,3,54,27,0,315,316,3,54,27,0,316,317,5,67,0,
        0,317,318,3,62,31,0,318,319,3,62,31,0,319,51,1,0,0,0,320,321,5,19,
        0,0,321,322,5,67,0,0,322,323,5,67,0,0,323,324,5,67,0,0,324,325,5,
        67,0,0,325,326,3,62,31,0,326,327,3,62,31,0,327,328,3,62,31,0,328,
        329,3,62,31,0,329,53,1,0,0,0,330,331,5,77,0,0,331,332,3,56,28,0,
        332,333,5,78,0,0,333,55,1,0,0,0,334,339,3,58,29,0,335,336,5,58,0,
        0,336,338,3,58,29,0,337,335,1,0,0,0,338,341,1,0,0,0,339,337,1,0,
        0,0,339,340,1,0,0,0,340,57,1,0,0,0,341,339,1,0,0,0,342,349,3,60,
        30,0,343,345,5,59,0,0,344,343,1,0,0,0,344,345,1,0,0,0,345,346,1,
        0,0,0,346,348,3,60,30,0,347,344,1,0,0,0,348,351,1,0,0,0,349,347,
        1,0,0,0,349,350,1,0,0,0,350,59,1,0,0,0,351,349,1,0,0,0,352,353,5,
        77,0,0,353,354,3,56,28,0,354,355,5,78,0,0,355,583,1,0,0,0,356,357,
        7,0,0,0,357,362,7,1,0,0,358,359,5,15,0,0,359,361,7,1,0,0,360,358,
        1,0,0,0,361,364,1,0,0,0,362,360,1,0,0,0,362,363,1,0,0,0,363,583,
        1,0,0,0,364,362,1,0,0,0,365,376,7,2,0,0,366,377,5,76,0,0,367,377,
        5,68,0,0,368,373,5,67,0,0,369,370,5,15,0,0,370,372,5,67,0,0,371,
        369,1,0,0,0,372,375,1,0,0,0,373,371,1,0,0,0,373,374,1,0,0,0,374,
        377,1,0,0,0,375,373,1,0,0,0,376,366,1,0,0,0,376,367,1,0,0,0,376,
        368,1,0,0,0,377,583,1,0,0,0,378,379,5,33,0,0,379,380,5,67,0,0,380,
        583,5,67,0,0,381,382,5,34,0,0,382,583,5,67,0,0,383,388,5,35,0,0,
        384,389,5,68,0,0,385,389,5,67,0,0,386,387,7,3,0,0,387,389,5,67,0,
        0,388,384,1,0,0,0,388,385,1,0,0,0,388,386,1,0,0,0,389,583,1,0,0,
        0,390,395,5,36,0,0,391,396,5,68,0,0,392,396,5,67,0,0,393,394,7,3,
        0,0,394,396,5,67,0,0,395,391,1,0,0,0,395,392,1,0,0,0,395,393,1,0,
        0,0,396,583,1,0,0,0,397,398,7,4,0,0,398,403,7,5,0,0,399,400,5,15,
        0,0,400,402,7,5,0,0,401,399,1,0,0,0,402,405,1,0,0,0,403,401,1,0,
        0,0,403,404,1,0,0,0,404,583,1,0,0,0,405,403,1,0,0,0,406,421,7,6,
        0,0,407,412,5,68,0,0,408,412,5,67,0,0,409,410,7,3,0,0,410,412,5,
        67,0,0,411,407,1,0,0,0,411,408,1,0,0,0,411,409,1,0,0,0,412,422,1,
        0,0,0,413,418,7,1,0,0,414,415,5,15,0,0,415,417,7,1,0,0,416,414,1,
        0,0,0,417,420,1,0,0,0,418,416,1,0,0,0,418,419,1,0,0,0,419,422,1,
        0,0,0,420,418,1,0,0,0,421,411,1,0,0,0,421,413,1,0,0,0,422,583,1,
        0,0,0,423,424,5,39,0,0,424,429,7,1,0,0,425,426,5,15,0,0,426,428,
        7,1,0,0,427,425,1,0,0,0,428,431,1,0,0,0,429,427,1,0,0,0,429,430,
        1,0,0,0,430,583,1,0,0,0,431,429,1,0,0,0,432,433,5,40,0,0,433,438,
        7,1,0,0,434,435,5,15,0,0,435,437,7,1,0,0,436,434,1,0,0,0,437,440,
        1,0,0,0,438,436,1,0,0,0,438,439,1,0,0,0,439,583,1,0,0,0,440,438,
        1,0,0,0,441,442,5,41,0,0,442,583,7,7,0,0,443,444,5,42,0,0,444,583,
        7,8,0,0,445,446,5,43,0,0,446,447,3,64,32,0,447,448,3,64,32,0,448,
        583,1,0,0,0,449,450,5,44,0,0,450,583,5,74,0,0,451,452,5,45,0,0,452,
        457,7,1,0,0,453,454,5,15,0,0,454,456,7,1,0,0,455,453,1,0,0,0,456,
        459,1,0,0,0,457,455,1,0,0,0,457,458,1,0,0,0,458,583,1,0,0,0,459,
        457,1,0,0,0,460,461,5,46,0,0,461,466,7,1,0,0,462,463,5,15,0,0,463,
        465,7,1,0,0,464,462,1,0,0,0,465,468,1,0,0,0,466,464,1,0,0,0,466,
        467,1,0,0,0,467,583,1,0,0,0,468,466,1,0,0,0,469,479,7,9,0,0,470,
        480,5,68,0,0,471,476,5,67,0,0,472,473,5,15,0,0,473,475,5,67,0,0,
        474,472,1,0,0,0,475,478,1,0,0,0,476,474,1,0,0,0,476,477,1,0,0,0,
        477,480,1,0,0,0,478,476,1,0,0,0,479,470,1,0,0,0,479,471,1,0,0,0,
        480,583,1,0,0,0,481,491,5,48,0,0,482,492,5,68,0,0,483,488,5,67,0,
        0,484,485,5,15,0,0,485,487,5,67,0,0,486,484,1,0,0,0,487,490,1,0,
        0,0,488,486,1,0,0,0,488,489,1,0,0,0,489,492,1,0,0,0,490,488,1,0,
        0,0,491,482,1,0,0,0,491,483,1,0,0,0,492,583,1,0,0,0,493,503,5,49,
        0,0,494,504,5,68,0,0,495,500,5,67,0,0,496,497,5,15,0,0,497,499,5,
        67,0,0,498,496,1,0,0,0,499,502,1,0,0,0,500,498,1,0,0,0,500,501,1,
        0,0,0,501,504,1,0,0,0,502,500,1,0,0,0,503,494,1,0,0,0,503,495,1,
        0,0,0,504,583,1,0,0,0,505,506,5,50,0,0,506,511,7,1,0,0,507,508,5,
        15,0,0,508,510,7,1,0,0,509,507,1,0,0,0,510,513,1,0,0,0,511,509,1,
        0,0,0,511,512,1,0,0,0,512,583,1,0,0,0,513,511,1,0,0,0,514,515,5,
        51,0,0,515,520,7,1,0,0,516,517,5,15,0,0,517,519,7,1,0,0,518,516,
        1,0,0,0,519,522,1,0,0,0,520,518,1,0,0,0,520,521,1,0,0,0,521,583,
        1,0,0,0,522,520,1,0,0,0,523,528,5,52,0,0,524,529,5,68,0,0,525,529,
        5,67,0,0,526,527,7,3,0,0,527,529,5,67,0,0,528,524,1,0,0,0,528,525,
        1,0,0,0,528,526,1,0,0,0,529,583,1,0,0,0,530,535,5,53,0,0,531,536,
        5,68,0,0,532,536,5,67,0,0,533,534,7,3,0,0,534,536,5,67,0,0,535,531,
        1,0,0,0,535,532,1,0,0,0,535,533,1,0,0,0,536,583,1,0,0,0,537,542,
        5,54,0,0,538,543,5,70,0,0,539,543,5,69,0,0,540,541,7,3,0,0,541,543,
        5,69,0,0,542,538,1,0,0,0,542,539,1,0,0,0,542,540,1,0,0,0,543,583,
        1,0,0,0,544,549,5,55,0,0,545,550,5,68,0,0,546,550,5,67,0,0,547,548,
        7,3,0,0,548,550,5,67,0,0,549,545,1,0,0,0,549,546,1,0,0,0,549,547,
        1,0,0,0,550,583,1,0,0,0,551,583,5,56,0,0,552,583,5,57,0,0,553,554,
        5,61,0,0,554,583,3,60,30,0,555,556,5,62,0,0,556,583,3,60,30,0,557,
        558,5,63,0,0,558,559,3,64,32,0,559,560,3,60,30,0,560,583,1,0,0,0,
        561,562,5,64,0,0,562,563,3,64,32,0,563,564,3,60,30,0,564,583,1,0,
        0,0,565,566,5,65,0,0,566,567,5,67,0,0,567,583,3,60,30,0,568,569,
        5,66,0,0,569,570,5,67,0,0,570,583,3,60,30,0,571,583,5,25,0,0,572,
        583,5,26,0,0,573,583,5,27,0,0,574,583,5,28,0,0,575,583,5,29,0,0,
        576,577,5,30,0,0,577,583,5,74,0,0,578,583,5,71,0,0,579,580,5,60,
        0,0,580,583,3,60,30,0,581,583,5,74,0,0,582,352,1,0,0,0,582,356,1,
        0,0,0,582,365,1,0,0,0,582,378,1,0,0,0,582,381,1,0,0,0,582,383,1,
        0,0,0,582,390,1,0,0,0,582,397,1,0,0,0,582,406,1,0,0,0,582,423,1,
        0,0,0,582,432,1,0,0,0,582,441,1,0,0,0,582,443,1,0,0,0,582,445,1,
        0,0,0,582,449,1,0,0,0,582,451,1,0,0,0,582,460,1,0,0,0,582,469,1,
        0,0,0,582,481,1,0,0,0,582,493,1,0,0,0,582,505,1,0,0,0,582,514,1,
        0,0,0,582,523,1,0,0,0,582,530,1,0,0,0,582,537,1,0,0,0,582,544,1,
        0,0,0,582,551,1,0,0,0,582,552,1,0,0,0,582,553,1,0,0,0,582,555,1,
        0,0,0,582,557,1,0,0,0,582,561,1,0,0,0,582,565,1,0,0,0,582,568,1,
        0,0,0,582,571,1,0,0,0,582,572,1,0,0,0,582,573,1,0,0,0,582,574,1,
        0,0,0,582,575,1,0,0,0,582,576,1,0,0,0,582,578,1,0,0,0,582,579,1,
        0,0,0,582,581,1,0,0,0,583,61,1,0,0,0,584,585,7,10,0,0,585,63,1,0,
        0,0,586,587,7,10,0,0,587,65,1,0,0,0,588,589,5,1,0,0,589,590,5,74,
        0,0,590,591,3,56,28,0,591,67,1,0,0,0,53,80,82,91,121,126,128,152,
        157,159,184,189,191,208,213,215,240,245,247,272,277,279,303,308,
        310,339,344,349,362,373,376,388,395,403,411,418,421,429,438,457,
        466,476,479,488,491,500,503,511,520,528,535,542,549,582
    ]

class SchrodingerMRParser ( Parser ):

    grammarFileName = "SchrodingerMRParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'set'", "'&STRUCT'", "'&DIST'", "'&TROS'", 
                     "'&ANGLE'", "<INVALID>", "'atom1'", "'atom2'", "'atom3'", 
                     "'atom4'", "'lo'", "'up'", "'fc'", "'target'", "','", 
                     "'FXDI'", "'FXBA'", "'FXTA'", "'FXHB'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'backbone'", "'sidechain'", "<INVALID>", "'/C3(-H1)(-H1)(-H1)/'", 
                     "'/C2(=O2)-N2-H2/'", "'smarts.'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'fillres'", "'fillmol'", "'within'", "'beyond'", "'withinbonds'", 
                     "'beyondbonds'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'('", "')'", 
                     "'<'", "'>'", "'<='", "'>='" ]

    symbolicNames = [ "<INVALID>", "Set", "Struct", "Dist", "Tors", "Angle", 
                      "End", "Atom1", "Atom2", "Atom3", "Atom4", "Lo", "Up", 
                      "Fc", "Target", "Comma", "FXDI", "FXBA", "FXTA", "FXHB", 
                      "Entry", "Molecule", "Chain", "Residue", "Atom", "Backbone", 
                      "Sidechain", "Water", "Methyl", "Amide", "Smarts", 
                      "Entry_name", "Molecule_number", "Molecule_modulo", 
                      "Molecule_entrynum", "Molecule_atoms", "Molecule_weight", 
                      "Chain_name", "Residue_name_or_number", "Residue_ptype", 
                      "Residue_mtype", "Residue_polarity", "Residue_secondary_structure", 
                      "Residue_position", "Residue_inscode", "Atom_ptype", 
                      "Atom_name", "Atom_number", "Atom_molnum", "Atom_entrynum", 
                      "Atom_mtype", "Atom_element", "Atom_attachements", 
                      "Atom_atomicnumber", "Atom_charge", "Atom_formalcharge", 
                      "Atom_displayed", "Atom_selected", "Or_op", "And_op", 
                      "Not_op", "Fillres_op", "Fillmol_op", "Within_op", 
                      "Beyond_op", "Withinbonds_op", "Beyondbonds_op", "Integer", 
                      "IntRange", "Float", "FloatRange", "Slash_quote_string", 
                      "SMCLN_COMMENT", "COMMENT", "Simple_name", "Simple_names", 
                      "Integers", "L_paren", "R_paren", "Lt_op", "Gt_op", 
                      "Leq_op", "Geq_op", "Equ_op", "SPACE", "ENCLOSE_COMMENT", 
                      "SECTION_COMMENT", "LINE_COMMENT", "Param_name", "Equ_op_SM", 
                      "SPACE_SM", "RETURN_SM", "End_SM", "Hydrophilic", 
                      "Hydrophobic", "Non_polar", "Polar", "Charged", "Positive", 
                      "Negative", "IGNORE_SPACE_PM", "Helix_or_strand", 
                      "Strand_or_loop", "Helix_or_loop", "Helix", "Strand", 
                      "Loop", "IGNORE_SPACE_SSM" ]

    RULE_schrodinger_mr = 0
    RULE_import_structure = 1
    RULE_struct_statement = 2
    RULE_distance_restraint = 3
    RULE_dihedral_angle_restraint = 4
    RULE_angle_restraint = 5
    RULE_distance_statement = 6
    RULE_distance_assign = 7
    RULE_distance_assign_by_number = 8
    RULE_dihedral_angle_statement = 9
    RULE_dihedral_angle_assign = 10
    RULE_dihedral_angle_assign_by_number = 11
    RULE_angle_statement = 12
    RULE_angle_assign = 13
    RULE_angle_assign_by_number = 14
    RULE_fxdi_statement = 15
    RULE_fxdi_assign = 16
    RULE_fxdi_assign_by_number = 17
    RULE_fxta_statement = 18
    RULE_fxta_assign = 19
    RULE_fxta_assign_by_number = 20
    RULE_fxba_statement = 21
    RULE_fxba_assign = 22
    RULE_fxba_assign_by_number = 23
    RULE_fxhb_statement = 24
    RULE_fxhb_assign = 25
    RULE_fxhb_assign_by_number = 26
    RULE_selection = 27
    RULE_selection_expression = 28
    RULE_term = 29
    RULE_factor = 30
    RULE_number = 31
    RULE_number_f = 32
    RULE_parameter_statement = 33

    ruleNames =  [ "schrodinger_mr", "import_structure", "struct_statement", 
                   "distance_restraint", "dihedral_angle_restraint", "angle_restraint", 
                   "distance_statement", "distance_assign", "distance_assign_by_number", 
                   "dihedral_angle_statement", "dihedral_angle_assign", 
                   "dihedral_angle_assign_by_number", "angle_statement", 
                   "angle_assign", "angle_assign_by_number", "fxdi_statement", 
                   "fxdi_assign", "fxdi_assign_by_number", "fxta_statement", 
                   "fxta_assign", "fxta_assign_by_number", "fxba_statement", 
                   "fxba_assign", "fxba_assign_by_number", "fxhb_statement", 
                   "fxhb_assign", "fxhb_assign_by_number", "selection", 
                   "selection_expression", "term", "factor", "number", "number_f", 
                   "parameter_statement" ]

    EOF = Token.EOF
    Set=1
    Struct=2
    Dist=3
    Tors=4
    Angle=5
    End=6
    Atom1=7
    Atom2=8
    Atom3=9
    Atom4=10
    Lo=11
    Up=12
    Fc=13
    Target=14
    Comma=15
    FXDI=16
    FXBA=17
    FXTA=18
    FXHB=19
    Entry=20
    Molecule=21
    Chain=22
    Residue=23
    Atom=24
    Backbone=25
    Sidechain=26
    Water=27
    Methyl=28
    Amide=29
    Smarts=30
    Entry_name=31
    Molecule_number=32
    Molecule_modulo=33
    Molecule_entrynum=34
    Molecule_atoms=35
    Molecule_weight=36
    Chain_name=37
    Residue_name_or_number=38
    Residue_ptype=39
    Residue_mtype=40
    Residue_polarity=41
    Residue_secondary_structure=42
    Residue_position=43
    Residue_inscode=44
    Atom_ptype=45
    Atom_name=46
    Atom_number=47
    Atom_molnum=48
    Atom_entrynum=49
    Atom_mtype=50
    Atom_element=51
    Atom_attachements=52
    Atom_atomicnumber=53
    Atom_charge=54
    Atom_formalcharge=55
    Atom_displayed=56
    Atom_selected=57
    Or_op=58
    And_op=59
    Not_op=60
    Fillres_op=61
    Fillmol_op=62
    Within_op=63
    Beyond_op=64
    Withinbonds_op=65
    Beyondbonds_op=66
    Integer=67
    IntRange=68
    Float=69
    FloatRange=70
    Slash_quote_string=71
    SMCLN_COMMENT=72
    COMMENT=73
    Simple_name=74
    Simple_names=75
    Integers=76
    L_paren=77
    R_paren=78
    Lt_op=79
    Gt_op=80
    Leq_op=81
    Geq_op=82
    Equ_op=83
    SPACE=84
    ENCLOSE_COMMENT=85
    SECTION_COMMENT=86
    LINE_COMMENT=87
    Param_name=88
    Equ_op_SM=89
    SPACE_SM=90
    RETURN_SM=91
    End_SM=92
    Hydrophilic=93
    Hydrophobic=94
    Non_polar=95
    Polar=96
    Charged=97
    Positive=98
    Negative=99
    IGNORE_SPACE_PM=100
    Helix_or_strand=101
    Strand_or_loop=102
    Helix_or_loop=103
    Helix=104
    Strand=105
    Loop=106
    IGNORE_SPACE_SSM=107

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Schrodinger_mrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SchrodingerMRParser.EOF, 0)

        def import_structure(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Import_structureContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Import_structureContext,i)


        def distance_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Distance_restraintContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Distance_restraintContext,i)


        def dihedral_angle_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Dihedral_angle_restraintContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Dihedral_angle_restraintContext,i)


        def angle_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Angle_restraintContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Angle_restraintContext,i)


        def distance_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Distance_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Distance_assignContext,i)


        def dihedral_angle_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Dihedral_angle_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Dihedral_angle_assignContext,i)


        def angle_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Angle_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Angle_assignContext,i)


        def parameter_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Parameter_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Parameter_statementContext,i)


        def fxdi_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxdi_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxdi_statementContext,i)


        def fxta_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxta_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxta_statementContext,i)


        def fxba_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxba_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxba_statementContext,i)


        def fxhb_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxhb_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxhb_statementContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_schrodinger_mr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchrodinger_mr" ):
                listener.enterSchrodinger_mr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchrodinger_mr" ):
                listener.exitSchrodinger_mr(self)




    def schrodinger_mr(self):

        localctx = SchrodingerMRParser.Schrodinger_mrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_schrodinger_mr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 983102) != 0) or _la==77:
                self.state = 80
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 68
                    self.import_structure()
                    pass

                elif la_ == 2:
                    self.state = 69
                    self.distance_restraint()
                    pass

                elif la_ == 3:
                    self.state = 70
                    self.dihedral_angle_restraint()
                    pass

                elif la_ == 4:
                    self.state = 71
                    self.angle_restraint()
                    pass

                elif la_ == 5:
                    self.state = 72
                    self.distance_assign()
                    pass

                elif la_ == 6:
                    self.state = 73
                    self.dihedral_angle_assign()
                    pass

                elif la_ == 7:
                    self.state = 74
                    self.angle_assign()
                    pass

                elif la_ == 8:
                    self.state = 75
                    self.parameter_statement()
                    pass

                elif la_ == 9:
                    self.state = 76
                    self.fxdi_statement()
                    pass

                elif la_ == 10:
                    self.state = 77
                    self.fxta_statement()
                    pass

                elif la_ == 11:
                    self.state = 78
                    self.fxba_statement()
                    pass

                elif la_ == 12:
                    self.state = 79
                    self.fxhb_statement()
                    pass


                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 85
            self.match(SchrodingerMRParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Import_structureContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Struct(self):
            return self.getToken(SchrodingerMRParser.Struct, 0)

        def End_SM(self):
            return self.getToken(SchrodingerMRParser.End_SM, 0)

        def struct_statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Struct_statementContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Struct_statementContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_import_structure

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_structure" ):
                listener.enterImport_structure(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_structure" ):
                listener.exitImport_structure(self)




    def import_structure(self):

        localctx = SchrodingerMRParser.Import_structureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_import_structure)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(SchrodingerMRParser.Struct)
            self.state = 89 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 88
                self.struct_statement()
                self.state = 91 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==88):
                    break

            self.state = 93
            self.match(SchrodingerMRParser.End_SM)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Struct_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Param_name(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Param_name)
            else:
                return self.getToken(SchrodingerMRParser.Param_name, i)

        def Equ_op_SM(self):
            return self.getToken(SchrodingerMRParser.Equ_op_SM, 0)

        def RETURN_SM(self):
            return self.getToken(SchrodingerMRParser.RETURN_SM, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_struct_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStruct_statement" ):
                listener.enterStruct_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStruct_statement" ):
                listener.exitStruct_statement(self)




    def struct_statement(self):

        localctx = SchrodingerMRParser.Struct_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_struct_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(SchrodingerMRParser.Param_name)
            self.state = 96
            self.match(SchrodingerMRParser.Equ_op_SM)
            self.state = 97
            self.match(SchrodingerMRParser.Param_name)
            self.state = 98
            self.match(SchrodingerMRParser.RETURN_SM)
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

        def Dist(self):
            return self.getToken(SchrodingerMRParser.Dist, 0)

        def distance_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Distance_statementContext,0)


        def End(self):
            return self.getToken(SchrodingerMRParser.End, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_distance_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraint" ):
                listener.enterDistance_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraint" ):
                listener.exitDistance_restraint(self)




    def distance_restraint(self):

        localctx = SchrodingerMRParser.Distance_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_distance_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(SchrodingerMRParser.Dist)
            self.state = 101
            self.distance_statement()
            self.state = 102
            self.match(SchrodingerMRParser.End)
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

        def Tors(self):
            return self.getToken(SchrodingerMRParser.Tors, 0)

        def dihedral_angle_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Dihedral_angle_statementContext,0)


        def End(self):
            return self.getToken(SchrodingerMRParser.End, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_dihedral_angle_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_restraint" ):
                listener.enterDihedral_angle_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_restraint" ):
                listener.exitDihedral_angle_restraint(self)




    def dihedral_angle_restraint(self):

        localctx = SchrodingerMRParser.Dihedral_angle_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_dihedral_angle_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(SchrodingerMRParser.Tors)
            self.state = 105
            self.dihedral_angle_statement()
            self.state = 106
            self.match(SchrodingerMRParser.End)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Angle_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Angle(self):
            return self.getToken(SchrodingerMRParser.Angle, 0)

        def angle_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Angle_statementContext,0)


        def End(self):
            return self.getToken(SchrodingerMRParser.End, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_angle_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_restraint" ):
                listener.enterAngle_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_restraint" ):
                listener.exitAngle_restraint(self)




    def angle_restraint(self):

        localctx = SchrodingerMRParser.Angle_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_angle_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.match(SchrodingerMRParser.Angle)
            self.state = 109
            self.angle_statement()
            self.state = 110
            self.match(SchrodingerMRParser.End)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Parameter_statementContext,0)


        def Atom1(self):
            return self.getToken(SchrodingerMRParser.Atom1, 0)

        def Atom2(self):
            return self.getToken(SchrodingerMRParser.Atom2, 0)

        def Lo(self):
            return self.getToken(SchrodingerMRParser.Lo, 0)

        def Up(self):
            return self.getToken(SchrodingerMRParser.Up, 0)

        def Fc(self):
            return self.getToken(SchrodingerMRParser.Fc, 0)

        def distance_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Distance_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Distance_assignContext,i)


        def distance_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Distance_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Distance_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_distance_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_statement" ):
                listener.enterDistance_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_statement" ):
                listener.exitDistance_statement(self)




    def distance_statement(self):

        localctx = SchrodingerMRParser.Distance_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_distance_statement)
        self._la = 0 # Token type
        try:
            self.state = 128
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self.parameter_statement()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 113
                self.match(SchrodingerMRParser.Atom1)
                self.state = 114
                self.match(SchrodingerMRParser.Atom2)
                self.state = 115
                self.match(SchrodingerMRParser.Lo)
                self.state = 116
                self.match(SchrodingerMRParser.Up)
                self.state = 117
                self.match(SchrodingerMRParser.Fc)
                pass
            elif token in [77]:
                self.enterOuterAlt(localctx, 3)
                self.state = 119 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 118
                    self.distance_assign()
                    self.state = 121 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==77):
                        break

                pass
            elif token in [67]:
                self.enterOuterAlt(localctx, 4)
                self.state = 124 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 123
                    self.distance_assign_by_number()
                    self.state = 126 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==67):
                        break

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


    class Distance_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_distance_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_assign" ):
                listener.enterDistance_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_assign" ):
                listener.exitDistance_assign(self)




    def distance_assign(self):

        localctx = SchrodingerMRParser.Distance_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_distance_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.selection()
            self.state = 131
            self.selection()
            self.state = 132
            self.number()
            self.state = 133
            self.number()
            self.state = 134
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_distance_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_assign_by_number" ):
                listener.enterDistance_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_assign_by_number" ):
                listener.exitDistance_assign_by_number(self)




    def distance_assign_by_number(self):

        localctx = SchrodingerMRParser.Distance_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_distance_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(SchrodingerMRParser.Integer)
            self.state = 137
            self.match(SchrodingerMRParser.Integer)
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


    class Dihedral_angle_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Parameter_statementContext,0)


        def Atom1(self):
            return self.getToken(SchrodingerMRParser.Atom1, 0)

        def Atom2(self):
            return self.getToken(SchrodingerMRParser.Atom2, 0)

        def Atom3(self):
            return self.getToken(SchrodingerMRParser.Atom3, 0)

        def Atom4(self):
            return self.getToken(SchrodingerMRParser.Atom4, 0)

        def Target(self):
            return self.getToken(SchrodingerMRParser.Target, 0)

        def Fc(self):
            return self.getToken(SchrodingerMRParser.Fc, 0)

        def dihedral_angle_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Dihedral_angle_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Dihedral_angle_assignContext,i)


        def dihedral_angle_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Dihedral_angle_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Dihedral_angle_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_dihedral_angle_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_statement" ):
                listener.enterDihedral_angle_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_statement" ):
                listener.exitDihedral_angle_statement(self)




    def dihedral_angle_statement(self):

        localctx = SchrodingerMRParser.Dihedral_angle_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_dihedral_angle_statement)
        self._la = 0 # Token type
        try:
            self.state = 159
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 142
                self.parameter_statement()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 143
                self.match(SchrodingerMRParser.Atom1)
                self.state = 144
                self.match(SchrodingerMRParser.Atom2)
                self.state = 145
                self.match(SchrodingerMRParser.Atom3)
                self.state = 146
                self.match(SchrodingerMRParser.Atom4)
                self.state = 147
                self.match(SchrodingerMRParser.Target)
                self.state = 148
                self.match(SchrodingerMRParser.Fc)
                pass
            elif token in [77]:
                self.enterOuterAlt(localctx, 3)
                self.state = 150 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 149
                    self.dihedral_angle_assign()
                    self.state = 152 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==77):
                        break

                pass
            elif token in [67]:
                self.enterOuterAlt(localctx, 4)
                self.state = 155 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 154
                    self.dihedral_angle_assign_by_number()
                    self.state = 157 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==67):
                        break

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


    class Dihedral_angle_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_dihedral_angle_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_assign" ):
                listener.enterDihedral_angle_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_assign" ):
                listener.exitDihedral_angle_assign(self)




    def dihedral_angle_assign(self):

        localctx = SchrodingerMRParser.Dihedral_angle_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_dihedral_angle_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.selection()
            self.state = 162
            self.selection()
            self.state = 163
            self.selection()
            self.state = 164
            self.selection()
            self.state = 165
            self.number()
            self.state = 166
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_angle_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_dihedral_angle_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_angle_assign_by_number" ):
                listener.enterDihedral_angle_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_angle_assign_by_number" ):
                listener.exitDihedral_angle_assign_by_number(self)




    def dihedral_angle_assign_by_number(self):

        localctx = SchrodingerMRParser.Dihedral_angle_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_dihedral_angle_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self.match(SchrodingerMRParser.Integer)
            self.state = 169
            self.match(SchrodingerMRParser.Integer)
            self.state = 170
            self.match(SchrodingerMRParser.Integer)
            self.state = 171
            self.match(SchrodingerMRParser.Integer)
            self.state = 172
            self.number()
            self.state = 173
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Angle_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter_statement(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Parameter_statementContext,0)


        def Atom1(self):
            return self.getToken(SchrodingerMRParser.Atom1, 0)

        def Atom2(self):
            return self.getToken(SchrodingerMRParser.Atom2, 0)

        def Atom3(self):
            return self.getToken(SchrodingerMRParser.Atom3, 0)

        def Target(self):
            return self.getToken(SchrodingerMRParser.Target, 0)

        def Fc(self):
            return self.getToken(SchrodingerMRParser.Fc, 0)

        def angle_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Angle_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Angle_assignContext,i)


        def angle_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Angle_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Angle_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_angle_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_statement" ):
                listener.enterAngle_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_statement" ):
                listener.exitAngle_statement(self)




    def angle_statement(self):

        localctx = SchrodingerMRParser.Angle_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_angle_statement)
        self._la = 0 # Token type
        try:
            self.state = 191
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 175
                self.parameter_statement()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 176
                self.match(SchrodingerMRParser.Atom1)
                self.state = 177
                self.match(SchrodingerMRParser.Atom2)
                self.state = 178
                self.match(SchrodingerMRParser.Atom3)
                self.state = 179
                self.match(SchrodingerMRParser.Target)
                self.state = 180
                self.match(SchrodingerMRParser.Fc)
                pass
            elif token in [77]:
                self.enterOuterAlt(localctx, 3)
                self.state = 182 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 181
                    self.angle_assign()
                    self.state = 184 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==77):
                        break

                pass
            elif token in [67]:
                self.enterOuterAlt(localctx, 4)
                self.state = 187 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 186
                    self.angle_assign_by_number()
                    self.state = 189 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==67):
                        break

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


    class Angle_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_angle_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_assign" ):
                listener.enterAngle_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_assign" ):
                listener.exitAngle_assign(self)




    def angle_assign(self):

        localctx = SchrodingerMRParser.Angle_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_angle_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.selection()
            self.state = 194
            self.selection()
            self.state = 195
            self.selection()
            self.state = 196
            self.number()
            self.state = 197
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Angle_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_angle_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_assign_by_number" ):
                listener.enterAngle_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_assign_by_number" ):
                listener.exitAngle_assign_by_number(self)




    def angle_assign_by_number(self):

        localctx = SchrodingerMRParser.Angle_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_angle_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.match(SchrodingerMRParser.Integer)
            self.state = 200
            self.match(SchrodingerMRParser.Integer)
            self.state = 201
            self.match(SchrodingerMRParser.Integer)
            self.state = 202
            self.number()
            self.state = 203
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxdi_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fxdi_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxdi_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxdi_assignContext,i)


        def fxdi_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxdi_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxdi_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxdi_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxdi_statement" ):
                listener.enterFxdi_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxdi_statement" ):
                listener.exitFxdi_statement(self)




    def fxdi_statement(self):

        localctx = SchrodingerMRParser.Fxdi_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_fxdi_statement)
        try:
            self.state = 215
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 206 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 205
                        self.fxdi_assign()

                    else:
                        raise NoViableAltException(self)
                    self.state = 208 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 211 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 210
                        self.fxdi_assign_by_number()

                    else:
                        raise NoViableAltException(self)
                    self.state = 213 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxdi_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXDI(self):
            return self.getToken(SchrodingerMRParser.FXDI, 0)

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxdi_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxdi_assign" ):
                listener.enterFxdi_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxdi_assign" ):
                listener.exitFxdi_assign(self)




    def fxdi_assign(self):

        localctx = SchrodingerMRParser.Fxdi_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_fxdi_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
            self.match(SchrodingerMRParser.FXDI)
            self.state = 218
            self.selection()
            self.state = 219
            self.selection()
            self.state = 220
            self.match(SchrodingerMRParser.Integer)
            self.state = 221
            self.match(SchrodingerMRParser.Integer)
            self.state = 222
            self.number()
            self.state = 223
            self.number()
            self.state = 224
            self.number()
            self.state = 225
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxdi_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXDI(self):
            return self.getToken(SchrodingerMRParser.FXDI, 0)

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxdi_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxdi_assign_by_number" ):
                listener.enterFxdi_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxdi_assign_by_number" ):
                listener.exitFxdi_assign_by_number(self)




    def fxdi_assign_by_number(self):

        localctx = SchrodingerMRParser.Fxdi_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_fxdi_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            self.match(SchrodingerMRParser.FXDI)
            self.state = 228
            self.match(SchrodingerMRParser.Integer)
            self.state = 229
            self.match(SchrodingerMRParser.Integer)
            self.state = 230
            self.match(SchrodingerMRParser.Integer)
            self.state = 231
            self.match(SchrodingerMRParser.Integer)
            self.state = 232
            self.number()
            self.state = 233
            self.number()
            self.state = 234
            self.number()
            self.state = 235
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxta_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fxta_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxta_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxta_assignContext,i)


        def fxta_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxta_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxta_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxta_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxta_statement" ):
                listener.enterFxta_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxta_statement" ):
                listener.exitFxta_statement(self)




    def fxta_statement(self):

        localctx = SchrodingerMRParser.Fxta_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_fxta_statement)
        try:
            self.state = 247
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 238 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 237
                        self.fxta_assign()

                    else:
                        raise NoViableAltException(self)
                    self.state = 240 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 243 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 242
                        self.fxta_assign_by_number()

                    else:
                        raise NoViableAltException(self)
                    self.state = 245 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxta_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXTA(self):
            return self.getToken(SchrodingerMRParser.FXTA, 0)

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxta_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxta_assign" ):
                listener.enterFxta_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxta_assign" ):
                listener.exitFxta_assign(self)




    def fxta_assign(self):

        localctx = SchrodingerMRParser.Fxta_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_fxta_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 249
            self.match(SchrodingerMRParser.FXTA)
            self.state = 250
            self.selection()
            self.state = 251
            self.selection()
            self.state = 252
            self.selection()
            self.state = 253
            self.selection()
            self.state = 254
            self.number()
            self.state = 255
            self.number()
            self.state = 256
            self.number()
            self.state = 257
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxta_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXTA(self):
            return self.getToken(SchrodingerMRParser.FXTA, 0)

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxta_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxta_assign_by_number" ):
                listener.enterFxta_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxta_assign_by_number" ):
                listener.exitFxta_assign_by_number(self)




    def fxta_assign_by_number(self):

        localctx = SchrodingerMRParser.Fxta_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_fxta_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 259
            self.match(SchrodingerMRParser.FXTA)
            self.state = 260
            self.match(SchrodingerMRParser.Integer)
            self.state = 261
            self.match(SchrodingerMRParser.Integer)
            self.state = 262
            self.match(SchrodingerMRParser.Integer)
            self.state = 263
            self.match(SchrodingerMRParser.Integer)
            self.state = 264
            self.number()
            self.state = 265
            self.number()
            self.state = 266
            self.number()
            self.state = 267
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxba_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fxba_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxba_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxba_assignContext,i)


        def fxba_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxba_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxba_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxba_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxba_statement" ):
                listener.enterFxba_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxba_statement" ):
                listener.exitFxba_statement(self)




    def fxba_statement(self):

        localctx = SchrodingerMRParser.Fxba_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_fxba_statement)
        try:
            self.state = 279
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 270 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 269
                        self.fxba_assign()

                    else:
                        raise NoViableAltException(self)
                    self.state = 272 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 275 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 274
                        self.fxba_assign_by_number()

                    else:
                        raise NoViableAltException(self)
                    self.state = 277 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxba_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXBA(self):
            return self.getToken(SchrodingerMRParser.FXBA, 0)

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def Integer(self):
            return self.getToken(SchrodingerMRParser.Integer, 0)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxba_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxba_assign" ):
                listener.enterFxba_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxba_assign" ):
                listener.exitFxba_assign(self)




    def fxba_assign(self):

        localctx = SchrodingerMRParser.Fxba_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_fxba_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self.match(SchrodingerMRParser.FXBA)
            self.state = 282
            self.selection()
            self.state = 283
            self.selection()
            self.state = 284
            self.selection()
            self.state = 285
            self.match(SchrodingerMRParser.Integer)
            self.state = 286
            self.number()
            self.state = 287
            self.number()
            self.state = 288
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxba_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXBA(self):
            return self.getToken(SchrodingerMRParser.FXBA, 0)

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxba_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxba_assign_by_number" ):
                listener.enterFxba_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxba_assign_by_number" ):
                listener.exitFxba_assign_by_number(self)




    def fxba_assign_by_number(self):

        localctx = SchrodingerMRParser.Fxba_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_fxba_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self.match(SchrodingerMRParser.FXBA)
            self.state = 291
            self.match(SchrodingerMRParser.Integer)
            self.state = 292
            self.match(SchrodingerMRParser.Integer)
            self.state = 293
            self.match(SchrodingerMRParser.Integer)
            self.state = 294
            self.match(SchrodingerMRParser.Integer)
            self.state = 295
            self.number()
            self.state = 296
            self.number()
            self.state = 297
            self.number()
            self.state = 298
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxhb_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fxhb_assign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxhb_assignContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxhb_assignContext,i)


        def fxhb_assign_by_number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Fxhb_assign_by_numberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Fxhb_assign_by_numberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxhb_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxhb_statement" ):
                listener.enterFxhb_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxhb_statement" ):
                listener.exitFxhb_statement(self)




    def fxhb_statement(self):

        localctx = SchrodingerMRParser.Fxhb_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_fxhb_statement)
        try:
            self.state = 310
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 301 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 300
                        self.fxhb_assign()

                    else:
                        raise NoViableAltException(self)
                    self.state = 303 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 306 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 305
                        self.fxhb_assign_by_number()

                    else:
                        raise NoViableAltException(self)
                    self.state = 308 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,22,self._ctx)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxhb_assignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXHB(self):
            return self.getToken(SchrodingerMRParser.FXHB, 0)

        def selection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.SelectionContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.SelectionContext,i)


        def Integer(self):
            return self.getToken(SchrodingerMRParser.Integer, 0)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxhb_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxhb_assign" ):
                listener.enterFxhb_assign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxhb_assign" ):
                listener.exitFxhb_assign(self)




    def fxhb_assign(self):

        localctx = SchrodingerMRParser.Fxhb_assignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_fxhb_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 312
            self.match(SchrodingerMRParser.FXHB)
            self.state = 313
            self.selection()
            self.state = 314
            self.selection()
            self.state = 315
            self.selection()
            self.state = 316
            self.match(SchrodingerMRParser.Integer)
            self.state = 317
            self.number()
            self.state = 318
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Fxhb_assign_by_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FXHB(self):
            return self.getToken(SchrodingerMRParser.FXHB, 0)

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.NumberContext,i)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_fxhb_assign_by_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFxhb_assign_by_number" ):
                listener.enterFxhb_assign_by_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFxhb_assign_by_number" ):
                listener.exitFxhb_assign_by_number(self)




    def fxhb_assign_by_number(self):

        localctx = SchrodingerMRParser.Fxhb_assign_by_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_fxhb_assign_by_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self.match(SchrodingerMRParser.FXHB)
            self.state = 321
            self.match(SchrodingerMRParser.Integer)
            self.state = 322
            self.match(SchrodingerMRParser.Integer)
            self.state = 323
            self.match(SchrodingerMRParser.Integer)
            self.state = 324
            self.match(SchrodingerMRParser.Integer)
            self.state = 325
            self.number()
            self.state = 326
            self.number()
            self.state = 327
            self.number()
            self.state = 328
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_paren(self):
            return self.getToken(SchrodingerMRParser.L_paren, 0)

        def selection_expression(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Selection_expressionContext,0)


        def R_paren(self):
            return self.getToken(SchrodingerMRParser.R_paren, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_selection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelection" ):
                listener.enterSelection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelection" ):
                listener.exitSelection(self)




    def selection(self):

        localctx = SchrodingerMRParser.SelectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_selection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.match(SchrodingerMRParser.L_paren)
            self.state = 331
            self.selection_expression()
            self.state = 332
            self.match(SchrodingerMRParser.R_paren)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Selection_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.TermContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.TermContext,i)


        def Or_op(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Or_op)
            else:
                return self.getToken(SchrodingerMRParser.Or_op, i)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_selection_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelection_expression" ):
                listener.enterSelection_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelection_expression" ):
                listener.exitSelection_expression(self)




    def selection_expression(self):

        localctx = SchrodingerMRParser.Selection_expressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_selection_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 334
            self.term()
            self.state = 339
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==58:
                self.state = 335
                self.match(SchrodingerMRParser.Or_op)
                self.state = 336
                self.term()
                self.state = 341
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.FactorContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.FactorContext,i)


        def And_op(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.And_op)
            else:
                return self.getToken(SchrodingerMRParser.And_op, i)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)




    def term(self):

        localctx = SchrodingerMRParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 342
            self.factor()
            self.state = 349
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,26,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 344
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==59:
                        self.state = 343
                        self.match(SchrodingerMRParser.And_op)


                    self.state = 346
                    self.factor() 
                self.state = 351
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,26,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_paren(self):
            return self.getToken(SchrodingerMRParser.L_paren, 0)

        def selection_expression(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Selection_expressionContext,0)


        def R_paren(self):
            return self.getToken(SchrodingerMRParser.R_paren, 0)

        def Entry(self):
            return self.getToken(SchrodingerMRParser.Entry, 0)

        def Entry_name(self):
            return self.getToken(SchrodingerMRParser.Entry_name, 0)

        def Simple_names(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Simple_names)
            else:
                return self.getToken(SchrodingerMRParser.Simple_names, i)

        def Simple_name(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Simple_name)
            else:
                return self.getToken(SchrodingerMRParser.Simple_name, i)

        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Comma)
            else:
                return self.getToken(SchrodingerMRParser.Comma, i)

        def Molecule(self):
            return self.getToken(SchrodingerMRParser.Molecule, 0)

        def Molecule_number(self):
            return self.getToken(SchrodingerMRParser.Molecule_number, 0)

        def Integers(self):
            return self.getToken(SchrodingerMRParser.Integers, 0)

        def IntRange(self):
            return self.getToken(SchrodingerMRParser.IntRange, 0)

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(SchrodingerMRParser.Integer)
            else:
                return self.getToken(SchrodingerMRParser.Integer, i)

        def Molecule_modulo(self):
            return self.getToken(SchrodingerMRParser.Molecule_modulo, 0)

        def Molecule_entrynum(self):
            return self.getToken(SchrodingerMRParser.Molecule_entrynum, 0)

        def Molecule_atoms(self):
            return self.getToken(SchrodingerMRParser.Molecule_atoms, 0)

        def Equ_op(self):
            return self.getToken(SchrodingerMRParser.Equ_op, 0)

        def Lt_op(self):
            return self.getToken(SchrodingerMRParser.Lt_op, 0)

        def Gt_op(self):
            return self.getToken(SchrodingerMRParser.Gt_op, 0)

        def Leq_op(self):
            return self.getToken(SchrodingerMRParser.Leq_op, 0)

        def Geq_op(self):
            return self.getToken(SchrodingerMRParser.Geq_op, 0)

        def Molecule_weight(self):
            return self.getToken(SchrodingerMRParser.Molecule_weight, 0)

        def Chain(self):
            return self.getToken(SchrodingerMRParser.Chain, 0)

        def Chain_name(self):
            return self.getToken(SchrodingerMRParser.Chain_name, 0)

        def Residue(self):
            return self.getToken(SchrodingerMRParser.Residue, 0)

        def Residue_name_or_number(self):
            return self.getToken(SchrodingerMRParser.Residue_name_or_number, 0)

        def Residue_ptype(self):
            return self.getToken(SchrodingerMRParser.Residue_ptype, 0)

        def Residue_mtype(self):
            return self.getToken(SchrodingerMRParser.Residue_mtype, 0)

        def Residue_polarity(self):
            return self.getToken(SchrodingerMRParser.Residue_polarity, 0)

        def Hydrophilic(self):
            return self.getToken(SchrodingerMRParser.Hydrophilic, 0)

        def Hydrophobic(self):
            return self.getToken(SchrodingerMRParser.Hydrophobic, 0)

        def Non_polar(self):
            return self.getToken(SchrodingerMRParser.Non_polar, 0)

        def Polar(self):
            return self.getToken(SchrodingerMRParser.Polar, 0)

        def Charged(self):
            return self.getToken(SchrodingerMRParser.Charged, 0)

        def Positive(self):
            return self.getToken(SchrodingerMRParser.Positive, 0)

        def Negative(self):
            return self.getToken(SchrodingerMRParser.Negative, 0)

        def Residue_secondary_structure(self):
            return self.getToken(SchrodingerMRParser.Residue_secondary_structure, 0)

        def Helix_or_strand(self):
            return self.getToken(SchrodingerMRParser.Helix_or_strand, 0)

        def Strand_or_loop(self):
            return self.getToken(SchrodingerMRParser.Strand_or_loop, 0)

        def Helix_or_loop(self):
            return self.getToken(SchrodingerMRParser.Helix_or_loop, 0)

        def Helix(self):
            return self.getToken(SchrodingerMRParser.Helix, 0)

        def Strand(self):
            return self.getToken(SchrodingerMRParser.Strand, 0)

        def Loop(self):
            return self.getToken(SchrodingerMRParser.Loop, 0)

        def Residue_position(self):
            return self.getToken(SchrodingerMRParser.Residue_position, 0)

        def number_f(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SchrodingerMRParser.Number_fContext)
            else:
                return self.getTypedRuleContext(SchrodingerMRParser.Number_fContext,i)


        def Residue_inscode(self):
            return self.getToken(SchrodingerMRParser.Residue_inscode, 0)

        def Atom_ptype(self):
            return self.getToken(SchrodingerMRParser.Atom_ptype, 0)

        def Atom_name(self):
            return self.getToken(SchrodingerMRParser.Atom_name, 0)

        def Atom(self):
            return self.getToken(SchrodingerMRParser.Atom, 0)

        def Atom_number(self):
            return self.getToken(SchrodingerMRParser.Atom_number, 0)

        def Atom_molnum(self):
            return self.getToken(SchrodingerMRParser.Atom_molnum, 0)

        def Atom_entrynum(self):
            return self.getToken(SchrodingerMRParser.Atom_entrynum, 0)

        def Atom_mtype(self):
            return self.getToken(SchrodingerMRParser.Atom_mtype, 0)

        def Atom_element(self):
            return self.getToken(SchrodingerMRParser.Atom_element, 0)

        def Atom_attachements(self):
            return self.getToken(SchrodingerMRParser.Atom_attachements, 0)

        def Atom_atomicnumber(self):
            return self.getToken(SchrodingerMRParser.Atom_atomicnumber, 0)

        def Atom_charge(self):
            return self.getToken(SchrodingerMRParser.Atom_charge, 0)

        def FloatRange(self):
            return self.getToken(SchrodingerMRParser.FloatRange, 0)

        def Float(self):
            return self.getToken(SchrodingerMRParser.Float, 0)

        def Atom_formalcharge(self):
            return self.getToken(SchrodingerMRParser.Atom_formalcharge, 0)

        def Atom_displayed(self):
            return self.getToken(SchrodingerMRParser.Atom_displayed, 0)

        def Atom_selected(self):
            return self.getToken(SchrodingerMRParser.Atom_selected, 0)

        def Fillres_op(self):
            return self.getToken(SchrodingerMRParser.Fillres_op, 0)

        def factor(self):
            return self.getTypedRuleContext(SchrodingerMRParser.FactorContext,0)


        def Fillmol_op(self):
            return self.getToken(SchrodingerMRParser.Fillmol_op, 0)

        def Within_op(self):
            return self.getToken(SchrodingerMRParser.Within_op, 0)

        def Beyond_op(self):
            return self.getToken(SchrodingerMRParser.Beyond_op, 0)

        def Withinbonds_op(self):
            return self.getToken(SchrodingerMRParser.Withinbonds_op, 0)

        def Beyondbonds_op(self):
            return self.getToken(SchrodingerMRParser.Beyondbonds_op, 0)

        def Backbone(self):
            return self.getToken(SchrodingerMRParser.Backbone, 0)

        def Sidechain(self):
            return self.getToken(SchrodingerMRParser.Sidechain, 0)

        def Water(self):
            return self.getToken(SchrodingerMRParser.Water, 0)

        def Methyl(self):
            return self.getToken(SchrodingerMRParser.Methyl, 0)

        def Amide(self):
            return self.getToken(SchrodingerMRParser.Amide, 0)

        def Smarts(self):
            return self.getToken(SchrodingerMRParser.Smarts, 0)

        def Slash_quote_string(self):
            return self.getToken(SchrodingerMRParser.Slash_quote_string, 0)

        def Not_op(self):
            return self.getToken(SchrodingerMRParser.Not_op, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)




    def factor(self):

        localctx = SchrodingerMRParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 582
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [77]:
                self.enterOuterAlt(localctx, 1)
                self.state = 352
                self.match(SchrodingerMRParser.L_paren)
                self.state = 353
                self.selection_expression()
                self.state = 354
                self.match(SchrodingerMRParser.R_paren)
                pass
            elif token in [20, 31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 356
                _la = self._input.LA(1)
                if not(_la==20 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()

                self.state = 357
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 362
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 358
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 359
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 364
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [21, 32]:
                self.enterOuterAlt(localctx, 3)
                self.state = 365
                _la = self._input.LA(1)
                if not(_la==21 or _la==32):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 376
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [76]:
                    self.state = 366
                    self.match(SchrodingerMRParser.Integers)
                    pass
                elif token in [68]:
                    self.state = 367
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 368
                    self.match(SchrodingerMRParser.Integer)
                    self.state = 373
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==15:
                        self.state = 369
                        self.match(SchrodingerMRParser.Comma)
                        self.state = 370
                        self.match(SchrodingerMRParser.Integer)
                        self.state = 375
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [33]:
                self.enterOuterAlt(localctx, 4)
                self.state = 378
                self.match(SchrodingerMRParser.Molecule_modulo)
                self.state = 379
                self.match(SchrodingerMRParser.Integer)
                self.state = 380
                self.match(SchrodingerMRParser.Integer)
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 5)
                self.state = 381
                self.match(SchrodingerMRParser.Molecule_entrynum)
                self.state = 382
                self.match(SchrodingerMRParser.Integer)
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 6)
                self.state = 383
                self.match(SchrodingerMRParser.Molecule_atoms)
                self.state = 388
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 384
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 385
                    self.match(SchrodingerMRParser.Integer)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 386
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 387
                    self.match(SchrodingerMRParser.Integer)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 7)
                self.state = 390
                self.match(SchrodingerMRParser.Molecule_weight)
                self.state = 395
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 391
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 392
                    self.match(SchrodingerMRParser.Integer)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 393
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 394
                    self.match(SchrodingerMRParser.Integer)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [22, 37]:
                self.enterOuterAlt(localctx, 8)
                self.state = 397
                _la = self._input.LA(1)
                if not(_la==22 or _la==37):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()

                self.state = 398
                _la = self._input.LA(1)
                if not(((((_la - 67)) & ~0x3f) == 0 and ((1 << (_la - 67)) & 385) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 403
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 399
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 400
                    _la = self._input.LA(1)
                    if not(((((_la - 67)) & ~0x3f) == 0 and ((1 << (_la - 67)) & 385) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 405
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [23, 38]:
                self.enterOuterAlt(localctx, 9)
                self.state = 406
                _la = self._input.LA(1)
                if not(_la==23 or _la==38):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 421
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [67, 68, 79, 80, 81, 82, 83]:
                    self.state = 411
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [68]:
                        self.state = 407
                        self.match(SchrodingerMRParser.IntRange)
                        pass
                    elif token in [67]:
                        self.state = 408
                        self.match(SchrodingerMRParser.Integer)
                        pass
                    elif token in [79, 80, 81, 82, 83]:
                        self.state = 409
                        _la = self._input.LA(1)
                        if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 410
                        self.match(SchrodingerMRParser.Integer)
                        pass
                    else:
                        raise NoViableAltException(self)

                    pass
                elif token in [74, 75]:
                    self.state = 413
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 418
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==15:
                        self.state = 414
                        self.match(SchrodingerMRParser.Comma)
                        self.state = 415
                        _la = self._input.LA(1)
                        if not(_la==74 or _la==75):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 420
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 10)
                self.state = 423
                self.match(SchrodingerMRParser.Residue_ptype)

                self.state = 424
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 429
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 425
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 426
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 431
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 11)
                self.state = 432
                self.match(SchrodingerMRParser.Residue_mtype)

                self.state = 433
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 438
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 434
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 435
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 440
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 12)
                self.state = 441
                self.match(SchrodingerMRParser.Residue_polarity)
                self.state = 442
                _la = self._input.LA(1)
                if not(((((_la - 93)) & ~0x3f) == 0 and ((1 << (_la - 93)) & 127) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 13)
                self.state = 443
                self.match(SchrodingerMRParser.Residue_secondary_structure)
                self.state = 444
                _la = self._input.LA(1)
                if not(((((_la - 101)) & ~0x3f) == 0 and ((1 << (_la - 101)) & 63) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 14)
                self.state = 445
                self.match(SchrodingerMRParser.Residue_position)
                self.state = 446
                self.number_f()
                self.state = 447
                self.number_f()
                pass
            elif token in [44]:
                self.enterOuterAlt(localctx, 15)
                self.state = 449
                self.match(SchrodingerMRParser.Residue_inscode)
                self.state = 450
                self.match(SchrodingerMRParser.Simple_name)
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 16)
                self.state = 451
                self.match(SchrodingerMRParser.Atom_ptype)

                self.state = 452
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 457
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 453
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 454
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 459
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 17)
                self.state = 460
                self.match(SchrodingerMRParser.Atom_name)

                self.state = 461
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 466
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 462
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 463
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 468
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [24, 47]:
                self.enterOuterAlt(localctx, 18)
                self.state = 469
                _la = self._input.LA(1)
                if not(_la==24 or _la==47):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 479
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 470
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 471
                    self.match(SchrodingerMRParser.Integer)
                    self.state = 476
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==15:
                        self.state = 472
                        self.match(SchrodingerMRParser.Comma)
                        self.state = 473
                        self.match(SchrodingerMRParser.Integer)
                        self.state = 478
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 19)
                self.state = 481
                self.match(SchrodingerMRParser.Atom_molnum)
                self.state = 491
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 482
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 483
                    self.match(SchrodingerMRParser.Integer)
                    self.state = 488
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==15:
                        self.state = 484
                        self.match(SchrodingerMRParser.Comma)
                        self.state = 485
                        self.match(SchrodingerMRParser.Integer)
                        self.state = 490
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 20)
                self.state = 493
                self.match(SchrodingerMRParser.Atom_entrynum)
                self.state = 503
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 494
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 495
                    self.match(SchrodingerMRParser.Integer)
                    self.state = 500
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==15:
                        self.state = 496
                        self.match(SchrodingerMRParser.Comma)
                        self.state = 497
                        self.match(SchrodingerMRParser.Integer)
                        self.state = 502
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [50]:
                self.enterOuterAlt(localctx, 21)
                self.state = 505
                self.match(SchrodingerMRParser.Atom_mtype)

                self.state = 506
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 511
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 507
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 508
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 513
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 22)
                self.state = 514
                self.match(SchrodingerMRParser.Atom_element)

                self.state = 515
                _la = self._input.LA(1)
                if not(_la==74 or _la==75):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 520
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==15:
                    self.state = 516
                    self.match(SchrodingerMRParser.Comma)
                    self.state = 517
                    _la = self._input.LA(1)
                    if not(_la==74 or _la==75):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 522
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [52]:
                self.enterOuterAlt(localctx, 23)
                self.state = 523
                self.match(SchrodingerMRParser.Atom_attachements)
                self.state = 528
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 524
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 525
                    self.match(SchrodingerMRParser.Integer)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 526
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 527
                    self.match(SchrodingerMRParser.Integer)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [53]:
                self.enterOuterAlt(localctx, 24)
                self.state = 530
                self.match(SchrodingerMRParser.Atom_atomicnumber)
                self.state = 535
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 531
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 532
                    self.match(SchrodingerMRParser.Integer)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 533
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 534
                    self.match(SchrodingerMRParser.Integer)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 25)
                self.state = 537
                self.match(SchrodingerMRParser.Atom_charge)
                self.state = 542
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [70]:
                    self.state = 538
                    self.match(SchrodingerMRParser.FloatRange)
                    pass
                elif token in [69]:
                    self.state = 539
                    self.match(SchrodingerMRParser.Float)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 540
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 541
                    self.match(SchrodingerMRParser.Float)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 26)
                self.state = 544
                self.match(SchrodingerMRParser.Atom_formalcharge)
                self.state = 549
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [68]:
                    self.state = 545
                    self.match(SchrodingerMRParser.IntRange)
                    pass
                elif token in [67]:
                    self.state = 546
                    self.match(SchrodingerMRParser.Integer)
                    pass
                elif token in [79, 80, 81, 82, 83]:
                    self.state = 547
                    _la = self._input.LA(1)
                    if not(((((_la - 79)) & ~0x3f) == 0 and ((1 << (_la - 79)) & 31) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 548
                    self.match(SchrodingerMRParser.Integer)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [56]:
                self.enterOuterAlt(localctx, 27)
                self.state = 551
                self.match(SchrodingerMRParser.Atom_displayed)
                pass
            elif token in [57]:
                self.enterOuterAlt(localctx, 28)
                self.state = 552
                self.match(SchrodingerMRParser.Atom_selected)
                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 29)
                self.state = 553
                self.match(SchrodingerMRParser.Fillres_op)
                self.state = 554
                self.factor()
                pass
            elif token in [62]:
                self.enterOuterAlt(localctx, 30)
                self.state = 555
                self.match(SchrodingerMRParser.Fillmol_op)
                self.state = 556
                self.factor()
                pass
            elif token in [63]:
                self.enterOuterAlt(localctx, 31)
                self.state = 557
                self.match(SchrodingerMRParser.Within_op)
                self.state = 558
                self.number_f()
                self.state = 559
                self.factor()
                pass
            elif token in [64]:
                self.enterOuterAlt(localctx, 32)
                self.state = 561
                self.match(SchrodingerMRParser.Beyond_op)
                self.state = 562
                self.number_f()
                self.state = 563
                self.factor()
                pass
            elif token in [65]:
                self.enterOuterAlt(localctx, 33)
                self.state = 565
                self.match(SchrodingerMRParser.Withinbonds_op)
                self.state = 566
                self.match(SchrodingerMRParser.Integer)
                self.state = 567
                self.factor()
                pass
            elif token in [66]:
                self.enterOuterAlt(localctx, 34)
                self.state = 568
                self.match(SchrodingerMRParser.Beyondbonds_op)
                self.state = 569
                self.match(SchrodingerMRParser.Integer)
                self.state = 570
                self.factor()
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 35)
                self.state = 571
                self.match(SchrodingerMRParser.Backbone)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 36)
                self.state = 572
                self.match(SchrodingerMRParser.Sidechain)
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 37)
                self.state = 573
                self.match(SchrodingerMRParser.Water)
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 38)
                self.state = 574
                self.match(SchrodingerMRParser.Methyl)
                pass
            elif token in [29]:
                self.enterOuterAlt(localctx, 39)
                self.state = 575
                self.match(SchrodingerMRParser.Amide)
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 40)
                self.state = 576
                self.match(SchrodingerMRParser.Smarts)
                self.state = 577
                self.match(SchrodingerMRParser.Simple_name)
                pass
            elif token in [71]:
                self.enterOuterAlt(localctx, 41)
                self.state = 578
                self.match(SchrodingerMRParser.Slash_quote_string)
                pass
            elif token in [60]:
                self.enterOuterAlt(localctx, 42)
                self.state = 579
                self.match(SchrodingerMRParser.Not_op)
                self.state = 580
                self.factor()
                pass
            elif token in [74]:
                self.enterOuterAlt(localctx, 43)
                self.state = 581
                self.match(SchrodingerMRParser.Simple_name)
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


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(SchrodingerMRParser.Float, 0)

        def Integer(self):
            return self.getToken(SchrodingerMRParser.Integer, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = SchrodingerMRParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 584
            _la = self._input.LA(1)
            if not(_la==67 or _la==69):
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


    class Number_fContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(SchrodingerMRParser.Float, 0)

        def Integer(self):
            return self.getToken(SchrodingerMRParser.Integer, 0)

        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_number_f

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber_f" ):
                listener.enterNumber_f(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber_f" ):
                listener.exitNumber_f(self)




    def number_f(self):

        localctx = SchrodingerMRParser.Number_fContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_number_f)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 586
            _la = self._input.LA(1)
            if not(_la==67 or _la==69):
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


    class Parameter_statementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Set(self):
            return self.getToken(SchrodingerMRParser.Set, 0)

        def Simple_name(self):
            return self.getToken(SchrodingerMRParser.Simple_name, 0)

        def selection_expression(self):
            return self.getTypedRuleContext(SchrodingerMRParser.Selection_expressionContext,0)


        def getRuleIndex(self):
            return SchrodingerMRParser.RULE_parameter_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameter_statement" ):
                listener.enterParameter_statement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameter_statement" ):
                listener.exitParameter_statement(self)




    def parameter_statement(self):

        localctx = SchrodingerMRParser.Parameter_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_parameter_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 588
            self.match(SchrodingerMRParser.Set)
            self.state = 589
            self.match(SchrodingerMRParser.Simple_name)
            self.state = 590
            self.selection_expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





