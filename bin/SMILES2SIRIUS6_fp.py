import numpy as np
import pandas as pd
import argparse
import os

import rdkit
from rdkit import Chem


from PyFingerprint.fingerprint import get_fingerprint, get_fingerprints

import jpype
import jpype.imports
from jpype.types import *

from java.util import Map
from org.openscience.cdk import DefaultChemObjectBuilder
from org.openscience.cdk.smiles import SmilesParser
from org.openscience.cdk.fingerprint import CircularFingerprinter

parser = argparse.ArgumentParser()

parser.add_argument('--SMILES', type=str, required=True,
                    help='List of SMILES')
parser.add_argument('--sirius6_fingerid', type=str, required=True,
                    help='SIRIUS+CSI:FingerID v6 fingerprint features')

args = parser.parse_args()

df = pd.read_csv(args.SMILES, sep='\t')
desc_fp = pd.read_csv(args.sirius6_fingerid, sep='\t')
abs_indices = desc_fp.absoluteIndex.values
SMARTS_fp3 = desc_fp[desc_fp.absoluteIndex < 55].description.values
ECFP6_hashes = list(map(lambda x: int(x.replace('ECFP6:','')), desc_fp[desc_fp.description.str.contains('ECFP6')].description.values))
SIRIUS_tailored_SMARTS = desc_fp[desc_fp.absoluteIndex > max(desc_fp[desc_fp.description.str.contains('ECFP6')].absoluteIndex)].description.values

def OpenBabelFP_calculator(smi, fp3_smarts=SMARTS_fp3):
    fp3_patterns = [Chem.MolFromSmarts(smarts) for smarts in fp3_smarts]
    return np.array([int(Chem.MolFromSmiles(smi).HasSubstructMatch(pattern)) for pattern in fp3_patterns])
    
def pyfingerprint_calculator(smi, index_list=abs_indices):
    fp_types = ['cdk-substructure', 'maccs', 'pubchem', 'klekota-roth']
    final_fp = []
    for type in fp_types:
        final_fp = np.concatenate((final_fp, get_fingerprint(smi, type).to_numpy().astype(int)))
    return final_fp[index_list[np.where((index_list >= 55) & (index_list < len(final_fp) + 55), True, False)] - 55]

def ecfp6_calculator(smi, hash_codes=ECFP6_hashes):
    builder = DefaultChemObjectBuilder.getInstance()
    smiles_parser = SmilesParser(builder)
    molecule = smiles_parser.parseSmiles(smi)
    fingerprinter = CircularFingerprinter()
    fingerprinter.calculate(molecule)
    count_fingerprint = fingerprinter.getCountFingerprint(molecule)
    num_bins = count_fingerprint.numOfPopulatedbins()
    hashed_fp = []
    for i in range(num_bins):
        hashed_fp.append(count_fingerprint.getHash(i))
    return np.array([1 if hash_code in hashed_fp else 0 for hash_code in hash_codes]) 

def tailoredFP_calculator(smi, smarts_patterns=SIRIUS_tailored_SMARTS):
    compiled_patterns = [Chem.MolFromSmarts(smarts) for smarts in smarts_patterns]
    return np.array([int(Chem.MolFromSmiles(smi).HasSubstructMatch(pattern)) for pattern in compiled_patterns])

def SIRIUS6FP_calculator(smi):
    try:
        return np.concatenate((OpenBabelFP_calculator(smi), pyfingerprint_calculator(smi), ecfp6_calculator(smi), tailoredFP_calculator(smi))).astype(int)
    except:
        return np.full(len(abs_indices), np.nan)
    
df['SIRIUS6_fp'] = df.SMILES.apply(lambda x: SIRIUS6FP_calculator(x))
columns = ['absoluteIndex_' + str(index) for index in desc_fp.absoluteIndex]
df = pd.concat([df, pd.DataFrame(df['SIRIUS6_fp'].to_list(), columns=columns)], axis=1)

file_name = os.path.basename(os.path.basename(args.SMILES))
df.to_csv(f'SIRIUS6_{file_name}', sep='\t', quoting=False, index=False)