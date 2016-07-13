import numpy as np
import matplotlib.pyplot as plt

def Compare(filename,vertical_shift): #filename needs to be in strings
    """Given a data file, this function plots a graph"""

    plot = np.loadtxt(filename + ".dat")
    frequency = plot[:,1]
    photocurrent = plot[:,2] + vertical_shift
    maximum_point = np.amax(plot[1:,0])

    photocurrent_list = []
    frequency_list = []
    index_list = []
    period_list = [0] #start with zero as first entry, introduce it as the starting point of the measurement
    envelope_photocurrent_list = []
    envelope_frequency_list = []
    log_envelope_photocurrent_list = []

    index = 0
    j = 0
    k = 0

    for value in photocurrent: #converts array to list [for now]
        photocurrent_list.append(value)

    for value in frequency:
        frequency_list.append(value)
    # print 'length of frequency is', len(frequency_list)
    # print 'first ten frequencies', frequency_list[0:9]

    while index < len(frequency_list)-1: # length of frequency_list is 48334
    # for index in range(0,frequency_list[-1]+1):
        if photocurrent_list[index] > 0 and photocurrent_list[index+1] < 0:
            # acquire_index = frequency_list.index(frequency_list[index])
            index_list.append(index)
        index +=1

    print 'length of index is', len(index_list)

    # while j < len(index_list)-1:
    #     acquire_period = index_list[j+1] - index_list[j]
    #     period_list.append(acquire_period)
    #     j += 1
    # print 'length of period list', len(period_list)
    print 'example index', index_list[0:15]
    print 'example period', period_list[0:15]

    while k < len(index_list)-1:
        start = index_list[k]
        end = index_list[k+1]
        shortened_photocurrent_list = photocurrent_list[start:end]
        shortened_frequency_list = frequency_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
        max_photocurrent = np.amax(photocurrent[start:end]) #picks out maximum value of photocurrent in one period
        envelope_photocurrent_list.append(max_photocurrent) #puts maximum photocurrent in list
        photocurrent_index = shortened_photocurrent_list.index(max_photocurrent) # gets the index corresponding to the selected photocurrent
        envelope_frequency_list.append(shortened_frequency_list[photocurrent_index])

        k += 1

    print 'new frequency', len(envelope_frequency_list)
    print 'envelope', len(envelope_photocurrent_list)

    # while start < maximum_point-period and end < maximum_point:

    #     # for plot #
    #     shortened_photocurrent_list = photocurrent_list[start:end]
    #     shortened_frequency_list = frequency_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
    #     max_photocurrent = np.amax(photocurrent[start:end]) #picks out maximum value of photocurrent in one period
    #     envelope_photocurrent_list.append(max_photocurrent) #puts maximum photocurrent in list
    #     index = shortened_photocurrent_list.index(max_photocurrent) # gets the index corresponding to the selected photocurrent
    #     envelope_frequency_list.append(shortened_frequency_list[index])
    #
    #     start += period
    #     end += period

    for value in envelope_photocurrent_list:
        new_value = 20*np.log10(value)
        log_envelope_photocurrent_list.append(new_value)
    return (envelope_frequency_list,log_envelope_photocurrent_list,frequency_list,photocurrent_list)
#



plt.figure()
plt.grid()
plt.xlabel('Frequency $GHz$')
plt.ylabel('Photocurrent $nA$')
plt.plot(Compare("water",0.5)[0], Compare("water",0.5)[1], label = 'Water Run 1 Without Average', color = 'b')
# plt.scatter(Compare("water",0.6)[2], Compare("water",0.6)[3], label = 'Water Run 1 Without Average', color = 'b')
plt.show()
