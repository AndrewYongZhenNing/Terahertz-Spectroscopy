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

#############
# FIX THIS NEXT TIME, INCLUDE LOOPS TO GENERALISE THE FUNCTION
###############

def Noise_Reduction(data_set, nearest_neighbours):
    """Reduces the noise of a graph by taking the average from the nearest neighbours of each data point"""
    noisy_data = data_set
    improved_data = []
    start_index = nearest_neighbours


    for index in range(0,nearest_neighbours): #fill in improved_data list with the first 'unused' points first (from 0th data point to (start_index-1)th data point)
        improved_data.append(noisy_data[index])

    liszt = []


    while start_index < len(noisy_data) - nearest_neighbours:#while start_index < 11,  maximum is thus 11 in this case
        i = -(nearest_neighbours) #left most neighbour
        while i < nearest_neighbours+1: #maximum value of i is equal to start index
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


test_liszt = [11,62,3,4,5,6,7,8,9,10,11,12,13,14,150]
liszt = []
output_liszt = []
# test_liszt[:] = [] # empties the list again

nearest_neighbours= 4
start_index = nearest_neighbours

# print 'number of points = ', len(test_liszt)- nearest_neighbours

while start_index < len(test_liszt) - nearest_neighbours: #while start_index < 11,  maximum is thus 11 in this case
    i = -nearest_neighbours # when re-iterating, resets i back to nearest neighbour value
    while i < nearest_neighbours+1: #maximum value of i is equal to start index
        # for points in test_liszt[(start_index)+i]
        liszt.append(test_liszt[(start_index)+i])
        i +=1
    total = sum(liszt)
    average_point = (1.*total)/((nearest_neighbours*2)+1)
    output_liszt.append(average_point)
    liszt[:] = []

    start_index += 1

# print 'average points = ', output_liszt, 'number of average points = ', len(output_liszt)

print Noise_Reduction(test_liszt, 4)
print len(Noise_Reduction(test_liszt, 4))
# blank = sum(test_liszt)
# print blank

leaf_average_x, leaf_average_y = Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[0], Average_Function(Comparison_Function("leaf",0.19,23),Comparison_Function("leaf_2",0.092,23))[1]
water_45_x, water_45_y = Average_Function(Comparison_Function("water_45_2",0.08,20),Comparison_Function("water_45",0.08,20))[0], Average_Function(Comparison_Function("water_45_2",0.08,20),Comparison_Function("water_45",0.08,20))[1]

# plt.figure()
# plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
# plt.xlabel("Frequency $GHz$")
# plt.ylabel("Photocurrent $nA$")

# plt.plot(Comparison_Function("water",0.6,25)[0], Comparison_Function("water",0.6,25)[1], label = 'Water Run 1', color = 'b')

# plt.plot(leaf_average_x, leaf_average_y, label = 'Average of Leaf Run', color = 'm')

# plt.plot(Comparison_Function("leaf",0.19,23)[0], Comparison_Function("leaf",0.19,23)[1], label = 'Leaf Run 1', color = 'g')

# plt.plot(Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[0],Average_Function(Comparison_Function("reference_scan2",0.5,24),Comparison_Function("reference_scan2.1",0.5,24))[1],  color = 'r', label = 'Average Reference Run')

# plt.plot(Comparison_Function("leaf_2",0.092,23)[2], Comparison_Function("leaf_2",0.092,23)[3], label = 'Leaf Run 2', color = 'm') # period = 28

# plt.plot(Average_Function(Comparison_Function("water_45",0.5,20),Comparison_Function("water_45",0.5,20))[0],Average_Function(Comparison_Function("water_45_2",0.5,20),Comparison_Function("water_45_2",0.5,20))[1])

# plt.plot(Comparison_Function("reference_45",0.1,18)[0], Comparison_Function("reference_45",0.1,18)[1], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')

# plt.plot(water_45_x, water_45_y, label = r'Average of Water Run 45$^\circ$', color = '')

# plt.plot(Comparison_Function("water_45",0.08,20)[0], Comparison_Function("water_45",0.08,20)[1], label = r'Water 45$^\circ$  Run 1', color = 'red')
# plt.plot(Comparison_Function("water_45",0.08,20)[0], Noise_Reduction(Comparison_Function("water_45",0.08,20)[1]), label = r'Water 45$^\circ$  Run 1', color = 'orange')



# plt.plot(Comparison_Function("water_45_2",0.08,20)[0], Comparison_Function("water_45_2",0.08,20)[1], label = r'Water 45$^\circ$  Run 2', color = 'purple')
#
# plt.legend()
# plt.show()
