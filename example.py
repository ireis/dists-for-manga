# coding: utf-8
import numpy, pandas
s = numpy.load('test_data/spectra_final.npy') # processed spectra
w = numpy.load('test_data/common_wave.npy') # common wavelength grid
m = pandas.read_csv('test_data/meta.csv') # metadata (galaxy name, pixel coordinates)
n = numpy.load('test_data/nns.npy') # 100 nearest neighbors for each spectrum
# dmt = numpy.load('test_data/distance_matrix.npy') # full distance matrix
m.head()
numpy.unique(m['galaxy'].iloc[n[0]], return_counts=True) # 65 of the 100 most similar spectra of spectrum 0 are from the same galaxy
