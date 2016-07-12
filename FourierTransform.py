import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
#
def Compare(filename,vertical_shift,period): #filename needs to be in strings
    """Given a data file, this function plots a graph"""

    # def obtain_period(frequency_data,photocurrent_data):
    #     def function(x,a,b,c): #presumed shape of the graph
    #         return a*np.sin(b*x)+c
    #     popt, pcov = curve_fit(function,frequency_data[-1000:],photocurrent_data[-1000:])
    #     period = (2*np.pi)/popt[1]
    #     return period # NOTE PROBLEM IS HERE

    plot = np.loadtxt(filename + ".dat")
    frequency = plot[:,1]
    photocurrent = plot[:,2] + vertical_shift
    maximum_point = np.amax(plot[1:,0])
    start = 0
    period = period
    end = period

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

def Average(function_1,function_2):
    """Takes two functions of the same dimension to make an average"""
    average_envelope_frequency = []
    average_envelope_photocurrent = []
    for frequency_1, frequency_2 in zip(function_1[0],function_2[0]): # frequency interation
        average_frequency = (frequency_1+frequency_2) * 0.5
        average_envelope_frequency.append(average_frequency)
    for photocurrent_1, photocurrent_2 in zip(function_1[1],function_2[1]): # photocurrent interation
         average_photocurrent = (photocurrent_1 + photocurrent_2) * 0.5
         average_envelope_photocurrent.append(average_photocurrent)

    return (average_envelope_frequency, average_envelope_photocurrent)

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
#
#
reference_lens_x, reference_lens_y = Average(Compare("reference_lens_2",0.0,20),Compare("reference_lens_2.1",0.00,20))[0],Average(Compare("reference_lens_2",0.0,20),Compare("reference_lens_2.1",0.0,20))[1]
water_45_closer_x, water_45_closer_y = Average(Compare("water_45_closer_2",0.09,22),Compare("water_45_closer",0.09,22))[0], Average(Compare("water_45_2",0.08,22),Compare("water_45",0.09,22))[1]
#

#
y = Noise_Reduction(reference_lens_y,4)
# n = len(y)                       # length of the signal
frequency = range(1,len(y)+1)           # one side frequency range
FT_y = np.fft.fft(y)            # fft computing here

#DATA POINTS NEED CLEANING IN FT_y: 65 TO 85

a = FT_y[0:65]
b = FT_y[65:85]*1.0/3
c = FT_y[85:2334]
d = FT_y[2334:2354]*1.0/3
e = FT_y[2354:]
array = np.concatenate((a,b))
array = np.concatenate((array,c))
array = np.concatenate((array,d))
array = np.concatenate((array,e))
IFT_y = np.fft.ifft(array)
#2334 - 2353
f = FT_y[85:]
array1 = np.concatenate((a,b))
array1 = np.concatenate((array1,f))
IFT_y1 = np.fft.ifft(array1)

plt.subplot(2,1,1)
plt.grid()
plt.title('Fourier Analysis')
plt.xlabel(r'Frequency $GHz$')
plt.ylabel(r'$\hatf$($\omega$)')
plt.plot(frequency, abs(FT_y), color = 'r', label = 'Before Peak Removal')
plt.legend()
plt.subplot(2,1,2)
plt.grid()
plt.xlabel(r'Frequency $GHz$')
plt.ylabel(r'$\hatf$($\omega$)')
plt.plot(frequency, abs(array), color = 'b', label = 'After Peak Removal')
plt.legend()
plt.show()

plt.subplot(2,1,1)
plt.title('Comparison')
plt.grid()
plt.xlabel('Frequency $GHz$')
plt.ylabel('Envelope Photocurrent $nA$')
plt.plot(reference_lens_x, Noise_Reduction(reference_lens_y,4), label = 'Before Fourier Transform', color = 'r')
plt.legend()
plt.subplot(2,1,2)
plt.grid()
plt.xlabel('Frequency $GHz$')
plt.ylabel('Envelope Photocurrent $nA$')
plt.plot(reference_lens_x, Noise_Reduction(IFT_y,4), label = 'After Fourier Transform')
plt.plot(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), color = 'g', label = r'Average of Water 45$^\circ$ Run 2')
plt.legend()
plt.show()
