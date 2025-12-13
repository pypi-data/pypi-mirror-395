import os
import astropy.io.fits as fits
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
import check_utils as cu
from starred.utils.generic_utils import Downsample, Upsample, save_fits
import scipy

SNR = [100,1000,10000,100000]
# SNR = [ 100000, 300000]
# SNR = [10000]
# instrument = ['HST-F814W']
instrument = ['WFI_odd']
upsamples = [1,2]
# upsamples = [2]
path = './mock_stars_shift05_oddkernel_multiple'
output = 'output_MC' #output, output_noreg, output_fullreg
# psfr_folder = 'psfr_output'
psf_photutils_folder = 'photutils_output'
psfr_folder = 'psfr_output_with_noise_maps'
bkg_noise = 10
plot = False
compare_psf = True
compare_photutils = True
verbose = True
exlcude_photutils_SNR100=True
seeds = np.arange(10)

for inst in instrument:
    psf_max_error_rel = np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # max error upsampled PSF, downsampled PSF
    psf_median_error_inner = np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # median RMS error upsampled PSF, downsampled PSF, on the inner 10 pixels
    psf_median_error = np.zeros((len(SNR), len(upsamples), 2, len(seeds))) # median RMS error upsampled PSF, downsampled PSF, full PSF

    psf_max_error_rel_psfr = np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # max error upsampled PSF, downsampled PSF
    psf_median_error_inner_psfr= np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # median RMS error upsampled PSF, downsampled PSF, on the inner 10 pixels
    psf_median_error_psfr = np.zeros((len(SNR), len(upsamples), 2, len(seeds))) # median RMS error upsampled PSF, downsampled PSF, full PSF

    psf_max_error_rel_psfphot = np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # max error upsampled PSF, downsampled PSF
    psf_median_error_inner_psfphot= np.zeros((len(SNR), len(upsamples), 2, len(seeds)))  # median RMS error upsampled PSF, downsampled PSF, on the inner 10 pixels
    psf_median_error_psfphot = np.zeros((len(SNR), len(upsamples), 2, len(seeds))) # median RMS error upsampled PSF, downsampled PSF, full PSF

    for kk,seed in enumerate(seeds):
        for ii,SN in enumerate(SNR):
            folder = os.path.join(path, inst,'seed_%i'%seed, 'SNR_%i' % SN)
            aperture_photometry = cu.get_aperture_photometry(folder)

            for jj,upsample in enumerate(upsamples):
                if inst == 'tinytim10':
                    true_PSF_path = './PSF/psf_tinytim_size59_upsampling%i.fits' % upsample
                    with open(true_PSF_path, 'rb') as f:
                        true_PSF = fits.open(f)[0].data
                    true_PSF = true_PSF + 1e-10 * np.random.normal(size=np.shape(true_PSF))

                elif inst == 'WFI_odd':
                    true_PSF_path = './PSF/psf_WFI_odd_size63_upsampling%i.fits' % upsample
                    with open(true_PSF_path, 'rb') as f:
                        true_PSF = fits.open(f)[0].data

                elif inst == 'HST-F814W' or inst == 'HST-F475W':
                    raise NotImplementedError()

                elif inst == 'Gaussian':
                    if 'oddkernel' in path:
                        true_PSF_path = './PSF/psf_Gaussian_size63_upsampling%i.fits'%upsample
                        with open(true_PSF_path, 'rb') as f:
                            true_PSF = fits.open(f)[0].data
                        # very small value are problematic, add some uncertainty floor
                        true_PSF = true_PSF + 1e-10 * np.random.normal(size=np.shape(true_PSF))
                else :
                    raise NotImplementedError()

                true_psf_size = np.shape(true_PSF)[0]
                print('### ', inst, 'seed %i'%seed, 'SNR : ', SN, 'upsampling :', upsample,'###')
                model_pkl = os.path.join(path,inst,'seed_%i'%seed, 'SNR_%i'%SN, output+'_%i'%upsample, 'model.pkl')
                pkl_true = os.path.join(path,inst, 'seed_%i'%seed, 'SNR_%i'%SN,'flux_mag.pkl')

                outpath = os.path.join(path, inst, 'seed_%i'%seed, 'results_'+output)
                psfr_path = os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i' % SN, psfr_folder, 'psfr_upsampling%i.fits'%upsample)
                psf_photutils_path = os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i' % SN, psf_photutils_folder, 'photutils_upsampling%i.fits'%upsample)
                psfr_center_path = os.path.join(path, inst, 'seed_%i'%seed, 'SNR_%i' % SN, psfr_folder, 'center_list_upsampling%i.txt'%upsample)

                if not os.path.exists(outpath):
                    os.mkdir(outpath)

                try :
                    with open(model_pkl, 'rb') as f:
                        model, kwargs_final, norm = pkl.load(f)
                    if not hasattr(model, 'shift_direction'):
                        model.shift_direction = 1.
                except FileNotFoundError as e:
                    print(e)
                    continue

                print('PSF sizes (true, upsampled) : ', true_psf_size, model.image_size_up)
                assert true_psf_size == model.image_size_up
                true_PSF_downsample = Downsample(true_PSF, factor=int(true_psf_size / model.image_size))

                psf_median_error[ii, jj,:,kk], psf_max_error_rel[ii, jj,:,kk],psf_median_error_inner[ii, jj,:,kk], psf_starred, residuals_starred = cu.check_psf_fidelity(model, kwargs_final,
                                                                                                                           true_PSF_downsample, true_PSF,
                                                                                                                           N_intern = 10, verbose = True)

                save_fits(residuals_starred[0], os.path.join(outpath, 'residuals_starred_upsample%i_SNR%i'%(upsample, SN)))
                save_fits(residuals_starred[1], os.path.join(outpath, 'residuals_starred_downsample%i_SNR%i'%(upsample,SN)))
                save_fits(true_PSF, os.path.join(outpath, 'true_PSF_upsample%i'%(upsample)))
                save_fits(true_PSF_downsample, os.path.join(outpath, 'true_PSF_upsample%i'%(upsample)))
                figpstarred = cu.plot_residuals(residuals_starred, psf_starred, show=False)
                figpstarred.savefig(os.path.join(outpath, 'residuals_starred_upsample%i_SNR%i.png' % (upsample, SN)))

                with open(os.path.join(outpath, 'starred_psf_metrics.pkl'), 'wb') as f:
                    pkl.dump([psf_median_error[:,:,:,kk], psf_max_error_rel[:,:,:,kk], psf_median_error_inner[:,:,:,kk]], f)

                # comparison with psfr
                if compare_psf:
                    print('--- PSFr ---')
                    psfr_up = np.zeros((model.image_size_up, model.image_size_up))
                    try :
                        if upsample %2 == 1:
                            psfr_up = fits.open(psfr_path)[0].data
                        elif upsample == 2 :
                            psfr_up[1::, 1::] = fits.open(psfr_path)[0].data  # pad PSFr, identical, because this row of pixel is beiing removed when rebinning
                            print('Warning interpolating PSFr PSF by half a pixel to match the convention')
                            psfr_up = scipy.ndimage.shift(psfr_up, (-0.5, -0.5), output=None, order=1, mode='nearest')

                        print('PSFr size, true size: ', np.shape(psfr_up), np.shape(true_PSF))
                    except FileNotFoundError :
                        print('NO PSFr reconstruction found.')
                        psf_median_error_psfr[ii, jj,:,kk], psf_max_error_rel_psfr[ii, jj,:,kk], psf_median_error_inner_psfr[ii, jj,:,kk] = np.nan, np.nan, np.nan
                    else :
                        psfr_down = Downsample(psfr_up, factor=upsample)
                        psf_median_error_psfr[ii, jj,:,kk], psf_max_error_rel_psfr[ii, jj,:,kk], psf_median_error_inner_psfr[
                            ii, jj, :,kk], _ , residuals_psfr = cu.check_psf_fidelity([psfr_up,psfr_down], kwargs_final,
                                                                                            true_PSF_downsample,
                                                                                            true_PSF,
                                                                                            N_intern=10, verbose=True)

                        save_fits(residuals_psfr[0], os.path.join(outpath, 'residuals_psfr_upsample%i_SNR%i'%(upsample,SN)))
                        save_fits(residuals_psfr[1], os.path.join(outpath, 'residuals_psfr_downsample%i_SNR%i'%(upsample,SN)))
                        figpsfr = cu.plot_residuals(residuals_starred, psf_starred, residuals_psfr, psfr_up, psfr_down,data_set='PSFr', show=False)
                        figpsfr.savefig(os.path.join(outpath, 'residuals_psfr_starred_upsample%i_SNR%i.png' % (upsample, SN)))

                        with open(os.path.join(outpath, 'psfr_psf_metrics.pkl'), 'wb') as f:
                            pkl.dump([psf_median_error_psfr[:,:,:,kk], psf_max_error_rel_psfr[:,:,:,kk], psf_median_error_inner_psfr[:,:,:,kk]], f)

                if compare_photutils:
                    #comparison with photutils:
                    if exlcude_photutils_SNR100 and SN == 100 :
                        psf_median_error_psfphot[ii, jj,:,kk], psf_max_error_rel_psfphot[ii, jj,:,kk], psf_median_error_inner_psfphot[
                            ii, jj,:,kk] = np.nan, np.nan, np.nan
                        continue
                    print('--- Photutils ---')
                    try :
                        if upsample == 1:
                            psf_photutils_up = fits.open(psf_photutils_path)[0].data[1:-1,1:-1]
                        elif upsample == 2 :
                            psf_photutils_up = fits.open(psf_photutils_path)[0].data[1::,1::]
                            print('Warning interpolating Photutils PSF by half a pixel to match the convention')
                            psf_photutils_up = scipy.ndimage.shift(psf_photutils_up, (0.5, 0.5), output=None, order=1, mode='nearest')
                        elif upsample == 3 :
                            psf_photutils_up = fits.open(psf_photutils_path)[0].data[1:-1, 1:-1]
                    except FileNotFoundError:
                        print('No Photutils reconstruction found.')
                        psf_median_error_psfphot[ii, jj,:,kk], psf_max_error_rel_psfphot[ii, jj,:,kk], psf_median_error_inner_psfphot[
                            ii, jj,:,kk] = np.nan, np.nan, np.nan
                    else :
                        print('Photutils size, true size: ', np.shape(psf_photutils_up), np.shape(true_PSF))
                        psf_photutils_down = Downsample(psf_photutils_up, factor=upsample)
                        psf_median_error_psfphot[ii, jj,:,kk], psf_max_error_rel_psfphot[ii, jj,:,kk], psf_median_error_inner_psfphot[
                            ii, jj,:,kk], _, residuals_psfphot = cu.check_psf_fidelity([psf_photutils_up, psf_photutils_down], kwargs_final,
                                                                               true_PSF_downsample,
                                                                               true_PSF,
                                                                               N_intern=10, verbose=True)

                        save_fits(residuals_psfphot[0], os.path.join(outpath, 'residuals_psfphot_upsample%i_SNR%i' % (upsample, SN)))
                        save_fits(residuals_psfphot[1],
                                  os.path.join(outpath, 'residuals_psfphot_downsample%i_SNR%i' % (upsample, SN)))

                        #plot residuals
                        figphot = cu.plot_residuals(residuals_starred, psf_starred, residuals_psfphot, psf_photutils_up, psf_photutils_down, data_set = 'Photutils', show= False)
                        figphot.savefig(os.path.join(outpath, 'residuals_photutils_starred_upsample%i_SNR%i.png'%(upsample,SN)))

                        with open(os.path.join(outpath, 'photutils_psf_metrics.pkl'), 'wb') as f:
                            pkl.dump([psf_median_error_psfphot[:,:,:,kk], psf_max_error_rel_psfphot[:,:,:,kk], psf_median_error_inner_psfphot[:,:,:,kk]], f)


        #Plotting figures
        colors = ['b','darkorange','g','cyan']
        for up in range(2):
            fig3, axs = plt.subplots(1,3, figsize=(15,10))
            axs[0].set_xlabel('SNR')
            axs[1].set_xlabel('SNR')
            axs[2].set_xlabel('SNR')
            axs[0].set_ylabel('Error')
            axs[0].set_title('PSF MAE error')
            axs[1].set_title('PSF MAE error (inner region)')
            axs[2].set_title('Max PSF error / max(PSF)')
            for aa in range(3):
                axs[aa].set_xscale('log')
                axs[aa].set_yscale('log')

            for k, upsample in enumerate(upsamples):
                axs[0].plot(SNR, psf_median_error[:, k, up,kk], color=colors[k], label='Upsampling :'+str(upsample))
                if compare_psf:
                    axs[0].plot(SNR, psf_median_error_psfr[:, k, up,kk], color=colors[k], linestyle='-.',label='Upsampling PSFr:' + str(upsample))
                if compare_photutils:
                    axs[0].plot(SNR, psf_median_error_psfphot[:, k, up,kk], color=colors[k], linestyle=':',label='Upsampling PSF photutils:' + str(upsample))
            for k, upsample in enumerate(upsamples):
                axs[1].plot(SNR, psf_median_error_inner[:, k, up,kk], color=colors[k], label='Upsampling :'+str(upsample))
                if compare_psf:
                    axs[1].plot(SNR, psf_median_error_inner_psfr[:, k, up,kk], color=colors[k], linestyle='-.',label='Upsampling PSFr:' + str(upsample))
                if compare_photutils:
                    axs[1].plot(SNR, psf_median_error_inner_psfphot[:, k, up,kk], color=colors[k], linestyle=':',label='Upsampling PSF photutils :' + str(upsample))
            for k, upsample in enumerate(upsamples):
                axs[2].plot(SNR, psf_max_error_rel[:,k,up,kk], color=colors[k], label='Upsampling :'+str(upsample))
                if compare_psf:
                    axs[2].plot(SNR, psf_max_error_rel_psfr[:, k, up,kk], color=colors[k], linestyle='-.',label='Upsampling PSFr:' + str(upsample))
                if compare_photutils:
                    axs[2].plot(SNR, psf_max_error_rel_psfphot[:, k, up,kk], color=colors[k], linestyle=':',label='Upsampling PSF photutils :' + str(upsample))

            plt.legend()
            if up == 0 :
                fig3.savefig(os.path.join(outpath, 'PSF_error_upsample.png'))
            else :
                fig3.savefig(os.path.join(outpath, 'PSF_error_downsample.png'))

        if compare_psf or compare_photutils:
            for up in range(2):
                fig5, axs = plt.subplots(1,2, figsize=(12,10))
                axs[0].set_xlabel('SNR')
                axs[1].set_xlabel('SNR')
                axs[0].set_ylabel('Error Ratio')
                axs[0].set_title('PSF MAE error')
                axs[1].set_title('PSF MAE error (inner region)')
                for aa in range(2):
                    axs[aa].set_xscale('log')
                    axs[aa].plot(SNR, 1 * np.ones_like(SNR), 'k--')

                for k, upsample in enumerate(upsamples):
                    if compare_psf:
                        axs[0].plot(SNR, psf_median_error_psfr[:, k, up, kk]/ psf_median_error[:,k,up, kk], color=colors[k], linestyle='-.',
                                    label='Upsampling PSFr/STARRED:' + str(upsample))
                    if compare_photutils:
                        axs[0].plot(SNR, psf_median_error_psfphot[:, k, up, kk]/ psf_median_error[:,k,up, kk], color=colors[k], linestyle=':',
                                    label='Upsampling PSF photutils/STARRED :' + str(upsample))
                for k, upsample in enumerate(upsamples):
                    if compare_psf:
                        axs[1].plot(SNR, psf_median_error_inner_psfr[:, k, up, kk] / psf_median_error_inner[:,k,up, kk], color=colors[k], linestyle='-.',
                                    label='Upsampling PSFr/STARRED:' + str(upsample))
                    if compare_photutils:
                        axs[1].plot(SNR, psf_median_error_inner_psfphot[:, k, up, kk]/ psf_median_error_inner[:,k,up, kk], color=colors[k], linestyle=':',
                                    label='Upsampling PSF photutils/STARRED :' + str(upsample))
                plt.legend()
                if up == 0:
                    fig5.savefig(os.path.join(outpath, 'PSF_error_ratio_upsample.png'))
                else:
                    fig5.savefig(os.path.join(outpath, 'PSF_error_ratio_downsample.png'))


    #saving overall metric:
    outpath_overall = os.path.join(path, inst, 'results_' + output)
    if not os.path.isdir(outpath_overall):
        os.mkdir(outpath_overall)
    with open(os.path.join(outpath_overall, 'starred_overall_psf_metrics.pkl'), 'wb') as f:
        pkl.dump([psf_median_error, psf_max_error_rel, psf_median_error_inner],f)

    if compare_psf:
        with open(os.path.join(outpath_overall, 'psfr_overall_psf_metrics.pkl'), 'wb') as f:
            pkl.dump([psf_median_error_psfr, psf_max_error_rel_psfr,
                      psf_median_error_inner_psfr], f)
    if compare_photutils:
        with open(os.path.join(outpath_overall, 'photutils_overall_psf_metrics.pkl'), 'wb') as f:
            pkl.dump([psf_median_error_psfphot, psf_max_error_rel_psfphot,
                      psf_median_error_inner_psfphot], f)





