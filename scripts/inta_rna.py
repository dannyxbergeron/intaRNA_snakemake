import subprocess
from io import StringIO
import shlex
import pandas as pd

files = sorted(list(snakemake.input.files))
path = snakemake.params.path
output = snakemake.output[0]

col_names = ['id1', 'start1', 'end1', 'id2', 'start2', 'end2', 'subseqDP',
       'hybridDP', 'E', 'DG']
master_df_list = []

def process(file):

    file_name = file.replace('{}/'.format(path), '')

    DG = '_'.join(file_name.split('_')[:-1]).replace('-', '|')
    num = file_name.split('_')[-1][:-3]

    return file, file_name, DG, num


for idx in range(0, len(files), 2):

    file1, file_name1, DG1, num1 = process(files[idx])
    file2, file_name2, DG2, num2 = process(files[idx+1])

    cmd_str = 'IntaRNA -q {} -t {} --outMode C --outSep=,'.format(file1, file2)
    cmd = shlex.split(cmd_str)
    p = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = p.communicate()

    result = StringIO(stdout.decode('utf-8'))
    df = pd.read_csv(result)

    if not df.empty:
        df['DG'] = DG1
        master_df_list.append(df.iloc[0].tolist())

master_df = pd.DataFrame(master_df_list, columns=col_names)

master_df.to_csv(output, sep='\t', index=False)
