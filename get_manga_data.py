import os
from marvin.tools.cube import Cube
from marvin.tools.maps import Maps
import numpy
import pandas
import os.path

#from tqdm import tqdm_notebook as tqdm

global metadata_path, wave_path, specra_path
raw_data_path = '/storage/fast/users/itamarreis/raw_data/'
metadata_path = '/storage/home/itamarreis/git/manga/meta.csv'
wave_path     = '/storage/home/itamarreis/git/manga/waves.npy'
specra_path   = '/storage/home/itamarreis/git/manga/spectra.npy'



global observed_wave
observed_wave = numpy.logspace(3.5589, 4.0151, 4563)
 # from https://www.sdss.org/dr15/manga/manga-data/data-model/#Cubes

def get_rest_wave(z):
    return observed_wave*(1 + z)

def get_raw_spectra_matrix(raw_data_path):

    if os.path.isfile(metadata_path):
        manga_metadata = pandas.read_csv(metadata_path)
        x_list = list(manga_metadata['x'].values)
        y_list = list(manga_metadata['y'].values)
        ra_list = list(manga_metadata['ra'].values)
        dec_list = list(manga_metadata['dec'].values)
        z_list = list(manga_metadata['z'].values)
        galaxy_name_list = list(manga_metadata['galaxy'].values)
        file_name_list = list(manga_metadata['cube_file_name'].values)

        waves = list(numpy.load(wave_path))
        spectra = list(numpy.load(specra_path))
        all_spxl_count = len(spectra)
    else:
        x_list = []
        y_list = []
        ra_list = []
        dec_list = []
        z_list = []
        galaxy_name_list = []
        file_name_list = []

        waves = []
        spectra = []
        all_spxl_count = 0

    for path, subdirs, files in os.walk(raw_data_path):
        for cube_file_name in files:
            if not cube_file_name in file_name_list:
                try:
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
                            x_list += [spx.x]
                            y_list += [spx.y]

                            z_list += [z]
                            ra_list += [spx.ra]
                            dec_list += [spx.dec]

                            galaxy_name_list += [galaxy]
                            file_name_list += [cube_file_name]

                            spectra += [spx.flux.value]
                            waves += [wave]
                            count = count + 1
                            all_spxl_count = all_spxl_count + 1

                    print('Got {} pixels from {}. Total so far {}:'.format( count, galaxy, all_spxl_count))
                    if all_spxl_count > 1000:
                        break

                except:
                    print('Error for cube {}'.format(cube_path))
                    pass



    manga_metadata = pandas.DataFrame()
    manga_metadata['x'] = x_list
    manga_metadata['y'] = y_list
    manga_metadata['ra'] = ra_list
    manga_metadata['dec'] = dec_list
    manga_metadata['galaxy'] = galaxy_name_list
    manga_metadata['cube_file_name'] = file_name_list

    return manga_metadata, numpy.array(waves), numpy.array(spectra)



if __name__ == '__main__':
    meta, waves, spectra = get_raw_spectra_matrix(raw_data_path)
    pandas.to_csv(metadata_path)
    numpy.save(wave_path, waves)
    numpy.save(specra_path, spectra)
