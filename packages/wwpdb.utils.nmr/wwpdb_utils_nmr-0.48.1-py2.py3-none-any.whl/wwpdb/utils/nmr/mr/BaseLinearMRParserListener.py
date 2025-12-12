##
# File: BaseLinearMRParserListener.py
# Date: 20-Oct-2025
#
# Updates:
""" ParserLister class for Generic Linear MR files.
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

from typing import IO, List, Tuple, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import (CifReader,
                                              SYMBOLS_ELEMENT)
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                                       extendCoordChainsForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomNameNoRef,
                                                       translateToStdAtomNameWithRef,
                                                       translateToStdAtomName,
                                                       translateToLigandName,
                                                       isCyclicPolymer,
                                                       isStructConn,
                                                       guessCompIdFromAtomId,
                                                       getMetalCoordOf,
                                                       getRestraintName,
                                                       contentSubtypeOf,
                                                       incListIdCounter,
                                                       decListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       MAX_ALLOWED_EXT_SEQ,
                                                       UNREAL_AUTH_SEQ_NUM,
                                                       THRESHOLD_FOR_CIRCULAR_SHIFT,
                                                       PLANE_LIKE_LOWER_LIMIT,
                                                       PLANE_LIKE_UPPER_LIMIT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR,
                                                       RDC_RESTRAINT_RANGE,
                                                       RDC_RESTRAINT_ERROR,
                                                       PCS_RESTRAINT_RANGE,
                                                       PCS_RESTRAINT_ERROR,
                                                       DIST_AMBIG_LOW,
                                                       DIST_AMBIG_MED,
                                                       DIST_AMBIG_UNCERT,
                                                       CYANA_MR_FILE_EXTS,
                                                       CARTN_DATA_ITEMS,
                                                       HEME_LIKE_RES_NAMES)
    from wwpdb.utils.nmr.nef.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (LARGE_ASYM_ID,
                                           monDict3,
                                           emptyValue,
                                           protonBeginCode,
                                           pseProBeginCode,
                                           aminoProtonCode,
                                           carboxylCode,
                                           zincIonCode,
                                           calciumIonCode,
                                           deepcopy,
                                           updatePolySeqRst,
                                           revertPolySeqRst,
                                           updatePolySeqRstAmbig,
                                           mergePolySeqRstAmbig,
                                           sortPolySeqRst,
                                           syncCompIdOfPolySeqRst,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           trimSequenceAlignment,
                                           retrieveAtomIdentFromMRMap,
                                           retrieveAtomIdFromMRMap,
                                           retrieveRemappedSeqId,
                                           retrieveRemappedSeqIdAndCompId,
                                           splitPolySeqRstForMultimers,
                                           splitPolySeqRstForExactNoes,
                                           retrieveRemappedChainId,
                                           splitPolySeqRstForNonPoly,
                                           retrieveRemappedNonPoly,
                                           splitPolySeqRstForBranched,
                                           retrieveOriginalSeqIdFromMRMap)
    from wwpdb.utils.nmr.NmrVrptUtility import (to_np_array,
                                                distance,
                                                dist_error,
                                                angle_target_values,
                                                dihedral_angle,
                                                angle_error)
except ImportError:
    from nmr.io.CifReader import (CifReader,
                                  SYMBOLS_ELEMENT)
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           extendCoordChainsForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomNameNoRef,
                                           translateToStdAtomNameWithRef,
                                           translateToStdAtomName,
                                           translateToLigandName,
                                           isCyclicPolymer,
                                           isStructConn,
                                           guessCompIdFromAtomId,
                                           getMetalCoordOf,
                                           getRestraintName,
                                           contentSubtypeOf,
                                           incListIdCounter,
                                           decListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           MAX_ALLOWED_EXT_SEQ,
                                           UNREAL_AUTH_SEQ_NUM,
                                           THRESHOLD_FOR_CIRCULAR_SHIFT,
                                           PLANE_LIKE_LOWER_LIMIT,
                                           PLANE_LIKE_UPPER_LIMIT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR,
                                           RDC_RESTRAINT_RANGE,
                                           RDC_RESTRAINT_ERROR,
                                           PCS_RESTRAINT_RANGE,
                                           PCS_RESTRAINT_ERROR,
                                           DIST_AMBIG_LOW,
                                           DIST_AMBIG_MED,
                                           DIST_AMBIG_UNCERT,
                                           CYANA_MR_FILE_EXTS,
                                           CARTN_DATA_ITEMS,
                                           HEME_LIKE_RES_NAMES)
    from nmr.nef.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (LARGE_ASYM_ID,
                               monDict3,
                               emptyValue,
                               protonBeginCode,
                               pseProBeginCode,
                               aminoProtonCode,
                               carboxylCode,
                               zincIonCode,
                               calciumIonCode,
                               deepcopy,
                               updatePolySeqRst,
                               revertPolySeqRst,
                               updatePolySeqRstAmbig,
                               mergePolySeqRstAmbig,
                               sortPolySeqRst,
                               syncCompIdOfPolySeqRst,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               trimSequenceAlignment,
                               retrieveAtomIdentFromMRMap,
                               retrieveAtomIdFromMRMap,
                               retrieveRemappedSeqId,
                               retrieveRemappedSeqIdAndCompId,
                               splitPolySeqRstForMultimers,
                               splitPolySeqRstForExactNoes,
                               retrieveRemappedChainId,
                               splitPolySeqRstForNonPoly,
                               retrieveRemappedNonPoly,
                               splitPolySeqRstForBranched,
                               retrieveOriginalSeqIdFromMRMap)
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


PCS_RANGE_MIN = PCS_RESTRAINT_RANGE['min_inclusive']
PCS_RANGE_MAX = PCS_RESTRAINT_RANGE['max_inclusive']

PCS_ERROR_MIN = PCS_RESTRAINT_ERROR['min_exclusive']
PCS_ERROR_MAX = PCS_RESTRAINT_ERROR['max_exclusive']


class BaseLinearMRParserListener():
    __slots__ = ('__class_name__',
                 '__version__',
                 '__verbose',
                 '__lfh',
                 'representativeModelId',
                 'representativeAltId',
                 '__mrAtomNameMapping',
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
                 'branched',
                 '__coordAtomSite',
                 '__coordUnobsRes',
                 '__coordUnobsAtom',
                 '__labelToAuthSeq',
                 'authToLabelSeq',
                 'authToStarSeq',
                 'authToOrigSeq',
                 'authToInsCode',
                 'authToEntityType',
                 '__modResidue',
                 '__splitLigand',
                 '__entityAssembly',
                 '__lenPolySeq',
                 '__monoPolymer',
                 '__multiPolymer',
                 '__lenNonPoly',
                 '__monoNonPoly',
                 'exptlMethod',
                 'fibril_chain_ids',
                 'offsetHolder',
                 'hasPolySeq',
                 'hasNonPoly',
                 '__hasBranched',
                 'hasNonPolySeq',
                 '__nonPolySeq',
                 'gapInAuthSeq',
                 'polyPeptide',
                 'polyDeoxyribonucleotide',
                 'polyRibonucleotide',
                 '__uniqAtomIdToSeqKey',
                 'csStat',
                 'nefT',
                 'pA',
                 'reasons',
                 '__preferAuthSeqCount',
                 '__preferLabelSeqCount',
                 'reasonsForReParsing',
                 'upl_or_lol',
                 'file_ext',
                 'max_dist_value',
                 'min_dist_value',
                 'dihed_lb_greater_than_ub',
                 'dihed_ub_always_positive',
                 'distRestraints',
                 'dihedRestraints',
                 'rdcRestraints',
                 'pcsRestraints',
                 'noepkRestraints',
                 'jcoupRestraints',
                 'geoRestraints',
                 'hbondRestraints',
                 'ssbondRestraints',
                 'fchiralRestraints',
                 'sfDict',
                 '__cachedDictForStarAtom',
                 '__chainNumberDict',
                 'extResKey',
                 '__polySeqRst',
                 '__polySeqRstFailed',
                 '__polySeqRstFailedAmbig',
                 '__compIdMap',
                 'f')

    file_type = ''
    software_name = ''

    __debug = False
    __remediate = False

    __createSfDict = False
    omitDistLimitOutlier = True
    allowZeroUpperLimit = False
    __correctCircularShift = True
    applyPdbStatCap = False

    cur_dist_type = ''
    local_dist_types = []  # list items must be one of ('upl', 'lol')

    # whether solid-state NMR is applied to symmetric samples such as fibrils
    symmetric = 'no'

    __shiftNonPosSeq = None

    __preferAuthSeq = True
    __extendAuthSeq = False

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    cur_subtype = ''

    # CYANA specific
    cur_subtype_altered = False

    # CYANA/ROSETTA specific
    cur_comment_inlined = False

    # CYANA specific
    cur_rdc_orientation = 0

    # column_order of distance restraints with chain
    col_order_of_dist_w_chain = {}

    # whether to allow extended sequence temporary
    allow_ext_seq = False

    # RDC parameter dictionary (CYANA specific)
    rdcParameterDict = None

    # PCS parameter dictionary (CYANA specific)
    pcsParameterDict = None

    # collection of atom selection
    atomSelectionSet = []

    # collection of number selection
    numberSelection = []

    # collection of auxiliary atom selection (CYANA/DYNAMO specific)
    auxAtomSelectionSet = ''

    # current residue name for atom name mapping (AMBER/CYANA specific)
    cur_resname_for_mapping = ''

    # unambigous atom name mapping (AMBER/ARIA/CYANA specific)
    unambigAtomNameMapping = {}

    # ambigous atom name mapping (AMBER/ARIA/CYANA specific)
    ambigAtomNameMapping = {}

    # collection of general residue number extended with chain code (CYANA/ROSETTA specific)
    genResNumSelection = []

    # collection of general simple name (CYANA/ROSETTA specific)
    genSimpleNameSelection = []

    # collection of general atom name extended with ambig code (CYANA specific)
    genAtomNameSelection = []

    # current Insight II restraint declaration (BIOSYM specific)
    cur_ins_decl = None

    # current boudary values (ARIA/BIOSYM/ISD specific)
    cur_lower_limit = None
    cur_upper_limit = None

    # current weight value (ARIA specific)
    cur_weight = 1.0

    # current target values (ARIA/XML specific)
    cur_target_value = None
    cur_target_value_uncertainty = None

    # collection of Insight II's atom selection (BIOSYM specific)
    insAtomSelection = []

    # internal sequence (DYNAMO specific)
    first_resid = 1
    cur_sequence = ''
    open_sequence = False
    has_sequence = False
    has_seq_align_err = False

    # collection of auxiliary atom selection (DYNAMO specific)
    auxAtomSelectionSet = []

    warningMessage = None

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
    __lastSfDict = {}

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None,
                 reasons: Optional[dict] = None, upl_or_lol: Optional[str] = None, file_ext: Optional[str] = None):
        self.__class_name__ = self.__class__.__name__
        self.__version__ = __version__

        self.__verbose = verbose
        self.__lfh = log

        self.representativeModelId = representativeModelId
        self.representativeAltId = representativeAltId
        self.__mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.cR = cR
        self.hasCoord = cR is not None

        self.nefT = nefT
        self.ccU = nefT.ccU
        self.csStat = nefT.csStat
        self.pA = nefT.pA

        self.polyPeptide = False
        self.polyDeoxyribonucleotide = False
        self.polyRibonucleotide = False

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
            self.branched = ret['branched']
            self.__coordAtomSite = ret['coord_atom_site']
            self.__coordUnobsRes = ret['coord_unobs_res']
            self.__coordUnobsAtom = ret['coord_unobs_atom'] if 'coord_unobs_atom' in ret else {}
            self.__labelToAuthSeq = ret['label_to_auth_seq']
            self.authToLabelSeq = ret['auth_to_label_seq']
            self.authToStarSeq = ret['auth_to_star_seq']
            self.authToOrigSeq = ret['auth_to_orig_seq']
            self.authToInsCode = ret['auth_to_ins_code']
            self.authToEntityType = ret['auth_to_entity_type']
            self.__modResidue = ret['mod_residue']
            self.__splitLigand = ret['split_ligand']
            self.__entityAssembly = ret['entity_assembly']

            self.__lenPolySeq = len(self.polySeq) if self.polySeq is not None else 0
            self.__monoPolymer = self.__lenPolySeq == 1
            self.__multiPolymer = self.__lenPolySeq > 1
            if self.__nonPoly is not None:
                self.__lenNonPoly = len(self.__nonPoly)
                self.__monoNonPoly = self.__lenNonPoly == 1

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
            self.branched = None
            self.__coordAtomSite = None
            self.__coordUnobsRes = None
            self.__coordUnobsAtom = None
            self.__labelToAuthSeq = None
            self.authToLabelSeq = None
            self.authToStarSeq = None
            self.authToOrigSeq = None
            self.authToInsCode = None
            self.authToEntityType = None
            self.__modResidue = None
            self.__splitLigand = None
            self.__entityAssembly = None

            self.__lenPolySeq = 0
            self.__monoPolymer = False
            self.__multiPolymer = False

        self.offsetHolder = {}

        self.hasPolySeq = self.polySeq is not None and self.__lenPolySeq > 0
        self.hasNonPoly = self.__nonPoly is not None and self.__lenNonPoly > 0
        self.__hasBranched = self.branched is not None and len(self.branched) > 0

        if self.hasNonPoly or self.__hasBranched:
            self.hasNonPolySeq = True
            if self.hasNonPoly and self.__hasBranched:
                self.__nonPolySeq = self.__nonPoly
                self.__nonPolySeq.extend(self.branched)
            elif self.hasNonPoly:
                self.__nonPolySeq = self.__nonPoly
            else:
                self.__nonPolySeq = self.branched

        else:
            self.hasNonPolySeq = False
            self.__nonPolySeq = None

        if self.hasPolySeq:
            self.gapInAuthSeq = self.hasPolySeq and any(True for ps in self.polySeq if 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq'])

            for entity in self.__entityAssembly:
                if 'entity_poly_type' in entity:
                    poly_type = entity['entity_poly_type']
                    if poly_type.startswith('polypeptide'):
                        self.polyPeptide = True
                    elif poly_type == 'polydeoxyribonucleotide':
                        self.polyDeoxyribonucleotide = True
                    elif poly_type == 'polyribonucleotide':
                        self.polyRibonucleotide = True

        else:
            self.gapInAuthSeq = False

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

        if reasons is not None and 'model_chain_id_ext' in reasons:
            self.polySeq, self.__altPolySeq, self.__coordAtomSite, self.__coordUnobsRes, \
                self.__labelToAuthSeq, self.authToLabelSeq, self.authToStarSeq, self.authToOrigSeq =\
                extendCoordChainsForExactNoes(reasons['model_chain_id_ext'],
                                              self.polySeq, self.__altPolySeq,
                                              self.__coordAtomSite, self.__coordUnobsRes,
                                              self.authToLabelSeq, self.authToStarSeq, self.authToOrigSeq)

        # reasons for re-parsing request from the previous trial
        self.reasons = reasons
        self.__preferAuthSeqCount = 0
        self.__preferLabelSeqCount = 0

        self.reasonsForReParsing = {}  # reset to prevent interference from the previous run

        self.upl_or_lol = upl_or_lol

        if upl_or_lol not in (None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl'):
            msg = f"The argument 'upl_or_lol' must be one of {(None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl')}"
            log.write(f"'+{self.__class_name__}.__init__() ++ ValueError  -  {msg}")
            raise ValueError(f"'+{self.__class_name__}.__init__() ++ ValueError  -  {msg}")

        self.file_ext = file_ext

        if file_ext not in CYANA_MR_FILE_EXTS:
            msg = f"The argument 'file_ext' must be one of {CYANA_MR_FILE_EXTS}"
            log.write(f"'+{self.__class_name__}.__init__() ++ ValueError  -  {msg}")
            raise ValueError(f"'+{self.__class_name__}.__init__() ++ ValueError  -  {msg}")

        if upl_or_lol is None and file_ext is not None:

            if file_ext == 'upl':
                self.upl_or_lol = 'upl_w_lol'

            if file_ext == 'lol':
                self.upl_or_lol = 'lol_w_upl'

        self.max_dist_value = DIST_ERROR_MIN
        self.min_dist_value = DIST_ERROR_MAX

        self.dihed_lb_greater_than_ub = False
        self.dihed_ub_always_positive = True

        self.distRestraints = 0      # Distance restraint file (.upl or .lol)
        self.dihedRestraints = 0     # Torsion angle restraint file (.aco)
        self.rdcRestraints = 0       # Residual dipolar coupling restraint file (.rdc)
        self.pcsRestraints = 0       # Pseudocontact shift restraint file (.pcs)
        self.noepkRestraints = 0     # NOESY volume restraint file (.upv or .lov)
        self.jcoupRestraints = 0     # Scalar coupling constant restraint file (.cco)
        self.geoRestraints = 0       # Coordinate geometry restraints
        self.hbondRestraints = 0     # Hydrogen bond geometry restraints
        self.ssbondRestraints = 0    # Disulfide bond geometry restraints
        self.fchiralRestraints = 0   # Floating chiral stereo assignments

        self.sfDict = {}  # dictionary of pynmrstar saveframes

        self.__cachedDictForStarAtom = {}

        # chain number dictionary
        self.__chainNumberDict = {}

        # extended residue key
        self.extResKey = []

        # polymer sequence of MR file
        self.__polySeqRst = []
        self.__polySeqRstFailed = []
        self.__polySeqRstFailedAmbig = []
        self.__compIdMap = {}

        self.f = []

    @property
    def verbose(self):
        return self.__verbose

    @property
    def log(self):
        return self.__lfh

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, debug: bool):
        self.__debug = debug

    @property
    def remediate(self):
        return self.__remediate

    @remediate.setter
    def remediate(self, remediate: bool):
        self.__remediate = remediate

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

        try:

            if self.hasPolySeq and self.__polySeqRst is not None:
                sortPolySeqRst(self.__polySeqRst,
                               None if self.reasons is None else self.reasons.get('non_poly_remap'))

                self.__seqAlign, _ = alignPolymerSequence(self.pA, self.polySeq, self.__polySeqRst,
                                                          resolvedMultimer=self.reasons is not None)
                self.__chainAssign, message = assignPolymerSequence(self.pA, self.ccU, self.file_type, self.polySeq, self.__polySeqRst, self.__seqAlign)

                if len(message) > 0:
                    self.f.extend(message)

                if self.__chainAssign is not None:

                    if self.__lenPolySeq == len(self.__polySeqRst):

                        chain_mapping = {}

                        for ca in self.__chainAssign:
                            ref_chain_id = ca['ref_chain_id']
                            test_chain_id = ca['test_chain_id']

                            if ref_chain_id != test_chain_id:
                                chain_mapping[test_chain_id] = ref_chain_id

                        if len(chain_mapping) == self.__lenPolySeq:

                            for ps in self.__polySeqRst:
                                if ps['chain_id'] in chain_mapping:
                                    ps['chain_id'] = chain_mapping[ps['chain_id']]

                            self.__seqAlign, _ = alignPolymerSequence(self.pA, self.polySeq, self.__polySeqRst,
                                                                      resolvedMultimer=self.reasons is not None)
                            self.__chainAssign, _ = assignPolymerSequence(self.pA, self.ccU, self.file_type, self.polySeq, self.__polySeqRst, self.__seqAlign)

                    trimSequenceAlignment(self.__seqAlign, self.__chainAssign)

                    if self.reasons is None and any(True for f in self.f
                                                    if '[Atom not found]' in f or '[Sequence mismatch]' in f or 'Invalid atom nomenclature' in f):

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
                            offset = None
                            for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                if test_seq_id is None:
                                    continue
                                if mid_code == '|':
                                    try:
                                        seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                           in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                           if seq_id == ref_seq_id and isinstance(auth_seq_id, int))
                                        if offset is None:
                                            offset = seq_id_mapping[test_seq_id] - test_seq_id
                                    except StopIteration:
                                        pass
                                elif mid_code == ' ' and test_seq_id in poly_seq_rst['seq_id']:
                                    idx = poly_seq_rst['seq_id'].index(test_seq_id)
                                    if poly_seq_rst['comp_id'][idx] == '.' and poly_seq_rst['auth_comp_id'][idx] not in emptyValue:
                                        seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                           in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                           if seq_id == ref_seq_id and isinstance(auth_seq_id, int))

                            if offset is not None and all(v - k == offset for k, v in seq_id_mapping.items()):
                                test_seq_id_list = list(seq_id_mapping.keys())
                                min_test_seq_id = min(test_seq_id_list)
                                max_test_seq_id = max(test_seq_id_list)
                                for test_seq_id in range(min_test_seq_id + 1, max_test_seq_id):
                                    if test_seq_id not in seq_id_mapping:
                                        seq_id_mapping[test_seq_id] = test_seq_id + offset

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
                            polySeqRst, chainIdMapping = splitPolySeqRstForMultimers(self.pA, self.polySeq, self.__polySeqRst, self.__chainAssign)

                            if polySeqRst is not None and (not self.hasNonPoly or self.__lenPolySeq // self.__lenNonPoly in (1, 2)):
                                self.__polySeqRst = polySeqRst
                                if 'chain_id_remap' not in self.reasonsForReParsing and len(chainIdMapping) > 0:
                                    self.reasonsForReParsing['chain_id_remap'] = chainIdMapping

                        if self.__monoPolymer and len(self.__polySeqRst) == 1:
                            polySeqRst, chainIdMapping, modelChainIdExt =\
                                splitPolySeqRstForExactNoes(self.pA, self.polySeq, self.__polySeqRst, self.__chainAssign)

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
                                else:
                                    for k, v in nonPolyMapping.items():
                                        if k not in self.reasonsForReParsing['non_poly_remap']:
                                            self.reasonsForReParsing['non_poly_remap'][k] = v
                                        else:
                                            for k2, v2 in v.items():
                                                if k2 not in self.reasonsForReParsing['non_poly_remap'][k]:
                                                    self.reasonsForReParsing['non_poly_remap'][k][k2] = v2

                        if self.__hasBranched:
                            polySeqRst, branchedMapping = splitPolySeqRstForBranched(self.pA, self.polySeq, self.branched, self.__polySeqRst,
                                                                                     self.__chainAssign)

                            if polySeqRst is not None:
                                self.__polySeqRst = polySeqRst
                                if 'branched_remap' not in self.reasonsForReParsing:
                                    self.reasonsForReParsing['branched_remap'] = branchedMapping

                        mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                        if len(self.__polySeqRstFailed) > 0:
                            sortPolySeqRst(self.__polySeqRstFailed)
                            if not any(True for f in self.f if '[Sequence mismatch]' in f):  # 2n6y
                                syncCompIdOfPolySeqRst(self.__polySeqRstFailed, self.__compIdMap)  # 2mx9

                            seqAlignFailed, _ = alignPolymerSequence(self.pA, self.polySeq, self.__polySeqRstFailed)

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
                                            _seqAlignFailed, _ = alignPolymerSequence(self.pA, self.polySeq, _polySeqRstFailed)
                                            _sa = next((_sa for _sa in _seqAlignFailed if _sa['test_chain_id'] == chainId), None)
                                            if _sa is None or _sa['conflict'] > 0:
                                                continue
                                            if _sa['matched'] > _matched:
                                                _matched = _sa['matched']
                                                _compId = compId
                                        if _compId is not None:
                                            updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, _compId)
                                            sortPolySeqRst(self.__polySeqRstFailed)

                            seqAlignFailed, _ = alignPolymerSequence(self.pA, self.polySeq, self.__polySeqRstFailed)
                            chainAssignFailed, _ = assignPolymerSequence(self.pA, self.ccU, self.file_type,
                                                                         self.polySeq, self.__polySeqRstFailed, seqAlignFailed)

                            if chainAssignFailed is not None:
                                seqIdRemapFailed = []

                                uniq_ps = not any(True for ps in self.polySeq if 'identical_chain_id' in ps)

                                for ca in chainAssignFailed:
                                    if ca['conflict'] > 0:
                                        continue
                                    ref_chain_id = ca['ref_chain_id']
                                    test_chain_id = ca['test_chain_id']

                                    sa = next((sa for sa in seqAlignFailed
                                               if sa['ref_chain_id'] == ref_chain_id
                                               and sa['test_chain_id'] == test_chain_id), None)

                                    if sa is None or sa['sequence_coverage'] < 0.0:
                                        continue

                                    poly_seq_model = next(ps for ps in self.polySeq
                                                          if ps['auth_chain_id'] == ref_chain_id)

                                    seq_id_mapping = {}
                                    for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                                        if test_seq_id is None:
                                            continue
                                        if mid_code == '|':
                                            try:
                                                seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                                   in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                                   if seq_id == ref_seq_id and isinstance(auth_seq_id, int))
                                            except StopIteration:
                                                if uniq_ps:
                                                    seq_id_mapping[test_seq_id] = ref_seq_id

                                    offset = None
                                    offsets = [v - k for k, v in seq_id_mapping.items()]
                                    if len(offsets) > 0 and ('gap_in_auth_seq' not in poly_seq_model or not poly_seq_model['gap_in_auth_seq']):
                                        offsets = collections.Counter(offsets).most_common()
                                        if len(offsets) > 1:
                                            offset = offsets[0][0]
                                            for k, v in seq_id_mapping.items():
                                                if v - k != offset:
                                                    seq_id_mapping[k] = k + offset

                                    if uniq_ps and offset is not None and len(seq_id_mapping) > 0\
                                       and ('gap_in_auth_seq' not in poly_seq_model or not poly_seq_model['gap_in_auth_seq']):
                                        for ref_seq_id, mid_code, test_seq_id, ref_code, test_code in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id'],
                                                                                                          sa['ref_code'], sa['test_code']):
                                            if test_seq_id is None:
                                                continue
                                            if mid_code == '|' and test_seq_id not in seq_id_mapping:
                                                seq_id_mapping[test_seq_id] = test_seq_id + offset
                                            elif ref_code != '.' and test_code == '.':
                                                seq_id_mapping[test_seq_id] = test_seq_id + offset

                                    if any(True for k, v in seq_id_mapping.items() if k != v)\
                                       and not any(True for k, v in seq_id_mapping.items()
                                                   if v in poly_seq_model['seq_id']
                                                   and k == poly_seq_model['auth_seq_id'][poly_seq_model['seq_id'].index(v)]):
                                        seqIdRemapFailed.append({'chain_id': ref_chain_id, 'seq_id_dict': seq_id_mapping,
                                                                 'comp_id_set': list(set(poly_seq_model['comp_id']))})

                                if len(seqIdRemapFailed) > 0:
                                    if 'chain_seq_id_remap' not in self.reasonsForReParsing:
                                        seqIdRemap = self.reasonsForReParsing['seq_id_remap'] if 'seq_id_remap' in self.reasonsForReParsing else []
                                        if len(seqIdRemap) != len(seqIdRemapFailed)\
                                           or seqIdRemap[0]['chain_id'] != seqIdRemapFailed[0]['chain_id']\
                                           or not all(src_seq_id in seqIdRemap[0] for src_seq_id in seqIdRemapFailed[0]):
                                            self.reasonsForReParsing['chain_seq_id_remap'] = seqIdRemapFailed

                                else:
                                    for ps in self.__polySeqRstFailed:
                                        for ca in self.__chainAssign:
                                            ref_chain_id = ca['ref_chain_id']
                                            test_chain_id = ca['test_chain_id']

                                            if test_chain_id != ps['chain_id']:
                                                continue

                                            sa = next(sa for sa in self.__seqAlign
                                                      if sa['ref_chain_id'] == ref_chain_id
                                                      and sa['test_chain_id'] == test_chain_id)

                                            if len(sa['test_seq_id']) != len(sa['ref_seq_id']):
                                                continue

                                            poly_seq_model = next(ps for ps in self.polySeq
                                                                  if ps['auth_chain_id'] == ref_chain_id)

                                            seq_id_mapping, comp_id_mapping = {}, {}

                                            for seq_id, comp_id in zip(ps['seq_id'], ps['comp_id']):
                                                if seq_id in sa['test_seq_id']:
                                                    idx = sa['test_seq_id'].index(seq_id)
                                                    auth_seq_id = sa['ref_seq_id'][idx]
                                                    seq_id_mapping[seq_id] = auth_seq_id
                                                    comp_id_mapping[seq_id] = comp_id
                                            if any(True for k, v in seq_id_mapping.items() if k != v)\
                                               or ('label_seq_scheme' not in self.reasonsForReParsing
                                                   and all(v not in poly_seq_model['auth_seq_id'] for v in seq_id_mapping.values())):
                                                seqIdRemapFailed.append({'chain_id': ref_chain_id, 'seq_id_dict': seq_id_mapping,
                                                                         'comp_id_dict': comp_id_mapping})

                                    if len(seqIdRemapFailed) > 0:
                                        if 'ext_chain_seq_id_remap' not in self.reasonsForReParsing:
                                            seqIdRemap = self.reasonsForReParsing['seq_id_remap'] if 'seq_id_remap' in self.reasonsForReParsing else []
                                            if len(seqIdRemap) != len(seqIdRemapFailed)\
                                               or seqIdRemap[0]['chain_id'] != seqIdRemapFailed[0]['chain_id']\
                                               or not all(src_seq_id in seqIdRemap[0] for src_seq_id in seqIdRemapFailed[0]):
                                                self.reasonsForReParsing['ext_chain_seq_id_remap'] = seqIdRemapFailed

                if self.reasons is None and any(True for f in self.f if '[Atom not found]' in f):
                    if len(self.unambigAtomNameMapping) > 0:
                        if 'unambig_atom_id_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['unambig_atom_id_remap'] = self.unambigAtomNameMapping
                    if len(self.ambigAtomNameMapping) > 0:
                        if 'ambig_atom_id_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['ambig_atom_id_remap'] = self.ambigAtomNameMapping
                    if len(self.unambigAtomNameMapping) + len(self.ambigAtomNameMapping) == 0:
                        __f = deepcopy(self.f)
                        self.f = []
                        for f in __f:
                            if '[Atom not found]' in f and 'makeDIST_RST' in f:
                                self.f.append(re.sub(r'\[Atom not found\]', '[Unsupported data]', f, 1))
                            else:
                                self.f.append(f)

            if 'local_seq_scheme' in self.reasonsForReParsing:
                if 'non_poly_remap' in self.reasonsForReParsing or 'branched_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                elif 'seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                elif 'chain_seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']
                elif 'ext_chain_seq_id_remap' in self.reasonsForReParsing:
                    del self.reasonsForReParsing['local_seq_scheme']

            if 'local_seq_scheme' in self.reasonsForReParsing and len(self.reasonsForReParsing) == 1:
                mergePolySeqRstAmbig(self.__polySeqRstFailed, self.__polySeqRstFailedAmbig)
                sortPolySeqRst(self.__polySeqRstFailed)
                if len(self.__polySeqRstFailed) > 0:
                    self.reasonsForReParsing['extend_seq_scheme'] = self.__polySeqRstFailed
                del self.reasonsForReParsing['local_seq_scheme']

            if self.__remediate:
                if self.dihed_lb_greater_than_ub and self.dihed_ub_always_positive:
                    if 'dihed_unusual_order' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['dihed_unusual_order'] = True

        finally:
            self.warningMessage = sorted(list(set(self.f)), key=self.f.index)

            self.translateToStdResNameWrapper.cache_clear()
            self.__getCoordAtomSiteOf.cache_clear()

            translateToStdAtomNameNoRef.cache_clear()
            translateToStdAtomNameWithRef.cache_clear()

    def validateDistanceRange(self, weight: float, target_value: Optional[float],
                              lower_limit: Optional[float], upper_limit: Optional[float],
                              target_value_uncertainty: Optional[float], omit_dist_limit_outlier: bool) -> Optional[dict]:
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value_uncertainty is not None:
            dstFunc['target_value_uncertainty'] = f"{target_value_uncertainty}"

        if None not in (target_value, upper_limit, lower_limit)\
           and abs(target_value - lower_limit) <= DIST_AMBIG_UNCERT\
           and abs(target_value - upper_limit) <= DIST_AMBIG_UNCERT:
            if target_value >= DIST_AMBIG_MED:
                lower_limit = None
            elif target_value <= DIST_AMBIG_LOW:
                upper_limit = None

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and target_value_uncertainty is not None and self.allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value:.3f}" if target_value > 0.0 else "0.0"
            else:
                if target_value <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    if 'upl' in (self.file_ext, self.cur_dist_type) or 'lol' in (self.file_ext, self.cur_dist_type):
                        dstFunc['target_value'] = f"{target_value:.3f}"
                    else:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The target value='{target_value:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        target_value = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The target value='{target_value:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}" if lower_limit > 0.0 else "0.0"
            else:
                if lower_limit <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    if 'lol' in (self.file_ext, self.cur_dist_type):
                        dstFunc['lower_limit'] = f"{lower_limit:.3f}"
                    else:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        lower_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and target_value_uncertainty is not None and self.allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}" if upper_limit > 0.0 else "0.0"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and omit_dist_limit_outlier:
                    if 'upl' in (self.file_ext, self.cur_dist_type):
                        dstFunc['upper_limit'] = f"{upper_limit:.3f}"
                    else:
                        self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                                      f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                        upper_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value:.3f}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value:.3f}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

            if upper_limit is None and lower_limit is not None and lower_limit <= 0.0:  # ignore meaningless lower limit restraint
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")
                validRange = False

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

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

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    def validateDistanceRangeWithIndex(self, index: int, group: int, weight: float, scale: float, target_value: Optional[float],
                                       lower_limit: Optional[float], upper_limit: Optional[float], omit_dist_limit_outlier: bool) -> Optional[dict]:
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'scale': scale}

        if None not in (target_value, upper_limit, lower_limit)\
           and abs(target_value - lower_limit) <= DIST_AMBIG_UNCERT\
           and abs(target_value - upper_limit) <= DIST_AMBIG_UNCERT:
            if target_value >= DIST_AMBIG_MED:
                lower_limit = None
            elif target_value <= DIST_AMBIG_LOW:
                upper_limit = None

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and self.allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value:.3f}" if target_value > 0.0 else "0.0"
            else:
                if target_value <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The target value='{target_value:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    target_value = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The target value='{target_value:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}" if lower_limit > 0.0 else "0.0"
            else:
                if lower_limit <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    lower_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and self.allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}" if upper_limit > 0.0 else "0.0"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and omit_dist_limit_outlier:
                    self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index,g=group)}"
                                  f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.")
                    upper_limit = None
                else:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value:.3f}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value:.3f}'.")

        else:

            if None not in (lower_limit, upper_limit):
                if lower_limit > upper_limit:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.")

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The target value='{target_value:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if DIST_RANGE_MIN <= lower_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The lower limit value='{lower_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if DIST_RANGE_MIN <= upper_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index, g=group)}"
                              f"The upper limit value='{upper_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    def validatePeakVolumeRange(self, weight: float, target_value: Optional[float],
                                lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate NOESY peak volume value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            dstFunc['target_value'] = f"{target_value}"

        if lower_limit is not None:
            dstFunc['lower_limit'] = f"{lower_limit}"

        if upper_limit is not None:
            dstFunc['upper_limit'] = f"{upper_limit}"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit}' must be greater than the target value '{target_value}'.")

        if not validRange:
            return None

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    @functools.lru_cache(maxsize=256)
    def translateToStdResNameWrapper(self, seqId: int, compId: str, preferNonPoly: bool = False) -> str:
        _compId = compId
        refCompId = None
        for ps in self.polySeq:
            if preferNonPoly:
                continue
            _, _, refCompId = self.getRealChainSeqId(ps, seqId, _compId)
            if refCompId is not None:
                compId = translateToStdResName(_compId, refCompId=refCompId, ccU=self.ccU)
                if compId != _compId and compId in monDict3 and _compId in monDict3:
                    continue
                break
        if refCompId is None and self.hasNonPolySeq:
            for np in self.__nonPolySeq:
                _, _, refCompId = self.getRealChainSeqId(np, seqId, _compId, False)
                if refCompId is not None:
                    compId = translateToStdResName(_compId, refCompId=refCompId, ccU=self.ccU)
                    break
        if refCompId is None:
            compId = translateToStdResName(_compId, ccU=self.ccU)
        return compId

    def getRealChainSeqId(self, ps: dict, seqId: int, compId: Optional[str] = None, isPolySeq: bool = True,
                          isFirstTrial: bool = True) -> Tuple[str, int, Optional[str]]:
        if compId in ('MTS', 'ORI'):
            compId = _compId = None
        if compId is not None:
            compId = _compId = translateToStdResName(compId, ccU=self.ccU)
            if len(_compId) == 2 and _compId.startswith('D'):
                _compId = compId[1]
        if not self.__preferAuthSeq:
            seqKey = (ps['auth_chain_id'], seqId)
            if seqKey in self.__labelToAuthSeq:
                _chainId, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _chainId, _seqId, ps['comp_id'][ps['seq_id'].index(seqId)]
                if seqKey[1] in ps['seq_id']:  # resolve conflict between label/auth sequence schemes of polymer/non-polymer (2l90)
                    idx = ps['seq_id'].index(seqKey[1])
                    return _chainId, ps['auth_seq_id'][idx], ps['comp_id'][idx]
        if seqId in ps['auth_seq_id']:
            if compId is None:
                return ps['auth_chain_id'], seqId, ps['comp_id'][ps['auth_seq_id'].index(seqId)]
            for idx in [_idx for _idx, _seqId in enumerate(ps['auth_seq_id']) if _seqId == seqId]:
                if 'alt_comp_id' in ps and idx < len(ps['alt_comp_id']):
                    if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx], ps['alt_comp_id'][idx]):
                        return ps['auth_chain_id'], seqId, ps['comp_id'][idx]
                    if compId != _compId and _compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx], ps['alt_comp_id'][idx]):
                        return ps['auth_chain_id'], seqId, ps['comp_id'][idx]
                if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx])\
                   or (isPolySeq and seqId == 1
                       and ((compId.endswith('-N') and all(c in ps['comp_id'][idx] for c in compId.split('-')[0]))
                            or (ps['comp_id'][idx] == 'PCA' and 'P' == compId[0] and ('GL' in compId or 'N' in compId)))):
                    return ps['auth_chain_id'], seqId, ps['comp_id'][idx]
                if compId != _compId and _compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
                    return ps['auth_chain_id'], seqId, ps['comp_id'][idx]
        if self.reasons is not None and 'extend_seq_scheme' in self.reasons:
            _ps = next((_ps for _ps in self.reasons['extend_seq_scheme'] if _ps['chain_id'] == ps['auth_chain_id']), None)
            if _ps is not None:
                if seqId in _ps['seq_id']:
                    return ps['auth_chain_id'], seqId, _ps['comp_id'][_ps['seq_id'].index(seqId)]
        if 'Check the 1th row of' in self.getCurrentRestraint() and isFirstTrial and isPolySeq\
           and (self.reasons is None
                or not ('seq_id_remap' in self.reasons or 'chain_seq_id_remap' in self.reasons or 'ext_chain_seq_id_remap' in self.reasons)):
            try:
                if not any(_ps['auth_seq_id'][0] - len(_ps['seq_id']) <= seqId <= _ps['auth_seq_id'][-1] + len(_ps['seq_id'])
                           and ('gap_in_auth_seq' not in _ps or _ps['auth_seq_id'][0] > 0)
                           for _ps in self.polySeq):
                    self.__preferAuthSeq = not self.__preferAuthSeq
                    trial = self.getRealChainSeqId(ps, seqId, compId, isPolySeq, False)
                    if trial[2] is not None and compId == trial[2]:
                        return trial
                    self.__preferAuthSeq = not self.__preferAuthSeq
            except TypeError:
                pass
        return ps['auth_chain_id'], seqId, None

    def assignCoordPolymerSequence(self, seqId: int, compId: str, atomId: str, enableWarning: bool = True
                                   ) -> Tuple[List[Tuple[str, int, str, bool]], bool]:
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        asis = preferNonPoly = False
        _seqId = seqId
        _compId = compId

        fixedChainId = fixedSeqId = fixedCompId = None

        if self.hasNonPoly:

            resolved = False

            for np in self.__nonPoly:
                if 'alt_comp_id' in np and 'alt_auth_seq_id' in np\
                   and compId in np['alt_comp_id'] and seqId in np['alt_auth_seq_id']:
                    npCompId = np['comp_id'][0]
                    npSeqId = np['auth_seq_id'][0]
                    for ps in self.polySeq:
                        if 'ambig_auth_seq_id' in ps and seqId in ps['ambig_auth_seq_id']:
                            psCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(psCompId, atomId, leave_unmatched=True)
                            if details is None:
                                _, _coordAtomSite = self.getCoordAtomSiteOf(ps['auth_chain_id'], seqId, psCompId, cifCheck=self.hasCoord)
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = psCompId
                                    resolved = True
                                    break
                            _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], npSeqId, npCompId, cifCheck=self.hasCoord)
                            if self.__mrAtomNameMapping is not None:
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, npSeqId, npCompId, atomId, _coordAtomSite)
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(npCompId, atomId, leave_unmatched=True)
                            if details is None:
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = npCompId
                                    seqId = _seqId = npSeqId
                                    preferNonPoly = resolved = True
                                    break

            if not resolved and compId in ('CYS', 'CYSZ', 'CYZ', 'CZN', 'CYO', 'ION', 'ZN1', 'ZN2')\
               and atomId in zincIonCode:
                znCount = 0
                znSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'ZN':
                        znSeqId = np['auth_seq_id'][0]
                        znCount += 1
                if znCount > 0:
                    compId = _compId = 'ZN'
                    if znCount == 1:
                        seqId = _seqId = znSeqId
                        atomId = 'ZN'
                        resolved = True
                    preferNonPoly = True

            if not resolved and compId in ('CYS', 'CYSC', 'CYC', 'CCA', 'CYO', 'ION', 'CA1', 'CA2')\
               and atomId in calciumIonCode:
                caCount = 0
                caSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'CA':
                        caSeqId = np['auth_seq_id'][0]
                        caCount += 1
                if caCount > 0:
                    compId = _compId = 'CA'
                    if caCount == 1:
                        seqId = _seqId = caSeqId
                        atomId = 'CA'
                        resolved = True
                    preferNonPoly = True

            if not resolved and len(atomId) > 1 and atomId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == atomId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, atomId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        compId = _compId = atomId
                        preferNonPoly = resolved = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == atomId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                compId = _compId = atomId
                                preferNonPoly = resolved = True

            if not resolved and len(compId) > 1 and compId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == compId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, compId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        atomId = _compId = compId
                        preferNonPoly = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == compId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                atomId = _compId = compId
                                preferNonPoly = True

        if self.__splitLigand is not None and len(self.__splitLigand):
            found = False
            for (_, _seqId_, _compId_), ligList in self.__splitLigand.items():
                if _seqId_ != seqId or _compId_ != compId:
                    continue
                for idx, lig in enumerate(ligList):
                    _atomId = atomId
                    if self.__mrAtomNameMapping is not None and compId not in monDict3:
                        _, _, _atomId = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

                    if _atomId in lig['atom_ids']:
                        seqId = _seqId = lig['auth_seq_id']
                        compId = _compId = lig['comp_id']
                        atomId = _atomId
                        preferNonPoly = idx > 0
                        found = True
                        break
                if found:
                    break

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

        compId = self.translateToStdResNameWrapper(_seqId, _compId, preferNonPoly)

        if len(self.__modResidue) > 0:
            modRes = next((modRes for modRes in self.__modResidue
                           if modRes['auth_comp_id'] == compId
                           and (compId != _compId or seqId in (modRes['auth_seq_id'], modRes['seq_id']))), None)
            if modRes is not None:
                compId = modRes['comp_id']

        self.allow_ext_seq = False

        if self.reasons is not None:
            if 'ambig_atom_id_remap' in self.reasons and _compId in self.reasons['ambig_atom_id_remap']\
               and atomId in self.reasons['ambig_atom_id_remap'][_compId]:
                return self.atomIdListToChainAssign(self.reasons['ambig_atom_id_remap'][_compId][atomId])
            if 'unambig_atom_id_remap' in self.reasons and _compId in self.reasons['unambig_atom_id_remap']\
               and atomId in self.reasons['unambig_atom_id_remap'][_compId]:
                atomId = self.reasons['unambig_atom_id_remap'][_compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.reasons and _compId in self.reasons['non_poly_remap']\
               and seqId in self.reasons['non_poly_remap'][_compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], None, None, seqId, _compId)
                preferNonPoly = True
            if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
                preferNonPoly = True
            if not preferNonPoly:
                if 'chain_id_remap' in self.reasons:  # and seqId in self.reasons['chain_id_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                    if seqId not in self.reasons['chain_id_remap']:
                        self.allow_ext_seq = True
                elif 'chain_id_clone' in self.reasons:  # and seqId in self.reasons['chain_id_clone']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                    if seqId not in self.reasons['chain_id_clone']:
                        self.allow_ext_seq = True
                elif 'seq_id_remap' in self.reasons\
                        or 'chain_seq_id_remap' in self.reasons\
                        or 'ext_chain_seq_id_remap' in self.reasons:
                    if 'ext_chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId, fixedCompId =\
                            retrieveRemappedSeqIdAndCompId(self.reasons['ext_chain_seq_id_remap'], None, seqId,
                                                           compId if compId in monDict3 else None)
                        self.allow_ext_seq = fixedCompId is not None
                    if fixedSeqId is None and 'chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], None, seqId,
                                                                         compId if compId in monDict3 else None)
                    if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], None, seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        pure_ambig = _compId == 'AMB' and (('-' in atomId and ':' in atomId) or '.' in atomId)

        updatePolySeqRst(self.__polySeqRst, self.polySeq[0]['chain_id'] if fixedChainId is None else fixedChainId, _seqId, compId, _compId)

        types = self.csStat.getTypeOfCompId(compId)
        if all(not t for t in types) or compId in ('MTS', 'ORI'):
            types = None
        elif compId != _compId:
            if types != self.csStat.getTypeOfCompId(_compId):
                types = None

        def comp_id_unmatched_with(ps, cif_comp_id):
            if 'alt_comp_id' in ps and self.csStat.peptideLike(cif_comp_id) and compId.startswith('D') and len(compId) >= 3\
               and self.ccU.lastChemCompDict['_chem_comp.type'].upper() == 'D-PEPTIDE LINKING':
                revertPolySeqRst(self.__polySeqRst, ps['chain_id'] if fixedChainId is None else fixedChainId, _seqId, compId)

            if types is None or ('alt_comp_id' in ps and _compId in ps['alt_comp_id']):
                return False
            if compId not in monDict3 and cif_comp_id not in monDict3:
                return False
            return types != self.csStat.getTypeOfCompId(cif_comp_id)

        def comp_id_in_polymer(np):
            return (_seqId == 1
                    and ((compId.endswith('-N') and all(c in np['comp_id'][0] for c in compId.split('-')[0]))
                         or (np['comp_id'][0] == 'PCA' and 'P' == compId[0] and ('GL' in compId or 'N' in compId))))\
                or (compId in monDict3
                    and any(compId in ps['comp_id'] for ps in self.polySeq)
                    and compId not in np['comp_id'])

        for ps in self.polySeq:
            if preferNonPoly or pure_ambig:
                continue
            chainId, seqId, cifCompId = self.getRealChainSeqId(ps, _seqId, compId)
            if self.reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId <= 0 and self.__shiftNonPosSeq is not None and chainId in self.__shiftNonPosSeq:
                seqId -= 1
            if seqId in ps['auth_seq_id'] or fixedCompId is not None:
                if fixedCompId is not None:
                    cifCompId = origCompId = fixedCompId
                else:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(ps['auth_seq_id'], ps['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), ps['auth_seq_id'].index(seqId))
                    else:
                        idx = ps['auth_seq_id'].index(seqId) if seqId in ps['auth_seq_id'] else ps['seq_id'].index(seqId)
                    cifCompId = ps['comp_id'][idx]
                    origCompId = ps['auth_comp_id'][idx]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                if cifCompId != compId:
                    if (self.__shiftNonPosSeq is None or chainId not in self.__shiftNonPosSeq)\
                       and seqId <= 0 and seqId - 1 in ps['auth_seq_id']\
                       and compId == ps['comp_id'][ps['auth_seq_id'].index(seqId - 1)]:
                        seqId -= 1
                        if self.__shiftNonPosSeq is None:
                            self.__shiftNonPosSeq = {}
                        self.__shiftNonPosSeq[chainId] = True
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                          if _seqId == seqId and _compId == compId)
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, True))
                else:
                    _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                    if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                        chainAssign.add((chainId, seqId, cifCompId, True))

            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
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
                            idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                            try:
                                seqId_ = ps['auth_seq_id'][idx]
                                cifCompId = ps['comp_id'][idx]
                                origCompId = ps['auth_comp_id'][idx]
                                if comp_id_unmatched_with(ps, cifCompId):
                                    continue
                                if cifCompId != compId:
                                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                                    if compId in compIds:
                                        cifCompId = compId
                                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                          if _seqId == seqId and _compId == compId)
                                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, cifCompId, cifCheck=self.hasCoord)
                                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                        chainAssign.add((chainId, seqId_, cifCompId, True))
                                    else:
                                        _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                        if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                            chainAssign.add((chainId, seqId_, cifCompId, True))
                            except IndexError:
                                pass

        if self.hasNonPolySeq:
            ligands = 0
            if self.hasNonPoly:
                for np in self.__nonPoly:
                    ligands += np['comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        ligands += np['comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0 and len(chainAssign) == 0 and _compId not in monDict3:
                    __compId = None
                    for np in self.__nonPoly:
                        for ligand in np['comp_id']:
                            __compId = translateToLigandName(_compId, ligand, self.ccU)
                            if __compId == ligand:
                                ligands += 1
                    if ligands == 1:
                        compId = _compId = __compId
                    elif self.__monoNonPoly and self.ccU.updateChemCompDict(_compId, False):
                        if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS':
                            compId = _compId = self.__nonPoly[0]['comp_id'][0]
                            ligands = 1
                        elif _compId == 'ION':
                            if self.__nonPoly[0]['comp_id'][0] in SYMBOLS_ELEMENT:
                                compId = _compId = self.__nonPoly[0]['comp_id'][0]
                                ligands = 1
                if self.reasons is None and atomId in self.__uniqAtomIdToSeqKey:
                    seqKey = self.__uniqAtomIdToSeqKey[atomId]
                    if _seqId != seqKey[1]:
                        if 'non_poly_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['non_poly_remap'] = {}
                        if _compId not in self.reasonsForReParsing['non_poly_remap']:
                            self.reasonsForReParsing['non_poly_remap'][_compId] = {}
                        if _seqId not in self.reasonsForReParsing['non_poly_remap'][_compId]:
                            self.reasonsForReParsing['non_poly_remap'][_compId][_seqId] =\
                                {'chain_id': seqKey[0],
                                 'seq_id': seqKey[1],
                                 'original_chain_id': None}
            for np in self.__nonPolySeq:
                chainId, seqId, cifCompId = self.getRealChainSeqId(np, _seqId, compId, False)
                if self.reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if comp_id_in_polymer(np):
                    continue
                if pure_ambig:
                    continue
                if 'alt_auth_seq_id' in np and seqId not in np['auth_seq_id'] and seqId in np['alt_auth_seq_id']:
                    try:
                        seqId = next(_seqId_ for _seqId_, _altSeqId_ in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _altSeqId_ == seqId)
                    except StopIteration:
                        pass
                if seqId in np['auth_seq_id']\
                   or (ligands == 1 and (_compId in np['comp_id'] or ('alt_comp_id' in np and _compId in np['alt_comp_id']))):
                    if ligands == 1 and cifCompId is None:
                        cifCompId = _compId
                    idx = -1
                    try:
                        if cifCompId is not None:
                            idx = next(_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(np['auth_seq_id'], np['comp_id']))
                                       if (_seqId_ == seqId or ligands == 1) and _cifCompId_ == cifCompId)
                            if ligands == 1:
                                seqId = np['auth_seq_id'][idx]
                    except StopIteration:
                        pass
                    if idx == -1:
                        idx = np['auth_seq_id'].index(seqId) if seqId in np['auth_seq_id']\
                            else np['seq_id'].index(seqId) if seqId in np['seq_id'] else 0
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    seqId = np['auth_seq_id'][idx]
                    if cifCompId in ('ZN', 'CA') and atomId[0] in protonBeginCode:  # 2loa
                        continue
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, _seqId, origCompId, atomId, coordAtomSite)
                    if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                        if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))
                    else:
                        _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                        if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.polySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.authToLabelSeq:
                    _, seqId = self.authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))

            if self.hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    if comp_id_in_polymer(np):
                        continue
                    if pure_ambig:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                            else:
                                _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['auth_chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                    if cifCompId != compId:
                        if cifCompId in monDict3 and compId in monDict3:
                            continue
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                        if compId in compIds:
                            cifCompId = compId
                    chainAssign.add((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0 and (self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT or self.__multiPolymer):
            for ps in self.polySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        idx = ps['seq_id'].index(_seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                if compId in (cifCompId, origCompId):
                                    self.authSeqId = 'label_seq_id'
                                    self.__setLocalSeqScheme()
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                self.authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()

        if len(chainAssign) == 0:
            if pure_ambig:
                if enableWarning:
                    warn_title = 'Atom not found' if self.reasons is None else 'Unsupported data'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                  f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                  "Please attach ambiguous atom name mapping information generated "
                                  f"by 'makeDIST_RST' to the {self.software_name} restraint file.")
            elif seqId == 1 or (chainId if fixedChainId is None else fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequence(seqId, compId, 'H1')
            else:
                auth_seq_id_list = list(filter(None, self.polySeq[0]['auth_seq_id']))
                min_auth_seq_id = max_auth_seq_id = UNREAL_AUTH_SEQ_NUM
                if len(auth_seq_id_list) > 0:
                    min_auth_seq_id = min(auth_seq_id_list)
                    max_auth_seq_id = max(auth_seq_id_list)
                if self.__monoPolymer\
                   and (seqId < 1
                        or (compId == 'ACE' and seqId == min_auth_seq_id - 1)
                        or (compId == 'NH2' and seqId == max_auth_seq_id + 1)
                        or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT)):
                    refChainId = self.polySeq[0]['auth_chain_id']
                    if (compId == 'ACE' and seqId == min_auth_seq_id - 1)\
                       or (compId == 'NH2' and seqId == max_auth_seq_id + 1)\
                       or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                           and (min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id
                                or max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ)):
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                        chainAssign.add((refChainId, _seqId, compId, True))
                        asis = True
                    elif compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT:
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                    else:
                        if enableWarning:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                          f"The residue number '{_seqId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                else:
                    ext_seq = False
                    if (compId in monDict3 or compId in ('ACE', 'NH2')) and (self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                                                                             or len(atomId) == 1):
                        refChainIds = []
                        _auth_seq_id_list = auth_seq_id_list
                        for idx, ps in enumerate(self.polySeq):
                            if idx > 0:
                                auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                                _auth_seq_id_list.extend(auth_seq_id_list)
                            if len(auth_seq_id_list) > 0:
                                if idx > 0:
                                    min_auth_seq_id = min(auth_seq_id_list)
                                    max_auth_seq_id = max(auth_seq_id_list)
                                if min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id\
                                   and (compId in monDict3 or (compId == 'ACE' and seqId == min_auth_seq_id - 1)):
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                                elif max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ\
                                        and (compId in monDict3 or (compId == 'NH2' and seqId == max_auth_seq_id + 1)):
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                                elif self.reasons is None and compId in monDict3 and atomId == 'H' and seqId < min_auth_seq_id\
                                        and self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT:
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                        if ext_seq and seqId in _auth_seq_id_list:
                            ext_seq = False
                    if self.allow_ext_seq:
                        refChainIds = [fixedChainId]
                        ext_seq = True
                        enableWarning = False
                    if ext_seq:
                        refChainId = refChainIds[0] if len(refChainIds) == 1 else refChainIds
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                        if isinstance(refChainId, str):
                            chainAssign.add((refChainId, _seqId, compId, True))
                        else:
                            for _refChainId in refChainIds:
                                chainAssign.add((_refChainId, _seqId, compId, True))
                        asis = True
                    else:
                        if enableWarning:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{_seqId}:{_compId}:{atomId} is not present in the coordinates.")
                    updatePolySeqRst(self.__polySeqRstFailed, self.polySeq[0]['chain_id'] if fixedChainId is None else fixedChainId,
                                     _seqId, compId, _compId)

        return list(chainAssign), asis

    def assignCoordPolymerSequenceWithChainId(self, refChainId: str, seqId: int, compId: str, atomId: str, enableWarning: bool = True
                                              ) -> Tuple[List[Tuple[str, int, str, bool]], bool]:
        """ Assign polymer sequences of the coordinates.
        """

        if refChainId is None:
            return self.assignCoordPolymerSequence(seqId, compId, atomId, enableWarning)

        _refChainId = refChainId

        chainAssign = set()
        asis = preferNonPoly = False
        _seqId = seqId
        _compId = compId

        fixedChainId = fixedSeqId = fixedCompId = None

        if self.hasNonPoly:

            resolved = False

            for np in self.__nonPoly:
                if 'alt_comp_id' in np and 'alt_auth_seq_id' in np\
                   and compId in np['alt_comp_id'] and seqId in np['alt_auth_seq_id']:
                    npCompId = np['comp_id'][0]
                    npSeqId = np['auth_seq_id'][0]
                    for ps in self.polySeq:
                        if 'ambig_auth_seq_id' in ps and seqId in ps['ambig_auth_seq_id']:
                            psCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(psCompId, atomId, leave_unmatched=True)
                            if details is None:
                                _, _coordAtomSite = self.getCoordAtomSiteOf(ps['auth_chain_id'], seqId, psCompId, cifCheck=self.hasCoord)
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = psCompId
                                    resolved = True
                                    break
                            _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], npSeqId, npCompId, cifCheck=self.hasCoord)
                            if self.__mrAtomNameMapping is not None:
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, npSeqId, npCompId, atomId, _coordAtomSite)
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(npCompId, atomId, leave_unmatched=True)
                            if details is None:
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = npCompId
                                    seqId = _seqId = npSeqId
                                    preferNonPoly = resolved = True
                                    break

            if not resolved and compId in ('CYS', 'CYSZ', 'CYZ', 'CZN', 'CYO', 'ION', 'ZN1', 'ZN2')\
               and atomId in zincIonCode:
                znCount = 0
                znSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'ZN':
                        znSeqId = np['auth_seq_id'][0]
                        znCount += 1
                if znCount > 0:
                    compId = _compId = 'ZN'
                    if znCount == 1:
                        seqId = _seqId = znSeqId
                        atomId = 'ZN'
                        resolved = True
                    preferNonPoly = True

            if not resolved and compId in ('CYS', 'CYSC', 'CYC', 'CCA', 'CYO', 'ION', 'CA1', 'CA2')\
               and atomId in calciumIonCode:
                caCount = 0
                caSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'CA':
                        caSeqId = np['auth_seq_id'][0]
                        caCount += 1
                if caCount > 0:
                    compId = _compId = 'CA'
                    if caCount == 1:
                        seqId = _seqId = caSeqId
                        atomId = 'CA'
                        resolved = True
                    preferNonPoly = True

            if not resolved and len(atomId) > 1 and atomId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == atomId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, atomId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        compId = _compId = atomId
                        preferNonPoly = resolved = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == atomId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                compId = _compId = atomId
                                preferNonPoly = resolved = True

            if not resolved and len(compId) > 1 and compId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == compId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, compId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        atomId = _compId = compId
                        preferNonPoly = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == compId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                atomId = _compId = compId
                                preferNonPoly = True

        if self.__splitLigand is not None and len(self.__splitLigand):
            found = False
            for (_, _seqId_, _compId_), ligList in self.__splitLigand.items():
                if _seqId_ != seqId or _compId_ != compId:
                    continue
                for idx, lig in enumerate(ligList):
                    _atomId = atomId
                    if self.__mrAtomNameMapping is not None and compId not in monDict3:
                        _, _, _atomId = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

                    if _atomId in lig['atom_ids']:
                        seqId = _seqId = lig['auth_seq_id']
                        compId = _compId = lig['comp_id']
                        atomId = _atomId
                        preferNonPoly = idx > 0
                        found = True
                        break
                if found:
                    break

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

        compId = self.translateToStdResNameWrapper(_seqId, _compId, preferNonPoly)

        if len(self.__modResidue) > 0:
            modRes = next((modRes for modRes in self.__modResidue
                           if modRes['auth_comp_id'] == compId
                           and (compId != _compId or seqId in (modRes['auth_seq_id'], modRes['seq_id']))), None)
            if modRes is not None:
                compId = modRes['comp_id']

        self.allow_ext_seq = False

        if self.reasons is not None:
            if 'ambig_atom_id_remap' in self.reasons and _compId in self.reasons['ambig_atom_id_remap']\
               and atomId in self.reasons['ambig_atom_id_remap'][_compId]:
                return self.atomIdListToChainAssign(self.reasons['ambig_atom_id_remap'][_compId][atomId])
            if 'unambig_atom_id_remap' in self.reasons and _compId in self.reasons['unambig_atom_id_remap']\
               and atomId in self.reasons['unambig_atom_id_remap'][_compId]:
                atomId = self.reasons['unambig_atom_id_remap'][_compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.reasons and _compId in self.reasons['non_poly_remap']\
               and seqId in self.reasons['non_poly_remap'][_compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], None, str(refChainId), seqId, _compId)
                refChainId = fixedChainId
                preferNonPoly = True
            if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
                refChainId = fixedChainId
                preferNonPoly = True
            if not preferNonPoly:
                if 'chain_id_remap' in self.reasons:  # and seqId in self.reasons['chain_id_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                    if seqId not in self.reasons['chain_id_remap']:
                        self.allow_ext_seq = True
                    refChainId = fixedChainId
                elif 'chain_id_clone' in self.reasons:  # and seqId in self.reasons['chain_id_clone']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                    if seqId not in self.reasons['chain_id_clone']:
                        self.allow_ext_seq = True
                    refChainId = fixedChainId
                elif 'seq_id_remap' in self.reasons\
                        or 'chain_seq_id_remap' in self.reasons\
                        or 'ext_chain_seq_id_remap' in self.reasons:
                    if 'ext_chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId, fixedCompId =\
                            retrieveRemappedSeqIdAndCompId(self.reasons['ext_chain_seq_id_remap'], str(refChainId), seqId,
                                                           compId if compId in monDict3 else None)
                        self.allow_ext_seq = fixedCompId is not None
                        if fixedSeqId is not None:
                            refChainId = fixedChainId
                    if fixedSeqId is None and 'chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], str(refChainId), seqId,
                                                                         compId if compId in monDict3 else None)
                        if fixedSeqId is not None:
                            refChainId = fixedChainId
                    if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], str(refChainId), seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        pure_ambig = _compId == 'AMB' and (('-' in atomId and ':' in atomId) or '.' in atomId)

        updatePolySeqRst(self.__polySeqRst, str(refChainId), _seqId, compId, _compId)

        types = self.csStat.getTypeOfCompId(compId)
        if all(not t for t in types) or compId in ('MTS', 'ORI'):
            types = None
        elif compId != _compId:
            if types != self.csStat.getTypeOfCompId(_compId):
                types = None

        def comp_id_unmatched_with(ps, cif_comp_id):
            if 'alt_comp_id' in ps and self.csStat.peptideLike(cif_comp_id) and compId.startswith('D') and len(compId) >= 3\
               and self.ccU.lastChemCompDict['_chem_comp.type'].upper() == 'D-PEPTIDE LINKING':
                revertPolySeqRst(self.__polySeqRst, str(refChainId), _seqId, compId)

            if types is None or ('alt_comp_id' in ps and _compId in ps['alt_comp_id']):
                return False
            if compId not in monDict3 and cif_comp_id not in monDict3:
                return False
            return types != self.csStat.getTypeOfCompId(cif_comp_id)

        def comp_id_in_polymer(np):
            return (_seqId == 1
                    and ((compId.endswith('-N') and all(c in np['comp_id'][0] for c in compId.split('-')[0]))
                         or (np['comp_id'][0] == 'PCA' and 'P' == compId[0] and ('GL' in compId or 'N' in compId))))\
                or (compId in monDict3
                    and any(compId in ps['comp_id'] for ps in self.polySeq)
                    and compId not in np['comp_id'])

        if refChainId is not None or refChainId != _refChainId:
            if any(True for ps in self.polySeq if ps['auth_chain_id'] == _refChainId):
                fixedChainId = _refChainId
            elif self.hasNonPolySeq:
                if any(True for np in self.__nonPolySeq if np['auth_chain_id'] == _refChainId):
                    fixedChainId = _refChainId

        for ps in self.polySeq:
            if preferNonPoly or pure_ambig:
                continue
            chainId, seqId, cifCompId = self.getRealChainSeqId(ps, _seqId, compId)
            if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                if chainId != self.__chainNumberDict[refChainId]:
                    continue
            if self.reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId <= 0 and self.__shiftNonPosSeq is not None and chainId in self.__shiftNonPosSeq:
                seqId -= 1
            if seqId in ps['auth_seq_id'] or fixedCompId is not None:
                if fixedCompId is not None:
                    cifCompId = origCompId = fixedCompId
                else:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(ps['auth_seq_id'], ps['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), ps['auth_seq_id'].index(seqId))
                    else:
                        idx = ps['auth_seq_id'].index(seqId) if seqId in ps['auth_seq_id'] else ps['seq_id'].index(seqId)
                    cifCompId = ps['comp_id'][idx]
                    origCompId = ps['auth_comp_id'][idx]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                if cifCompId != compId:
                    if (self.__shiftNonPosSeq is None or chainId not in self.__shiftNonPosSeq)\
                       and seqId <= 0 and seqId - 1 in ps['auth_seq_id']\
                       and compId == ps['comp_id'][ps['auth_seq_id'].index(seqId - 1)]:
                        seqId -= 1
                        if self.__shiftNonPosSeq is None:
                            self.__shiftNonPosSeq = {}
                        self.__shiftNonPosSeq[chainId] = True
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                          if _seqId == seqId and _compId == compId)
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId
                else:
                    _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                    if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                        chainAssign.add((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId

            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
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
                            idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                            try:
                                seqId_ = ps['auth_seq_id'][idx]
                                cifCompId = ps['comp_id'][idx]
                                origCompId = ps['auth_comp_id'][idx]
                                if comp_id_unmatched_with(ps, cifCompId):
                                    continue
                                if cifCompId != compId:
                                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                                    if compId in compIds:
                                        cifCompId = compId
                                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                          if _seqId == seqId and _compId == compId)
                                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, cifCompId, cifCheck=self.hasCoord)
                                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                        chainAssign.add((chainId, seqId_, cifCompId, True))
                                    else:
                                        _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                        if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                            chainAssign.add((chainId, seqId_, cifCompId, True))
                            except IndexError:
                                pass

        if self.hasNonPolySeq:
            ligands = 0
            if self.hasNonPoly:
                for np in self.__nonPoly:
                    ligands += np['comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        ligands += np['comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0 and len(chainAssign) == 0 and _compId not in monDict3:
                    __compId = None
                    for np in self.__nonPoly:
                        for ligand in np['comp_id']:
                            __compId = translateToLigandName(_compId, ligand, self.ccU)
                            if __compId == ligand:
                                ligands += 1
                    if ligands == 1:
                        compId = _compId = __compId
                    elif self.__monoNonPoly and self.ccU.updateChemCompDict(_compId, False):
                        if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS':
                            compId = _compId = self.__nonPoly[0]['comp_id'][0]
                            ligands = 1
                        elif _compId == 'ION':
                            if self.__nonPoly[0]['comp_id'][0] in SYMBOLS_ELEMENT:
                                compId = _compId = self.__nonPoly[0]['comp_id'][0]
                                ligands = 1
                if self.reasons is None and atomId in self.__uniqAtomIdToSeqKey:
                    seqKey = self.__uniqAtomIdToSeqKey[atomId]
                    if _seqId != seqKey[1]:
                        if 'non_poly_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['non_poly_remap'] = {}
                        if _compId not in self.reasonsForReParsing['non_poly_remap']:
                            self.reasonsForReParsing['non_poly_remap'][_compId] = {}
                        if _seqId not in self.reasonsForReParsing['non_poly_remap'][_compId]:
                            self.reasonsForReParsing['non_poly_remap'][_compId][_seqId] =\
                                {'chain_id': seqKey[0],
                                 'seq_id': seqKey[1],
                                 'original_chain_id': refChainId}
            for np in self.__nonPolySeq:
                chainId, seqId, cifCompId = self.getRealChainSeqId(np, _seqId, compId, False)
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if self.reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if comp_id_in_polymer(np):
                    continue
                if pure_ambig:
                    continue
                if 'alt_auth_seq_id' in np and seqId not in np['auth_seq_id'] and seqId in np['alt_auth_seq_id']:
                    try:
                        seqId = next(_seqId_ for _seqId_, _altSeqId_ in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _altSeqId_ == seqId)
                    except StopIteration:
                        pass
                if seqId in np['auth_seq_id']\
                   or (ligands == 1 and (_compId in np['comp_id'] or ('alt_comp_id' in np and _compId in np['alt_comp_id']))):
                    if ligands == 1 and cifCompId is None:
                        cifCompId = _compId
                    idx = -1
                    try:
                        if cifCompId is not None:
                            idx = next(_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(np['auth_seq_id'], np['comp_id']))
                                       if (_seqId_ == seqId or ligands == 1) and _cifCompId_ == cifCompId)
                            if ligands == 1:
                                seqId = np['auth_seq_id'][idx]
                    except StopIteration:
                        pass
                    if idx == -1:
                        idx = np['auth_seq_id'].index(seqId) if seqId in np['auth_seq_id']\
                            else np['seq_id'].index(seqId) if seqId in np['seq_id'] else 0
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    seqId = np['auth_seq_id'][idx]
                    if cifCompId in ('ZN', 'CA') and atomId[0] in protonBeginCode:  # 2loa
                        continue
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, _seqId, origCompId, atomId, coordAtomSite)
                    if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                        if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                    else:
                        _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                        if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            for ps in self.polySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.authToLabelSeq:
                    _, seqId = self.authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

            if self.hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                        if chainId != self.__chainNumberDict[refChainId]:
                            continue
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    if comp_id_in_polymer(np):
                        continue
                    if pure_ambig:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                            else:
                                _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['auth_chain_id']
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        _seqId = fixedSeqId
                elif fixedSeqId is not None:
                    _seqId = fixedSeqId
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                    if cifCompId != compId:
                        if cifCompId in monDict3 and compId in monDict3:
                            continue
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                        if compId in compIds:
                            cifCompId = compId
                    chainAssign.add((chainId, _seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and (self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT or self.__multiPolymer):
            for ps in self.polySeq:
                if preferNonPoly or pure_ambig:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        idx = ps['seq_id'].index(_seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                if compId in (cifCompId, origCompId):
                                    self.authSeqId = 'label_seq_id'
                                    self.__setLocalSeqScheme()
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                self.authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            if pure_ambig:
                if enableWarning:
                    warn_title = 'Atom not found' if self.reasons is None else 'Unsupported data'
                    self.f.append(f"[{warn_title}] {self.getCurrentRestraint()}"
                                  f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                  "Please attach ambiguous atom name mapping information generated "
                                  f"by 'makeDIST_RST' to the {self.software_name} restraint file.")
            elif seqId == 1 or (refChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithChainId(refChainId, seqId, compId, 'H1')
            else:
                auth_seq_id_list = list(filter(None, self.polySeq[0]['auth_seq_id']))
                min_auth_seq_id = max_auth_seq_id = UNREAL_AUTH_SEQ_NUM
                if len(auth_seq_id_list) > 0:
                    min_auth_seq_id = min(auth_seq_id_list)
                    max_auth_seq_id = max(auth_seq_id_list)
                if self.__monoPolymer\
                   and (seqId < 1
                        or (compId == 'ACE' and seqId == min_auth_seq_id - 1)
                        or (compId == 'NH2' and seqId == max_auth_seq_id + 1)
                        or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT)):
                    refChainId = self.polySeq[0]['auth_chain_id']
                    if (compId == 'ACE' and seqId == min_auth_seq_id - 1)\
                       or (compId == 'NH2' and seqId == max_auth_seq_id + 1)\
                       or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                           and (min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id
                                or max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ)):
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                        chainAssign.add((refChainId, _seqId, compId, True))
                        asis = True
                    elif compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT:
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                    else:
                        if enableWarning:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                          f"The residue number '{_seqId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                else:
                    ext_seq = False
                    if (compId in monDict3 or compId in ('ACE', 'NH2')) and (self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                                                                             or len(atomId) == 1):
                        refChainIds = []
                        _auth_seq_id_list = auth_seq_id_list
                        for idx, ps in enumerate(self.polySeq):
                            if idx > 0:
                                auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                                _auth_seq_id_list.extend(auth_seq_id_list)
                            if len(auth_seq_id_list) > 0:
                                if idx > 0:
                                    min_auth_seq_id = min(auth_seq_id_list)
                                    max_auth_seq_id = max(auth_seq_id_list)
                                if min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id\
                                   and (compId in monDict3 or (compId == 'ACE' and seqId == min_auth_seq_id - 1)):
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                                elif max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ\
                                        and (compId in monDict3 or (compId == 'NH2' and seqId == max_auth_seq_id + 1)):
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                                elif self.reasons is None and compId in monDict3 and atomId == 'H' and seqId < min_auth_seq_id\
                                        and self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT:
                                    refChainIds.append(ps['auth_chain_id'])
                                    ext_seq = True
                        if ext_seq and seqId in _auth_seq_id_list:
                            ext_seq = False
                    if self.allow_ext_seq:
                        refChainIds = [fixedChainId]
                        ext_seq = True
                        enableWarning = False
                    if ext_seq:
                        refChainId = refChainIds[0] if len(refChainIds) == 1 else refChainIds
                        if enableWarning:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                          f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                          f"of chain {refChainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            resKey = (_seqId, _compId)
                            if resKey not in self.extResKey:
                                self.extResKey.append(resKey)
                        if isinstance(refChainId, str):
                            chainAssign.add((refChainId, _seqId, compId, True))
                        else:
                            for _refChainId in refChainIds:
                                chainAssign.add((_refChainId, _seqId, compId, True))
                        asis = True
                    else:
                        if enableWarning:
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                          f"{_seqId}:{_compId}:{atomId} is not present in the coordinates.")
                    updatePolySeqRst(self.__polySeqRstFailed, str(refChainId), _seqId, compId, _compId)

        elif any(True for ca in chainAssign if ca[0] == refChainId) and any(True for ca in chainAssign if ca[0] != refChainId):
            _chainAssign = copy.copy(chainAssign)
            for _ca in _chainAssign:
                if _ca[0] != refChainId:
                    chainAssign.remove(_ca)

        return list(chainAssign), asis

    def assignCoordPolymerSequenceWithoutCompId(self, seqId: int, atomId: Optional[str] = None) -> List[Tuple[str, int, str, bool]]:
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        _seqId = seqId

        fixedChainId = fixedSeqId = fixedCompId = None

        self.allow_ext_seq = False

        if self.reasons is not None:
            if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
            if 'chain_id_remap' in self.reasons:  # and seqId in self.reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                if seqId not in self.reasons['chain_id_remap']:
                    self.allow_ext_seq = True
            elif 'chain_id_clone' in self.reasons:  # and seqId in self.reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                if seqId not in self.reasons['chain_id_clone']:
                    self.allow_ext_seq = True
            if fixedSeqId is not None:
                seqId = _seqId = fixedSeqId

        for ps in self.polySeq:
            chainId, seqId, cifCompId = self.getRealChainSeqId(ps, _seqId, None)
            if self.reasons is not None:
                if 'seq_id_remap' not in self.reasons\
                   and 'chain_seq_id_remap' not in self.reasons\
                   and 'ext_chain_seq_id_remap' not in self.reasons:
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                else:
                    if 'ext_chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId, fixedCompId =\
                            retrieveRemappedSeqIdAndCompId(self.reasons['ext_chain_seq_id_remap'], chainId, seqId)
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            self.allow_ext_seq = fixedCompId is not None
                            seqId = _seqId = fixedSeqId
                    if fixedSeqId is None and 'chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], chainId, seqId)
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                    if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], None, seqId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id'] or fixedCompId is not None:
                if fixedCompId is not None:
                    cifCompId = fixedCompId
                else:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(ps['auth_seq_id'], ps['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), ps['auth_seq_id'].index(seqId))
                    else:
                        idx = ps['auth_seq_id'].index(seqId) if seqId in ps['auth_seq_id'] else ps['seq_id'].index(seqId)
                    cifCompId = ps['comp_id'][idx]
                if self.reasons is not None:
                    if 'non_poly_remap' in self.reasons and cifCompId in self.reasons['non_poly_remap']\
                       and seqId in self.reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], None, chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if (fixedChainId is not None and fixedChainId != chainId) or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
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
                            idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                            try:
                                seqId_ = ps['auth_seq_id'][idx]
                                cifCompId = ps['comp_id'][idx]
                                updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                                if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                            except IndexError:
                                pass

        if self.hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId, cifCompId = self.getRealChainSeqId(np, _seqId, None, False)
                if self.reasons is not None:
                    if 'seq_id_remap' not in self.reasons and 'chain_seq_id_remap' not in self.reasons:
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                    else:
                        if 'chain_seq_id_remap' in self.reasons:
                            fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], chainId, seqId)
                            if fixedChainId is not None and fixedChainId != chainId:
                                continue
                            if fixedSeqId is not None:
                                seqId = _seqId = fixedSeqId
                        if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                            _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], None, seqId)
                            if fixedSeqId is not None:
                                seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(np['auth_seq_id'], np['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), np['auth_seq_id'].index(seqId))
                    else:
                        idx = np['auth_seq_id'].index(seqId) if seqId in np['auth_seq_id'] else np['seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.authToLabelSeq:
                    _, seqId = self.authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                        if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))

            if self.hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                            if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    chainAssign.add((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0 and (self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT or self.__multiPolymer):
            for ps in self.polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        cifCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, chainId, seqId, cifCompId)
                        if atomId is None or len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()

        if len(chainAssign) == 0:
            if seqId == 1 or (chainId if fixedChainId is None else fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId is not None and atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithoutCompId(seqId, 'H1')
            if atomId is not None and (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                              f"{_seqId}:?:{atomId} is not present in the coordinates. "
                              "Please attach ambiguous atom name mapping information generated "
                              f"by 'makeDIST_RST' to the {self.software_name} restraint file.")
            elif atomId is not None:
                if self.__monoPolymer and seqId < 1:
                    refChainId = self.polySeq[0]['auth_chain_id']
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                  f"{_seqId}:?:{atomId} is not present in the coordinates. "
                                  f"The residue number '{_seqId}' is not present in polymer sequence "
                                  f"of chain {refChainId} of the coordinates. "
                                  "Please update the sequence in the Macromolecules page.")
                else:
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                  f"{_seqId}:{atomId} is not present in the coordinates.")
                    compIds = guessCompIdFromAtomId([atomId], self.polySeq, self.nefT)
                    if compIds is not None:
                        chainId = fixedChainId
                        if chainId is None and self.__monoPolymer:
                            chainId = self.polySeq[0]['chain_id']
                        if chainId is not None:
                            if len(compIds) == 1:
                                updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, compIds[0])
                            else:
                                updatePolySeqRstAmbig(self.__polySeqRstFailedAmbig, chainId, seqId, compIds)

        return list(chainAssign)

    def assignCoordPolymerSequenceWithChainIdWithoutCompId(self, fixedChainId: Optional[str], seqId: int, atomId: str) -> List[Tuple[str, int, str, bool]]:
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = set()
        _seqId = seqId

        fixedSeqId = fixedCompId = None

        self.allow_ext_seq = False

        if self.reasons is not None:
            if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
            if 'chain_id_remap' in self.reasons:  # and seqId in self.reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                if seqId not in self.reasons['chain_id_remap']:
                    self.allow_ext_seq = True
            elif 'chain_id_clone' in self.reasons:  # and seqId in self.reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                if seqId not in self.reasons['chain_id_clone']:
                    self.allow_ext_seq = True
            if fixedSeqId is not None:
                seqId = _seqId = fixedSeqId

        for ps in self.polySeq:
            chainId, seqId, cifCompId = self.getRealChainSeqId(ps, _seqId, None)
            if fixedChainId is not None and chainId != fixedChainId:
                continue
            if self.reasons is not None:
                if 'seq_id_remap' not in self.reasons\
                   and 'chain_seq_id_remap' not in self.reasons\
                   and 'ext_chain_seq_id_remap' not in self.reasons:
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                else:
                    if 'ext_chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId, fixedCompId =\
                            retrieveRemappedSeqIdAndCompId(self.reasons['ext_chain_seq_id_remap'], chainId, seqId)
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            self.allow_ext_seq = fixedCompId is not None
                            seqId = _seqId = fixedSeqId
                    if fixedSeqId is None and 'chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], chainId, seqId)
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                    if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], None, seqId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id'] or fixedCompId is not None:
                if fixedCompId is not None:
                    cifCompId = fixedCompId
                else:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(ps['auth_seq_id'], ps['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), ps['auth_seq_id'].index(seqId))
                    else:
                        idx = ps['auth_seq_id'].index(seqId) if seqId in ps['auth_seq_id'] else ps['seq_id'].index(seqId)
                    cifCompId = ps['comp_id'][idx]
                if self.reasons is not None:
                    if 'non_poly_remap' in self.reasons and cifCompId in self.reasons['non_poly_remap']\
                       and seqId in self.reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], None, chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if (fixedChainId is not None and fixedChainId != chainId) or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.add((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
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
                            idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                            try:
                                seqId_ = ps['auth_seq_id'][idx]
                                cifCompId = ps['comp_id'][idx]
                                updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                                if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((chainId, seqId_, cifCompId, True))
                            except IndexError:
                                pass

        if self.hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId, cifCompId = self.getRealChainSeqId(np, _seqId, None, False)
                if fixedChainId is not None and chainId != fixedChainId:
                    continue
                if self.reasons is not None:
                    if 'seq_id_remap' not in self.reasons and 'chain_seq_id_remap' not in self.reasons:
                        if fixedChainId is not None and fixedChainId != chainId:
                            continue
                    else:
                        if 'chain_seq_id_remap' in self.reasons:
                            fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], chainId, seqId)
                            if fixedChainId is not None and fixedChainId != chainId:
                                continue
                            if fixedSeqId is not None:
                                seqId = _seqId = fixedSeqId
                        if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                            _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], None, seqId)
                            if fixedSeqId is not None:
                                seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(np['auth_seq_id'], np['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), np['auth_seq_id'].index(seqId))
                    else:
                        idx = np['auth_seq_id'].index(seqId) if seqId in np['auth_seq_id'] else np['seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None and chainId != fixedChainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.authToLabelSeq:
                    _, seqId = self.authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                        if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))

            if self.hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None and chainId != fixedChainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is not None and chainId != fixedChainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    chainAssign.add((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0 and (self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT or self.__multiPolymer):
            for ps in self.polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None and chainId != fixedChainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        cifCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, fixedChainId, seqId, cifCompId)
                        if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                            self.authSeqId = 'label_seq_id'
                            self.__setLocalSeqScheme()

        if len(chainAssign) == 0:
            if seqId == 1 or (fixedChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithChainIdWithoutCompId(fixedChainId, seqId, 'H1')
            if (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                              f"{fixedChainId}:{_seqId}:?:{atomId} is not present in the coordinates. "
                              "Please attach ambiguous atom name mapping information generated "
                              f"by 'makeDIST_RST' to the {self.software_name} restraint file.")
            else:
                if self.__monoPolymer and seqId < 1:
                    refChainId = self.polySeq[0]['auth_chain_id']
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                  f"{_seqId}:?:{atomId} is not present in the coordinates. "
                                  f"The residue number '{_seqId}' is not present in polymer sequence "
                                  f"of chain {refChainId} of the coordinates. "
                                  "Please update the sequence in the Macromolecules page.")
                else:
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                  f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates.")
                    compIds = guessCompIdFromAtomId([atomId], self.polySeq, self.nefT)
                    if compIds is not None:
                        if len(compIds) == 1:
                            updatePolySeqRst(self.__polySeqRstFailed, fixedChainId, seqId, compIds[0])
                        else:
                            updatePolySeqRstAmbig(self.__polySeqRstFailedAmbig, fixedChainId, seqId, compIds)

        return list(chainAssign)

    def assignCoordPolymerSequenceWithIndex(self, refChainId: str, seqId: int, compId: str, atomId: str,
                                            index: Optional[int] = None, group: Optional[int] = None) -> Tuple[List[Tuple[str, int, str, bool]], bool]:
        """ Assign polymer sequences of the coordinates.
        """

        if self.has_sequence and self.reasons is None:
            if self.first_resid <= seqId < self.first_resid + len(self.cur_sequence):
                oneLetterCode = self.cur_sequence[seqId - self.first_resid].upper()

                _compId = next(k for k, v in monDict3.items() if v == oneLetterCode)

                if _compId != translateToStdResName(compId, ccU=self.ccU) and _compId != 'X':
                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"Sequence alignment error between the sequence ({seqId}:{_compId}) "
                                  f"and data ({seqId}:{compId}). "
                                  "Please verify the consistency between the internally defined sequence and restraints and re-upload the restraint file(s).")
                    self.has_seq_align_err = True
                    return []

        _refChainId = refChainId

        chainAssign = set()
        asis = preferNonPoly = False

        _seqId = seqId
        _compId = compId

        fixedChainId = fixedSeqId = fixedCompId = None

        self.allow_ext_seq = False

        if self.hasNonPoly:

            resolved = False

            for np in self.__nonPoly:
                if 'alt_comp_id' in np and 'alt_auth_seq_id' in np\
                   and compId in np['alt_comp_id'] and seqId in np['alt_auth_seq_id']:
                    npCompId = np['comp_id'][0]
                    npSeqId = np['auth_seq_id'][0]
                    for ps in self.polySeq:
                        if 'ambig_auth_seq_id' in ps and seqId in ps['ambig_auth_seq_id']:
                            psCompId = ps['comp_id'][ps['auth_seq_id'].index(seqId)]
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(psCompId, atomId, leave_unmatched=True)
                            if details is None:
                                _, _coordAtomSite = self.getCoordAtomSiteOf(ps['auth_chain_id'], seqId, psCompId, cifCheck=self.hasCoord)
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = psCompId
                                    resolved = True
                                    break
                            _, _coordAtomSite = self.getCoordAtomSiteOf(np['auth_chain_id'], npSeqId, npCompId, cifCheck=self.hasCoord)
                            if self.__mrAtomNameMapping is not None:
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, npSeqId, npCompId, atomId, _coordAtomSite)
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(npCompId, atomId, leave_unmatched=True)
                            if details is None:
                                if _coordAtomSite is not None and all(_atomId_ in _coordAtomSite['atom_id'] for _atomId_ in _atomId):
                                    compId = _compId = npCompId
                                    seqId = _seqId = npSeqId
                                    preferNonPoly = resolved = True
                                    break

            if not resolved and compId in ('CYSZ', 'CYZ', 'CYS', 'ION', 'ZN1', 'ZN2')\
               and atomId in zincIonCode:
                znCount = 0
                znSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'ZN':
                        znSeqId = np['auth_seq_id'][0]
                        znCount += 1
                if znCount > 0:
                    compId = _compId = 'ZN'
                    if znCount == 1:
                        seqId = _seqId = znSeqId
                        atomId = 'ZN'
                        resolved = True
                    preferNonPoly = True

            if not resolved and compId in ('CYS', 'CYSC', 'CYC', 'CCA', 'CYO', 'ION', 'CA1', 'CA2')\
               and atomId in calciumIonCode:
                caCount = 0
                caSeqId = None
                for np in self.__nonPoly:
                    if np['comp_id'][0] == 'CA':
                        caSeqId = np['auth_seq_id'][0]
                        caCount += 1
                if caCount > 0:
                    compId = _compId = 'CA'
                    if caCount == 1:
                        seqId = _seqId = caSeqId
                        atomId = 'CA'
                        resolved = True
                    preferNonPoly = True

            if not resolved and len(atomId) > 1 and atomId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == atomId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, atomId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        compId = _compId = atomId
                        preferNonPoly = resolved = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == atomId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                compId = _compId = atomId
                                preferNonPoly = resolved = True

            if not resolved and len(compId) > 1 and compId in SYMBOLS_ELEMENT:
                elemCount = 0
                for np in self.__nonPoly:
                    if np['comp_id'][0] == compId:
                        elemCount += 1
                if elemCount > 0:
                    _, elemSeqId = getMetalCoordOf(self.cR, seqId, compId, compId)
                    if elemSeqId is not None:
                        seqId = _seqId = elemSeqId
                        atomId = _compId = compId
                        preferNonPoly = True
                    elif elemCount == 1:
                        for np in self.__nonPoly:
                            if np['comp_id'][0] == compId:
                                seqId = _seqId = np['auth_seq_id'][0]
                                atomId = _compId = compId
                                preferNonPoly = True

        if self.__splitLigand is not None and len(self.__splitLigand):
            found = False
            for (_, _seqId_, _compId_), ligList in self.__splitLigand.items():
                if _seqId_ != seqId or _compId_ != compId:
                    continue
                for idx, lig in enumerate(ligList):
                    _atomId = atomId
                    if self.__mrAtomNameMapping is not None and compId not in monDict3:
                        _, _, _atomId = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

                    if _atomId in lig['atom_ids']:
                        seqId = _seqId = lig['auth_seq_id']
                        compId = _compId = lig['comp_id']
                        atomId = _atomId
                        preferNonPoly = idx > 0
                        found = True
                        break
                if found:
                    break

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

        compId = self.translateToStdResNameWrapper(_seqId, _compId, preferNonPoly)

        if len(self.__modResidue) > 0:
            modRes = next((modRes for modRes in self.__modResidue
                           if modRes['auth_comp_id'] == compId
                           and (compId != _compId or seqId in (modRes['auth_seq_id'], modRes['seq_id']))), None)
            if modRes is not None:
                compId = modRes['comp_id']

        if self.reasons is not None:
            if 'non_poly_remap' in self.reasons and _compId in self.reasons['non_poly_remap']\
               and seqId in self.reasons['non_poly_remap'][_compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.reasons['non_poly_remap'], None, refChainId, seqId, _compId)
                refChainId = fixedChainId
                preferNonPoly = True
            if 'branched_remap' in self.reasons and seqId in self.reasons['branched_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['branched_remap'], seqId)
                refChainId = fixedChainId
                preferNonPoly = True
            if not preferNonPoly:
                if 'chain_id_remap' in self.reasons:  # and seqId in self.reasons['chain_id_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_remap'], seqId)
                    if seqId not in self.reasons['chain_id_remap']:
                        self.allow_ext_seq = True
                    refChainId = fixedChainId
                elif 'chain_id_clone' in self.reasons:  # and seqId in self.reasons['chain_id_clone']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.reasons['chain_id_clone'], seqId)
                    if seqId not in self.reasons['chain_id_clone']:
                        self.allow_ext_seq = True
                    refChainId = fixedChainId
                elif 'seq_id_remap' in self.reasons\
                        or 'chain_seq_id_remap' in self.reasons\
                        or 'ext_chain_seq_id_remap' in self.reasons:
                    if 'ext_chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId, fixedCompId =\
                            retrieveRemappedSeqIdAndCompId(self.reasons['ext_chain_seq_id_remap'], refChainId, seqId,
                                                           compId if compId in monDict3 else None)
                        self.allow_ext_seq = fixedCompId is not None
                        if fixedSeqId is not None:
                            refChainId = fixedChainId
                    if fixedSeqId is None and 'chain_seq_id_remap' in self.reasons:
                        fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.reasons['chain_seq_id_remap'], refChainId, seqId,
                                                                         compId if compId in monDict3 else None)
                        if fixedSeqId is not None:
                            refChainId = fixedChainId
                    if fixedSeqId is None and 'seq_id_remap' in self.reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.reasons['seq_id_remap'], _refChainId, seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        updatePolySeqRst(self.__polySeqRst, self.polySeq[0]['chain_id'] if refChainId is None else refChainId, _seqId, compId, _compId)

        types = self.csStat.getTypeOfCompId(compId)
        if all(not t for t in types) or compId in ('MTS', 'ORI'):
            types = None
        elif compId != _compId:
            if types != self.csStat.getTypeOfCompId(_compId):
                types = None

        def comp_id_unmatched_with(ps, cif_comp_id):
            if 'alt_comp_id' in ps and self.csStat.peptideLike(cif_comp_id) and compId.startswith('D') and len(compId) >= 3\
               and self.ccU.lastChemCompDict['_chem_comp.type'].upper() == 'D-PEPTIDE LINKING':
                revertPolySeqRst(self.__polySeqRst, ps['chain_id'] if fixedChainId is None else fixedChainId, _seqId, compId)

            if types is None or ('alt_comp_id' in ps and _compId in ps['alt_comp_id']):
                return False
            if compId not in monDict3 and cif_comp_id not in monDict3:
                return False
            return types != self.csStat.getTypeOfCompId(cif_comp_id)

        def comp_id_in_polymer(np):
            return (_seqId == 1
                    and ((compId.endswith('-N') and all(c in np['comp_id'][0] for c in compId.split('-')[0]))
                         or (np['comp_id'][0] == 'PCA' and 'P' == compId[0] and ('GL' in compId or 'N' in compId))))\
                or (compId in monDict3
                    and any(compId in ps['comp_id'] for ps in self.polySeq)
                    and compId not in np['comp_id'])

        if refChainId is not None or refChainId != _refChainId:
            if any(True for ps in self.polySeq if ps['auth_chain_id'] == _refChainId):
                fixedChainId = _refChainId
            elif self.hasNonPolySeq:
                if any(True for np in self.__nonPolySeq if np['auth_chain_id'] == _refChainId):
                    fixedChainId = _refChainId

        for ps in self.polySeq:
            if preferNonPoly:
                continue
            chainId, seqId, cifCompId = self.getRealChainSeqId(ps, _seqId, compId)
            if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                if chainId != self.__chainNumberDict[refChainId]:
                    continue
            if self.reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    if fixedSeqId is not None:
                        seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId <= 0 and self.__shiftNonPosSeq is not None and chainId in self.__shiftNonPosSeq:
                seqId -= 1
            if seqId in ps['auth_seq_id'] or fixedCompId is not None:
                if fixedCompId is not None:
                    cifCompId = origCompId = fixedCompId
                else:
                    if cifCompId is not None:
                        idx = next((_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(ps['auth_seq_id'], ps['comp_id']))
                                    if _seqId_ == seqId and _cifCompId_ == cifCompId), ps['auth_seq_id'].index(seqId))
                    else:
                        idx = ps['auth_seq_id'].index(seqId) if seqId in ps['auth_seq_id'] else ps['seq_id'].index(seqId)
                    cifCompId = ps['comp_id'][idx]
                    origCompId = ps['auth_comp_id'][idx]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                if cifCompId != compId:
                    if (self.__shiftNonPosSeq is None or chainId not in self.__shiftNonPosSeq)\
                       and seqId <= 0 and seqId - 1 in ps['auth_seq_id']\
                       and compId == ps['comp_id'][ps['auth_seq_id'].index(seqId - 1)]:
                        seqId -= 1
                        if self.__shiftNonPosSeq is None:
                            self.__shiftNonPosSeq = {}
                        self.__shiftNonPosSeq[chainId] = True
                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                    if compId in compIds:
                        cifCompId = compId
                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                          if _seqId == seqId and _compId == compId)
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.add((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId
                else:
                    _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                    if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                        chainAssign.add((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId

            elif 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']:
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
                            idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                            try:
                                seqId_ = ps['auth_seq_id'][idx]
                                cifCompId = ps['comp_id'][idx]
                                origCompId = ps['auth_comp_id'][idx]
                                if comp_id_unmatched_with(ps, cifCompId):
                                    continue
                                if cifCompId != compId:
                                    compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                                    if compId in compIds:
                                        cifCompId = compId
                                        origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                          if _seqId == seqId and _compId == compId)
                                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, cifCompId, cifCheck=self.hasCoord)
                                    atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                                if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                    if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                        chainAssign.add((chainId, seqId_, cifCompId, True))
                                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                            self.__chainNumberDict[refChainId] = chainId
                                else:
                                    _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                    if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                        chainAssign.add((chainId, seqId_, cifCompId, True))
                                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                            self.__chainNumberDict[refChainId] = chainId
                            except IndexError:
                                pass

        if self.hasNonPolySeq:
            ligands = 0
            if self.hasNonPoly:
                for np in self.__nonPoly:
                    ligands += np['comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        ligands += np['comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(_compId)
                if ligands == 0:
                    for np in self.__nonPoly:
                        if 'alt_comp_id' in np:
                            ligands += np['alt_comp_id'].count(compId)
                    if ligands == 1:
                        _compId = compId
                if ligands == 0 and len(chainAssign) == 0 and _compId not in monDict3:
                    __compId = None
                    for np in self.__nonPoly:
                        for ligand in np['comp_id']:
                            __compId = translateToLigandName(_compId, ligand, self.ccU)
                            if __compId == ligand:
                                ligands += 1
                    if ligands == 1:
                        compId = _compId = __compId
                    elif self.__monoNonPoly and self.ccU.updateChemCompDict(_compId, False):
                        if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS':
                            compId = _compId = self.__nonPoly[0]['comp_id'][0]
                            ligands = 1
                        elif _compId == 'ION':
                            if self.__nonPoly[0]['comp_id'][0] in SYMBOLS_ELEMENT:
                                compId = _compId = self.__nonPoly[0]['comp_id'][0]
                                ligands = 1
                if self.reasons is None and atomId in self.__uniqAtomIdToSeqKey:
                    seqKey = self.__uniqAtomIdToSeqKey[atomId]
                    if _seqId != seqKey[1]:
                        if 'non_poly_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['non_poly_remap'] = {}
                        if _compId not in self.reasonsForReParsing['non_poly_remap']:
                            self.reasonsForReParsing['non_poly_remap'][_compId] = {}
                        if _seqId not in self.reasonsForReParsing['non_poly_remap'][_compId]:
                            self.reasonsForReParsing['non_poly_remap'][_compId][_seqId] =\
                                {'chain_id': seqKey[0],
                                 'seq_id': seqKey[1],
                                 'original_chain_id': refChainId}
            for np in self.__nonPolySeq:
                chainId, seqId, cifCompId = self.getRealChainSeqId(np, _seqId, compId, False)
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if self.reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        if fixedSeqId is not None:
                            seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if comp_id_in_polymer(np):
                    continue
                if 'alt_auth_seq_id' in np and seqId not in np['auth_seq_id'] and seqId in np['alt_auth_seq_id']:
                    try:
                        seqId = next(_seqId_ for _seqId_, _altSeqId_ in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _altSeqId_ == seqId)
                    except StopIteration:
                        pass
                if seqId in np['auth_seq_id']\
                   or (ligands == 1 and (_compId in np['comp_id'] or ('alt_comp_id' in np and _compId in np['alt_comp_id']))):
                    if ligands == 1 and cifCompId is None:
                        cifCompId = _compId
                    idx = -1
                    try:
                        if cifCompId is not None:
                            idx = next(_idx for _idx, (_seqId_, _cifCompId_) in enumerate(zip(np['auth_seq_id'], np['comp_id']))
                                       if (_seqId_ == seqId or ligands == 1) and _cifCompId_ == cifCompId)
                            if ligands == 1:
                                seqId = np['auth_seq_id'][idx]
                    except StopIteration:
                        pass
                    if idx == -1:
                        idx = np['auth_seq_id'].index(seqId) if seqId in np['auth_seq_id']\
                            else np['seq_id'].index(seqId) if seqId in np['seq_id'] else 0
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    seqId = np['auth_seq_id'][idx]
                    if cifCompId in ('ZN', 'CA') and atomId[0] in protonBeginCode:  # 2loa
                        continue
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, _seqId, origCompId, atomId, coordAtomSite)
                    if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                        if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                    else:
                        _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                        if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                            if (ligands == 1 or cifCompId in HEME_LIKE_RES_NAMES) and any(a[3] for a in chainAssign):
                                chainAssign.clear()
                            chainAssign.add((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            for ps in self.polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.authToLabelSeq:
                    _, seqId = self.authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

            if self.hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                        if chainId != self.__chainNumberDict[refChainId]:
                            continue
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    if comp_id_in_polymer(np):
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.authToLabelSeq:
                        _, seqId = self.authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, cifCompId, cifCheck=self.hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                                if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                            else:
                                _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                                if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                    chainAssign.add((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                if preferNonPoly:
                    continue
                chainId = ps['auth_chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    if comp_id_unmatched_with(ps, cifCompId):
                        continue
                    if cifCompId != compId:
                        if cifCompId in monDict3 and compId in monDict3:
                            continue
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                        if compId in compIds:
                            cifCompId = compId
                    chainAssign.add((chainId, _seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and (self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT or self.__multiPolymer):
            for ps in self.polySeq:
                if preferNonPoly:
                    continue
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__labelToAuthSeq:
                    _, seqId = self.__labelToAuthSeq[seqKey]
                    if seqId in ps['auth_seq_id']:
                        idx = ps['seq_id'].index(_seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if comp_id_unmatched_with(ps, cifCompId):
                            continue
                        if cifCompId != compId:
                            compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == seqId]
                            if compId in compIds:
                                cifCompId = compId
                                origCompId = next(origCompId for _seqId, _compId, origCompId in zip(ps['auth_seq_id'], ps['comp_id'], ps['auth_comp_id'])
                                                  if _seqId == seqId and _compId == compId)
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, cifCompId, cifCheck=self.hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId, 'MTS', 'ORI'):
                            if len(self.nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                if compId in (cifCompId, origCompId):
                                    self.authSeqId = 'label_seq_id'
                                    self.__setLocalSeqScheme()
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                        else:
                            _atomId, _, details = self.nefT.get_valid_star_atom(cifCompId, atomId)
                            if len(_atomId) > 0 and (details is None or _compId not in monDict3):
                                chainAssign.add((ps['auth_chain_id'], seqId, cifCompId, True))
                                self.authSeqId = 'label_seq_id'
                                self.__setLocalSeqScheme()
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            if seqId == 1 or (refChainId, seqId - 1) in self.__coordUnobsRes:
                if atomId in aminoProtonCode and atomId != 'H1':
                    return self.assignCoordPolymerSequenceWithIndex(refChainId, seqId, compId, 'H1')
            auth_seq_id_list = list(filter(None, self.polySeq[0]['auth_seq_id']))
            min_auth_seq_id = max_auth_seq_id = UNREAL_AUTH_SEQ_NUM
            if len(auth_seq_id_list) > 0:
                min_auth_seq_id = min(auth_seq_id_list)
                max_auth_seq_id = max(auth_seq_id_list)
            if self.__monoPolymer\
               and (seqId < 1
                    or (compId == 'ACE' and seqId == min_auth_seq_id - 1)
                    or (compId == 'NH2' and seqId == max_auth_seq_id + 1)
                    or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT)):
                refChainId = self.polySeq[0]['auth_chain_id']
                if (compId == 'ACE' and seqId == min_auth_seq_id - 1)\
                   or (compId == 'NH2' and seqId == max_auth_seq_id + 1)\
                   or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                       and (min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id
                            or max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ)):
                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                  f"of chain {refChainId} of the coordinates. "
                                  "Please update the sequence in the Macromolecules page.")
                    resKey = (_seqId, _compId)
                    if resKey not in self.extResKey:
                        self.extResKey.append(resKey)
                    chainAssign.add((refChainId, _seqId, compId, True))
                    asis = True
                elif compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT:
                    self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                  f"of chain {refChainId} of the coordinates. "
                                  "Please update the sequence in the Macromolecules page.")
                    resKey = (_seqId, _compId)
                    if resKey not in self.extResKey:
                        self.extResKey.append(resKey)
                else:
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"{_seqId}:{_compId}:{atomId} is not present in the coordinates. "
                                  f"The residue number '{_seqId}' is not present in polymer sequence "
                                  f"of chain {refChainId} of the coordinates. "
                                  "Please update the sequence in the Macromolecules page.")
            else:
                ext_seq = False
                if (compId in monDict3 or compId in ('ACE', 'NH2')) and (self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                                                                         or len(atomId) == 1):
                    refChainIds = []
                    _auth_seq_id_list = auth_seq_id_list
                    for idx, ps in enumerate(self.polySeq):
                        if idx > 0:
                            auth_seq_id_list = list(filter(None, ps['auth_seq_id']))
                            _auth_seq_id_list.extend(auth_seq_id_list)
                        if len(auth_seq_id_list) > 0:
                            if idx > 0:
                                min_auth_seq_id = min(auth_seq_id_list)
                                max_auth_seq_id = max(auth_seq_id_list)
                            if min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id\
                               and (compId in monDict3 or (compId == 'ACE' and seqId == min_auth_seq_id - 1)):
                                refChainIds.append(ps['auth_chain_id'])
                                ext_seq = True
                            elif max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ\
                                    and (compId in monDict3 or (compId == 'NH2' and seqId == max_auth_seq_id + 1)):
                                refChainIds.append(ps['auth_chain_id'])
                                ext_seq = True
                            elif self.reasons is None and compId in monDict3 and atomId == 'H' and seqId < min_auth_seq_id\
                                    and self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT:
                                refChainIds.append(ps['auth_chain_id'])
                                ext_seq = True
                    if ext_seq and seqId in _auth_seq_id_list:
                        ext_seq = False
                if self.allow_ext_seq:
                    refChainIds = [fixedChainId]
                    ext_seq = True
                if ext_seq:
                    refChainId = refChainIds[0] if len(refChainIds) == 1 else refChainIds
                    if not self.allow_ext_seq:
                        self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint(n=index, g=group)}"
                                      f"The residue '{_seqId}:{_compId}' is not present in polymer sequence "
                                      f"of chain {refChainId} of the coordinates. "
                                      "Please update the sequence in the Macromolecules page.")
                    resKey = (_seqId, _compId)
                    if resKey not in self.extResKey:
                        self.extResKey.append(resKey)
                    if isinstance(refChainId, str):
                        chainAssign.add((refChainId, _seqId, compId, True))
                    else:
                        for _refChainId in refChainIds:
                            chainAssign.add((_refChainId, _seqId, compId, True))
                    asis = True
                else:
                    self.f.append(f"[Atom not found] {self.getCurrentRestraint(n=index, g=group)}"
                                  f"{_seqId}:{_compId}:{atomId} is not present in the coordinates.")
                updatePolySeqRst(self.__polySeqRstFailed, self.polySeq[0]['chain_id'] if refChainId is None else refChainId, _seqId, compId, _compId)

        elif any(True for ca in chainAssign if ca[0] == refChainId) and any(True for ca in chainAssign if ca[0] != refChainId):
            _chainAssign = copy.copy(chainAssign)
            for _ca in _chainAssign:
                if _ca[0] != refChainId:
                    chainAssign.remove(_ca)

        return list(chainAssign), asis

    def selectCoordAtoms(self, chainAssign: List[Tuple[str, int, str, bool]], seqId: int, compId: str, atomId: str,
                         allowAmbig: bool = True, enableWarning: bool = True, offset: int = 0):
        """ Select atoms of the coordinates.
        """

        atomSelection = []

        authAtomId = atomId

        __compId = compId
        __atomId = atomId

        if compId is not None:

            if self.__mrAtomNameMapping is not None and compId not in monDict3:
                __atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

            if self.reasons is not None:
                if 'ambig_atom_id_remap' in self.reasons and compId in self.reasons['ambig_atom_id_remap']\
                   and atomId in self.reasons['ambig_atom_id_remap'][compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.reasons['ambig_atom_id_remap'][compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
                if 'unambig_atom_id_remap' in self.reasons and compId in self.reasons['unambig_atom_id_remap']\
                   and atomId in self.reasons['unambig_atom_id_remap'][compId]:
                    atomIds = self.reasons['unambig_atom_id_remap'][compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                            atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

            if len(self.ambigAtomNameMapping) > 0:
                if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.ambigAtomNameMapping[compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
            if len(self.unambigAtomNameMapping) > 0:
                if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                    atomIds = self.unambigAtomNameMapping[compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                            atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

            compId = self.translateToStdResNameWrapper(seqId, __compId)

        for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:

            if offset != 0:
                cifSeqId += offset
                cifCompId = compId

            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId, asis=self.__preferAuthSeq)

            if self.cur_subtype == 'dist' and __compId is not None\
               and (__compId.startswith('MTS') or __compId.startswith('ORI')) and cifCompId != __compId:
                if __atomId[0] in ('O', 'N'):

                    if cifCompId == 'CYS':
                        atomId = 'SG'
                    elif cifCompId == 'SER':
                        atomId = 'OG'
                    elif cifCompId == 'GLU':
                        atomId = 'OE2'
                    elif cifCompId == 'ASP':
                        atomId = 'OD2'
                    elif cifCompId == 'GLN':
                        atomId = 'NE2'
                    elif cifCompId == 'ASN':
                        atomId = 'ND2'
                    elif cifCompId == 'LYS':
                        atomId = 'NZ'
                    elif cifCompId == 'THR':
                        atomId = 'OG1'
                    elif compId == 'HIS':
                        atomId = 'NE2'
                    elif compId == 'R1A':
                        atomId = 'O1'
                    elif compId == '3X9':
                        atomId = 'OAH'

                elif self.csStat.peptideLike(cifCompId):
                    atomId = 'CA'

            if self.__mrAtomNameMapping is not None and cifCompId not in monDict3:
                __atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, cifSeqId, cifCompId, atomId, coordAtomSite)
                if atomId != __atomId and coordAtomSite is not None\
                   and (__atomId in coordAtomSite['atom_id'] or (__atomId.endswith('%') and __atomId[:-1] + '2' in coordAtomSite['atom_id'])):
                    atomId = __atomId
                elif self.reasons is not None and 'branched_remap' in self.reasons:
                    _seqId = retrieveOriginalSeqIdFromMRMap(self.reasons['branched_remap'], chainId, cifSeqId)
                    if _seqId != cifSeqId:
                        _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, _seqId, cifCompId, atomId, None, coordAtomSite)

            _atomIdSet, _atomId = [], []
            skip = False
            for atomId_ in atomId.split('|'):
                if len(_atomId) > 0:
                    _atomId = []

                if not isPolySeq and atomId_[0] in ('Q', 'M') and coordAtomSite is not None:
                    key = (chainId, cifSeqId, compId, atomId_)
                    if key in self.__cachedDictForStarAtom:
                        _atomId = deepcopy(self.__cachedDictForStarAtom[key])
                    else:
                        pattern = re.compile(fr'H{atomId_[1:]}\d+') if compId in monDict3 else re.compile(fr'H{atomId_[1:]}\S?$')
                        atomIdList = [a for a in coordAtomSite['atom_id'] if re.search(pattern, a) and a[-1] in ('1', '2', '3')]
                        if len(atomIdList) > 1:
                            hvyAtomIdList = [a for a in coordAtomSite['atom_id'] if a[0] in ('C', 'N')]
                            hvyAtomId = None
                            for canHvyAtomId in hvyAtomIdList:
                                if isStructConn(self.cR, chainId, cifSeqId, canHvyAtomId, chainId, cifSeqId, atomIdList[0],
                                                representativeModelId=self.representativeModelId, representativeAltId=self.representativeAltId,
                                                modelNumName=self.modelNumName):
                                    hvyAtomId = canHvyAtomId
                                    break
                            if hvyAtomId is not None:
                                for _atomId_ in atomIdList:
                                    if isStructConn(self.cR, chainId, cifSeqId, hvyAtomId, chainId, cifSeqId, _atomId_,
                                                    representativeModelId=self.representativeModelId, representativeAltId=self.representativeAltId,
                                                    modelNumName=self.modelNumName):
                                        _atomId.append(_atomId_)
                        if len(_atomId) > 1:
                            self.__cachedDictForStarAtom[key] = deepcopy(_atomId)
                if len(_atomId) > 1:
                    details = None
                else:
                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId_, leave_unmatched=True)
                    if details is not None:
                        if atomId_ != __atomId:
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, __atomId, leave_unmatched=True)
                        elif len(atomId_) > 1 and not atomId_[-1].isalpha() and (atomId_[0] in pseProBeginCode or atomId_[0] in ('C', 'N', 'P', 'F')):
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId_[:-1], leave_unmatched=True)
                            if atomId_[-1].isdigit() and int(atomId_[-1]) <= len(_atomId):
                                _atomId = [_atomId[int(atomId_[-1]) - 1]]

                if details is not None or atomId_.endswith('"'):
                    _atomId_ = translateToStdAtomName(atomId_, cifCompId, ccU=self.ccU, unambig=self.cur_subtype != 'dist')
                    if _atomId_ != atomId_:
                        if atomId_.startswith('HT') and len(_atomId_) == 2:
                            _atomId_ = 'H'
                        __atomId__ = self.nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                        if coordAtomSite is not None:
                            if any(True for _atomId_ in __atomId__ if _atomId_ in coordAtomSite['atom_id']):
                                _atomId = __atomId__
                            elif __atomId__[0][0] in protonBeginCode:
                                __bondedTo = self.ccU.getBondedAtoms(cifCompId, __atomId__[0])
                                if len(__bondedTo) > 0 and __bondedTo[0] in coordAtomSite['atom_id']:
                                    _atomId = __atomId__
                    elif coordAtomSite is not None:
                        _atomId = []
                # _atomId = self.nefT.get_valid_star_atom(cifCompId, atomId_)[0]

                if coordAtomSite is not None\
                   and not any(True for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id']):
                    if atomId_ in coordAtomSite['atom_id']:
                        _atomId = [atomId_]
                    elif seqId == 1 and atomId_ == 'H1' and self.csStat.peptideLike(compId) and 'H' in coordAtomSite['atom_id']:
                        _atomId = ['H']

                if authAtomId.upper().startswith('CEN') and len(_atomId) == 0:
                    peptide, nucleotide, carbohydrate = self.csStat.getTypeOfCompId(cifCompId)
                    _atomId = self.csStat.getCentroidAtoms(cifCompId, False, peptide, nucleotide, carbohydrate)

                if coordAtomSite is None and not isPolySeq and self.hasNonPolySeq:
                    try:
                        for np in self.__nonPolySeq:
                            if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                                cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                                if coordAtomSite is not None:
                                    break
                    except ValueError:
                        pass

                if coordAtomSite is not None:
                    atomSiteAtomId = coordAtomSite['atom_id']
                    if len(_atomId) == 0 and __atomId in zincIonCode and 'ZN' in atomSiteAtomId:
                        compId = atomId_ = 'ZN'
                        _atomId = [atomId_]
                    elif len(_atomId) == 0 and __atomId in calciumIonCode and 'CA' in atomSiteAtomId:
                        compId = atomId_ = 'CA'
                        _atomId = [atomId_]
                    elif not any(_atomId_ in atomSiteAtomId for _atomId_ in _atomId):
                        pass
                    elif atomId_[0] not in pseProBeginCode and not all(_atomId in atomSiteAtomId for _atomId in _atomId):
                        _atomId = [_atomId_ for _atomId_ in _atomId if _atomId_ in atomSiteAtomId]

                lenAtomId = len(_atomId)
                if self.reasons is not None and compId != cifCompId and __compId == cifCompId:
                    compId = cifCompId
                if compId != cifCompId and compId in monDict3 and cifCompId in monDict3:
                    multiChain = insCode = False
                    if len(chainAssign) > 0:
                        chainIds = [ca[0] for ca in chainAssign]
                        multiChain = len(collections.Counter(chainIds).most_common()) > 1
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == cifSeqId]
                        if compId in compIds:
                            insCode = True
                            cifCompId = compId
                    if not multiChain and not insCode:
                        if self.__preferAuthSeq:
                            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId, asis=False)
                            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                                if lenAtomId > 0 and _atomId[0] in _coordAtomSite['atom_id']:
                                    self.authSeqId = 'label_seq_id'
                                    self.__setLocalSeqScheme()
                                    skip = True
                                    break
                        self.f.append(f"[Sequence mismatch] {self.getCurrentRestraint()}"
                                      f"Residue name {__compId!r} of the restraint does not match with {chainId}:{cifSeqId}:{cifCompId} of the coordinates.")
                        skip = True
                        break

                if compId != cifCompId and cifCompId in monDict3 and not isPolySeq:
                    skip = True
                    break

                if lenAtomId == 0 and not isPolySeq and cifCompId in SYMBOLS_ELEMENT:
                    _atomId = [cifCompId]
                    lenAtomId = 1

                if lenAtomId > 0:
                    _atomIdSet.append(_atomId)

            if skip:
                continue

            if len(_atomIdSet) > 1:
                _atomId = []
                for _atomId_ in _atomIdSet:
                    _atomId.extend(_atomId_)
                lenAtomId = len(_atomId)

            if lenAtomId == 0 and not isPolySeq and cifCompId in SYMBOLS_ELEMENT:
                _atomId = [cifCompId]
                lenAtomId = 1

            if lenAtomId == 0:
                if compId != cifCompId and any(True for item in chainAssign if item[2] == compId):
                    continue
                if seqId == 1 and isPolySeq and cifCompId == 'ACE' and cifCompId != compId and offset == 0:
                    self.selectCoordAtoms(chainAssign, seqId, compId, atomId, allowAmbig, enableWarning, offset=1)
                    return
                if enableWarning:
                    self.f.append(f"[Invalid atom nomenclature] {self.getCurrentRestraint()}"
                                  f"{seqId}:{__compId}:{__atomId} is invalid atom nomenclature.")
                    compIds = guessCompIdFromAtomId([__atomId], self.polySeq, self.nefT)
                    if compIds is not None:
                        if len(compIds) == 1:
                            updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, compIds[0])
                        else:
                            updatePolySeqRstAmbig(self.__polySeqRstFailedAmbig, chainId, seqId, compIds)
                continue
            if lenAtomId > 1 and not allowAmbig:
                if enableWarning:
                    self.f.append(f"[Invalid atom selection] {self.getCurrentRestraint()}"
                                  f"Ambiguous atom selection '{seqId}:{__compId}:{__atomId}' is not allowed as a angle restraint.")
                continue

            if __compId != cifCompId and __compId not in self.__compIdMap:
                self.__compIdMap[__compId] = cifCompId

            for cifAtomId in _atomId:

                if seqKey in self.__coordUnobsRes and cifCompId in monDict3 and self.reasons is not None and 'non_poly_remap' in self.reasons:
                    if self.ccU.updateChemCompDict(cifCompId):
                        try:
                            next(cca for cca in self.ccU.lastAtomList
                                 if cca[self.ccU.ccaAtomId] == cifAtomId and cca[self.ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            continue
                        try:
                            if len(authAtomId) > len(cifAtomId):
                                next(cca for cca in self.ccU.lastAtomList
                                     if cca[self.ccU.ccaAtomId] == authAtomId and cca[self.ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            break

                if authAtomId in ('H', 'HN') and cifAtomId in ('HN1', 'HN2', 'HNA') and self.csStat.peptideLike(cifCompId)\
                   and coordAtomSite is not None and cifAtomId not in coordAtomSite['atom_id']:
                    if cifAtomId in ('HN2', 'HNA'):
                        if 'H2' not in coordAtomSite['atom_id']:
                            continue
                        cifAtomId = 'H2'
                    if cifAtomId == 'HN1' and 'H' in coordAtomSite['atom_id']:
                        cifAtomId = 'H'

                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                                      'atom_id': cifAtomId, 'auth_atom_id': authAtomId})

                _cifAtomId, asis = self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                if asis:
                    atomSelection[-1]['asis'] = True
                if cifAtomId != _cifAtomId:
                    atomSelection[-1]['atom_id'] = _cifAtomId
                    if _cifAtomId.startswith('Ignorable'):
                        atomSelection.pop()

        if len(atomSelection) > 0:
            self.atomSelectionSet.append(atomSelection)

    def selectCoordAtomsWithIndex(self, chainAssign: List[Tuple[str, int, str, bool]], seqId: int, compId: str, atomId: str,
                                  allowAmbig: bool = True, index: Optional[int] = None, group: Optional[int] = None, offset: int = 0):
        """ Select atoms of the coordinates.
        """

        atomSelection = []

        authAtomId = atomId

        __compId = compId
        __atomId = atomId

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            __atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, seqId, compId, atomId)

        compId = self.translateToStdResNameWrapper(seqId, __compId)

        for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:

            if offset != 0:
                cifSeqId += offset
                cifCompId = compId

            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId, asis=self.__preferAuthSeq)

            if self.cur_subtype == 'dist' and __compId is not None\
               and (__compId.startswith('MTS') or __compId.startswith('ORI')) and cifCompId != __compId:
                if __atomId[0] in ('O', 'N'):

                    if cifCompId == 'CYS':
                        atomId = 'SG'
                    elif cifCompId == 'SER':
                        atomId = 'OG'
                    elif cifCompId == 'GLU':
                        atomId = 'OE2'
                    elif cifCompId == 'ASP':
                        atomId = 'OD2'
                    elif cifCompId == 'GLN':
                        atomId = 'NE2'
                    elif cifCompId == 'ASN':
                        atomId = 'ND2'
                    elif cifCompId == 'LYS':
                        atomId = 'NZ'
                    elif cifCompId == 'THR':
                        atomId = 'OG1'
                    elif compId == 'HIS':
                        atomId = 'NE2'
                    elif compId == 'R1A':
                        atomId = 'O1'
                    elif compId == '3X9':
                        atomId = 'OAH'

                elif self.csStat.peptideLike(cifCompId):
                    atomId = 'CA'

            if self.__mrAtomNameMapping is not None and cifCompId not in monDict3:
                __atomId = retrieveAtomIdFromMRMap(self.ccU, self.__mrAtomNameMapping, cifSeqId, cifCompId, atomId, coordAtomSite)
                if atomId != __atomId and coordAtomSite is not None\
                   and (__atomId in coordAtomSite['atom_id'] or (__atomId.endswith('%') and __atomId[:-1] + '2' in coordAtomSite['atom_id'])):
                    atomId = __atomId
                elif self.reasons is not None and 'branched_remap' in self.reasons:
                    _seqId = retrieveOriginalSeqIdFromMRMap(self.reasons['branched_remap'], chainId, cifSeqId)
                    if _seqId != cifSeqId:
                        _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.__mrAtomNameMapping, _seqId, cifCompId, atomId, None, coordAtomSite)

            _atomIdSet, _atomId = [], []
            skip = False
            for atomId_ in atomId.split('|'):
                if len(_atomId) > 0:
                    _atomId = []

                if not isPolySeq and atomId_[0] in ('Q', 'M') and coordAtomSite is not None:
                    key = (chainId, cifSeqId, compId, atomId_)
                    if key in self.__cachedDictForStarAtom:
                        _atomId = deepcopy(self.__cachedDictForStarAtom[key])
                    else:
                        pattern = re.compile(fr'H{atomId_[1:]}\d+') if compId in monDict3 else re.compile(fr'H{atomId_[1:]}\S?$')
                        atomIdList = [a for a in coordAtomSite['atom_id'] if re.search(pattern, a) and a[-1] in ('1', '2', '3')]
                        if len(atomIdList) > 1:
                            hvyAtomIdList = [a for a in coordAtomSite['atom_id'] if a[0] in ('C', 'N')]
                            hvyAtomId = None
                            for canHvyAtomId in hvyAtomIdList:
                                if isStructConn(self.cR, chainId, cifSeqId, canHvyAtomId, chainId, cifSeqId, atomIdList[0],
                                                representativeModelId=self.representativeModelId, representativeAltId=self.representativeAltId,
                                                modelNumName=self.modelNumName):
                                    hvyAtomId = canHvyAtomId
                                    break
                            if hvyAtomId is not None:
                                for _atomId_ in atomIdList:
                                    if isStructConn(self.cR, chainId, cifSeqId, hvyAtomId, chainId, cifSeqId, _atomId_,
                                                    representativeModelId=self.representativeModelId, representativeAltId=self.representativeAltId,
                                                    modelNumName=self.modelNumName):
                                        _atomId.append(_atomId_)
                        if len(_atomId) > 1:
                            self.__cachedDictForStarAtom[key] = deepcopy(_atomId)
                if len(_atomId) > 1:
                    details = None
                else:
                    _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId_, leave_unmatched=True)
                    if details is not None:
                        if atomId_ != __atomId:
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, __atomId, leave_unmatched=True)
                        elif len(atomId_) > 1 and not atomId_[-1].isalpha() and (atomId_[0] in pseProBeginCode or atomId_[0] in ('C', 'N', 'P', 'F')):
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId_[:-1], leave_unmatched=True)
                            if atomId_[-1].isdigit() and int(atomId_[-1]) <= len(_atomId):
                                _atomId = [_atomId[int(atomId_[-1]) - 1]]

                if details is not None or atomId_.endswith('"'):
                    _atomId_ = translateToStdAtomName(atomId_, cifCompId, ccU=self.ccU, unambig=self.cur_subtype != 'dist')
                    if _atomId_ != atomId_:
                        if atomId_.startswith('HT') and len(_atomId_) == 2:
                            _atomId_ = 'H'
                        __atomId__ = self.nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                        if coordAtomSite is not None:
                            if any(True for _atomId_ in __atomId__ if _atomId_ in coordAtomSite['atom_id']):
                                _atomId = __atomId__
                            elif __atomId__[0][0] in protonBeginCode:
                                __bondedTo = self.ccU.getBondedAtoms(cifCompId, __atomId__[0])
                                if len(__bondedTo) > 0 and __bondedTo[0] in coordAtomSite['atom_id']:
                                    _atomId = __atomId__
                    elif coordAtomSite is not None:
                        _atomId = []
                # _atomId = self.nefT.get_valid_star_atom(cifCompId, atomId_)[0]

                if coordAtomSite is not None\
                   and not any(True for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id']):
                    if atomId_ in coordAtomSite['atom_id']:
                        _atomId = [atomId_]
                    elif seqId == 1 and atomId_ == 'H1' and self.csStat.peptideLike(compId) and 'H' in coordAtomSite['atom_id']:
                        _atomId = ['H']

                if coordAtomSite is None and not isPolySeq and self.hasNonPolySeq:
                    try:
                        for np in self.__nonPolySeq:
                            if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                                cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                                seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                                if coordAtomSite is not None:
                                    break
                    except ValueError:
                        pass

                if coordAtomSite is not None:
                    atomSiteAtomId = coordAtomSite['atom_id']
                    if len(_atomId) == 0 and __atomId in zincIonCode and 'ZN' in atomSiteAtomId:
                        compId = atomId_ = 'ZN'
                        _atomId = [atomId_]
                    elif len(_atomId) == 0 and __atomId in calciumIonCode and 'CA' in atomSiteAtomId:
                        compId = atomId_ = 'CA'
                        _atomId = [atomId_]
                    elif not any(_atomId_ in atomSiteAtomId for _atomId_ in _atomId):
                        pass
                    elif atomId_[0] not in pseProBeginCode and not all(_atomId in atomSiteAtomId for _atomId in _atomId):
                        _atomId = [_atomId_ for _atomId_ in _atomId if _atomId_ in atomSiteAtomId]

                lenAtomId = len(_atomId)
                if self.reasons is not None and compId != cifCompId and __compId == cifCompId:
                    compId = cifCompId
                if compId != cifCompId and compId in monDict3 and cifCompId in monDict3:
                    multiChain = insCode = False
                    if len(chainAssign) > 0:
                        chainIds = [ca[0] for ca in chainAssign]
                        multiChain = len(collections.Counter(chainIds).most_common()) > 1
                    ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                    if ps is not None:
                        compIds = [_compId for _seqId, _compId in zip(ps['auth_seq_id'], ps['comp_id']) if _seqId == cifSeqId]
                        if compId in compIds:
                            insCode = True
                            cifCompId = compId
                    if not multiChain and not insCode:
                        if self.__preferAuthSeq:
                            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId, asis=False)
                            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                                if lenAtomId > 0 and _atomId[0] in _coordAtomSite['atom_id']:
                                    self.authSeqId = 'label_seq_id'
                                    self.__setLocalSeqScheme()
                                    skip = True
                                    break
                        self.f.append(f"[Sequence mismatch] {self.getCurrentRestraint(n=index, g=group)}"
                                      f"Residue name {__compId!r} of the restraint does not match with {chainId}:{cifSeqId}:{cifCompId} of the coordinates.")
                        skip = True
                        break

                if compId != cifCompId and cifCompId in monDict3 and not isPolySeq:
                    skip = True
                    break

                if lenAtomId == 0 and not isPolySeq and cifCompId in SYMBOLS_ELEMENT:
                    _atomId = [cifCompId]
                    lenAtomId = 1

                if lenAtomId > 0:
                    _atomIdSet.append(_atomId)

            if skip:
                continue

            if len(_atomIdSet) > 1:
                _atomId = []
                for _atomId_ in _atomIdSet:
                    _atomId.extend(_atomId_)
                lenAtomId = len(_atomId)

            if lenAtomId == 0 and not isPolySeq and cifCompId in SYMBOLS_ELEMENT:
                _atomId = [cifCompId]
                lenAtomId = 1

            if lenAtomId == 0:
                if compId != cifCompId and any(True for item in chainAssign if item[2] == compId):
                    continue
                if seqId == 1 and isPolySeq and cifCompId == 'ACE' and cifCompId != compId and offset == 0:
                    self.selectCoordAtomsWithIndex(chainAssign, seqId, compId, atomId, allowAmbig, index, group, offset=1)
                    return
                self.f.append(f"[Invalid atom nomenclature] {self.getCurrentRestraint(n=index, g=group)}"
                              f"{seqId}:{__compId}:{__atomId} is invalid atom nomenclature.")
                continue
            if lenAtomId > 1 and not allowAmbig:
                self.f.append(f"[Invalid atom selection] {self.getCurrentRestraint(n=index, g=group)}"
                              f"Ambiguous atom selection '{seqId}:{__compId}:{__atomId}' is not allowed as a angle restraint.")
                continue

            if __compId != cifCompId and __compId not in self.__compIdMap:
                self.__compIdMap[__compId] = cifCompId

            for cifAtomId in _atomId:

                if seqKey in self.__coordUnobsRes and cifCompId in monDict3 and self.reasons is not None and 'non_poly_remap' in self.reasons:
                    if self.ccU.updateChemCompDict(cifCompId):
                        try:
                            next(cca for cca in self.ccU.lastAtomList
                                 if cca[self.ccU.ccaAtomId] == cifAtomId and cca[self.ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            continue
                        try:
                            if len(authAtomId) > len(cifAtomId):
                                next(cca for cca in self.ccU.lastAtomList
                                     if cca[self.ccU.ccaAtomId] == authAtomId and cca[self.ccU.ccaLeavingAtomFlag] != 'Y')
                        except StopIteration:
                            break

                if authAtomId in ('H', 'HN') and cifAtomId in ('HN1', 'HN2', 'HNA') and self.csStat.peptideLike(cifCompId)\
                   and coordAtomSite is not None and cifAtomId not in coordAtomSite['atom_id']:
                    if cifAtomId in ('HN2', 'HNA'):
                        if 'H2' not in coordAtomSite['atom_id']:
                            continue
                        cifAtomId = 'H2'
                    if cifAtomId == 'HN1' and 'H' in coordAtomSite['atom_id']:
                        cifAtomId = 'H'

                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                                      'atom_id': cifAtomId, 'auth_atom_id': authAtomId})

                self.testCoordAtomIdConsistencyWithIndex(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, index, group)

        if len(atomSelection) > 0:
            self.atomSelectionSet.append(atomSelection)

    def selectAuxCoordAtomsWithIndex(self, chainAssign: List[Tuple[str, int, str, bool]], seqId: int, compId: str, atomId: str,
                                     allowAmbig: bool = True, index: Optional[int] = None, group: Optional[int] = None):
        """ Select auxiliary atoms of the coordinates.
        """

        atomSelection = []

        for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)

            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId, leave_unmatched=True)
            if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomId[:-1], leave_unmatched=True)
                if atomId[-1].isdigit() and int(atomId[-1]) <= len(_atomId):
                    _atomId = [_atomId[int(atomId[-1]) - 1]]

            if details is not None or atomId.endswith('"'):
                _atomId_ = translateToStdAtomName(atomId, cifCompId, ccU=self.ccU, unambig=False)
                if _atomId_ != atomId:
                    if atomId.startswith('HT') and len(_atomId_) == 2:
                        _atomId_ = 'H'
                    __atomId = self.nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                    if coordAtomSite is not None:
                        if any(True for _atomId_ in __atomId if _atomId_ in coordAtomSite['atom_id']):
                            _atomId = __atomId
                        elif __atomId[0][0] in protonBeginCode:
                            __bondedTo = self.ccU.getBondedAtoms(cifCompId, __atomId[0])
                            if len(__bondedTo) > 0 and __bondedTo[0] in coordAtomSite['atom_id']:
                                _atomId = __atomId
                elif coordAtomSite is not None:
                    _atomId = []
            # _atomId = self.nefT.get_valid_star_atom(cifCompId, atomId)[0]

            if coordAtomSite is not None\
               and not any(True for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id'])\
               and atomId in coordAtomSite['atom_id']:
                _atomId = [atomId]

            if coordAtomSite is None and not isPolySeq:
                try:
                    for np in self.__nonPoly:
                        if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                            cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, cifCompId)
                            if coordAtomSite is not None:
                                break
                except ValueError:
                    pass

            lenAtomId = len(_atomId)
            if lenAtomId == 0:
                self.f.append(f"[Invalid atom nomenclature] {self.getCurrentRestraint(n=index, g=group)}"
                              f"{seqId}:{compId}:{atomId} is invalid atom nomenclature.")
                continue
            if lenAtomId > 1 and not allowAmbig:
                self.f.append(f"[Invalid atom selection] {self.getCurrentRestraint(n=index, g=group)}"
                              f"Ambiguous atom selection '{seqId}:{compId}:{atomId}' is not allowed as a angle restraint.")
                continue

            for cifAtomId in _atomId:
                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})

                _cifAtomId, asis = self.testCoordAtomIdConsistencyWithIndex(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, index, group)
                if asis:
                    atomSelection[-1]['asis'] = True
                if cifAtomId != _cifAtomId:
                    atomSelection[-1]['atom_id'] = _cifAtomId
                    if _cifAtomId.startswith('Ignorable'):
                        atomSelection.pop()

        if len(atomSelection) > 0:
            self.auxAtomSelectionSet.append(atomSelection)

    def testCoordAtomIdConsistency(self, chainId: str, seqId: int, compId: str, atomId: str,
                                   seqKey: Tuple[str, int], coordAtomSite: Optional[dict], enableWarning: bool = True) -> Tuple[str, bool]:
        asis = False
        if not self.hasCoord:
            return atomId, asis

        found = False

        if coordAtomSite is not None:
            if atomId in coordAtomSite['atom_id']:
                found = True
            elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in coordAtomSite['atom_id']
                                                      or ('H' + atomId[-1]) in coordAtomSite['atom_id']):
                atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in coordAtomSite['atom_id'] else 'H' + atomId[-1]
                found = True
            elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
                found = True
                self.authAtomId = 'auth_atom_id'

            elif self.__preferAuthSeq and not self.__extendAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()

            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif not self.__extendAuthSeq:
                        self.__preferAuthSeq = False
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False

        elif self.__preferAuthSeq and seqKey not in self.__coordUnobsRes:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        elif not self.__preferAuthSeq:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False
            elif not self.__extendAuthSeq:
                self.__preferAuthSeq = False

        if found:
            if self.__preferAuthSeq:
                self.__preferAuthSeqCount += 1
            return atomId, asis

        if self.__preferAuthSeq and seqKey not in self.__coordUnobsRes:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        elif not self.__preferAuthSeq:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False
            elif not self.__extendAuthSeq:
                self.__preferAuthSeq = False

        if found:
            if self.__preferAuthSeq:
                self.__preferAuthSeqCount += 1
            return atomId, asis

        if self.ccU.updateChemCompDict(compId):
            cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)
            if cca is not None and seqKey not in self.__coordUnobsRes and self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                checked = False
                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                auth_seq_id_list = list(filter(None, ps['auth_seq_id'])) if ps is not None else None
                min_auth_seq_id = max_auth_seq_id = UNREAL_AUTH_SEQ_NUM
                if auth_seq_id_list is not None and len(auth_seq_id_list) > 0:
                    min_auth_seq_id = min(auth_seq_id_list)
                    max_auth_seq_id = max(auth_seq_id_list)
                if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes\
                   or seqId == min_auth_seq_id:
                    if atomId in aminoProtonCode and atomId != 'H1':
                        return self.testCoordAtomIdConsistency(chainId, seqId, compId, 'H1', seqKey, coordAtomSite)
                    if atomId in aminoProtonCode or atomId == 'P' or atomId.startswith('HOP'):
                        checked = True
                if not checked:
                    if atomId[0] in protonBeginCode:
                        bondedTo = self.ccU.getBondedAtoms(compId, atomId)
                        if len(bondedTo) > 0 and bondedTo[0][0] != 'P':
                            if coordAtomSite is not None and bondedTo[0] in coordAtomSite['atom_id']:
                                if cca[self.ccU.ccaLeavingAtomFlag] != 'Y'\
                                   or (self.csStat.peptideLike(compId)
                                       and cca[self.ccU.ccaNTerminalAtomFlag] == 'N'
                                       and cca[self.ccU.ccaCTerminalAtomFlag] == 'N'):
                                    self.f.append(f"[Hydrogen not instantiated] {self.getCurrentRestraint()}"
                                                  f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "
                                                  "Please re-upload the model file.")
                                    return atomId, asis
                            if bondedTo[0][0] == 'O':
                                return 'Ignorable hydroxyl group', asis
                    if seqId == max_auth_seq_id\
                       or (chainId, seqId + 1) in self.__coordUnobsRes and self.csStat.peptideLike(compId):
                        if coordAtomSite is not None and atomId in carboxylCode\
                           and not isCyclicPolymer(self.cR, self.polySeq, chainId, self.representativeModelId, self.representativeAltId, self.modelNumName):
                            self.f.append(f"[Coordinate issue] {self.getCurrentRestraint()}"
                                          f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "
                                          "Please re-upload the model file.")
                            return atomId, asis

                    if enableWarning:
                        ext_seq = False
                        if auth_seq_id_list is not None and len(auth_seq_id_list) > 0:
                            if (compId == 'ACE' and seqId == min_auth_seq_id - 1)\
                               or (compId == 'NH2' and seqId == max_auth_seq_id + 1)\
                               or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                                   and (min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id
                                        or max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ)):
                                ext_seq = True
                            elif self.reasons is None and compId in monDict3 and atomId == 'H' and seqId < min_auth_seq_id\
                                    and self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT:
                                ext_seq = True
                        if chainId in LARGE_ASYM_ID:
                            if ext_seq:
                                return atomId, asis
                            if self.allow_ext_seq:
                                self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint()}"
                                              f"The residue '{chainId}:{seqId}:{compId}' is not present in polymer sequence "
                                              f"of chain {chainId} of the coordinates. "
                                              "Please update the sequence in the Macromolecules page.")
                                asis = True
                            else:
                                if seqKey in self.__coordUnobsAtom\
                                   and (atomId in self.__coordUnobsAtom[seqKey]['atom_ids']
                                        or (atomId[0] in protonBeginCode
                                            and any(True for bondedTo in self.ccU.getBondedAtoms(compId, atomId, exclProton=True)
                                                    if bondedTo in self.__coordUnobsAtom[seqKey]['atom_ids']))):
                                    self.f.append(f"[Coordinate issue] {self.getCurrentRestraint()}"
                                                  f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                                    return atomId, asis
                                if (compId == 'ASP' and atomId == 'HD1') or (compId == 'GLU' and atomId == 'HE1'):
                                    self.f.append(f"[Hydrogen not instantiated] {self.getCurrentRestraint()}"
                                                  f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                                    return atomId, asis
                                self.f.append(f"[Atom not found] {self.getCurrentRestraint()}"
                                              f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                                updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, compId)
        return atomId, asis

    def testCoordAtomIdConsistencyWithIndex(self, chainId: str, seqId: int, compId: str, atomId: str,
                                            seqKey: Tuple[str, int], coordAtomSite: Optional[dict],
                                            index: Optional[int] = None, group: Optional[int] = None) -> Tuple[str, bool]:
        asis = False
        if not self.hasCoord:
            return atomId, asis

        found = False

        if coordAtomSite is not None:
            if atomId in coordAtomSite['atom_id']:
                found = True
            elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in coordAtomSite['atom_id']
                                                      or ('H' + atomId[-1]) in coordAtomSite['atom_id']):
                atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in coordAtomSite['atom_id'] else 'H' + atomId[-1]
                found = True
            elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
                found = True
                # self.authAtomId = 'auth_atom_id'

            elif self.__preferAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        # self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()

            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        # self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif not self.__extendAuthSeq:
                        self.__preferAuthSeq = False
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False

        elif self.__preferAuthSeq and seqKey not in self.__coordUnobsRes:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.authSeqId = 'label_seq_id'
                    # self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        elif not self.__preferAuthSeq:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                          or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                    atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.authSeqId = 'auth_seq_id'
                    # self.authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False
            elif not self.__extendAuthSeq:
                self.__preferAuthSeq = False

        if found:
            if self.__preferAuthSeq:
                self.__preferAuthSeqCount += 1
            return atomId, asis

        if chainId in self.__chainNumberDict.values():

            if self.__preferAuthSeq and seqKey not in self.__coordUnobsRes:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId and not self.__extendAuthSeq:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.authSeqId = 'label_seq_id'
                        # self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
            elif not self.__preferAuthSeq:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, compId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif atomId in ('HN1', 'HN2', 'HN3') and ((atomId[-1] + 'HN') in _coordAtomSite['atom_id']
                                                              or ('H' + atomId[-1]) in _coordAtomSite['atom_id']):
                        atomId = atomId[-1] + 'HN' if atomId[-1] + 'HN' in _coordAtomSite['atom_id'] else 'H' + atomId[-1]
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.authSeqId = 'auth_seq_id'
                        # self.authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif not self.__extendAuthSeq:
                        self.__preferAuthSeq = False
                elif not self.__extendAuthSeq:
                    self.__preferAuthSeq = False

            if found:
                if self.__preferAuthSeq:
                    self.__preferAuthSeqCount += 1
                return atomId, asis

        if self.ccU.updateChemCompDict(compId):
            cca = next((cca for cca in self.ccU.lastAtomList if cca[self.ccU.ccaAtomId] == atomId), None)
            if cca is not None and seqKey not in self.__coordUnobsRes and self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                checked = False
                ps = next((ps for ps in self.polySeq if ps['auth_chain_id'] == chainId), None)
                auth_seq_id_list = list(filter(None, ps['auth_seq_id'])) if ps is not None else None
                min_auth_seq_id = max_auth_seq_id = UNREAL_AUTH_SEQ_NUM
                if auth_seq_id_list is not None and len(auth_seq_id_list) > 0:
                    min_auth_seq_id = min(auth_seq_id_list)
                    max_auth_seq_id = max(auth_seq_id_list)
                if seqId == 1 or (chainId, seqId - 1) in self.__coordUnobsRes\
                   or seqId == min_auth_seq_id:
                    if atomId in aminoProtonCode and atomId != 'H1':
                        return self.testCoordAtomIdConsistencyWithIndex(chainId, seqId, compId, 'H1', seqKey, coordAtomSite)
                    if atomId in aminoProtonCode or atomId == 'P' or atomId.startswith('HOP'):
                        checked = True
                if not checked:
                    if atomId[0] in protonBeginCode:
                        bondedTo = self.ccU.getBondedAtoms(compId, atomId)
                        if len(bondedTo) > 0 and bondedTo[0][0] != 'P':
                            if coordAtomSite is not None and bondedTo[0] in coordAtomSite['atom_id']:
                                if cca[self.ccU.ccaLeavingAtomFlag] != 'Y'\
                                   or (self.csStat.peptideLike(compId)
                                       and cca[self.ccU.ccaNTerminalAtomFlag] == 'N'
                                       and cca[self.ccU.ccaCTerminalAtomFlag] == 'N'):
                                    self.f.append(f"[Hydrogen not instantiated] {self.getCurrentRestraint(n=index, g=group)}"
                                                  f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "
                                                  "Please re-upload the model file.")
                                    return atomId, asis
                            if bondedTo[0][0] == 'O':
                                return 'Ignorable hydroxyl group', asis
                    if seqId == max_auth_seq_id\
                       or (chainId, seqId + 1) in self.__coordUnobsRes and self.csStat.peptideLike(compId):
                        if coordAtomSite is not None and atomId in carboxylCode\
                           and not isCyclicPolymer(self.cR, self.polySeq, chainId, self.representativeModelId, self.representativeAltId, self.modelNumName):
                            self.f.append(f"[Coordinate issue] {self.getCurrentRestraint(n=index, g=group)}"
                                          f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "
                                          "Please re-upload the model file.")
                            return atomId, asis

                    ext_seq = False
                    if auth_seq_id_list is not None and len(auth_seq_id_list) > 0:
                        if (compId == 'ACE' and seqId == min_auth_seq_id - 1)\
                           or (compId == 'NH2' and seqId == max_auth_seq_id + 1)\
                           or (compId in monDict3 and self.__preferAuthSeqCount - self.__preferLabelSeqCount >= MAX_PREF_LABEL_SCHEME_COUNT
                               and (min_auth_seq_id - MAX_ALLOWED_EXT_SEQ <= seqId < min_auth_seq_id
                                    or max_auth_seq_id < seqId <= max_auth_seq_id + MAX_ALLOWED_EXT_SEQ)):
                            ext_seq = True
                        elif self.reasons is None and compId in monDict3 and atomId == 'H' and seqId < min_auth_seq_id\
                                and self.__preferAuthSeqCount - self.__preferLabelSeqCount < MAX_PREF_LABEL_SCHEME_COUNT:
                            ext_seq = True
                    if chainId in LARGE_ASYM_ID:
                        if ext_seq:
                            return atomId, asis
                        if self.allow_ext_seq:
                            self.f.append(f"[Sequence mismatch warning] {self.getCurrentRestraint(n=index, g=group)}"
                                          f"The residue '{chainId}:{seqId}:{compId}' is not present in polymer sequence "
                                          f"of chain {chainId} of the coordinates. "
                                          "Please update the sequence in the Macromolecules page.")
                            asis = True
                        else:
                            if seqKey in self.__coordUnobsAtom\
                               and (atomId in self.__coordUnobsAtom[seqKey]['atom_ids']
                                    or (atomId[0] in protonBeginCode
                                        and any(True for bondedTo in self.ccU.getBondedAtoms(compId, atomId, exclProton=True)
                                                if bondedTo in self.__coordUnobsAtom[seqKey]['atom_ids']))):
                                self.f.append(f"[Coordinate issue] {self.getCurrentRestraint(n=index, g=group)}"
                                              f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                                return atomId, asis
                            if (compId == 'ASP' and atomId == 'HD1') or (compId == 'GLU' and atomId == 'HE1'):
                                self.f.append(f"[Hydrogen not instantiated] {self.getCurrentRestraint(n=index, g=group)}"
                                              f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                                return atomId, asis
                            self.f.append(f"[Atom not found] {self.getCurrentRestraint(n=index, g=group)}"
                                          f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.")
                            updatePolySeqRst(self.__polySeqRstFailed, chainId, seqId, compId)
        return atomId, asis

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

    def getCoordAtomSiteOf(self, chainId: str, seqId: int, compId: Optional[str] = None, cifCheck: bool = True, asis: bool = True
                           ) -> Tuple[Tuple[str, int], Optional[dict]]:
        return self.__getCoordAtomSiteOf(chainId, seqId, compId, cifCheck, asis, self.__preferAuthSeq)

    @functools.lru_cache(maxsize=2048)
    def __getCoordAtomSiteOf(self, chainId: str, seqId: int, compId: Optional[str] = None, cifCheck: bool = True, asis: bool = True,
                             __preferAuthSeq: bool = True) -> Tuple[Tuple[str, int], Optional[dict]]:
        seqKey = (chainId, seqId)
        if cifCheck:
            preferAuthSeq = __preferAuthSeq if asis else not __preferAuthSeq
            if preferAuthSeq:
                if compId is not None:
                    _seqKey = (chainId, seqId, compId)
                    if _seqKey in self.__coordAtomSite:
                        return seqKey, self.__coordAtomSite[_seqKey]
                if seqKey in self.__coordAtomSite:
                    if compId is None:
                        return seqKey, self.__coordAtomSite[seqKey]
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
                    return seqKey, self.__coordAtomSite[seqKey]
            else:
                if seqKey in self.__labelToAuthSeq:
                    seqKey = self.__labelToAuthSeq[seqKey]
                    if cifCheck and compId is not None:
                        _seqKey = (seqKey[0], seqKey[1], compId)
                        if _seqKey in self.__coordAtomSite:
                            return seqKey, self.__coordAtomSite[_seqKey]
                    if seqKey in self.__coordAtomSite:
                        return seqKey, self.__coordAtomSite[seqKey]
        return seqKey, None

    def validateAngleRange(self, weight: float, target_value: Optional[float],
                           lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit],
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

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The target value='{target_value:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The target value='{target_value:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The lower limit value='{lower_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint()}"
                              f"The upper limit value='{upper_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        if None not in (upper_limit, lower_limit)\
           and (PLANE_LIKE_LOWER_LIMIT <= lower_limit < 0.0 < upper_limit <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 180.0 < 0.0 < upper_limit - 180.0 <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 360.0 < 0.0 < upper_limit - 360.0 <= PLANE_LIKE_UPPER_LIMIT):
            dstFunc['plane_like'] = True

        return dstFunc

    def validateAngleRangeWithIndex(self, index: int, weight: float, target_value: Optional[float],
                                    lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit],
                                 dtype=float)

            shift = None
            if numpy.nanmin(_array) >= THRESHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmax(_array) // 360) * 360
            elif numpy.nanmax(_array) <= -THRESHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmin(_array) // 360) * 360
            if shift is not None:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              "The target/limit values for an angle restraint have been circularly shifted "
                              f"to fit within range {ANGLE_RESTRAINT_ERROR}.")
                if target_value is not None:
                    target_value += shift
                if lower_limit is not None:
                    lower_limit += shift
                if upper_limit is not None:
                    upper_limit += shift

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The target value='{target_value}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The lower limit value='{lower_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.3f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The upper limit value='{upper_limit:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.")

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The target value='{target_value}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The lower limit value='{lower_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The upper limit value='{upper_limit:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        if None not in (upper_limit, lower_limit)\
           and (PLANE_LIKE_LOWER_LIMIT <= lower_limit < 0.0 < upper_limit <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 180.0 < 0.0 < upper_limit - 180.0 <= PLANE_LIKE_UPPER_LIMIT
                or PLANE_LIKE_LOWER_LIMIT <= lower_limit - 360.0 < 0.0 < upper_limit - 360.0 <= PLANE_LIKE_UPPER_LIMIT):
            dstFunc['plane_like'] = True

        return dstFunc

    def validateRdcRange(self, weight: float, orientation: int, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate RDC value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if orientation is not None:
            dstFunc['orientation'] = orientation

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

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

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

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    def areUniqueCoordAtoms(self, subtype_name: str, allow_ambig: bool = False, allow_ambig_warn_title: str = '') -> bool:
        """ Check whether atom selection sets are uniquely assigned.
        """

        for _atomSelectionSet in self.atomSelectionSet:
            _lenAtomSelectionSet = len(_atomSelectionSet)

            if _lenAtomSelectionSet == 0:
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

    def validateCoupRangeWithIndex(self, index: int, weight: float, target_value: Optional[float],
                                   lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate scalar J-coupling value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            if RDC_ERROR_MIN < target_value < RDC_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The target value='{target_value}' must be within range {RDC_RESTRAINT_ERROR}.")

        if lower_limit is not None:
            if RDC_ERROR_MIN <= lower_limit < RDC_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The lower limit value='{lower_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if upper_limit is not None:
            if RDC_ERROR_MIN < upper_limit <= RDC_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                              f"The upper limit value='{upper_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.")

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint(n=index)}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

        if not validRange:
            return None

        if target_value is not None:
            if RDC_RANGE_MIN <= target_value <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The target value='{target_value}' should be within range {RDC_RESTRAINT_RANGE}.")

        if lower_limit is not None:
            if RDC_RANGE_MIN <= lower_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The lower limit value='{lower_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if upper_limit is not None:
            if RDC_RANGE_MIN <= upper_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.f.append(f"[Range value warning] {self.getCurrentRestraint(n=index)}"
                              f"The upper limit value='{upper_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.")

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    def validatePcsRange(self, weight: float, orientation: int, target_value: Optional[float],
                         lower_limit: Optional[float], upper_limit: Optional[float]) -> Optional[dict]:
        """ Validate PCS value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'orientation': orientation}

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

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.")

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.f.append(f"[Range value error] {self.getCurrentRestraint()}"
                                  f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.")

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

        if target_value is None and lower_limit is None and upper_limit is None:
            return None

        return dstFunc

    def updateAmbigAtomNameMapping(self):
        if (not self.hasPolySeq and not self.hasNonPolySeq) or len(self.ambigAtomNameMapping) == 0:
            return

        unambigResidues = None
        if len(self.unambigAtomNameMapping) > 0:
            unambigResidues = [translateToStdResName(residue, ccU=self.ccU) for residue in self.unambigAtomNameMapping.keys()]

        for ambigDict in self.ambigAtomNameMapping.values():
            for ambigList in ambigDict.values():
                for ambig in ambigList:

                    if 'atom_id_list' in ambig:
                        continue

                    atomName = ambig['atom_name']
                    seqId = ambig['seq_id']

                    chainAssign = self.assignCoordPolymerSequenceWithoutCompId(seqId)

                    if len(chainAssign) == 0:
                        continue

                    ambig['atom_id_list'] = []

                    for cifChainId, cifSeqId, cifCompId, _ in chainAssign:

                        has_unambig = False

                        if unambigResidues is not None and cifCompId in unambigResidues:

                            unambigMap = next(v for k, v in self.unambigAtomNameMapping.items()
                                              if translateToStdResName(k, ccU=self.ccU) == cifCompId)

                            if atomName in unambigMap:

                                for cifAtomId in unambigMap[atomName]:
                                    ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                                  'seq_id': cifSeqId,
                                                                  'comp_id': cifCompId,
                                                                  'atom_id': cifAtomId})

                                has_unambig = True

                        if has_unambig:
                            continue

                        self.atomSelectionSet.clear()

                        self.selectCoordAtoms(chainAssign, seqId, None, ambig['atom_name'].upper(), enableWarning=False)

                        if len(self.atomSelectionSet[0]) > 0:
                            ambig['atom_id_list'].extend(self.atomSelectionSet[0])
                            continue

                        _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomName, leave_unmatched=True)
                        if details is not None and len(atomName) > 1:
                            _atomId, _, details = self.nefT.get_valid_star_atom_in_xplor(cifCompId, atomName[:-1], leave_unmatched=True)

                        if details is not None or atomName.endswith('"'):
                            _atomId_ = translateToStdAtomName(atomName, cifCompId, ccU=self.ccU)
                            if _atomId_ != atomName:
                                if atomName.startswith('HT') and len(_atomId_) == 2:
                                    _atomId_ = 'H'
                                _atomId = self.nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]

                        for cifAtomId in _atomId:
                            ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                          'seq_id': cifSeqId,
                                                          'comp_id': cifCompId,
                                                          'atom_id': cifAtomId})

                    ambig['atom_id_list'] = [dict(s) for s in set(frozenset(atom.items()) for atom in ambig['atom_id_list'])]

    def atomIdListToChainAssign(self, atomIdList: List[dict]) -> List[dict]:  # pylint: disable=no-self-use
        chainAssign = set()
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    chainAssign.add((atom_id['chain_id'], atom_id['seq_id'], atom_id['comp_id']))
        return list(chainAssign)

    def atomIdListToAtomSelection(self, atomIdList: List[dict]) -> List[dict]:  # pylint: disable=no-self-use
        atomSelection = []
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    if atom_id not in atomSelection:
                        atomSelection.append(atom_id)
        return atomSelection

    def getCurrentRestraint(self, n: Optional[int] = None, g: Optional[int] = None) -> str:
        if self.cur_subtype == 'dist':
            if None in (n, g):
                return f"[Check the {self.distRestraints}th row of distance restraints, {self.__def_err_sf_framecode}] "
            return f"[Check the {self.distRestraints}th row of distance restraints (index={n} group={g}), {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'dihed':
            if n is None:
                return f"[Check the {self.dihedRestraints}th row of torsion angle restraints, {self.__def_err_sf_framecode}] "
            return f"[Check the {self.dihedRestraints}th row of torsion angle restraints (index={n}), {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'rdc':
            return f"[Check the {self.rdcRestraints}th row of residual dipolar coupling restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'pcs':
            return f"[Check the {self.pcsRestraints}th row of pseudocontact shift restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'noepk':
            return f"[Check the {self.noepkRestraints}th row of NOESY volume restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'jcoup':
            if n is None:
                return f"[Check the {self.jcoupRestraints}th row of scalar coupling constant restraints, {self.__def_err_sf_framecode}] "
            return f"[Check the {self.jcoupRestraints}th row of scalar coupling constant restraints (index={n}), {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of coordinate geometry restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'hbond':
            return f"[Check the {self.hbondRestraints}th row of hydrogen bond restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'ssbond':
            return f"[Check the {self.ssbondRestraints}th row of disulfide bond restraints, {self.__def_err_sf_framecode}] "
        if self.cur_subtype == 'fchiral':
            return f"[Check the {self.fchiralRestraints}th row of floating chiral stereo assignments, {self.__def_err_sf_framecode}] "
        return ''

    def __setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        preferAuthSeq = self.authSeqId == 'auth_seq_id'
        if self.cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.distRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.dihedRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'rdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.rdcRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'pcs':
            self.reasonsForReParsing['loca_seq_scheme'][(self.cur_subtype, self.pcsRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'noepk':
            self.reasonsForReParsing['loca_seq_scheme'][(self.cur_subtype, self.noepkRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'jcoup':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.jcoupRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.geoRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'hbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.hbondRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'ssbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.ssbondRestraints)] = preferAuthSeq
        elif self.cur_subtype == 'fchiral':
            self.reasonsForReParsing['local_seq_scheme'][(self.cur_subtype, self.fchiralRestraints)] = preferAuthSeq
        if not preferAuthSeq:
            self.__preferLabelSeqCount += 1
            if self.__preferLabelSeqCount > MAX_PREF_LABEL_SCHEME_COUNT:
                self.reasonsForReParsing['label_seq_scheme'] = True

    def retrieveLocalSeqScheme(self):
        if self.reasons is None\
           or ('label_seq_scheme' not in self.reasons
               and 'local_seq_scheme' not in self.reasons
               and 'extend_seq_scheme' not in self.reasons):
            return
        if 'extend_seq_scheme' in self.reasons:
            self.__preferAuthSeq = self.__extendAuthSeq = True
            return
        if 'label_seq_scheme' in self.reasons and self.reasons['label_seq_scheme']:
            self.__preferAuthSeq = False
            self.authSeqId = 'label_seq_id'
            return
        if self.cur_subtype == 'dist':
            key = (self.cur_subtype, self.distRestraints)
        elif self.cur_subtype == 'dihed':
            key = (self.cur_subtype, self.dihedRestraints)
        elif self.cur_subtype == 'rdc':
            key = (self.cur_subtype, self.rdcRestraints)
        elif self.cur_subtype == 'pcs':
            key = (self.cur_subtype, self.pcsRestraints)
        elif self.cur_subtype == 'noepk':
            key = (self.cur_subtype, self.noepkRestraints)
        elif self.cur_subtype == 'jcoup':
            key = (self.cur_subtype, self.jcoupRestraints)
        elif self.cur_subtype == 'geo':
            key = (self.cur_subtype, self.geoRestraints)
        elif self.cur_subtype == 'hbond':
            key = (self.cur_subtype, self.hbondRestraints)
        elif self.cur_subtype == 'ssbond':
            key = (self.cur_subtype, self.ssbondRestraints)
        elif self.cur_subtype == 'fchiral':
            key = (self.cur_subtype, self.fchiralRestraints)
        else:
            return

        if key in self.reasons['local_seq_scheme']:
            self.__preferAuthSeq = self.reasons['local_seq_scheme'][key]

    def __addSf(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
                rdcCode: Optional[str] = None, orientationId: Optional[str] = None,
                cyanaParameter: Optional[str] = None):
        content_subtype = contentSubtypeOf(self.cur_subtype)

        if content_subtype is None:
            return

        self.__listIdCounter = incListIdCounter(self.cur_subtype, self.__listIdCounter)

        key = (self.cur_subtype, constraintType, potentialType, rdcCode, orientationId)

        if key in self.sfDict:
            if len(self.sfDict[key]) > 0:
                decListIdCounter(self.cur_subtype, self.__listIdCounter)
                return
        else:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[content_subtype]

        restraint_name = getRestraintName(self.cur_subtype)

        sf_framecode = (f'{self.software_name}_' if self.software_name not in emptyValue else '') + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                          cyanaParameter=cyanaParameter)

        not_valid = True

        lp = getLoop(self.cur_subtype, hasInsCode=self.authToInsCode is not None)
        if not isinstance(lp, dict):
            sf.add_loop(lp)
            not_valid = False

        _restraint_name = restraint_name.split()
        if _restraint_name[-1] == 'assignments':
            _restraint_name.append('dummy')  # to preserve 'floating chiral stereo assignments'

        item = {'file_type': self.file_type, 'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0,
                'constraint_type': ' '.join(_restraint_name[:-1]),
                'sf_framecode': sf_framecode}

        if not_valid:
            item['tags'] = []

        if self.cur_subtype == 'dist':
            item['constraint_subsubtype'] = 'simple'

        self.__lastSfDict[self.cur_subtype] = item

        self.sfDict[key].append(item)

    def __addSfWithSoftware(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
                            rdcCode: Optional[str] = None, softwareName: Optional[str] = None):
        content_subtype = contentSubtypeOf(self.cur_subtype)

        if content_subtype is None:
            return

        self.listIdCounter = incListIdCounter(self.cur_subtype, self.listIdCounter)

        key = (self.cur_subtype, constraintType, potentialType, rdcCode, None)

        if key in self.sfDict:
            if len(self.sfDict[key]) > 0:
                decListIdCounter(self.cur_subtype, self.listIdCounter)
                return
        else:
            self.sfDict[key] = []

        list_id = self.listIdCounter[content_subtype]

        restraint_name = getRestraintName(self.cur_subtype)

        sf_framecode = (self.software_name if softwareName is None else softwareName) + '_' + restraint_name.replace(' ', '_') + f'_{list_id}'

        sf = getSaveframe(self.cur_subtype, sf_framecode, list_id, self.entryId, self.originalFileName,
                          constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode)

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

        self.sfDict[key].append(item)

    def getSf(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
              rdcCode: Optional[str] = None, orientationId: Optional[str] = None,
              cyanaParameter: Optional[str] = None) -> dict:
        key = (self.cur_subtype, constraintType, potentialType, rdcCode, orientationId)

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None or rdcCode is not None or orientationId is not None:
                old_key = (self.cur_subtype, self.cur_constraint_type, None, None, orientationId)
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
            if not replaced:
                self.__addSf(constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                             orientationId=orientationId, cyanaParameter=cyanaParameter)

        self.cur_constraint_type = constraintType

        _key = next((_key for _key in self.sfDict if _key[0] == 'dist' and _key[1] is None), key) if self.cur_subtype == 'dist' else key
        self.__def_err_sf_framecode = self.sfDict[_key][-1]['sf_framecode']

        return self.sfDict[key][-1]

    def getSfWithSoftware(self, constraintType: Optional[str] = None, potentialType: Optional[str] = None,
                          rdcCode: Optional[str] = None, softwareName: Optional[str] = None) -> dict:
        key = (self.cur_subtype, constraintType, potentialType, rdcCode, None)

        if key not in self.sfDict:
            replaced = False
            if potentialType is not None or rdcCode is not None:
                old_key = (self.cur_subtype, constraintType, None, None, None)
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
            if not replaced:
                self.__addSfWithSoftware(constraintType=constraintType, potentialType=potentialType, rdcCode=rdcCode,
                                         softwareName=softwareName)

        self.cur_constraint_type = constraintType

        _key = next((_key for _key in self.sfDict if _key[0] == 'dist' and _key[1] is None), key) if self.cur_subtype == 'dist' else key
        self.__def_err_sf_framecode = self.sfDict[_key][-1]['sf_framecode']

        return self.sfDict[key][-1]

    def trimSfWoLp(self):
        if self.cur_subtype not in self.__lastSfDict:
            return
        if self.__lastSfDict[self.cur_subtype]['index_id'] > 0:
            return
        for k, v in self.sfDict.items():
            for item in reversed(v):
                if item == self.__lastSfDict:
                    v.remove(item)
                    if len(v) == 0:
                        del self.sfDict[k]
                    self.__listIdCounter = decListIdCounter(k[0], self.__listIdCounter)
                    return

    def getContentSubtype(self) -> dict:
        """ Return content subtype of MR file.
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints,
                          'noepk_restraint': self.noepkRestraints,
                          'jcoup_restraint': self.jcoupRestraints,
                          'geo_restraint': self.geoRestraints,
                          'hbond_restraint': self.hbondRestraints,
                          'ssbond_restraint': self.ssbondRestraints,
                          'fchiral_restraint': self.fchiralRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getEffectiveContentSubtype(self) -> dict:
        """ Return effective content subtype of MR file (excluding .upv, lov, and .cco).
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

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

    def getTypeOfDistanceRestraints(self) -> str:
        """ Return type of distance restraints of the MR file.
        """

        if self.file_ext is not None:
            if self.file_ext in ('upl', 'lol'):
                return self.file_ext

        if len(self.local_dist_types) > 0:
            if 'upl' in self.local_dist_types and 'lol' not in self.local_dist_types:
                return 'upl'
            if 'lol' in self.local_dist_types and 'upl' not in self.local_dist_types:
                return 'lol'
            return 'both'

        if self.max_dist_value == DIST_ERROR_MIN:
            return ''

        if self.max_dist_value > 3.5 and self.min_dist_value > 2.7:
            return 'upl'
        if self.max_dist_value < 2.7:
            return 'lol'

        return 'both'

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
