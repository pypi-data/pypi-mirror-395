import os
import time
import numpy as np

# SNR = [10000]
SNR = [100, 1000, 10000, 100000]
upsamplings = [1]
# upsamplings = [6]

instrument = ['tinytim10']
file_to_run = '../1_generate_psf.py'
sim = './mock_stars_shift05_oddkernel_multiple'

lambda_scale = 1.
lambda_hf = 1.
niter = 1500
rerun = True
plot = False
no_bkg_fit = False
regularize_full_psf = False
method_noise = 'MC'
simout = 'output_'+method_noise
seeds = np.arange(1)

for inst in instrument:
    for seed in seeds:
        for SN in SNR:
            for upsampling in upsamplings:
                folder = './%s/%s/seed_%i/SNR_%2.f/'%(sim, inst, seed, SN)
                # folder = './%s/%s/notebook_data/'%(sim, inst)
                datapath = os.path.join(folder, 'stars')
                noise_path = os.path.join(folder, 'noise_maps')
                # datapath = '../../notebooks/data/1_observations'
                if no_bkg_fit:
                    outputpath = os.path.join(folder, simout + '_noreg%i'%upsampling)
                elif regularize_full_psf:
                    outputpath = os.path.join(folder, simout + '_fullreg%i' % upsampling)
                else :
                    outputpath = os.path.join(folder, simout + '_%i'%upsampling)

                if not os.path.isdir(outputpath):
                    os.mkdir(outputpath)
                else :
                    if not rerun:
                        continue

                argument = '--data_path %s --output_path %s '%(datapath,outputpath)
                argument += '--lambda_scales %2.2e '%lambda_scale
                argument += '--lambda_hf %2.2e '%lambda_hf
                argument += '--niter %i '%niter
                argument += '--subsampling_factor %i '%upsampling
                argument += '--method %s '%method_noise
                if regularize_full_psf:
                    argument += '--regularize_full_psf '
                if plot:
                    argument += '--plot-interactive '
                if no_bkg_fit :
                    argument += '--no_bkg_fit '
                argument += '--noise_map --noise_map_path %s '%noise_path
                start_time = time.time()
                cmd = 'python3.8 %s %s'%(file_to_run, argument)
                print(cmd)
                os.system('python3.8 %s %s'%(file_to_run, argument))
                print('Running in %2.2f seconds'%(time.time() - start_time))