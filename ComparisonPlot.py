import numpy as np
import matplotlib.pyplot as plt

#############################
# FUNCTION FOR DATA ANALYSIS
#############################

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




leaf_average_x, leaf_average_y = Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[0], Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[1]
water_45_x, water_45_y = Average_Function(Comparison_Function("water_45_2",0.08,22),Comparison_Function("water_45",0.08,22))[0], Average_Function(Comparison_Function("water_45_2",0.08,22),Comparison_Function("water_45",0.08,22))[1]
water_45_closer_x, water_45_closer_y = Average_Function(Comparison_Function("water_45_closer_2",0.09,22),Comparison_Function("water_45_closer",0.09,22))[0], Average_Function(Comparison_Function("water_45_2",0.08,22),Comparison_Function("water_45",0.09,22))[1]
reference_45_closer_x, reference_45_closer_y = Average_Function(Comparison_Function("reference_45_closer_2",0.09,22),Comparison_Function("reference_45_closer",0.09,22))[0], Average_Function(Comparison_Function("reference_45_closer_2",0.09,22),Comparison_Function("reference_45_closer",0.09,22))[1]

###############
# PLOT SECTION
###############

plt.figure()
plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
plt.xlabel("Frequency $GHz$")
plt.ylabel("Photocurrent $nA$")

# REFERENCE RUN
#
# plt.plot(Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[0],Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[1],  color = 'r', label = 'Average Reference Run')
# plt.plot(Comparison_Function("reference_45",0.1,20)[0], Comparison_Function("reference_45",0.1,20)[1], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.scatter(Comparison_Function("reference_45",0.1,18)[2], Comparison_Function("reference_45",0.1,18)[3], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.plot(Comparison_Function("reference_45",0.1,20)[0], Noise_Reduction(Comparison_Function("reference_45",0.1,20)[1],8), label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.plot(Comparison_Function("reference_45_closer",0.09,22)[0], Noise_Reduction(Comparison_Function("reference_45_closer",0.09,22)[1],4), label = r'Reference 45$^\circ$  Run 2.1', color = 'darkgreen')
# plt.scatter(Comparison_Function("reference_45_closer",0.09,22)[2], Comparison_Function("reference_45_closer",0.09,22)[3], label = r'Reference 45$^\circ$  Run 2.1', color = 'darkgreen')
# plt.plot(Comparison_Function("reference_45_closer_2",0.09,23)[0], Noise_Reduction(Comparison_Function("reference_45_closer_2",0.09,23)[1],4), label = r'Reference 45$^\circ$  Run 2.2', color = 'firebrick')
# plt.scatter(Comparison_Function("reference_45_closer_2",0.09,23)[0], Comparison_Function("reference_45_closer_2",0.09,23)[1], label = r'Reference 45$^\circ$  Run 2.2', color = 'firebrick')

# plt.plot(reference_45_closer_x, Noise_Reduction(reference_45_closer_y,4), label = 'Average o Reference Scan 2', color = 'fuchsia')
#
# WATER RUN
plt.plot(Comparison_Function("water",0.6,25)[2], Comparison_Function("water",0.6,25)[3], label = 'Water Run 1 Without Average', color = 'b')
## plt.plot(Comparison_Function("water",0.6,25)[0], Noise_Reduction(Comparison_Function("water",0.6,25)[1],14), label = 'Water Run 1', color = 'b')

# plt.plot(Comparison_Function("water_45",0.08,22)[2], Noise_Reduction(Comparison_Function("water_45",0.08,22)[3],4), label = r'Water 45$^\circ$  Run 1.1', color = 'orange')
# plt.scatter(Comparison_Function("water_45",0.08,20)[2], Noise_Reduction(Comparison_Function("water_45",0.08,20)[3],4), label = r'Water 45$^\circ$  Run 1.1', color = 'orange')

## plt.plot(Comparison_Function("water_45_2",0.08,20)[0], Noise_Reduction(Comparison_Function("water_45_2",0.08,20)[1],4), label = r'Water 45$^\circ$  Run 1.2', color = 'r')
## USE THE ONE BELOW FOR COMPARING WITH WATER_45

# USE THIS
# plt.plot(water_45_x, Noise_Reduction(water_45_y,4), label = r'Average of Water 45$^\circ$ Run 1' , color = 'r')
# plt.plot(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = r'Average of Water 45$^\circ$ Run 2' , color = 'b')

##
## plt.plot(Comparison_Function("water_45_closer",0.09,23)[2], Comparison_Function("water_45_closer",0.09,23)[3], label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')
## plt.scatter(Comparison_Function("water_45_closer",0.09,23)[2], Comparison_Function("water_45_closer",0.09,23)[3], label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')
## plt.plot(Comparison_Function("water_45_closer_2",0.08,34)[2], Comparison_Function("water_45_closer_2",0.08,34)[3], label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')
## plt.scatter(Comparison_Function("water_45_closer_2",0.08,34)[2], Comparison_Function("water_45_closer_2",0.08,34)[3], label = 'Water 45$^\circ$ Run 2.2', color = 'r')
## plt.plot(Comparison_Function("water_45_closer",0.09,34)[0], Noise_Reduction(Comparison_Function("water_45_closer",0.09,34)[1],4), label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')

# plt.plot(Comparison_Function("water_45_closer_2",0.09,22)[0], Noise_Reduction(Comparison_Function("water_45_closer_2",0.09,22)[1],4), label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')


# plt.scatter(Comparison_Function("water_45_closer_2",0.08,22)[0], Noise_Reduction(Comparison_Function("water_45_closer_2",0.08,22)[1],4), label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')
# plt.plot(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = 'Average of Water 45$^\circ$', color = 'darksalmon')
# plt.scatter(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = 'Average of Water 45$^\circ$', color = 'darksalmon')

# LEAF RUN
# plt.plot(Comparison_Function("leaf",0.19,23)[0], Comparison_Function("leaf",0.19,23)[1], label = 'Leaf Run 1', color = 'g')
# plt.plot(Comparison_Function("leaf_2",0.092,23)[0], Comparison_Function("leaf_2",0.092,23)[1], label = 'Leaf Run 2', color = 'm') # period = 28
# plt.plot(leaf_average_x, Noise_Reduction(leaf_average_y,4), label = 'Average of Leaf Run', color = 'sandybrown')

# ACERTONE RUN
# plt.plot(Comparison_Function("acetone_closer",0.1,20)[0],Noise_Reduction(Comparison_Function("acetone_closer",0.1,20)[1],4), label = 'Acetone Run 1', color = 'chocolate')

# plt.spines['bottom'].set_position('zero')
plt.legend()
plt.show()
