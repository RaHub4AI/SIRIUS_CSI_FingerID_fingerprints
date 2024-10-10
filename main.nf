#!/bin/bash nextflow
nextflow.enable.dsl=2

// Importing modules
include { DATA2BATCH } from './modules/data2batch'
include { SMILES2SIRIUS6_FP } from './modules/smiles2sirius_fp'

workflow {
    data_ch = Channel.from(params.batch_size)
                     .combine(Channel.fromPath(params.data))
   
    input_ch = DATA2BATCH(data_ch).flatten()
                                  .combine(Channel.fromPath(params.sirius6_fingerid))

    SMILES2SIRIUS6_FP(input_ch)
}