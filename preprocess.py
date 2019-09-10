import numpy
from sklearn.preprocessing import Imputer
from scipy.interpolate import interp1d

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


def norm_spectra(spectra_mat):
    normed_spectra_mat = numpy.zeros(spectra_mat.shape)
    for i, spec in enumerate(spectra_mat):
        normed_spec = norm_spectrum(spec)
        normed_spectra_mat[i] = normed_spec

    return normed_spectra_mat


def same_grid(wave, waves, specs):
    """
    Putting all spectra on the same wavelength grid
    """
    print('Putting all spectra on the same grid wit min lambda = ', wave.min(), 'and max lambda = ', wave.max())

    specs_same_grid = numpy.zeros([specs.shape[0], wave.shape[0]])
    for i in range(waves.shape[0]):
        specs_same_grid[i] = same_grid_single(wave, waves[i], specs[i])

    return specs_same_grid

def same_grid_single(wave_common, wave_orig, spec_orig):
    """
    Putting a single spectrum on the common wavelength grid
    """
    spec = numpy.interp(wave_common, wave_orig, spec_orig, left=numpy.nan, right=numpy.nan)

    return spec

if __name__ == '__main__':
    w = numpy.load('waves.npy')
    s = numpy.load('spectra.npy')
    common_w = numpy.load('common_wave.npy')
    s = same_grid(common_w, w, s)
    s, common_w = impute_spec(s, common_w)
    s =  norm_spectra(s)
    numpy.save('spectra_final.npy', s)
