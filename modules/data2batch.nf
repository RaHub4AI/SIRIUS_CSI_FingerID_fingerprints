#!/usr/bin/env nextflow

process DATA2BATCH {
    container = "quay.io/ida_rahu/sirius6_fp:v1.0.1"
    
    input:
    tuple val(batch_size), path(data)

    output:
    path("${data.baseName}_*.tsv")

    shell:
    '''
    basename=$(basename "!{data}" .tsv)
    
    # Preprocess the file to remove trailing spaces and carriage returns
    sed '1s/[ \t]*$//' "!{data}" | tr -d '\\r' > cleaned_file.tsv
    
    # Extract SMILES column to a temporary file
    awk -F'\\t' '
        BEGIN {OFS="\\t"} 
        NR==1 {
            colnum = -1
            for (i=1; i<=NF; i++) {
                header = $i
                gsub(/^[ \t]+|[ \t]+$/, "", header)  # Trim leading and trailing whitespace
                if (header == "SMILES") colnum = i
            }
            if (colnum == -1) { print "Column \'SMILES\' not found"; exit 1 }
        }
        NR>1 {print $colnum}
    ' cleaned_file.tsv > temp_SMILES.txt
    
    if [ ! -s temp_SMILES.txt ]; then
        echo "No SMILES data found or file is empty."
        exit 1
    fi

    # Count the number of rows
    row_count=$(wc -l < temp_SMILES.txt)

    # If the number of rows is less than or equal to the batch size, write all to one file
    if [ "$row_count" -le "!{batch_size}" ]; then
        echo -e "SMILES" > "${basename}_1.tsv"
        cat temp_SMILES.txt >> "${basename}_1.tsv"
    else
        split -l !{batch_size} temp_SMILES.txt "output_chunk_"

        counter=1
        for file in output_chunk_*
        do
            echo -e "SMILES" > "${basename}_\${counter}.tsv"
            cat "$file" >> "${basename}_\${counter}.tsv"
            rm "$file"
            ((counter++))
        done
    fi

    rm temp_SMILES.txt cleaned_file.tsv
    '''
}
