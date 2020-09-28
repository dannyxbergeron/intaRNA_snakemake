import os
import pandas as pd

files = sorted(list(snakemake.input.files))
path = snakemake.params.path
output = snakemake.output[0]

with open(output, 'w') as out:

    for f in files:

        file_name = f.replace('{}/'.format(path), '')

        DG = '_'.join(file_name.split('_')[:-1]).replace('-', '|')
        num = file_name.split('_')[-1][:-3]

        with open(f, 'r') as inp:
            for i, line in enumerate(inp.read().splitlines()):
                if i == 0:
                    out.write('>{}\n'.format(DG))
                else:
                    out.write('{}'.format(line))
            out.write('\n')
