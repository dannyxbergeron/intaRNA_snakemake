import pandas as pd

starting_file = snakemake.input.starting
analysed_file = snakemake.input.inta

output = snakemake.output.final

start = pd.read_csv(starting_file, sep='\t')
analysed = pd.read_csv(analysed_file, sep='\t')

analysed = analysed[['start1', 'end1', 'start2', 'end2', 'subseqDP',
       'hybridDP', 'E', 'DG']]
analysed.columns = ['off_start1', 'off_end1', 'off_start2', 'off_end2', 'subseqDP',
       'hybridDP', 'E', 'DG']

final_df = start.merge(analysed, on='DG', how='left')

final_df.to_csv(output, sep='\t', index=False)
