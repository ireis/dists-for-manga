import numpy
from sklearn.preprocessing import Imputer

def impute_spec(specs, wave):

    imp = Imputer(missing_values='NaN', strategy='median', axis=0)
    imp = imp.fit(specs)
    specs_imp = imp.transform(specs)
    wave_imp = imp.transform(wave.reshape(1, -1)).T

    return specs_imp, wave_imp



def norm_spectrum(spec):
    """
    Normalize spectrum - divide by median (clipped to one)
    :param spec:
    :return:
    """
    spec_norm = numpy.nanmedian(spec)
    #if spec_norm >= 1:
    spec = (spec / spec_norm)
    #else:
    #    spec = spec + (1 - spec_norm)

    return spec


def norm_spectrum_all(spectra_mat):
    normed_spectra_mat = numpy.zeros(spectra_mat.shape)
    for i, spec in enumerate(spectra_mat):
        normed_spec = norm_spectrum(spec)
        normed_spectra_mat[i] = normed_spec

    return normed_spectra_mat
