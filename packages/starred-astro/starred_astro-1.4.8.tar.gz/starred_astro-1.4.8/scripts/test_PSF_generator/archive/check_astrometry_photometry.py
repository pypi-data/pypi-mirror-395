import os
import astropy.io.fits as fits
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
import check_utils as cu

SNR = [100,1000,10000,100000]
# SNR = [ 100000, 300000]
# SNR = [10000]
# instrument = ['WFI']
instrument = ['WFI_odd']
upsamples = [1,2,3]
# upsamples = [2]
path = './mock_stars_shift05_oddkernel_multiple'
output = 'output_MC' #output, output_noreg, output_fullreg
psfr_folder = 'psfr_output_with_noise_maps'
photutils_folder = 'photutils_output'
# psfr_folder = 'psfr_output_with_noise_maps'
bkg_noise = 10
compare_psfr = True
compare_photutils = True
verbose = True
plot_errorbar = False
correct_offset = True
show=False
seeds = np.arange(10)

for inst in instrument:
    error_astrom = np.zeros((len(SNR),len(upsamples), 3, len(seeds))) # Stat, systematic and total MAE error
    error_photom = np.zeros((len(SNR),len(upsamples), 3, len(seeds)))
    error_ap = np.zeros((len(SNR), 3, len(seeds)))

    error_astrom_psfr = np.zeros((len(SNR), len(upsamples), 3, len(seeds)))  # median RMS error, std of the RMS error
    error_photom_psfr = np.zeros((len(SNR), len(upsamples), 3, len(seeds)))  # median RMS error, std of the RMS error
    error_astrom_photutils = np.zeros((len(SNR), len(upsamples), 3, len(seeds)))  # median RMS error, std of the RMS error
    error_photom_photutils = np.zeros((len(SNR), len(upsamples), 3, len(seeds)))  # median RMS error, std of the RMS error

    for kk, seed in enumerate(seeds):
        for ii,SN in enumerate(SNR):
            folder = os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i' % SN)
            aperture_photometry = cu.get_aperture_photometry(folder)

            for jj,upsample in enumerate(upsamples):
                print('### ', inst, ' seed:', seed, ' SNR : ', SN, ' upsampling :', upsample,'###')
                model_pkl = os.path.join(path,inst, 'seed_%i'%seed, 'SNR_%i'%SN, output+'_%i'%upsample, 'model.pkl')
                pkl_true = os.path.join(path,inst,'seed_%i'%seed, 'SNR_%i'%SN,'flux_mag.pkl')
                outpath = os.path.join(path, inst,'seed_%i'%seed, 'results_'+output)
                psfr_path = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, psfr_folder, 'psfr_upsampling%i.fits'%upsample)
                psfr_center_path = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, psfr_folder, 'center_list_upsampling%i.txt'%upsample)
                psfr_amp_path = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, psfr_folder, 'fluxes_upsampling%i.txt'%upsample)

                photutils_path = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, photutils_folder, 'photutils_upsampling%i.fits'%upsample)
                photutils_center_path = os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i' % SN, photutils_folder, 'center_list_upsampling%i.txt'%upsample)
                photutils_amp_path = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN, photutils_folder, 'fluxes_upsampling%i.txt'%upsample)

                if not os.path.exists(outpath):
                    os.mkdir(outpath)

                with open(pkl_true, 'rb') as f:
                    kwargs_true = pkl.load(f)
                try :
                    with open(model_pkl, 'rb') as f:
                        model, kwargs_final, norm = pkl.load(f)
                    if not hasattr(model, 'shift_direction'):
                        model.shift_direction = 1.

                except FileNotFoundError as e:
                    print(e)
                    error_astrom[ii, jj, :, kk] = np.nan
                    error_photom[ii, jj, :, kk] = np.nan
                else :
                    error_astrom[ii, jj, 0, kk], error_astrom[ii, jj, 1, kk], error_astrom[ii, jj, 2, kk] = cu.get_astrometric_error(model, kwargs_final, kwargs_true, correct_offset=correct_offset, verbose = verbose)
                    error_photom[ii, jj, 0, kk], error_photom[ii, jj, 1, kk], error_photom[ii, jj, 2, kk]= cu.get_photometric_error(model, norm, kwargs_final, kwargs_true, high_res= False, verbose=verbose)
                    if jj == 0 :
                        error_ap[ii, 0, kk], error_ap[ii, 1, kk], error_ap[ii, 2, kk] = cu.get_aperture_photometric_error(kwargs_true, aperture_photometry, verbose=True)

                if compare_psfr:
                    # PSFr astrometry
                    try:
                        centers = np.loadtxt(psfr_center_path)
                        amps = np.loadtxt(psfr_amp_path)
                    except FileNotFoundError as e:
                        print('No PSFr reconstruction for upsample %i SNR %i'%(upsample, SN))
                        error_astrom_psfr[ii, jj, 0, kk], error_astrom_psfr[ii, jj, 1, kk], error_astrom_psfr[ii, jj, 2, kk] = np.nan, np.nan, np.nan
                        error_photom_psfr[ii, jj, 0, kk], error_photom_psfr[ii, jj, 1, kk], error_photom_psfr[ii, jj, 2, kk]= np.nan, np.nan, np.nan
                    else:
                        if verbose:
                            print ('#### PSFr error ####')
                        error_astrom_psfr[ii, jj, 0, kk], error_astrom_psfr[ii, jj, 1, kk], error_astrom_psfr[ii, jj, 2, kk] = cu.get_astrometric_error(centers, None, kwargs_true, verbose = verbose)
                        error_photom_psfr[ii, jj, 0, kk], error_photom_psfr[ii, jj, 1, kk], error_photom_psfr[ii, jj, 2, kk] = cu.get_photometric_error(amps, None, None, kwargs_true, high_res= False, verbose=verbose)

                if compare_photutils:
                    try:
                        centers_photutils = np.loadtxt(photutils_center_path)
                        amps_phot = np.loadtxt(photutils_amp_path)
                    except FileNotFoundError as e:
                        print('No photutils reconstruction for upsample %i SNR %i' % (upsample, SN))
                        error_astrom_photutils[ii, jj, 0, kk], error_astrom_photutils[ii, jj, 1, kk], error_astrom_photutils[ii, jj, 2, kk] = np.nan, np.nan, np.nan
                        error_photom_photutils[ii, jj, 0, kk], error_photom_photutils[ii, jj, 1, kk], error_photom_photutils[ii, jj, 2, kk] = np.nan, np.nan, np.nan
                    else :
                        if verbose:
                            print ('#### Photutils PSF error ####')
                        error_astrom_photutils[ii, jj, 0, kk],  error_astrom_photutils[ii, jj, 1, kk], error_astrom_photutils[ii, jj, 2, kk] = cu.get_astrometric_error(centers_photutils, None, kwargs_true, verbose = verbose)
                        error_photom_photutils[ii, jj, 0, kk], error_photom_photutils[ii, jj, 1, kk], error_photom_photutils[ii, jj, 2, kk] = cu.get_photometric_error(amps_phot, None, None, kwargs_true, high_res=False,verbose=verbose)

                print(' --- Photometry --- ')
                print('Starred errors :', error_photom[ii, jj, :, kk])
                if compare_psfr:
                    print('PSFr errors :', error_photom_psfr[ii, jj, :, kk])
                if compare_photutils :
                    print('Photutils errors :', error_photom_photutils[ii, jj, :, kk])
                print('Aperture errors :', error_ap[ii, :, kk])

                print(' --- Astrometry --- ')
                print('Starred errors :', error_astrom[ii, jj, :, kk])
                if compare_psfr:
                    print('PSFr errors :', error_astrom_psfr[ii, jj, :, kk])
                if compare_photutils:
                    print('Photutils errors :', error_astrom_photutils[ii, jj, :, kk])

        with open(os.path.join(outpath, 'starred_astro-photo_metrics.pkl'),'wb') as f:
            pkl.dump([error_astrom[:,:,:,kk], error_photom[:,:,:,kk]], f)
        if compare_psfr:
            with open(os.path.join(outpath, 'psfr_astro-photo_metrics.pkl'), 'wb') as f:
                pkl.dump([error_astrom_psfr[:,:,:,kk], error_photom_psfr[:,:,:,kk]], f)
        if compare_photutils:
            with open(os.path.join(outpath, 'photutils_astro-photo_metrics.pkl'), 'wb') as f:
                pkl.dump([error_astrom_photutils[:,:,:,kk], error_photom_photutils[:,:,:,kk]], f)

        colors = ['b','darkorange','g','cyan']

        SNR = np.asarray(SNR)
        fig1, ax = plt.subplots(1,3, figsize=(12,12))
        for k, upsample in enumerate(upsamples):
            for t in range(len(ax)):
                ax[t].plot(SNR, error_astrom[:,k,t, kk], color=colors[k], label='Upsampling :'+str(upsample))
                if compare_psfr:
                    ax[t].plot(SNR, error_astrom_psfr[:, k, t, kk], color=colors[k], linestyle = '-.', label='Upsampling PSFr :'+str(upsample))
                if compare_photutils:
                    ax[t].plot(SNR, error_astrom_photutils[:, k, t, kk], color=colors[k], linestyle = ':', label='Upsampling Photutils :'+str(upsample))

                ax[t].set_xlabel('SNR')
                ax[t].set_xlabel('Error')
                ax[t].set_xscale('log')
                if not t == 1:
                    ax[t].set_yscale('log')
                ax[t].legend()
        ax[0].set_title('Statistical error')
        ax[1].set_title('Bias')
        ax[2].set_title('Total')
        plt.tight_layout()
        plt.savefig(os.path.join(outpath, 'astrometric_errors.png'), dpi =300)
        if show:
            plt.show()


        fig2, ax = plt.subplots(1,3, figsize=(12,12))
        precision_th = 1. / SNR + bkg_noise / SNR ** 2
        for k, upsample in enumerate(upsamples):
            for t in range(len(ax)):
                ax[t].plot(SNR, error_photom[:,k,t, kk],  color=colors[k], label='Upsampling :'+str(upsample))
                if compare_psfr:
                    ax[t].plot(SNR, error_photom_psfr[:, k, t, kk], color=colors[k], linestyle = '-.', label='Upsampling PSFr :'+str(upsample))
                if compare_photutils:
                    ax[t].plot(SNR, error_photom_photutils[:, k, t, kk], color=colors[k], linestyle = ':', label='Upsampling Photutils :'+str(upsample))
                if k == 0:
                    ax[t].plot(SNR, error_ap[:, t, kk], 'b--', label='aperture photometry')
                if k==0 and t == 2:
                    ax[t].plot(SNR, precision_th, 'k--', label='theory')
                ax[t].set_xlabel('SNR')
                ax[t].set_xlabel('Error')
                ax[t].set_xscale('log')
                if not t == 1 :
                    ax[t].set_yscale('log')
                ax[t].legend()
        ax[0].set_title('Statistical error')
        ax[1].set_title('Bias')
        ax[2].set_title('Total')
        plt.tight_layout()
        plt.savefig(os.path.join(outpath, 'photometric_errors.png'), dpi =300)
        if show:
            plt.show()

        plt.figure(3,figsize=(12,12))
        for k, upsample in enumerate(upsamples):
            plt.plot(SNR, error_ap[:,2, kk] / error_photom[:,k,2, kk], color=colors[k], label='Upsampling :'+str(upsample))
        plt.xscale('log')
        plt.xlabel('SNR')
        plt.ylabel('Aperture precision / PSF precision')
        plt.legend()
        plt.savefig(os.path.join(outpath, 'ratio_precision.png'), dpi =300)
        if show:
            plt.show()
        plt.close('all')


    #saving overall metrics:
    outpath_overall = os.path.join(path, inst, 'results_' + output)
    if not os.path.isdir(outpath_overall):
        os.mkdir(outpath_overall)

    with open(os.path.join(outpath_overall, 'starred_overall_astro-photo_metrics.pkl'), 'wb') as f:
        pkl.dump([error_astrom, error_photom], f)
    if compare_psfr:
        with open(os.path.join(outpath_overall, 'psfr_overall_astro-photo_metrics.pkl'), 'wb') as f:
            pkl.dump([error_astrom_psfr, error_photom_psfr], f)
    if compare_photutils:
        with open(os.path.join(outpath_overall, 'photutils_overall_astro-photo_metrics.pkl'), 'wb') as f:
            pkl.dump([error_astrom_photutils, error_photom_photutils], f)
