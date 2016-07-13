import numpy as np
import matplotlib.pyplot as plt

def Compare(filename): #filename needs to be in strings
    """Given a data file, this function plots a graph"""

    plot = np.loadtxt(filename + ".dat")
    frequency = plot[:,1]
    photocurrent = plot[:,2]
    maximum_point = np.amax(plot[1:,0])

    #
    for value in photocurrent:
        SUM = 0
        SUM += value
        # average = average*1.0/len(photocurrent)
    print 'sum', SUM

    if SUM > 0:
        photocurrent = photocurrent + SUM
    elif SUM < 0:
        photocurrent = photocurrent - SUM

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

    # print 'length of index is', len(index_list)

    # while j < len(index_list)-1:
    #     acquire_period = index_list[j+1] - index_list[j]
    #     period_list.append(acquire_period)
    #     j += 1
    # print 'length of period list', len(period_list)
    # print 'example index', index_list[0:15]
    # print 'example period', period_list[0:15]

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

    # print 'new frequency', len(envelope_frequency_list)
    # print 'envelope', len(envelope_photocurrent_list)

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
def Noise_Reduction(data_set, nearest_neighbours):
    """Improves the quality of the data by reducing the noise of a graph. Takes the average from the nearest neighbours of each data point."""
    noisy_data = data_set
    improved_data = []
    start_index = nearest_neighbours


    for index in range(0,nearest_neighbours): #fill in improved_data list with the first 'unused' points first (from 0th data point to (start_index-1)th data point)
        improved_data.append(noisy_data[index])

    liszt = []


    while start_index < len(noisy_data) - nearest_neighbours:#while start_index < 11,  maximum is thus 11 in this case
        i = -(nearest_neighbours) #left most neighbour
        while i < nearest_neighbours+1: #maximum value of i is equal to right most value
            liszt.append(noisy_data[(start_index)+i])
            i +=1

    # for i in range(-(nearest_neighbours),(nearest_neighbours)): #for loop is awkward, fix here
    #     liszt.append(start_index+i)
        # for points in noisy_data[(start_index)+i]:
        #     liszt.append(points)
        # print 'current list is:',liszt

        total = sum(liszt)
        average_point = (1.*total)/((nearest_neighbours*2)+1) # the 1. is there to convert fractions into accurate decimal points
        improved_data.append(average_point)
        liszt[:] = [] #empties the list to be re-used again

        start_index += 1


    for index in range(len(noisy_data)-nearest_neighbours,len(noisy_data)): #fill in final few points into improved data
        improved_data.append(noisy_data[index])

    return improved_data




# plt.figure()
plt.grid(True)
plt.title('Graph of Envelope Photocurrent $nA$ vs Frequency $GHz$')
plt.xlabel('Frequency $GHz$')
plt.ylabel('Photocurrent $nA$')
plt.plot(Compare("water")[0], Compare("water")[1], label = 'Water Run 1 Without Average', color = 'b')
# plt.scatter(Compare("water")[2], Compare("water")[3], label = 'Water Run 1 Without Average', color = 'b')
plt.show()
