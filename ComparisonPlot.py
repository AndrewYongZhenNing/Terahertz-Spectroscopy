import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#############################
# FUNCTION FOR DATA ANALYSIS
#############################

def CompareOld(filename,vertical_shift,period): #filename needs to be in strings
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

def Compare(filename, nearest_neighbours): #filename needs to be in strings
    """Given a data file, this function plots a graph"""

    plot = np.loadtxt(filename + ".dat")
    frequency = plot[:,1]
    photocurrent = plot[:,2]
    maximum_point = np.amax(plot[1:,0])

    for value in photocurrent:
        SUM = 0
        SUM += value

    photocurrent = photocurrent - SUM

    photocurrent_list = []
    frequency_list = []
    index_list = []
    envelope_photocurrent_list = []
    envelope_frequency_list = []
    log_envelope_photocurrent_list = []

    index = 0
    k = 0

    for value in photocurrent: #converts array to list [for now]
        photocurrent_list.append(value)

    for value in frequency:
        frequency_list.append(value)

    while index < len(frequency_list)-1: # length of frequency_list is 48334
    # for index in range(0,frequency_list[-1]+1):
        if photocurrent_list[0] > photocurrent_list[1]:
            if photocurrent_list[index] > 0 and photocurrent_list[index+1] < 0:
                index_list.append(index)
        elif photocurrent_list[0] < photocurrent_list[1]:
            if photocurrent_list[index] < 0 and photocurrent_list[index+1] > 0:
                index_list.append(index)
        index +=1


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

    for value in envelope_photocurrent_list:
        new_value = 20*np.log10(value)
        log_envelope_photocurrent_list.append(new_value)

    # NOISE REDUCTION BEGINS HERE:
    """Improves the quality of the data by reducing the noise of a graph. Takes the average from the nearest neighbours of each data point."""
    noisy_data = log_envelope_photocurrent_list
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

        total = sum(liszt)
        average_point = (1.*total)/((nearest_neighbours*2)+1) # the 1. is there to convert fractions into accurate decimal points
        improved_data.append(average_point)
        liszt[:] = [] #empties the list to be re-used again

        start_index += 1

    for index in range(len(noisy_data)-nearest_neighbours,len(noisy_data)): #fill in final few points into improved data
        improved_data.append(noisy_data[index])

    return (envelope_frequency_list,improved_data,frequency_list,photocurrent_list)


def Average(file_1,file_2, nearest_neighbours):
    """Takes two functions of the same dimension to make an average"""

    plot1 = np.loadtxt(file_1 + ".dat")
    plot2 = np.loadtxt(file_2 + ".dat")

    frequency1 = []
    photocurrent1 = plot1[:,2]

    frequency2 = []
    photocurrent2 = plot2[:,2]

    for value in plot1[:,1]:
        frequency1.append(value)

    for value in plot2[:,1]:
        frequency2.append(value)

    average_frequency = []
    average_photocurrent = []

    for frequency_1, frequency_2 in zip(frequency1,frequency2): # frequency interation
        average_f = (frequency_1+frequency_2) * 0.5
        average_frequency.append(average_f)

    average_photocurrent_array = (photocurrent1 + photocurrent2) * 0.5 # array form of photocurrent

    for value in average_photocurrent_array:
        SUM = 0
        SUM += value

    average_photocurrent_array = average_photocurrent_array - SUM

    for value in average_photocurrent_array:
        average_photocurrent.append(value) # list form of photocurrent

    index_list = []
    envelope_photocurrent_list = []
    envelope_frequency_list = []
    log_envelope_photocurrent_list = []

    index = 0
    k = 0


    while index < len(average_photocurrent)-1:
        if average_photocurrent[0] > average_photocurrent[1]: # oscillates in a -sin(x) form
            if average_photocurrent[index] > 0 and average_photocurrent[index+1] < 0:
                index_list.append(index)
        elif average_photocurrent[0] < average_photocurrent[1]: # oscillates in a sin(x) form
            if average_photocurrent[index] < 0 and average_photocurrent[index+1] > 0:
                index_list.append(index)
        index +=1


    while k < len(index_list)-1:
        start = index_list[k]
        end = index_list[k+1]
        shortened_photocurrent_list = average_photocurrent[start:end]
        shortened_frequency_list = average_frequency[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
        max_photocurrent = np.amax(average_photocurrent_array[start:end]) #picks out maximum value of photocurrent in one period
        envelope_photocurrent_list.append(max_photocurrent) #puts maximum photocurrent in list
        photocurrent_index = shortened_photocurrent_list.index(max_photocurrent) # gets the index corresponding to the selected photocurrent
        envelope_frequency_list.append(shortened_frequency_list[photocurrent_index])

        k += 1

    for value in envelope_photocurrent_list:
        new_value = 20*np.log10(value)
        log_envelope_photocurrent_list.append(new_value)

    # NOISE REDUCTION BEGINS HERE:
    """Improves the quality of the data by reducing the noise of a graph. Takes the average from the nearest neighbours of each data point."""
    noisy_data = log_envelope_photocurrent_list
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

        total = sum(liszt)
        average_point = (1.*total)/((nearest_neighbours*2)+1) # the 1. is there to convert fractions into accurate decimal points
        improved_data.append(average_point)
        liszt[:] = [] #empties the list to be re-used again

        start_index += 1

    for index in range(len(noisy_data)-nearest_neighbours,len(noisy_data)): #fill in final few points into improved data
        improved_data.append(noisy_data[index])

    # return (envelope_frequency_list,improved_data,frequency_list,photocurrent_list)


    return (envelope_frequency_list, improved_data, average_frequency, average_photocurrent)



# def Envelope_Average(function_1,function_2):
#     """Takes two functions of the same dimension to make an average"""
#     average_envelope_frequency = []
#     average_envelope_photocurrent = []
#     for frequency_1, frequency_2 in zip(function_1[0],function_2[0]): # frequency interation
#         average_frequency = (frequency_1+frequency_2) * 0.5
#         average_envelope_frequency.append(average_frequency)
#     for photocurrent_1, photocurrent_2 in zip(function_1[1],function_2[1]): # photocurrent interation
#          average_photocurrent = (photocurrent_1 + photocurrent_2) * 0.5
#          average_envelope_photocurrent.append(average_photocurrent)
#     print 'average envelope' , len(average_envelope_photocurrent)
#     return (average_envelope_frequency, average_envelope_photocurrent)

# def Noise_Reduction(data_set, nearest_neighbours):
#     """Improves the quality of the data by reducing the noise of a graph. Takes the average from the nearest neighbours of each data point."""
    # noisy_data = data_set
    # improved_data = []
    # start_index = nearest_neighbours
    #
    #
    # for index in range(0,nearest_neighbours): #fill in improved_data list with the first 'unused' points first (from 0th data point to (start_index-1)th data point)
    #     improved_data.append(noisy_data[index])
    #
    # liszt = []
    #
    #
    # while start_index < len(noisy_data) - nearest_neighbours:#while start_index < 11,  maximum is thus 11 in this case
    #     i = -(nearest_neighbours) #left most neighbour
    #     while i < nearest_neighbours+1: #maximum value of i is equal to right most value
    #         liszt.append(noisy_data[(start_index)+i])
    #         i +=1
    #
    # # for i in range(-(nearest_neighbours),(nearest_neighbours)): #for loop is awkward, fix here
    # #     liszt.append(start_index+i)
    #     # for points in noisy_data[(start_index)+i]:
    #     #     liszt.append(points)
    #     # print 'current list is:',liszt
    #
    #     total = sum(liszt)
    #     average_point = (1.*total)/((nearest_neighbours*2)+1) # the 1. is there to convert fractions into accurate decimal points
    #     improved_data.append(average_point)
    #     liszt[:] = [] #empties the list to be re-used again
    #
    #     start_index += 1
    #
    #
    # for index in range(len(noisy_data)-nearest_neighbours,len(noisy_data)): #fill in final few points into improved data
    #     improved_data.append(noisy_data[index])
    #
    # return improved_data

def Characteristic(function1_y, function2_y, nearest_neighbours):
    """Makes a spectral plot"""
    spectral = []
    for value1, value2 in zip(function1_y,function2_y):
        spec = abs(value1-value2) # it is the difference that we are interested in, so by putting it in absolte value, we know that the high peaks corresponds to a large difference between reference and sample, ie a drop in photocurrent due to absorption!
        spectral.append(spec)

    noisy_data = spectral
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
# reference_x, reference_y = Average(CompareOld("reference_scan2",0.5,24),CompareOld("reference_scan2.1",0.5,24))[0],Average(CompareOld("reference_scan2",0.5,24),CompareOld("reference_scan2.1",0.5,24))[1]
# leaf_average_x, leaf_average_y = Average(CompareOld("leaf",0.19,23),CompareOld("leaf_2",0.092,23))[0], Average(CompareOld("leaf",0.19,23),CompareOld("leaf_2",0.092,23))[1]
# water_45_x, water_45_y = Average(CompareOld("water_45_2",0.08,22),CompareOld("water_45",0.08,22))[0], Average(CompareOld("water_45_2",0.08,22),CompareOld("water_45",0.08,22))[1]
# water_45_closer_x, water_45_closer_y = Average(CompareOld("water_45_closer_2",0.09,22),CompareOld("water_45_closer",0.09,22))[0], Average(CompareOld("water_45_2",0.08,22),CompareOld("water_45",0.09,22))[1]
# reference_45_closer_x, reference_45_closer_y = Average(CompareOld("reference_45_closer_2",0.09,22),CompareOld("reference_45_closer",0.09,22))[0], Average(CompareOld("reference_45_closer_2",0.09,22),CompareOld("reference_45_closer",0.09,22))[1]
# reference_lens_x, reference_lens_y = Average(CompareOld("reference_lens_2",0.0,20),CompareOld("reference_lens_2.1",0.00,20))[0], Average(CompareOld("reference_lens_2",0.0,20),CompareOld("reference_lens_2.1",0.0,20))[1]

# reference_x, reference_y = Compare("reference_scan",4)[0], Compare("reference_scan",4)[1]
reference_x1, reference_y1 = Compare("reference_scan2",12)[0], Compare("reference_scan2",12)[1]
ref_45_x, ref_45_y = Average("reference_45_closer","reference_45_closer_2",12)[0], Average("reference_45_closer","reference_45_closer_2",12)[1]
ref_lens_x, ref_lens_y = Average("reference_lens_2", "reference_lens_2.1",12)[0],Average("reference_lens_2", "reference_lens_2.1",12)[1]

water_x, water_y = Compare("water",4)[0],Compare("water",4)[1]
water_45_x, water_45_y = Average("water_45_2","water_45",12)[0], Average("water_45_2","water_45",12)[1]
water_45_x1, water_45_y1 = Average("water_45_closer_2", "water_45_closer",15)[0], Average("water_45_closer_2", "water_45_closer",15)[1]

leaf_x, leaf_y = Average("leaf", "leaf_2",12)[0],Average("leaf", "leaf_2",12)[1]
leaf_x1, leaf_y1 = Compare("leaf_3",12)[0], Compare("leaf_3",12)[1]

acetone_x, acetone_y = Average("acetone_closer", "acetone_closer_2",12)[0],Average("acetone_closer", "acetone_closer_2",12)[1]
wafer_acetone_x, wafer_acetone_y = Average("wafer_acetone1","wafer_acetone2",12)[0], Average("wafer_acetone1","wafer_acetone2",12)[1]

wafer_x, wafer_y = Average("wafer_1","wafer_2",12)[0],Average("wafer_1","wafer_2",12)[1]
wafer_water_x, wafer_water_y = Average("wafer_water","wafer_water2",12)[0], Average("wafer_water","wafer_water2",12)[1]

#SPECTRAL PLOTS
water_char = Characteristic(reference_y1,water_y,6)
water_45_char = Characteristic(ref_45_y,water_45_y,6)
leaf_char = Characteristic(reference_y1,leaf_y1,6)
acetone_char = Characteristic(ref_45_y, acetone_y,6)
wafer_char = Characteristic(ref_lens_y,Compare("wafer_3",12)[1],6)
wafer_acetone_char = Characteristic( wafer_acetone_y,Compare("wafer_3",12)[1],6)
#
# print 'ref',len(reference_y1),'leaf',len(leaf_y1), 'water', len(water_y)
# print 'leafchar',len(leaf_char) #leaf char cannot be plotted as leaf has more data points than ref. zip can only perform operations up till the list with smallest elements, so the output of char will have smaller elements than the xdat of leaf, so they are different dimensions
# print 'acechar', len(acetone_char), 'ace', len(acetone_y)
# print 'wafchar', len(wafer_char), 'wafer', len(Compare("wafer_3",12)[1])
print 'wafacechar', len(wafer_acetone_char), 'ace', len(wafer_acetone_y)
###############
# PLOT SECTION
###############

plt.figure()
plt.grid()
plt.title("Plot of Envelope Photocurrent(nA) vs Frequency(GHz)")#, fontsize = 30
# plt.title("Spectral Plot of Acetone Run 3")
plt.xlabel("Frequency $GHz$")#, fontsize = 30
plt.ylabel("Dynamic Range $dB$")#, fontsize = 30
plt.xticks()#fontsize = 20
plt.yticks()#fontsize = 20

# REFERENCE RUN
# plt.plot(Compare("reference_scan2",0)[0],Compare("reference_scan2",0)[1], label = 'Reference Run 2')
# plt.plot(Compare("reference_scan2.1",0)[0],Compare("reference_scan2.1",0)[1], label = 'Reference Run 2.1')
# plt.plot(Compare("reference_scan2.1",0)[2],Compare("reference_scan2.1",0)[3], label = 'Reference Run 2.1#')
# plt.plot(ref_x,ref_y, color = 'yellow',label = 'Average Reference Run')

# plt.plot(water_x1, water_y1, color = 'cyan', label = 'Water Run 550-570GHz')
# plt.plot(water_x2, water_y2, color = 'blueviolet', label = 'Water Run 1255-1280GHz')

##SPECTRAL PLOTS
# plt.plot(water_x, water_char, color = 'b')
# plt.plot(water_45_x, water_45_char, color = 'b')
# plt.plot(leaf_x1,leaf_char, color = 'g')
# plt.plot(acetone_x, acetone_char, color = 'purple')
# plt.plot(Compare("wafer_3",12)[0], wafer_char, color = 'gold')
# plt.plot(wafer_acetone_x, wafer_acetone_char, color = 'purple')
#################

# plt.plot(reference_x, reference_y, color = 'r', label = 'Reference Run     1')
# plt.plot(reference_x1, reference_y1, color = 'y', label = 'Reference Run')
# plt.plot(ref_lens_x, ref_lens_y, color = 'yellow', label = 'Reference (Lens) Run')
plt.plot(Compare("reference_lens_3",12)[0],Compare("reference_lens_3",12)[1], color = 'y', label = 'Reference Run')

# plt.plot(Compare("water",12)[0],Compare("water",12)[1], color = 'b', label = 'Water Run')
# plt.plot(leaf_x,leaf_y,color = 'g', label = 'Average Leaf Run')
# plt.plot(leaf_x1,leaf_y1, color = 'g', label = 'Leaf Run')
# plt.plot(ref_45_x, ref_45_y, color = 'y', label =r'Average Reference 45$^\circ$ Run' )
# plt.plot(water_45_x1, water_45_y1, color ='b', label =  r'Average Water 45$^\circ$ Run')
# plt.plot(acetone_x,acetone_y, color = 'purple', label =   r'Average Acetone 45$^\circ$ Run')

# plt.plot(Compare("wafer_1",12)[0],Compare("wafer_1",12)[1], color = 'g',label = 'test1')
# plt.plot(Compare("wafer_2",12)[0],Compare("wafer_2",12)[1], color = 'gold',label = 'test2')
plt.plot(Compare("wafer_3",12)[0],Compare("wafer_3",12)[1], color = 'tomato', label = 'Silicon Mesh Run')
# plt.plot(wafer_x, wafer_y, color = 'brown',label = 'Wafer Run')

plt.plot(wafer_water_x, wafer_water_y, color = 'b', label = 'Silicon Mesh (Water) Run')
# plt.plot(Compare("wafer_water",12)[0],Compare("wafer_water",12)[1], color = 'b', label = 'Wafer (water) Run')
# plt.plot(Compare("wafer_water2",12)[0],Compare("wafer_water2",12)[1], color = 'b', label = 'water')

# plt.plot(Compare("wafer_acetone1",12)[0],Compare("wafer_acetone1",12)[1], color = 'purple', label ='test')
plt.plot(wafer_acetone_x, wafer_acetone_y, color = 'purple', label = 'Silicon Mesh (Acetone) Run')
# plt.plot(CompareOld("reference_scan2",0.5,24)[2],CompareOld("reference_scan2",0.5,24)[3],  color = 'r', label = 'Average Reference Run')
# plt.scatter(CompareOld("reference_scan2",0.5,24)[2],CompareOld("reference_scan2",0.5,24)[3],  color = 'r', label = 'Average Reference Run')
# plt.plot(CompareOld("reference_scan2.1",0.5,24)[0],CompareOld("reference_scan2.1",0.5,24)[1],color = 'r')
# plt.plot(reference_x, Noise_Reduction(reference_y,4), color = 'r', label = 'Average Reference Run')
# plt.plot(CompareOld('reference_scan',0,31)[0],CompareOld('reference_scan',0,31)[1], label = 'Reference Scan 1', color = 'y')
# plt.scatter(CompareOld('reference_scan',0,31)[2],CompareOld('reference_scan',0,20)[3])

# plt.plot(CompareOld("reference_45",0.1,20)[0], CompareOld("reference_45",0.1,20)[1], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.scatter(CompareOld("reference_45",0.1,18)[2], CompareOld("reference_45",0.1,18)[3], label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.plot(CompareOld("reference_45",0.1,20)[0], Noise_Reduction(CompareOld("reference_45",0.1,20)[1],8), label = r'Reference 45$^\circ$  Run 1', color = 'firebrick')
# plt.plot(CompareOld("reference_45_closer",0.09,22)[0], Noise_Reduction(CompareOld("reference_45_closer",0.09,22)[1],4), label = r'Reference 45$^\circ$  Run 2.1', color = 'darkgreen')
# plt.scatter(CompareOld("reference_45_closer",0.09,22)[2], CompareOld("reference_45_closer",0.09,22)[3], label = r'Reference 45$^\circ$  Run 2.1', color = 'darkgreen')
# plt.plot(CompareOld("reference_45_closer_2",0.09,23)[0], Noise_Reduction(CompareOld("reference_45_closer_2",0.09,23)[1],4), label = r'Reference 45$^\circ$  Run 2.2', color = 'firebrick')
# plt.scatter(CompareOld("reference_45_closer_2",0.09,23)[0], CompareOld("reference_45_closer_2",0.09,23)[1], label = r'Reference 45$^\circ$  Run 2.2', color = 'firebrick')
# plt.scatter(CompareOld("reference_lens",0.05,23)[0], CompareOld("reference_lens",0.05,23)[1], label = r'Reference with Lens  Run 1', color = 'firebrick')


# plt.plot(CompareOld("reference_lens",0.05,20)[0], Noise_Reduction(CompareOld("reference_lens",0.05,20)[1],4), label = r'Reference with Lens  Run 1', color = 'rosybrown')
# plt.scatter(CompareOld("reference_lens",0.05,23)[2], Noise_Reduction(CompareOld("reference_lens",0.05,23)[3],0), label = r'Reference with Lens  Run 2.1', color = 'darkgreen')


# plt.plot(CompareOld("reference_lens_2",0.0,20)[0], Noise_Reduction(CompareOld("reference_lens_2",0.0,20)[1],4), label = r'Reference with Lens  Run 2', color = 'tomato')
# plt.scatter(CompareOld("reference_lens_2",0.0,23)[2], Noise_Reduction(CompareOld("reference_lens_2",0.0,23)[3],0), label = r'Reference with Lens  Run 2', color = 'tomato')

# plt.plot(CompareOld("reference_lens_2.1",0.0,20)[0], Noise_Reduction(CompareOld("reference_lens_2.1",0.0,20)[1],4), label = r'Reference with Lens  Run 2.1', color = 'darkgreen')
# plt.scatter(CompareOld("reference_lens_2.1",0.0,20)[2], Noise_Reduction(CompareOld("reference_lens_2.1",0.0,20)[3],0), label = r'Reference with Lens  Run 2.1', color = 'darkgreen')

# plt.plot(reference_lens_x, Noise_Reduction(reference_lens_y,4), color = 'tomato', label = 'Average of Lens Run 2')
# plt.scatter(reference_lens_x, Noise_Reduction(reference_lens_y,4), color = 'tomato', label = 'Average of Lens Run 2')

# plt.plot(reference_45_closer_x, Noise_Reduction(reference_45_closer_y,0), label = 'Average of Reference Scan 2', color = 'g')
#
# WATER RUN
# plt.plot(CompareOld("water",0.6,25)[0], Noise_Reduction(CompareOld("water",0.6,25)[1],4), label = 'Water Run 1 Without Average', color = 'b')
# plt.scatter(CompareOld("water",0.6,25)[2], CompareOld("water",0.6,25)[3], label = 'Water Run 1 Without Average', color = 'b')
# plt.plot(CompareOld("water",0.6,24)[0], Noise_Reduction(CompareOld("water",0.6,24)[1],4), label = 'Water Run 1', color = 'b')

# plt.plot(CompareOld("water_45",0.08,22)[0], Noise_Reduction(CompareOld("water_45",0.08,22)[1],4), label = r'Water 45$^\circ$  Run 1.1', color = 'orange')
# plt.scatter(CompareOld("water_45",0.08,20)[2], Noise_Reduction(CompareOld("water_45",0.08,20)[3],4), label = r'Water 45$^\circ$  Run 1.1', color = 'orange')

## plt.plot(CompareOld("water_45_2",0.08,20)[0], Noise_Reduction(CompareOld("water_45_2",0.08,20)[1],4), label = r'Water 45$^\circ$  Run 1.2', color = 'r')
## USE THE ONE BELOW FOR COMPARING WITH WATER_45

# USE THIS
# plt.plot(water_45_x, Noise_Reduction(water_45_y,4), label = r'Average of Water 45$^\circ$ Run 1' , color = 'r')

# plt.plot(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = r'Average of Water 45$^\circ$ Run 2' , color = 'b')

##
## plt.plot(("water_45_closer",0.09,23)[2], CompareOld("water_45_closer",0.09,23)[3], label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')
## plt.scatter(CompareOld("water_45_closer",0.09,23)[2], CompareOld("water_45_closer",0.09,23)[3], label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')
# plt.plot(CompareOld("water_45_closer_2",0.08,34)[0], Noise_Reduction(CompareOld("water_45_closer_2",0.08,34)[1],4), label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')
## plt.scatter(CompareOld("water_45_closer_2",0.08,34)[2], CompareOld("water_45_closer_2",0.08,34)[3], label = 'Water 45$^\circ$ Run 2.2', color = 'r')
## plt.plot(CompareOld("water_45_closer",0.09,34)[0], Noise_Reduction(CompareOld("water_45_closer",0.09,34)[1],4), label = 'Water 45$^\circ$ Run 2.1', color = 'chartreuse')

# plt.plot(CompareOld("water_45_closer_2",0.09,22)[0], Noise_Reduction(CompareOld("water_45_closer_2",0.09,22)[1],4), label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')


# plt.scatter(CompareOld("water_45_closer_2",0.08,22)[0], Noise_Reduction(CompareOld("water_45_closer_2",0.08,22)[1],4), label = 'Water 45$^\circ$ Run 2.2', color = 'maroon')
# plt.plot(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = 'Average of Water 45$^\circ$', color = 'darksalmon')
# plt.scatter(water_45_closer_x, Noise_Reduction(water_45_closer_y,4), label = 'Average of Water 45$^\circ$', color = 'darksalmon')

# LEAF RUN
# plt.plot(CompareOld("leaf",0.19,23)[0], CompareOld("leaf",0.19,23)[1], label = 'Leaf Run 1', color = 'g')
# plt.plot(CompareOld("leaf_2",0.092,23)[0], CompareOld("leaf_2",0.092,23)[1], label = 'Leaf Run 2', color = 'm') # period = 28
# plt.plot(leaf_average_x, Noise_Reduction(leaf_average_y,4), label = 'Average of Leaf Run', color = 'sandybrown')

# ACERTONE RUN
# plt.plot(CompareOld("acetone_closer",0.1,20)[0],Noise_Reduction(CompareOld("acetone_closer",0.1,20)[1],4), label = 'Acetone Run 1', color = 'chocolate')
# plt.plot(CompareOld("acetone_closer_2",0.1,20)[0],Noise_Reduction(CompareOld("acetone_closer",0.1,20)[1],4), label = 'Acetone Run 2', color = 'tan')
# plt.scatter(CompareOld("acetone_closer_2",0.1,24)[2],Noise_Reduction(CompareOld("acetone_closer",0.1,24)[3],0), label = 'Acetone Run 1', color = 'powderblue')
#

# WAFER RUN
# plt.plot(CompareOld("wafer_1",0.1,23)[0],Noise_Reduction(CompareOld('wafer_1',0.1,23)[1],4), label = 'Wafer Run 1: Original function')
# plt.plot(Compare("wafer_1")[0],Noise_Reduction(Compare('wafer_1')[1],8), label = 'Wafer Run 1 :New function')
# plt.plot(CompareOld("wafer_water",0.04,22)[0], Noise_Reduction(CompareOld("wafer_water",0.04,22)[1],4), label = 'Wafer Water Run 1: Original')
# plt.plot(Compare("wafer_water")[0],Noise_Reduction(Compare("wafer_water")[1],8), label = 'Wafer Water Run 1: New')
# plt.plot(CompareOld("wafer_water2",0.11,21)[0], Noise_Reduction(CompareOld("wafer_water2",0.11,21)[1],4), label = 'Wafer Water Run 2: Original')
# plt.scatter(CompareOld("wafer_water2",0.11,22)[2], Noise_Reduction(CompareOld("wafer_water2",0.11,21)[3],0), label = 'Wafer Water Run 1: Original')
# plt.plot(Compare("wafer_water2")[0],Noise_Reduction(Compare("wafer_water2")[1],8), label = 'Wafer Water Run 2: New')
# plt.scatter(CompareOld("wafer_water",0.04,20)[2], CompareOld("wafer_water",0.04,22)[3])
plt.plot()

plt.legend()
plt.show()
