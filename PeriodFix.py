import numpy as np
import matplotlib.pyplot as plt

def Compare(filename,vertical_shift,start_frequency): #filename needs to be in strings
    """Given a data file, this function plots a graph"""

    plot = np.loadtxt(filename + ".dat")
    frequency = plot[:,1]
    photocurrent = plot[:,2] + vertical_shift
    maximum_point = np.amax(plot[1:,0])
    # start = 0
    # period = period
    # end = period
    c = 3*10**8
    L_ref = (1.0*c)/start_frequency # path difference stays as constant

    photocurrent_list = []
    frequency_list = []
    envelope_photocurrent_list = []
    envelope_frequency_list = []
    log_envelope_photocurrent_list = []

    for value in photocurrent: #converts array to list [for now]
        photocurrent_list.append(value)

    for value in frequency:
        frequency_list.append(value)

    while start < maximum_point-period and end < maximum_point:
        # for plot #
        shortened_photocurrent_list = photocurrent_list[start:end]
        shortened_frequency_list = frequency_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
        max_photocurrent = np.amax(photocurrent[start:end]) #picks out maximum value of photocurrent in one period
        envelope_photocurrent_list.append(max_photocurrent) #puts maximum photocurrent in list
        index = shortened_photocurrent_list.index(max_photocurrent) # gets the index corresponding to the selected photocurrent
        envelope_frequency_list.append(shortened_frequency_list[index])

        start += period
        end += period

    for value in envelope_photocurrent_list:
        new_value = 20*np.log10(value)
        log_envelope_photocurrent_list.append(new_value)

    return (envelope_frequency_list,log_envelope_photocurrent_list,frequency_list,photocurrent_list)
#


plt.figure()
plt.xlabel('Frequency $GHz$')
plt.ylabel('Photocurrent $nA$')
plt.plot(Compare("water",0.6)[0], Compare("water",0.6)[1], label = 'Water Run 1 Without Average', color = 'b')
plt.show()
