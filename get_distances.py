import preprocess as pp
import numpy

import sys
sys.path.append('unsupervised-random-forest/')
from unsupervised_random_forest import urf


specra_path   = '/storage/home/itamarreis/git/manga/test_data/spectra_final.npy'
spectra = numpy.load(specra_path)
#spectra = numpy.random.rand(1000,100)

#spectra = pp.norm_spectra(spectra)

urf_ = urf(n_trees = 100)
distance_matrix = urf_.get_distance(spectra)

numpy.save('distance_matrix', distance_matrix.astype('f2'))
