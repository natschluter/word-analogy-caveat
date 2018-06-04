
import glob

dir='/home/natalie/NLPsoftware/word-embeddings-benchmarks-master/results/'
#outfile=open('allscores.csv','w')
#count=0
#for file in glob.glob(dir+'*c_nocheat.score'):
#	base=file.split('/')[-1]
#	infile=open(file,'r')
#	lines=infile.readlines()
#	if count==0:
#		outfile.write(lines[0])
#	count+=1
#	outfile.write(base+lines[1][1:])
#	infile.close()
#outfile.close()

outfile=open('allscores.tex','w')
count=0
dims=['50','100','300']

for d in dims:
	files=glob.glob(dir+'glove.6B.'+d+'d.txt_c*')
	files.sort()
	c2=True
	indices=[15,16,17]
	#,1AP,2BLESS,3Battig,4ESSLI_1a,5ESSLI_2b,6ESSLI_2c,7MEN,8MTurk,9RG65,10RW,11SimLex999,12WS353,13WS353R,14WS353S,15Google,16MSR,17SemEval2012_2
	#,AP,BLESS,Battig,ESSLI_1a,ESSLI_2b,ESSLI_2c,MEN,MTurk,RG65,RW,SimLex999,WS353,WS353R,WS353S,Google,MSR,SemEval2012_2

	for file in files:
		base=file.split('/')[-1].split('.')[-2]
		suff=base.split('_')[2:]
		print suff
		infile=open(file,'r')
		lines=infile.readlines()
		if count==0:
			data=lines[0].strip().split(',')
			print data
			header='$d$&&'+'&'.join([data[i] for i in xrange(len(data)) if i in indices])+'\\\\\n'
			print header
			outfile.write(header)
		count+=1
		data=lines[1].strip().split(',')
		if len(suff)==0:
			s='&&'+'&'.join([str(round(float(x),4)*100) for x in [data[i] for i in xrange(len(data)) if i in indices]])+'\\\\\n'
			print s
			if c2:
				s=d+s
		elif len(suff)==2:
			s='&\\textsc{H,D}&'+'&'.join([str(round(float(x),4)*100) for x in [data[i] for i in xrange(len(data)) if i in indices]])+'\\\\\n'
			print s
			if c2:
				s=d+s
		elif 'nonorm' in suff:
			s='&\\textsc{D}&'+'&'.join([str(round(float(x),4)*100) for x in [data[i] for i in xrange(len(data)) if i in indices]])+'\\\\\n'
			print s
			if c2:
				s=d+s
		else:
			s='&\\textsc{H}&'+'&'.join([str(round(float(x),4)*100) for x in [data[i] for i in xrange(len(data)) if i in indices]])+'\\\\\n'
			print s
			if c2:
				s=d+s
		outfile.write(s)
		infile.close()
		c2=False
outfile.close()

