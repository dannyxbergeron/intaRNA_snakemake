import os
import subprocess
import pandas as pd

file = snakemake.input.master_file

output = snakemake.output.seq_fasta_dir
subprocess.call('mkdir -p {}'.format(output), shell=True)

chr_dir = snakemake.params.chr_dir

script = snakemake.params.rev_script

data = pd.read_csv(file, sep='\t')


def get_info(df, i, num):

    ID = df.at[i, 'single_id{}'.format(num)]
    contig = 'chr' + df.at[i, 'chr{}'.format(num)]
    start = df.at[i, 'start{}'.format(num)]-1
    end = df.at[i, 'end{}'.format(num)]
    strand = df.at[i, 'strand{}'.format(num)]

    return ID, contig, start, end, strand


for i in data.index:
    DG = data.at[i, 'DG']
    DG = DG.replace('|', '-')
    DG = os.path.join(output, DG)

    for num in [1, 2]:
        ID, contig, start, end, strand = get_info(data, i, num)

        if strand == '+':
            rev = ''
            to_rev = False
        else:
            rev = '_reverse'
            to_rev = True

        chrom_file = os.path.join(chr_dir, '{}.2bit'.format(contig))

        name = '{}_{}{}.fa'.format(DG, num, rev)
        cmd = 'twoBitToFa {}:{}:{}-{} {}'.format(chrom_file,
                                                 contig,
                                                 start,
                                                 end,
                                                 name)

        subprocess.call(cmd, shell=True)

        if to_rev:
            new_name = '{}_{}.fa'.format(DG, num)

            new_cmd = '{} {} > {}'.format(script, name, new_name)
            subprocess.call(new_cmd, shell=True)
            subprocess.call('rm {}'.format(name), shell=True)

subprocess.call(["touch", os.path.join(snakemake.params.path, 'token')], shell=False)
