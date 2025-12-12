##
# File: BaseStackedMRParserListener.py
# Date: 23-Oct-2025
#
# Updates:
""" ParserLister class for Generic Stacked MR files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import re
import itertools
import numpy
import copy
import collections
import functools
import random

from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import (CifReader,
                                              SYMBOLS_ELEMENT)
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toRegEx,
                                                       toNefEx,
                                                       coordAssemblyChecker,
                                                       extendCoordChainsForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       translateToStdAtomNameNoRef,
                                                       translateToStdAtomNameWithRef,
                                                       backTranslateFromStdResName,
                                                       isCyclicPolymer,
                                                       getStructConnPtnr,
                                                       getWatsonCrickPtnr,
                                                       getRestraintName,
                                                       contentSubtypeOf,
                                                       guessCompIdFromAtomId,
                                                       guessCompIdFromAtomIdWoLimit,
                                                       incListIdCounter,
                                                       decListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       THRESHOLD_FOR_CIRCULAR_SHIFT,
                                                       MIN_EXT_SEQ_FOR_ATOM_SEL_ERR,
                                                       PLANE_LIKE_LOWER_LIMIT,
                                                       PLANE_LIKE_UPPER_LIMIT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR,
                                                       RDC_RESTRAINT_RANGE,
                                                       RDC_RESTRAINT_ERROR,
                                                       CSA_RESTRAINT_RANGE,
                                                       CSA_RESTRAINT_ERROR,
                                                       PCS_RESTRAINT_RANGE,
                                                       PCS_RESTRAINT_ERROR,
                                                       CCR_RESTRAINT_RANGE,
                                                       CCR_RESTRAINT_ERROR,
                                                       PRE_RESTRAINT_RANGE,
                                                       PRE_RESTRAINT_ERROR,
                                                       CS_RESTRAINT_RANGE,
                                                       CS_RESTRAINT_ERROR,
                                                       T1T2_RESTRAINT_RANGE,
                                                       T1T2_RESTRAINT_ERROR,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_UP,
                                                       DIST_AMBIG_MED,
                                                       DIST_AMBIG_UNCERT,
                                                       XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                                       XPLOR_NITROXIDE_NAMES,
                                                       NITROOXIDE_ANCHOR_RES_NAMES,
                                                       CARTN_DATA_ITEMS)
    from wwpdb.utils.nmr.nef.NEFTranslator import (NEFTranslator,
                                                   PARAMAGNETIC_ELEMENTS,
                                                   FERROMAGNETIC_ELEMENTS,
                                                   LANTHANOID_ELEMENTS)
    from wwpdb.utils.nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                                           LARGE_ASYM_ID,
                                           monDict3,
                                           emptyValue,
                                           protonBeginCode,
                                           pseProBeginCode,
                                           aminoProtonCode,
                                           carboxylCode,
                                           jcoupBbPairCode,
                                           zincIonCode,
                                           calciumIonCode,
                                           deepcopy,
                                           indexToLetter,
                                           updatePolySeqRst,
                                           updatePolySeqRstAmbig,
                                           mergePolySeqRstAmbig,
                                           sortPolySeqRst,
                                           updateSeqAtmRst,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           trimSequenceAlignment,
                                           splitPolySeqRstForMultimers,
                                           splitPolySeqRstForExactNoes,
                                           splitPolySeqRstForNonPoly,
                                           splitPolySeqRstForBranched,
                                           retrieveAtomIdentFromMRMap,
                                           retrieveAtomIdFromMRMap,
                                           retrieveOriginalSeqIdFromMRMap,
                                           retrieveRemappedSeqId,
                                           retrieveRemappedChainId,
                                           retrieveRemappedNonPoly)
    from wwpdb.utils.nmr.CifToNmrStar import (get_first_sf_tag,
                                              set_sf_tag)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance,
                                                dist_error,
                                                angle_target_values,
                                                dihedral_angle,
                                                angle_error)
except ImportError:
    from nmr.io.CifReader import (CifReader,
                                  SYMBOLS_ELEMENT)
    from nmr.mr.ParserListenerUtil import (toRegEx,
                                           toNefEx,
                                           coordAssemblyChecker,
                                           extendCoordChainsForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           translateToStdAtomNameNoRef,
                                           translateToStdAtomNameWithRef,
                                           backTranslateFromStdResName,
                                           isCyclicPolymer,
                                           getStructConnPtnr,
                                           getRestraintName,
                                           getWatsonCrickPtnr,
                                           contentSubtypeOf,
                                           guessCompIdFromAtomId,
                                           guessCompIdFromAtomIdWoLimit,
                                           incListIdCounter,
                                           decListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           THRESHOLD_FOR_CIRCULAR_SHIFT,
                                           MIN_EXT_SEQ_FOR_ATOM_SEL_ERR,
                                           PLANE_LIKE_LOWER_LIMIT,
                                           PLANE_LIKE_UPPER_LIMIT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR,
                                           RDC_RESTRAINT_RANGE,
                                           RDC_RESTRAINT_ERROR,
                                           CSA_RESTRAINT_RANGE,
                                           CSA_RESTRAINT_ERROR,
                                           PCS_RESTRAINT_RANGE,
                                           PCS_RESTRAINT_ERROR,
                                           CCR_RESTRAINT_RANGE,
                                           CCR_RESTRAINT_ERROR,
                                           PRE_RESTRAINT_RANGE,
                                           PRE_RESTRAINT_ERROR,
                                           CS_RESTRAINT_RANGE,
                                           CS_RESTRAINT_ERROR,
                                           T1T2_RESTRAINT_RANGE,
                                           T1T2_RESTRAINT_ERROR,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_UP,
                                           DIST_AMBIG_MED,
                                           DIST_AMBIG_UNCERT,
                                           XPLOR_RDC_PRINCIPAL_AXIS_NAMES,
                                           XPLOR_NITROXIDE_NAMES,
                                           NITROOXIDE_ANCHOR_RES_NAMES,
                                           CARTN_DATA_ITEMS)
    from nmr.nef.NEFTranslator import (NEFTranslator,
                                       PARAMAGNETIC_ELEMENTS,
                                       FERROMAGNETIC_ELEMENTS,
                                       LANTHANOID_ELEMENTS)
    from nmr.AlignUtil import (LEN_LARGE_ASYM_ID,
                               LARGE_ASYM_ID,
                               monDict3,
                               emptyValue,
                               protonBeginCode,
                               pseProBeginCode,
                               aminoProtonCode,
                               carboxylCode,
                               jcoupBbPairCode,
                               zincIonCode,
                               calciumIonCode,
                               deepcopy,
                               indexToLetter,
                               updatePolySeqRst,
                               updatePolySeqRstAmbig,
                               mergePolySeqRstAmbig,
                               sortPolySeqRst,
                               updateSeqAtmRst,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               trimSequenceAlignment,
                               splitPolySeqRstForMultimers,
                               splitPolySeqRstForExactNoes,
                               splitPolySeqRstForNonPoly,
                               splitPolySeqRstForBranched,
                               retrieveAtomIdentFromMRMap,
                               retrieveAtomIdFromMRMap,
                               retrieveOriginalSeqIdFromMRMap,
                               retrieveRemappedSeqId,
                               retrieveRemappedChainId,
                               retrieveRemappedNonPoly)
    from nmr.CifToNmrStar import (get_first_sf_tag,
                                  set_sf_tag)
    from nmr.NmrVrptUtility import (to_np_array,
                                    distance,
                                    dist_error,
                                    angle_target_values,
                                    dihedral_angle,
                                    angle_error)


DIST_RANGE_MIN = DIST_RESTRAINT_RANGE['min_inclusive']
DIST_RANGE_MAX = DIST_RESTRAINT_RANGE['max_inclusive']

DIST_ERROR_MIN = DIST_RESTRAINT_ERROR['min_exclusive']
DIST_ERROR_MAX = DIST_RESTRAINT_ERROR['max_exclusive']


ANGLE_RANGE_MIN = ANGLE_RESTRAINT_RANGE['min_inclusive']
ANGLE_RANGE_MAX = ANGLE_RESTRAINT_RANGE['max_inclusive']

ANGLE_ERROR_MIN = ANGLE_RESTRAINT_ERROR['min_exclusive']
ANGLE_ERROR_MAX = ANGLE_RESTRAINT_ERROR['max_exclusive']


RDC_RANGE_MIN = RDC_RESTRAINT_RANGE['min_inclusive']
RDC_RANGE_MAX = RDC_RESTRAINT_RANGE['max_inclusive']

RDC_ERROR_MIN = RDC_RESTRAINT_ERROR['min_exclusive']
RDC_ERROR_MAX = RDC_RESTRAINT_ERROR['max_exclusive']


CSA_RANGE_MIN = CSA_RESTRAINT_RANGE['min_inclusive']
CSA_RANGE_MAX = CSA_RESTRAINT_RANGE['max_inclusive']

CSA_ERROR_MIN = CSA_RESTRAINT_ERROR['min_exclusive']
CSA_ERROR_MAX = CSA_RESTRAINT_ERROR['max_exclusive']


PCS_RANGE_MIN = PCS_RESTRAINT_RANGE['min_inclusive']
PCS_RANGE_MAX = PCS_RESTRAINT_RANGE['max_inclusive']

PCS_ERROR_MIN = PCS_RESTRAINT_ERROR['min_exclusive']
PCS_ERROR_MAX = PCS_RESTRAINT_ERROR['max_exclusive']


CCR_RANGE_MIN = CCR_RESTRAINT_RANGE['min_inclusive']
CCR_RANGE_MAX = CCR_RESTRAINT_RANGE['max_inclusive']

CCR_ERROR_MIN = CCR_RESTRAINT_ERROR['min_exclusive']
CCR_ERROR_MAX = CCR_RESTRAINT_ERROR['max_exclusive']


PRE_RANGE_MIN = PRE_RESTRAINT_RANGE['min_inclusive']
PRE_RANGE_MAX = PRE_RESTRAINT_RANGE['max_inclusive']

PRE_ERROR_MIN = PRE_RESTRAINT_ERROR['min_exclusive']
PRE_ERROR_MAX = PRE_RESTRAINT_ERROR['max_exclusive']


CS_RANGE_MIN = CS_RESTRAINT_RANGE['min_inclusive']
CS_RANGE_MAX = CS_RESTRAINT_RANGE['max_inclusive']

CS_ERROR_MIN = CS_RESTRAINT_ERROR['min_exclusive']
CS_ERROR_MAX = CS_RESTRAINT_ERROR['max_exclusive']


T1T2_RANGE_MIN = T1T2_RESTRAINT_RANGE['min_inclusive']
T1T2_RANGE_MAX = T1T2_RESTRAINT_RANGE['max_inclusive']

T1T2_ERROR_MIN = T1T2_RESTRAINT_ERROR['min_exclusive']
T1T2_ERROR_MAX = T1T2_RESTRAINT_ERROR['max_exclusive']


class BaseStackedMRParserListener():
    __slots__ = ('__class_name__',
                 '__version__',
                 '__verbose',
                 '__lfh',
                 'representativeModelId',
                 'representativeAltId',
                 'mrAtomNameMapping',
                 'cR',
                 'hasCoord',
                 'ccU',
                 'modelNumName',
                 'authAsymId',
                 'authSeqId',
                 'authAtomId',
                 'polySeq',
                 '__altPolySeq',
                 '__nonPoly',
                 '__branched',
                 '__coordAtomSite',
                 '__coordUnobsRes',
                 '__coordUnobsAtom',
                 '__labelToAuthSeq',
                 'authToLabelSeq',
                 'authToStarSeq',
                 'authToOrigSeq',
                 'authToInsCode',
                 '__entityAssembly',
                 '__lenPolySeq',
                 'monoPolymer',
                 '__multiPolymer',
                 '__lenNonPoly',
                 'exptlMethod',
                 'fibril_chain_ids',
                 'offsetHolder',
                 'hasPolySeq',
                 'hasNonPoly',
                 'hasBranched',
                 'hasNonPolySeq',
                 'nonPolySeq',
                 'fullPolySeq',
                 'atomIdSetPerChain',
                 'gapInAuthSeq',
                 '__complexSeqScheme',
                 '__polyPeptide',
                 '__polyDeoxyribonucleotide',
                 '__polyRibonucleotide',
                 'compIdSet',
                 'altCompIdSet',
                 'cyanaCompIdSet',
                 '__uniqAtomIdToSeqKey',
                 '__largeModel',
                 '__representativeAsymId',
                 'csStat',
                 'nefT',
                 '__pA',
                 '__effSeqIdSet',
                 'reasons',
                 '__preferLabelSeqCount',
                 'reasonsForReParsing',
                 '__cachedDictForAtomIdList',
                 '__cachedDictForFactor',
                 'distRestraints',
                 'dihedRestraints',
                 'rdcRestraints',
                 'planeRestraints',
                 'adistRestraints',
                 'jcoupRestraints',
                 'hvycsRestraints',
                 'procsRestraints',
                 'ramaRestraints',
                 'radiRestraints',
                 'diffRestraints',
                 'nbaseRestraints',
                 'csaRestraints',
                 'angRestraints',
                 'preRestraints',
                 'pcsRestraints',
                 'prdcRestraints',
                 'pangRestraints',
                 'pccrRestraints',
                 'hbondRestraints',
                 'geoRestraints',
                 'distStatements',
                 'dihedStatements',
                 'rdcStatements',
                 'planeStatements',
                 'adistStatements',
                 'jcoupStatements',
                 'hvycsStatements',
                 'procsStatements',
                 'ramaStatements',
                 'radiStatements',
                 'diffStatements',
                 'nbaseStatements',
                 'csaStatements',
                 'angStatements',
                 'preStatements',
                 'pcsStatements',
                 'prdcStatements',
                 'pangStatements',
                 'pccrStatements',
                 'hbondStatements',
                 'geoStatements',
                 'sfDict',
                 '__polySeqRst',
                 '__polySeqRstValid',
                 '__polySeqRstFailed',
                 '__polySeqRstFailedAmbig',
                 '__seqAtmRstFailed',
                 'f',
                 'g')

    file_type = ''
    software_name = ''

    __debug = False
    __verbose_debug = False
    __remediate = False
    __internal = False

    __nmrVsModel = None

    __createSfDict = False
    omitDistLimitOutlier = True
    allowZeroUpperLimit = False
    __correctCircularShift = True

    # @see: https://bmrb.io/ref_info/atom_nom.tbl
    # @see: https://bmrb.io/macro/files/xplor_to_iupac.Nov140620
    # whether to trust the ref_info or the macro for atom nomenclature of ASN/GLN amino group
    __trust_bmrb_ref_info = True

    in_hbdb_statement = False
    cur_dist_type = False

    # whether solid-state NMR is applied to symmetric samples such as fibrils
    symmetric = 'no'

    preferAuthSeq = True

    __extendAuthSeq = False

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    cur_subtype = ''
    cur_subtype_altered = False
    with_axis = False
    with_para = False
    in_block = False
    in_noe = False  # resolve side effect derived from rdc -> dist type change (2ljb)
    __cur_auth_atom_id = ''

    # vector statement
    cur_vector_mode = ''
    cur_vector_atom_prop_type = ''

    # evaluate statement
    cur_symbol_name = ''
    cur_vflc_op_code = ''

    # union expression
    cur_union_expr = False
    con_union_expr = False
    top_union_expr = False

    # has nitroxide
    has_nx = False

    # has Gd3+
    has_gd = False

    # has lanthanoide
    has_la = False

    depth = 0

    stackSelections = None  # stack of selection
    stackTerms = None  # stack of term
    stackFactors = None  # stack of factor
    stackVflc = None  # stack of Vflc

    factor = None
    unionFactor = None

    # distance
    noePotential = 'biharmonic'
    noeAverage = 'r-6'
    squareExponent = 2.0
    softExponent = 2.0
    squareConstant = 20.0
    squareOffset = 0.0
    rSwitch = 10.0
    scale = 1.0
    asymptote = 0.0
    B_high = 0.01
    ceiling = 30.0
    temperature = 300.0
    monomers = 1
    ncount = 2
    scale_a = None
    adistExpectGrid = None
    adistExpectValue = 0.0
    adistSizeMaxDist = 10.0
    adistSizeStep = None
    adistForceConst = 1.0
    symmTarget = None
    symmDminus = None
    symmDplus = None

    # 3D vectors in point clause
    inVector3D = False
    inVector3D_columnSel = -1
    inVector3D_tail = None
    inVector3D_head = None
    vector3D = None

    # RDC
    potential = 'square'
    average = 'sum'

    # CSA
    csaType = None
    csaSigma = None

    # PRE
    preParameterDict = None

    # CS
    csExpect = None

    # planarity
    planeWeight = 300.0

    # NCS
    ncsSigb = 2.0
    ncsWeight = 300.0

    # Rama
    ramaScale = 1.0
    ramaCutoff = None
    ramaForceConst = 1.0
    ramaShape = None
    ramaSize = None
    ramaPhase = None
    ramaGaussian = None
    ramaQuartic = None

    # CNS specific
    ramaPotential = None
    ramaError = None
    ramaExpectGrid = None
    ramaExpectValue = None

    # radius of gyration
    radiScale = 1.0

    # diffusion
    diffCoef = None
    diffForceConst = 1.0
    diffPotential = None
    diffType = None

    # orientation database
    nbaseCutoff = None
    nbaseHeight = None
    nbaseForceConst = 1.0
    nbaseGaussian = None
    nbaseMaxGauss = None
    nbaseNewGauss = None
    nbaseQuartic = None
    nbaseResidues = None
    nbaseCubicSize = None

    # paramagnetic orientation
    pangForceConst = 1.0

    # generic statements
    classification = None
    coefficients = None

    # collection of atom selection
    atomSelectionSet = []
    __lenAtomSelectionSet = 0

    # factor of paramagnetic center
    paramagCenter = None

    # description of spin labeling
    spinLabeling = None

    # collection of number selection
    numberSelection = []

    # collection of number selection in factor
    numberFSelection = []

    # store[1-9]
    storeSet = {i: [] for i in range(1, 10)}

    # vector mode: do
    vectorDo = {}

    # evaluate
    evaluate = {}

    # control
    evaluateFor = {}

    # Hydrogen bond database restraint
    donor_columnSel = -1
    acceptor_columnSel = -1

    # loop control statement
    in_loop = False

    h = None
    warningMessage = None

    # record failed chain id for segment_id assignment
    __failure_chain_ids = []

    # original source MR file name
    __originalFileName = '.'

    # list id counter
    __listIdCounter = {}

    # entry ID
    __entryId = '.'

    # current constraint type
    cur_constraint_type = None

    # default saveframe name for error handling
    __def_err_sf_framecode = None

    # last edited pynmrstar saveframe
    lastSfDict = {}

    __pro_hn_atom_not_found_pat = re.compile(r"^\[Atom not found\] \[Check the \d+th row of [^,]+s.*\] (\S+):(\d+):PRO:[Hh][Nn]? is not present in the coordinates\.$")
    __pro_hn_anomalous_data_pat = re.compile(r"^\[Anomalous data\] \[Check the \d+th row of [^,]+s.*\] (\S+):(\d+):PRO:[Hh][Nn]? is not present in the coordinates\.$")
    __gly_hb_atom_not_found_pat = re.compile(r"^\[Atom not found\] \[Check the \d+th row of [^,]+s.*\] (\S+):(\d+):GLY:[Hh][Bb]\S* is not present in the coordinates\.$")
    __any_atom_not_found_pat = re.compile(r"^\[Atom not found\] \[Check the \d+th row of [^,]+s.*\] (\S+):(\d+):\S+:(\S+) is not present in the coordinates\.$")

    # last comment (CHARMM specific)
    lastComment = None

    __dist_comment_pat = re.compile('.*:'
                                    r'([A-Za-z]+)(\d+):(\S+)-'
                                    r'([A-Za-z]+)(\d+):(\S+).*')

    __dist_comment_pat2 = re.compile('.*:'
                                     r'([A-Z]+):([A-Za-z]+)(\d+):(\S+)-'
                                     r'([A-Z]+):([A-Za-z]+)(\d+):(\S+).*')

    __dihed_comment_pat = re.compile('.*:'
                                     r'([A-Za-z]+)(\d+):(\S+)-'
                                     r'([A-Za-z]+)(\d+):(\S+)-'
                                     r'([A-Za-z]+)(\d+):(\S+)-'
                                     r'([A-Za-z]+)(\d+):(\S+).*')

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None,
                 reasons: Optional[dict] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        self.__verbose = verbose
        self.__lfh = log

        self.representativeModelId = representativeModelId
        self.representativeAltId = representativeAltId
        self.mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.cR = cR
        self.hasCoord = cR is not None

        self.nefT = nefT
        self.ccU = nefT.ccU
        self.csStat = nefT.csStat
        self.__pA = nefT.pA

        self.__polyPeptide = False
        self.__polyDeoxyribonucleotide = False
        self.__polyRibonucleotide = False

        self.exptlMethod = ''
        self.fibril_chain_ids = []

        if self.hasCoord:
            ret = coordAssemblyChecker(verbose, log, representativeModelId, representativeAltId,
                                       cR, self.ccU, caC)
            self.modelNumName = ret['model_num_name']
            self.authAsymId = ret['auth_asym_id']
            self.authSeqId = ret['auth_seq_id']
            self.authAtomId = ret['auth_atom_id']
            self.polySeq = ret['polymer_sequence']
            self.__altPolySeq = ret['alt_polymer_sequence']
            self.__nonPoly = ret['non_polymer']
            self.__branched = ret['branched']
            self.__coordAtomSite = ret['coord_atom_site']
            self.__coordUnobsRes = ret['coord_unobs_res']
            self.__coordUnobsAtom = ret['coord_unobs_atom'] if 'coord_unobs_atom' in ret else {}
            self.__labelToAuthSeq = ret['label_to_auth_seq']
            self.authToLabelSeq = ret['auth_to_label_seq']
            self.authToStarSeq = ret['auth_to_star_seq']
            self.authToOrigSeq = ret['auth_to_orig_seq']
            self.authToInsCode = ret['auth_to_ins_code']
            self.__entityAssembly = ret['entity_assembly']

            self.__lenPolySeq = len(self.polySeq) if self.polySeq is not None else 0
            self.monoPolymer = self.__lenPolySeq == 1
            self.__multiPolymer = self.__lenPolySeq > 1
            if self.__nonPoly is not None:
                self.__lenNonPoly = len(self.__nonPoly)

            exptl = cR.getDictList('exptl')
            if len(exptl) > 0:
                for item in exptl:
                    if 'method' in item:
                        if 'NMR' in item['method']:
                            self.exptlMethod = item['method']
                            break
                if self.exptlMethod == 'SOLID-STATE NMR' and self.__lenPolySeq >= 8:
                    fibril_chain_ids = []
                    for item in exptl:
                        if 'method' in item:
                            if item['method'] == 'ELECTRON MICROSCOPY':
                                for ps in self.polySeq:
                                    if 'identical_chain_id' in ps:
                                        fibril_chain_ids.append(ps['auth_chain_id'])
                                        fibril_chain_ids.extend(ps['identical_chain_id'])
                    if len(fibril_chain_ids) > 0:
                        self.fibril_chain_ids = list(set(fibril_chain_ids))

        else:
            self.modelNumName = None
            self.authAsymId = None
            self.authSeqId = None
            self.authAtomId = None
            self.polySeq = None
            self.__altPolySeq = None
            self.__nonPoly = None
            self.__branched = None
            self.__coordAtomSite = None
            self.__coordUnobsRes = None
            self.__coordUnobsAtom = None
            self.__labelToAuthSeq = None
            self.authToLabelSeq = None
            self.authToStarSeq = None
            self.authToOrigSeq = None
            self.authToInsCode = None
            self.__entityAssembly = None

            self.__lenPolySeq = 0
            self.monoPolymer = False
            self.__multiPolymer = False
            self.__lenNonPoly = 0

        self.offsetHolder = {}

        self.hasPolySeq = self.polySeq is not None and self.__lenPolySeq > 0
        self.hasNonPoly = self.__nonPoly is not None and self.__lenNonPoly > 0
        self.hasBranched = self.__branched is not None and len(self.__branched) > 0

        if self.hasNonPoly or self.hasBranched:
            self.hasNonPolySeq = True
            if self.hasNonPoly and self.hasBranched:
                self.nonPolySeq = self.__nonPoly
                self.nonPolySeq.extend(self.__branched)
            elif self.hasNonPoly:
                self.nonPolySeq = self.__nonPoly
            else:
                self.nonPolySeq = self.__branched
            self.fullPolySeq = deepcopy(self.polySeq)
            self.fullPolySeq.extend(self.nonPolySeq)

        else:
            self.hasNonPolySeq = False
            self.nonPolySeq = None
            self.fullPolySeq = self.polySeq if self.hasPolySeq else None

        self.atomIdSetPerChain = {}
        if self.hasCoord and self.__multiPolymer:  # 7d3v
            for ps in self.polySeq:
                chainId = ps['auth_chain_id']
                if chainId not in self.atomIdSetPerChain:
                    self.atomIdSetPerChain[chainId] = set()
            if self.hasNonPoly:
                for np in self.__nonPoly:
                    chainId = np['auth_chain_id']
                    if chainId not in self.atomIdSetPerChain:
                        self.atomIdSetPerChain[chainId] = set()
            if self.hasBranched:
                for br in self.__branched:
                    chainId = br['auth_chain_id']
                    if chainId not in self.atomIdSetPerChain:
                        self.atomIdSetPerChain[chainId] = set()
            for k, v in self.__coordAtomSite.items():
                self.atomIdSetPerChain[k[0]] |= set(v['atom_id'])

        if self.hasPolySeq:
            self.gapInAuthSeq = any(True for ps in self.polySeq if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq'])

            self.__complexSeqScheme = False
            if self.__multiPolymer and not all('identical_chain_id' in ps for ps in self.polySeq):
                self.__complexSeqScheme = True
                for ps in self.polySeq:
                    if ps['auth_seq_id'][0] == ps['seq_id'] or ps['auth_seq_id'][-1] == ps['seq_id'][-1]\
                       or ('gap_in_auth_seq' in ps and ps['gap_in_auth_seq']):  # 2kyg
                        self.__complexSeqScheme = False
                        break

            for entity in self.__entityAssembly:
                if 'entity_poly_type' in entity:
                    poly_type = entity['entity_poly_type']
                    if poly_type.startswith('polypeptide'):
                        self.__polyPeptide = True
                    elif poly_type == 'polydeoxyribonucleotide':
                        self.__polyDeoxyribonucleotide = True
                    elif poly_type == 'polyribonucleotide':
                        self.__polyRibonucleotide = True

            self.compIdSet = set()
            self.altCompIdSet = set()

            def is_data(array: list) -> bool:
                return not any(d in emptyValue for d in array)

            for ps in self.polySeq:
                self.compIdSet.update(set(filter(is_data, ps['comp_id'])))
                if 'auth_comp_id' in ps and ps['comp_id'] != ps['auth_comp_id']:
                    self.altCompIdSet.update(set(filter(is_data, ps['auth_comp_id'])))
                if 'alt_comp_id' in ps and ps['comp_id'] != ps['alt_comp_id']:
                    self.altCompIdSet.update(set(filter(is_data, ps['alt_comp_id'])))

            if self.hasNonPolySeq:
                for np in self.nonPolySeq:
                    self.compIdSet.update(set(filter(is_data, np['comp_id'])))
                    if 'auth_comp_id' in np and np['comp_id'] != np['auth_comp_id']:
                        self.altCompIdSet.update(set(filter(is_data, np['auth_comp_id'])))
                    if 'alt_comp_id' in np and np['comp_id'] != np['alt_comp_id']:
                        self.altCompIdSet.update(set(filter(is_data, np['alt_comp_id'])))

        else:
            self.gapInAuthSeq = False
            self.__complexSeqScheme = False
            self.compIdSet = self.altCompIdSet = set(monDict3.keys())

        self.cyanaCompIdSet = set()
        for compId in self.compIdSet:
            self.cyanaCompIdSet |= backTranslateFromStdResName(compId)

        self.__uniqAtomIdToSeqKey = {}
        if self.hasNonPoly:
            atom_list = []
            for v in self.__coordAtomSite.values():
                atom_list.extend(v['atom_id'])
            common_atom_list = collections.Counter(atom_list).most_common()
            uniq_atom_ids = [atom_id for atom_id, count in common_atom_list if count == 1]
            if len(uniq_atom_ids) > 0:
                for k, v in self.__coordAtomSite.items():
                    if any(True for np in self.__nonPoly if np['comp_id'][0] == v['comp_id']):
                        for atom_id in v['atom_id']:
                            if atom_id in uniq_atom_ids:
                                self.__uniqAtomIdToSeqKey[atom_id] = k

        self.__largeModel = self.hasPolySeq and self.__lenPolySeq > LEN_LARGE_ASYM_ID
        if self.__largeModel:
            self.__representativeAsymId = next(c for c in LARGE_ASYM_ID if any(True for ps in self.polySeq if ps['auth_chain_id'] == c))

        if reasons is not None and 'model_chain_id_ext' in reasons:
            self.polySeq, self.__altPolySeq, self.__coordAtomSite, self.__coordUnobsRes, \
                self.__labelToAuthSeq, self.authToLabelSeq, self.authToStarSeq, self.authToOrigSeq =\
                extendCoordChainsForExactNoes(reasons['model_chain_id_ext'],
                                              self.polySeq, self.__altPolySeq,
                                              self.__coordAtomSite, self.__coordUnobsRes,
                                              self.authToLabelSeq, self.authToStarSeq, self.authToOrigSeq)

        if self.__altPolySeq is not None:
            self.__effSeqIdSet = set()
            for ps in self.polySeq:
                self.__effSeqIdSet |= set(ps['auth_seq_id'])
                self.__effSeqIdSet |= set(ps['seq_id'])
            if self.hasNonPolySeq:
                for np in self.nonPolySeq:
                    self.__effSeqIdSet |= set(np['auth_seq_id'])
                    self.__effSeqIdSet |= set(np['seq_id'])

        # reasons for re-parsing request from the previous trial
        self.reasons = reasons
        self.__preferLabelSeqCount = 0

        self.reasonsForReParsing = {}  # reset to prevent interference from the previous run

        self.__cachedDictForAtomIdList = {}
        self.__cachedDictForFactor = {}

        self.distRestraints = 0      # Distance restraints
        self.dihedRestraints = 0     # Dihedral angle restraints
        self.rdcRestraints = 0       # Residual dipolar coupling restraints
        self.planeRestraints = 0     # Planarity restraints
        self.adistRestraints = 0     # Antidiatance restraints
        self.jcoupRestraints = 0     # Scalar J-coupling restraints
        self.hvycsRestraints = 0     # Carbon chemical shift restraints
        self.procsRestraints = 0     # Proton chemical shift restraints
        self.ramaRestraints = 0      # Dihedral angle database restraints
        self.radiRestraints = 0      # Radius of gyration restraints
        self.diffRestraints = 0      # Diffusion anisotropy restraints
        self.nbaseRestraints = 0     # Residue-residue position/orientation database restraints
        self.csaRestraints = 0       # (Pseudo) Chemical shift anisotropy restraints
        self.angRestraints = 0       # Angle database restraints (SCHRODINGER specific)
        self.preRestraints = 0       # Paramagnetic relaxation enhancement restraints
        self.pcsRestraints = 0       # Paramagnetic pseudocontact shift restraints
        self.prdcRestraints = 0      # Paramagnetic residual dipolar coupling restraints
        self.pangRestraints = 0      # Paramagnetic orientation restraints
        self.pccrRestraints = 0      # Paramagnetic cross-correlation rate restraints
        self.hbondRestraints = 0     # Hydrogen bond geometry/database restraints
        self.geoRestraints = 0       # Harmonic coordinate/NCS restraints
        self.distStatements = 0      # Distance statements
        self.dihedStatements = 0     # Dihedral angle statements
        self.rdcStatements = 0       # Residual dipolar coupling statements
        self.planeStatements = 0     # Planarity statements
        self.adistStatements = 0     # Antidiatance statements
        self.jcoupStatements = 0     # Scalar J-coupling statements
        self.hvycsStatements = 0     # Carbon chemical shift statements
        self.procsStatements = 0     # Proton chemical shift statements
        self.ramaStatements = 0      # Dihedral angle database statements
        self.radiStatements = 0      # Radius of gyration statements
        self.diffStatements = 0      # Diffusion anisotropy statements
        self.nbaseStatements = 0     # Residue-residue position/orientation database statements
        self.csaStatements = 0       # (Pseudo) Chemical shift anisotropy statements
        self.angStatements = 0       # Angle database statements (SCHRODINGER specific)
        self.preStatements = 0       # Paramagnetic relaxation enhancement statements
        self.pcsStatements = 0       # Paramagnetic pseudocontact shift statements
        self.prdcStatements = 0      # Paramagnetic residual dipolar coupling statements
        self.pangStatements = 0      # Paramagnetic orientation statements
        self.pccrStatements = 0      # Paramagnetic cross-correlation rate statements
        self.hbondStatements = 0     # Hydrogen bond geometry/database statements
        self.geoStatements = 0       # Harmonic coordinate/NCS restraints

        self.sfDict = {}  # dictionary of pynmrstar saveframes

        # polymer sequence of MR file
        self.__polySeqRst = []
        self.__polySeqRstValid = []
        self.__polySeqRstFailed = []
        self.__polySeqRstFailedAmbig = []
        self.__seqAtmRstFailed = []

        self.f = []
        self.g = []

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, debug: bool):
        self.__debug = debug

    @property
    def log(self):
        return self.__lfh

    @property
    def verbose_debug(self):
        return self.__verbose_debug

    @verbose_debug.setter
    def verbose_debug(self, verbose_debug: bool):
        self.__verbose_debug = verbose_debug

    @property
    def remediate(self):
        return self.__remediate

    @remediate.setter
    def remediate(self, remediate: bool):
        self.__remediate = remediate

    @property
    def internal(self):
        return self.__internal

    @internal.setter
    def internal(self, internal: bool):
        self.__internal = internal

    @property
    def nmrVsModel(self):
        return self.__nmrVsModel

    @nmrVsModel.setter
    def nmrVsModel(self, nmrVsModel: Optional[List[dict]]):
        self.__nmrVsModel = nmrVsModel

    @property
    def createSfDict(self):
        return self.__createSfDict

    @createSfDict.setter
    def createSfDict(self, createSfDict: bool):
        self.__createSfDict = createSfDict

    @property
    def originalFileName(self):
        return self.__originalFileName

    @originalFileName.setter
    def originalFileName(self, originalFileName: str):
        self.__originalFileName = originalFileName

    @property
    def listIdCounter(self):
        return self.__listIdCounter

    @listIdCounter.setter
    def listIdCounter(self, listIdCounter: dict):
        self.__listIdCounter = listIdCounter

    @property
    def entryId(self):
        return self.__entryId

    @entryId.setter
    def entryId(self, entryId: str):
        self.__entryId = entryId

    def exit(self):

        def set_label_seq_scheme():
            if 'label_seq_scheme' not in self.reasonsForReParsing:
                self.reasonsForReParsing['label_seq_scheme'] = {}
            if self.distRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['dist'] = True
            if self.dihedRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['dihed'] = True
            if self.rdcRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['rdc'] = True
            if self.planeRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['plane'] = True
            if self.adistRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['adist'] = True
            if self.jcoupRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['jcoup'] = True
            if self.hvycsRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['hvycs'] = True
            if self.procsRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['procs'] = True
            if self.ramaRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['rama'] = True
            if self.radiRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['radi'] = True
            if self.diffRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['diff'] = True
            if self.nbaseRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['nbase'] = True
            if self.csaRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['csa'] = True
            if self.angRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['ang'] = True
            if self.preRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['pre'] = True
            if self.pcsRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['pcs'] = True
            if self.prdcRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['prdc'] = True
            if self.pangRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['pang'] = True
            if self.pccrRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['pccr'] = True
            if self.hbondRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['hbond'] = True
            if self.geoRestraints > 0:
                self.reasonsForReParsing['label_seq_scheme']['geo'] = True
            if 'local_seq_scheme' in self.reasonsForReParsing:
                del self.reasonsForReParsing['local_seq_scheme']

        def chain_id_remap_with_offset(trust_cur_chain_assign=True):
            refChainIds, ovwChainIds = [], []
            chainIdRemap = {}
            if trust_cur_chain_assign:
                for ca in self.__chainAssign:
                    if ca['conflict'] > 0:
                        continue
                    ref_chain_id = ca['ref_chain_id']
                    test_chain_id = ca['test_chain_id']

                    if ref_chain_id in refChainIds:
                        continue

                    sa = next((sa for sa in self.__seqAlign
                               if sa['ref_chain_id'] == ref_chain_id
                               and sa['test_chain_id'] == test_chain_id), None)

                    if sa is None:
                        continue

                    if any(seq_id in chainIdRemap for seq_id in sa['test_seq_id']):
                        continue

                    ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == ref_chain_id)
                    has_gap_in_auth_seq = 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']

                    label_seq_scheme = False
                    _ps = next((_ps for _ps in self.__polySeqRstValid if _ps['chain_id'] == ref_chain_id), None)
                    if _ps is not None and all(seq_id in ps['seq_id'] for seq_id in _ps['seq_id']):
                        label_seq_scheme = True  # 2m3o

                    rev_seq_id_mapping = {}
                    if 'ref_auth_seq_id' in sa and sa['ref_auth_seq_id'] == sa['test_seq_id'] and not label_seq_scheme:
                        pass  # 6f0y
                    else:
                        for ref_seq_id, test_seq_id in zip(sa['ref_seq_id'], sa['test_seq_id']):
                            if test_seq_id is not None:
                                rev_seq_id_mapping[test_seq_id] = ref_seq_id

                    if has_gap_in_auth_seq:
                        for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                            if auth_seq_id in emptyValue:
                                continue
                            if auth_seq_id in rev_seq_id_mapping:
                                test_seq_id = rev_seq_id_mapping[auth_seq_id]
                                chainIdRemap[test_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                            elif seq_id not in chainIdRemap:
                                chainIdRemap[seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                    else:
                        for auth_seq_id in ps['auth_seq_id']:
                            if auth_seq_id in emptyValue:
                                continue
                            if auth_seq_id in rev_seq_id_mapping:
                                test_seq_id = rev_seq_id_mapping[auth_seq_id]
                                chainIdRemap[test_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                            elif auth_seq_id not in chainIdRemap:
                                chainIdRemap[auth_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}

                    refChainIds.append(ref_chain_id)

            score = {1: 8, 2: 6, 3: 4, 4: 2, 5: 1, 6: 1, 7: 1}

            for ps in self.polySeq:
                chainId = ps['auth_chain_id']
                if chainId in refChainIds:
                    continue
                has_gap_in_auth_seq = 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']
                seq_id_name = 'seq_id' if has_gap_in_auth_seq else 'auth_seq_id'

                chainIds = [chainId]
                if 'identical_chain_id' in ps:
                    chainIds.extend(ps['identical_chain_id'])

                offsets = []
                if trust_cur_chain_assign:
                    for item in self.__polySeqRstFailed:
                        if item['chain_id'] in chainIds:
                            for seqId, compId in zip(item['seq_id'], item['comp_id']):
                                offsets.extend([_seqId - seqId for _seqId, _compId in zip(ps[seq_id_name], ps['comp_id']) if _compId == compId])
                    for item in self.__polySeqRstFailedAmbig:
                        if item['chain_id'] in chainIds:
                            for seqId, compIds in zip(item['seq_id'], item['comp_ids']):
                                offsets.extend([_seqId - seqId for _seqId, _compId in zip(ps[seq_id_name], ps['comp_id']) if _compId in compIds])

                if len(offsets) == 0:
                    # predict sequence offset purely from __seqAtmRstFailed (2l12)
                    for item in self.__seqAtmRstFailed:
                        if item['chain_id'] not in chainIds:
                            continue
                        for seqId, atomIds in zip(item['seq_id'], item['atom_id']):
                            if seqId in chainIdRemap:
                                continue
                            compIds = guessCompIdFromAtomIdWoLimit(atomIds, [ps], self.nefT)
                            lenCompIds = len(compIds)
                            if lenCompIds < 5:
                                for _seqId, _compId in zip(ps[seq_id_name], ps['comp_id']):
                                    if _compId in compIds:
                                        offsets.extend([_seqId - seqId] * score[lenCompIds])
                            else:
                                for _seqId, _compId in zip(ps[seq_id_name], ps['comp_id']):
                                    if _compId in compIds:
                                        offsets.append(_seqId - seqId)

                    if len(offsets) == 0:
                        continue

                common_offsets = collections.Counter(offsets).most_common()
                offsets = [offset for offset, count in common_offsets if count == common_offsets[0][1]]

                item = next((item for item in self.__seqAtmRstFailed if item['chain_id'] in chainIds), None)
                if item is None:
                    continue

                _matched = 0
                _offsets = []
                for offset in offsets:
                    valid = True
                    matched = 0
                    for item in self.__seqAtmRstFailed:
                        if item['chain_id'] not in chainIds:
                            continue
                        for _seqId, _atomIds in zip(item['seq_id'], item['atom_id']):
                            if _seqId in chainIdRemap:
                                continue
                            _compIds = guessCompIdFromAtomIdWoLimit(_atomIds, [ps], self.nefT)
                            if _seqId + offset in ps[seq_id_name]:
                                compId = ps['comp_id'][ps[seq_id_name].index(_seqId + offset)]
                                if compId in _compIds:
                                    matched += 1
                                elif compId not in monDict3 or len(_compIds) == 0:  # 6f0y
                                    continue
                                else:
                                    valid = False
                                    break
                            else:
                                matched -= 1
                    if valid:
                        if matched > _matched:
                            _matched = matched
                            _offsets = [offset]
                        elif matched == _matched:
                            _offsets.append(offset)

                if len(_offsets) == 1:
                    _offset = _offsets[0]

                elif len(_offsets) == 0 or len(offsets) > 4:  # 2ymj, 2js1
                    continue

                else:  # 2n3a
                    _matched = -10000
                    _offset = None
                    for offset in _offsets:
                        matched = 0
                        for item in self.__seqAtmRstFailed:
                            if item['chain_id'] not in chainIds:
                                continue
                            for _seqId, _atomIds in zip(item['seq_id'], item['atom_id']):
                                _compIds = guessCompIdFromAtomIdWoLimit(_atomIds, [ps], self.nefT)
                                if _seqId + offset in ps[seq_id_name]:
                                    idx = ps[seq_id_name].index(_seqId + offset)
                                    compId = ps['comp_id'][idx]
                                    if compId in _compIds:
                                        matched += 100
                                        if all(abs(offset_) > 950 for offset_ in _offsets):  # 6e5n
                                            matched -= abs((offset % 100) - 100) % 100
                                        elif ps['auth_seq_id'][idx] not in emptyValue:
                                            matched -= abs(offset - (ps['auth_seq_id'][idx] - ps['seq_id'][idx]))
                                else:
                                    matched -= 100
                            if matched > _matched:
                                _matched, _offset = matched, offset
                    if _offset is None:
                        _offset = _offsets[0]

                if len(_offsets) == 0:
                    continue

                if has_gap_in_auth_seq:

                    if len(refChainIds) == 0:  # 2kny
                        continue

                    for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                        if auth_seq_id in emptyValue:
                            continue
                        if seq_id - _offset in chainIdRemap:
                            _chainId = chainIdRemap[seq_id - _offset]['chain_id']
                            if _chainId not in ovwChainIds:
                                ovwChainIds.append(_chainId)
                        chainIdRemap[seq_id - _offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                else:
                    for auth_seq_id in ps['auth_seq_id']:
                        if auth_seq_id in emptyValue:
                            continue
                        if auth_seq_id - _offset in chainIdRemap:
                            _chainId = chainIdRemap[auth_seq_id - _offset]['chain_id']
                            if _chainId not in ovwChainIds:
                                ovwChainIds.append(_chainId)
                        chainIdRemap[auth_seq_id - _offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}

                if 'label_seq_offset' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['label_seq_offset']
                if 'local_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing:
                    if chainId in self.reasonsForReParsing['inhibit_label_seq_scheme']:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId]
                    if len(self.reasonsForReParsing['inhibit_label_seq_scheme']) == 0:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme']

            # try to handle chain_id remapping conflicts (2knh)
            for chainId in ovwChainIds:
                ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)
                has_gap_in_auth_seq = 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']
                seq_id_name = 'seq_id' if has_gap_in_auth_seq else 'auth_seq_id'

                offsets = []
                for item in self.__polySeqRstFailedAmbig:
                    if item['chain_id'] == chainId:
                        for seqId, compIds in zip(item['seq_id'], item['comp_ids']):
                            if seqId in chainIdRemap:
                                continue
                            offsets.extend([_seqId - seqId for _seqId, _compId in zip(ps[seq_id_name], ps['comp_id']) if _compId in compIds])

                if len(offsets) == 0:
                    continue

                common_offsets = collections.Counter(offsets).most_common()
                offsets = [offset for offset, count in common_offsets if count == common_offsets[0][1]]

                item = next((item for item in self.__seqAtmRstFailed if item['chain_id'] == chainId), None)
                if item is None:
                    continue

                _matched = 0
                _offset = None

                for item in self.__seqAtmRstFailed:
                    if item['chain_id'] != chainId:
                        continue
                    for offset in offsets:
                        valid = True
                        matched = 0
                        for _seqId, _atomIds in zip(item['seq_id'], item['atom_id']):
                            if _seqId in chainIdRemap:
                                continue
                            _compIds = guessCompIdFromAtomIdWoLimit(_atomIds, [ps], self.nefT)
                            if _seqId + offset in ps[seq_id_name]:
                                if ps['comp_id'][ps[seq_id_name].index(_seqId + offset)] in _compIds:
                                    matched += 1
                                else:
                                    valid = False
                                    break
                        if valid:
                            if matched > _matched:
                                _matched, _offset = matched, offset

                if _offset is None:
                    continue

                if has_gap_in_auth_seq:
                    for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                        if auth_seq_id in emptyValue:
                            continue
                        chainIdRemap[seq_id - _offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                else:
                    for auth_seq_id in ps['auth_seq_id']:
                        if auth_seq_id in emptyValue:
                            continue
                        chainIdRemap[auth_seq_id - _offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}

                self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing:
                    if chainId in self.reasonsForReParsing['inhibit_label_seq_scheme']:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId]
                    if len(self.reasonsForReParsing['inhibit_label_seq_scheme']) == 0:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme']

        def chain_id_split_with_offset(failed_seq_ids):
            refChainIds = []
            chainIdRemap = {}
            for ca in self.__chainAssign:
                if ca['conflict'] > 0:
                    continue
                ref_chain_id = ca['ref_chain_id']
                test_chain_id = ca['test_chain_id']

                if ref_chain_id in refChainIds:
                    continue

                sa = next((sa for sa in self.__seqAlign
                           if sa['ref_chain_id'] == ref_chain_id
                           and sa['test_chain_id'] == test_chain_id), None)

                if sa is None:
                    continue

                if any(seq_id in chainIdRemap for seq_id in sa['test_seq_id']):
                    continue

                ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == ref_chain_id)
                has_gap_in_auth_seq = 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']

                label_seq_scheme = False
                _ps = next((_ps for _ps in self.__polySeqRstValid if _ps['chain_id'] == ref_chain_id), None)
                if _ps is not None and all(seq_id in ps['seq_id'] for seq_id in _ps['seq_id']):
                    label_seq_scheme = True  # 2m3o

                rev_seq_id_mapping = {}
                if 'ref_auth_seq_id' in sa and sa['ref_auth_seq_id'] == sa['test_seq_id'] and not label_seq_scheme:
                    pass  # 6f0y
                else:
                    for ref_seq_id, test_seq_id in zip(sa['ref_seq_id'], sa['test_seq_id']):
                        if test_seq_id is not None:
                            rev_seq_id_mapping[test_seq_id] = ref_seq_id

                if has_gap_in_auth_seq:
                    for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                        if auth_seq_id in emptyValue:
                            continue
                        if auth_seq_id in rev_seq_id_mapping:
                            test_seq_id = rev_seq_id_mapping[auth_seq_id]
                            chainIdRemap[test_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                        elif seq_id not in chainIdRemap:
                            chainIdRemap[seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                else:
                    for auth_seq_id in ps['auth_seq_id']:
                        if auth_seq_id in emptyValue:
                            continue
                        if auth_seq_id in rev_seq_id_mapping:
                            test_seq_id = rev_seq_id_mapping[auth_seq_id]
                            chainIdRemap[test_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}
                        elif auth_seq_id not in chainIdRemap:
                            chainIdRemap[auth_seq_id] = {'chain_id': ref_chain_id, 'seq_id': auth_seq_id}

                refChainIds.append(ref_chain_id)

            for ps in self.polySeq:
                chainId = ps['auth_chain_id']
                if chainId in refChainIds:
                    continue

                has_gap_in_auth_seq = 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']
                seq_id_name = 'seq_id' if has_gap_in_auth_seq else 'auth_seq_id'

                len_seq_id = len(ps['seq_id'])

                src_seq_ids = failed_seq_ids[:len_seq_id]
                failed_seq_ids = failed_seq_ids[len_seq_id:]

                offset = ps[seq_id_name][0] - src_seq_ids[0]

                if has_gap_in_auth_seq:
                    for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                        if auth_seq_id in emptyValue:
                            continue
                        chainIdRemap[seq_id - offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                else:
                    for auth_seq_id in ps['auth_seq_id']:
                        if auth_seq_id in emptyValue:
                            continue
                        chainIdRemap[auth_seq_id - offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}

                self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing:
                    if chainId in self.reasonsForReParsing['inhibit_label_seq_scheme']:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId]
                    if len(self.reasonsForReParsing['inhibit_label_seq_scheme']) == 0:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme']

            self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

        try:

            pro_hn_atom_not_found_warnings = [f for f in self.f if self.__pro_hn_atom_not_found_pat.match(f) or self.__pro_hn_anomalous_data_pat.match(f)]
            gly_hb_atom_not_found_warnings = [f for f in self.f if self.__gly_hb_atom_not_found_pat.match(f)]
            any_atom_not_found_warnings = (f for f in self.f if self.__any_atom_not_found_pat.match(f))

            if 'segment_id_mismatch' in self.reasonsForReParsing\
               and (len(self.reasonsForReParsing['segment_id_mismatch']) == 0
                    or (len(self.reasonsForReParsing['segment_id_mismatch']) < len(self.atomIdSetPerChain)
                        and all(all(score < 0 for score in stat.values()) and len(set(stat.values())) == 1
                                for stat in self.reasonsForReParsing['segment_id_match_stats'].values()))):  # 2lzs
                del self.reasonsForReParsing['segment_id_mismatch']
                del self.reasonsForReParsing['segment_id_match_stats']
                del self.reasonsForReParsing['segment_id_poly_type_stats']

            _seqIdRemap = []

            if self.hasPolySeq and self.__polySeqRst is not None:
                sortPolySeqRst(self.__polySeqRst,
                               None if self.reasons is None else self.reasons.get('non_poly_remap'))

                self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRst,
                                                          resolvedMultimer=self.reasons is not None)
                self.__chainAssign, message = assignPolymerSequence(self.__pA, self.ccU, self.file_type, self.polySeq, self.__polySeqRst, self.__seqAlign)

                if len(message) > 0:
                    self.f.extend(message)

                if self.__chainAssign is not None:

                    if self.__lenPolySeq == len(self.__polySeqRst):

                        chain_id_mapping = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            if ref_chain_id != test_chain_id:
                                chain_id_mapping[test_chain_id] = ref_chain_id

                        if len(chain_id_mapping) == self.__lenPolySeq:

                            if not any('identical_chain_id' in ps for ps in self.polySeq if ps['auth_chain_id'] in chain_id_mapping):
                                for ps in self.__polySeqRst:
                                    if ps['chain_id'] in chain_id_mapping:
                                        ps['chain_id'] = chain_id_mapping[ps['chain_id']]

                                self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRst,
                                                                          resolvedMultimer=self.reasons is not None)
                                self.__chainAssign, _ = assignPolymerSequence(self.__pA, self.ccU, self.file_type, self.polySeq, self.__polySeqRst, self.__seqAlign)

                            elif len(self.__chainAssign) > len(self.__polySeqRst) and len(self.__polySeqRstFailed) > 0:
                                mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                                sortPolySeqRst(self.__polySeqRstFailed)

                                overlap = False
                                for _ps in self.__polySeqRstFailed:
                                    ps = next((ps for ps in self.__polySeqRst if ps['chain_id'] == _ps['chain_id']), None)
                                    if ps is not None and any(_seq_id in ps['seq_id'] for _seq_id in _ps['seq_id']):
                                        overlap = True
                                        break

                                if not overlap:  # 2lfr
                                    seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)

                                    if all(sa['matched'] > 0 and sa['conflict'] == 0 for sa in seqAlignFailed):
                                        chain_id_remap_with_offset()  # 2l01

                    elif self.__lenPolySeq > len(self.__polySeqRst) > 0 and all('identical_chain_id' in ps for ps in self.polySeq):

                        chain_id_mapping = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            if ref_chain_id != test_chain_id:
                                chain_id_mapping[test_chain_id] = ref_chain_id

                        if len(chain_id_mapping) == len(self.__polySeqRst) and len(self.__chainAssign) > len(self.__polySeqRst):
                            if len(self.__polySeqRstFailed) > 0:
                                mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                                sortPolySeqRst(self.__polySeqRstFailed)

                                overlap = False
                                for _ps in self.__polySeqRstFailed:
                                    ps = next((ps for ps in self.__polySeqRst if ps['chain_id'] == _ps['chain_id']), None)
                                    if ps is not None and any(_seq_id in ps['seq_id'] for _seq_id in _ps['seq_id']):
                                        overlap = True
                                        break

                                if not overlap:  # 2lfr
                                    seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)

                                    if all(sa['matched'] > 0 and sa['conflict'] == 0 for sa in seqAlignFailed):
                                        chain_id_remap_with_offset()

                            elif len(self.__seqAtmRstFailed) > 0:
                                chain_id_remap_with_offset()  # 2n9b

                    trimSequenceAlignment(self.__seqAlign, self.__chainAssign)

                    if self.reasons is None\
                       and any(True for f in self.f if '[Anomalous data]' in f)\
                       and 'segment_id_mismatch' not in self.reasonsForReParsing\
                       and (self.distRestraints > 0 or self.monoPolymer or all('identical_chain_id' in ps for ps in self.polySeq)):
                        set_label_seq_scheme()

                    if self.reasons is None\
                       and (any(True for f in self.f if '[Atom not found]' in f or '[Anomalous data]' in f or '[Sequence mismatch]' in f)
                            or any(True for f in self.f if '[Insufficient atom selection]' in f)):

                        seqIdRemap = []

                        cyclicPolymer = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            sa = next(sa for sa in self.__seqAlign
                                      if sa['ref_chain_id'] == ref_chain_id
                                      and sa['test_chain_id'] == test_chain_id)

                            poly_seq_model = next(ps for ps in self.polySeq
                                                  if ps['auth_chain_id'] == ref_chain_id)
                            poly_seq_rst = next(ps for ps in self.__polySeqRst
                                                if ps['chain_id'] == test_chain_id)

                            seq_id_mapping = {}
                            for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                if mid_code == '|' and test_seq_id is not None:
                                    try:
                                        seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                           in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                           if seq_id == ref_seq_id and isinstance(auth_seq_id, int))
                                    except StopIteration:
                                        pass

                            if ref_chain_id not in cyclicPolymer:
                                cyclicPolymer[ref_chain_id] =\
                                    isCyclicPolymer(self.cR, self.polySeq, ref_chain_id,
                                                    self.representativeModelId, self.representativeAltId, self.modelNumName)

                            if cyclicPolymer[ref_chain_id]:

                                poly_seq_model = next(ps for ps in self.polySeq
                                                      if ps['auth_chain_id'] == ref_chain_id)

                                offset = None
                                for seq_id, comp_id in zip(poly_seq_rst['seq_id'], poly_seq_rst['comp_id']):
                                    if seq_id is not None and seq_id not in seq_id_mapping:
                                        _seq_id = next((_seq_id for _seq_id, _comp_id in zip(poly_seq_model['seq_id'], poly_seq_model['comp_id'])
                                                        if _seq_id not in seq_id_mapping.values() and _comp_id == comp_id), None)
                                        if _seq_id is not None:
                                            offset = seq_id - _seq_id
                                            break

                                if offset is not None:
                                    for seq_id in poly_seq_rst['seq_id']:
                                        if seq_id is not None and seq_id not in seq_id_mapping:
                                            seq_id_mapping[seq_id] = seq_id - offset

                            if any(True for k, v in seq_id_mapping.items() if k != v)\
                               and not any(True for k, v in seq_id_mapping.items()
                                           if v in poly_seq_model['seq_id']
                                           and k == poly_seq_model['auth_seq_id'][poly_seq_model['seq_id'].index(v)]):
                                seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': seq_id_mapping})
                            else:
                                _seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': seq_id_mapping})

                        if len(seqIdRemap) > 0:
                            if 'seq_id_remap' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['seq_id_remap'] = seqIdRemap

                        if any(True for ps in self.polySeq if 'identical_chain_id' in ps):
                            polySeqRst, chainIdMapping = splitPolySeqRstForMultimers(self.__pA, self.polySeq, self.__polySeqRst, self.__chainAssign)

                            if polySeqRst is not None and (not self.hasNonPoly or self.__lenPolySeq // self.__lenNonPoly in (1, 2)):
                                self.__polySeqRst = polySeqRst
                                if 'chain_id_remap' not in self.reasonsForReParsing and len(chainIdMapping) > 0:
                                    self.reasonsForReParsing['chain_id_remap'] = chainIdMapping

                        if self.monoPolymer and len(self.__polySeqRst) == 1:
                            polySeqRst, chainIdMapping, modelChainIdExt =\
                                splitPolySeqRstForExactNoes(self.__pA, self.polySeq, self.__polySeqRst, self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'chain_id_clone' not in self.reasonsForReParsing and len(chainIdMapping) > 0:
                                    self.reasonsForReParsing['chain_id_clone'] = chainIdMapping
                                if 'model_chain_id_ext' not in self.reasonsForReParsing and len(modelChainIdExt) > 0:
                                    self.reasonsForReParsing['model_chain_id_ext'] = modelChainIdExt

                        if self.hasNonPoly:
                            polySeqRst, nonPolyMapping = splitPolySeqRstForNonPoly(self.ccU, self.__nonPoly, self.__polySeqRst,
                                                                                   self.__seqAlign, self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'non_poly_remap' not in self.reasonsForReParsing and len(nonPolyMapping) > 0:
                                    self.reasonsForReParsing['non_poly_remap'] = nonPolyMapping

                        if self.hasBranched:
                            polySeqRst, branchedMapping = splitPolySeqRstForBranched(self.__pA, self.polySeq, self.__branched, self.__polySeqRst,
                                                                                     self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'branched_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['branched_remap'] = branchedMapping

                        mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                        if len(self.__polySeqRstFailed) > 0:
                            sortPolySeqRst(self.__polySeqRstFailed)

                            seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)

                            # extend restraint polymer sequence from single match (2joa)
                            if len(seqAlignFailed) == 0 and len(self.__polySeqRstFailed) > 0 and len(self.__polySeqRstFailedAmbig) > 0:
                                for ps in self.__polySeqRstFailed:
                                    chainId = ps['chain_id']
                                    _ps = next((_ps for _ps in self.__polySeqRstFailedAmbig if _ps['chain_id'] == chainId), None)
                                    if _ps is None:
                                        continue
                                    _matched = 0
                                    for seqId, compIds in zip(_ps['seq_id'], _ps['comp_ids']):
                                        _compId = None
                                        for compId in list(compIds):
                                            _polySeqRstFailed = deepcopy(self.__polySeqRstFailed)
                                            updatePolySeqRst(_polySeqRstFailed, chainId, seqId, compId)
                                            sortPolySeqRst(_polySeqRstFailed)
                                            _seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, _polySeqRstFailed)
                                            _sa = next((_sa for _sa in _seqAlignFailed if _sa['test_chain_id'] == chainId), None)
                                            if _sa is None or _sa['conflict'] > 0:
                                                continue
                                            if _sa['matched'] > _matched:
                                                _matched = _sa['matched']
                                                _compId = compId
                                        if _compId is not None:
                                            updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, _compId)
                                            sortPolySeqRst(self.__polySeqRstFailed)

                            for sa in seqAlignFailed:
                                if sa['conflict'] == 0:
                                    chainId = sa['test_chain_id']
                                    _ps = next((_ps for _ps in self.__polySeqRstFailedAmbig if _ps['chain_id'] == chainId), None)
                                    if _ps is None:
                                        continue
                                    _matched = sa['matched']
                                    for seqId, compIds in zip(_ps['seq_id'], _ps['comp_ids']):
                                        _compId = None
                                        for compId in list(compIds):
                                            _polySeqRstFailed = deepcopy(self.__polySeqRstFailed)
                                            updatePolySeqRst(_polySeqRstFailed, chainId, seqId, compId)
                                            sortPolySeqRst(_polySeqRstFailed)
                                            _seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, _polySeqRstFailed)
                                            _sa = next((_sa for _sa in _seqAlignFailed if _sa['test_chain_id'] == chainId), None)
                                            if _sa is None or _sa['conflict'] > 0:
                                                continue
                                            if _sa['matched'] > _matched:
                                                _matched = _sa['matched']
                                                _compId = compId
                                        if _compId is not None:
                                            updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, _compId)
                                            sortPolySeqRst(self.__polySeqRstFailed)

                            seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)
                            chainAssignFailed, _ = assignPolymerSequence(self.__pA, self.ccU, self.file_type,
                                                                         self.polySeq, self.__polySeqRstFailed, seqAlignFailed)

                            if chainAssignFailed is not None:

                                seqAlignValid = None
                                if len(self.__polySeqRstValid) > 0:
                                    sortPolySeqRst(self.__polySeqRstValid)
                                    seqAlignValid, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstValid)

                                if seqAlignValid is not None and len(seqAlignValid) == 0 and len(seqAlignFailed) == 0:
                                    if 'local_seq_scheme' in self.reasonsForReParsing:
                                        del self.reasonsForReParsing['local_seq_scheme']
                                    if 'label_seq_scheme' in self.reasonsForReParsing:
                                        del self.reasonsForReParsing['label_seq_scheme']
                                    if len(pro_hn_atom_not_found_warnings) + len(gly_hb_atom_not_found_warnings) > 0:
                                        self.__seqAtmRstFailed = []
                                        for f in any_atom_not_found_warnings:
                                            g = self.__any_atom_not_found_pat.search(f).groups()
                                            updateSeqAtmRst(self.__seqAtmRstFailed, g[0], int(g[1]), [g[2]])
                                        chain_id_remap_with_offset(False)  # 5xs1

                                for ca in chainAssignFailed:
                                    if ca['conflict'] > 0:
                                        continue
                                    ref_chain_id = ca['ref_chain_id']
                                    test_chain_id = ca['test_chain_id']

                                    sa = next((sa for sa in seqAlignFailed
                                               if sa['ref_chain_id'] == ref_chain_id
                                               and sa['test_chain_id'] == test_chain_id), None)

                                    if sa is None:
                                        continue

                                    poly_seq_model = next(ps for ps in self.polySeq
                                                          if ps['auth_chain_id'] == ref_chain_id)

                                    seq_id_mapping = {}
                                    for ref_auth_seq_id, mid_code, test_seq_id in zip(sa['ref_auth_seq_id'] if 'ref_auth_seq_id' in sa else sa['ref_seq_id'],
                                                                                      sa['mid_code'], sa['test_seq_id']):
                                        if mid_code == '|' and test_seq_id is not None:
                                            seq_id_mapping[test_seq_id] = ref_auth_seq_id

                                    ref_seq_id_mapping = {}
                                    if seqAlignValid is not None:
                                        sa_ref = next((sa for sa in seqAlignValid
                                                       if sa['ref_chain_id'] == ref_chain_id
                                                       and sa['test_chain_id'] == test_chain_id), None)

                                        if sa_ref is not None:
                                            for ref_auth_seq_id, mid_code, test_seq_id in zip(sa_ref['ref_auth_seq_id'] if 'ref_auth_seq_id' in sa_ref else sa_ref['ref_seq_id'],
                                                                                              sa_ref['mid_code'], sa_ref['test_seq_id']):
                                                if mid_code == '|' and test_seq_id is not None:
                                                    ref_seq_id_mapping[test_seq_id] = ref_auth_seq_id

                                    if len(seq_id_mapping) > 1:
                                        for k, v in seq_id_mapping.items():
                                            offset = v - k
                                            break

                                        if len(ref_seq_id_mapping) > 1:
                                            for k, v in ref_seq_id_mapping.items():
                                                ref_offset = v - k
                                                break

                                            if offset != ref_offset:
                                                continue

                                        if any(True for k, v in seq_id_mapping.items() if k != v):
                                            if not any(v - k != offset for k, v in seq_id_mapping.items()):
                                                if 'global_auth_sequence_offset' not in self.reasonsForReParsing:
                                                    self.reasonsForReParsing['global_auth_sequence_offset'] = {}
                                                self.reasonsForReParsing['global_auth_sequence_offset'][ref_chain_id] = offset
                                            else:
                                                offsets = [v - k for k, v in seq_id_mapping.items()]
                                                common_offsets = collections.Counter(offsets).most_common()
                                                if common_offsets[0][1] > 1 and common_offsets[0][1] > common_offsets[1][1]\
                                                   and abs(common_offsets[0][0] - common_offsets[1][0]) == 1:
                                                    offset = common_offsets[0][0]
                                                    if 'global_auth_sequence_offset' not in self.reasonsForReParsing:
                                                        self.reasonsForReParsing['global_auth_sequence_offset'] = {}
                                                    self.reasonsForReParsing['global_auth_sequence_offset'][ref_chain_id] = offset
                                                else:
                                                    seq_id_mapping = {}
                                                    for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                                        if mid_code == '|' and test_seq_id is not None:
                                                            seq_id_mapping[test_seq_id] = ref_seq_id

                                                    for k, v in seq_id_mapping.items():
                                                        offset = v - k
                                                        break

                                                    if offset != 0 and not any(v - k != offset for k, v in seq_id_mapping.items()):
                                                        offsets = {}
                                                        for ref_auth_seq_id, auth_seq_id in zip(sa['ref_auth_seq_id'], sa['ref_seq_id']):
                                                            offsets[auth_seq_id - offset] = ref_auth_seq_id - auth_seq_id
                                                        if 'global_auth_sequence_offset' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['global_auth_sequence_offset'] = {}
                                                        self.reasonsForReParsing['global_auth_sequence_offset'][ref_chain_id] = offsets

                                if len(chainAssignFailed) == 0\
                                   or (self.monoPolymer and 'label_seq_scheme' not in self.reasonsForReParsing
                                       and 'gap_in_auth_seq' in self.polySeq[0] and self.polySeq[0]['gap_in_auth_seq']):  # 6mv3
                                    valid_auth_seq = valid_label_seq = True
                                    for _ps in self.__polySeqRstFailed:
                                        test_chain_id = _ps['chain_id']
                                        try:
                                            ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == test_chain_id)
                                            for test_seq_id, test_comp_id in zip(_ps['seq_id'], _ps['comp_id']):
                                                if test_seq_id not in ps['seq_id']:
                                                    valid_label_seq = False
                                                elif test_comp_id not in emptyValue and test_comp_id != ps['comp_id'][ps['seq_id'].index(test_seq_id)]:
                                                    valid_label_seq = False
                                                if test_seq_id not in ps['auth_seq_id']:
                                                    valid_auth_seq = False
                                                elif test_comp_id != ps['comp_id'][ps['auth_seq_id'].index(test_seq_id)]:
                                                    valid_auth_seq = False
                                                if not valid_auth_seq and not valid_label_seq:
                                                    break
                                        except StopIteration:
                                            valid_auth_seq = valid_label_seq = False
                                            break
                                    if not valid_auth_seq and valid_label_seq:
                                        set_label_seq_scheme()
                                    else:
                                        chain_id_remap_with_offset()

                                elif len(self.__chainAssign) > 0 and len(self.__polySeqRstFailed) == 1 and len(self.__seqAtmRstFailed) > 0\
                                        and all('identical_chain_id' in ps for ps in self.polySeq)\
                                        and 'global_auth_sequence_offset' in self.reasonsForReParsing\
                                        and len(set(self.reasonsForReParsing['global_auth_sequence_offset'].values())) == 1:
                                    if len(self.__polySeqRstFailed[0]['seq_id']) == len(self.polySeq[0]['seq_id']) * (self.__lenPolySeq - 1):
                                        chain_id_split_with_offset(self.__polySeqRstFailed[0]['seq_id'])  # 6ge1

                        elif len(self.__seqAtmRstFailed) > 0\
                                and 'label_seq_scheme' not in self.reasonsForReParsing\
                                and 'label_seq_offset' in self.reasonsForReParsing:
                            chainIdRemap = {}
                            valid = True
                            for item in self.__seqAtmRstFailed:
                                chainId = item['chain_id']
                                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                                if ps is None:
                                    continue
                                if chainId in self.reasonsForReParsing['label_seq_offset']:
                                    for auth_seq_id in ps['auth_seq_id']:
                                        if auth_seq_id in chainIdRemap:
                                            valid = False
                                            break
                                        chainIdRemap[auth_seq_id] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                                    if len(pro_hn_atom_not_found_warnings) + len(gly_hb_atom_not_found_warnings) == 0:
                                        continue
                                if all(seqId in ps['seq_id'] and seqId not in ps['auth_seq_id'] for seqId in item['seq_id']):
                                    for seqId, atoms in zip(item['seq_id'], item['atom_id']):
                                        compId = ps['comp_id'][ps['seq_id'].index(seqId)]
                                        for atom in atoms:
                                            _, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atom, leave_unmatched=True)
                                            if details is not None:
                                                valid = False
                                                break
                                    if valid:
                                        for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                                            if seq_id in chainIdRemap:
                                                valid = False
                                                break
                                            chainIdRemap[seq_id] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                            if valid:
                                del self.reasonsForReParsing['label_seq_offset']
                                if 'local_seq_scheme' in self.reasonsForReParsing:
                                    del self.reasonsForReParsing['local_seq_scheme']
                                self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

                        # try to find valid sequence offset from failed ambiguous assignments (2js1)
                        elif len(self.__chainAssign) > 0 and len(self.__seqAtmRstFailed) > 0\
                                and self.__multiPolymer:  # 2n3a, 6e5n
                            # and 'local_seq_scheme' in self.reasonsForReParsing:  # and 'label_seq_scheme' in self.reasonsForReParsing: (2lxs)
                            chain_id_remap_with_offset()

                    # DAOTHER-9063
                    if self.reasons is None and 'np_seq_id_remap' in self.reasonsForReParsing:

                        seqIdRemap = []

                        for test_chain_id, np_seq_id_mapping in self.reasonsForReParsing['np_seq_id_remap'].items():
                            _np_seq_id_mapping = {k: v for k, v in np_seq_id_mapping.items() if v is not None}
                            if len(_np_seq_id_mapping) == 0:
                                continue
                            _np_seq_id_mapping_ = {v: k for k, v in np_seq_id_mapping.items() if v is not None}
                            if len(_np_seq_id_mapping) != len(_np_seq_id_mapping_):
                                continue
                            seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': _np_seq_id_mapping})

                        if len(seqIdRemap) == 0:
                            del self.reasonsForReParsing['np_seq_id_remap']
                        else:
                            self.reasonsForReParsing['np_seq_id_remap'] = seqIdRemap

                    # attempt to resolve case where there is no valid restraint, but only insufficient atom selection errors
                    # due to arbitrary shift of sequence number that does not match with any coordinate sequence schemes (2lzs)
                    mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                    if self.reasons is None and len(self.__polySeqRst) == 0 and len(self.__polySeqRstFailed) > 0\
                       and any(True for f in self.f if '[Insufficient atom selection]' in f):
                        sortPolySeqRst(self.__polySeqRstFailed)

                        seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)

                        # extend restraint polymer sequence from single match (2joa)
                        if len(seqAlignFailed) == 0 and len(self.__polySeqRstFailed) > 0 and len(self.__polySeqRstFailedAmbig) > 0:
                            for ps in self.__polySeqRstFailed:
                                chainId = ps['chain_id']
                                _ps = next((_ps for _ps in self.__polySeqRstFailedAmbig if _ps['chain_id'] == chainId), None)
                                if _ps is None:
                                    continue
                                _matched = 0
                                for seqId, compIds in zip(_ps['seq_id'], _ps['comp_ids']):
                                    _compId = None
                                    for compId in list(compIds):
                                        _polySeqRstFailed = deepcopy(self.__polySeqRstFailed)
                                        updatePolySeqRst(_polySeqRstFailed, chainId, seqId, compId)
                                        sortPolySeqRst(_polySeqRstFailed)
                                        _seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, _polySeqRstFailed)
                                        _sa = next((_sa for _sa in _seqAlignFailed if _sa['test_chain_id'] == chainId), None)
                                        if _sa is None or _sa['conflict'] > 0:
                                            continue
                                        if _sa['matched'] > _matched:
                                            _matched = _sa['matched']
                                            _compId = compId
                                    if _compId is not None:
                                        updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, _compId)
                                        sortPolySeqRst(self.__polySeqRstFailed)

                        for sa in seqAlignFailed:
                            if sa['conflict'] == 0:
                                chainId = sa['test_chain_id']
                                _ps = next((_ps for _ps in self.__polySeqRstFailedAmbig if _ps['chain_id'] == chainId), None)
                                if _ps is None:
                                    continue
                                _matched = sa['matched']
                                for seqId, compIds in zip(_ps['seq_id'], _ps['comp_ids']):
                                    _compId = None
                                    for compId in list(compIds):
                                        _polySeqRstFailed = deepcopy(self.__polySeqRstFailed)
                                        updatePolySeqRst(_polySeqRstFailed, chainId, seqId, compId)
                                        sortPolySeqRst(_polySeqRstFailed)
                                        _seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, _polySeqRstFailed)
                                        _sa = next((_sa for _sa in _seqAlignFailed if _sa['test_chain_id'] == chainId), None)
                                        if _sa is None or _sa['conflict'] > 0:
                                            continue
                                        if _sa['matched'] > _matched:
                                            _matched = _sa['matched']
                                            _compId = compId
                                    if _compId is not None:
                                        updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, _compId)
                                        sortPolySeqRst(self.__polySeqRstFailed)

                        seqAlignFailed, _ = alignPolymerSequence(self.__pA, self.polySeq, self.__polySeqRstFailed)
                        chainAssignFailed, _ = assignPolymerSequence(self.__pA, self.ccU, self.file_type,
                                                                     self.polySeq, self.__polySeqRstFailed, seqAlignFailed)

                        if chainAssignFailed is not None:

                            seqIdRemap = []

                            cyclicPolymer = {}

                            for ca in chainAssignFailed:
                                ref_chain_id = ca['ref_chain_id']
                                test_chain_id = ca['test_chain_id']

                                sa = next(sa for sa in seqAlignFailed
                                          if sa['ref_chain_id'] == ref_chain_id
                                          and sa['test_chain_id'] == test_chain_id)

                                poly_seq_model = next(ps for ps in self.polySeq
                                                      if ps['auth_chain_id'] == ref_chain_id)
                                poly_seq_rst = next(ps for ps in self.__polySeqRstFailed
                                                    if ps['chain_id'] == test_chain_id)

                                seq_id_mapping = {}
                                for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                    if mid_code == '|' and test_seq_id is not None:
                                        try:
                                            seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                               in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                               if seq_id == ref_seq_id and isinstance(auth_seq_id, int))
                                        except StopIteration:
                                            pass

                                if ref_chain_id not in cyclicPolymer:
                                    cyclicPolymer[ref_chain_id] =\
                                        isCyclicPolymer(self.cR, self.polySeq, ref_chain_id,
                                                        self.representativeModelId, self.representativeAltId, self.modelNumName)

                                if cyclicPolymer[ref_chain_id]:

                                    poly_seq_model = next(ps for ps in self.polySeq
                                                          if ps['auth_chain_id'] == ref_chain_id)

                                    offset = None
                                    for seq_id, comp_id in zip(poly_seq_rst['seq_id'], poly_seq_rst['comp_id']):
                                        if seq_id is not None and seq_id not in seq_id_mapping:
                                            _seq_id = next((_seq_id for _seq_id, _comp_id in zip(poly_seq_model['seq_id'], poly_seq_model['comp_id'])
                                                            if _seq_id not in seq_id_mapping.values() and _comp_id == comp_id), None)
                                            if _seq_id is not None:
                                                offset = seq_id - _seq_id
                                                break

                                    if offset is not None:
                                        for seq_id in poly_seq_rst['seq_id']:
                                            if seq_id is not None and seq_id not in seq_id_mapping:
                                                seq_id_mapping[seq_id] = seq_id - offset

                                if any(True for k, v in seq_id_mapping.items() if k != v)\
                                   and not any(True for k, v in seq_id_mapping.items()
                                               if v in poly_seq_model['seq_id']
                                               and k == poly_seq_model['auth_seq_id'][poly_seq_model['seq_id'].index(v)]):
                                    seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': seq_id_mapping})

                            if len(seqIdRemap) > 0:
                                if 'seq_id_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['seq_id_remap'] = seqIdRemap

                            if any(True for ps in self.polySeq if 'identical_chain_id' in ps):
                                polySeqRst, chainIdMapping = splitPolySeqRstForMultimers(self.__pA, self.polySeq, self.__polySeqRstFailed, chainAssignFailed)

                                if polySeqRst is not None and (not self.hasNonPoly or self.__lenPolySeq // self.__lenNonPoly in (1, 2)):
                                    self.__polySeqRst = polySeqRst
                                    if 'chain_id_remap' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['chain_id_remap'] = chainIdMapping

                            if self.monoPolymer and len(self.__polySeqRstFailed) == 1:
                                polySeqRst, chainIdMapping, modelChainIdExt =\
                                    splitPolySeqRstForExactNoes(self.__pA, self.polySeq, self.__polySeqRstFailed, chainAssignFailed)

                                if polySeqRst is not None:
                                    self.__polySeqRst = polySeqRst
                                    if 'chain_id_clone' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['chain_id_clone'] = chainIdMapping
                                    if 'model_chain_id_ext' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['model_chain_id_ext'] = modelChainIdExt

                            if self.hasNonPoly:
                                polySeqRst, nonPolyMapping = splitPolySeqRstForNonPoly(self.ccU, self.__nonPoly, self.__polySeqRstFailed,
                                                                                       seqAlignFailed, chainAssignFailed)

                                if polySeqRst is not None:
                                    self.__polySeqRst = polySeqRst
                                    if 'non_poly_remap' not in self.reasonsForReParsing and len(nonPolyMapping) > 0:
                                        self.reasonsForReParsing['non_poly_remap'] = nonPolyMapping

                            if self.hasBranched:
                                polySeqRst, branchedMapping = splitPolySeqRstForBranched(self.__pA, self.polySeq, self.__branched, self.__polySeqRstFailed,
                                                                                         chainAssignFailed)

                                if polySeqRst is not None:
                                    self.__polySeqRst = polySeqRst
                                    if 'branched_remap' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['branched_remap'] = branchedMapping

            insuff_dist_atom_sel_warnings = [f for f in self.f if '[Insufficient atom selection]' in f and 'distance restraints' in f]

            if 'alt_global_sequence_offset' in self.reasonsForReParsing:
                if len(insuff_dist_atom_sel_warnings) < 20\
                   or not any(True for f in self.f if '[Insufficient atom selection]' in f)\
                   or len(self.reasonsForReParsing) > 1:
                    del self.reasonsForReParsing['alt_global_sequence_offset']
                else:
                    globalSequenceOffset = copy.copy(self.reasonsForReParsing['alt_global_sequence_offset'])
                    for k, v in globalSequenceOffset.items():
                        len_v = 0 if v is None else len(v)
                        if len_v != 1:
                            del self.reasonsForReParsing['alt_global_sequence_offset'][k]
                        else:
                            self.reasonsForReParsing['alt_global_sequence_offset'][k] = list(v)[0]
                    if len(self.reasonsForReParsing['alt_global_sequence_offset']) == 0:
                        del self.reasonsForReParsing['alt_global_sequence_offset']

            if 'local_seq_scheme' in self.reasonsForReParsing:
                if 'non_poly_remap' in self.reasonsForReParsing or 'branched_remap' in self.reasonsForReParsing\
                   or 'np_seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                if 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['seq_id_remap']

            if 'local_seq_scheme' in self.reasonsForReParsing:
                if 'label_seq_offset' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                elif len(self.reasonsForReParsing['local_seq_scheme']) == 1:
                    for k, v in self.reasonsForReParsing['local_seq_scheme'].items():
                        if k[0] == 'dist' and not v\
                           and k[1] > 1\
                           and len(insuff_dist_atom_sel_warnings) == 1\
                           and any(f'Check the {k[1]}th row of distance restraints' in f for f in insuff_dist_atom_sel_warnings):
                            set_label_seq_scheme()  # 2lif

            if 'seq_id_remap' in self.reasonsForReParsing and 'non_poly_remap' in self.reasonsForReParsing:
                if self.reasons is None and not any(True for f in self.f if '[Sequence mismatch]' in f):
                    del self.reasonsForReParsing['seq_id_remap']

            if 'np_seq_id_remap' in self.reasonsForReParsing and 'non_poly_remap' in self.reasonsForReParsing:
                effective = False
                for np_remap in self.reasonsForReParsing['np_seq_id_remap']:
                    chainId = np_remap['chain_id']
                    seqIdDict = np_remap['seq_id_dict']
                    for compId, _seqIdDict in self.reasonsForReParsing['non_poly_remap'].items():
                        for _seqId in _seqIdDict:
                            if _seqId in seqIdDict.values():
                                _seqId_ = next(k for k, v in seqIdDict.items() if v == _seqId)
                                if _seqId_ != _seqId:
                                    effective = True
                                    break
                if not effective:
                    del self.reasonsForReParsing['np_seq_id_remap']

            if len(self.__polySeqRstValid) > 0:
                sortPolySeqRst(self.__polySeqRstValid)

            label_seq_scheme = 'label_seq_scheme' in self.reasonsForReParsing\
                and all(t for t in self.reasonsForReParsing['label_seq_scheme'].values())
            local_to_label_seq_scheme = False  # 2lp4

            assert_auth_seq_scheme = 'global_auth_sequence_offset' in self.reasonsForReParsing and not label_seq_scheme

            if 'global_sequence_offset' in self.reasonsForReParsing:
                globalSequenceOffset = copy.copy(self.reasonsForReParsing['global_sequence_offset'])
                for k, v in globalSequenceOffset.items():
                    if v is None:
                        del self.reasonsForReParsing['global_sequence_offset'][k]  # 2l12
                        if not label_seq_scheme\
                           and 'global_auth_sequence_offset' not in self.reasonsForReParsing\
                           and 'segment_id_mismatch' not in self.reasonsForReParsing:  # 2n2w, 2b87, 2mf6 (excl label_seq_scheme)
                            if 'uninterpretable_chain_id' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['uninterpretable_chain_id'] = {}
                            self.reasonsForReParsing['uninterpretable_chain_id'][k] = True  # 2lqc
                if len(self.reasonsForReParsing['global_sequence_offset']) == 0:
                    del self.reasonsForReParsing['global_sequence_offset']

            if 'global_sequence_offset' in self.reasonsForReParsing:
                globalSequenceOffset = copy.copy(self.reasonsForReParsing['global_sequence_offset'])
                has_label_seq_scheme_pred = False
                for k, v in globalSequenceOffset.items():
                    len_v = 0 if v is None else len(v)
                    if len_v != 1:
                        ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == k), None)
                        if ps is not None:
                            try:
                                offset = ps['auth_seq_id'][0] - ps['seq_id'][0]
                                if offset == ps['auth_seq_id'][-1] - ps['seq_id'][-1] and offset in v:
                                    has_label_seq_scheme_pred = True
                            except TypeError:
                                pass
                        del self.reasonsForReParsing['global_sequence_offset'][k]
                    else:
                        self.reasonsForReParsing['global_sequence_offset'][k] = list(v)[0]
                    if len(self.reasonsForReParsing['global_sequence_offset']) == 0:
                        del self.reasonsForReParsing['global_sequence_offset']
                        if len_v > 2:
                            if 'label_seq_scheme' in self.reasonsForReParsing and not has_label_seq_scheme_pred:
                                del self.reasonsForReParsing['label_seq_scheme']
                            if 'seq_id_remap' in self.reasonsForReParsing:
                                del self.reasonsForReParsing['seq_id_remap']

            seqIdRemapForRemaining = []
            if 'global_sequence_offset' in self.reasonsForReParsing:
                if 'local_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                if 'label_seq_offset' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['label_seq_offset']
                if 'label_seq_scheme' in self.reasonsForReParsing:
                    if 'global_auth_sequence_offset' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['global_auth_sequence_offset'] = self.reasonsForReParsing['global_sequence_offset']
                        del self.reasonsForReParsing['global_sequence_offset']
                    no_gap = True
                    for ps in self.polySeq:
                        chainId = ps['auth_chain_id']
                        if chainId not in self.reasonsForReParsing['global_auth_sequence_offset']:
                            if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                                offset = next(seq_id - auth_seq_id for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']))
                                if any(abs(seq_id - auth_seq_id - offset) > 20 for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id'])):
                                    failed_ps = next((failed_ps for failed_ps in self.__polySeqRstFailed if failed_ps['chain_id'] == chainId), None)
                                    if failed_ps is None:
                                        continue
                                    if any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in failed_ps['seq_id']):
                                        seqIdRemapForRemaining.append({'chain_id': chainId, 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})
                            elif any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in ps['seq_id']):
                                safe = True
                                for _ps in self.polySeq:
                                    if _ps['auth_chain_id'] in self.reasonsForReParsing['global_auth_sequence_offset']:
                                        if any(seq_id in ps['seq_id'] and seq_id in _ps['auth_seq_id'] for seq_id in ps['seq_id']):
                                            safe = False
                                            break
                                if safe:
                                    seqIdRemapForRemaining.append({'chain_id': chainId, 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})
                            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                                _ps = next((_ps for _ps in self.__polySeqRstFailed if _ps['chain_id'] == chainId), None)
                                if _ps is None or not all(_seq_id in ps['seq_id'] for _seq_id, _comp_id in zip(_ps['seq_id'], _ps['comp_id']) if _comp_id not in emptyValue):
                                    del self.reasonsForReParsing['global_auth_sequence_offset'][chainId]
                                    if len(self.reasonsForReParsing['global_auth_sequence_offset']) == 0:
                                        del self.reasonsForReParsing['global_auth_sequence_offset']
                                    no_gap = False
                    if no_gap:
                        del self.reasonsForReParsing['label_seq_scheme']
                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['inhibit_label_seq_scheme']
                if 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['seq_id_remap']

            if 'global_auth_sequence_offset' in self.reasonsForReParsing:
                if 'local_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                if 'label_seq_scheme' in self.reasonsForReParsing:
                    no_gap = True
                    for ps in self.polySeq:
                        chainId = ps['auth_chain_id']
                        if chainId not in self.reasonsForReParsing['global_auth_sequence_offset']:
                            if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                                offset = next(seq_id - auth_seq_id for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']))
                                if any(abs(seq_id - auth_seq_id - offset) > 20 for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id'])):
                                    failed_ps = next((failed_ps for failed_ps in self.__polySeqRstFailed if failed_ps['chain_id'] == chainId), None)
                                    if failed_ps is None:
                                        continue
                                    if any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in failed_ps['seq_id']):
                                        seqIdRemapForRemaining.append({'chain_id': chainId, 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})
                            elif any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in ps['seq_id']):
                                safe = True
                                for _ps in self.polySeq:
                                    if _ps['auth_chain_id'] in self.reasonsForReParsing['global_auth_sequence_offset']:
                                        if any(seq_id in ps['seq_id'] and seq_id in _ps['auth_seq_id'] for seq_id in ps['seq_id']):
                                            safe = False
                                            break
                                if safe:
                                    seqIdRemapForRemaining.append({'chain_id': chainId, 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})
                        elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            _ps = next((_ps for _ps in self.__polySeqRstFailed if _ps['chain_id'] == chainId), None)
                            if _ps is None or not all(_seq_id in ps['seq_id'] for _seq_id, _comp_id in zip(_ps['seq_id'], _ps['comp_id']) if _comp_id not in emptyValue):
                                del self.reasonsForReParsing['global_auth_sequence_offset'][chainId]
                                if len(self.reasonsForReParsing['global_auth_sequence_offset']) == 0:
                                    del self.reasonsForReParsing['global_auth_sequence_offset']
                                no_gap = False
                    if no_gap:
                        del self.reasonsForReParsing['label_seq_scheme']
                if 'label_seq_offset' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['label_seq_offset']
                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['inhibit_label_seq_scheme']
                if 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['seq_id_remap']
                if len(_seqIdRemap) > 0 and 'chain_id_remap' not in self.reasonsForReParsing:
                    _chainIds = [d['chain_id'] for d in _seqIdRemap]
                    chainIds = [k for k, v in self.reasonsForReParsing['global_auth_sequence_offset'].items() if v is not None]
                    if any(_c in chainIds for _c in _chainIds) and len(chainIds) < len(_chainIds):
                        chainIdRemap = {}
                        valid = True
                        for d in _seqIdRemap:
                            chainId = d['chain_id']
                            ps = next(ps for ps in self.polySeq if ps['auth_chain_id'] == chainId)
                            subst_label_seq_scheme = ps['seq_id'] == ps['auth_seq_id']  # 2n2w
                            if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                                valid = False
                                break
                            if chainId in chainIds:
                                offset = next(v for k, v in self.reasonsForReParsing['global_auth_sequence_offset'].items() if k == chainId and v is not None)
                                for auth_seq_id in ps['auth_seq_id']:
                                    if auth_seq_id - offset in chainIdRemap:
                                        valid = False
                                        break
                                    chainIdRemap[auth_seq_id - offset] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                            else:
                                if label_seq_scheme or subst_label_seq_scheme or 'local_seq_scheme' in self.reasonsForReParsing:
                                    for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']):
                                        if seq_id in chainIdRemap:
                                            valid = False
                                            break
                                        chainIdRemap[seq_id] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                                else:
                                    for auth_seq_id in ps['auth_seq_id']:
                                        if auth_seq_id in chainIdRemap:
                                            valid = False
                                            break
                                        if len(_chainIds) > 1:
                                            overlap = False
                                            for _chainId in _chainIds:
                                                if _chainId == chainId:
                                                    continue
                                                _ps = next(_ps for _ps in self.polySeq if _ps['auth_chain_id'] == _chainId)
                                                if auth_seq_id in ps['auth_seq_id']:
                                                    overlap = True
                                                    break
                                            if overlap:  # 2law
                                                continue
                                        chainIdRemap[auth_seq_id] = {'chain_id': chainId, 'seq_id': auth_seq_id}
                        if valid:
                            if 'global_sequence_offset' in self.reasonsForReParsing:
                                del self.reasonsForReParsing['global_sequence_offset']
                            del self.reasonsForReParsing['global_auth_sequence_offset']
                            self.reasonsForReParsing['chain_id_remap'] = chainIdRemap

            if len(seqIdRemapForRemaining) > 0:
                self.reasonsForReParsing['seq_id_remap'] = seqIdRemapForRemaining

            insuff_dist_atom_sel_in_1st_row_warnings = [f for f in insuff_dist_atom_sel_warnings if 'Check the 1th row of distance restraints' in f]
            invalid_dist_atom_sel_in_1st_row = any(True for f in self.f if 'Check the 1th row of distance restraints' in f
                                                   and ('[Atom not found]' in f or '[Hydrogen not instantiated]' in f or '[Coordinate issue]' in f))

            if 'local_seq_scheme' in self.reasonsForReParsing\
               and (len(self.reasonsForReParsing) == 1 or len(insuff_dist_atom_sel_warnings) == len(self.f)  # 2ljb
                    or 'label_seq_scheme' in self.reasonsForReParsing):  # 2joa
                mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                sortPolySeqRst(self.__polySeqRstFailed)

                valid = True
                if len(self.__polySeqRstFailed) > 0 and 'label_seq_scheme' not in self.reasonsForReParsing:  # 6qeu
                    for _ps in self.__polySeqRstFailed:
                        ps = next((ps for ps in self.__polySeqRstValid if ps['chain_id'] == _ps['chain_id']), None)
                        if ps is None:
                            break
                        if len([compId for compId in ps['comp_id'] if compId not in emptyValue]) > len(_ps['comp_id']) * 2:
                            valid = False
                            break
                if len(self.__polySeqRstFailed) > 0:
                    self.reasonsForReParsing['extend_seq_scheme'] = self.__polySeqRstFailed
                if valid:
                    if len(insuff_dist_atom_sel_in_1st_row_warnings) > 0 and not invalid_dist_atom_sel_in_1st_row:
                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['label_seq_scheme'] = {}
                        self.reasonsForReParsing['label_seq_scheme']['dist'] = True
                        set_label_seq_scheme()
                        local_to_label_seq_scheme = True  # 2ljb, 2lp4
                    else:
                        del self.reasonsForReParsing['local_seq_scheme']
                else:  # 2ld3
                    if 'inhibit_label_seq_scheme' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['inhibit_label_seq_scheme'] = {}
                    set_label_seq_scheme()
                    for ps in self.__polySeqRstValid:
                        chainId = ps['chain_id']
                        if 'label_seq_scheme' in self.reasonsForReParsing:
                            self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId] = self.reasonsForReParsing['label_seq_scheme']
                    if 'local_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['local_seq_scheme']
                    if 'label_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['label_seq_scheme']

            if 'label_seq_scheme' in self.reasonsForReParsing and 'extend_seq_scheme' in self.reasonsForReParsing:  # 2mbv
                for _ps in self.reasonsForReParsing['extend_seq_scheme']:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == _ps['chain_id']), None)
                    if ps is None:
                        continue
                    if all(seqId in ps['seq_id'] for seqId in _ps['seq_id']):
                        self.reasonsForReParsing['extend_seq_scheme'].remove(_ps)
                if len(self.reasonsForReParsing['extend_seq_scheme']) == 0:
                    del self.reasonsForReParsing['extend_seq_scheme']

            if self.hasAnyRestraints():

                if len(self.f) == 0\
                   and 'label_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['label_seq_scheme']
                    if 'local_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['local_seq_scheme']

                elif all('[Anomalous data]' in f for f in self.f)\
                        and all('distance' in f for f in self.f)\
                        and 'label_seq_scheme' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['label_seq_scheme']
                    if 'local_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['local_seq_scheme']
                    __f = deepcopy(self.f)
                    self.f = []
                    for f in __f:
                        self.f.append(re.sub(r'\[Anomalous data\]', '[Atom not found]', f, 1))

                elif all('[Anomalous data]' in f for f in self.f):
                    pass

                elif not any(True for f in self.f if '[Atom not found]' in f or '[Anomalous data]' in f)\
                        and 'non_poly_remap' not in self.reasonsForReParsing\
                        and 'branch_remap' not in self.reasonsForReParsing:

                    # ad hoc sequence scheme switching of distance restraints should be inherited
                    if len(insuff_dist_atom_sel_in_1st_row_warnings) > 0 and not invalid_dist_atom_sel_in_1st_row\
                       and (len(self.reasonsForReParsing) == 0 or (len(self.reasonsForReParsing) == 1 and 'label_seq_scheme' in self.reasonsForReParsing))\
                       and (any(True for f in insuff_dist_atom_sel_in_1st_row_warnings if '_distance_' in f)
                            or (len(insuff_dist_atom_sel_warnings) == 1 and any(True for f in insuff_dist_atom_sel_in_1st_row_warnings if 'None' in f))):
                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['label_seq_scheme'] = {}
                        self.reasonsForReParsing['label_seq_scheme']['dist'] = True
                        set_label_seq_scheme()

                    elif len(self.reasonsForReParsing) > 0 and self.distRestraints > 0\
                            and 'global_auth_sequence_offset' not in self.reasonsForReParsing\
                            and len(insuff_dist_atom_sel_in_1st_row_warnings) == 0\
                            and not all('[Insufficient atom selection]' in f and 'distance restraints' in f for f in self.f):
                        if any('[Insufficient atom selection]' in f and 'distance restraints' not in f for f in self.f):
                            if 'label_seq_scheme' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['label_seq_scheme'] = {}
                            self.reasonsForReParsing['label_seq_scheme']['dist'] = True
                            set_label_seq_scheme()
                        elif 'np_seq_id_remap' not in self.reasonsForReParsing and 'non_poly_remap' not in self.reasonsForReParsing:  # 2lml
                            if 'assert_label_seq_scheme' not in self.reasonsForReParsing\
                               and 'assert_uniq_segment_id' not in self.reasonsForReParsing:  # 2m0k
                                self.reasonsForReParsing = {}

                    if any(True for f in self.f if '[Sequence mismatch]' in f):
                        __f = copy.copy(self.f)
                        for f in __f:
                            if '[Sequence mismatch]' in f:
                                self.f.remove(f)

                elif not assert_auth_seq_scheme:  # 2n0s
                    if 'label_seq_offset' in self.reasonsForReParsing and len(insuff_dist_atom_sel_in_1st_row_warnings) > 0 and not invalid_dist_atom_sel_in_1st_row\
                       and (any(True for f in insuff_dist_atom_sel_in_1st_row_warnings if '_distance_' in f)
                            or (len(insuff_dist_atom_sel_warnings) >= 1 and any(True for f in insuff_dist_atom_sel_in_1st_row_warnings if 'None' in f))):
                        if len(pro_hn_atom_not_found_warnings) + len(gly_hb_atom_not_found_warnings) > 0:
                            for chain_id in self.reasonsForReParsing['label_seq_offset']:
                                pro_seq_ids, gly_seq_ids = set(), set()
                                for f in pro_hn_atom_not_found_warnings:
                                    g = self.__pro_hn_atom_not_found_pat.search(f).groups()
                                    if g[0] != chain_id:
                                        continue
                                    pro_seq_ids.add(int(g[1]))
                                for f in gly_hb_atom_not_found_warnings:
                                    g = self.__gly_hb_atom_not_found_pat.search(f).groups()
                                    if g[0] != chain_id:
                                        continue
                                    gly_seq_ids.add(int(g[1]))
                                if len(pro_seq_ids) + len(gly_seq_ids) == 0:
                                    continue
                                ps = next((ps for ps in self.polySeq if ps['chain_id'] == chain_id), None)
                                if ps is not None and ps['comp_id'][0] == 'ACE':
                                    self.reasonsForReParsing['label_seq_offset'][chain_id] = 1
                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['label_seq_scheme'] = {}
                        self.reasonsForReParsing['label_seq_scheme']['dist'] = True
                        set_label_seq_scheme()

                    elif ('non_poly_remap' in self.reasonsForReParsing or 'branch_remap' in self.reasonsForReParsing)\
                            and 'global_sequence_offset' not in self.reasonsForReParsing\
                            and 'global_auth_sequence_offset' not in self.reasonsForReParsing\
                            and 'segment_id_mismatch' not in self.reasonsForReParsing:
                        if self.distRestraints > 0 or self.monoPolymer or all('identical_chain_id' in ps for ps in self.polySeq):
                            if 'label_seq_scheme' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['label_seq_scheme'] = {}
                            self.reasonsForReParsing['label_seq_scheme']['dist'] = True
                            set_label_seq_scheme()

            elif self.reasons is None and len(self.reasonsForReParsing) == 0 and all('[Insufficient atom selection]' in f for f in self.f):
                set_label_seq_scheme()

            if self.reasons is None and self.__complexSeqScheme and 'inhibit_label_seq_scheme_stats' in self.reasonsForReParsing:
                if 'label_seq_scheme' not in self.reasonsForReParsing:
                    del self.reasonsForReParsing['inhibit_label_seq_scheme_stats']
                else:
                    positive = negative = 0  # 2n1a
                    for ps in self.polySeq:
                        if ps['auth_chain_id'] in self.reasonsForReParsing['inhibit_label_seq_scheme_stats']:
                            if self.reasonsForReParsing['inhibit_label_seq_scheme_stats'][ps['auth_chain_id']] / len(ps['seq_id']) < 1.0:  # 2ruk
                                negative += 1
                                del self.reasonsForReParsing['inhibit_label_seq_scheme_stats'][ps['auth_chain_id']]
                            else:
                                positive += 1
                    if len(self.reasonsForReParsing['inhibit_label_seq_scheme_stats']) == 0 or positive * negative == 0:
                        del self.reasonsForReParsing['inhibit_label_seq_scheme_stats']

            if 'segment_id_mismatch' in self.reasonsForReParsing:
                if 'np_seq_id_remap' not in self.reasonsForReParsing and 'non_poly_remap' not in self.reasonsForReParsing\
                   and not local_to_label_seq_scheme\
                   and 'inhibit_label_seq_scheme' not in self.reasonsForReParsing:  # 2ljb, 2lp4, 1qkg, 2lkm
                    if 'local_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['local_seq_scheme']
                    if 'label_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['label_seq_scheme']
                    if 'label_seq_offset' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['label_seq_offset']

                for chainId, _chainId in self.reasonsForReParsing['segment_id_mismatch'].items():
                    uniq = True
                    for k, v in self.reasonsForReParsing['segment_id_mismatch'].items():
                        if k == chainId:
                            continue
                        if v == _chainId:
                            uniq = False
                            break
                    if not uniq:
                        ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == _chainId and 'identical_auth_chain_id' in ps), None)
                        if ps is not None:
                            dst_chain_id_set = [_chainId]
                            dst_chain_id_set.extend(ps['identical_auth_chain_id'])
                            dst_chain_id_set.sort()
                            src_chain_id_set = [chainId]
                            for k, v in self.reasonsForReParsing['segment_id_mismatch'].items():
                                if k == chainId or v not in dst_chain_id_set:
                                    continue
                                src_chain_id_set.append(k)
                            src_chain_id_set.sort()
                            for src_chain_id, dst_chain_id in zip(src_chain_id_set, dst_chain_id_set):
                                self.reasonsForReParsing['segment_id_mismatch'][src_chain_id] = dst_chain_id

                if 'inhibit_label_seq_scheme' in self.reasonsForReParsing\
                   and len(self.reasonsForReParsing['inhibit_label_seq_scheme']) == len(set(filter(None, self.reasonsForReParsing['segment_id_mismatch'].values())))\
                   and all(chainId in self.reasonsForReParsing['segment_id_mismatch'].values()
                           for chainId in self.reasonsForReParsing['inhibit_label_seq_scheme']):  # 2ljc, 1qkg
                    if 'local_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['local_seq_scheme']
                    if 'label_seq_scheme' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['label_seq_scheme']
                    if 'label_seq_offset' in self.reasonsForReParsing:
                        del self.reasonsForReParsing['label_seq_offset']

                if (label_seq_scheme and 'inhibit_label_seq_scheme' not in self.reasonsForReParsing)\
                   or ('np_seq_id_remap' in self.reasonsForReParsing or 'non_poly_remap' in self.reasonsForReParsing):  # 6f0y, 2lkm, 2mnz
                    for chain_id in self.reasonsForReParsing['segment_id_mismatch'].values():
                        ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id), None)
                        if ps is None:
                            continue
                        if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                            offset = next(seq_id - auth_seq_id for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id']))
                            if any(abs(seq_id - auth_seq_id - offset) > 20 for seq_id, auth_seq_id in zip(ps['seq_id'], ps['auth_seq_id'])):
                                failed_ps = next((failed_ps for failed_ps in self.__polySeqRstFailed if failed_ps['chain_id'] == ps['auth_chain_id']), None)
                                if failed_ps is None:
                                    continue
                                if any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in failed_ps['seq_id']):
                                    seqIdRemapForRemaining.append({'chain_id': ps['auth_chain_id'], 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})
                        elif any(seq_id in ps['seq_id'] and seq_id not in ps['auth_seq_id'] for seq_id in ps['seq_id']):
                            safe = True
                            for _ps in self.polySeq:
                                if _ps['auth_chain_id'] != ps['auth_chain_id']:
                                    if any(seq_id in ps['seq_id'] and seq_id in _ps['auth_seq_id'] for seq_id in ps['seq_id']):
                                        safe = False
                                        break
                            if 'np_seq_id_remap' in self.reasonsForReParsing or 'non_poly_remap' in self.reasonsForReParsing:
                                for _np in self.nonPolySeq:
                                    if _np['auth_chain_id'] == chain_id:
                                        safe = False  # 2lba
                                        break
                            if safe:
                                seqIdRemapForRemaining.append({'chain_id': ps['auth_chain_id'], 'seq_id_dict': dict(zip(ps['seq_id'], ps['auth_seq_id']))})

                    if len(seqIdRemapForRemaining) > 0:
                        self.reasonsForReParsing['seq_id_remap'] = seqIdRemapForRemaining

                if 'chain_id_remap' in self.reasonsForReParsing:
                    stat_chain_ids = set()
                    for v in self.reasonsForReParsing['segment_id_match_stats'].values():
                        for _k, _v in v.items():
                            if _v > 0:
                                stat_chain_ids.add(_k)
                    map_chain_ids = set()
                    for v in self.reasonsForReParsing['chain_id_remap'].values():
                        map_chain_ids.add(v['chain_id'])
                    if stat_chain_ids == map_chain_ids:
                        # del self.reasonsForReParsing['segment_id_mismatch'] 6f0y
                        del self.reasonsForReParsing['segment_id_match_stats']
                        del self.reasonsForReParsing['segment_id_poly_type_stats']
                        if 'global_auth_sequence_offset' in self.reasonsForReParsing:
                            del self.reasonsForReParsing['global_auth_sequence_offset']

                if len(self.f) == 0 and len(self.reasonsForReParsing) > 0:
                    if 'assert_label_seq_scheme' not in self.reasonsForReParsing\
                       and 'assert_uniq_segment_id' not in self.reasonsForReParsing:
                        self.reasonsForReParsing = {}

            elif 'chain_id_remap' in self.reasonsForReParsing:
                if 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['seq_id_remap']  # 6ijv

                if 'global_auth_sequence_offset' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['global_auth_sequence_offset']  # 2lzs

                if len(self.f) == 0 and len(self.reasonsForReParsing) > 0:
                    if 'assert_label_seq_scheme' not in self.reasonsForReParsing\
                       and 'assert_uniq_segment_id' not in self.reasonsForReParsing:
                        self.reasonsForReParsing = {}

            if len(self.reasonsForReParsing) == 0 and self.reasons is None\
               and any('[Insufficient atom selection]' in f and 'Macromolecules page' in f for f in self.f):
                __f = deepcopy(self.f)
                self.f = []
                for f in __f:
                    if '[Insufficient atom selection]' in f and 'Macromolecules page' in f:
                        self.f.append(f.replace('[Insufficient atom selection]', '[Sequence mismatch warning]'))  # 2laz
                    else:
                        self.f.append(f)

        finally:
            self.warningMessage = sorted(list(set(self.f)), key=self.f.index)

            self.getRealCompId.cache_clear()
            self.getRealChainId.cache_clear()
            self.getCoordAtomSiteOf.cache_clear()

            translateToStdAtomNameNoRef.cache_clear()
            translateToStdAtomNameWithRef.cache_clear()

    def validateDistanceRange(self, weight: float, target_value: Optional[float],
                              lower_limit: Optional[float], upper_limit: Optional[float],
                              lower_linear_limit: Optional[float], upper_linear_limit: Optional[float],
                              squareExponent: Optional[float] = None) -> Optional[dict]:
        """ Validate distance value range.
        """

        validRange = True
        if self.file_type in ('nm-res-cns', 'nm-res-xpl'):
            dstFunc = {'weight': weight, 'potential': self.noePotential, 'average': self.noeAverage}
        elif self.file_type == 'nm-res-cha':
            dstFunc = {'weight': weight, 'average': self.noeAverage, 'exponent_over_upper_limit': squareExponent}
        elif self.file_type == 'nm-res-sch':
            dstFunc = {'weight': weight, 'energy_const': squareExponent}
        else:
            return None

        if None not in (target_value, upper_limit, lower_limit)\
           and abs(target_value - lower_limit) <= DIST_AMBIG_UNCERT\
           and abs(target_value - upper_limit) <= DIST_AMBIG_UNCERT:
            if target_value >= DIST_AMBIG_MED:
                lower_limit = lower_linear_limit = None
            elif target_value <= DIST_AMBIG_LOW:
                upper_limit = upper_linear_limit = None

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and self.allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value}" if target_value > 0.0 else "0.0"
            else:
                if target_value <= DIST_ERROR_MIN and self.omitDistLimitOutlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The target value='{target_value}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    target_value = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The target value='{target_value}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}" if lower_limit > 0.0 else "0.0"
            else:
                if lower_limit <= DIST_ERROR_MIN and self.omitDistLimitOutlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    lower_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and self.allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}" if upper_limit > 0.0 else "0.0"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and self.omitDistLimitOutlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    upper_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if DIST_ERROR_MIN <= lower_linear_limit < DIST_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.3f}" if lower_linear_limit > 0.0 else "0.0"
            else:
                if lower_linear_limit <= DIST_ERROR_MIN and self.omitDistLimitOutlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    lower_linear_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if DIST_ERROR_MIN < upper_linear_limit <= DIST_ERROR_MAX or (upper_linear_limit == 0.0 and self.allowZeroUpperLimit):
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.3f}" if upper_linear_limit > 0.0 else "0.0"
            else:
                if (upper_linear_limit <= DIST_ERROR_MIN or upper_linear_limit > DIST_ERROR_MAX) and self.omitDistLimitOutlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    upper_linear_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value}'. "
                                  "It indicates that a negative value was unexpectedly set: "
                                  f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the target value '{target_value}'. "
                                  "It indicates that a negative value was unexpectedly set: "
                                  f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value}'. "
                                  "It indicates that a negative value was unexpectedly set: "
                                  f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.3f}' must be greater than the target value '{target_value}'. "
                                  "It indicates that a negative value was unexpectedly set: "
                                  f"d={target_value}, dminus={self.numberSelection[1]}, dplus={self.numberSelection[2]}.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_linear_limit:.3f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the upper limit value '{upper_linear_limit:.3f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the lower limit value '{lower_limit:.3f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' must be less than the upper linear limit value '{upper_linear_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {DIST_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if DIST_RANGE_MIN <= lower_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if DIST_RANGE_MIN <= upper_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if DIST_RANGE_MIN <= lower_linear_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if DIST_RANGE_MIN <= upper_linear_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validateAngleRange(self, weight: float, misc_dict: dict, target_value: Optional[float],
                           lower_limit: Optional[float], upper_limit: Optional[float],
                           lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate angle value range (SCHRODINGER specific).
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit, lower_linear_limit, upper_linear_limit],
                                 dtype=float)

            shift = None
            if numpy.nanmin(_array) >= THRESHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmax(_array) // 360) * 360
            elif numpy.nanmax(_array) <= -THRESHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmin(_array) // 360) * 360
            if shift is not None:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              "The target/limit values for an angle restraint have been circularly shifted "
                              f"to fit within range {ANGLE_RESTRAINT_ERROR}.")
                if target_value is not None:
                    target_value += shift
                if lower_limit is not None:
                    lower_limit += shift
                if upper_limit is not None:
                    upper_limit += shift
                if lower_linear_limit is not None:
                    upper_linear_limit += shift
                if upper_linear_limit is not None:
                    upper_linear_limit += shift

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if ANGLE_ERROR_MIN <= lower_linear_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if ANGLE_ERROR_MIN < upper_linear_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if None not in (lower_limit, lower_linear_limit):
            if lower_linear_limit > lower_limit:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.3f}' must be less than the lower limit value '{lower_limit:.3f}'.")

        if None not in (upper_limit, upper_linear_limit):
            if upper_limit > upper_linear_limit:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.3f}' must be less than the upper linear limit value '{upper_linear_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if ANGLE_RANGE_MIN <= lower_linear_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if ANGLE_RANGE_MIN <= upper_linear_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        if None not in (upper_limit, lower_limit)\
           and (PLANE_LIKE_LOWER_LIMIT <= lower_limit < 0.0 < upper_limit <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 180.0 < 0.0 < upper_limit - 180.0 <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 360.0 < 0.0 < upper_limit - 360.0 <= PLANE_LIKE_UPPER_LIMIT):
            dstFunc['plane_like'] = True

        return dstFunc

    def validateRdcRange(self, weight: float, misc_dict: dict, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float],
                         lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

        if target_value is not None:
            if RDC_ERROR_MIN < target_value < RDC_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if RDC_ERROR_MIN <= lower_limit < RDC_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if RDC_ERROR_MIN < upper_limit <= RDC_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if RDC_ERROR_MIN <= lower_linear_limit < RDC_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if RDC_ERROR_MIN < upper_linear_limit <= RDC_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if RDC_RANGE_MIN <= target_value <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {RDC_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if RDC_RANGE_MIN <= lower_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if RDC_RANGE_MIN <= upper_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if RDC_RANGE_MIN <= lower_linear_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if RDC_RANGE_MIN <= upper_linear_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validateRdcRange2(self, weight: float, misc_dict: dict,
                          target_value_1: Optional[float], lower_limit_1: Optional[float], upper_limit_1: Optional[float],
                          target_value_2: Optional[float], lower_limit_2: Optional[float], upper_limit_2: Optional[float]) -> Optional[dict]:
        """ Validate two RDC value ranges.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if isinstance(misc_dict, dict):
            for k, v in misc_dict.items():
                dstFunc[k] = v

        if RDC_ERROR_MIN < target_value_1 < RDC_ERROR_MAX:
            dstFunc['target_value_1'] = f"{target_value_1:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The target value(1)='{target_value_1}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN <= lower_limit_1 < RDC_ERROR_MAX:
            dstFunc['lower_limit_1'] = f"{lower_limit_1:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(1)='{lower_limit_1:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < upper_limit_1 <= RDC_ERROR_MAX:
            dstFunc['upper_limit_1'] = f"{upper_limit_1:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(1)='{upper_limit_1:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < target_value_2 < RDC_ERROR_MAX:
            dstFunc['target_value_2'] = f"{target_value_2:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The target value(2)='{target_value_2}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN <= lower_limit_2 < RDC_ERROR_MAX:
            dstFunc['lower_limit_2'] = f"{lower_limit_2:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(2)='{lower_limit_2:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if RDC_ERROR_MIN < upper_limit_2 <= RDC_ERROR_MAX:
            dstFunc['upper_limit_2'] = f"{upper_limit_2:.6f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(2)='{upper_limit_2:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_limit_1 > target_value_1:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(1)='{lower_limit_1:.6f}' must be less than the target value(1) '{target_value_1}'.")

        if upper_limit_1 < target_value_1:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(1)='{upper_limit_1:.6f}' must be greater than the target value(1) '{target_value_1}'.")

        if lower_limit_2 > target_value_2:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(2)='{lower_limit_2:.6f}' must be less than the target value(2) '{target_value_2}'.")

        if upper_limit_2 < target_value_2:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(2)='{upper_limit_2:.6f}' must be greater than the target value(2) '{target_value_2}'.")

        if not validRange:
            return None

        if RDC_RANGE_MIN <= target_value_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The target value(1)='{target_value_1}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= lower_limit_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The lower limit value(1)='{lower_limit_1:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= upper_limit_1 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The upper limit value(1)='{upper_limit_1:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= target_value_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The target value(2)='{target_value_2}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= lower_limit_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The lower limit value(2)='{lower_limit_2:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if RDC_RANGE_MIN <= upper_limit_2 <= RDC_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The upper limit value(2)='{upper_limit_2:.6f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if target_value_1 is None and lower_limit_1 is None and upper_limit_1 is None:
            return None

        if target_value_2 is None and lower_limit_2 is None and upper_limit_2 is None:
            return None

        return dstFunc

    def validateAngleRange2(self, weight: float,
                            target_value_1: Optional[float], lower_limit_1: Optional[float], upper_limit_1: Optional[float],
                            target_value_2: Optional[float], lower_limit_2: Optional[float], upper_limit_2: Optional[float]) -> Optional[dict]:
        """ Validate two angle value ranges.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if ANGLE_ERROR_MIN < target_value_1 < ANGLE_ERROR_MAX:
            dstFunc['target_value_1'] = f"{target_value_1}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The target value(1)='{target_value_1}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN <= lower_limit_1 < ANGLE_ERROR_MAX:
            dstFunc['lower_limit_1'] = f"{lower_limit_1:.3f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(1)='{lower_limit_1:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < upper_limit_1 <= ANGLE_ERROR_MAX:
            dstFunc['upper_limit_1'] = f"{upper_limit_1:.3f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(1)='{upper_limit_1:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < target_value_2 < ANGLE_ERROR_MAX:
            dstFunc['target_value_2'] = f"{target_value_2}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The target value(2)='{target_value_2}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN <= lower_limit_2 < ANGLE_ERROR_MAX:
            dstFunc['lower_limit_2'] = f"{lower_limit_2:.3f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The lower limit value(2)='{lower_limit_2:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if ANGLE_ERROR_MIN < upper_limit_2 <= ANGLE_ERROR_MAX:
            dstFunc['upper_limit_2'] = f"{upper_limit_2:.3f}"
        else:
            validRange = False
            self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                          f"The upper limit value(2)='{upper_limit_2:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if not validRange:
            return None

        if ANGLE_RANGE_MIN <= target_value_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The target value(1)='{target_value_1}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= lower_limit_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The lower limit value(1)='{lower_limit_1:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= upper_limit_1 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The upper limit value(1)='{upper_limit_1:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= target_value_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The target value(2)='{target_value_2}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= lower_limit_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The lower limit value(2)='{lower_limit_2:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if ANGLE_RANGE_MIN <= upper_limit_2 <= ANGLE_RANGE_MAX:
            pass
        else:
            self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                          f"The upper limit value(2)='{upper_limit_2:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if target_value_1 is None and lower_limit_1 is None and upper_limit_1 is None:
            return None

        if target_value_2 is None and lower_limit_2 is None and upper_limit_2 is None:
            return None

        return dstFunc

    def validateT1T2Range(self, weight: float, target_value: Optional[float],
                          lower_limit: Optional[float], upper_limit: Optional[float],
                          lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate T1/T2 value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if T1T2_ERROR_MIN < target_value < T1T2_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if T1T2_ERROR_MIN <= lower_limit < T1T2_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if T1T2_ERROR_MIN < upper_limit <= T1T2_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if T1T2_ERROR_MIN <= lower_linear_limit < T1T2_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if T1T2_ERROR_MIN < upper_linear_limit <= T1T2_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {T1T2_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if T1T2_RANGE_MIN <= target_value <= T1T2_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if T1T2_RANGE_MIN <= lower_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if T1T2_RANGE_MIN <= upper_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if T1T2_RANGE_MIN <= lower_linear_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if T1T2_RANGE_MIN <= upper_linear_limit <= T1T2_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {T1T2_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validateCsaRange(self, weight: float, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float],
                         lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate CSA value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if CSA_ERROR_MIN < target_value < CSA_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {CSA_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if CSA_ERROR_MIN <= lower_limit < CSA_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if CSA_ERROR_MIN < upper_limit <= CSA_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if CSA_ERROR_MIN <= lower_linear_limit < CSA_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if CSA_ERROR_MIN < upper_linear_limit <= CSA_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {CSA_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if CSA_RANGE_MIN <= target_value <= CSA_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {CSA_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if CSA_RANGE_MIN <= lower_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if CSA_RANGE_MIN <= upper_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if CSA_RANGE_MIN <= lower_linear_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if CSA_RANGE_MIN <= upper_linear_limit <= CSA_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {CSA_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validatePreRange(self, weight: float, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float],
                         lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate PRE value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if PRE_ERROR_MIN < target_value < PRE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {PRE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if PRE_ERROR_MIN <= lower_limit < PRE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if PRE_ERROR_MIN < upper_limit <= PRE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if PRE_ERROR_MIN <= lower_linear_limit < PRE_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if PRE_ERROR_MIN < upper_linear_limit <= PRE_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {PRE_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if PRE_RANGE_MIN <= target_value <= PRE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {PRE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if PRE_RANGE_MIN <= lower_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if PRE_RANGE_MIN <= upper_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if PRE_RANGE_MIN <= lower_linear_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if PRE_RANGE_MIN <= upper_linear_limit <= PRE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {PRE_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validatePcsRange(self, weight: float, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float],
                         lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate PCS value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            if PCS_ERROR_MIN < target_value < PCS_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {PCS_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if PCS_ERROR_MIN <= lower_limit < PCS_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if PCS_ERROR_MIN < upper_limit <= PCS_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if PCS_ERROR_MIN <= lower_linear_limit < PCS_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if PCS_ERROR_MIN < upper_linear_limit <= PCS_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if PCS_RANGE_MIN <= target_value <= PCS_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {PCS_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if PCS_RANGE_MIN <= lower_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if PCS_RANGE_MIN <= upper_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if PCS_RANGE_MIN <= lower_linear_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if PCS_RANGE_MIN <= upper_linear_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def validateCcrRange(self, weight: float, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float],
                         lower_linear_limit: Optional[float] = None, upper_linear_limit: Optional[float] = None) -> Optional[dict]:
        """ Validate CCR value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'potential': self.potential}

        if target_value is not None:
            if CCR_ERROR_MIN < target_value < CCR_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' must be within range {CCR_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if CCR_ERROR_MIN <= lower_limit < CCR_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if CCR_ERROR_MIN < upper_limit <= CCR_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if lower_linear_limit is not None:
            if CCR_ERROR_MIN <= lower_linear_limit < CCR_ERROR_MAX:
                dstFunc['lower_linear_limit'] = f"{lower_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if upper_linear_limit is not None:
            if CCR_ERROR_MIN < upper_linear_limit <= CCR_ERROR_MAX:
                dstFunc['upper_linear_limit'] = f"{upper_linear_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' must be within range {CCR_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if lower_linear_limit is not None:
                if lower_linear_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

            if upper_linear_limit is not None:
                if upper_linear_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper linear limit value='{upper_linear_limit:.6f}' must be greater than the target value '{target_value}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_limit):
                if lower_linear_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_limit:.6f}'.")

            if None not in (lower_limit, upper_linear_limit):
                if lower_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_linear_limit, upper_linear_limit):
                if lower_linear_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the upper limit value '{upper_linear_limit:.6f}'.")

            if None not in (lower_limit, lower_linear_limit):
                if lower_linear_limit > lower_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower linear limit value='{lower_linear_limit:.6f}' must be less than the lower limit value '{lower_limit:.6f}'.")

            if None not in (upper_limit, upper_linear_limit):
                if upper_limit > upper_linear_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be less than the upper linear limit value '{upper_linear_limit:.6f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if CCR_RANGE_MIN <= target_value <= CCR_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value}' should be within range {CCR_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if CCR_RANGE_MIN <= lower_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if CCR_RANGE_MIN <= upper_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if lower_linear_limit is not None:
            if CCR_RANGE_MIN <= lower_linear_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower linear limit value='{lower_linear_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if upper_linear_limit is not None:
            if CCR_RANGE_MIN <= upper_linear_limit <= CCR_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper linear limit value='{upper_linear_limit:.6f}' should be within range {CCR_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None and lower_linear_limit is None and upper_linear_limit is None:
            return None

        return dstFunc

    def areUniqueCoordAtoms(self, subtype_name: str, skip_col: List[int] = None,
                            allow_ambig: bool = False, allow_ambig_warn_title: str = '') -> bool:
        """ Check whether atom selection sets are uniquely assigned.
        """

        for col, _atomSelectionSet in enumerate(self.atomSelectionSet):
            _lenAtomSelectionSet = len(_atomSelectionSet)

            if _lenAtomSelectionSet == 0:
                if skip_col is not None and col in skip_col:
                    continue
                return False  # raised error already

            if _lenAtomSelectionSet == 1:
                continue

            for (atom1, atom2) in itertools.combinations(_atomSelectionSet, 2):
                if atom1['chain_id'] != atom2['chain_id']:
                    continue
                if atom1['seq_id'] != atom2['seq_id']:
                    continue
                if allow_ambig:
                    self.f.append(f"[{allow_ambig_warn_title}] {self.getCurrentRestraint()}"
                                  f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                                  f"{atom2['atom_id']}' found in {subtype_name} restraint.")
                    continue
                self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                              f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "
                              f"{atom2['atom_id']}' is not allowed as {subtype_name} restraint.")
                return False

        return True

    def intersectionFactor_expressions(self, atomSelection: Optional[List[dict]] = None):
        self.consumeFactor_expressions(cifCheck=False)

        self.factor = self.doIntersectionFactor_expressions(self.factor, atomSelection)

    def doIntersectionFactor_expressions(self, _factor: dict, atomSelection: Optional[List[dict]] = None) -> dict:  # pylint: disable=no-self-use
        if 'atom_selection' not in _factor:
            _factor['atom_selection'] = atomSelection
            return _factor

        if atomSelection is None or len(atomSelection) == 0:
            _factor['atom_selection'] = []

        else:
            atom_sel0 = atomSelection[0]
            if isinstance(atom_sel0, str) and atom_sel0 == '*':
                return _factor

        factor_has_is_poly = factor_has_auth_atom_id = factor_has_segment_id =\
            atomsel_has_is_poly = atomsel_has_auth_atom_id = atomsel_has_segment_id = None
        if len(_factor['atom_selection']) > 0:
            _atom_sel0 = _factor['atom_selection'][0]
            factor_has_is_poly = 'is_poly' in _atom_sel0
            factor_has_auth_atom_id = 'auth_atom_id' in _atom_sel0
            factor_has_segment_id = 'segment_id' in _atom_sel0
        if atomSelection is not None and len(atomSelection) > 0:
            atomsel_has_is_poly = 'is_poly' in atom_sel0
            atomsel_has_auth_atom_id = 'auth_atom_id' in atom_sel0
            atomsel_has_segment_id = 'segment_id' in atom_sel0

        refAtomSelection = _factor['atom_selection']
        if factor_has_is_poly != atomsel_has_is_poly\
           or factor_has_auth_atom_id != atomsel_has_auth_atom_id\
           or factor_has_segment_id != atomsel_has_segment_id:
            refAtomSelection = deepcopy(_factor['atom_selection'])
            if factor_has_is_poly != atomsel_has_is_poly:
                if factor_has_is_poly:
                    for _atom in refAtomSelection:
                        try:
                            del _atom['is_poly']
                        except KeyError:
                            pass
                if atomsel_has_is_poly:
                    for _atom in atomSelection:
                        try:
                            del _atom['is_poly']
                        except KeyError:
                            pass
            if factor_has_auth_atom_id != atomsel_has_auth_atom_id:
                if factor_has_auth_atom_id:
                    for _atom in refAtomSelection:
                        try:
                            del _atom['auth_atom_id']
                        except KeyError:
                            pass
                if atomsel_has_auth_atom_id:
                    for _atom in atomSelection:
                        try:
                            del _atom['auth_atom_id']
                        except KeyError:
                            pass
            if factor_has_segment_id != atomsel_has_segment_id:
                if factor_has_segment_id:
                    segment_id = _atom_sel0['segment_id']
                    for _atom in atomSelection:
                        _atom['segment_id'] = segment_id
                if atomsel_has_segment_id:
                    segment_id = atom_sel0['segment_id']
                    for _atom in refAtomSelection:
                        _atom['segment_id'] = segment_id
                    _factor['atom_selection'] = refAtomSelection

        _atomSelection = []
        for _atom, _atom_ in zip(refAtomSelection, _factor['atom_selection']):
            if isinstance(_atom, str) and _atom == '*':
                _factor['atom_selection'] = atomSelection
                return _factor
            if _atom in atomSelection:
                _atomSelection.append(_atom_)
            elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                chain_id = _atom['chain_id']
                seq_id = _atom['seq_id']
                if any(True for _atom2 in atomSelection if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                    _atomSelection.append(_atom_)

        _factor['atom_selection'] = _atomSelection

        return _factor

    def intersectionAtom_selections(self, _selection1: List[dict], _selection2: List[dict]) -> List[dict]:  # pylint: disable=no-self-use
        if None in (_selection1, _selection2) or 0 in (len(_selection1), len(_selection2)):
            return []

        if isinstance(_selection2[0], str) and _selection2[0] == '*':
            return _selection1

        max_sample = 40
        len_selection1 = len(_selection1)
        len_selection2 = len(_selection2)

        if len_selection1 <= max_sample:
            slice1 = _selection1
        elif len_selection1 <= max_sample * 2:
            slice1 = _selection1[0:len_selection1:2]
        else:
            slice1 = [_selection1[0], _selection1[-1]]
            for _ in range(max_sample - 2):
                idx = random.randint(2, len_selection1 - 1)
                slice1.append(_selection1[idx])

        if len_selection2 <= max_sample:
            slice2 = _selection2
        elif len_selection2 <= max_sample * 2:
            slice2 = _selection2[0:len_selection2:2]
        else:
            slice2 = [_selection2[0], _selection2[-1]]
            for _ in range(max_sample - 2):
                idx = random.randint(2, len_selection2 - 1)
                slice2.append(_selection2[idx])

        hasAuthAtomId1 = any(True for _atom in slice1 if 'auth_atom_id' in _atom)
        hasAuthAtomId2 = any(True for _atom in slice2 if 'auth_atom_id' in _atom)
        hasSegmentId1 = any(True for _atom in slice1 if 'segment_id' in _atom)
        hasSegmentId2 = any(True for _atom in slice2 if 'segment_id' in _atom)

        _atomSelection = []

        if hasSegmentId1 != hasSegmentId2:
            if hasSegmentId1:
                segmentId = next(_atom['segment_id'] for _atom in _selection1 if 'segment_id' in _atom)
                for _atom in _selection2:
                    _atom['segment_id'] = segmentId
            else:
                segmentId = next(_atom['segment_id'] for _atom in _selection2 if 'segment_id' in _atom)
                for _atom in _selection1:
                    _atom['segment_id'] = segmentId

        if not hasAuthAtomId1 and not hasAuthAtomId2:
            for _atom in _selection1:
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in _selection2:
                    _atomSelection.append(_atom)
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(True for _atom2 in _selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_atom)

        elif hasAuthAtomId1 and not hasAuthAtomId2:
            __selection1 = deepcopy(_selection1)
            for _atom in __selection1:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection1):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in _selection2:
                    _atomSelection.append(_selection1[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(True for _atom2 in _selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_selection1[idx])

        elif not hasAuthAtomId1 and hasAuthAtomId2:
            __selection2 = deepcopy(_selection2)
            for idx, _atom in enumerate(__selection2):
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection2):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection1
                if _atom in _selection1:
                    _atomSelection.append(_selection2[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(True for _atom1 in _selection1 if _atom1['chain_id'] == chain_id and _atom1['seq_id'] == seq_id):
                        _atomSelection.append(_selection2[idx])

        else:
            __selection1 = deepcopy(_selection1)
            for _atom in __selection1:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            __selection2 = deepcopy(_selection2)
            for _atom in __selection2:
                if 'auth_atom_id' in _atom:
                    _atom.pop('auth_atom_id')
            for idx, _atom in enumerate(__selection1):
                if isinstance(_atom, str) and _atom == '*':
                    return _selection2
                if _atom in __selection2:
                    _atomSelection.append(_selection1[idx])
                elif 'hydrogen_not_instantiated' in _atom and _atom['hydrogen_not_instantiated']:
                    chain_id = _atom['chain_id']
                    seq_id = _atom['seq_id']
                    if any(True for _atom2 in __selection2 if _atom2['chain_id'] == chain_id and _atom2['seq_id'] == seq_id):
                        _atomSelection.append(_selection1[idx])

        return _atomSelection

    def consumeFactor_expressions(self, clauseName: str = 'atom selection expression', cifCheck: bool = True):
        """ Consume factor expressions as atom selection if possible.
        """

        if self.stackFactors:
            self.stackFactors.pop()

        self.factor = self.doConsumeFactor_expressions(self.factor, clauseName, cifCheck)

    def doConsumeFactor_expressions(self, _factor: dict, clauseName: str = 'atom selection expression', cifCheck: bool = True, trial: int = 1) -> dict:
        """ Consume factor expressions as atom selection if possible.
        """

        if not self.hasPolySeq and not self.hasNonPolySeq:
            return _factor

        if not self.hasCoord:
            cifCheck = False

        self.__lenAtomSelectionSet = len(self.atomSelectionSet)  # pylint: disable=attribute-defined-outside-init

        if self.file_type == 'nm-res-cha' and 'atom_num' in _factor and 'atom_id' not in _factor:
            g = None
            if self.lastComment is not None:
                if self.cur_subtype == 'dist':
                    if self.__dist_comment_pat.match(self.lastComment):
                        g = self.__dist_comment_pat.search(self.lastComment).groups()
                        offset = self.__lenAtomSelectionSet * 3
                        # _factor['comp_id'] = [g[offset]]
                        _factor['seq_id'] = [int(g[offset + 1])]
                        _factor['atom_id'] = [g[offset + 2]]
                        _seqId = _factor['seq_id'][0]
                        _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq if _seqId in ps['seq_id']]
                        if self.hasNonPolySeq:
                            for np in self.nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId not in _factor['chain_id'] and _seqId in np['seq_id']:
                                    _factor['chain_id'].append(_chainId)
                        if len(_factor['chain_id']) == 0:
                            del _factor['chain_id']
                    elif self.__dist_comment_pat2.match(self.lastComment):
                        g = self.__dist_comment_pat2.search(self.lastComment).groups()
                        offset = self.__lenAtomSelectionSet * 4
                        _factor['chain_id'] = [g[offset]]
                        # _factor['comp_id'] = [g[offset + 1]]
                        _factor['seq_id'] = [int(g[offset + 2])]
                        _factor['atom_id'] = [g[offset + 3]]
                elif self.cur_subtype == 'dihed':
                    if self.__dihed_comment_pat.match(self.lastComment):
                        g = self.__dihed_comment_pat.search(self.lastComment).groups()
                        offset = self.__lenAtomSelectionSet * 3
                        # _factor['comp_id'] = [g[offset]]
                        _factor['seq_id'] = [int(g[offset + 1])]
                        _factor['atom_id'] = [g[offset + 2]]
                        _seqId = _factor['seq_id'][0]
                        _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq if _seqId in ps['seq_id']]
                        if self.hasNonPolySeq:
                            for np in self.nonPolySeq:
                                _chainId = np['auth_chain_id']
                                if _chainId not in _factor['chain_id'] and _seqId in np['seq_id']:
                                    _factor['chain_id'].append(_chainId)
                        if len(_factor['chain_id']) == 0:
                            del _factor['chain_id']
            if g is None:
                _factor['atom_id'] = [None]
                if 'chain_id' in _factor:
                    del _factor['chain_id']
                if 'seq_id' in _factor:
                    del _factor['seq_id']

                self.f.append(f"[Unsupported data] {self.getCurrentRestraint()}"
                              "The 'bynumber' clause has no effect "
                              "because CHARMM CRD file is not provided.")

                return _factor

        if ('atom_id' in _factor and len(_factor['atom_id']) > 0 and _factor['atom_id'][0] is None)\
           or ('atom_selection' in _factor and (_factor['atom_selection'] is None or len(_factor['atom_selection']) == 0)):
            return {'atom_selection': []}

        if not any(True for key in _factor if not (key == 'atom_selection' or key.startswith('auth'))):
            return _factor

        if 'alt_chain_id' in _factor:
            len_factor = len(_factor)

            if len_factor == 2 and 'chain_id' in _factor and len(_factor['chain_id']) == 0:
                if self.__largeModel:
                    _factor['chain_id'] = [self.__representativeAsymId]
                else:
                    _factor['atom_selection'] = ['*']
                    del _factor['chain_id']
                    return _factor

            elif len_factor == 1:
                _factor['atom_selection'] = ['*']
                return _factor

            self.__failure_chain_ids.clear()

        self.with_para = self.cur_subtype in ('pcs', 'pre', 'prdc', 'pccr')

        if self.__lenAtomSelectionSet == 0:

            if 'atom_id' in _factor and len(_factor['atom_id']) > 0:
                _atomId0 = _factor['atom_id'][0].upper()

                if self.cur_subtype == 'pcs' and not self.in_block and _atomId0 in ('C', "C'", 'CO'):
                    self.cur_subtype = 'hvycs'
                    self.with_para = False

                # for the case dist -> pre transition occurs
                if _atomId0 not in ('CA', 'CE')\
                   and (_atomId0 in PARAMAGNETIC_ELEMENTS or _atomId0 == 'OO'):
                    if self.cur_subtype == 'dist':
                        self.with_para = True
                    if self.with_para:
                        self.paramagCenter = copy.copy(_factor)

        self.retrieveLocalSeqScheme()

        if 'atom_id' in _factor and len(_factor['atom_id']) == 1:
            self.__cur_auth_atom_id = _factor['atom_id'][0]
        elif 'atom_ids' in _factor and len(_factor['atom_ids']) == 1:
            self.__cur_auth_atom_id = _factor['atom_ids'][0]
        else:
            self.__cur_auth_atom_id = ''

        ambigAtomSelect = False
        if 'atom_id' not in _factor and 'atom_ids' not in _factor\
           and 'type_symbol' not in _factor and 'type_symbols' not in _factor:
            _factor['atom_not_specified'] = True
            if 'atom_selection' not in _factor:
                ambigAtomSelect = True

        elif 'chain_id' not in _factor and 'seq_id' not in _factor and 'seq_ids' not in _factor:
            if 'atom_selection' not in _factor:
                ambigAtomSelect = True

        if 'seq_id' not in _factor and 'seq_ids' not in _factor:
            _factor['seq_not_specified'] = True

        key = str(_factor)
        if key in self.__cachedDictForFactor:
            _factor_ = self.__cachedDictForFactor[key]
            if 'has_nitroxide' in _factor_:
                self.has_nx = True
            elif 'has_gd3+' in _factor_:
                self.has_gd = True
            elif 'has_lanthanide' in _factor_:
                self.has_la = True
            return deepcopy(_factor_)

        unambig = self.cur_subtype != 'dist'

        len_warn_msg = len(self.f)

        chain_not_specified = np_chain_not_specified = 'alt_chain_id' not in _factor
        if 'chain_id' not in _factor or len(_factor['chain_id']) == 0:
            if self.__largeModel:
                _factor['chain_id'] = [self.__representativeAsymId]
            else:
                _factor['chain_id'] = [ps['auth_chain_id'] for ps in self.polySeq]
                if self.hasNonPolySeq:
                    for np in self.nonPolySeq:
                        _chainId = np['auth_chain_id']
                        if _chainId not in _factor['chain_id']:
                            _factor['chain_id'].append(_chainId)
                if len(_factor['chain_id']) == 1:
                    chain_not_specified = False
        elif len(_factor['chain_id']) == 1:
            _chainId = _factor['chain_id'][0]
            if chain_not_specified and any(True for ps in self.polySeq if ps['auth_chain_id'] == _chainId):
                _factor['auth_chain_id'] = _factor['chain_id']
                chain_not_specified = False
            if self.hasNonPolySeq and np_chain_not_specified:
                if any(True for np in self.nonPolySeq if np['auth_chain_id'] == _chainId):
                    _factor['auth_chain_id'] = _factor['chain_id']
                    np_chain_not_specified = False
                elif not chain_not_specified and any(True for np in self.nonPolySeq if np['chain_id'] == _chainId):
                    _factor['auth_chain_id'] = _factor['chain_id']
                    np_chain_not_specified = False

        if self.__complexSeqScheme and self.reasons is not None and 'inhibit_label_seq_scheme_stats' in self.reasons\
           and not chain_not_specified and _factor['chain_id'][0] in self.reasons['inhibit_label_seq_scheme_stats']:
            self.preferAuthSeq = True

        if 'seq_id' not in _factor and 'seq_ids' not in _factor:
            if 'comp_ids' in _factor and len(_factor['comp_ids']) > 0\
               and ('comp_id' not in _factor or len(_factor['comp_id']) == 0):
                lenCompIds = len(_factor['comp_ids'])
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                    for ps in psList:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = self.getRealCompId(ps['comp_id'][idx])
                            origCompId = ps['auth_comp_id'][idx]
                            if lenCompIds == 1:
                                compIds_ex = toRegEx(translateToStdResName(_factor['comp_ids'][0], realCompId, self.ccU))
                                if re.match(compIds_ex, realCompId) or re.match(compIds_ex, origCompId):
                                    _compIdSelect.add(realCompId)
                            elif lenCompIds == 2:
                                compIds0 = translateToStdResName(_factor['comp_ids'][0], realCompId, self.ccU)
                                compIds1 = translateToStdResName(_factor['comp_ids'][1], realCompId, self.ccU)
                                if compIds0 <= realCompId <= compIds1 or compIds0 <= origCompId <= compIds1:
                                    _compIdSelect.add(realCompId)
                _factor['comp_id'] = list(_compIdSelect)
                del _factor['comp_ids']

        if 'seq_ids' in _factor and len(_factor['seq_ids']) > 0\
           and ('seq_id' not in _factor or len(_factor['seq_id']) == 0):
            seqId = _factor['seq_ids'][0]
            seqId_ex = toRegEx(seqId)
            seqIds = []
            for chainId in _factor['chain_id']:
                psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                for ps in psList:
                    found = False
                    for realSeqId in ps['auth_seq_id']:
                        if realSeqId is None:
                            continue
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = self.getRealCompId(ps['comp_id'][idx])
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                            if set(_factor['comp_id']) != set(_compIdList):
                                _factor['alt_comp_id'] = _factor['comp_id']
                                _factor['comp_id'] = _compIdList
                        if re.match(seqId_ex, str(realSeqId)):
                            seqIds.append(realSeqId)
                            found = True
                    if not found:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                idx = ps['auth_seq_id'].index(realSeqId)
                                realCompId = self.getRealCompId(ps['comp_id'][idx])
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                                if set(_factor['comp_id']) != set(_compIdList):
                                    _factor['alt_comp_id'] = _factor['comp_id']
                                    _factor['comp_id'] = _compIdList
                            seqKey = (chainId, realSeqId)
                            if seqKey in self.authToLabelSeq:
                                _, realSeqId = self.authToLabelSeq[seqKey]
                                if re.match(seqId_ex, str(realSeqId)):
                                    seqIds.append(realSeqId)
            _factor['seq_id'] = list(set(seqIds))
            del _factor['seq_ids']

        if 'seq_id' not in _factor or len(_factor['seq_id']) == 0:
            seqIds = []
            for chainId in _factor['chain_id']:
                psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                for ps in psList:
                    for realSeqId in ps['auth_seq_id']:
                        if realSeqId is None:
                            continue
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = self.getRealCompId(ps['comp_id'][idx])
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                            if set(_factor['comp_id']) != set(_compIdList):
                                _factor['alt_comp_id'] = _factor['comp_id']
                                _factor['comp_id'] = _compIdList
                        seqIds.append(realSeqId)
            _factor['seq_id'] = list(set(seqIds))

            if len(_factor['seq_id']) > 0 and 'comp_id' in _factor and 'seq_not_specified' in _factor:  # 2lr1
                del _factor['seq_not_specified']  # 2krf

        if 'atom_id' not in _factor and 'atom_ids' not in _factor:
            if 'type_symbols' in _factor and len(_factor['type_symbols']) > 0\
               and ('type_symbol' not in _factor or len(_factor['type_symbol']) == 0):
                lenTypeSymbols = len(_factor['type_symbols'])
                _typeSymbolSelect = set()
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                    for ps in psList:
                        _compIdSelect |= set(ps['comp_id'])
                typeSymBols_ex = toRegEx(_factor['type_symbols'][0]) if lenTypeSymbols == 1 else None
                for compId in _compIdSelect:
                    if self.ccU.updateChemCompDict(compId):
                        for cca in self.ccU.lastAtomList:
                            realTypeSymbol = cca[self.ccU.ccaTypeSymbol]
                            if (lenTypeSymbols == 1 and re.match(typeSymBols_ex, realTypeSymbol))\
                               or (lenTypeSymbols == 2 and _factor['type_symbols'][0] <= realTypeSymbol <= _factor['type_symbols'][1]):
                                _typeSymbolSelect.add(realTypeSymbol)
                _factor['type_symbol'] = list(_typeSymbolSelect)
                if len(_factor['type_symbol']) == 0:
                    _factor['atom_id'] = [None]
                del _factor['type_symbols']

            if 'type_symbol' in _factor:
                _atomIdSelect = set()
                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                    for ps in psList:
                        _compIdSelect |= set(ps['comp_id'])
                for compId in _compIdSelect:
                    if self.ccU.updateChemCompDict(compId):
                        for cca in self.ccU.lastAtomList:
                            if cca[self.ccU.ccaTypeSymbol] in _factor['type_symbol']\
                               and cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                _atomIdSelect.add(cca[self.ccU.ccaAtomId])

                _factor['atom_id'] = list(_atomIdSelect)
                if len(_factor['atom_id']) == 0:
                    _factor['atom_id'] = [None]

        def get_real_seq_id(ps, real_seq_id):
            chain_id = ps['auth_chain_id']
            _seq_ids = _factor['seq_id']
            _seq_id = _seq_ids[0]

            if not self.preferAuthSeq:
                if 'label_seq_offset' in self.reasons\
                   and chain_id in self.reasons['label_seq_offset']:
                    offset = self.reasons['label_seq_offset'][chain_id]
                    if _seq_id + offset in ps['seq_id']:
                        return ps['auth_seq_id'][ps['seq_id'].index(_seq_id + offset)]
                elif _seq_id in ps['seq_id']:
                    return ps['auth_seq_id'][ps['seq_id'].index(_seq_id)]
                if 'chain_id_remap' in self.reasons\
                        and _seq_id in self.reasons['chain_id_remap']\
                        and chain_id == self.reasons['chain_id_remap'][_seq_id]['chain_id']:
                    return real_seq_id
                if 'seq_id_remap' in self.reasons:
                    _, _real_seq_id = retrieveRemappedSeqId(self.reasons['seq_id_remap'], chain_id, _seq_id)
                    if _real_seq_id == real_seq_id:
                        return real_seq_id
                return None

            if 'global_auth_sequence_offset' in self.reasons\
               and chain_id in self.reasons['global_auth_sequence_offset']:
                offset = self.reasons['global_auth_sequence_offset'][chain_id]
                if real_seq_id in [seq_id + offset for seq_id in _seq_ids]:
                    return real_seq_id
                if isinstance(offset, dict):
                    if real_seq_id in offset:
                        offset = offset[real_seq_id]
                    else:
                        for shift in range(1, 100):
                            if real_seq_id + shift in offset:
                                offset = offset[real_seq_id + shift]
                                break
                            if real_seq_id - shift in offset:
                                offset = offset[real_seq_id - shift]
                                break
                        if isinstance(offset, dict):
                            return None
                if real_seq_id + offset in ps['auth_seq_id']:
                    return real_seq_id + offset
                if offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                    for shift in range(1, 100):
                        if real_seq_id + shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(real_seq_id + shift + offset) - shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx]
                        if real_seq_id - shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(real_seq_id - shift + offset) + shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx]

            elif 'global_sequence_offset' in self.reasons\
                    and chain_id in self.reasons['global_sequence_offset']:
                offset = self.reasons['global_sequence_offset'][chain_id]
                if real_seq_id in [seq_id + offset for seq_id in _seq_ids]:
                    return real_seq_id

            elif 'chain_id_remap' in self.reasons\
                    and _seq_id in self.reasons['chain_id_remap']\
                    and chain_id == self.reasons['chain_id_remap'][_seq_id]['chain_id']:
                return real_seq_id

            elif 'seq_id_remap' in self.reasons:
                _, _real_seq_id = retrieveRemappedSeqId(self.reasons['seq_id_remap'], chain_id, _seq_id)
                if _real_seq_id == real_seq_id:
                    return real_seq_id

            return None

        def is_real_nucleic_atom_id(real_atom_id, test_atom_id, src_atom_id, candidates):
            if ("'" in test_atom_id and "'" in real_atom_id)\
               or ("'" not in test_atom_id and "'" not in real_atom_id):
                pass

            else:
                if len(test_atom_id) > 1 and test_atom_id[1] != src_atom_id[1]:
                    if "'" in real_atom_id:
                        return False

                else:
                    min_len = min(len(src_atom_id), 2)
                    if real_atom_id.startswith(src_atom_id[:min_len]):
                        if ("'" in src_atom_id and "'" in real_atom_id)\
                           or ("'" not in src_atom_id and "'" not in real_atom_id):
                            pass
                        elif len(candidates) == 1 or (all("'" in a for a in candidates) or all("'" not in a for a in candidates)):
                            pass  # 2lzv
                        else:
                            return False

            if len([_atom_id_ for _atom_id_ in candidates
                    if ("'" in _atom_id_ and "'" in real_atom_id)
                    or ("'" not in _atom_id_ and "'" not in real_atom_id)]) < 2:
                return len(candidates) == 1 or (all("'" in a for a in candidates) or all("'" not in a for a in candidates))  # 2lzv

            return True

        if 'atom_ids' in _factor and len(_factor['atom_ids']) > 0\
           and ('atom_id' not in _factor or len(_factor['atom_id']) == 0):
            lenAtomIds = len(_factor['atom_ids'])
            _compIdSelect = set()
            for chainId in _factor['chain_id']:
                psList = [ps for ps in self.fullPolySeq if ps['auth_chain_id'] == chainId]
                for ps in psList:
                    for realSeqId in ps['auth_seq_id']:
                        if realSeqId is None:
                            continue
                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                            if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                if self.reasons is None:
                                    continue
                                realSeqId = get_real_seq_id(ps, realSeqId)
                                if realSeqId is None:
                                    continue
                        idx = ps['auth_seq_id'].index(realSeqId)
                        realCompId = self.getRealCompId(ps['comp_id'][idx])
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                            if set(_factor['comp_id']) != set(_compIdList):
                                _factor['alt_comp_id'] = _factor['comp_id']
                                _factor['comp_id'] = _compIdList
                        _compIdSelect.add(realCompId)

            if len(_compIdSelect) == 0 and self.reasons is None:
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if realCompId in ('ACE', 'NH2'):
                                continue
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                                if set(_factor['comp_id']) != set(_compIdList):
                                    _factor['alt_comp_id'] = _factor['comp_id']
                                    _factor['comp_id'] = _compIdList
                            _compIdSelect.add(realCompId)

                        wcPtnrChainIds = getWatsonCrickPtnr(self.cR, chainId)
                        if wcPtnrChainIds is not None:
                            for wcChainId in wcPtnrChainIds:
                                if wcChainId in _factor['chain_id']:
                                    continue
                                wc = next((wc for wc in self.polySeq if wc['auth_chain_id'] == wcChainId), None)
                                if wc is not None:
                                    for realSeqId in wc['auth_seq_id']:
                                        if realSeqId is None:
                                            continue
                                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                            if self.getOrigSeqId(wc, realSeqId) not in _factor['seq_id']:
                                                if self.reasons is None:
                                                    continue
                                                realSeqId = get_real_seq_id(wc, realSeqId)
                                                if realSeqId is None:
                                                    continue
                                        idx = wc['auth_seq_id'].index(realSeqId)
                                        realCompId = wc['comp_id'][idx]
                                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                            origCompId = wc['auth_comp_id'][idx]
                                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                                continue
                                            if set(_factor['comp_id']) != set(_compIdList):
                                                _factor['alt_comp_id'] = _factor['comp_id']
                                                _factor['comp_id'] = _compIdList
                                        _compIdSelect.add(realCompId)
                                        _factor['chain_id'].append(wcChainId)
                                        if chainId in _factor['chain_id']:
                                            _factor['chain_id'].remove(chainId)

            _atomIdSelect = set()
            for compId in _compIdSelect:
                if self.ccU.updateChemCompDict(compId):
                    nucleotide = self.csStat.getTypeOfCompId(compId)[1]
                    refAtomIdList = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                    tmpAtomId = _factor['atom_ids'][0].upper()
                    if lenAtomIds == 1:
                        atomId = _atomId = translateToStdAtomName(tmpAtomId, compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                        if atomId[-1] in ('%', '*', '#'):
                            if atomId[0] == 'H' and len(atomId) > 2:
                                if atomId[1] != 'M':
                                    _atomId = 'Q' + atomId[1:-1]
                                else:
                                    _atomId = atomId[1:-1]
                            elif atomId[0] in ('Q', 'M'):
                                _atomId = atomId[:-1]
                            elif atomId[:-1] in XPLOR_NITROXIDE_NAMES:
                                _atomIdSelect.add(atomId[:-1])
                                _factor['alt_atom_id'] = atomId
                        atomIds, _, details = self.nefT.get_valid_star_atom(compId, _atomId, leave_unmatched=True)
                        if details is not None:
                            atomIds, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId, leave_unmatched=True)
                        if details is not None and atomId[-1] in ('%', '*', '#'):
                            _atomIds, _, _details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
                            if _details is None and len(_atomIds) > 0:  # 5z4f: GLU:HG1# -> GLU:HG3
                                if nucleotide and atomId[0] in protonBeginCode and len(atomId) > 1 and len(_atomIds[0]) > 1\
                                   and atomId[1].isdigit() and _atomIds[0][1].isdigit() and atomId[1] != _atomIds[0][0]:
                                    pass  # 2lzv
                                else:
                                    atomId = _atomIds[0]
                                    atomIds, details = _atomIds, _details
                        atomId_ex = toNefEx(toRegEx(atomId))
                        if atomId_ex.endswith('.') and details is None:
                            atomId_ex += '$'  # HT# -> H. should match with H1/2/3 and not with HA2/3 (5iew)
                        elif atomId_ex.endswith('.*') and details is not None:  # remove excess wild card code e.g. LYS:HB1* -> LYS:HB3 (5kqj)
                            _atomIds, _, _details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId_ex[:-2], leave_unmatched=True)
                            if len(_atomIds) > 0 and _details is None:
                                atomId_ex = _atomIds[0]
                                atomIds, details = _atomIds, _details
                        tmpAtomId_ex = toNefEx(toRegEx(tmpAtomId))
                    elif lenAtomIds == 2:
                        atomId1 = translateToStdAtomName(tmpAtomId, compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                        atomId2 = translateToStdAtomName(_factor['atom_ids'][1], compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                    _atomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                    if lenAtomIds == 1 and nucleotide:
                        _matchedAtomIds = [_atomId_ for _atomId_ in _atomIds if re.match(atomId_ex, _atomId_)]
                    matched = False
                    for realAtomId in _atomIds:
                        if lenAtomIds == 1:
                            if re.match(atomId_ex, realAtomId):
                                if nucleotide and not is_real_nucleic_atom_id(realAtomId, atomId, tmpAtomId, _matchedAtomIds):
                                    continue
                                _atomIdSelect.add(realAtomId)
                                _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                matched = True
                            elif details is None:
                                if len(atomIds) == 1 and not re.match(tmpAtomId_ex, atomIds[0]):  # len(atomIds) == 1 to allow map HR# to H[DE][12]
                                    continue
                                _atomIdSelect |= set(atomIds)
                                _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                matched = True
                        elif lenAtomIds == 2:
                            if (atomId1 < atomId2 and atomId1 <= realAtomId <= atomId2)\
                               or (atomId1 > atomId2 and atomId2 <= realAtomId <= atomId1):
                                _atomIdSelect.add(realAtomId)
                    if lenAtomIds == 1 and not matched:
                        for chainId in _factor['chain_id']:
                            ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                            if ps is not None:
                                for realSeqId, realCompId in zip(ps['auth_seq_id'], ps['comp_id']):
                                    if realSeqId is None or realCompId != compId:
                                        continue
                                    if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                        if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                            if self.reasons is None:
                                                continue
                                            realSeqId = get_real_seq_id(ps, realSeqId)
                                            if realSeqId is None:
                                                continue
                                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, realSeqId, cifCheck=cifCheck)
                                        if coordAtomSite is not None:
                                            for realAtomId in coordAtomSite['atom_id']:
                                                if re.match(atomId_ex, realAtomId) or re.match(tmpAtomId_ex, realAtomId):
                                                    if nucleotide and not is_real_nucleic_atom_id(realAtomId, atomId, tmpAtomId, _matchedAtomIds):
                                                        continue
                                                    _atomIdSelect.add(realAtomId)
                                                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
                            if self.hasNonPolySeq:
                                np = next((np for np in self.nonPolySeq if np['auth_chain_id'] == chainId), None)
                                if np is not None:
                                    for realSeqId, realCompId in zip(np['auth_seq_id'], np['comp_id']):
                                        if realSeqId is None or realCompId != compId:
                                            continue
                                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                            ptnr = None
                                            if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                                ptnr = getStructConnPtnr(self.cR, chainId, realSeqId, realCompId)
                                                if ptnr is None:
                                                    continue
                                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, realSeqId, cifCheck=cifCheck)
                                            if coordAtomSite is not None:
                                                for realAtomId in coordAtomSite['atom_id']:
                                                    if re.match(atomId_ex, realAtomId) or re.match(tmpAtomId_ex, realAtomId):
                                                        if nucleotide and not is_real_nucleic_atom_id(realAtomId, atomId, tmpAtomId, _matchedAtomIds):
                                                            continue
                                                        _atomIdSelect.add(realAtomId)
                                                        _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                                        if ptnr is not None:
                                                            _factor['seq_id'] = [realSeqId]

            _factor['atom_id'] = list(_atomIdSelect)

            if len(_compIdSelect) > 0 and len(_atomIdSelect) == 0 and self.mrAtomNameMapping is not None:
                tmpAtomId = 'Q' + _factor['atom_ids'][0][1:-1].upper()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                    if self.reasons is None:
                                        continue
                                    realSeqId = get_real_seq_id(ps, realSeqId)
                                    if realSeqId is None:
                                        continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if realCompId not in monDict3 and realCompId in _compIdSelect:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, realSeqId, cifCheck=cifCheck)
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.mrAtomNameMapping, realSeqId, realCompId, tmpAtomId, coordAtomSite, ignoreSeqId=True)
                                atomIds, _, details = self.nefT.get_valid_star_atom(realCompId, atomId, leave_unmatched=True)
                                if details is None:
                                    _atomIdSelect |= set(atomIds)
                                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
                    if self.hasNonPolySeq:
                        np = next((np for np in self.nonPolySeq if np['auth_chain_id'] == chainId), None)
                        if np is not None:
                            for realSeqId, realCompId in zip(np['auth_seq_id'], np['comp_id']):
                                if realSeqId is None:
                                    continue
                                if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                    ptnr = None
                                    if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                        ptnr = getStructConnPtnr(self.cR, chainId, realSeqId, realCompId)
                                        if ptnr is None:
                                            continue
                                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, realSeqId, cifCheck=cifCheck)
                                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.mrAtomNameMapping, realSeqId, realCompId, tmpAtomId, coordAtomSite, ignoreSeqId=True)
                                    atomIds, _, details = self.nefT.get_valid_star_atom(realCompId, atomId, leave_unmatched=True)
                                    if details is None:
                                        _atomIdSelect |= set(atomIds)
                                        _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                        if ptnr is not None:
                                            _factor['seq_id'] = [realSeqId]

                _factor['atom_id'] = list(_atomIdSelect)

            if len(_factor['atom_id']) == 0:
                if self.reasons is None:
                    self.preferAuthSeq = not self.preferAuthSeq

                _compIdSelect = set()
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                _seqId = self.getOrigSeqId(ps, realSeqId)
                                if self.reasons is None and not self.preferAuthSeq:
                                    _seqKey = (chainId, _seqId)
                                    if _seqKey in self.authToLabelSeq:
                                        _seqId = self.authToLabelSeq[_seqKey][1]
                                if _seqId not in _factor['seq_id']:
                                    if self.reasons is None:
                                        continue
                                    realSeqId = get_real_seq_id(ps, realSeqId)
                                    if realSeqId is None:
                                        continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                                if set(_factor['comp_id']) != set(_compIdList):
                                    _factor['alt_comp_id'] = _factor['comp_id']
                                    _factor['comp_id'] = _compIdList
                            _compIdSelect.add(realCompId)
                if self.hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            for realSeqId in np['auth_seq_id']:
                                if realSeqId is None:
                                    continue
                                if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                    _seqId = self.getOrigSeqId(np, realSeqId, False)
                                    if not self.preferAuthSeq and not np_chain_not_specified:
                                        if self.reasons is None:
                                            _seqKey = (chainId, _seqId)
                                            if _seqKey in self.authToLabelSeq:
                                                _seqId = self.authToLabelSeq[_seqKey][1]
                                        elif 'alt_auth_seq_id' in np and np['alt_auth_seq_id'][np['auth_seq_id'].index(_seqId)] in _factor['seq_id']:
                                            _seqId = np['alt_auth_seq_id'][np['auth_seq_id'].index(_seqId)]
                                    if _seqId not in _factor['seq_id']:
                                        if self.reasons is not None and (self.preferAuthSeq or _seqId != realSeqId) and realSeqId in np['auth_seq_id']:
                                            pass
                                        else:
                                            ptnr = getStructConnPtnr(self.cR, chainId, realSeqId)
                                            if ptnr is None:
                                                continue
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = self.getRealCompId(np['comp_id'][idx])
                                if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                    origCompId = np['auth_comp_id'][idx]
                                    _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                    if realCompId not in _compIdList and origCompId not in _compIdList:
                                        continue
                                    if set(_factor['comp_id']) != set(_compIdList):
                                        _factor['alt_comp_id'] = _factor['comp_id']
                                        _factor['comp_id'] = _compIdList
                                _compIdSelect.add(realCompId)

                _atomIdSelect = set()
                for compId in _compIdSelect:
                    if self.ccU.updateChemCompDict(compId):
                        nucleotide = self.csStat.getTypeOfCompId(compId)[1]
                        refAtomIdList = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                        tmpAtomId = _factor['atom_ids'][0].upper()
                        if lenAtomIds == 1:
                            atomId = _atomId = translateToStdAtomName(tmpAtomId, compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                            if atomId[-1] in ('%', '*', '#'):
                                if atomId[0] == 'H' and len(atomId) > 2:
                                    if atomId[1] != 'M':
                                        _atomId = 'Q' + atomId[1:-1]
                                    else:
                                        _atomId = atomId[1:-1]
                                elif atomId[0] in ('Q', 'M'):
                                    _atomId = atomId[:-1]
                                elif atomId[:-1] in XPLOR_NITROXIDE_NAMES:
                                    _atomIdSelect.add(atomId[:-1])
                                    _factor['alt_atom_id'] = atomId
                            atomIds, _, details = self.nefT.get_valid_star_atom(compId, _atomId, leave_unmatched=True)
                            if details is not None:
                                atomIds, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId, leave_unmatched=True)
                            atomId_ex = toNefEx(toRegEx(atomId))
                            tmpAtomId_ex = toNefEx(toRegEx(tmpAtomId))
                        elif lenAtomIds == 2:
                            atomId1 = translateToStdAtomName(tmpAtomId, compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                            atomId2 = translateToStdAtomName(_factor['atom_ids'][1], compId, refAtomIdList, ccU=self.ccU, unambig=unambig)
                        _atomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                        if lenAtomIds == 1 and nucleotide:
                            _matchedAtomIds = [_atomId_ for _atomId_ in _atomIds if re.match(atomId_ex, _atomId_)]
                        for realAtomId in _atomIds:
                            if lenAtomIds == 1:
                                if re.match(atomId_ex, realAtomId):
                                    if nucleotide and not is_real_nucleic_atom_id(realAtomId, atomId, tmpAtomId, _matchedAtomIds):
                                        continue
                                    _atomIdSelect.add(realAtomId)
                                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
                                elif details is None:
                                    if len(atomIds) == 1 and not re.match(tmpAtomId_ex, atomIds[0]):
                                        continue
                                    _atomIdSelect |= set(atomIds)
                                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
                            elif lenAtomIds == 2:
                                if (atomId1 < atomId2 and atomId1 <= realAtomId <= atomId2)\
                                   or (atomId1 > atomId2 and atomId2 <= realAtomId <= atomId1):
                                    _atomIdSelect.add(realAtomId)

                _factor['atom_id'] = list(_atomIdSelect)

                if self.reasons is None:
                    self.preferAuthSeq = not self.preferAuthSeq

                if len(_atomIdSelect) > 0:
                    if self.__lenAtomSelectionSet > 0:
                        self.setLocalSeqScheme()
                else:
                    if not self.__internal or all(compId in monDict3 for compId in _compIdSelect):
                        _factor['atom_id'] = [None]
                    _factor['alt_atom_id'] = _factor['atom_ids'][0]
            # del _factor['atom_ids']

        if 'atom_id' not in _factor or len(_factor['atom_id']) == 0:
            _compIdSelect = set()
            _repNstdResidueInstance = {}
            _nonPolyCompIdSelect = []
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    for realSeqId in ps['auth_seq_id']:
                        if realSeqId is None:
                            continue
                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                            if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                if self.reasons is None:
                                    continue
                                realSeqId = get_real_seq_id(ps, realSeqId)
                                if realSeqId is None:
                                    continue
                        idx = ps['auth_seq_id'].index(realSeqId)
                        realCompId = ps['comp_id'][idx]
                        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                            origCompId = ps['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                            if set(_factor['comp_id']) != set(_compIdList):
                                _factor['alt_comp_id'] = _factor['comp_id']
                                _factor['comp_id'] = _compIdList
                        _compIdSelect.add(realCompId)
                        if realCompId not in monDict3:
                            _repNstdResidueInstance[realCompId] = (chainId, realSeqId)
            if self.hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        for realSeqId in np['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                seqId = _factor['seq_id'][0]
                                if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                    if seqId not in np['seq_id']:
                                        continue
                                    realSeqId = np['auth_seq_id'][np['seq_id'].index(seqId)]
                            idx = np['auth_seq_id'].index(realSeqId)
                            realCompId = self.getRealCompId(np['comp_id'][idx])
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = np['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                                if set(_factor['comp_id']) != set(_compIdList):
                                    _factor['alt_comp_id'] = _factor['comp_id']
                                    _factor['comp_id'] = _compIdList
                            _nonPolyCompIdSelect.append({'chain_id': chainId,
                                                         'seq_id': realSeqId,
                                                         'comp_id': realCompId})

            _atomIdSelect = set()
            for compId in _compIdSelect:
                if self.ccU.updateChemCompDict(compId):
                    for cca in self.ccU.lastAtomList:
                        if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                            realAtomId = cca[self.ccU.ccaAtomId]
                            _atomIdSelect.add(realAtomId)
                    if compId in _repNstdResidueInstance:
                        chainId, seqId = _repNstdResidueInstance[compId]
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)
                        if coordAtomSite is not None:
                            _atomIdSelect |= set(coordAtomSite['atom_id'])  # D_1300057999

            for nonPolyCompId in _nonPolyCompIdSelect:
                _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], nonPolyCompId['seq_id'], cifCheck=cifCheck)
                if coordAtomSite is not None:
                    if coordAtomSite['comp_id'] == nonPolyCompId['comp_id']:
                        for realAtomId in coordAtomSite['atom_id']:
                            _atomIdSelect.add(realAtomId)
                    else:
                        compId = nonPolyCompId['comp_id']
                        if self.ccU.updateChemCompDict(compId):
                            for cca in self.ccU.lastAtomList:
                                if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                    realAtomId = cca[self.ccU.ccaAtomId]
                                    _atomIdSelect.add(realAtomId)
                else:
                    for np in self.nonPolySeq:
                        if nonPolyCompId['seq_id'] == np['auth_seq_id'][0]:
                            _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], np['seq_id'][0], cifCheck=cifCheck)
                            if coordAtomSite is not None:
                                if coordAtomSite['comp_id'] == nonPolyCompId['comp_id']:
                                    for realAtomId in coordAtomSite['atom_id']:
                                        _atomIdSelect.add(realAtomId)
                                else:
                                    compId = nonPolyCompId['comp_id']
                                    if self.ccU.updateChemCompDict(compId):
                                        for cca in self.ccU.lastAtomList:
                                            if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                                realAtomId = cca[self.ccU.ccaAtomId]
                                                _atomIdSelect.add(realAtomId)

            _factor['atom_id'] = list(_atomIdSelect)

            if len(_factor['atom_id']) == 0:
                if self.reasons is None:
                    self.preferAuthSeq = not self.preferAuthSeq

                _compIdSelect = set()
                _repNstdResidueInstance = {}
                _nonPolyCompIdSelect = []
                for chainId in _factor['chain_id']:
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        for realSeqId in ps['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                _seqId = self.getOrigSeqId(ps, realSeqId)
                                if self.reasons is None and not self.preferAuthSeq:
                                    _seqKey = (chainId, _seqId)
                                    if _seqKey in self.authToLabelSeq:
                                        _seqId = self.authToLabelSeq[_seqKey][1]
                                if _seqId not in _factor['seq_id']:
                                    if self.reasons is None:
                                        continue
                                    realSeqId = get_real_seq_id(ps, realSeqId)
                                    if realSeqId is None:
                                        continue
                            idx = ps['auth_seq_id'].index(realSeqId)
                            realCompId = ps['comp_id'][idx]
                            if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                origCompId = ps['auth_comp_id'][idx]
                                _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                if realCompId not in _compIdList and origCompId not in _compIdList:
                                    continue
                                if set(_factor['comp_id']) != set(_compIdList):
                                    _factor['alt_comp_id'] = _factor['comp_id']
                                    _factor['comp_id'] = _compIdList
                            _compIdSelect.add(realCompId)
                            if realCompId not in monDict3:
                                _repNstdResidueInstance[realCompId] = (chainId, realSeqId)
                if self.hasNonPolySeq:
                    for chainId in _factor['chain_id']:
                        npList = [np for np in self.nonPolySeq if np['auth_chain_id'] == chainId]
                        for np in npList:
                            for realSeqId in np['auth_seq_id']:
                                if realSeqId is None:
                                    continue
                                if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                    _seqId = self.getOrigSeqId(np, realSeqId, False)
                                    if not self.preferAuthSeq and not np_chain_not_specified:
                                        if self.reasons is None:
                                            _seqKey = (chainId, _seqId)
                                            if _seqKey in self.authToLabelSeq:
                                                _seqId = self.authToLabelSeq[_seqKey][1]
                                        elif 'alt_auth_seq_id' in np and np['alt_auth_seq_id'][np['auth_seq_id'].index(_seqId)] in _factor['seq_id']:
                                            _seqId = np['alt_auth_seq_id'][np['auth_seq_id'].index(_seqId)]
                                    if _seqId not in _factor['seq_id']:
                                        if self.reasons is not None and (self.preferAuthSeq or _seqId != realSeqId) and realSeqId in np['auth_seq_id']:
                                            pass
                                        else:
                                            ptnr = getStructConnPtnr(self.cR, chainId, realSeqId)
                                            if ptnr is None:
                                                continue
                                idx = np['auth_seq_id'].index(realSeqId)
                                realCompId = self.getRealCompId(np['comp_id'][idx])
                                if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
                                    origCompId = np['auth_comp_id'][idx]
                                    _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                                    if realCompId not in _compIdList and origCompId not in _compIdList:
                                        continue
                                    if set(_factor['comp_id']) != set(_compIdList):
                                        _factor['alt_comp_id'] = _factor['comp_id']
                                        _factor['comp_id'] = _compIdList
                                _nonPolyCompIdSelect.append({'chain_id': chainId,
                                                             'seq_id': realSeqId,
                                                             'comp_id': realCompId})

                _atomIdSelect = set()
                for compId in _compIdSelect:
                    if self.ccU.updateChemCompDict(compId):
                        for cca in self.ccU.lastAtomList:
                            if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                realAtomId = cca[self.ccU.ccaAtomId]
                                _atomIdSelect.add(realAtomId)
                        if compId in _repNstdResidueInstance:
                            chainId, seqId = _repNstdResidueInstance[compId]
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)
                            if coordAtomSite is not None:
                                _atomIdSelect |= set(coordAtomSite['atom_id'])  # D_1300057999

                for nonPolyCompId in _nonPolyCompIdSelect:
                    _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], nonPolyCompId['seq_id'], cifCheck=cifCheck)
                    if coordAtomSite is not None:
                        if coordAtomSite['comp_id'] == nonPolyCompId['comp_id']:
                            for realAtomId in coordAtomSite['atom_id']:
                                _atomIdSelect.add(realAtomId)
                        else:
                            compId = nonPolyCompId['comp_id']
                            if self.ccU.updateChemCompDict(compId):
                                for cca in self.ccU.lastAtomList:
                                    if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                        realAtomId = cca[self.ccU.ccaAtomId]
                                        _atomIdSelect.add(realAtomId)
                    else:
                        for np in self.nonPolySeq:
                            if nonPolyCompId['seq_id'] == np['auth_seq_id'][0]:
                                _, coordAtomSite = self.getCoordAtomSiteOf(nonPolyCompId['chain_id'], np['seq_id'][0], cifCheck=cifCheck)
                                if coordAtomSite is not None:
                                    if coordAtomSite['comp_id'] == nonPolyCompId['comp_id']:
                                        for realAtomId in coordAtomSite['atom_id']:
                                            _atomIdSelect.add(realAtomId)
                                    else:
                                        compId = nonPolyCompId['comp_id']
                                        if self.ccU.updateChemCompDict(compId):
                                            for cca in self.ccU.lastAtomList:
                                                if cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                                    realAtomId = cca[self.ccU.ccaAtomId]
                                                    _atomIdSelect.add(realAtomId)

                _factor['atom_id'] = list(_atomIdSelect)

                if self.reasons is None:
                    self.preferAuthSeq = not self.preferAuthSeq

                if len(_factor['atom_id']) > 0:
                    if self.__lenAtomSelectionSet > 0:
                        self.setLocalSeqScheme()
                else:
                    _factor['atom_id'] = [None]

        if 'comp_id' in _factor and len(_factor['comp_id']) > 0:
            for chainId in _factor['chain_id']:
                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                if ps is not None:
                    for realSeqId in ps['auth_seq_id']:
                        if realSeqId is None:
                            continue
                        if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                            if self.getOrigSeqId(ps, realSeqId) not in _factor['seq_id']:
                                if self.reasons is None:
                                    continue
                                realSeqId = get_real_seq_id(ps, realSeqId)
                                if realSeqId is None:
                                    continue
                        idx = ps['auth_seq_id'].index(realSeqId)
                        realCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                        if realCompId not in _compIdList and origCompId not in _compIdList:
                            continue
                        if set(_factor['comp_id']) != set(_compIdList):
                            _factor['alt_comp_id'] = _factor['comp_id']
                            _factor['comp_id'] = _compIdList
            if self.hasNonPolySeq:
                for chainId in _factor['chain_id']:
                    npList = [np for np in self.nonPolySeq if np['auth_chain_id'] == chainId]
                    for np in npList:
                        for realSeqId in np['auth_seq_id']:
                            if realSeqId is None:
                                continue
                            if 'seq_id' in _factor and len(_factor['seq_id']) > 0:
                                seqId = _factor['seq_id'][0]
                                if self.getOrigSeqId(np, realSeqId, False) not in _factor['seq_id']:
                                    if seqId not in np['seq_id']:
                                        continue
                                    realSeqId = np['auth_seq_id'][np['seq_id'].index(seqId)]
                            idx = np['auth_seq_id'].index(realSeqId)
                            realCompId = self.getRealCompId(np['comp_id'][idx])
                            origCompId = np['auth_comp_id'][idx]
                            _compIdList = [translateToStdResName(_compId, realCompId, self.ccU) for _compId in _factor['comp_id']]
                            if realCompId not in _compIdList and origCompId not in _compIdList:
                                continue
                            if set(_factor['comp_id']) != set(_compIdList):
                                _factor['alt_comp_id'] = _factor['comp_id']
                                _factor['comp_id'] = _compIdList

        if self.reasons is not None and 'np_atom_id_remap' in self.reasons\
           and len(_factor['atom_id']) == 1 and _factor['atom_id'][0] is not None:
            _atomId = _factor['atom_id'][0].upper()
            if _atomId in self.reasons['np_atom_id_remap']:
                _seqKey = self.reasons['np_atom_id_remap'][_atomId]
                _factor['chain_id'] = [_seqKey[0]]
                _factor['seq_id'] = [_seqKey[1]]

        _atomSelection = []

        self.with_axis = self.cur_subtype in ('rdc', 'diff', 'csa', 'pcs', 'pre', 'prdc')

        len_f = len(self.f)

        foundCompId = False
        if _factor['atom_id'][0] is not None:
            foundCompId = self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection,
                                                             isPolySeq=True, isChainSpecified=True)
            if self.hasNonPolySeq:
                foundCompId |= self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection,
                                                                  isPolySeq=False, isChainSpecified=True,
                                                                  altPolySeq=self.nonPolySeq, resolved=foundCompId)

            if not foundCompId and len(_factor['chain_id']) == 1 and self.__multiPolymer\
               and 'global_sequence_offset' not in self.reasonsForReParsing\
               and (self.reasons is None or 'global_sequence_offset' not in self.reasons):
                foundCompId |= self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection,
                                                                  isPolySeq=True, isChainSpecified=False)
                if self.hasNonPolySeq:
                    self.__consumeFactor_expressions__(_factor, cifCheck, _atomSelection,
                                                       isPolySeq=False, isChainSpecified=False,
                                                       altPolySeq=self.nonPolySeq, resolved=foundCompId)

        atom_not_found_error = len(self.f) > len_f and any('[Atom not found]' in f or 'Hydrogen not instantiated' in f for f in self.f[len_f:])

        if self.reasons is None and self.preferAuthSeq and not atom_not_found_error and self.__complexSeqScheme\
           and not chain_not_specified and 'seq_not_specified' not in _factor:
            if guessCompIdFromAtomId(_factor['atom_id'], self.polySeq, self.nefT) is not None:
                if 'inhibit_label_seq_scheme_stats' not in self.reasonsForReParsing:
                    self.reasonsForReParsing['inhibit_label_seq_scheme_stats'] = {}
                chainId = _factor['chain_id'][0]
                if chainId not in self.reasonsForReParsing['inhibit_label_seq_scheme_stats']:
                    self.reasonsForReParsing['inhibit_label_seq_scheme_stats'][chainId] = 0
                self.reasonsForReParsing['inhibit_label_seq_scheme_stats'][chainId] += 1

        if 'segment_id' in _factor:
            del _factor['segment_id']
        if 'atom_ids' in _factor:
            del _factor['atom_ids']
        if 'atom_not_specified' in _factor:
            del _factor['atom_not_specified']
        if 'seq_not_specified' in _factor:
            del _factor['seq_not_specified']

        atomSelection = [dict(s) for s in set(frozenset(atom.items())
                                              for atom in _atomSelection
                                              if isinstance(atom, dict))]

        valid = len(self.f) == len_warn_msg

        if 'alt_chain_id' in _factor:
            for _atom in atomSelection:
                self.updateSegmentIdDict(_factor, _atom['chain_id'], _atom['is_poly'], valid)

        if 'atom_selection' not in _factor:
            _factor['atom_selection'] = atomSelection
        else:
            _factor['atom_selection'] = self.intersectionAtom_selections(_factor['atom_selection'], atomSelection)

        _atomId = _factor['atom_id'][0].upper() if _factor['atom_id'][0] is not None else None

        def has_identical_chain_id(chain_id):
            try:
                next(ps for ps in self.polySeq if ps['auth_chain_id'] == chain_id and 'identical_chain_id' in ps)
                return True
            except StopIteration:
                pass
            return False

        def update_np_atom_id_remap():
            if len(_factor['chain_id']) == 1 and len(_factor['seq_id']) == 1:
                if 'np_seq_id_remap' not in self.reasonsForReParsing:
                    self.reasonsForReParsing['np_seq_id_remap'] = {}
                chainId = _factor['chain_id'][0]
                srcSeqId = _factor['seq_id'][0]
                dstSeqId = self.__uniqAtomIdToSeqKey[_atomId][1]
                if chainId not in self.reasonsForReParsing['np_seq_id_remap']:
                    self.reasonsForReParsing['np_seq_id_remap'][chainId] = {}
                if srcSeqId in self.reasonsForReParsing['np_seq_id_remap'][chainId]:
                    if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] is not None:
                        if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] != dstSeqId:
                            self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = None
            else:
                if 'np_atom_id_remap' not in self.reasonsForReParsing:
                    self.reasonsForReParsing['np_atom_id_remap'] = {}
                if _atomId not in self.reasonsForReParsing['np_atom_id_remap']:
                    self.reasonsForReParsing['np_atom_id_remap'][_atomId] = self.__uniqAtomIdToSeqKey[_atomId]

        if len(_factor['atom_selection']) == 0:
            if _atomId is not None:
                __atomId = _atomId if len(_atomId) <= 2 else _atomId[:2]
                if self.with_axis and __atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                    return _factor
                if self.with_para and (('comp_id' in _factor and _atomId == _factor['comp_id'][0] and __atomId in PARAMAGNETIC_ELEMENTS)
                                       or __atomId in FERROMAGNETIC_ELEMENTS
                                       or __atomId in LANTHANOID_ELEMENTS):
                    return _factor
                if self.cur_subtype == 'dist' and __atomId in XPLOR_NITROXIDE_NAMES:
                    return _factor
            __factor = copy.copy(_factor)
            del __factor['atom_selection']
            if _atomId is None and 'alt_atom_id' not in _factor:
                if self.cur_subtype != 'plane' and cifCheck and not self.cur_union_expr:
                    if len(_factor['seq_id']) == 1 and 'alt_atom_id' in _factor and _factor['alt_atom_id'][0] is not None and 'comp_id' not in _factor:
                        for chainId in _factor['chain_id']:
                            updateSeqAtmRst(self.__seqAtmRstFailed, chainId, _factor['seq_id'][0], [_factor['alt_atom_id']])
                            if has_identical_chain_id(chainId):
                                break

            else:
                if self.cur_subtype != 'plane'\
                   and not (self.cur_subtype == 'rdc' and self.__lenAtomSelectionSet == 4
                            and len(_atomId) >= 2 and _atomId[:2] in PARAMAGNETIC_ELEMENTS):
                    if cifCheck:
                        if self.cur_union_expr or (self.top_union_expr and ambigAtomSelect):  # 2mws, 2krf
                            self.g.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.")
                            if len(_factor['atom_id']) == 1 and _atomId in self.__uniqAtomIdToSeqKey:
                                update_np_atom_id_remap()

                        else:
                            # self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                            #                 f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.")
                            if 'alt_chain_id' in _factor:  # 2mnz
                                for chainId in _factor['chain_id']:
                                    self.updateSegmentIdDict(_factor, chainId, None, False)
                            if foundCompId and len(_factor['atom_id']) == 1 and 'comp_id' not in _factor:
                                compIds = guessCompIdFromAtomId(_factor['atom_id'], self.polySeq, self.nefT)
                                if compIds is not None:
                                    foundCompId = False  # 2l5y
                            if not foundCompId:
                                # DAOTHER-9063
                                ligands = 0
                                npChainIds = set()
                                if self.hasNonPoly and self.cur_subtype == 'dist':
                                    for np in self.__nonPoly:
                                        ligands += len(np['seq_id'])
                                        npChainIds.add(np['auth_chain_id'])  # 2lqc
                                if ligands == 1:
                                    npChainIds.clear()  # 2ljc
                                if (len(_factor['chain_id']) == 1 or _factor['chain_id'][0] in npChainIds) and len(_factor['seq_id']) == 1:

                                    def update_np_seq_id_remap_request(np, ligands):
                                        if 'np_seq_id_remap' not in self.reasonsForReParsing:
                                            self.reasonsForReParsing['np_seq_id_remap'] = {}
                                        chainId = _factor['chain_id'][0]
                                        srcSeqId = _factor['seq_id'][0]
                                        dstSeqId = np['seq_id'][0]
                                        if chainId not in self.reasonsForReParsing['np_seq_id_remap']:
                                            self.reasonsForReParsing['np_seq_id_remap'][chainId] = {}
                                        if srcSeqId in self.reasonsForReParsing['np_seq_id_remap'][chainId]:
                                            if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] is not None:
                                                if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] != dstSeqId:
                                                    self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = None
                                                    ligands = 0
                                            else:
                                                ligands = 0
                                        else:
                                            self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = dstSeqId
                                        return ligands

                                    def upsert_np_seq_id_remap_request(np):
                                        if 'np_seq_id_remap' not in self.reasonsForReParsing:
                                            self.reasonsForReParsing['np_seq_id_remap'] = {}
                                        chainId = _factor['chain_id'][0]
                                        srcSeqId = _factor['seq_id'][0]
                                        dstSeqId = np['seq_id'][0]
                                        if chainId not in self.reasonsForReParsing['np_seq_id_remap']:
                                            self.reasonsForReParsing['np_seq_id_remap'][chainId] = {}
                                        if srcSeqId in self.reasonsForReParsing['np_seq_id_remap'][chainId]:
                                            if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] != dstSeqId:
                                                keys = list(self.reasonsForReParsing['np_seq_id_remap'][chainId].keys())
                                                vals = list(self.reasonsForReParsing['np_seq_id_remap'][chainId].values())
                                                if keys != sorted(keys) or vals != sorted(vals) or len(set(keys)) != len(set(vals)):
                                                    self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = dstSeqId
                                        else:
                                            self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = dstSeqId

                                    if ligands == 1:
                                        for np in self.__nonPoly:
                                            _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], np['seq_id'][0], cifCheck=cifCheck)
                                            if _coordAtomSite is not None and len(_factor['atom_id']) == 1\
                                               and _atomId is not None\
                                               and (_atomId in _coordAtomSite['atom_id']
                                                    or (len(_atomId) == 4 and ((_atomId[-2] == '+' and _atomId[-1].isdigit())
                                                                               or (_atomId[-1] == '+' and _atomId[-2].isdigit()))
                                                        and _atomId[:2] in _coordAtomSite['atom_id'])
                                                    or (len(_atomId) == 3 and (_atomId[-1].isdigit() or _atomId[-1] in ('+', '-'))
                                                        and _atomId[:2] in _coordAtomSite['atom_id'])
                                                    or (_atomId == 'X' and ('UNK' in _coordAtomSite['atom_id'] or 'UNX' in _coordAtomSite['atom_id']))):
                                                ligands = update_np_seq_id_remap_request(self.__nonPoly[0], ligands)
                                            else:
                                                ligands = 0

                                    elif ligands > 1 and len(_factor['atom_id']) == 1\
                                            and _atomId is not None\
                                            and (_atomId in SYMBOLS_ELEMENT  # 2n3r
                                                 or (len(_atomId) == 4 and ((_atomId[-2] == '+' and _atomId[-1].isdigit())
                                                                            or (_atomId[-1] == '+' and _atomId[-2].isdigit()))
                                                     and _atomId[:2] in SYMBOLS_ELEMENT)  # 6kg9, 2ma7
                                                 or (len(_atomId) == 3 and (_atomId[-1].isdigit() or _atomId[-1] in ('+', '-'))
                                                     and _atomId[:2] in SYMBOLS_ELEMENT)  # 2m28, 2mco
                                                 or _atomId == 'X'):  # 2mjq, 2mjr, 2mjs, 2mjt
                                        if _atomId != 'X':
                                            elemName = _atomId[:2]
                                            elemCount = 0
                                            refElemSeqIds = []
                                            for np in self.__nonPoly:
                                                if np['comp_id'][0] == elemName:
                                                    elemCount += 1
                                                    refElemSeqIds.append(np['seq_id'][0])
                                            if elemCount == 1:
                                                for np in self.__nonPoly:
                                                    if np['comp_id'][0] == elemName:
                                                        ligands = update_np_seq_id_remap_request(np, ligands)
                                                        break
                                            elif elemCount > 1:
                                                try:
                                                    elemSeqId = int(_factor['seq_id'][0])
                                                    found = False
                                                    for np in self.__nonPoly:
                                                        if np['comp_id'][0] == elemName and (elemSeqId in np['seq_id'] or elemSeqId in np['auth_seq_id']):
                                                            ligands = update_np_seq_id_remap_request(np, ligands)
                                                            found = True
                                                            break
                                                    if not found:
                                                        if 'alt_chain_id' in _factor:
                                                            elemChainId = _factor['alt_chain_id']
                                                            if elemName in elemChainId and len(elemChainId) > len(elemName) and elemChainId[len(elemName):].isdigit():
                                                                elemChainOrder = int(elemChainId[len(elemName):])
                                                                if 1 <= elemChainOrder <= len(refElemSeqIds):
                                                                    np_idx = 1
                                                                    for np in self.__nonPoly:
                                                                        if np['comp_id'][0] == elemName:
                                                                            if elemChainOrder == np_idx:
                                                                                ligands = update_np_seq_id_remap_request(np, ligands)
                                                                                found = True
                                                                                break
                                                                            np_idx += 1
                                                                else:  # 2lqc
                                                                    for elemSeqId in refElemSeqIds:
                                                                        for np in self.__nonPoly:
                                                                            if np['comp_id'][0] == elemName and elemSeqId in np['seq_id']:
                                                                                upsert_np_seq_id_remap_request(np)
                                                                    found = True
                                                        if not found:
                                                            if 1 <= elemSeqId <= len(refElemSeqIds):
                                                                elemSeqId = refElemSeqIds[elemSeqId - 1]
                                                                for np in self.__nonPoly:
                                                                    if np['comp_id'][0] == elemName and elemSeqId in np['seq_id']:
                                                                        ligands = update_np_seq_id_remap_request(np, ligands)
                                                            else:  # 2lqc
                                                                for elemSeqId in refElemSeqIds:
                                                                    for np in self.__nonPoly:
                                                                        if np['comp_id'][0] == elemName and elemSeqId in np['seq_id']:
                                                                            upsert_np_seq_id_remap_request(np)
                                                except ValueError:
                                                    pass
                                        else:
                                            for np in self.__nonPoly:
                                                _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], np['seq_id'][0], cifCheck=cifCheck)
                                                if 'UNK' in _coordAtomSite['atom_id']:  # 2mjq, 2mjr, 2mjs
                                                    ligands = update_np_seq_id_remap_request(np, ligands)
                                                    break
                                                if 'UNX' in _coordAtomSite['atom_id']:  # 2mjt
                                                    ligands = update_np_seq_id_remap_request(np, ligands)
                                                    break

                                    elif len(_factor['atom_id']) == 1 and _atomId in self.__uniqAtomIdToSeqKey:
                                        update_np_atom_id_remap()
                                        ligands = 1

                                if len(_factor['seq_id']) == 1:
                                    if len(_factor['atom_id']) == 1 and 'comp_id' not in _factor:
                                        compIds = guessCompIdFromAtomId(_factor['atom_id'], self.polySeq, self.nefT)
                                        if compIds is not None:
                                            for chainId in _factor['chain_id']:
                                                if len(compIds) == 1:
                                                    updatePolySeqRst(self.__polySeqRstFailed, chainId, _factor['seq_id'][0], compIds[0])
                                                else:
                                                    updatePolySeqRstAmbig(self.__polySeqRstFailedAmbig, chainId, _factor['seq_id'][0], compIds)
                                                if has_identical_chain_id(chainId):
                                                    break
                                        for chainId in _factor['chain_id']:
                                            updateSeqAtmRst(self.__seqAtmRstFailed, chainId, _factor['seq_id'][0], _factor['atom_id'])
                                            if has_identical_chain_id(chainId):
                                                break

                                if ligands == 0 and not self.has_nx and not self.has_gd and not self.has_la\
                                   and (self.monoPolymer or all('identical_chain_id' in ps for ps in self.polySeq) or not chain_not_specified):
                                    if _atomId is not None and _atomId.startswith('X')\
                                       and _atomId not in SYMBOLS_ELEMENT:
                                        pass  # 8bxj
                                    elif self.reasons is not None and 'segment_id_mismatch' in self.reasons:
                                        pass  # 6f0y
                                    # 2knf, 2ma9
                                    elif _atomId is None\
                                            or (_atomId not in aminoProtonCode and _atomId not in carboxylCode and _atomId not in jcoupBbPairCode)\
                                            or self.gapInAuthSeq:  # 2kyg
                                        if not self.cur_subtype_altered or not self.in_noe:  # 2ljc
                                            if self.reasons is None:
                                                self.preferAuthSeq = not self.preferAuthSeq
                                                # self.authSeqId = 'auth_seq_id' if self.preferAuthSeq else 'label_seq_id'
                                                self.setLocalSeqScheme()
                                                # ad hoc sequence scheme switching is possible for the first restraint, otherwise the entire restraints should be re-parsed
                                                if trial < 3 and 'Check the 1th row of' in self.getCurrentRestraint()\
                                                   and (self.cur_subtype != 'dist' and not self.in_noe):
                                                    # skip ad hoc sequence scheme switching should be inherited to the other restraints
                                                    del _factor['atom_selection']
                                                    return self.doConsumeFactor_expressions(_factor, clauseName, cifCheck, trial + 1)
                                                if not self.preferAuthSeq and self.reasons is None\
                                                   and ((self.cur_subtype != 'dist' and not self.in_noe) or 'Check the 2th row of' in self.getCurrentRestraint()):  # 6nk9
                                                    if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                        self.reasonsForReParsing['label_seq_scheme'] = {}
                                                    self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True

                                elif self.with_para and _atomId not in XPLOR_RDC_PRINCIPAL_AXIS_NAMES and self.reasons is None:
                                    self.preferAuthSeq = not self.preferAuthSeq
                                    self.setLocalSeqScheme()
                                    if 'label_seq_scheme' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['label_seq_scheme'] = {}
                                    self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True

                            if not atom_not_found_error:
                                if _atomId is not None and _atomId.startswith('X')\
                                   and _atomId not in SYMBOLS_ELEMENT:  # 8bxj
                                    self.f.append(f"[Invalid data] {self.getCurrentRestraint()}"
                                                  f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.")
                                else:
                                    no_ext_seq = True
                                    unobs_seq = False
                                    if len(_factor['chain_id']) == 1 and len(_factor['seq_id']) == 1:
                                        _chainId = _factor['chain_id'][0]
                                        _seqId = _factor['seq_id'][0]
                                        ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == _chainId), None)
                                        no_nonpoly = not self.hasNonPolySeq\
                                            or not any(_seqId in np['auth_seq_id'] for np in self.nonPolySeq if np['auth_chain_id'] == _chainId)  # 2mco
                                        if ps is not None and _seqId not in ps['auth_seq_id'] and no_nonpoly:
                                            if self.__nmrVsModel is not None and not ('gap_in_auth_seq' in ps and ps['gap_in_auth_seq']):
                                                nmr_offset = ps['seq_id'][0] - ps['auth_seq_id'][0]  # 2lzn
                                                if self.reasons is not None and 'global_auth_sequence_offset' in self.reasons\
                                                   and _chainId in self.reasons['global_auth_sequence_offset']:
                                                    nmr_offset += self.reasons['global_auth_sequence_offset'][_chainId]
                                                elif self.reasons is not None and 'auth_sequence_offset' in self.reasons\
                                                        and _chainId in self.reasons['auth_sequence_offset']:
                                                    nmr_offset += self.reasons['auth_sequence_offset'][_chainId]
                                                elif self.reasons is not None and 'label_sequence_offset' in self.reasons\
                                                        and _chainId in self.reasons['label_sequence_offset']:
                                                    nmr_offset += self.reasons['label_sequence_offset'][_chainId]
                                                item = next((item for item in self.__nmrVsModel
                                                             if item['test_auth_chain_id' if 'test_auth_chain_id' in item else 'test_chain_id'] == _chainId), None)
                                                if item is not None and item['conflict'] == 0 and item['unmapped'] > 0 and 'unmapped_sequence' in item:
                                                    refCompId = next((u['ref_comp_id'] for u in item['unmapped_sequence']
                                                                      if 'ref_seq_id' in u and u['ref_seq_id'] == _seqId + nmr_offset), None)
                                                    if refCompId is not None:
                                                        hint = f" The residue '{_seqId}:{refCompId}' is not present in polymer sequence "\
                                                            f"of chain {_chainId} of the coordinates. "\
                                                            "Please update the sequence in the Macromolecules page."
                                                        if self.reasons is not None:
                                                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                                          f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.{hint}")
                                                        no_ext_seq = False  # 2ls7
                                            if no_ext_seq:
                                                auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                                                if len(auth_seq_id_list) > 0:
                                                    min_auth_seq_id = min(auth_seq_id_list)
                                                    max_auth_seq_id = max(auth_seq_id_list)
                                                    if (_seqId < min_auth_seq_id and min_auth_seq_id - _seqId <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR)\
                                                       or (_seqId > max_auth_seq_id and _seqId - max_auth_seq_id <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR):
                                                        hint = f" The residue '{_seqId}' is not present in polymer sequence "\
                                                            f"of chain {_chainId} of the coordinates. "\
                                                            "Please update the sequence in the Macromolecules page."
                                                        if self.reasons is not None:
                                                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                                          f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.{hint}")
                                                        no_ext_seq = False  # 2law
                                        _seqKey = (_chainId, _seqId)
                                        if _seqKey in self.__coordUnobsRes:
                                            unobs_seq = True  # 2n25
                                        if _seqKey in self.__coordUnobsAtom and 'atom_id' in _factor and len(_factor['atom_id']) > 0:
                                            _atomIds = self.getAtomIdList(_factor, self.__coordUnobsAtom[_seqKey]['comp_id'], _factor['atom_id'][0])
                                            if _atomIds[0] in self.__coordUnobsAtom[_seqKey]['atom_ids']:
                                                unobs_seq = True
                                    elif len(_factor['chain_id']) > 1 and len(_factor['seq_id']) == 1:
                                        _chainId_ = []
                                        _seqId = _factor['seq_id'][0]
                                        for _chainId in _factor['chain_id']:
                                            ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == _chainId), None)
                                            if ps is not None and _seqId not in ps['auth_seq_id']:
                                                auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                                                if len(auth_seq_id_list) > 0:
                                                    min_auth_seq_id = min(auth_seq_id_list)
                                                    max_auth_seq_id = max(auth_seq_id_list)
                                                    if (_seqId < min_auth_seq_id and min_auth_seq_id - _seqId <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR)\
                                                       or (_seqId > max_auth_seq_id and _seqId - max_auth_seq_id <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR):
                                                        _chainId_.append(_chainId)
                                        if len(_chainId_) == 1:
                                            _chainId = _chainId_[0]
                                            ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == _chainId), None)
                                            no_nonpoly = not self.hasNonPolySeq\
                                                or not any(_seqId in np['auth_seq_id'] for np in self.nonPolySeq if np['auth_chain_id'] == _chainId)
                                            if ps is not None and _seqId not in ps['auth_seq_id'] and no_nonpoly:
                                                auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                                                if len(auth_seq_id_list) > 0:
                                                    min_auth_seq_id = min(auth_seq_id_list)
                                                    max_auth_seq_id = max(auth_seq_id_list)
                                                    if (_seqId < min_auth_seq_id and min_auth_seq_id - _seqId <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR)\
                                                       or (_seqId > max_auth_seq_id and _seqId - max_auth_seq_id <= MIN_EXT_SEQ_FOR_ATOM_SEL_ERR):
                                                        hint = f" The residue '{_seqId}' is not present in polymer sequence "\
                                                            f"of chain {_chainId} of the coordinates. "\
                                                            "Please update the sequence in the Macromolecules page."
                                                        if self.reasons is not None:
                                                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                                          f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.{hint}")
                                                        no_ext_seq = False  # 2mps
                                            _seqKey = (_chainId, _seqId)
                                            if _seqKey in self.__coordUnobsRes:
                                                unobs_seq = True  # 2n25
                                            if _seqKey in self.__coordUnobsAtom and 'atom_id' in _factor and len(_factor['atom_id']) > 0:
                                                _atomIds[0] = self.getAtomIdList(_factor, self.__coordUnobsAtom[_seqKey]['comp_id'], _factor['atom_id'][0])
                                                if _atomIds in self.__coordUnobsAtom[_seqKey]['atom_ids']:
                                                    unobs_seq = True
                                    if (no_ext_seq or self.reasons is None) and not unobs_seq:
                                        if no_ext_seq:  # 2laz
                                            hint = " Please make sure that the values in 'segidentifier', 'residue', and 'name' clauses of the restraint file match "\
                                                "the auth_asym_id, auth_seq_id, and auth_atom_id values of the coordinates, respectively. "
                                            if self.has_gd:
                                                hint += "We ignore the atom selection since it may be related to ambiguous PRE restraints induced by Gd3+ spin label."
                                            elif self.has_la:
                                                hint += "We ignore the atom selection since it may be related to paramagnetic restraints induced by Lanthanide ion."
                                            elif self.has_nx:
                                                hint += "We ignore the atom selection since it may be related to ambiguous PRE restraints induced by nitroxide spin label."
                                            else:
                                                hint += "Alternatively, try to upload the genuine coordinate file generated by structure determination software without editing."
                                        self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                                      f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.{hint}")
                    else:
                        self.g.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                      f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}. "
                                      "Please update the sequence in the Macromolecules page.")
                elif self.cur_subtype == 'plane':
                    if 'atom_id' not in _factor or ('H5T' not in _factor['atom_id'] and 'H3T' not in _factor['atom_id']
                                                    and 'HOP2' not in _factor['atom_id'] and "HO3'" not in _factor['atom_id']
                                                    and "O2'" not in _factor['atom_id']):
                        if not atom_not_found_error:
                            hint = f" Please verify that the planarity restraints match with the residue {_factor['comp_id'][0]!r}"\
                                if 'comp_id' in _factor and len(_factor['comp_id']) == 1 else ''
                            self.f.append(f"[Insufficient atom selection] {self.getCurrentRestraint()}"
                                          f"The {clauseName} has no effect for a factor {self.getReadableFactor(__factor)}.{hint}")

        elif len(_factor['chain_id']) == 1 and len(_factor['seq_id']) == 1 and len(_factor['atom_id']) == 1 and 'comp_id' not in _factor:
            compIds = guessCompIdFromAtomId(_factor['atom_id'], self.polySeq, self.nefT)
            if compIds is not None:
                if len(compIds) == 1:
                    updatePolySeqRst(self.__polySeqRstValid, _factor['chain_id'][0], _factor['seq_id'][0], compIds[0])

        if 'chain_id' in _factor:
            del _factor['chain_id']
        if 'comp_id' in _factor:
            del _factor['comp_id']
        if 'seq_id' in _factor:
            del _factor['seq_id']
        if 'type_symbol' in _factor:
            del _factor['type_symbol']
        if 'atom_id' in _factor:
            del _factor['atom_id']
        if 'alt_chain_id' in _factor:
            del _factor['alt_chain_id']
        if 'alt_atom_id' in _factor:
            del _factor['alt_atom_id']

        if ambigAtomSelect or valid:
            self.__cachedDictForFactor[key] = deepcopy(_factor)

        return _factor

    def __consumeFactor_expressions__(self, _factor: dict, cifCheck: bool, _atomSelection: List[dict],
                                      isPolySeq: bool = True, isChainSpecified: bool = True,
                                      altPolySeq: Optional[List[dict]] = None, resolved: bool = False) -> bool:
        atomSpecified = True
        if 'atom_not_specified' in _factor:
            atomSpecified = not _factor['atom_not_specified']
        seqSpecified = True
        if 'seq_not_specified' in _factor:
            seqSpecified = not _factor['seq_not_specified']
        foundCompId = False

        if self.reasons is not None and 'segment_id_poly_type_stats' in self.reasons\
           and 'segment_id' in _factor and _factor['segment_id'] in self.reasons['segment_id_poly_type_stats']:
            stats = self.reasons['segment_id_poly_type_stats'][_factor['segment_id']]
            if isPolySeq and stats['polymer'] < stats['non-poly']:
                return False
            if not isPolySeq and 'np_seq_id_remap' not in self.reasons:
                if stats['polymer'] > 10 * stats['non-poly']:
                    return False
                if stats['polymer'] >= stats['non-poly']\
                   and 'non_poly_remap' not in self.reasons\
                   and (not self.hasNonPoly
                        or not any(any(ps['auth_chain_id'] == np['auth_chain_id'] for ps in self.polySeq)
                                   for np in self.__nonPoly)):
                    return False

        chainIds = (_factor['chain_id'] if isChainSpecified else [ps['auth_chain_id'] for ps in (self.polySeq if isPolySeq else altPolySeq)])

        for chainId in chainIds:

            if self.reasons is not None:

                if 'label_seq_scheme' in self.reasons\
                   and self.reasons['label_seq_scheme'] is not None\
                   and self.cur_subtype in self.reasons['label_seq_scheme']\
                   and self.reasons['label_seq_scheme'][self.cur_subtype]\
                   and 'inhibit_label_seq_scheme' in self.reasons and chainId in self.reasons['inhibit_label_seq_scheme']\
                   and self.cur_subtype in self.reasons['inhibit_label_seq_scheme'][chainId]\
                   and self.reasons['inhibit_label_seq_scheme'][chainId][self.cur_subtype]\
                   and 'segment_id_mismatch' not in self.reasons:
                    continue

                if 'uninterpretable_chain_id' in self.reasons\
                   and chainId in self.reasons['uninterpretable_chain_id']\
                   and self.cur_subtype != 'dist'\
                   and 'chain_id_remap' not in self.reasons:  # 2n2w
                    continue  # 2lqc

            psList = [ps for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['auth_chain_id'] == chainId]

            if len(psList) == 0:
                if isChainSpecified:
                    _chainIds = [ps['auth_chain_id'] for ps in (self.polySeq if isPolySeq else altPolySeq)]
                    if self.hasBranched:
                        _chainIds.extend([br['auth_chain_id'] for br in self.__branched])
                    if all(_chainId not in _chainIds for _chainId in chainIds)\
                       and chainId in [ps['chain_id'] for ps in (self.polySeq if isPolySeq else altPolySeq)]:
                        psList = [ps for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['chain_id'] == chainId]
                    if len(psList) == 0:
                        continue
                    if 'auth_chain_id' in _factor:
                        _authChainIds = []
                        for _chainId in _factor['auth_chain_id']:
                            _authChainId = next((ps['auth_chain_id'] for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['chain_id'] == _chainId), _chainId)
                            if _chainId == chainId:
                                chainId = _authChainId
                            _authChainIds.append(_authChainId)
                        _factor['auth_chain_id'] = _authChainIds
                else:
                    continue

            prefAltAuthSeqId = False

            for ps in psList:

                for seqId in _factor['seq_id']:

                    if seqId is None:
                        continue

                    _seqId_ = seqId
                    seqId, _compId_, extSeqScheme = self.getRealSeqId(ps, seqId, isPolySeq)

                    if seqId is None:
                        continue

                    _seqId = seqId
                    if self.reasons is not None:
                        if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
                            if fixedChainId != chainId:
                                continue
                        if 'np_seq_id_remap' in self.reasons:
                            if isPolySeq:
                                if 'segment_id' in _factor and 'segment_id_mismatch' in self.reasons\
                                   and chainId in self.reasons['segment_id_mismatch'].values()\
                                   and 'segment_id_poly_type_stats' in self.reasons\
                                   and _factor['segment_id'] in self.reasons['segment_id_poly_type_stats']\
                                   and stats['polymer'] <= stats['non-poly']:  # 2mtk
                                    _, __seqId = retrieveRemappedSeqId(self.reasons['np_seq_id_remap'], chainId, seqId)
                                    if __seqId is not None and __seqId != seqId and list(self.reasons['segment_id_mismatch'].values()).count(chainId) > 1:
                                        continue  # 2lkd
                            else:
                                _, seqId = retrieveRemappedSeqId(self.reasons['np_seq_id_remap'], chainId, seqId)
                                if seqId is not None:
                                    if _seqId_ != seqId and len(_atomSelection) > 0:
                                        continue
                                    _seqId_ = seqId
                        elif 'chain_id_remap' in self.reasons and seqId in self.reasons['chain_id_remap']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                            if fixedChainId != chainId:
                                continue
                        elif 'chain_id_clone' in self.reasons and seqId in self.reasons['chain_id_clone']:
                            fixedChainId, seqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                            if fixedChainId != chainId and isPolySeq:
                                continue
                        elif 'seq_id_remap' in self.reasons:
                            _, seqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], chainId, seqId)
                        if seqId is None:
                            seqId = _seqId

                    if ps is not None and seqId in ps['auth_seq_id']:
                        compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                    elif _compId_ is not None and self.reasons is not None and 'extend_seq_scheme' in self.reasons:
                        compId = _compId_
                    elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq'] and seqId is not None:
                        compId = None
                        auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                        if len(auth_seq_id_list) > 0:
                            min_auth_seq_id = min(auth_seq_id_list)
                            max_auth_seq_id = max(auth_seq_id_list)
                            if min_auth_seq_id <= seqId <= max_auth_seq_id:
                                _seqId_ = seqId + 1
                                while _seqId_ <= max_auth_seq_id:
                                    if _seqId_ in ps['auth_seq_id']:
                                        break
                                    _seqId_ += 1
                                if _seqId_ not in ps['auth_seq_id']:
                                    _seqId_ = seqId - 1
                                    while _seqId_ >= min_auth_seq_id:
                                        if _seqId_ in ps['auth_seq_id']:
                                            break
                                        _seqId_ -= 1
                                if _seqId_ in ps['auth_seq_id']:
                                    idx = ps['auth_seq_id'].index(_seqId_) - _seqId_ - seqId
                                    try:
                                        seqId = ps['auth_seq_id'][idx]
                                        compId = ps['comp_id'][idx]
                                    except IndexError:
                                        pass
                    else:
                        compId = None

                    if not isPolySeq:
                        if compId is None:
                            if 'alt_auth_seq_id' in ps and seqId in ps['alt_auth_seq_id']:
                                idx = ps['alt_auth_seq_id'].index(seqId)
                                seqId = ps['seq_id'][idx]
                                compId = ps['comp_id'][idx]
                                prefAltAuthSeqId = True
                            elif seqId in ps['seq_id']:
                                idx = ps['seq_id'].index(seqId)
                                compId = ps['comp_id'][idx]
                                _seqId_ = ps['auth_seq_id'][idx]
                        elif prefAltAuthSeqId:
                            continue

                    if None in (self.authToInsCode, _compId_) or len(self.authToInsCode) == 0:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, cifCheck=cifCheck)
                    else:
                        compId = _compId_
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, _compId_, cifCheck=cifCheck)

                    if compId is None and seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if ps is not None and seqId in ps['auth_seq_id']:
                            compId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)

                    if compId is None and coordAtomSite is not None and ps is not None and seqKey[1] in ps['auth_seq_id']:
                        compId = ps['comp_id'][ps['auth_seq_id'].index(seqKey[1])]

                    if coordAtomSite is None and not isPolySeq:
                        try:
                            idx = ps['auth_seq_id'].index(seqId)
                            seqId = ps['seq_id'][idx]
                            compId = ps['comp_id'][idx]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)
                        except ValueError:  # 2yhh (branched)
                            try:
                                idx = ps['seq_id'].index(seqId)
                                seqId = ps['auth_seq_id'][idx]
                                compId = ps['comp_id'][idx]
                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)
                            except ValueError:
                                pass

                    atomId = _factor['atom_id'][0].upper()

                    if self.hasNonPoly:
                        if isPolySeq and len(atomId) == 4\
                           and atomId[:2] in SYMBOLS_ELEMENT\
                           and atomId[2:] in ('+1', '+2', '+3', '1+', '2+', '3+'):
                            elemName = atomId[:2]
                            elemCount = 0
                            for np in self.__nonPoly:
                                if np['comp_id'][0] == elemName:
                                    elemCount += 1
                            if elemCount > 0:
                                continue

                        elif not isPolySeq and len(atomId) >= 2\
                                and (atomId in SYMBOLS_ELEMENT
                                     or (len(atomId) == 4 and atomId[:2] in SYMBOLS_ELEMENT
                                         and atomId[2:] in ('+1', '+2', '+3', '1+', '2+', '3+'))):
                            elemName = atomId[:2]
                            elemCount = 0
                            for np in self.__nonPoly:
                                if np['comp_id'][0] == elemName:
                                    elemCount += 1
                            if elemCount == 1 and elemName in ps['comp_id']\
                               and (self.cur_subtype == 'dist' or self.with_para):
                                compId = elemName
                                seqId = ps['auth_seq_id'][0]
                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, cifCheck=cifCheck)

                    if compId is None:
                        # """ cancel the following code because comp_id prediction conflicts with extended sequence (7zjy)
                        # if isPolySeq and isChainSpecified and self.reasons is None and self.preferAuthSeq:
                        #     self.preferAuthSeq = False
                        #     seqId, _compId_, _ = self.getRealSeqId(ps, seqId, isPolySeq)
                        #     if self.csStat.peptideLike(_compId_):
                        #         compIds = guessCompIdFromAtomId(_factor['atom_id'], self.polySeq, self.nefT)
                        #         if compIds is not None and _compId_ in compIds:
                        #             if 'label_seq_scheme' not in self.reasonsForReParsing:
                        #                 self.reasonsForReParsing['label_seq_scheme'] = {}
                        #             self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                        #     self.preferAuthSeq = True
                        # """
                        if isPolySeq and seqSpecified and atomSpecified\
                           and self.reasons is None and self.preferAuthSeq and self.__altPolySeq is not None:
                            if seqId in self.__effSeqIdSet:
                                continue
                            __ps = next((__ps for __ps in self.__altPolySeq if __ps['auth_chain_id'] == chainId), None)  # 2mg5
                            if __ps is None or seqId not in __ps['auth_seq_id']:
                                continue
                            try:
                                __seqId = ps['auth_seq_id'][__ps['auth_seq_id'].index(seqId)]
                                if seqId == __seqId:
                                    continue
                                _, __coordAtomSite = self.getCoordAtomSiteOf(chainId, __seqId, cifCheck=cifCheck)
                                if __coordAtomSite is None:
                                    continue
                                __compId = __coordAtomSite['comp_id']
                                __atomSiteAtomId = __coordAtomSite['atom_id']

                                offsets = set()

                                for atomId in _factor['atom_id']:
                                    _atomId = atomId.upper() if len(atomId) <= 2 else atomId[:2].upper()
                                    if self.with_axis:
                                        if _atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                                            continue
                                    atomId = atomId.upper()
                                    if __compId not in monDict3 and self.mrAtomNameMapping is not None:
                                        authCompId = ps['auth_comp_id'][ps['auth_seq_id'].index(__seqId)]
                                        atomId = retrieveAtomIdFromMRMap(self.ccU, self.mrAtomNameMapping, __seqId, authCompId, atomId, __coordAtomSite)
                                    __atomIds = self.getAtomIdList(_factor, __compId, atomId)
                                    if __atomIds[0] in __atomSiteAtomId:
                                        offsets.add(__seqId - seqId)

                                if len(offsets) > 0:
                                    if 'alt_global_sequence_offset' not in self.reasonsForReParsing:
                                        self.reasonsForReParsing['alt_global_sequence_offset'] = {}
                                    if chainId in self.reasonsForReParsing['alt_global_sequence_offset']:
                                        if self.reasonsForReParsing['alt_global_sequence_offset'][chainId] is None:
                                            continue
                                        self.reasonsForReParsing['alt_global_sequence_offset'][chainId] &= offsets
                                        if len(self.reasonsForReParsing['alt_global_sequence_offset'][chainId]) == 0:
                                            self.reasonsForReParsing['alt_global_sequence_offset'][chainId] = None
                                            continue
                                        continue
                                    self.reasonsForReParsing['alt_global_sequence_offset'][chainId] = offsets
                            except IndexError:
                                pass
                        continue

                    if self.reasons is not None:
                        if 'non_poly_remap' in self.reasons and compId in self.reasons['non_poly_remap']\
                           and _factor['seq_id'][0] in self.reasons['non_poly_remap'][compId]:
                            fixedChainId, seqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], ps, chainId, _factor['seq_id'][0], compId)
                            if fixedChainId != chainId:
                                continue
                            if not isPolySeq and len(_atomSelection) > 0:
                                continue

                    _seqId = seqId
                    if self.reasons is None and not isPolySeq and 'alt_auth_seq_id' in ps and seqId not in ps['auth_seq_id'] and seqId in ps['alt_auth_seq_id']:
                        try:
                            seqId = next(_seqId_ for _seqId_, _altSeqId_ in zip(ps['auth_seq_id'], ps['alt_auth_seq_id']) if _altSeqId_ == seqId)
                        except StopIteration:
                            pass
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck)

                    if not isPolySeq and isChainSpecified and self.doesNonPolySeqIdMatchWithPolySeqUnobs(_factor['chain_id'][0], _seqId_):
                        if coordAtomSite is None or atomId not in coordAtomSite['atom_id']:
                            continue

                    if not isPolySeq:
                        replacedBy = self.getRealCompId(compId)
                        if replacedBy != compId:
                            compId = replacedBy
                            _coordAtomSite = deepcopy(coordAtomSite)
                            _coordAtomSite['comp_id'] = compId
                            _coordAtomSite['atom_id'] = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                            _coordAtomSite['alt_atom_id'] = [cca[self.ccU.ccaAltAtomId] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                            _coordAtomSite['type_symbol'] = [cca[self.ccU.ccaTypeSymbol] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaLeavingAtomFlag] != 'Y']
                            _coordAtomSite['alt_comp_id'] = [coordAtomSite['alt_comp_id'][0]] * len(_coordAtomSite['atom_id'])
                            coordAtomSite = _coordAtomSite

                    foundCompId = True

                    if not self.with_axis and not self.with_para:
                        updatePolySeqRst(self.__polySeqRst, chainId, seqId, compId)

                    atomSiteAtomId = None if coordAtomSite is None else coordAtomSite['atom_id']

                    if atomSiteAtomId is not None and isPolySeq and self.csStat.peptideLike(compId)\
                       and not any(_atomId in atomSiteAtomId for _atomId in _factor['atom_id'])\
                       and all(_atomId in ('H1', 'H2', 'HN1', 'HN2', 'NT') for _atomId in _factor['atom_id']):
                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId + 1, cifCheck=cifCheck)
                        if _coordAtomSite is not None and _coordAtomSite['comp_id'] == 'NH2':
                            compId = 'NH2'
                            seqId = seqId + 1
                            seqKey = _seqKey
                            coordAtomSite = _coordAtomSite
                            atomSiteAtomId = _coordAtomSite['atom_id']
                        elif 'split_comp_id' in coordAtomSite and 'NH2' in coordAtomSite['split_comp_id']:
                            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, 'NH2', cifCheck=cifCheck)
                            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == 'NH2':
                                compId = 'NH2'
                                seqKey = _seqKey
                                coordAtomSite = _coordAtomSite
                                atomSiteAtomId = _coordAtomSite['atom_id']

                    if self.hasNonPoly and compId == 'CYS':

                        if atomId in zincIonCode:
                            znCount = 0
                            znSeqId = None
                            for np in self.__nonPoly:
                                if np['comp_id'][0] == 'ZN':
                                    znSeqId = np['auth_seq_id'][0]
                                    znCount += 1
                            if znCount > 0:
                                if znCount == 1:
                                    _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, znSeqId, 'ZN', cifCheck=cifCheck)
                                    if _coordAtomSite is not None and _coordAtomSite['comp_id'] == 'ZN':
                                        compId = 'ZN'
                                        seqId = znSeqId
                                        seqKey = _seqKey
                                        coordAtomSite = _coordAtomSite
                                        atomSiteAtomId = _coordAtomSite['atom_id']

                        if atomId in calciumIonCode:
                            caCount = 0
                            caSeqId = None
                            for np in self.__nonPoly:
                                if np['comp_id'][0] == 'CA':
                                    caSeqId = np['auth_seq_id'][0]
                                    caCount += 1
                            if caCount > 0:
                                if caCount == 1:
                                    _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, caSeqId, 'CA', cifCheck=cifCheck)
                                    if _coordAtomSite is not None and _coordAtomSite['comp_id'] == 'CA':
                                        compId = 'CA'
                                        seqId = caSeqId
                                        seqKey = _seqKey
                                        coordAtomSite = _coordAtomSite
                                        atomSiteAtomId = _coordAtomSite['atom_id']

                    auth_seq_id_list = list(filter(None, ps['auth_seq_id']))

                    for atomId in _factor['atom_id']:
                        _atomId = atomId.upper() if len(atomId) <= 2 else atomId[:2].upper()
                        if self.with_axis:
                            if _atomId in XPLOR_RDC_PRINCIPAL_AXIS_NAMES:
                                continue
                        if self.with_para:
                            if (atomId == compId and _atomId in PARAMAGNETIC_ELEMENTS) or _atomId in FERROMAGNETIC_ELEMENTS:  # or _atomId in LANTHANOID_ELEMENTS:
                                continue
                        if self.with_axis or self.with_para:
                            updatePolySeqRst(self.__polySeqRst, chainId, seqId, compId)

                        origAtomId = _factor['atom_id'] if 'alt_atom_id' not in _factor else _factor['alt_atom_id']
                        # """
                        # if isinstance(origAtomId, str) and origAtomId.startswith('HT') and coordAtomSite is not None and origAtomId not in atomSiteAtomId:
                        #     if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or seqId == min(auth_seq_id_list):
                        #         continue
                        # """
                        atomId = atomId.upper()

                        if not isPolySeq and compId in PARAMAGNETIC_ELEMENTS:
                            if compId not in atomId:
                                continue
                            if compId != atomId:
                                atomId = compId

                        if self.mrAtomNameMapping is not None:
                            # 6u24: split during annotation
                            if isPolySeq and compId in monDict3 and 'alt_comp_id' in ps and self.hasNonPolySeq:
                                if _seqId in ps['auth_seq_id']:
                                    authCompId = ps['alt_comp_id'][ps['auth_seq_id'].index(_seqId)]
                                else:
                                    authCompId = ps['alt_comp_id'][ps['auth_seq_id'].index(_seqId_)]
                                if authCompId not in monDict3:
                                    __seqId__, __compId__, __atomId__ = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, _seqId,
                                                                                                   authCompId, atomId, ignoreSeqId=True)
                                    split = 0
                                    for np in self.nonPolySeq:
                                        if __compId__ in np['comp_id']:
                                            split += 1
                                    if split == 1:
                                        for np in self.nonPolySeq:
                                            if __compId__ in np['comp_id']:
                                                _factor['chain_id'] = [np['auth_chain_id']]
                                                _factor['seq_id'] = [__seqId__]
                                                _factor['atom_id'] = [__atomId__]
                                        continue

                            if compId not in monDict3\
                               and ((_seqId in ps['auth_seq_id'] or _seqId_ in ps['auth_seq_id'])
                                    or ('alt_auth_seq_id' in ps
                                        and (_seqId in ps['alt_auth_seq_id'] or _seqId_ in ps['alt_auth_seq_id']))):
                                if _seqId in ps['auth_seq_id']:
                                    authCompId = ps['auth_comp_id'][ps['auth_seq_id'].index(_seqId)]
                                elif _seqId_ in ps['auth_seq_id']:
                                    authCompId = ps['auth_comp_id'][ps['auth_seq_id'].index(_seqId_)]
                                elif _seqId in ps['alt_auth_seq_id']:
                                    authCompId = ps['auth_comp_id'][ps['alt_auth_seq_id'].index(_seqId)]
                                else:
                                    authCompId = ps['auth_comp_id'][ps['alt_auth_seq_id'].index(_seqId_)]
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.mrAtomNameMapping, _seqId, authCompId, atomId, coordAtomSite)
                                if coordAtomSite is not None and atomId not in atomSiteAtomId:
                                    if self.reasons is not None and 'branched_remap' in self.reasons:
                                        _seqId_ = retrieveOriginalSeqIdFromMRMap(self.reasons['branched_remap'], chainId, seqId)
                                        if _seqId_ != seqId:
                                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, _seqId_, authCompId, atomId, compId, coordAtomSite)
                                    elif seqId != _seqId:
                                        atomId = retrieveAtomIdFromMRMap(self.ccU, self.mrAtomNameMapping, seqId, authCompId, atomId, coordAtomSite)

                        atomIds = self.getAtomIdList(_factor, compId, atomId)

                        if atomSiteAtomId is not None:
                            if not any(_atomId in atomSiteAtomId for _atomId in atomIds):
                                atomId = translateToStdAtomName(atomId, compId, atomSiteAtomId, self.ccU, False)
                            elif atomId[0] not in pseProBeginCode and not all(_atomId in atomSiteAtomId for _atomId in atomIds):
                                atomIds = [_atomId for _atomId in atomIds if _atomId in atomSiteAtomId]

                        # @see: https://bmrb.io/ref_info/atom_nom.tbl
                        if self.__trust_bmrb_ref_info:
                            pass

                        # @see: https://bmrb.io/macro/files/xplor_to_iupac.Nov140620
                        else:
                            if compId == 'ASN':
                                if atomId == 'HD21':
                                    _atomId = atomId[:-1] + '2'
                                    if self.nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.nefT.get_valid_star_atom(compId, _atomId)[0]
                                elif atomId == 'HD22':
                                    _atomId = atomId[:-1] + '1'
                                    if self.nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.nefT.get_valid_star_atom(compId, _atomId)[0]
                            elif compId == 'GLN':
                                if atomId == 'HE21':
                                    _atomId = atomId[:-1] + '2'
                                    if self.nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.nefT.get_valid_star_atom(compId, _atomId)[0]
                                elif atomId == 'HE22':
                                    _atomId = atomId[:-1] + '1'
                                    if self.nefT.validate_comp_atom(compId, _atomId):
                                        atomIds = self.nefT.get_valid_star_atom(compId, _atomId)[0]

                        if coordAtomSite is not None\
                           and not any(True for _atomId in atomIds if _atomId in atomSiteAtomId):
                            if atomId in atomSiteAtomId:
                                atomIds = [atomId]
                            elif 'alt_atom_id' in _factor:
                                altAtomId_ex = toNefEx(toRegEx(_factor['alt_atom_id']))
                                _atomIds_ = [_atomId for _atomId in atomSiteAtomId if re.match(altAtomId_ex, _atomId)]
                                if len(_atomIds_) > 0:
                                    atomIds = _atomIds_
                            elif seqId == 1 and atomId == 'H1' and self.csStat.peptideLike(compId) and 'H' in atomSiteAtomId:
                                atomIds = ['H']

                        if atomId.startswith('CEN') and len(atomIds) == 1:
                            peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(compId)
                            atomIds = self.csStat.getCentroidAtoms(compId, False, peptide, nucleotide, carbohydrate)

                        has_nx_local = has_nx_anchor = False

                        if self.cur_subtype in ('dist', 'pcs', 'pre', 'prdc', 'pccr')\
                           and (atomId in XPLOR_NITROXIDE_NAMES
                                or (isinstance(origAtomId, list) and origAtomId[0] in XPLOR_NITROXIDE_NAMES)
                                or (_atomId in LANTHANOID_ELEMENTS and atomSpecified
                                    and coordAtomSite is not None and atomId not in atomSiteAtomId
                                    and ('alt_atom_id' not in _factor
                                         or not ('%' in _factor['alt_atom_id'] or '*' in _factor['alt_atom_id'] or '#' in _factor['alt_atom_id'])))):
                            self.has_nx = has_nx_local = has_nx_anchor = _factor['has_nitroxide'] = True
                            desc = '(attaching point for for nitroxide spin label)'
                            if _atomId == 'GD':
                                self.has_gd = _factor['has_gd3+'] = True
                                desc = '(attaching point for Gd3+ spin label)'
                            elif _atomId in LANTHANOID_ELEMENTS:
                                self.has_la = _factor['has_lanthanide'] = True
                                desc = f'(attaching point for {_atomId.title()}3+ spin label)'
                            if compId == 'CYS':
                                atomIds = ['SG']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'SER':
                                atomIds = ['OG']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'GLU':
                                atomIds = ['OE2']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'ASP':
                                atomIds = ['OD2']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'GLN':
                                atomIds = ['NE2']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'ASN':
                                atomIds = ['ND2']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'LYS':
                                atomIds = ['NZ']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'THR':
                                atomIds = ['OG1']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'HIS':
                                atomIds = ['NE2']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId in ('ILE', 'LEU'):
                                atomIds = ['CD1']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'MET':
                                atomIds = ['CE']
                                _factor['alt_atom_id'] = atomIds[0] + desc
                            elif compId == 'R1A':
                                atomIds = ['O1']
                                desc = '(nitroxide spin label)'
                            elif compId == '3X9':
                                atomIds = ['OAH']
                                desc = '(nitroxide spin label)'
                            else:
                                has_nx_anchor = False
                                desc = '(nitroxide spin label)'
                            self.spinLabeling = desc

                        if coordAtomSite is not None and compId != coordAtomSite['comp_id'] and any(_atomId not in atomSiteAtomId for _atomId in atomIds):
                            atomIds = self.getAtomIdList(_factor, coordAtomSite['comp_id'], _atomId)

                        for _atomId in atomIds:
                            ccdCheck = not cifCheck

                            if cifCheck:
                                _atom = None
                                if coordAtomSite is not None:
                                    if _atomId in atomSiteAtomId:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                        _atom['type_symbol'] = coordAtomSite['type_symbol'][atomSiteAtomId.index(_atomId)]
                                    elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in atomSiteAtomId
                                                                               or ('H' + _atomId[-1]) in atomSiteAtomId):
                                        _atomId = _atomId[-1] + 'HN' if _atomId[-1] + 'HN' in atomSiteAtomId else 'H' + _atomId[-1]
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                        _atom['type_symbol'] = coordAtomSite['type_symbol'][atomSiteAtomId.index(_atomId)]
                                    elif 'alt_atom_id' in coordAtomSite and _atomId in coordAtomSite['alt_atom_id']:
                                        _atom = {}
                                        _atom['comp_id'] = coordAtomSite['comp_id']
                                        _atom['type_symbol'] = coordAtomSite['type_symbol'][coordAtomSite['alt_atom_id'].index(_atomId)]
                                        self.authAtomId = 'auth_atom_id'
                                    elif self.preferAuthSeq and atomSpecified:
                                        may_exist = False
                                        if self.ccU.updateChemCompDict(compId):
                                            cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                            if cca is not None and cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                                may_exist = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck, asis=False)
                                        if _coordAtomSite is not None and not may_exist:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            skip = self.with_axis and self.__multiPolymer and not all('identical_chain_id' in ps for ps in self.polySeq)
                                            if _atomId in _coordAtomSite['atom_id']\
                                               or (has_nx_local and not has_nx_anchor):
                                                if (self.cur_subtype != 'dist' and not self.in_noe)\
                                                   or (has_nx_local and not has_nx_anchor and _compId in NITROOXIDE_ANCHOR_RES_NAMES):
                                                    if skip:
                                                        pass
                                                    else:
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                elif _atomId in _coordAtomSite['atom_id']:
                                                    # _atom = {}
                                                    # _atom['comp_id'] = _compId
                                                    # _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                    if self.ccU.updateChemCompDict(compId):
                                                        cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                        if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                            if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['label_seq_scheme'] = {}
                                                            if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                            elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                                                       or ('H' + _atomId[-1]) in _coordAtomSite['atom_id']):
                                                _atomId = _atomId[-1] + 'HN' if _atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + _atomId[-1]
                                                if (self.cur_subtype != 'dist' and not self.in_noe)\
                                                   or (has_nx_local and not has_nx_anchor and _compId in NITROOXIDE_ANCHOR_RES_NAMES):
                                                    if skip:
                                                        pass
                                                    else:
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                else:
                                                    _atom = {}
                                                    _atom['comp_id'] = _compId
                                                    _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                    if self.ccU.updateChemCompDict(compId):
                                                        cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                        if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                            if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['label_seq_scheme'] = {}
                                                            if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                if (self.cur_subtype != 'dist' and not self.in_noe)\
                                                   or (has_nx_local and not has_nx_anchor and _compId in NITROOXIDE_ANCHOR_RES_NAMES):
                                                    if skip:
                                                        pass
                                                    else:
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                else:
                                                    _atom = {}
                                                    _atom['comp_id'] = _compId
                                                    _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                    if self.ccU.updateChemCompDict(compId):
                                                        cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                        if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                            if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['label_seq_scheme'] = {}
                                                            if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                    elif _seqId_ in ps['auth_seq_id'] and atomSpecified\
                                            and (self.reasons is None or 'label_seq_scheme' not in self.reasons
                                                 or self.reasons['label_seq_scheme'] is None
                                                 or self.cur_subtype not in self.reasons['label_seq_scheme']
                                                 or not self.reasons['label_seq_scheme'][self.cur_subtype]):
                                        self.preferAuthSeq = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId_, cifCheck=cifCheck)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if self.__lenAtomSelectionSet > 0:
                                                    self.setLocalSeqScheme()
                                            elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                                                       or ('H' + _atomId[-1]) in _coordAtomSite['atom_id']):
                                                _atomId = _atomId[-1] + 'HN' if _atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + _atomId[-1]
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if self.__lenAtomSelectionSet > 0:
                                                    self.setLocalSeqScheme()
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                                self.authAtomId = 'auth_atom_id'
                                                seqKey = _seqKey
                                                chainId, seqId = seqKey
                                                if self.__lenAtomSelectionSet > 0:
                                                    self.setLocalSeqScheme()
                                            elif not self.__extendAuthSeq:
                                                self.preferAuthSeq = False
                                        elif not self.__extendAuthSeq:
                                            self.preferAuthSeq = False

                                elif self.preferAuthSeq and atomSpecified:
                                    if self.__lenAtomSelectionSet == 0:
                                        may_exist = False
                                        if self.ccU.updateChemCompDict(compId):
                                            cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                            if cca is not None and cca[self.ccU.ccaLeavingAtomFlag] != 'Y':
                                                may_exist = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCheck=cifCheck, asis=False)
                                        if _coordAtomSite is not None and not may_exist:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                # _atom = {}
                                                # _atom['comp_id'] = _compId
                                                # _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                if self.ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                            self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                            elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                                                       or ('H' + _atomId[-1]) in _coordAtomSite['atom_id']):
                                                _atomId = _atomId[-1] + 'HN' if _atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + _atomId[-1]
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                if self.ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                            self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                if self.ccU.updateChemCompDict(compId):
                                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                    if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                        if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                            self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                elif _seqId_ in ps['auth_seq_id'] and atomSpecified:
                                    if self.__lenAtomSelectionSet == 0\
                                       and (self.reasons is None or 'label_seq_scheme' not in self.reasons
                                            or self.reasons['label_seq_scheme'] is None
                                            or self.cur_subtype not in self.reasons['label_seq_scheme']
                                            or not self.reasons['label_seq_scheme'][self.cur_subtype]):
                                        self.preferAuthSeq = True
                                        _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId_, cifCheck=cifCheck)
                                        if _coordAtomSite is not None:
                                            _compId = _coordAtomSite['comp_id']
                                            _atomId = self.getAtomIdList(_factor, _compId, atomId)[0]
                                            if _atomId in _coordAtomSite['atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                            elif _atomId in ('HN1', 'HN2', 'HN3') and ((_atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                                                       or ('H' + _atomId[-1]) in _coordAtomSite['atom_id']):
                                                _atomId = _atomId[-1] + 'HN' if _atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + _atomId[-1]
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                            elif 'alt_atom_id' in _coordAtomSite and _atomId in _coordAtomSite['alt_atom_id']:
                                                _atom = {}
                                                _atom['comp_id'] = _compId
                                                _atom['type_symbol'] = _coordAtomSite['type_symbol'][_coordAtomSite['alt_atom_id'].index(_atomId)]
                                                self.authSeqId = 'auth_seq_id'
                                                self.authAtomId = 'auth_atom_id'
                                            elif not self.__extendAuthSeq:
                                                self.preferAuthSeq = False
                                        elif not self.__extendAuthSeq:
                                            self.preferAuthSeq = False

                                if _atom is not None:
                                    _compIdList = None if 'comp_id' not in _factor else [translateToStdResName(_compId, ccU=self.ccU) for _compId in _factor['comp_id']]
                                    if ('comp_id' not in _factor or _atom['comp_id'] in _compIdList)\
                                       and ('type_symbol' not in _factor or _atom['type_symbol'] in _factor['type_symbol']):
                                        selection = {'chain_id': chainId, 'seq_id': seqId, 'comp_id': _atom['comp_id'], 'atom_id': _atomId, 'is_poly': isPolySeq}
                                        if 'alt_chain_id' in _factor and not self.cur_union_expr:
                                            selection['segment_id'] = _factor['alt_chain_id']
                                        if len(self.__cur_auth_atom_id) > 0:
                                            selection['auth_atom_id'] = self.__cur_auth_atom_id
                                        if not atomSpecified or not seqSpecified:
                                            if self.ccU.updateChemCompDict(compId):
                                                cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                                if cca is None or (cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y'):
                                                    if atomSiteAtomId is None or _atomId not in atomSiteAtomId:
                                                        continue
                                        _atomSelection.append(selection)
                                else:
                                    ccdCheck = True

                            if (len(_factor['chain_id']) > 1 or len(_factor['seq_id']) > 1 or not isPolySeq) and not atomSpecified:
                                continue

                            if isPolySeq and 'ambig_auth_seq_id' in ps and _seqId in ps['ambig_auth_seq_id']:
                                continue

                            if not isPolySeq and 'alt_auth_seq_id' in ps and _seqId in ps['auth_seq_id'] and _seqId not in ps['alt_auth_seq_id']:
                                continue

                            if isinstance(origAtomId, str) and origAtomId.startswith('*'):
                                continue

                            origAtomId0 = origAtomId[0] if isinstance(origAtomId, list) else origAtomId

                            if isPolySeq and len(_factor['chain_id']) > 1 and self.con_union_expr:  # D_1300057999: verify if another polymer can take over in union expression
                                hasAltPolymer = False
                                for chainId1, chainId2 in itertools.combinations(_factor['chain_id'], 2):
                                    ps1 = next((ps for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['auth_chain_id'] == chainId1), None)
                                    if ps1 is not None:
                                        if 'identical_auth_chain_id' in ps1 and chainId2 in ps1['identical_auth_chain_id']:
                                            continue
                                    ps2 = next((ps for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['auth_chain_id'] == chainId2), None)
                                    if ps2 is not None and ps1['comp_id'] != ps2['comp_id']:
                                        hasAltPolymer = True
                                        break
                                if hasAltPolymer:
                                    hasAltPolymer = False
                                    for chainId2 in _factor['chain_id']:
                                        if chainId2 == chainId:
                                            continue
                                        ps2 = next((ps for ps in (self.polySeq if isPolySeq else altPolySeq) if ps['auth_chain_id'] == chainId2), None)
                                        if ps2 is None or ('identical_auth_chain_id' in ps2 and chainId in ps2['identical_auth_chain_id']):
                                            continue
                                        if seqId in ps2['auth_seq_id']:
                                            _, _coordAtomSite = self.getCoordAtomSiteOf(chainId2, seqId, cifCheck=cifCheck)
                                            if _coordAtomSite is not None:
                                                _atomSiteAtomId = _coordAtomSite['atom_id']
                                                if origAtomId0 in _atomSiteAtomId:
                                                    hasAltPolymer = True
                                                    break
                                                _compId = ps2['comp_id'][ps2['auth_seq_id'].index(seqId)]
                                                _origAtomId0 = translateToStdAtomName(origAtomId0, _compId, _atomSiteAtomId, self.ccU, False)
                                                __origAtomId0, _, details = self.nefT.get_valid_star_atom(_compId, _origAtomId0, leave_unmatched=True)
                                                if details is None and __origAtomId0[0] in _atomSiteAtomId:
                                                    hasAltPolymer = True
                                                    break
                                    if hasAltPolymer:
                                        continue

                            if ccdCheck and compId is not None and _atomId not in XPLOR_RDC_PRINCIPAL_AXIS_NAMES and _atomId not in XPLOR_NITROXIDE_NAMES:
                                _compIdList = None if 'comp_id' not in _factor else [translateToStdResName(_compId, ccU=self.ccU) for _compId in _factor['comp_id']]
                                if self.ccU.updateChemCompDict(compId) and ('comp_id' not in _factor or compId in _compIdList):
                                    if len(origAtomId) > 1:
                                        typeSymbols = set()
                                        for _atomId_ in origAtomId:
                                            typeSymbol = next((cca[self.ccU.ccaTypeSymbol] for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId_), None)
                                            if typeSymbol is not None:
                                                typeSymbols.add(typeSymbol)
                                                if len(typeSymbols) > 1:
                                                    break
                                        if len(typeSymbols) > 1:
                                            continue
                                    cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == _atomId), None)
                                    if cca is not None and cca[self.ccU.ccaLeavingAtomFlag] == 'Y' and (not atomSpecified or not seqSpecified):
                                        continue
                                    if cca is not None and ('type_symbol' not in _factor or cca[self.ccU.ccaTypeSymbol] in _factor['type_symbol']):
                                        selection = {'chain_id': chainId, 'seq_id': seqId, 'comp_id': compId, 'atom_id': _atomId, 'is_poly': isPolySeq}
                                        if 'alt_chain_id' in _factor and not self.cur_union_expr:
                                            selection['segment_id'] = _factor['alt_chain_id']
                                        if len(self.__cur_auth_atom_id) > 0:
                                            selection['auth_atom_id'] = self.__cur_auth_atom_id
                                        if _atomId.startswith('HOP') and isinstance(origAtomId, str) and '*' in origAtomId:
                                            continue
                                        if not seqSpecified:
                                            continue
                                        _atomSelection.append(selection)
                                        if cifCheck and seqKey not in self.__coordUnobsRes and self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                                            if self.cur_subtype != 'plane' and coordAtomSite is not None:
                                                checked = False
                                                if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or seqId == min(auth_seq_id_list):
                                                    if coordAtomSite is not None and ((_atomId in aminoProtonCode and 'H1' in atomSiteAtomId)
                                                                                      or _atomId == 'P' or _atomId.startswith('HOP')):
                                                        checked = True
                                                if _atomId[0] in protonBeginCode:
                                                    bondedTo = self.ccU.getBondedAtoms(compId, _atomId)
                                                    if len(bondedTo) > 0 and bondedTo[0][0] != 'P':
                                                        if coordAtomSite is not None and bondedTo[0] in atomSiteAtomId:
                                                            if cca[self.ccU.ccaLeavingAtomFlag] != 'Y'\
                                                               or (self.csStat.peptideLike(compId)
                                                                   and cca[self.ccU.ccaNTerminalAtomFlag] == 'N'
                                                                   and cca[self.ccU.ccaCTerminalAtomFlag] == 'N'):
                                                                checked = True
                                                                if len(origAtomId) == 1:
                                                                    _atomSelection[-1]['hydrogen_not_instantiated'] = True
                                                                    self.f.append(f"[Hydrogen not instantiated] {self.getCurrentRestraint()}"
                                                                                  f"{chainId}:{seqId}:{compId}:{origAtomId0} is not properly instantiated in the coordinates. "
                                                                                  "Please re-upload the model file.")
                                                        elif bondedTo[0][0] == 'O':
                                                            checked = True
                                                if seqId == max(auth_seq_id_list) or (chainId, seqId + 1) in self.__coordUnobsRes and self.csStat.peptideLike(compId):
                                                    if coordAtomSite is not None and _atomId in carboxylCode\
                                                       and not isCyclicPolymer(self.cR, self.polySeq, chainId, self.representativeModelId,
                                                                               self.representativeAltId, self.modelNumName):
                                                        self.f.append(f"[Coordinate issue] {self.getCurrentRestraint()}"
                                                                      f"{chainId}:{seqId}:{compId}:{origAtomId0} is not properly instantiated in the coordinates. "
                                                                      "Please re-upload the model file.")
                                                        checked = True

                                                if not checked and not self.cur_union_expr:
                                                    if chainId in LARGE_ASYM_ID:
                                                        if isPolySeq and not self.preferAuthSeq\
                                                           and ('label_seq_offset' not in self.reasonsForReParsing
                                                                or chainId not in self.reasonsForReParsing['label_seq_offset']):
                                                            if self.csStat.peptideLike(compId) and origAtomId0 in aminoProtonCode\
                                                               and (self.has_nx and compId == 'PRO') or origAtomId0.startswith('HT'):
                                                                pass
                                                            else:
                                                                if 'label_seq_offset' not in self.reasonsForReParsing:
                                                                    self.reasonsForReParsing['label_seq_offset'] = {}
                                                                offset = self.getLabelSeqOffsetDueToUnobs(ps)
                                                                self.reasonsForReParsing['label_seq_offset'][chainId] = offset
                                                                if offset != 0:
                                                                    if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                        self.reasonsForReParsing['label_seq_scheme'] = {}
                                                                    if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                        self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                        if self.monoPolymer\
                                                           and (seqId < 1
                                                                or (compId == 'ACE' and seqId == min(self.polySeq[0]['auth_seq_id']) - 1)
                                                                or (compId == 'NH2' and seqId == max(self.polySeq[0]['auth_seq_id']) + 1)):
                                                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                                          f"{chainId}:{seqId}:{compId}:{origAtomId0} is not present in the coordinates. "
                                                                          f"The residue number '{seqId}' is not present in polymer sequence "
                                                                          f"of chain {chainId} of the coordinates. "
                                                                          "Please update the sequence in the Macromolecules page.")
                                                            if 'alt_chain_id' in _factor:
                                                                self.__failure_chain_ids.append(chainId)
                                                        else:
                                                            if len(chainIds) > 1 and isPolySeq and not self.__extendAuthSeq and not self.with_axis:
                                                                __preferAuthSeq = self.preferAuthSeq
                                                                self.preferAuthSeq = False
                                                                for __chainId in chainIds:
                                                                    if __chainId == chainId:
                                                                        continue
                                                                    __psList = [__ps for __ps in (self.polySeq if isPolySeq else altPolySeq)
                                                                                if __ps['auth_chain_id'] == __chainId]
                                                                    if len(__psList) == 0:
                                                                        continue
                                                                    for __ps in __psList:
                                                                        __seqId = self.getRealSeqId(__ps, seqId, isPolySeq)[0]
                                                                        _, __coordAtomSite = self.getCoordAtomSiteOf(__chainId, __seqId, cifCheck=cifCheck)
                                                                        if __coordAtomSite is not None\
                                                                           and ((seqId in ps['auth_seq_id'] and ps['seq_id'][ps['auth_seq_id'].index(seqId)] != seqId)  # 2lr1, 2lqc
                                                                                or seqId != __seqId):  # 1qkg
                                                                            __compId = __coordAtomSite['comp_id']
                                                                            __atomIds = self.getAtomIdList(_factor, __compId, atomId)
                                                                            if compId != __compId and __atomIds[0] in __coordAtomSite['atom_id']:
                                                                                if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                                    self.reasonsForReParsing['label_seq_scheme'] = {}
                                                                                if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                                    self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                                                if isChainSpecified:
                                                                                    if 'inhibit_label_seq_scheme' not in self.reasonsForReParsing:
                                                                                        self.reasonsForReParsing['inhibit_label_seq_scheme'] = {}
                                                                                    if chainId not in self.reasonsForReParsing['inhibit_label_seq_scheme']:
                                                                                        self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId] = {}
                                                                                    self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId][self.cur_subtype] = True
                                                                                break
                                                                self.preferAuthSeq = __preferAuthSeq
                                                            if isPolySeq and not isChainSpecified and seqSpecified and len(_factor['chain_id']) == 1\
                                                               and _factor['chain_id'][0] != chainId and compId in monDict3:
                                                                continue
                                                            if self.with_para and len(origAtomId0) >= 2 and origAtomId0[:2].upper() in LANTHANOID_ELEMENTS:
                                                                continue
                                                            if self.csStat.peptideLike(compId) and origAtomId0 in aminoProtonCode:
                                                                if (self.has_nx and compId == 'PRO') or origAtomId0.startswith('HT'):
                                                                    _atomSelection.remove(selection)
                                                                    continue
                                                                if self.has_nx:
                                                                    continue
                                                            if self.cur_subtype == 'dihed' and _atomId == 'P' and self.csStat.getTypeOfCompId(compId)[1]:
                                                                continue
                                                            warn_title = 'Anomalous data' if self.preferAuthSeq and compId == 'PRO' and origAtomId0 in aminoProtonCode\
                                                                and (seqId != 1 and (chainId, seqId - 1) not in self.__coordUnobsRes and seqId != min(auth_seq_id_list))\
                                                                else 'Atom not found'
                                                            if seqKey in self.__coordUnobsAtom\
                                                               and (_atomId in self.__coordUnobsAtom[seqKey]['atom_ids']
                                                                    or (_atomId[0] in protonBeginCode
                                                                        and any(True for bondedTo in self.ccU.getBondedAtoms(compId, _atomId, exclProton=True)
                                                                                if bondedTo in self.__coordUnobsAtom[seqKey]['atom_ids']))):
                                                                warn_title = 'Coordinate issue'
                                                            if (compId == 'ASP' and _atomId == 'HD1') or (compId == 'GLU' and _atomId == 'HE1'):
                                                                warn_title = 'Hydrogen not instantiated'
                                                            self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                                                          f"{chainId}:{seqId}:{compId}:{origAtomId0} is not present in the coordinates.")
                                                            if warn_title in ('Coordinate issue', 'Hydrogen not instantiated'):
                                                                _atomSelection.append(selection)
                                                                continue
                                                            if 'alt_chain_id' in _factor:
                                                                self.__failure_chain_ids.append(chainId)
                                    elif cca is None and 'type_symbol' not in _factor and 'atom_ids' not in _factor:
                                        if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes or seqId == min(auth_seq_id_list):
                                            if coordAtomSite is not None and ((_atomId in aminoProtonCode and 'H1' in atomSiteAtomId)
                                                                              or _atomId == 'P' or _atomId.startswith('HOP')):
                                                continue
                                        if cifCheck and self.cur_subtype != 'plane'\
                                           and 'seq_id' in _factor and len(_factor['seq_id']) == 1\
                                           and (self.reasons is None or 'non_poly_remap' not in self.reasons)\
                                           and not self.cur_union_expr:
                                            if chainId in LARGE_ASYM_ID:
                                                if self.monoPolymer\
                                                   and (seqId < 1
                                                        or (compId == 'ACE' and seqId == min(self.polySeq[0]['auth_seq_id']) - 1)
                                                        or (compId == 'NH2' and seqId == max(self.polySeq[0]['auth_seq_id']) + 1)):
                                                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                                                  f"{chainId}:{seqId}:{compId}:{origAtomId0} is not present in the coordinates. "
                                                                  f"The residue number '{seqId}' is not present in polymer sequence "
                                                                  f"of chain {chainId} of the coordinates. "
                                                                  "Please update the sequence in the Macromolecules page.")
                                                    if 'alt_chain_id' in _factor:
                                                        self.__failure_chain_ids.append(chainId)
                                                elif seqSpecified:
                                                    if resolved and altPolySeq is not None:
                                                        continue
                                                    if len(chainIds) > 1 and isPolySeq and not self.__extendAuthSeq and not self.with_axis:
                                                        __preferAuthSeq = self.preferAuthSeq
                                                        self.preferAuthSeq = False
                                                        for __chainId in chainIds:
                                                            if __chainId == chainId:
                                                                continue
                                                            __psList = [__ps for __ps in (self.polySeq if isPolySeq else altPolySeq)
                                                                        if __ps['auth_chain_id'] == __chainId]
                                                            if len(__psList) == 0:
                                                                continue
                                                            for __ps in __psList:
                                                                __seqId = self.getRealSeqId(__ps, seqId, isPolySeq)[0]
                                                                _, __coordAtomSite = self.getCoordAtomSiteOf(__chainId, __seqId, cifCheck=cifCheck)
                                                                if __coordAtomSite is not None\
                                                                   and ((seqId in ps['auth_seq_id'] and ps['seq_id'][ps['auth_seq_id'].index(seqId)] != seqId)  # 2lr1, 2lqc
                                                                        or seqId != __seqId):  # 1qkg
                                                                    __compId = __coordAtomSite['comp_id']
                                                                    __atomIds = self.getAtomIdList(_factor, __compId, atomId)
                                                                    if compId != __compId and __atomIds[0] in __coordAtomSite['atom_id']\
                                                                       and self.csStat.getTypeOfCompId(compId) == self.csStat.getTypeOfCompId(__compId):  # 2ld5
                                                                        if 'label_seq_scheme' not in self.reasonsForReParsing:
                                                                            self.reasonsForReParsing['label_seq_scheme'] = {}
                                                                        if self.cur_subtype not in self.reasonsForReParsing['label_seq_scheme']:
                                                                            self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True
                                                                            if 'segment_id' in _factor and 'assert_label_scheme_scheme' not in self.reasonsForReParsing:
                                                                                self.reasonsForReParsing['assert_label_seq_scheme'] = True  # 2m0k
                                                                        if isChainSpecified:
                                                                            if 'inhibit_label_seq_scheme' not in self.reasonsForReParsing:
                                                                                self.reasonsForReParsing['inhibit_label_seq_scheme'] = {}
                                                                            if chainId not in self.reasonsForReParsing['inhibit_label_seq_scheme']:
                                                                                self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId] = {}
                                                                            self.reasonsForReParsing['inhibit_label_seq_scheme'][chainId][self.cur_subtype] = True
                                                                        break
                                                        self.preferAuthSeq = __preferAuthSeq
                                                    if isPolySeq and not isChainSpecified and seqSpecified and len(_factor['chain_id']) == 1\
                                                       and _factor['chain_id'][0] != chainId and compId in monDict3:
                                                        continue
                                                    # 2mgt
                                                    if self.hasNonPoly and len(_factor['seq_id']) == 1 and len(_factor['atom_id']) == 1:
                                                        if _atomId in self.__uniqAtomIdToSeqKey:  # 7jk8
                                                            if 'np_atom_id_remap' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['np_atom_id_remap'] = {}
                                                            if _atomId not in self.reasonsForReParsing['np_atom_id_remap']:
                                                                self.reasonsForReParsing['np_atom_id_remap'][_atomId] = self.__uniqAtomIdToSeqKey[_atomId]
                                                        _coordAtomSite = None
                                                        ligands = 0
                                                        for np in self.__nonPoly:
                                                            if np['auth_chain_id'] == chainId and atomId == np['comp_id'][0]:
                                                                ligands += len(np['seq_id'])
                                                        if ligands == 0:
                                                            for np in self.__nonPoly:
                                                                if 'alt_comp_id' in np and np['auth_chain_id'] == chainId and atomId == np['alt_comp_id'][0]:
                                                                    ligands += len(np['seq_id'])
                                                        if ligands == 0:
                                                            for np in self.__nonPoly:
                                                                _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], np['seq_id'][0], cifCheck=cifCheck)
                                                                if _coordAtomSite is not None and atomId in _coordAtomSite['atom_id']:
                                                                    ligands += len(np['seq_id'])
                                                        if ligands == 1:
                                                            checked = False
                                                            if 'np_seq_id_remap' not in self.reasonsForReParsing:
                                                                self.reasonsForReParsing['np_seq_id_remap'] = {}
                                                            srcSeqId = _factor['seq_id'][0]
                                                            for np in self.__nonPoly:
                                                                if atomId == np['comp_id'][0]\
                                                                   or ('alt_comp_id' in np and atomId == np['alt_comp_id'][0]):
                                                                    dstSeqId = np['seq_id'][0]
                                                                    if chainId not in self.reasonsForReParsing['np_seq_id_remap']:
                                                                        self.reasonsForReParsing['np_seq_id_remap'][chainId] = {}
                                                                    if srcSeqId in self.reasonsForReParsing['np_seq_id_remap'][chainId]:
                                                                        if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] is not None:
                                                                            if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] != dstSeqId:
                                                                                self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = None
                                                                            else:
                                                                                checked = True
                                                                    else:
                                                                        self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = dstSeqId
                                                                        checked = True
                                                            for np in self.__nonPoly:
                                                                if _coordAtomSite is not None and atomId in _coordAtomSite['atom_id']:
                                                                    dstSeqId = np['seq_id'][0]
                                                                    if chainId not in self.reasonsForReParsing['np_seq_id_remap']:
                                                                        self.reasonsForReParsing['np_seq_id_remap'][chainId] = {}
                                                                    if srcSeqId in self.reasonsForReParsing['np_seq_id_remap'][chainId]:
                                                                        if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] is not None:
                                                                            if self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] != dstSeqId:
                                                                                self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = None
                                                                            else:
                                                                                checked = True
                                                                    else:
                                                                        self.reasonsForReParsing['np_seq_id_remap'][chainId][srcSeqId] = dstSeqId
                                                                        checked = True
                                                            if checked and isPolySeq and (self.reasons is None
                                                                                          or (self.reasons is not None and 'np_seq_id_remap' in self.reasons)):
                                                                continue
                                                        # 2n3r
                                                        elif ligands > 1 and isPolySeq and self.reasons is not None and 'np_seq_id_remap' in self.reasons\
                                                                and retrieveRemappedSeqId(self.reasons['np_seq_id_remap'], chainId, seqId)[0] is not None:
                                                            continue
                                                    if extSeqScheme:
                                                        self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                                                      f"The residue '{seqId}:{compId}' is not present in polymer sequence "
                                                                      f"of chain {chainId} of the coordinates. "
                                                                      "Please update the sequence in the Macromolecules page.")
                                                        if 'expected_comp_id' not in _factor:
                                                            _factor['expected_comp_id'] = [compId]
                                                        if compId not in _factor['expected_comp_id']:
                                                            _factor['expected_comp_id'].append(compId)
                                                        continue
                                                    # 5t1n: SANI -> PCS
                                                    if self.cur_subtype == 'rdc' and self.__lenAtomSelectionSet == 4 and\
                                                       compId in NITROOXIDE_ANCHOR_RES_NAMES\
                                                       and len(origAtomId0) >= 2 and origAtomId0[:2].upper() in PARAMAGNETIC_ELEMENTS:
                                                        self.paramagCenter = copy.copy(_factor)
                                                        self.paramagCenter['atom_id'][0] = origAtomId0[:2].upper()
                                                        continue
                                                    if self.with_para and len(origAtomId0) >= 2 and origAtomId0[:2].upper() in LANTHANOID_ELEMENTS:
                                                        continue
                                                    if self.csStat.peptideLike(compId) and origAtomId0 in aminoProtonCode:
                                                        if self.has_nx or origAtomId0.startswith('HT'):
                                                            continue
                                                    if self.cur_subtype == 'dihed' and _atomId == 'P' and self.csStat.getTypeOfCompId(compId)[1]:
                                                        continue
                                                    warn_title = 'Anomalous data' if self.preferAuthSeq and compId == 'PRO' and origAtomId0 in aminoProtonCode\
                                                        and (seqId != 1 and (chainId, seqId - 1) not in self.__coordUnobsRes and seqId != min(auth_seq_id_list))\
                                                        else 'Atom not found'
                                                    if seqKey in self.__coordUnobsAtom\
                                                       and (_atomId in self.__coordUnobsAtom[seqKey]['atom_ids']
                                                            or (_atomId[0] in protonBeginCode
                                                                and any(True for bondedTo in self.ccU.getBondedAtoms(compId, _atomId, exclProton=True)
                                                                        if bondedTo in self.__coordUnobsAtom[seqKey]['atom_ids']))):
                                                        warn_title = 'Coordinate issue'
                                                    if (compId == 'ASP' and _atomId == 'HD1') or (compId == 'GLU' and _atomId == 'HE1'):
                                                        warn_title = 'Hydrogen not instantiated'
                                                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                                                  f"{chainId}:{seqId}:{compId}:{origAtomId0} is not present in the coordinates.")
                                                    if warn_title in ('Coordinate issue', 'Hydrogen not instantiated'):
                                                        continue
                                                    if self.cur_subtype == 'dist' and isPolySeq and isChainSpecified and compId in monDict3 and self.csStat.peptideLike(compId):
                                                        self.checkDistSequenceOffset(chainId, seqId, compId, origAtomId0)
                                                    if 'alt_chain_id' in _factor:
                                                        self.__failure_chain_ids.append(chainId)

        return foundCompId

    @functools.lru_cache(maxsize=128)
    def getRealCompId(self, compId: str) -> str:
        if self.ccU.updateChemCompDict(compId, False):
            if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS' and '_chem_comp.pdbx_replaced_by' in self.ccU.lastChemCompDict:
                replacedBy = self.ccU.lastChemCompDict['_chem_comp.pdbx_replaced_by']
                if replacedBy not in emptyValue and self.ccU.updateChemCompDict(replacedBy):
                    return replacedBy
        return compId

    def getOrigSeqId(self, ps: dict, seqId: int, isPolySeq: bool = True) -> Optional[int]:
        offset = 0
        if not self.preferAuthSeq:
            chainId = ps['chain_id']
            if isPolySeq and self.reasons is not None and 'label_seq_offset' in self.reasons\
               and chainId in self.reasons['label_seq_offset']:
                offset = self.reasons['label_seq_offset'][chainId]
            if isPolySeq and self.reasons is not None and 'global_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_sequence_offset']:
                offset = self.reasons['global_sequence_offset'][ps['auth_chain_id']]
            if isPolySeq and self.reasons is not None and 'global_auth_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_auth_sequence_offset']:
                offset = self.reasons['global_auth_sequence_offset'][ps['auth_chain_id']]
                if isinstance(offset, dict):
                    if seqId in offset:
                        offset = offset[seqId]
                    else:
                        for shift in range(1, 100):
                            if seqId + shift in offset:
                                offset = offset[seqId + shift]
                                break
                            if seqId - shift in offset:
                                offset = offset[seqId - shift]
                                break
                        if isinstance(offset, dict):
                            return None
                if seqId + offset in ps['auth_seq_id']:
                    return seqId + offset
                if offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                    for shift in range(1, 100):
                        if seqId + shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(seqId + shift + offset) - shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx]
                        if seqId - shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(seqId - shift + offset) + shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx]
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId + offset)
            if seqKey in self.__labelToAuthSeq:
                _, _seqId = self.__labelToAuthSeq[seqKey]
                return _seqId
            if seqKey[1] in ps['seq_id']:
                return ps['auth_seq_id'][ps['seq_id'].index(seqKey[1])]
        else:
            if isPolySeq and self.reasons is not None and 'global_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_sequence_offset']:
                offset = self.reasons['global_sequence_offset'][ps['auth_chain_id']]
            if isPolySeq and self.reasons is not None and 'global_auth_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_auth_sequence_offset']:
                offset = self.reasons['global_auth_sequence_offset'][ps['auth_chain_id']]
                if isinstance(offset, dict):
                    if seqId in offset:
                        offset = offset[seqId]
                    else:
                        for shift in range(1, 100):
                            if seqId + shift in offset:
                                offset = offset[seqId + shift]
                                break
                            if seqId - shift in offset:
                                offset = offset[seqId - shift]
                                break
                        if isinstance(offset, dict):
                            return None
        if seqId + offset in ps['auth_seq_id']:
            return seqId + offset
        if offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
            for shift in range(1, 100):
                if seqId + shift + offset in ps['auth_seq_id']:
                    idx = ps['auth_seq_id'].index(seqId + shift + offset) - shift
                    if 0 <= idx < len(ps['auth_seq_id']):
                        return ps['auth_seq_id'][idx]
                if seqId - shift + offset in ps['auth_seq_id']:
                    idx = ps['auth_seq_id'].index(seqId - shift + offset) + shift
                    if 0 <= idx < len(ps['auth_seq_id']):
                        return ps['auth_seq_id'][idx]
        return seqId

    def getRealSeqId(self, ps: dict, seqId: int, isPolySeq: bool = True) -> Tuple[Optional[int], Optional[str], bool]:
        offset = 0
        preferLabelSeq = False
        if self.reasons is not None and 'segment_id_mismatch' in self.reasons and 'segment_id_match_stats' in self.reasons:
            for k, v in self.reasons['segment_id_mismatch'].items():
                if v == ps['auth_chain_id'] and 'identical_auth_chain_id' not in ps:  # prevent unexpected sequence scheme switch (6l8v)
                    if k in self.reasons['segment_id_match_stats']:
                        if v in self.reasons['segment_id_match_stats'][k] and self.reasons['segment_id_match_stats'][k][v] == 0:
                            # no hope for auth sequence scheme (2mnz)
                            preferLabelSeq = True
                            break
        inhibitLabelSeq = self.reasons is not None and 'inhibit_label_seq_scheme' in self.reasons\
            and ps['auth_chain_id'] in self.reasons['inhibit_label_seq_scheme']
        if (not self.preferAuthSeq or preferLabelSeq) and not inhibitLabelSeq:
            chainId = ps['chain_id']
            if isPolySeq and self.reasons is not None and 'label_seq_offset' in self.reasons\
               and chainId in self.reasons['label_seq_offset']:
                offset = self.reasons['label_seq_offset'][chainId]
            if isPolySeq and self.reasons is not None and 'global_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_sequence_offset']:
                offset = self.reasons['global_sequence_offset'][ps['auth_chain_id']]
            if isPolySeq and self.reasons is not None and 'global_auth_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_auth_sequence_offset']:
                offset = self.reasons['global_auth_sequence_offset'][ps['auth_chain_id']]
                if isinstance(offset, dict):
                    if seqId in offset:
                        offset = offset[seqId]
                    else:
                        for shift in range(1, 100):
                            if seqId + shift in offset:
                                offset = offset[seqId + shift]
                                break
                            if seqId - shift in offset:
                                offset = offset[seqId - shift]
                                break
                        if isinstance(offset, dict):
                            return None, None, False
                if seqId + offset in ps['auth_seq_id']:
                    return seqId + offset, ps['comp_id'][ps['auth_seq_id'].index(seqId + offset)], False
                if offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
                    for shift in range(1, 100):
                        if seqId + shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(seqId + shift + offset) - shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx], ps['comp_id'][idx], False
                        if seqId - shift + offset in ps['auth_seq_id']:
                            idx = ps['auth_seq_id'].index(seqId - shift + offset) + shift
                            if 0 <= idx < len(ps['auth_seq_id']):
                                return ps['auth_seq_id'][idx], ps['comp_id'][idx], False
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId + offset)
            if seqKey in self.__labelToAuthSeq:
                _, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _seqId, ps['comp_id'][ps['seq_id'].index(seqId + offset)
                                                 if seqId + offset in ps['seq_id']
                                                 else ps['auth_seq_id'].index(_seqId)], False
                if seqKey[1] in ps['seq_id']:  # resolve conflict between label/auth sequence schemes of polymer/non-polymer (2l90)
                    idx = ps['seq_id'].index(seqKey[1])
                    return ps['auth_seq_id'][idx], ps['comp_id'][idx], False
        else:
            if isPolySeq and self.reasons is not None and 'global_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_sequence_offset']:
                offset = self.reasons['global_sequence_offset'][ps['auth_chain_id']]
            if isPolySeq and self.reasons is not None and 'global_auth_sequence_offset' in self.reasons\
               and ps['auth_chain_id'] in self.reasons['global_auth_sequence_offset']:
                offset = self.reasons['global_auth_sequence_offset'][ps['auth_chain_id']]
                if isinstance(offset, dict):
                    if seqId in offset:
                        offset = offset[seqId]
                    else:
                        for shift in range(1, 100):
                            if seqId + shift in offset:
                                offset = offset[seqId + shift]
                                break
                            if seqId - shift in offset:
                                offset = offset[seqId - shift]
                                break
                        if isinstance(offset, dict):
                            return None, None, False
        if seqId + offset in ps['auth_seq_id']:
            return seqId + offset, ps['comp_id'][ps['auth_seq_id'].index(seqId + offset)], False
        if self.reasons is not None and 'extend_seq_scheme' in self.reasons:
            _ps = next((_ps for _ps in self.reasons['extend_seq_scheme'] if _ps['chain_id'] == ps['auth_chain_id']), None)
            if _ps is not None:
                if seqId + offset in _ps['seq_id']:
                    return seqId + offset, _ps['comp_id'][_ps['seq_id'].index(seqId + offset)], True
        if offset != 0 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
            for shift in range(1, 100):
                if seqId + shift + offset in ps['auth_seq_id']:
                    idx = ps['auth_seq_id'].index(seqId + shift + offset) - shift
                    if 0 <= idx < len(ps['auth_seq_id']):
                        return ps['auth_seq_id'][idx], ps['comp_id'][idx], False
                if seqId - shift + offset in ps['auth_seq_id']:
                    idx = ps['auth_seq_id'].index(seqId - shift + offset) + shift
                    if 0 <= idx < len(ps['auth_seq_id']):
                        return ps['auth_seq_id'][idx], ps['comp_id'][idx], False
        return seqId, None, False

    @functools.lru_cache(maxsize=128)
    def getRealChainId(self, chainId: str, hint: str = None) -> str:
        if self.reasons is not None and 'segment_id_mismatch' in self.reasons and chainId in self.reasons['segment_id_mismatch']:
            _chainId = self.reasons['segment_id_mismatch'][chainId]
            if _chainId is not None:
                chainId = _chainId
        if hint is not None:
            if hint.isupper() != chainId.isupper() and hint == chainId.upper():
                chainId = hint
            if chainId.isdigit() and not hint.isdigit() and indexToLetter(int(chainId) - 1) == hint:
                chainId = hint
        return chainId

    def updateSegmentIdDict(self, factor: dict, chainId: str, isPolymer: Optional[bool], valid: bool):
        if self.reasons is not None or 'alt_chain_id' not in factor\
           or len(self.reasonsForReParsing) == 0 or 'segment_id_mismatch' not in self.reasonsForReParsing:
            return
        altChainId = factor['alt_chain_id']
        if altChainId not in self.reasonsForReParsing['segment_id_mismatch']:
            return
        if 'atom_id' in factor and len(factor['atom_id']) == 1 and self.__polyPeptide:  # 7lgi
            atomId = factor['atom_id'][0]
            if atomId in aminoProtonCode or atomId in carboxylCode or atomId in jcoupBbPairCode:
                if self.__polyDeoxyribonucleotide or self.__polyRibonucleotide or self.hasBranched:  # 2n8a, 4b1q (branched)
                    return
                if (self.cur_subtype == 'dist' or self.in_noe) and not valid:
                    return  # D_1300057999
        if chainId not in self.reasonsForReParsing['segment_id_match_stats'][altChainId]:
            self.reasonsForReParsing['segment_id_match_stats'][altChainId][chainId] = 0
            self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['polymer'] = 0
            self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['non-polymer'] = 0
        checked = False
        if not valid and chainId not in self.__failure_chain_ids and chainId in self.atomIdSetPerChain:
            if 'atom_id' in factor:
                for atomId in factor['atom_id']:
                    if atomId in self.atomIdSetPerChain[chainId]:
                        checked = True  # 7d3v
                        break
        if valid or checked:
            self.reasonsForReParsing['segment_id_match_stats'][altChainId][chainId] += 1
            if len(altChainId) < 3 and altChainId.startswith(chainId):
                self.reasonsForReParsing['segment_id_match_stats'][altChainId][chainId] += 1
            if isPolymer is not None:
                if isPolymer:
                    self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['polymer'] += 1
                else:
                    self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['non-poly'] += 1
        else:
            for _chainId in factor['chain_id']:
                if _chainId in self.__failure_chain_ids or not checked:
                    if _chainId not in self.reasonsForReParsing['segment_id_match_stats'][altChainId]:
                        self.reasonsForReParsing['segment_id_match_stats'][altChainId][_chainId] = 0
                        self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['polymer'] = 0
                        self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['non-poly'] = 0
                    self.reasonsForReParsing['segment_id_match_stats'][altChainId][_chainId] -= 1
                    if isPolymer is not None:
                        if isPolymer:
                            self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['polymer'] -= 1
                        else:
                            self.reasonsForReParsing['segment_id_poly_type_stats'][altChainId]['non-poly'] -= 1
        # try to avoid multiple segment_id assignments
        for k, _stats in self.reasonsForReParsing['segment_id_match_stats'].items():
            if k == altChainId:
                continue
            if chainId in _stats:
                _stats[chainId] -= 1
        stats = self.reasonsForReParsing['segment_id_match_stats'][altChainId]
        _chainId = max(stats, key=lambda key: stats[key])[0]
        _score = stats[_chainId]
        if _score > 0 or len(stats) == 1:  # 2mtk
            self.reasonsForReParsing['segment_id_mismatch'][altChainId] = _chainId
        elif _score < 0:
            __chainId = min(stats, key=lambda key: stats[key])[0]
            __score = stats[__chainId]
            if _score == __score and _chainId != __chainId and altChainId in self.reasonsForReParsing['segment_id_mismatch']:  # 2la5
                del self.reasonsForReParsing['segment_id_mismatch'][altChainId]  # 2lzs

    @functools.lru_cache(maxsize=2048)
    def getCoordAtomSiteOf(self, chainId: str, seqId: int, compId: Optional[str] = None, cifCheck: bool = True, asis: bool = True
                           ) -> Tuple[Tuple[str, int], Optional[dict]]:
        seqKey = (chainId, seqId)
        if asis:
            if cifCheck and compId is not None:
                _seqKey = (chainId, seqId, compId)
                if _seqKey in self.__coordAtomSite:
                    return seqKey, self.__coordAtomSite[_seqKey]
                if cifCheck and seqKey in self.__coordAtomSite:
                    _compId = self.__coordAtomSite[seqKey]['comp_id']
                    if compId == _compId:
                        return seqKey, self.__coordAtomSite[seqKey]
                    if self.hasNonPoly:
                        npList = [np for np in self.__nonPoly if np['auth_chain_id'] == chainId]
                        for np in npList:
                            if np['comp_id'][0] == compId and np['auth_seq_id'][0] == seqId:
                                _seqKey = (chainId, np['seq_id'][0])
                                if _seqKey in self.__coordAtomSite and self.__coordAtomSite[_seqKey]['comp_id'] == compId:
                                    return _seqKey, self.__coordAtomSite[_seqKey]
            return seqKey, self.__coordAtomSite[seqKey] if cifCheck and seqKey in self.__coordAtomSite else None
        if seqKey in self.__labelToAuthSeq:
            seqKey = self.__labelToAuthSeq[seqKey]
            if cifCheck and compId is not None:
                _seqKey = (seqKey[0], seqKey[1], compId)
                if _seqKey in self.__coordAtomSite:
                    return seqKey, self.__coordAtomSite[_seqKey]
            return seqKey, self.__coordAtomSite[seqKey] if cifCheck and seqKey in self.__coordAtomSite else None
        return seqKey, None

    def getAtomIdList(self, factor: dict, compId: str, atomId: str) -> List[str]:
        key = (compId, atomId, 'alt_atom_id' in factor)
        if key in self.__cachedDictForAtomIdList:
            return copy.copy(self.__cachedDictForAtomIdList[key])
        atomIds, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
        if self.cur_subtype not in ('dist', 'adist', 'plane', 'geo') and len(atomIds) > 1:
            if self.cur_subtype == 'dihed' and len(atomIds) == 2 and self.ccU.hasIntervenedAtom(compId, atomIds[0], atomIds[1]):
                return atomIds
            return [atomId]
        if details is not None and len(atomId) > 1 and not atomId[-1].isalpha()\
           and 'alt_atom_id' in factor and factor['alt_atom_id'][-1] not in ('%', '*', '#') and self.cur_subtype == 'dist':
            atomIds, _, details = self.nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)
            if atomId[-1].isdigit() and int(atomId[-1]) <= len(atomIds):
                atomIds = [atomIds[int(atomId[-1]) - 1]]

        if details is not None or atomId.endswith('"'):
            _atomId = toNefEx(translateToStdAtomName(atomId, compId, ccU=self.ccU, unambig=False))
            if _atomId != atomId:
                atomIds = self.nefT.get_valid_star_atom_in_xplor(compId, _atomId)[0]
        self.__cachedDictForAtomIdList[key] = atomIds
        return atomIds

    def getLabelSeqOffsetDueToUnobs(self, ps: dict) -> int:
        authChainId = ps['auth_chain_id']
        for labelSeqId, authSeqId in zip(ps['seq_id'], ps['auth_seq_id']):
            seqKey = (authChainId, authSeqId)
            if seqKey not in self.__coordUnobsRes:
                return labelSeqId - 1
        return max(list(filter(None, ps['seq_id']))) - 1

    def doesNonPolySeqIdMatchWithPolySeqUnobs(self, chainId: str, seqId: int) -> bool:
        _ps_ = next((_ps_ for _ps_ in self.polySeq if _ps_['auth_chain_id'] == chainId), None)
        if _ps_ is not None:
            _chainId_ = _ps_['chain_id']
            _seqKey_ = (_chainId_, seqId)
            if _seqKey_ in self.__labelToAuthSeq:
                if self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                    if self.__labelToAuthSeq[_seqKey_] in self.__coordUnobsRes:
                        return True
                else:
                    seq_id_list = list(filter(None, _ps_['seq_id']))
                    max_label_seq_id = max(seq_id_list)
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_label_seq_id:
                        if _seqId_ in _ps_['seq_id']:
                            _seqKey_ = (_chainId_, _seqId_)
                            if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                                break
                        _seqId_ += 1
                    if _seqId_ not in _ps_['seq_id']:
                        min_label_seq_id = min(seq_id_list)
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_label_seq_id:
                            if _seqId_ in _ps_['seq_id']:
                                _seqKey_ = (_chainId_, _seqId_)
                                if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                                    break
                            _seqId_ -= 1
                    if _seqId_ in _ps_['seq_id']:
                        _seqKey_ = (_chainId_, _seqId_)
                        if _seqKey_ in self.__labelToAuthSeq and self.__labelToAuthSeq[_seqKey_] != _seqKey_:
                            __chainId__, __seqId__ = self.__labelToAuthSeq[_seqKey_]
                            __seqKey__ = (__chainId__, __seqId__ - (_seqId_ - seqId))
                            if __seqKey__ in self.__coordUnobsRes:
                                return True
        return False

    def checkDistSequenceOffset(self, chainId: str, seqId: int, compId: str, origAtomId: str) -> bool:
        """ Try to find sequence offset.
        """

        if not self.hasPolySeq or self.cur_subtype != 'dist':
            return False

        ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)

        if ps is None:
            return False

        compIds = ps['comp_id']
        candidates = []

        for _compId in set(compIds):
            if compId == _compId:
                continue
            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(_compId, origAtomId)
            if len(_atomId) > 0 and details is None:
                candidates.append(_compId)

        if len(candidates) != 1:
            return False

        compId = candidates[0]

        idx_list = [idx for idx, _compId in enumerate(compIds) if _compId == compId]

        offsets = set(ps['auth_seq_id'][idx] - seqId for idx in idx_list)

        if 'global_sequence_offset' not in self.reasonsForReParsing:
            self.reasonsForReParsing['global_sequence_offset'] = {}
        if chainId in self.reasonsForReParsing['global_sequence_offset']:
            if self.reasonsForReParsing['global_sequence_offset'][chainId] is None:
                return False
            self.reasonsForReParsing['global_sequence_offset'][chainId] &= offsets
            if len(self.reasonsForReParsing['global_sequence_offset'][chainId]) == 0:
                self.reasonsForReParsing['global_sequence_offset'][chainId] = None
                return False
            return True

        self.reasonsForReParsing['global_sequence_offset'][chainId] = offsets

        return True

    def selectRealisticBondConstraint(self, atom1: str, atom2: str, alt_atom_id1: str, alt_atom_id2: str, dst_func: dict
                                      ) -> Tuple[str, str]:
        """ Return realistic bond constraint taking into account the current coordinates.
        """

        if not self.hasCoord:
            return atom1, atom2

        try:

            _p1 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom1['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p1) != 1:
                return atom1, atom2

            p1 = to_np_array(_p1[0])

            _p2 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom2['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p2) != 1:
                return atom1, atom2

            p2 = to_np_array(_p2[0])

            d_org = distance(p1, p2)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            if alt_atom_id1 is not None:

                _p1 =\
                    self.cR.getDictListWithFilter('atom_site',
                                                  CARTN_DATA_ITEMS,
                                                  [{'name': self.authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                                   {'name': self.authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                                   {'name': self.authAtomId, 'type': 'str', 'value': alt_atom_id1},
                                                   {'name': self.modelNumName, 'type': 'int',
                                                    'value': self.representativeModelId},
                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                    'enum': (self.representativeAltId,)}
                                                   ])

                if len(_p1) != 1:
                    return atom1, atom2

                p1_alt = to_np_array(_p1[0])

                d_alt = distance(p1_alt, p2)

                if dist_error(lower_limit, upper_limit, d_org) > dist_error(lower_limit, upper_limit, d_alt):
                    if 'auth_atom_id' not in atom1:
                        atom1['auth_atom_id'] = atom1['atom_id']
                    atom1['atom_id'] = alt_atom_id1

            elif alt_atom_id2 is not None:

                _p2 =\
                    self.cR.getDictListWithFilter('atom_site',
                                                  CARTN_DATA_ITEMS,
                                                  [{'name': self.authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                                   {'name': self.authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                                   {'name': self.authAtomId, 'type': 'str', 'value': alt_atom_id2},
                                                   {'name': self.modelNumName, 'type': 'int',
                                                    'value': self.representativeModelId},
                                                   {'name': 'label_alt_id', 'type': 'enum',
                                                    'enum': (self.representativeAltId,)}
                                                   ])

                if len(_p2) != 1:
                    return atom1, atom2

                p2_alt = to_np_array(_p2[0])

                d_alt = distance(p1, p2_alt)

                if dist_error(lower_limit, upper_limit, d_org) > dist_error(lower_limit, upper_limit, d_alt):
                    if 'auth_atom_id' not in atom2:
                        atom2['auth_atom_id'] = atom2['atom_id']
                    atom2['atom_id'] = alt_atom_id2

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+{self.__class_name__}.selectRealisticBondConstraint() ++ Error  - {str(e)}")

        return atom1, atom2

    def selectRealisticChi2AngleConstraint(self, atom1: str, atom2: str, atom3: str, atom4: str, dst_func: dict
                                           ) -> dict:
        """ Return realistic chi2 angle constraint taking into account the current coordinates.
        """

        if not self.hasCoord:
            return dst_func

        try:

            _p1 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom1['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p1) != 1:
                return dst_func

            p1 = to_np_array(_p1[0])

            _p2 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom2['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p2) != 1:
                return dst_func

            p2 = to_np_array(_p2[0])

            _p3 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom3['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom3['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom3['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p3) != 1:
                return dst_func

            p3 = to_np_array(_p3[0])

            _p4 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom4['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom4['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': 'CD1'},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p4) != 1:
                return dst_func

            p4 = to_np_array(_p4[0])

            chi2 = dihedral_angle(p1, p2, p3, p4)

            _p4 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom4['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom4['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': 'CD2'},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p4) != 1:
                return dst_func

            alt_p4 = to_np_array(_p4[0])

            alt_chi2 = dihedral_angle(p1, p2, p3, alt_p4)

            target_value = dst_func.get('target_value')
            if target_value is not None:
                target_value = float(target_value)
            target_value_uncertainty = dst_func.get('target_value_uncertainty')
            if target_value_uncertainty is not None:
                target_value_uncertainty = float(target_value_uncertainty)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            lower_linear_limit = dst_func.get('lower_linear_limit')
            if lower_linear_limit is not None:
                lower_linear_limit = float(lower_linear_limit)
            upper_linear_limit = dst_func.get('upper_linear_limit')
            if upper_linear_limit is not None:
                upper_linear_limit = float(upper_linear_limit)

            target_value, lower_bound, upper_bound =\
                angle_target_values(target_value, target_value_uncertainty,
                                    lower_limit, upper_limit,
                                    lower_linear_limit, upper_linear_limit)

            if target_value is None:
                return dst_func

            if angle_error(lower_bound, upper_bound, target_value, chi2) > angle_error(lower_bound, upper_bound, target_value, alt_chi2):
                target_value = dst_func.get('target_value')
                if target_value is not None:
                    target_value = float(target_value) + 180.0
                lower_limit = dst_func.get('lower_limit')
                if lower_limit is not None:
                    lower_limit = float(lower_limit) + 180.0
                upper_limit = dst_func.get('upper_limit')
                if upper_limit is not None:
                    upper_limit = float(upper_limit) + 180.0

                if lower_linear_limit is not None:
                    lower_linear_limit += 180.0
                if upper_linear_limit is not None:
                    upper_linear_limit += 180.0

                _array = numpy.array([target_value, lower_limit, upper_limit, lower_linear_limit, upper_linear_limit],
                                     dtype=float)

                shift = 0.0
                if self.__correctCircularShift:
                    if numpy.nanmin(_array) >= THRESHOLD_FOR_CIRCULAR_SHIFT:
                        shift = -(numpy.nanmax(_array) // 360) * 360
                    elif numpy.nanmax(_array) <= -THRESHOLD_FOR_CIRCULAR_SHIFT:
                        shift = -(numpy.nanmin(_array) // 360) * 360
                if target_value is not None:
                    dst_func['target_value'] = str(target_value + shift)
                if lower_limit is not None:
                    dst_func['lower_limit'] = str(lower_limit + shift)
                if upper_limit is not None:
                    dst_func['upper_limit'] = str(upper_limit + shift)
                if lower_linear_limit is not None:
                    dst_func['lower_linear_limit'] = str(lower_linear_limit + shift)
                if upper_linear_limit is not None:
                    dst_func['upper_linear_limit'] = str(upper_linear_limit + shift)

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+{self.__class_name__}.selectRealisticChi2AngleConstraint() ++ Error  - {str(e)}")

        return dst_func

    def isRealisticDistanceRestraint(self, atom1: str, atom2: str, dst_func: dict) -> bool:
        """ Return whether a given distance restraint is realistic in the assembly.
        """

        if not self.hasCoord:
            return True

        try:

            _p1 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom1['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom1['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom1['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p1) != 1:
                return True

            p1 = to_np_array(_p1[0])

            _p2 =\
                self.cR.getDictListWithFilter('atom_site',
                                              CARTN_DATA_ITEMS,
                                              [{'name': self.authAsymId, 'type': 'str', 'value': atom2['chain_id']},
                                               {'name': self.authSeqId, 'type': 'int', 'value': atom2['seq_id']},
                                               {'name': self.authAtomId, 'type': 'str', 'value': atom2['atom_id']},
                                               {'name': self.modelNumName, 'type': 'int',
                                                'value': self.representativeModelId},
                                               {'name': 'label_alt_id', 'type': 'enum',
                                                'enum': (self.representativeAltId,)}
                                               ])

            if len(_p2) != 1:
                return True

            p2 = to_np_array(_p2[0])

            d_org = distance(p1, p2)

            lower_limit = dst_func.get('lower_limit')
            if lower_limit is not None:
                lower_limit = float(lower_limit)
            upper_limit = dst_func.get('upper_limit')
            if upper_limit is not None:
                upper_limit = float(upper_limit)

            if dist_error(lower_limit, upper_limit, d_org) >= DIST_AMBIG_UP:
                return False

        except Exception as e:
            if self.__verbose:
                self.__lfh.write(f"+{self.__class_name__}.isRealisticDistanceRestraint() ++ Error  - {str(e)}")

        return True

    def getReadableFactor(self, factor: dict) -> str:
        """ Return human readable XPLOR-NIH/CNS/CHARMM/SCHRODINGER factor expression.
        """

        _factor = {k: sorted(list(set(v))) if isinstance(v, list) else v for k, v in factor.items()}

        key_order = ['chain_id', 'auth_chain_id', 'alt_chain_id', 'seq_id', 'comp_id', 'alt_comp_id', 'type_symbol', 'atom_id', 'alt_atom_id']

        key_map = {'chain_id': 'segidentifier',
                   'auth_chain_id': 'original segidentifier',
                   'alt_chain_id': 'original segidentifier',
                   'seq_id': 'residue',
                   'comp_id': 'resname',
                   'alt_comp_id': 'original resname',
                   'type_symbol': 'chemical',
                   'atom_id': 'name',
                   'alt_atom_id': 'original name'}

        if self.file_type == 'nm-res-sch':  # DAOTHER-10172: Schrodinger/ASL
            key_map = {'chain_id': 'chain.name',
                       'auth_chain_id': 'original chain.name',
                       'alt_chain_id': 'original chain.name',
                       'seq_id': 'residue.number',
                       'comp_id': 'residue.ptype',
                       'alt_comp_id': 'original residue.ptype',
                       'type_symbol': 'atom.element',
                       'atom_id': 'atom.ptype',
                       'alt_atom_id': 'original atom.ptype'}

        for k in _factor.keys():

            if k in key_map or k == 'is_poly':
                continue

            key_order.append(k)
            key_map[k] = k

        __factor = {}

        for k in key_order:

            if k not in _factor:
                continue

            v = _factor[k]

            if v in emptyValue or (isinstance(v, list) and (len(v) == 0 or v[0] in emptyValue)):
                continue

            if k == 'atom_id' and 'alt_atom_id' in _factor:
                _v = _factor['alt_atom_id']
                if _v in ('%', '*', '#') or (len(_v) == 2 and _v[-1] in ('%', '*', '#')) or (_v.startswith('HT') and len(v) > 1):
                    continue

            if k in ('chain_id', 'seq_id') and isinstance(v, list) and len(v) > 20:
                v = 'specified elsewhere or unspecified'

            if k in ('auth_chain_id', 'alt_chain_id'):
                if v == _factor['chain_id']:
                    continue

            if k == 'alt_comp_id' and 'comp_id' in _factor and v == _factor['comp_id']:
                continue

            if k == 'alt_atom_id' and v == _factor['atom_id']:
                continue

            __factor[key_map[k]] = (v if len(v) > 1 else v[0]) if isinstance(v, list) else v

        return str(__factor)

    def getReadableParamagCenter(self) -> str:
        """ Return human readable paramagnetic center.
        """

        _factor = {k: sorted(list(set(v))) if isinstance(v, list) else v for k, v in self.paramagCenter.items()}

        key_order = ['chain_id', 'seq_id', 'comp_id', 'alt_comp_id', 'atom_id', 'alt_atom_id']

        __factor = []

        for k in key_order:

            if k not in _factor:
                continue

            v = _factor[k]

            if v in emptyValue or (isinstance(v, list) and (len(v) == 0 or v[0] in emptyValue)):
                continue

            if k == 'atom_id' and 'alt_atom_id' in _factor:
                _v = _factor['alt_atom_id']
                if _v in ('%', '*', '#') or (len(_v) == 2 and _v[-1] in ('%', '*', '#')) or (_v.startswith('HT') and len(v) > 1):
                    continue

            if k in ('chain_id', 'seq_id') and isinstance(v, list) and len(v) > 20:
                continue

            __factor.append(str((v if len(v) > 1 else v[0]) if isinstance(v, list) else v))

            if k.startswith('alt'):
                __factor[-1] = f'({__factor[-1]})'

        return '/'.join(__factor)

    def getCurrentRestraint(self) -> str:
        if self.cur_subtype == 'dist' or (self.in_noe and self.cur_subtype_altered):  # resolve side effect derived from rdc -> dist type change (2ljb)
            return f"[Check the {self.distRestraints}th row of distance restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of dihedral angle restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'rdc':
            return f"[Check the {self.rdcRestraints}th row of residual dipolar coupling restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'plane':
            return f"[Check the {self.planeRestraints}th row of planarity restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'adist':
            return f"[Check the {self.adistRestraints}th row of antidistance restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'jcoup':
            return f"[Check the {self.jcoupRestraints}th row of scalar J-coupling restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'hvycs':
            return f"[Check the {self.hvycsRestraints}th row of carbon chemical shift restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'procs':
            return f"[Check the {self.procsRestraints}th row of proton chemical shift restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'rama':
            return f"[Check the {self.ramaRestraints}th row of dihedral angle database restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'radi':
            return f"[Check the {self.radiRestraints}th row of radius of gyration restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'diff':
            return f"[Check the {self.diffRestraints}th row of duffusion anisotropy restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'nbase':
            return f"[Check the {self.nbaseRestraints}th row of residue-residue position/orientation database restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'csa':
            return f"[Check the {self.csaRestraints}th row of (pseudo) chemical shift anisotropy restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'ang':
            return f"[Check the {self.angRestraints}th row of angle database restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'pre':
            return f"[Check the {self.preRestraints}th row of paramagnetic relaxation enhancement restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'pcs':
            return f"[Check the {self.pcsRestraints}th row of paramagnetic pseudocontact shift restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'prdc':
            return f"[Check the {self.prdcRestraints}th row of paramagnetic residual dipolar coupling restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'pang':
            return f"[Check the {self.pangRestraints}th row of paramagnetic orientation restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'pccr':
            return f"[Check the {self.pccrRestraints}th row of paramagnetic cross-correlation rate restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'hbond':
            return f"[Check the {self.hbondRestraints}th row of hydrogen bond geometry/database restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of harmonic coordinate/NCS restraints, {self.__def_err_sf_framecode}] "
        return ''

    def setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        if self.cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.distRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.dihedRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'rdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.rdcRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'plane':
            self.reasonsForReParsing['loca_seq_scheme'][(self.cur_subtype, self.planeRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'adist':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.adistRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'jcoup':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.jcoupRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'hvycs':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.hvycsRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'procs':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.procsRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'rama':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.ramaRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'radi':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.radiRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'diff':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.diffRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'nbase':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.nbaseRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'csa':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.csaRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'ang':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.angRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'pre':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.preRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'pcs':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.pcsRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'prdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.prdcRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'pang':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.pangRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'pccr':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.pccrRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'hbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.hbondRestraints)] = self.preferAuthSeq
        elif self.cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.geoRestraints)] = self.preferAuthSeq
        if not self.preferAuthSeq:
            self.__preferLabelSeqCount += 1
            if self.__preferLabelSeqCount > MAX_PREF_LABEL_SCHEME_COUNT:
                if 'label_seq_scheme' not in self.reasonsForReParsing:
                    self.reasonsForReParsing['label_seq_scheme'] = {}
                self.reasonsForReParsing['label_seq_scheme'][self.cur_subtype] = True

    def retrieveLocalSeqScheme(self):
        if self.reasons is None\
           or ('label_seq_scheme' not in self.reasons
               and 'local_seq_scheme' not in self.reasons
               and 'extend_seq_scheme' not in self.reasons):
            #    and 'inhibit_label_seq_scheme' not in self.reasons):
            return
        if 'extend_seq_scheme' in self.reasons:
            self.__extendAuthSeq = True
            if 'label_seq_scheme' not in self.reasons:  # 2joa
                self.preferAuthSeq = True
                self.authSeqId = 'label_seq_id'
            return
        if 'label_seq_scheme' in self.reasons and self.reasons['label_seq_scheme']:  # \
            # and 'segment_id_mismatch' not in self.reasons:
            if self.cur_subtype in self.reasons['label_seq_scheme']\
               and self.reasons['label_seq_scheme'][self.cur_subtype]:
                self.preferAuthSeq = False
                self.authSeqId = 'label_seq_id'
                return
            if self.cur_subtype != 'dist' and 'dist' in self.reasons['label_seq_scheme']\
               and self.reasons['label_seq_scheme']['dist']:
                self.preferAuthSeq = False
                self.authSeqId = 'label_seq_id'
                return
        if 'local_seq_scheme' not in self.reasons:
            return
        if self.cur_subtype == 'dist':
            key = (self.cur_subtype, self.distRestraints)
        elif self.cur_subtype == 'dihed':
            key = (self.cur_subtype, self.dihedRestraints)
        elif self.cur_subtype == 'rdc':
            key = (self.cur_subtype, self.rdcRestraints)
        elif self.cur_subtype == 'plane':
            key = (self.cur_subtype, self.planeRestraints)
        elif self.cur_subtype == 'adist':
            key = (self.cur_subtype, self.adistRestraints)
        elif self.cur_subtype == 'jcoup':
            key = (self.cur_subtype, self.jcoupRestraints)
        elif self.cur_subtype == 'hvycs':
            key = (self.cur_subtype, self.hvycsRestraints)
        elif self.cur_subtype == 'procs':
            key = (self.cur_subtype, self.procsRestraints)
        elif self.cur_subtype == 'rama':
            key = (self.cur_subtype, self.ramaRestraints)
        elif self.cur_subtype == 'radi':
            key = (self.cur_subtype, self.radiRestraints)
        elif self.cur_subtype == 'diff':
            key = (self.cur_subtype, self.diffRestraints)
        elif self.cur_subtype == 'nbase':
            key = (self.cur_subtype, self.nbaseRestraints)
        elif self.cur_subtype == 'csa':
            key = (self.cur_subtype, self.csaRestraints)
        elif self.cur_subtype == 'ang':
            key = (self.cur_subtype, self.angRestraints)
        elif self.cur_subtype == 'pre':
            key = (self.cur_subtype, self.preRestraints)
        elif self.cur_subtype == 'pcs':
            key = (self.cur_subtype, self.pcsRestraints)
        elif self.cur_subtype == 'prdc':
            key = (self.cur_subtype, self.prdcRestraints)
        elif self.cur_subtype == 'pang':
            key = (self.cur_subtype, self.pangRestraints)
        elif self.cur_subtype == 'pccr':
            key = (self.cur_subtype, self.pccrRestraints)
        elif self.cur_subtype == 'hbond':
            key = (self.cur_subtype, self.hbondRestraints)
        elif self.cur_subtype == 'geo':
            key = (self.cur_subtype, self.geoRestraints)
        else:
            return

        if key in self.reasons['local_seq_scheme']:
            self.preferAuthSeq = self.reasons['local_seq_scheme'][key]

    def addSf(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
              rdcCode: Optional[str] = None, alignCenter: Optional[str] = None):
        content_subtype = contentSubtypeOf(self.cur_subtype)

        if content_subtype is None:
            return

        self.__listIdCounter = incListIdCounter(self.cur_subtype, self.__listIdCounter)

        key = (self.cur_subtype, constraintType, potentialType, rdcCode, None if alignCenter is None else str(alignCenter))

        if key in self.sfDict:
            if len(self.sfDict[key]) > 0:
                decListIdCounter(self.cur_subtype, self.__listIdCounter)
                return
        else:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[content_subtype]

        restraint_name = getRestraintName(self.cur_subtype)

        software_name = self.software_name
        if self.file_type == 'nm-res-xpl' and self.cur_subtype not in ('dist', 'dihed', 'rdc', 'plane', 'jcoup', 'hvycs', 'procs', 'rama', 'diff', 'nbase', 'geo'):
            software_name = 'XPLOR-NIH'

        sf_framecode = f'{software_name}_' + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                          alignCenter=alignCenter)

        not_valid = True

        lp = getLoop(self.cur_subtype, hasInsCode=self.authToInsCode is not None)
        if not isinstance(lp, dict):
            sf.add_loop(lp)
            not_valid = False

        _restraint_name = restraint_name.split()

        item = {'file_type': self.file_type, 'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0,
                'constraint_type': ' '.join(_restraint_name[:-1]),
                'sf_framecode': sf_framecode}

        if not_valid:
            item['tags'] = []

        if self.cur_subtype == 'dist':
            item['constraint_subsubtype'] = 'simple'
            if constraintType is None:
                item['NOE_dist_averaging_method'] = self.noeAverage
            elif 'ROE' in constraintType:
                item['ROE_dist_averaging_method'] = self.noeAverage

        self.lastSfDict[self.cur_subtype] = item

        self.sfDict[key].append(item)

    def getSf(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
              rdcCode: Optional[str] = None, alignCenter: Optional[str] = None) -> dict:
        key = (self.cur_subtype, constraintType, potentialType, rdcCode, None if alignCenter is None else str(alignCenter))

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None or rdcCode is not None or alignCenter is not None:
                old_key = (self.cur_subtype, self.cur_constraint_type, None, None, None)
                if old_key in self.sfDict:
                    replaced = True
                    self.sfDict[key] = [self.sfDict[old_key].pop(-1)]
                    if len(self.sfDict[old_key]) == 0:
                        del self.sfDict[old_key]
                    sf = self.sfDict[key][-1]['saveframe']
                    idx = next((idx for idx, t in enumerate(sf.tags) if t[0] == 'Potential_type'), -1)
                    if idx != -1:
                        sf.tags[idx][1] = potentialType
                    else:
                        sf.add_tag('Potential_type', potentialType)
                    if rdcCode is not None:
                        idx = next((idx for idx, t in enumerate(sf.tags) if t[0] == 'Details'), -1)
                        if idx != -1:
                            sf.tags[idx][1] = rdcCode
                        else:
                            sf.add_tag('Details', rdcCode)
            elif constraintType is not None:
                old_key = (self.cur_subtype, None, None, None, None)
                if old_key in self.sfDict:
                    replaced = True
                    self.sfDict[key] = [self.sfDict[old_key].pop(-1)]
            if not replaced:
                self.addSf(constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                           alignCenter=alignCenter)

        self.cur_constraint_type = constraintType

        _key = next((_key for _key in self.sfDict if _key[0] == 'dist' and _key[1] is None), key) if self.cur_subtype == 'dist' else key
        self.__def_err_sf_framecode = self.sfDict[_key][-1]['sf_framecode']

        sf = self.sfDict[key][-1]

        if (self.classification not in emptyValue or self.with_para) and 'classification' not in sf:
            if get_first_sf_tag(sf['saveframe'], 'Details') in emptyValue:
                desc = ''
                if self.classification not in emptyValue:
                    desc = f'{self.classification},'
                if self.with_para and self.spinLabeling is not None:
                    desc += f' {self.spinLabeling[1:-1]}: {self.getReadableParamagCenter()}'
                desc = desc.strip()
                if desc not in emptyValue:
                    set_sf_tag(sf['saveframe'], 'Details', desc)
                sf['classification'] = desc

        return sf

    def trimSfWoLp(self):
        if self.cur_subtype not in self.lastSfDict:
            return
        if self.lastSfDict[self.cur_subtype]['index_id'] > 0:
            return
        for k, v in self.sfDict.items():
            for item in reversed(v):
                if item == self.lastSfDict:
                    v.remove(item)
                    if len(v) == 0:
                        del self.sfDict[k]
                    self.__listIdCounter = decListIdCounter(k[0], self.__listIdCounter)
                    return

    def getContentSubtype(self) -> dict:
        """ Return content subtype of the MR file.
        """

        if self.distStatements == 0 and self.distRestraints > 0:
            self.distStatements = 1

        if self.dihedStatements == 0 and self.dihedRestraints > 0:
            self.dihedStatements = 1

        if self.rdcStatements == 0 and self.rdcRestraints > 0:
            self.rdcStatements = 1

        if self.planeStatements == 0 and self.planeRestraints > 0:
            self.planeStatements = 1

        if self.adistStatements == 0 and self.adistRestraints > 0:
            self.adistStatements = 1

        if self.jcoupStatements == 0 and self.jcoupRestraints > 0:
            self.jcoupStatements = 1

        if self.hvycsStatements == 0 and self.hvycsRestraints > 0:
            self.hvycsStatements = 1

        if self.procsStatements == 0 and self.procsRestraints > 0:
            self.procsStatements = 1

        if self.ramaStatements == 0 and self.ramaRestraints > 0:
            self.ramaStatements = 1

        if self.radiStatements == 0 and self.radiRestraints > 0:
            self.radiStatements = 1

        if self.diffStatements == 0 and self.diffRestraints > 0:
            self.diffStatements = 1

        if self.nbaseStatements == 0 and self.nbaseRestraints > 0:
            self.nbaseStatements = 1

        if self.csaStatements == 0 and self.csaRestraints > 0:
            self.csaStatements = 1

        if self.angStatements == 0 and self.angRestraints > 0:
            self.angStatements = 1

        if self.preStatements == 0 and self.preRestraints > 0:
            self.preStatements = 1

        if self.pcsStatements == 0 and self.pcsRestraints > 0:
            self.pcsStatements = 1

        if self.prdcStatements == 0 and self.prdcRestraints > 0:
            self.prdcStatements = 1

        if self.pangStatements == 0 and self.pangRestraints > 0:
            self.pangStatements = 1

        if self.pccrStatements == 0 and self.pccrRestraints > 0:
            self.pccrStatements = 1

        if self.hbondStatements == 0 and self.hbondRestraints > 0:
            self.hbondStatements = 1

        if self.geoStatements == 0 and self.geoRestraints > 0:
            self.geoStatements = 1

        contentSubtype = {'dist_restraint': self.distStatements,
                          'dihed_restraint': self.dihedStatements,
                          'rdc_restraint': self.rdcStatements,
                          'plane_restraint': self.planeStatements,
                          'adist_restraint': self.adistStatements,
                          'jcoup_restraint': self.jcoupStatements,
                          'hvycs_restraint': self.hvycsStatements,
                          'procs_restraint': self.procsStatements,
                          'rama_restraint': self.ramaStatements,
                          'radi_restraint': self.radiStatements,
                          'diff_restraint': self.diffStatements,
                          'nbase_restraint': self.nbaseStatements,
                          'csa_restraint': self.csaStatements,
                          'ang_restraint': self.angStatements,
                          'pre_restraint': self.preStatements,
                          'pcs_restraint': self.pcsStatements,
                          'prdc_restraint': self.prdcStatements,
                          'pang_restraint': self.pangStatements,
                          'pccr_restraint': self.pccrStatements,
                          'hbond_restraint': self.hbondStatements,
                          'geo_restraint': self.geoStatements
                          }

        return {k: v for k, v in contentSubtype.items() if v > 0}

    def hasAnyRestraints(self) -> bool:
        """ Return whether any restraint is parsed successfully.
        """

        if self.__createSfDict:
            if len(self.sfDict) == 0:
                return False
            for v in self.sfDict.values():
                for item in v:
                    if item['index_id'] > 0:
                        return True
            return False
        return len(self.getContentSubtype()) > 0

    def getPolymerSequence(self) -> Optional[List[dict]]:
        """ Return polymer sequence of MR file.
        """

        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self) -> Optional[List[dict]]:
        """ Return sequence alignment between coordinates and MR.
        """

        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self) -> Optional[List[dict]]:
        """ Return chain assignment between coordinates and MR.
        """

        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self) -> Optional[dict]:
        """ Return reasons for re-parsing MR file.
        """

        return None if len(self.reasonsForReParsing) == 0 else self.reasonsForReParsing

    def getSfDict(self) -> Tuple[dict, Optional[dict]]:
        """ Return a dictionary of pynmrstar saveframes.
        """

        if len(self.sfDict) == 0:
            return self.__listIdCounter, None
        ign_keys = []
        for k, v in self.sfDict.items():
            for item in reversed(v):
                if item['index_id'] == 0:
                    v.remove(item)
                    if len(v) == 0:
                        ign_keys.append(k)
                    self.__listIdCounter = decListIdCounter(k[0], self.__listIdCounter)
        for k in ign_keys:
            del self.sfDict[k]
        return self.__listIdCounter, None if len(self.sfDict) == 0 else self.sfDict
