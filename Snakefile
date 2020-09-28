import os

configfile: "config.json"

chr_names = [x for x in range(1, 23)] + ['X', 'Y', 'MT']

rule all:
    input:
        final = config['final_file'],
        final_path = config['path']['final']

rule download_chrom:
    output:
        expand('chrom/chr{chr_name}.fa', chr_name=chr_names)
    params:
        chr_dir = 'chrom',
        release = 87,
        chrom = chr_names
    script:
        'scripts/download_chrom.py'

rule change_header:
    input:
        'chrom/chr{chr_name}.fa'
    output:
        'chrom/modif_chr{chr_name}.fa'
    shell:
        """awk '{{if(NR == 1){{print ">chr" substr($1,2)}}else{{print$0}}}}' {input} > {output}"""


rule tobittofa:
    input:
        modif = 'chrom/modif_chr{chr_name}.fa',
        original = 'chrom/chr{chr_name}.fa'
    output:
        'chrom/chr{chr_name}.2bit'
    shell:
        "faToTwoBit {input.modif} {output} && rm {input.original} && rm {input.modif}"

checkpoint extract_coord:
    input:
        master_file = config['raw_file']
    params:
        chr_dir = 'chrom',
        rev_script = 'scripts/reverseComplementFa',
        path = 'data'
    conda:
        "envs/pandas.yaml"
    output:
        seq_fasta_dir = directory("data/seq_fasta"),
        tok = 'data/token'
    script:
        "scripts/extract_coord.py"


def gather_(wildcards):
    checkpoint_output = checkpoints.extract_coord.get(**wildcards).output.seq_fasta_dir
    # That will raise if not ready.

    ivals = glob_wildcards(os.path.join(checkpoint_output,
                                        "{i}.fa")).i
    return expand("data/seq_fasta/{i}.fa", i=ivals)


rule merge_seqs:
    input:
        files = gather_,
        tok = 'data/token'
    params:
        path = 'data/seq_fasta',
    conda:
        "envs/pandas.yaml"
    output:
        'data/merged_seq/merged.tsv'
    script:
        'scripts/merge_seq.py'

# rule rnaplex:
#     input:
#         merged = 'data/merged_seq/merged.tsv'
#     output:
#         analysed = 'data/merged_seq/analysed_merged.tsv',
#         tok = 'data/token2'
#     shell:
#         """
#         RNAplex < {input.merged} | scripts/RNAplexProcess | awk '$2 != ""' > {output.analysed};
#         touch {output.tok}
#         """

rule intarna:
    input:
        files = gather_,
        tok = 'data/token'
    params:
        path = 'data/seq_fasta'
    conda:
        "envs/intarna.yaml"
    output:
        'data/merged_seq/intaRNA_analysed_merged.tsv'
    script:
        'scripts/inta_rna.py'

rule merge_intaRNA:
    input:
        inta = 'data/merged_seq/intaRNA_analysed_merged.tsv',
        starting = config['raw_file']
    conda:
        "envs/pandas.yaml"
    output:
        final = config['final_file']
    script:
        'scripts/merge_intaRNA.py'

rule ship_back:
    input:
        final = config['final_file']
    output:
        final_path_output = config['path']['final']
    params:
        final_path = config['path']['final']
    shell:
        'cp {input.final} {output.final_path_output}'
