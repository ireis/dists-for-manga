import os
from marvin.tools.cube import Cube
from marvin.tools.maps import Maps
import numpy
import pandas
#from tqdm import tqdm_notebook as tqdm

data_path = '/storage/fast/users/itamarreis/raw_data'



global observed_wave
observed_wave = numpy.logspace(3.5589, 4.0151, 4563)
 # from https://www.sdss.org/dr15/manga/manga-data/data-model/#Cubes

def get_rest_wave(z):
    return observed_wave*(1 + z)

def get_raw_spectra_matrix(data_path):
    x_list = []
    y_list = []
    ra_list = []
    dec_list = []
    z_list = []
    galaxy_name_list = []

    waves = []
    spectra = []

    for path, subdirs, files in os.walk(data_path):
        for cube_file_name in files:

            cube_path = os.path.join(path, cube_file_name)
            cube = Cube(cube_path)

            galaxy = cube.nsa['iauname']
            z = cube.nsa['z']
            wave = get_rest_wave(z)

            maps = cube.getMaps()
            snr = maps.bin_snr
            high_snr_pixels = numpy.where(snr.value > 10)
            nof_high_snr_pixels = high_snr_pixels[0].size
            spxls = cube[high_snr_pixels]

            count = 0
            for spx in spxls:
                if spx.quality_flags[1].bits is None:
                    x_list += [spx.x_cen]
                    y_list += [spx.y_cen]

                    z_list += [z]
                    ra_list += [spx.ra]
                    dec_list += [spx.dec]

                    galaxy_name_list += [galaxy]

                    spectra += [spx.flux.value]
                    waves += [wave]
                    count = count + 1


            print('Got {} pixels from {}', count, galaxy)

            #except:
            #    print('Error for cube {}'.format(cube_path))
            #    pass

    manga_metadata = pandas.DataFrame()
    manga_metadata['x'] = x_list
    manga_metadata['y'] = y_list
    manga_metadata['ra'] = ra_list
    manga_metadata['dec'] = dec_list
    manga_metadata['galaxy'] = galaxy_name_list
    manga_metadata['snr'] = snr_list

    return manga_metadata, numpy.array(waves), numpy.array(spectra)



if __name__ == '__main__':
    meta, waves, spectra = get_raw_spectra_matrix(data_path)
    pandas.to_csv(meta, index = False)
    numpy.save('waves', waves)
    numpy.save('spectra', spectra)
