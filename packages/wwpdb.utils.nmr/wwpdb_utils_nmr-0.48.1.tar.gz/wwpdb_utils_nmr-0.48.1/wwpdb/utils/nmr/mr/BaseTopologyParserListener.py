##
# File: BaseTopologyParserListener.py
# Date: 05-Nov-2025
#
# Updates:
""" ParserLister base class for any topology files.
    @author: Masashi Yokochi
"""
__docformat__ = "restructuredtext en"
__author__ = "Masashi Yokochi"
__email__ = "yokochi@protein.osaka-u.ac.jp"
__license__ = "Apache License 2.0"
__version__ = "1.1.1"

import sys
import collections
import copy
import functools

from rmsd.calculate_rmsd import NAMES_ELEMENT  # noqa: F401 pylint: disable=no-name-in-module, import-error, unused-import
from typing import IO, List, Optional

try:
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                                       translateToStdAtomName,
                                                       translateToStdAtomNameNoRef,
                                                       translateToStdAtomNameWithRef,
                                                       translateToStdAtomNameOfDmpc,
                                                       translateToStdResName,
                                                       translateToLigandName,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       REPRESENTATIVE_ALT_ID)
    from wwpdb.utils.nmr.nef.NEFTranslator import (NEFTranslator,
                                                   NON_METAL_ELEMENTS)
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           protonBeginCode,
                                           pseProBeginCode,
                                           aminoProtonCode,
                                           letterToDigit,
                                           indexToLetter,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           trimSequenceAlignment,
                                           retrieveAtomIdentFromMRMap,
                                           alignPolymerSequenceWithConflicts,
                                           getRestraintFormatName,
                                           getOneLetterCodeCanSequence)
except ImportError:
    from nmr.io.CifReader import CifReader
    from nmr.mr.ParserListenerUtil import (coordAssemblyChecker,
                                           translateToStdAtomName,
                                           translateToStdAtomNameNoRef,
                                           translateToStdAtomNameWithRef,
                                           translateToStdAtomNameOfDmpc,
                                           translateToStdResName,
                                           translateToLigandName,
                                           REPRESENTATIVE_MODEL_ID,
                                           REPRESENTATIVE_ALT_ID)
    from nmr.nef.NEFTranslator import (NEFTranslator,
                                       NON_METAL_ELEMENTS)
    from nmr.AlignUtil import (monDict3,
                               protonBeginCode,
                               pseProBeginCode,
                               aminoProtonCode,
                               letterToDigit,
                               indexToLetter,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               trimSequenceAlignment,
                               retrieveAtomIdentFromMRMap,
                               alignPolymerSequenceWithConflicts,
                               getRestraintFormatName,
                               getOneLetterCodeCanSequence)


