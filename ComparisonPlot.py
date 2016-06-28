import numpy as np
import matplotlib.pyplot as plt



def Comparison_Function(filename,vertical_shift,period): #filename needs to be in strings
    """Given a data file, this function plots a graph"""
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
#
def Average_Function(function_1,function_2):
    """Takes two functions of the same dimension to make an average"""
    average_envelope_frequency = []
    average_envelope_photocurrent = []
    for frequency_1, frequency_2 in zip(function_1[0],function_2[0]): # frequency interation
        average_frequency = (frequency_1+frequency_2) * 0.5
        average_envelope_frequency.append(average_frequency)
    for photocurrent_1, photocurrent_2 in zip(function_1[1],function_2[1]): # photocurrent interation
         average_photocurrent = (photocurrent_1+ photocurrent_2) * 0.5
         average_envelope_photocurrent.append(average_photocurrent)

    return (average_envelope_frequency, average_envelope_photocurrent)

test_liszt = [1,2,3,4,5,6,7,8,9,10,11,12,13]

def Noise_Reduction(data_file):
    """Reduces the noise of a graph by taking the average from two nearest neighbours of each data point"""
    noisy_data = data_file
    # shortened_data = data_file[2:-2]
    improved_data = []
    start_index = 2
    for point in noisy_data:
        total = point[start_index-2] + point[start_index-1] + point[0] + point[start_index+1] + point[start_index+2]
        average_point = total/5

        improved_data.append(average_point)
        if point[start_index+1] == noisy_data[-1]:
            break

    return improved_data

print test_liszt[2:-2][-1]

# test = Noise_Reduction
leaf_average_x, leaf_average_y = Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[0], Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[1]
water_45_x, water_45_y = Average_Function(Comparison_Function("water_45_2",0.08,20),Comparison_Function("water_45",0.08,20))[0], Average_Function(Comparison_Function("water_45_2",0.08,20),Comparison_Function("water_45",0.08,20))[1]

plt.figure()
plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
plt.xlabel("Frequency $GHz$")
plt.ylabel("Photocurrent $nA$")

plt.plot(Comparison_Function("water",0.6,25)[0], Comparison_Function("water",0.6,25)[1], label = 'Water Run 1', color = 'b')

plt.plot(leaf_average_x, leaf_average_y, label = 'Average of Leaf Run', color = 'm')

# plt.plot(Comparison_Function("leaf",0.19,23)[0], Comparison_Function("leaf",0.19,23)[1], label = 'Leaf Run 1', color = 'g')

# plt.plot(Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[0],Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[1],  color = 'r', label = 'Average Reference Run')

# plt.plot(Comparison_Function("leaf_2",0.092,23)[2], Comparison_Function("leaf_2",0.092,23)[3], label = 'Leaf Run 2', color = 'm') # period = 28

# plt.plot(Average_Function(Comparison_Function("water_45",0.5,20),Comparison_Function("water_45",0.5,20))[0],Average_Function(Comparison_Function("water_45_2",0.5,20),Comparison_Function("water_45_2",0.5,20))[1])

# plt.plot(Comparison_Function("reference_45",0.1,18)[0], Comparison_Function("reference_45",0.1,18)[1], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')

# plt.plot(water_45_x, water_45_y, label = r'Average of Water Run 45$^\circ$', color = 'forestgreen')

# plt.plot(Comparison_Function("water_45",0.08,20)[0], Comparison_Function("water_45",0.08,20)[1], label = r'Water 45$^\circ$  Run 1', color = 'orange')

# plt.plot(Comparison_Function("water_45_2",0.08,20)[0], Comparison_Function("water_45_2",0.08,20)[1], label = r'Water 45$^\circ$  Run 2', color = 'purple')

plt.legend()
plt.show()
