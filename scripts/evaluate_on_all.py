#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 This script calculates embedding results against all available fast running
 benchmarks in the repository and saves results as single row csv table.

 Usage: ./evaluate_on_all -f <path to file> -o <path to output file>

 NOTE:
 * script doesn't evaluate on WordRep (nor its subset) as it is non standard
 for now and long running (unless some nearest neighbor approximation is used).

 * script is using CosAdd for calculating analogy answer.

 * script is not reporting results per category (for instance semantic/syntactic) in analogy benchmarks.
 It is easy to change it by passing category parameter to evaluate_analogy function (see help).
"""
from optparse import OptionParser
import logging, sys
import os
from web.embeddings import fetch_GloVe, load_embedding
from web.datasets.utils import _get_dataset_dir

from web.evaluate import evaluate_on_all


# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
				  help="Path to the file with embedding. If relative will load from data directory.",
				  default=None)

parser.add_option("-p", "--format", dest="format",
				  help="Format of the embedding, possible values are: word2vec, word2vec_bin, dict and glove.",
				  default=None)

parser.add_option("-o", "--output", dest="output",
				  help="Path where to save results.",
				  default=None)

parser.add_option("-n", "--nonorm", dest="nonorm",
				  help="Do not take norm of vectors in word analogy.",action="store_true",
				  default=False)
				  
parser.add_option("-d", "--nocheat", dest="nocheat",
				  help="Do not remove hypothesis vectors from optional answer set.",action="store_true",
				  default=False)
				  
parser.add_option("-c", "--clean_words", dest="clean_words",
                  action="store_true",
				  help="Clean_words argument passed to load_embedding function. If set to True will remove"
					   "most of the non-alphanumeric characters, which should speed up evaluation.",
				  default=False)

if __name__ == "__main__":
	(options, args) = parser.parse_args()
	print options

	# Load embeddings
	fname = options.filename
#	fname='/home/natalie/NLPsoftware/retrofitting-master/output/glove.6B.300d.txt.out'
	print "FNAME", fname
#	sys.exit()
	if not fname:
		print "fetching new file!"
		w = fetch_GloVe(corpus="wiki-6B", dim=300)
	else:
		if not os.path.isabs(fname):
			fname = os.path.join(_get_dataset_dir(), fname)
			print fname
			sys.exit()

		format = options.format

		if not format:
			_, ext = os.path.splitext(fname)
			if ext == ".bin":
				format = "word2vec_bin"
			elif ext == ".txt":
				format = "word2vec"
			elif ext == ".pkl":
				format = "dict"

#		assert format in ['word2vec_bin', 'word2vec', 'glove', 'bin'], "Unrecognized format"

		load_kwargs = {}
		if format == "glove":
			vocab_size = sum(1 for line in open(fname))
			dim = len(next(open(fname)).split()) - 1
			load_kwargs={"vocab_size": vocab_size, "dim": dim}
		w = load_embedding(fname, format=format, normalize=True, lower=True, clean_words=options.clean_words,
						   load_kwargs=load_kwargs, nonorm=options.nonorm, nocheat=options.nocheat)

	out_fname = options.output if options.output else "results.csv"

	results = evaluate_on_all(w, options.nocheat)

	logger.info("Saving results...")
	print(results)
	results.to_csv(out_fname)