class BaseTopologyParserListener():
    __slots__ = ('mrAtomNameMapping',
                 'hasCoord',
                 'ccU',
                 'polySeqModel',
                 'nonPolyModel',
                 '__branchedModel',
                 '__coordAtomSite',
                 '__coordUnobsRes',
                 '__chemCompAtom',
                 'hasPolySeqModel',
                 'hasNonPolyModel',
                 '__hasBranchedModel',
                 'noWaterMol',
                 'csStat',
                 '__nefT',
                 '__pA',
                 'atomNumberDict',
                 'polySeqPrmTop',
                 '__f',
                 'atoms',
                 'prev_nr',
                 'cur_nr')

    # whether to restrict to unambiguous atom mapping
    unambig = True

    file_type = ''

    __seqAlign = None
    __chainAssign = None

    warningMessage = None

    def __init__(self, verbose: bool = True, log: IO = sys.stdout,
                 representativeModelId: int = REPRESENTATIVE_MODEL_ID,
                 representativeAltId: str = REPRESENTATIVE_ALT_ID,
                 mrAtomNameMapping: Optional[List[dict]] = None,
                 cR: Optional[CifReader] = None, caC: Optional[dict] = None,
                 nefT: NEFTranslator = None):

        self.mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.hasCoord = cR is not None

        self.__nefT = nefT
        self.ccU = nefT.ccU
        self.csStat = nefT.csStat
        self.__pA = nefT.pA

        if self.hasCoord:
            ret = coordAssemblyChecker(verbose, log, representativeModelId, representativeAltId,
                                       cR, self.ccU, caC, None, fullCheck=True)
            self.polySeqModel = ret['polymer_sequence']
            self.nonPolyModel = ret['non_polymer']
            self.__branchedModel = ret['branched']
            self.__coordAtomSite = ret['coord_atom_site']
            self.__coordUnobsRes = ret['coord_unobs_res']
            self.__chemCompAtom = ret['chem_comp_atom']

        else:
            self.polySeqModel = None
            self.nonPolyModel = None
            self.__branchedModel = None
            self.__coordAtomSite = None
            self.__coordUnobsRes = None
            self.__chemCompAtom = None

        self.hasPolySeqModel = self.polySeqModel is not None and len(self.polySeqModel) > 0
        self.hasNonPolyModel = self.nonPolyModel is not None and len(self.nonPolyModel) > 0
        self.__hasBranchedModel = self.__branchedModel is not None and len(self.__branchedModel) > 0
        self.noWaterMol = not self.hasNonPolyModel or not any(np['comp_id'][0] == 'HOH' for np in self.nonPolyModel)

        self.atomNumberDict = {}

        self.polySeqPrmTop = []

        self.__f = []

        # CHARMM/GROMACS specific
        self.atoms = []
        self.prev_nr = -1
        # PDB specific
        self.cur_nr = -1

    def exit(self, retrievedAtomNumList: List[int]):

        try:

            nonPolyCompIdList = []
            if self.hasNonPolyModel:
                for np in self.nonPolyModel:
                    compId = np['comp_id'][0]
                    if compId not in nonPolyCompIdList:
                        nonPolyCompIdList.append(compId)

            for ps in self.polySeqPrmTop:
                chainId = ps['chain_id']
                compIdList = []
                for seqId, authCompId in zip(ps['seq_id'], ps['auth_comp_id']):
                    authAtomIds = [translateToStdAtomName(atomNum['auth_atom_id'], atomNum['auth_comp_id'],
                                                          ccU=self.ccU, unambig=self.unambig)
                                   for atomNum in self.atomNumberDict.values()
                                   if atomNum['chain_id'] == chainId
                                   and atomNum['seq_id'] == seqId
                                   and atomNum['auth_atom_id'][0] not in protonBeginCode]
                    authCompId = translateToStdResName(authCompId, ccU=self.ccU)
                    if self.ccU.updateChemCompDict(authCompId):
                        chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                        valid = True
                        for _atomId in authAtomIds:
                            if _atomId not in chemCompAtomIds:
                                if not self.unambig:
                                    _, _, details = self.__nefT.get_valid_star_atom_in_xplor(authCompId, _atomId)
                                    if details is None:
                                        continue
                                valid = False
                                break
                            if not valid:
                                break
                        if valid:
                            compIdList.append(authCompId)
                            for k, atomNum in self.atomNumberDict.items():
                                if atomNum['chain_id'] == chainId and atomNum['seq_id'] == seqId:
                                    atomNum['comp_id'] = authCompId

                                    if authCompId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                                       and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                                        _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'], None, None, True)
                                    else:
                                        atomId = atomNum['auth_atom_id']

                                    if atomId.endswith('*'):
                                        _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                                        atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                    atomId = translateToStdAtomName(atomId, authCompId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)

                                    if atomId[0] not in protonBeginCode or atomId in chemCompAtomIds:
                                        atomNum['atom_id'] = atomId
                                        if 'atom_type' in atomNum:
                                            del atomNum['atom_type']
                                    else:
                                        if atomId in chemCompAtomIds:
                                            atomNum['atom_id'] = atomId
                                            if 'atom_type' in atomNum:
                                                del atomNum['atom_type']

                        else:
                            compId = self.csStat.getSimilarCompIdFromAtomIds([translateToStdAtomName(atomNum['auth_atom_id'],
                                                                                                     atomNum['auth_comp_id'],
                                                                                                     ccU=self.ccU,
                                                                                                     unambig=self.unambig)
                                                                              for atomNum in self.atomNumberDict.values()
                                                                              if atomNum['chain_id'] == chainId
                                                                              and atomNum['seq_id'] == seqId])

                            if self.hasNonPolyModel and compId != authCompId:
                                ligands = 0
                                for np in self.nonPolyModel:
                                    if 'alt_comp_id' in np:
                                        ligands += np['alt_comp_id'].count(authCompId)
                                if ligands > 0:
                                    for np in self.nonPolyModel:
                                        if authCompId in np['alt_comp_id']:
                                            compId = np['comp_id'][0]
                                            break
                                if ligands == 0:
                                    __compId = None
                                    for np in self.nonPolyModel:
                                        for ligand in np['comp_id']:
                                            __compId = translateToLigandName(authCompId, ligand, self.ccU)
                                            if __compId == ligand:
                                                ligands += 1
                                    if ligands == 1:
                                        compId = __compId
                                    elif len(self.nonPolyModel) == 1 and self.ccU.updateChemCompDict(authCompId, False):
                                        if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS':
                                            compId = self.nonPolyModel[0]['comp_id'][0]

                            if compId is not None:
                                compIdList.append(compId + '?')  # decide when coordinate is available
                                chemCompAtomIds = None
                                if self.ccU.updateChemCompDict(compId):
                                    chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                                for k, atomNum in self.atomNumberDict.items():
                                    if atomNum['chain_id'] == chainId and atomNum['seq_id'] == seqId:
                                        atomNum['comp_id'] = compId

                                        if compId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                                           and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, compId, atomNum['auth_atom_id'], None, None, True)
                                        else:
                                            atomId = atomNum['auth_atom_id']

                                        if atomId.endswith('*'):
                                            _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                                            atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                        atomId = translateToStdAtomName(atomId, compId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)

                                        if chemCompAtomIds is not None and atomId in chemCompAtomIds:
                                            atomNum['atom_id'] = atomId
                                            if 'atom_type' in atomNum:
                                                del atomNum['atom_type']
                                        elif chemCompAtomIds is not None:
                                            if atomId in chemCompAtomIds:
                                                atomNum['atom_id'] = atomId
                                                if 'atom_type' in atomNum:
                                                    del atomNum['atom_type']
                            else:
                                compIdList.append('.')
                                unknownAtomIds = [_atomId for _atomId in authAtomIds if _atomId not in chemCompAtomIds]
                                self.__f.append(f"[Unknown atom name] "
                                                f"{unknownAtomIds} are unknown atom names for {authCompId} residue.")
                                compIdList.append(f"? {authCompId} {unknownAtomIds}")
                    else:
                        compId = self.csStat.getSimilarCompIdFromAtomIds([atomNum['auth_atom_id']
                                                                          for atomNum in self.atomNumberDict.values()
                                                                          if atomNum['chain_id'] == chainId
                                                                          and atomNum['seq_id'] == seqId])

                        if self.hasNonPolyModel and compId != authCompId:
                            ligands = 0
                            for np in self.nonPolyModel:
                                if 'alt_comp_id' in np:
                                    ligands += np['alt_comp_id'].count(authCompId)
                            if ligands == 1:
                                for np in self.nonPolyModel:
                                    if authCompId in np['alt_comp_id']:
                                        compId = np['comp_id'][0]
                            if ligands == 0:
                                __compId = None
                                for np in self.nonPolyModel:
                                    for ligand in np['comp_id']:
                                        __compId = translateToLigandName(authCompId, ligand, self.ccU)
                                        if __compId == ligand:
                                            ligands += 1
                                if ligands == 1:
                                    compId = __compId
                                elif len(self.nonPolyModel) == 1 and self.ccU.updateChemCompDict(authCompId, False):
                                    if self.ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'OBS':
                                        compId = self.nonPolyModel[0]['comp_id'][0]

                        if compId is not None:
                            compIdList.append(compId + '?')  # decide when coordinate is available
                            chemCompAtomIds = None
                            if self.ccU.updateChemCompDict(compId):
                                chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                            for k, atomNum in self.atomNumberDict.items():
                                if atomNum['chain_id'] == chainId and atomNum['seq_id'] == seqId:
                                    atomNum['comp_id'] = compId

                                    if compId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                                       and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                                        _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, compId, atomNum['auth_atom_id'], None, None, True)
                                    else:
                                        atomId = atomNum['auth_atom_id']

                                    if atomId.endswith('*'):
                                        _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                                        atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                    atomId = translateToStdAtomName(atomId, compId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)

                                    if chemCompAtomIds is not None and atomId in chemCompAtomIds:
                                        atomNum['atom_id'] = atomId
                                        if 'atom_type' in atomNum:
                                            del atomNum['atom_type']
                                    elif chemCompAtomIds is not None:
                                        if atomId in chemCompAtomIds:
                                            atomNum['atom_id'] = atomId
                                            if 'atom_type' in atomNum:
                                                del atomNum['atom_type']
                        else:
                            compIdList.append('.')
                            """ deferred to assignNonPolymer()
                            self.__f.append(f"[Unknown residue name] "
                                            f"{authCompId!r} is unknown residue name.")
                            """

                ps['comp_id'] = compIdList

            for k, atomNum in self.atomNumberDict.items():
                if 'atom_type' not in atomNum:
                    continue
                if 'comp_id' in atomNum and atomNum['comp_id'] != atomNum['auth_comp_id']\
                   and 'atom_id' not in atomNum:
                    compId = atomNum['comp_id']
                    if self.ccU.updateChemCompDict(compId):
                        chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                        if compId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                           and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, compId, atomNum['auth_atom_id'], None, None, True)
                        else:
                            atomId = atomNum['auth_atom_id']

                        if atomId.endswith('*'):
                            _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                            atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                        atomId = translateToStdAtomName(atomId, compId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)

                        if atomId is not None and atomId in chemCompAtomIds:
                            atomNum['atom_id'] = atomId
                            if 'atom_type' in atomNum:
                                del atomNum['atom_type']
                        elif atomNum['comp_id'] != atomNum['auth_comp_id']:
                            authCompId = translateToStdResName(atomNum['auth_comp_id'], ccU=self.ccU)
                            if self.ccU.updateChemCompDict(authCompId):
                                chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                                if authCompId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                                   and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                                    _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'], None, None, True)
                                else:
                                    atomId = atomNum['auth_atom_id']

                                if atomId.endswith('*'):
                                    _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                                    atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                atomId = translateToStdAtomName(atomId, authCompId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)

                                if atomId is not None and atomId in chemCompAtomIds:
                                    atomNum['atom_id'] = atomId
                                    if 'atom_type' in atomNum:
                                        del atomNum['atom_type']
                else:
                    authCompId = translateToStdResName(atomNum['auth_comp_id'], ccU=self.ccU)
                    if self.ccU.updateChemCompDict(authCompId):

                        if authCompId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                           and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'], None, None, True)
                        else:
                            atomId = atomNum['auth_atom_id']

                        if atomId.endswith('*'):
                            _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                            atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                        atomId = translateToStdAtomName(atomId, authCompId, ccU=self.ccU, unambig=self.unambig)
                        atomIds = self.__nefT.get_valid_star_atom_in_xplor(authCompId, atomId)[0]
                        if len(atomIds) == 1:
                            atomNum['atom_id'] = atomIds[0]
                            if 'atom_type' in atomNum:
                                del atomNum['atom_type']

            polySeqModel = copy.copy(self.polySeqModel)
            if self.__hasBranchedModel:
                polySeqModel.extend(self.__branchedModel)

            self.__seqAlign, compIdMapping = alignPolymerSequence(self.__pA, polySeqModel, self.polySeqPrmTop)

            if len(self.__seqAlign) == 0:
                for c in range(1, 5):
                    self.__seqAlign, compIdMapping = alignPolymerSequenceWithConflicts(self.__pA, polySeqModel, self.polySeqPrmTop, c)
                    if len(self.__seqAlign) > 0:
                        break

            if len(self.__seqAlign) == 0:
                len_cif_na = sum(len(ps_cif['seq_id']) for ps_cif in polySeqModel if 'identical_chain_id' in ps_cif and len(ps_cif['seq_id']) > 3)
                len_top_na = sum(len(ps_top['seq_id']) for ps_top in self.polySeqPrmTop
                                 if len(ps_top['seq_id']) > 3 and any(compId in ('DA?', 'DT?', 'DG?', 'DC?', 'A?', 'U?', 'G?', 'C?') for compId in ps_top['comp_id']))
                if len_cif_na == len_top_na:
                    chainIdList = []
                    seqIdList = []
                    authCompIdList = []
                    for ps_top in self.polySeqPrmTop:
                        len_ps_cif_seq = len(ps_top['seq_id'])
                        if len_ps_cif_seq > 3 and any(compId in ('DA?', 'DT?', 'DG?', 'DC?', 'A?', 'U?', 'G?', 'C?') for compId in ps_top['comp_id']):
                            chainId = ps_top['chain_id']
                            for seqId, compId in zip(ps_top['seq_id'], ps_top['auth_comp_id']):
                                chainIdList.append(chainId)
                                seqIdList.append(seqId)
                                authCompIdList.append(compId)

                    chainIndex = letterToDigit(self.polySeqModel[0]['chain_id']) - 1
                    idOffset = 0

                    touched = []

                    polySeqPrmTop = []
                    for ps_cif in polySeqModel:
                        len_ps_cif_seq = len(ps_cif['seq_id'])
                        if 'identical_chain_id' in ps_cif and len_ps_cif_seq > 3:
                            chainId = indexToLetter(chainIndex)
                            polySeqPrmTop.append({'chain_id': chainId,
                                                  'seq_id': seqIdList[idOffset:idOffset + len_ps_cif_seq],
                                                  'comp_id': ps_cif['comp_id'],
                                                  'auth_comp_id': authCompIdList[idOffset:idOffset + len_ps_cif_seq]})

                            for idx, (_chainId, _seqId) in enumerate(zip(chainIdList[idOffset:idOffset + len_ps_cif_seq],
                                                                         seqIdList[idOffset:idOffset + len_ps_cif_seq])):
                                for k, atomNum in self.atomNumberDict.items():
                                    if atomNum['chain_id'] == _chainId and atomNum['seq_id'] == _seqId:
                                        atomNum['chain_id'] = chainId
                                        atomNum['cif_comp_id'] = ps_cif['comp_id'][idx]
                                        touched.append(k)

                            idOffset += len_ps_cif_seq
                            chainIndex += 1

                    for ps_top in self.polySeqPrmTop:
                        if len(ps_top['seq_id']) > 3 and any(compId in ('DA?', 'DT?', 'DG?', 'DC?', 'A?', 'U?', 'G?', 'C?') for compId in ps_top['comp_id']):
                            continue
                        _chainId = copy.copy(ps_top['chain_id'])
                        chainId = indexToLetter(chainIndex)
                        ps_top['chain_id'] = chainId
                        polySeqPrmTop.append(ps_top)

                        for k, atomNum in self.atomNumberDict.items():
                            if k in touched:
                                continue
                            if atomNum['chain_id'] == _chainId:
                                atomNum['chain_id'] = chainId
                                touched.append(k)

                        chainIndex += 1

                    self.polySeqPrmTop = polySeqPrmTop

                    self.__seqAlign, compIdMapping = alignPolymerSequence(self.__pA, polySeqModel, self.polySeqPrmTop)

                    _seqAlign = copy.copy(self.__seqAlign)
                    for sa in _seqAlign:
                        if sa['ref_chain_id'] != sa['test_chain_id']:
                            self.__seqAlign.remove(sa)

            # test chain assignment before applying comp_id mapping
            self.__chainAssign, message = assignPolymerSequence(self.__pA, self.ccU, self.file_type, self.polySeqModel, self.polySeqPrmTop, self.__seqAlign)

            for cmap in compIdMapping:
                if any(True for ca in self.__chainAssign if ca['test_chain_id'] == cmap['chain_id']):
                    for k, atomNum in self.atomNumberDict.items():
                        if atomNum['chain_id'] == cmap['chain_id'] and atomNum['seq_id'] == cmap['seq_id']:
                            atomNum['comp_id'] = cmap['comp_id']
                            atomNum['auth_comp_id'] = cmap['auth_comp_id']
                            if 'atom_type' in atomNum:
                                authCompId = cmap['auth_comp_id']
                                if self.ccU.updateChemCompDict(authCompId):
                                    chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                                    if authCompId in nonPolyCompIdList and self.mrAtomNameMapping is not None\
                                       and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                                        _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'],
                                                                                  atomNum['comp_id'], None, True)
                                    else:
                                        atomId = atomNum['auth_atom_id']

                                    if atomId.endswith('*'):
                                        _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                                        atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                    atomNum['atom_id'] = translateToStdAtomName(atomId, authCompId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)
                                    del atomNum['atom_type']

            for k, atomNum in self.atomNumberDict.items():
                if 'atom_type' not in atomNum:
                    continue
                if 'atom_id' not in atomNum:
                    if 'comp_id' not in atomNum or atomNum['comp_id'] == atomNum['auth_comp_id']:
                        authCompId = translateToStdResName(atomNum['auth_comp_id'], ccU=self.ccU)

                        if self.mrAtomNameMapping is not None\
                           and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'], None, None, True)
                        else:
                            atomId = atomNum['auth_atom_id']

                        if self.ccU.updateChemCompDict(authCompId):
                            chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                            if atomId.endswith('*'):
                                _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                                atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                            atomId = translateToStdAtomName(atomId, authCompId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)
                            if atomId in chemCompAtomIds:
                                atomNum['atom_id'] = atomId
                                continue
                            if not self.unambig:
                                _, _, details = self.__nefT.get_valid_star_atom_in_xplor(authCompId, atomId)
                                if details is None:
                                    atomNum['atom_id'] = atomId
                                    continue
                            if self.__chemCompAtom is not None:
                                if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                    if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                        atomNum['atom_id'] = atomId
                                        continue
                                if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                    if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                        atomNum['atom_id'] = atomId
                                        continue
                            if atomId == "HO5'" and atomNum['seq_id'] == 1 and self.csStat.getTypeOfCompId(atomNum['auth_comp_id'])[1]:
                                continue
                            self.__f.append(f"[Unknown atom name] "
                                            f"{atomNum['auth_atom_id']!r} is not recognized as the atom name of {atomNum['auth_comp_id']!r} residue.")
                        elif self.__chemCompAtom is not None:
                            if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                    atomNum['atom_id'] = atomId
                                    continue
                            if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                    atomNum['atom_id'] = atomId
                                    continue

                    else:
                        authCompId = translateToStdResName(atomNum['auth_comp_id'], ccU=self.ccU)
                        if self.mrAtomNameMapping is not None\
                           and atomNum['auth_atom_id'][0] in protonBeginCode and k not in retrievedAtomNumList:
                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, authCompId, atomNum['auth_atom_id'],
                                                                      atomNum['comp_id'], None, True)
                        else:
                            atomId = atomNum['auth_atom_id']

                        if self.ccU.updateChemCompDict(authCompId):
                            chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                            if atomId.endswith('*'):
                                _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(authCompId, ccU=self.ccU))
                                atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                            atomId = translateToStdAtomName(atomId, authCompId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)
                            if atomId in chemCompAtomIds:
                                atomNum['atom_id'] = atomId
                                continue
                            if not self.unambig:
                                _, _, details = self.__nefT.get_valid_star_atom_in_xplor(authCompId, atomId)
                                if details is None:
                                    atomNum['atom_id'] = atomId
                                    continue
                            if self.__chemCompAtom is not None:
                                if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                    if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                        atomNum['atom_id'] = atomId
                                        continue
                                if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                    if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                        atomNum['atom_id'] = atomId
                                        continue
                            atomNum['atom_id'] = atomNum['auth_atom_id']
                            if atomNum['atom_id'] == "HO5'" and atomNum['seq_id'] == 1 and self.csStat.getTypeOfCompId(atomNum['comp_id'])[1]:
                                continue
                            self.__f.append(f"[Unknown atom name] "
                                            f"{atomNum['auth_atom_id']!r} is not recognized as the atom name of {atomNum['comp_id']!r} residue "
                                            f"(the original residue label is {atomNum['auth_comp_id']!r}).")
                        elif self.__chemCompAtom is not None:
                            if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                    atomNum['atom_id'] = atomId
                                    continue
                            if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                    atomNum['atom_id'] = atomId
                                    continue

            self.__chainAssign, message = assignPolymerSequence(self.__pA, self.ccU, self.file_type, self.polySeqModel, self.polySeqPrmTop, self.__seqAlign)

            if len(message) > 0:
                self.__f.extend(message)

            if len(self.__seqAlign) == 0:
                mrFormatName = getRestraintFormatName(self.file_type)
                _a_mr_format_name = 'the ' + mrFormatName

                ref_code = getOneLetterCodeCanSequence(self.polySeqModel[0]['comp_id'])
                test_code = getOneLetterCodeCanSequence(self.polySeqPrmTop[0]['comp_id'])

                hint = ''
                if abs(len(ref_code) - len(test_code)) < 20 and len(ref_code) > 40:
                    hint = f"For example, coordinates ({self.polySeqModel[0]['auth_chain_id']}): {ref_code} vs topology: {test_code}. "

                self.__f.append(f"[Sequence mismatch] Polymer sequence between the coordinate and {_a_mr_format_name} data does not match. {hint}"
                                "Please verify the two sequences and re-upload the correct file(s) if required.")

            assi_ref_chain_ids = {}
            proc_test_chain_ids, atom_nums, delete_atom_nums = [], [], []

            def update_atom_num(seq_align, orphan):
                ref_chain_id = seq_align['ref_chain_id']
                test_chain_id = seq_align['test_chain_id']

                if ref_chain_id in assi_ref_chain_ids or test_chain_id in proc_test_chain_ids:
                    return

                ps_cif = next(ps for ps in self.polySeqModel if ps['auth_chain_id'] == ref_chain_id)

                if ref_chain_id not in assi_ref_chain_ids:
                    assi_ref_chain_ids[ref_chain_id] = seq_align['length'] - seq_align['matched'] - seq_align['conflict']
                else:
                    assi_ref_chain_ids[ref_chain_id] -= seq_align['matched'] + seq_align['conflict']
                proc_test_chain_ids.append(test_chain_id)

                offset = first_seq_id = None

                for atom_num, atomNum in self.atomNumberDict.items():
                    if atom_num in atom_nums:
                        continue
                    if atomNum['chain_id'] == test_chain_id:
                        atom_nums.append(atom_num)

                        test_seq_id = atomNum['seq_id']

                        if first_seq_id is None:
                            first_seq_id = test_seq_id

                        if test_seq_id in seq_align['test_seq_id']:
                            idx = seq_align['test_seq_id'].index(test_seq_id)
                            if 'ref_auth_seq_id' in seq_align and idx < len(seq_align['ref_auth_seq_id']):
                                ref_seq_id = seq_align['ref_auth_seq_id'][idx]
                            elif offset is not None:
                                ref_seq_id = test_seq_id + offset
                            else:
                                continue
                        elif offset is not None:
                            ref_seq_id = test_seq_id + offset
                        else:
                            continue

                        if offset is None:
                            offset = ref_seq_id - test_seq_id

                        atomNum['chain_id'] = ref_chain_id
                        atomNum['seq_id'] = ref_seq_id

                        if ref_seq_id in ps_cif['auth_seq_id']:
                            idx = ps_cif['auth_seq_id'].index(ref_seq_id)
                            atomNum['comp_id'] = ps_cif['comp_id'][idx]
                            if 'atom_id' not in atomNum:
                                compId = atomNum['comp_id']
                                atomId = atomNum['auth_atom_id']
                                if self.ccU.updateChemCompDict(compId):
                                    chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                                    if atomId.endswith('*'):
                                        _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                                        atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                    atomId = translateToStdAtomName(atomId, compId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)
                                    if atomId in chemCompAtomIds:
                                        atomNum['atom_id'] = atomId
                                        continue
                                    if self.__chemCompAtom is not None:
                                        if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                            if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                                atomNum['atom_id'] = atomId
                                                continue
                                        if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                            if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                                atomNum['atom_id'] = atomId
                                                continue

                        if 'atom_id' in atomNum and orphan and test_seq_id == first_seq_id\
                           and self.csStat.peptideLike(translateToStdResName(atomNum['comp_id'], ccU=self.ccU)):
                            if self.ccU.updateChemCompDict(atomNum['comp_id']):
                                chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]
                                leavingAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList
                                                  if cca[self.ccU.ccaLeavingAtomFlag] == 'Y']
                                if atomNum['atom_id'] not in chemCompAtomIds or atomNum['atom_id'] in leavingAtomIds:
                                    delete_atom_nums.append(atom_num)

            trial = 0

            while True:

                orphanPolySeqPrmTop = []

                for ps in self.polySeqPrmTop:
                    test_chain_id = ps['chain_id']
                    if test_chain_id in proc_test_chain_ids:
                        continue
                    try:
                        ca = next(ca for ca in self.__chainAssign if ca['test_chain_id'] == test_chain_id)

                        ref_chain_id = ca['ref_chain_id']
                        sa = next((sa for sa in self.__seqAlign
                                   if sa['ref_chain_id'] == ref_chain_id and sa['test_chain_id'] == test_chain_id), None)

                        if sa is not None:  # and sa['conflict'] == 0:
                            update_atom_num(sa, False)

                    except StopIteration:
                        orphanPolySeqPrmTop.append(ps)

                resolved = False

                if len(orphanPolySeqPrmTop) > 0:
                    max_length = max(len(ps['seq_id']) for ps in orphanPolySeqPrmTop)
                    polySeqModel__ = [ps for ps in self.polySeqModel
                                      if ps['auth_chain_id'] not in assi_ref_chain_ids
                                      or assi_ref_chain_ids[ps['auth_chain_id']] >= max_length]
                    __seqAlign__, _ = alignPolymerSequence(self.__pA, polySeqModel__, orphanPolySeqPrmTop)
                    if len(__seqAlign__) > 0:
                        for sa in __seqAlign__:
                            if sa['conflict'] == 0:
                                update_atom_num(sa, True)

                                resolved = True

                    if not resolved:
                        for c in range(1, 5):
                            __seqAlign__, _ = alignPolymerSequenceWithConflicts(self.__pA, polySeqModel__, orphanPolySeqPrmTop, c)
                            if len(__seqAlign__) > 0:
                                for sa in __seqAlign__:
                                    if sa['conflict'] <= c:
                                        update_atom_num(sa, True)

                                        resolved = True
                            if resolved:
                                break

                if not resolved:
                    break

                trial += 1

                if trial > 10:
                    break

            for ps in self.polySeqPrmTop:
                test_chain_id = ps['chain_id']

                if test_chain_id in proc_test_chain_ids:
                    continue

                for cif_ps in self.polySeqModel:
                    ref_chain_id = cif_ps['auth_chain_id']

                    if ref_chain_id in assi_ref_chain_ids:
                        continue

                    len_gap = abs(len(ps['seq_id']) - len(cif_ps['auth_seq_id']))

                    if len_gap > 20:
                        continue

                    if len_gap == 0:
                        offset = cif_ps['auth_seq_id'][0] - ps['seq_id'][0]

                    for atomNum in self.atomNumberDict.values():
                        if atomNum['chain_id'] == test_chain_id:
                            atomNum['chain_id'] = ref_chain_id
                            if len_gap == 0:
                                atomNum['seq_id'] += offset

                    proc_test_chain_ids.append(test_chain_id)
                    assi_ref_chain_ids[ref_chain_id] = len_gap

            if len(delete_atom_nums) > 0:
                for atom_num in sorted(delete_atom_nums, reverse=True):
                    del self.atomNumberDict[atom_num]

            for atomNum in self.atomNumberDict.values():
                if 'atom_id' in atomNum and atomNum['atom_id'] in aminoProtonCode:
                    _seqKey = (atomNum['chain_id'], atomNum['seq_id'] - 1)
                    seqKey = (atomNum['chain_id'], atomNum['seq_id'])
                    if _seqKey in self.__coordUnobsRes and seqKey in self.__coordAtomSite:
                        coordAtomSite = self.__coordAtomSite[seqKey]
                        if atomNum['atom_id'] not in coordAtomSite['atom_id']:
                            for atomId in aminoProtonCode:
                                if atomId in coordAtomSite['atom_id']:
                                    atomNum['atom_id'] = atomId
                                    break

            if self.__chainAssign is not None:
                trimSequenceAlignment(self.__seqAlign, self.__chainAssign)

                if self.hasNonPolyModel:

                    # metal ion
                    if any(True for ps in self.polySeqPrmTop
                           if len(ps['seq_id']) == 1 and (ps['comp_id'][0].title() in NAMES_ELEMENT
                                                          or (len(ps['comp_id'][0]) > 2 and ps['comp_id'][0][:2].title() in NAMES_ELEMENT)
                                                          or (ps['comp_id'][0][-1] in ('+', '-') and ps['comp_id'][0][:-1].title() in NAMES_ELEMENT)
                                                          or (len(ps['comp_id'][0]) > 2 and ps['comp_id'][0][-2] in ('+', '-')
                                                              and ps['comp_id'][0][:-2].title() in NAMES_ELEMENT))):
                        self.assignMetalIon()

                    # other non-polymer
                    nonPolyIndices = [idx for idx, ps in enumerate(self.polySeqPrmTop)
                                      if not any(True for ca in self.__chainAssign
                                                 if ca['test_chain_id'] == ps['chain_id'])
                                      and len(set(ps['comp_id'])) > 0 and ps['comp_id'][0] == '.']

                    if len(nonPolyIndices) > 0:
                        self.assignNonPolymer(nonPolyIndices)

                        for idx in sorted(nonPolyIndices, reverse=True):
                            del self.polySeqPrmTop[idx]

            if self.hasNonPolyModel:
                compIdMapping = {}
                mappedSeqVal, mappedAtomNum = [], []

                for np in self.nonPolyModel:
                    authChainId = np['auth_chain_id']
                    authSeqId = np['auth_seq_id'][0]
                    compId = np['comp_id'][0]

                    for k, v in self.atomNumberDict.items():
                        if k in mappedAtomNum:
                            continue
                        if 'comp_id' in v and v['comp_id'] == compId:
                            seqKey = (v['comp_id'], v['chain_id'], v['seq_id'])
                            seqVal = (authChainId, authSeqId)
                            if seqKey not in compIdMapping:
                                if seqVal not in mappedSeqVal:
                                    compIdMapping[seqKey] = seqVal
                            if seqKey in compIdMapping:
                                v['chain_id'], v['seq_id'] = compIdMapping[seqKey]
                                mappedSeqVal.append(seqVal)
                                mappedAtomNum.append(k)

            if any(True for f in message if '[Concatenated sequence]' in f):  # DAOTHER-9511: resolve concatenated sequence
                test_chain_id_map = {}
                for ca in self.__chainAssign:
                    ref_chain_id = ca['ref_chain_id']
                    test_chain_id = ca['test_chain_id']
                    if test_chain_id not in test_chain_id_map:
                        test_chain_id_map[test_chain_id] = []
                    test_chain_id_map[test_chain_id].append(ref_chain_id)

                _test_chain_id_map = copy.copy(test_chain_id_map)
                for test_chain_id, cmap in _test_chain_id_map.items():
                    if len(cmap) < 2:
                        del test_chain_id_map[test_chain_id]

                if len(test_chain_id_map) > 0:
                    cmap = {}
                    for test_chain_id, ref_chain_ids in test_chain_id_map.items():
                        ref_chain_id0 = ref_chain_ids[0]
                        for ref_chain_id in ref_chain_ids[1:]:
                            sa = next((sa for sa in self.__seqAlign if sa['ref_chain_id'] == ref_chain_id and sa['test_chain_id'] == test_chain_id), None)
                            if sa is None:
                                continue
                            ps = next((ps for ps in self.polySeqModel if ps['auth_chain_id'] == ref_chain_id), None)
                            if ps is None:
                                continue
                            for auth_seq_id, comp_id in zip(ps['auth_seq_id'], ps['comp_id']):
                                seq_key = (ref_chain_id0, auth_seq_id)
                                cmap[seq_key] = (ref_chain_id, comp_id)
                    if len(cmap) > 0:
                        for atomNum in self.atomNumberDict.values():
                            seq_key = (atomNum['chain_id'], atomNum['seq_id'])
                            if seq_key in cmap:
                                atomNum['chain_id'], atomNum['comp_id'] = cmap[seq_key]
                                if 'atom_id' not in atomNum:
                                    compId = atomNum['comp_id']
                                    atomId = atomNum['auth_atom_id']
                                    if self.ccU.updateChemCompDict(compId):
                                        chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

                                        if atomId.endswith('*'):
                                            _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                                            atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                                        atomId = translateToStdAtomName(atomId, compId, chemCompAtomIds, ccU=self.ccU, unambig=self.unambig)
                                        if atomId in chemCompAtomIds:
                                            atomNum['atom_id'] = atomId
                                            continue
                                        if self.__chemCompAtom is not None:
                                            if 'comp_id' in atomNum and atomNum['comp_id'] in self.__chemCompAtom:
                                                if atomId in self.__chemCompAtom[atomNum['comp_id']]:
                                                    atomNum['atom_id'] = atomId
                                                    continue
                                            if 'cif_comp_id' in atomNum and atomNum['cif_comp_id'] in self.__chemCompAtom:
                                                if atomId in self.__chemCompAtom[atomNum['cif_comp_id']]:
                                                    atomNum['atom_id'] = atomId
                                                    continue

            # resolve ligand split during annotation (2miv)
            if self.mrAtomNameMapping is not None:
                for v in self.atomNumberDict.values():
                    authCompId = v['auth_comp_id']
                    if translateToStdResName(authCompId, ccU=self.ccU) in monDict3:
                        continue
                    seqId = v['seq_id']
                    authAtomId = v['auth_atom_id']
                    _seqId_, _compId_, _atomId_ = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, seqId, authCompId, authAtomId)
                    if _seqId_ != seqId and _compId_ != authCompId:
                        v['seq_id'] = _seqId_
                        v['comp_id'] = _compId_
                        v['atom_id'] = _atomId_

        finally:
            self.warningMessage = sorted(list(set(self.__f)), key=self.__f.index)

            self.isSegment.cache_clear()
            self.isSegmentWithAsymHint.cache_clear()
            self.isLigand.cache_clear()
            self.isMetalIon.cache_clear()
            self.isMetalElem.cache_clear()

            translateToStdAtomNameNoRef.cache_clear()
            translateToStdAtomNameWithRef.cache_clear()

    @functools.lru_cache(maxsize=128)
    def isSegment(self, prev_comp_id: Optional[str], prev_atom_name: str, comp_id: str, atom_name: str) -> bool:
        if prev_comp_id is None:
            return False
        is_prev_term_atom = prev_atom_name.endswith('T')
        if is_prev_term_atom and atom_name.endswith('T'):
            return True
        is_prev_3_prime_comp = prev_comp_id.endswith('3')
        if is_prev_3_prime_comp and (is_prev_term_atom
                                     or self.csStat.peptideLike(translateToStdResName(comp_id, ccU=self.ccU))):
            return True
        return comp_id.endswith('5')\
            and (is_prev_3_prime_comp
                 or self.csStat.peptideLike(translateToStdResName(prev_comp_id, ccU=self.ccU)))

    @functools.lru_cache(maxsize=128)
    def isSegmentWithAsymHint(self, prev_asym_id: Optional[str], prev_comp_id: Optional[str], prev_atom_name: str,
                              asym_id: str, comp_id: str, atom_name: str) -> bool:
        if prev_asym_id is None or prev_comp_id is None:
            return False
        if prev_asym_id != asym_id:
            return True
        is_prev_term_atom = prev_atom_name.endswith('T')
        if is_prev_term_atom and atom_name.endswith('T'):
            return True
        is_prev_3_prime_comp = prev_comp_id.endswith('3')
        if is_prev_3_prime_comp and (is_prev_term_atom
                                     or self.csStat.peptideLike(translateToStdResName(comp_id, ccU=self.ccU))):
            return True
        return comp_id.endswith('5')\
            and (is_prev_3_prime_comp
                 or self.csStat.peptideLike(translateToStdResName(prev_comp_id, ccU=self.ccU)))

    @functools.lru_cache(maxsize=128)
    def isLigand(self, prev_comp_id: Optional[str], comp_id: str) -> bool:  # pylint: disable=no-self-use
        if prev_comp_id is None or not self.hasNonPolyModel:
            return False
        prev_comp_id = prev_comp_id.upper()
        comp_id = comp_id.upper()
        for np in self.nonPolyModel:
            if prev_comp_id in np['comp_id']:
                if not any(True for np in self.nonPolyModel if comp_id in np['comp_id']):
                    return True
        if not prev_comp_id.endswith('3') or prev_comp_id == comp_id:
            return False
        for np in self.nonPolyModel:
            if comp_id in np['comp_id']:
                return True
        for np in self.nonPolyModel:
            if 'alt_comp_id' in np:
                if comp_id in np['alt_comp_id']:
                    return True
        return False

    @functools.lru_cache(maxsize=128)
    def isMetalIon(self, comp_id: Optional[str], atom_name: str) -> bool:  # pylint: disable=no-self-use
        if comp_id is None:
            return False
        if not comp_id.startswith(atom_name):
            return False
        if atom_name in NON_METAL_ELEMENTS:
            return False
        return (len(comp_id) > 2 and comp_id[:2].title() in NAMES_ELEMENT)\
            or (comp_id[-1] in ('+', '-') and comp_id[:-1].title() in NAMES_ELEMENT)\
            or (len(comp_id) > 2 and comp_id[-2] in ('+', '-') and comp_id[:-2].title() in NAMES_ELEMENT)

    @functools.lru_cache(maxsize=128)
    def isMetalElem(self, prev_atom_name: str, prev_seq_id: int, seq_id: int) -> bool:  # pylint: disable=no-self-use
        if len(prev_atom_name) == 0:
            return False
        return prev_seq_id != seq_id and prev_atom_name[0] not in NON_METAL_ELEMENTS\
            and (self.unambig or prev_atom_name[0] not in pseProBeginCode)

    def assignMetalIon(self):

        if not self.hasNonPolyModel:
            return

        metals = collections.Counter(ps['comp_id'][0] for ps in self.polySeqPrmTop
                                     if len(ps['seq_id']) == 1
                                     and (ps['comp_id'][0].title() in NAMES_ELEMENT
                                          or (len(ps['comp_id'][0]) > 2 and ps['comp_id'][0][:2].title() in NAMES_ELEMENT)
                                          or (ps['comp_id'][0][-1] in ('+', '-') and ps['comp_id'][0][:-1].title() in NAMES_ELEMENT)
                                          or (len(ps['comp_id'][0]) > 2 and ps['comp_id'][0][-2] in ('+', '-')
                                              and ps['comp_id'][0][:-2].title() in NAMES_ELEMENT))).most_common()

        for metal in metals:
            compId = metal[0]
            if compId.title() in NAMES_ELEMENT:
                pass
            elif len(compId) > 2 and compId[:2].title() in NAMES_ELEMENT:
                compId = compId[:2]
            elif compId[-1] in ('+', '-') and compId[:-1].title() in NAMES_ELEMENT:
                compId = compId[:-1]
            else:
                compId = compId[:-2]

            atomNums = [atomNum for atomNum in self.atomNumberDict.values()
                        if atomNum['auth_comp_id'].startswith(compId) and atomNum['auth_atom_id'] == compId]

            nonPolys = [nonPoly for nonPoly in self.nonPolyModel
                        if nonPoly['comp_id'][0] == compId]

            for atomNum, nonPoly in zip(atomNums, nonPolys):
                atomNum['chain_id'] = nonPoly['auth_chain_id']
                atomNum['seq_id'] = nonPoly['auth_seq_id'][0]

    def assignNonPolymer(self, nonPolyIndices: List[int]):

        if not self.hasNonPolyModel:
            return

        authCompIds = []

        for idx, ps in enumerate(self.polySeqPrmTop):
            if idx not in nonPolyIndices:
                continue
            for authCompId, compId in zip(ps['auth_comp_id'], ps['comp_id']):
                if compId != '.':
                    continue
                authCompIds.append(authCompId)

        nonPolyCompIds = collections.Counter(authCompIds).most_common()

        compIds = []
        for nonPoly in self.nonPolyModel:
            compId = nonPoly['comp_id'][0]
            if compId.title() in NAMES_ELEMENT:
                continue
            compIds.append(compId)

        refCompIds = collections.Counter(compIds).most_common()

        comp_id_mapping = {}

        for authCompId in nonPolyCompIds:
            refCompId = next((compId[0] for compId in refCompIds if compId[1] == authCompId[1] and compId[1] not in comp_id_mapping.values()), None)
            if refCompId is None:
                self.__f.append(f"[Unknown residue name] "
                                f"{authCompId[0]!r} is unknown residue name.")
                continue
            comp_id_mapping[authCompId[0]] = refCompId

        for authCompId, compId in comp_id_mapping.items():
            chemCompAtomIds = None
            if self.ccU.updateChemCompDict(compId):
                chemCompAtomIds = [cca[self.ccU.ccaAtomId] for cca in self.ccU.lastAtomList]

            authSeqKeys = []

            for idx, ps in enumerate(self.polySeqPrmTop):
                if idx not in nonPolyIndices:
                    continue
                _chainId = ps['chain_id']
                for _authCompId, _compId, _seqId in zip(ps['auth_comp_id'], ps['comp_id'], ps['seq_id']):
                    if _authCompId != authCompId or _compId != '.':
                        continue
                    authSeqKeys.append((_chainId, _seqId))

            nonPolys = [nonPoly for nonPoly in self.nonPolyModel
                        if nonPoly['comp_id'][0] == compId]

            reported_auth_atom_id = []

            for authSeqKey, nonPoly in zip(authSeqKeys, nonPolys):
                atomNums = [atomNum for atomNum in self.atomNumberDict.values()
                            if atomNum['chain_id'] == authSeqKey[0] and atomNum['seq_id'] == authSeqKey[1]]
                authAtomNames = [atomNum['auth_atom_id'] for atomNum in self.atomNumberDict.values()
                                 if atomNum['chain_id'] == authSeqKey[0] and atomNum['seq_id'] == authSeqKey[1]]

                for atomNum in atomNums:
                    atomNum['chain_id'] = nonPoly['auth_chain_id']
                    atomNum['seq_id'] = nonPoly['auth_seq_id'][0]
                    atomNum['comp_id'] = compId
                    authAtomId = atomNum['auth_atom_id']
                    if chemCompAtomIds is not None and authAtomId in chemCompAtomIds:
                        atomNum['atom_id'] = authAtomId
                    else:
                        dmpcNameSystemId = -1
                        if compId == 'PX4':
                            if 'OE' in authAtomNames:
                                dmpcNameSystemId = 1
                            elif 'OS31' in authAtomNames:
                                dmpcNameSystemId = 2
                            elif 'O21' in authAtomNames:
                                if 'C314' in authAtomNames:
                                    dmpcNameSystemId = 3
                                elif 'C114' in authAtomNames:
                                    dmpcNameSystemId = 4

                        if dmpcNameSystemId != -1:
                            atomId = translateToStdAtomNameOfDmpc(authAtomId, dmpcNameSystemId)
                        else:
                            atomId = translateToStdAtomName(authAtomId, compId, chemCompAtomIds, ccU=self.ccU)

                        if atomId.endswith('*'):
                            _, nucleotide, _ = self.csStat.getTypeOfCompId(translateToStdResName(compId, ccU=self.ccU))
                            atomId = atomId[:-1] + ("'" if nucleotide and not atomId[0].isdigit() else "")

                        if atomId in chemCompAtomIds:
                            atomNum['atom_id'] = atomId
                            continue

                        if not self.unambig:
                            _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId)
                            if details is None:
                                atomNum['atom_id'] = atomId
                                continue

                        if self.mrAtomNameMapping is not None:
                            _, _, atomId = retrieveAtomIdentFromMRMap(self.ccU, self.mrAtomNameMapping, None, compId, authAtomId, None, None, True)

                        if atomId in chemCompAtomIds:
                            atomNum['atom_id'] = atomId
                            continue

                        if not self.unambig:
                            _, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId)
                            if details is None:
                                atomNum['atom_id'] = atomId
                                continue

                        if authAtomId not in reported_auth_atom_id:
                            atomNum['atom_id'] = atomNum['auth_atom_id']
                            if authAtomId == "HO5'" and atomNum['seq_id'] == 1 and self.csStat.getTypeOfCompId(compId)[1]:
                                continue

                            self.__f.append(f"[Unknown atom name] "
                                            f"{authAtomId!r} is not recognized as the atom name of {compId!r} residue "
                                            f"(the original residue label is {authCompId!r}).")
                            reported_auth_atom_id.append(authAtomId)

    def getAtomNumberDict(self) -> dict:
        """ Return atomic number dictionary.
        """

        return self.atomNumberDict

    def getPolymerSequence(self) -> Optional[List[dict]]:
        """ Return polymer sequence of the topology file.
        """

        return None if self.polySeqPrmTop is None or len(self.polySeqPrmTop) == 0 else self.polySeqPrmTop

    def getSequenceAlignment(self) -> Optional[List[dict]]:
        """ Return sequence alignment between coordinates and topology.
        """

        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self) -> Optional[List[dict]]:
        """ Return chain assignment between coordinates and topology.
        """

        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign
