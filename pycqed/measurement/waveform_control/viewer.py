# module for visualizing sequences.
#
# author: Wolfgang Pfaff
# modified by: Adriaan Rol and Ramiro Sagastizabal

import numpy as np
from matplotlib import pyplot as plt


def show_element_dclab(element, delay=True, channels='all', ax=None):
    if ax is None:
        add_extra_labs = True
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    else:
        # prevents super long legends if plots are combined
        add_extra_labs = False
    axs2 = ax.twinx()
    colors_dict = {'ch1': 'red',
                   'ch1_marker1': 'orangered',
                   'ch1_marker2': 'darkred',
                   'ch2': 'gold',
                   'ch2_marker1': 'orange',
                   'ch2_marker2': 'yellow',
                   'ch3': 'green',
                   'ch3_marker1': 'lime',
                   'ch3_marker2': 'turquoise',
                   'ch4': 'darkblue',
                   'ch4_marker1': 'indigo',
                   'ch4_marker2': 'navy'}
    t_vals, outputs_dict = element.waveforms()
    t_vals = t_vals*1e9
    for key in outputs_dict:
        if 'marker' in key:
            axs2.plot(
                t_vals, outputs_dict[key], label=key, color=colors_dict[key])
        else:
            ax.plot(
                t_vals, outputs_dict[key], label=key, color=colors_dict[key])
    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Analog output (V)')
    if add_extra_labs:  # only set it once otherwise we end up with 20 labels
        axs2.set_ylabel('Marker output (V)')

    hi = element._channels['ch1']['high']
    lo = element._channels['ch1']['low']
    ax.set_ylim(lo-0.1*(hi-lo), hi+0.1*(hi-lo))
    hi = element._channels['ch1_marker1']['high']
    lo = element._channels['ch1_marker1']['low']
    axs2.set_ylim(lo-0.1*(hi-lo), hi+0.1*(hi-lo))

    ax.set_xlim(t_vals.min(), t_vals.max())
    if add_extra_labs:
        ax.legend(loc='best')
    return ax


def show_wf(tvals, wf, name='', ax=None, ret=None, dt=None):

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    if dt is None:
        dt = tvals[1]-tvals[0]
    ax.plot(tvals, wf, ls='-', marker='.')

    ax.set_xlim(tvals[0], 2*tvals[-1]-tvals[-2])
    ax.set_ylabel(name + ' Amplitude')

    if ret == 'ax':
        return ax
    else:
        return None


def show_element(element, delay=True, channels='all'):
    tvals, wfs = element.waveforms()
    if channels == 'all':
        cnt = len(wfs)
    else:
        cnt = len(channels)
    i = 0

    fig, axs = plt.subplots(cnt, 1, sharex=True)
    t0 = 0
    t1 = 0

    for wf in wfs:
        if channels == 'all' or wf in channels:
            i += 1
            hi = element._channels[wf]['high']
            lo = element._channels[wf]['low']
            # some prettifying
            ax = axs[i-1]
            ax.set_axis_bgcolor('gray')
            ax.axhspan(lo, hi, facecolor='w', linewidth=0)
            # the waveform
            if delay:
                t = tvals
            else:
                t = element.real_times(tvals, wf)

            t0 = min(t0, t[0])
            t1 = max(t1, t[-1])
            # TODO style options
            show_wf(t, wfs[wf], name=wf, ax=ax, dt=1./element.clock)

            ax.set_ylim(lo*1.1, hi*1.1)

            if i == cnt:
                ax.set_xlabel('Time')
                ax.set_xlim(t0, t1)


def show_fourier_of_element_channels(element, channels, units='Hz'):
    '''
    Shows a fourier transform of a waveform.
    element : from which a waveform needs to be displayed
    channels (str): names of the channels on which the waveform is defined
                    in time domain. If the lenght of the channels is 2 it
                    interprets the first as being the I quadrature and the
                    second as the q quadrature.
    '''
    tvals, wfs = element.waveforms()
    fig, ax = plt.subplots(1, 1)
    dt = tvals[1]-tvals[0]

    if len(channels) == 2:
        compl_data = wfs[channels[0]] + 1j * wfs[channels[1]]
        trans_dat = np.fft.fft(compl_data)*dt
        n = len(compl_data)
    elif len(channels) == 1:
        trans_dat = np.fft.fft(wfs[channels[0]])*dt
        n = len(wfs[channels[0]])
    else:
        trans_dat = np.fft.fft(wfs[channels])*dt
        n = len(wfs[channels])

    freqs = np.fft.fftfreq(n, d=dt)

    if units == 'MHz':
        freqs *= 1e-6
    elif units == 'GHz':
        freqs *= 1e-9
    elif units == 'Hz':
        pass
    else:
        raise Exception('units "%s" not recognized, valid options' +
                        ' are GHz, MHz and Hz')
    ax.plot(freqs, trans_dat, ls='-o', marker='.')
    ax.set_xlabel('Frequency (%s)' % units)
