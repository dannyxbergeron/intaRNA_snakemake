import os
import subprocess

chrom = snakemake.params['chrom']
release = snakemake.params['release']

for chr in chrom:
    link = 'ftp://ftp.ensembl.org/pub/release-{}'.format(release) + \
            '/fasta/homo_sapiens/dna/' + \
            'Homo_sapiens.GRCh38.dna.chromosome.{}.fa.gz'.format(chr)
    out = os.path.join(snakemake.params['chr_dir'], 'chr{}.fa.gz'.format(chr))
    cmd = 'axel -a -o {} {}'.format(out, link)
    subprocess.call(cmd, shell=True)
    cmd = 'gunzip {}'.format(out)
    subprocess.call(cmd, shell=True)
