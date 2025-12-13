import numpy as np
import os 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pandas import read_csv

def generate_SNIa_lcs(nepochs=20, sn_template='/Users/martin/Desktop/modules/piscola/data/03D1au.dat', dt_sampling=10, blanck_epoch=5,
                      output_file = './test_SNIa/interpolated_03D1au.txt', redo_SNIa_lcs=True):

    if redo_SNIa_lcs: 
        import piscola
        sn = piscola.call_sn(sn_template)
        sn.fit()

        t0 = sn.lc_fits.Megacam_r.time[200]
        time_array = np.arange(int(t0), t0 + nepochs * dt_sampling - 1 , dt_sampling)
        lcs_mag = np.interp(time_array, sn.lc_fits.Megacam_r.time, sn.lc_fits.Megacam_r.mag)
        lcs = np.nan_to_num(lcs_mag, nan=35.)
        lcs = np.append(np.ones(blanck_epoch)*35, lcs)
        time_array = np.append(np.linspace(t0 - blanck_epoch*dt_sampling, t0, blanck_epoch), time_array)
        np.savetxt(output_file, [lcs, time_array])

    else: 
        lcs, time_array = np.loadtxt(output_file)
        t0 = 52881.54
    
    return lcs, time_array, t0

def generate_QSO_lcs(nepochs, mag=21, constant=True, dt_sampling=1, lcs_source=None):
    time_array = np.linspace(0, nepochs*dt_sampling - dt_sampling, nepochs)
    if constant is True: 
        lcs =  np.ones(nepochs) * mag
    else :
        data=read_csv(lcs_source)
        lcs=np.asarray(data['mag_A'].values + 30.) #rough ZP correction
        jds = np.asarray(data['mhjd'].values)

        lcs = lcs[660:] #we start from the Euler season 
        lcs += (mag - np.mean(lcs)) #renormalise the mag
        jds = jds[660:]
        jds = jds - jds[0]
        lcs = np.interp(time_array, jds, lcs)
    return lcs, time_array


def kwargs_lensed_quasars(i, j, sim_r, shift_vecx, shift_vecy, thetaE, lcs, extended_source=False, realistic=False,
                          image=None, image_source=None, scale_factor=2):
    """
    param i: exposure index
    param j: epoch index

    """
    if realistic: 
        kwargs_lens_light_mag_r = [
            {'magnitude': 17, 'image': image, 'scale': 0.06*scale_factor, 'phi_G': 0, 'center_x': 0.+ shift_vecx[i], 
                                'center_y': 0 + shift_vecy[i]}]
    else: 
        kwargs_lens_light_mag_r = [
            {'magnitude': 17, 'R_sersic': 3.0, 'n_sersic': 2., 'e1': 0.1, 'e2': -0.1, 'center_x': 0 + shift_vecx[i],
            'center_y': 0 + shift_vecy[i]}]
    
    kwargs_source_mag_r = []
    if extended_source:
        if realistic:
            kwargs_source_mag_r = [
            {'magnitude': 19, 'image': image_source, 'scale': 0.06*scale_factor, 'phi_G': 0, 'center_x': 0.+ shift_vecx[i], 
                                'center_y': 0 + shift_vecy[i]}]
        else: 
            kwargs_source_mag_r.append(
                {'magnitude': 18, 'R_sersic': 2.0, 'n_sersic': 1., 'e1': -0.3, 'e2': -0.2, 'center_x': 0 + shift_vecx[i],
                'center_y': 0 + shift_vecy[i]})
        kwargs_ps_mag_r = [{'magnitude': lcs[j], 'ra_source': 0.03 + shift_vecx[i], 'dec_source': 0 + shift_vecy[i]}]
    kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r = sim_r.magnitude2amplitude(kwargs_lens_light_mag_r,
                                                                                  kwargs_source_mag_r, kwargs_ps_mag_r)

    kwargs_lens = [
        {'theta_E': thetaE, 'e1': 0.4, 'e2': -0.1, 'center_x': 0 + shift_vecx[i], 'center_y': 0 + shift_vecy[i]},
        # SIE model
        {'gamma1': 0.03, 'gamma2': 0.01, 'ra_0': 0 + shift_vecx[i], 'dec_0': 0 + shift_vecy[i]}  # SHEAR model
    ]

    return kwargs_lens, kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r

def kwargs_SNIa(i,j, sim_r, shift_vecx, shift_vecy, d, lcs, no_host=False):
    """
    param i: exposure index
    param j: epoch index
    
    """
    
    if no_host: 
        kwargs_lens_light_mag_r = []
    else: 
        kwargs_lens_light_mag_r = [
            {'magnitude': 16, 'R_sersic': 4.0, 'n_sersic': 2., 'e1': 0.1, 'e2': -0.1, 'center_x': 0 + shift_vecx[i],
            'center_y': 0 + shift_vecy[i]}]
    kwargs_source_mag_r = []
    kwargs_ps_mag_r = [{'magnitude': [lcs[j]], 'ra_image': [d + shift_vecx[i]], 'dec_image':[d + shift_vecy[i]]}]
    kwargs_lens = []
    kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r = sim_r.magnitude2amplitude(kwargs_lens_light_mag_r,
                                                                                  kwargs_source_mag_r, kwargs_ps_mag_r)
    return kwargs_lens, kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r

