
import glob
import numpy as np
import scipy.stats

indir='/home/natalie/data/'
norms=[]
outfile=open('norms.tsv','w')
for file in glob.glob(indir+'glove*.txt'):
	del norms[:]
	b=file.split('/')[-1]
	print b
	infile=open(file, 'r')
	norms=[np.linalg.norm(np.array([float(x) for x in line.strip().split()[1:]])) for line in infile.readlines()]
	outfile.write(b+'\t'+'\t'.join([str(x) for x in scipy.stats.describe(norms)])+'\n')
	infile.close()
outfile.close()