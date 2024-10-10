#!/bin/bash nextflow 

process SMILES2SIRIUS6_FP {
    container = "quay.io/ida_rahu/sirius6_fp:v1.0.1"
    
    publishDir "${params.results}/", mode: 'copy', pattern: "*.tsv"
    
    input:
    tuple path(SMILES), path(sirius6_fingerid)

    output:
    path('*.tsv')
    
    shell:
    '''
    python !{baseDir}/bin/SMILES2SIRIUS6_fp.py \
     --SMILES !{SMILES} \ 
     --sirius6_fingerid !{sirius6_fingerid}
    '''
}