def kwargs_SNIa_realistic(i,j, sim_r, shift_vecx, shift_vecy, d, lcs, image, scale_factor=2):
    """
    param i: exposure index
    param j: epoch index
    
    """
        
    kwargs_lens_light_mag_r = [{'magnitude': 16, 'image': image, 'scale': 0.06*scale_factor, 'phi_G': 0, 'center_x': 0.+ shift_vecx[i], 
                                'center_y': 0 + shift_vecy[i]}]
    kwargs_source_mag_r = []
    kwargs_ps_mag_r = [{'magnitude': [lcs[j]], 'ra_image': [d + shift_vecx[i]], 'dec_image':[d + shift_vecy[i]]}]
    kwargs_lens = []
    kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r = sim_r.magnitude2amplitude(kwargs_lens_light_mag_r,
                                                                                  kwargs_source_mag_r, kwargs_ps_mag_r)
    return kwargs_lens, kwargs_lens_light_r, kwargs_source_r, kwargs_ps_r

def read_seeing_file(seeing_file): 
    with open(seeing_file) as f:
        lines = f.readlines()

    names = []
    seeing = [] 
    goodstars = [] 
    skylevel = []
    for line in lines[6:]:
        data = line.split('|')
        names.append(data[0].replace(" ", ""))
        skylevel.append(float(data[1]))
        seeing.append(float(data[3]))
        goodstars.append(float(data[4]))

    return names, seeing, goodstars, skylevel

def pick_psfs(psfs_list, names, seeing, goodstar, skylevel, psfcuts = [1.0, 200, 1000], n=10, seed = None): 
    new_psf_list = []
    new_names = [] 
    new_seeing = []
    new_goostar = [] 
    new_skylevel = [] 

    if seed is not None: 
        np.random.seed(seed)
        np.random.shuffle(psfs_list)

    for i, psf in enumerate(psfs_list): 
        basename = os.path.basename(psf)
        psf_name = basename.split('_psf.fits')[0]
        ind = np.where(np.asarray(names) == psf_name)[0]
        if len(ind) == 1: 
            j = ind[0]
            if seeing[j] < psfcuts[0] and goodstar[j]>psfcuts[1] and skylevel[j]<psfcuts[2]: 
                new_psf_list.append(psf)
                new_names.append(names[j])
                new_goostar.append(goodstar[j])
                new_skylevel.append(skylevel[j])
                new_seeing.append(seeing[j])
                print('Including :', psf)

            if len(new_psf_list) == n:
                break
    
    return new_psf_list, new_names, new_seeing, new_goostar, new_skylevel


def plt_lcs(t, lclist, truth_list, error_list, color_list = ['royalblue', 'darkorange', 'lightgreen', 'magenta'], labels_list = ['A', 'B', 'C', 'D'],
            M=1, ylim = [18.5,22], detection_epoch = 0, ms =6): 
    """
    
    :param t: Time array, corresponding to the observation.
    :param lclist: list of light curves, must have dimension (Nepoch, M)
    :param truth_list: list of true light curve, must have dimension (Nepoch, M)
    :param error_list: list of error bars, must have dimension (Nepoch, M)
    :param M: Number of point source
    """

    residuals = lclist - truth_list
    truth_epoch = max(0, detection_epoch - 2)

    fig = plt.figure(figsize=(12,5+2*M))
    gs1 = gridspec.GridSpec(5+2*M, 2)
    gs1.update(left=0.08, right=0.96, top=0.98, bottom=0.1, wspace=0.05, hspace=0.09)
    ax = [plt.subplot(gs1[0:5, :])]
    for k in range(M):
        ax.append(plt.subplot(gs1[5+2*k:5+2*k+2, :],sharex=ax[0]))

    for k in range(M): 
        ax[0].errorbar(t[detection_epoch:], lclist[detection_epoch:, k], yerr=error_list[detection_epoch:, k], marker='o', 
                       c=color_list[k], linestyle='None', label='STARRED photometry source %s'%labels_list[k], markerfacecolor = color_list[k], ms = ms  )
        ax[0].plot(t[truth_epoch:], truth_list[truth_epoch:,k], label = 'Truth %s'%labels_list[k], color=color_list[k], linestyle=':')
        
    ax[0].set_ylabel('Magnitude')
    ax[0].set_ylim(ylim)
    ax[0].xaxis.set_tick_params(which='both', labelbottom=False)
    ax[0].invert_yaxis()
    ax[0].legend(fontsize = 14)

    #residuals plot
    for k in range(M): 
        ax[k+1].errorbar(t[detection_epoch:], residuals[detection_epoch:, k], yerr=error_list[detection_epoch:, k], marker='None', c=color_list[k], label=labels_list[k], linestyle = 'none')
        ax[k+1].errorbar(t[detection_epoch:], residuals[detection_epoch:, k], marker='o', label=labels_list[k], markerfacecolor = color_list[k], ms = ms, linestyle = 'none', mec = color_list[k])

        ax[k+1].invert_yaxis()
        ax[k+1].set_ylabel('Residuals [mag]')
        ax[k+1].hlines(0, t[truth_epoch] - 0.5, t[-1] + 0.5, colors='k', linestyles='--')

    ax[-1].set_xlabel('Epoch')

    return fig 
    