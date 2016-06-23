import numpy as np
import matplotlib.pyplot as plt

# this is a github edit

def Comparison_Function(filename,vertical_shift,period): #filename needs to be in strings
    plot = np.loadtxt(filename + ".dat")
    a = vertical_shift
    frequency = plot[:,1]
    photocurrent = plot[:,2] + a
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

    return (envelope_frequency_list,log_envelope_photocurrent_list,photo)
#
# # plot_frequency, plot_photocurrent = Comparison_Function()
#
# #############################################################################################
# #add a new plot here under the name plot_n, where n is a new set of data
# #############################################################################################
# plot_1 = np.loadtxt("leaf.dat")
# plot_2 = np.loadtxt("reference_scan2.dat")
# plot_3 = np.loadtxt("reference_scan2.1.dat")
# plot_4 = np.loadtxt("water.dat")
#
# ############################################################################################
# # add vertical shift to respective plots to make it symmetrical about x axis [DEFAULT = 0]
# ############################################################################################
# a = 0.2 # leaf
# b = 0.4
# c = 0.4
# d = 0.6 # water
#
# ############################################################################################
# frequency_p1 = plot_1[1:,1]
# photocurrent_p1 = plot_1[1:,2]+ a #shifts the graph to be minimally symmetric at y=0
#
# frequency_p2 = plot_2[:,1]
# photocurrent_p2 = plot_2[:,2]+ b #shifts the graph to be minimally symmetric at y=0
#
# frequency_p3 = plot_3[:,1]
# photocurrent_p3 = plot_3[:,2]+ c #shifts the graph to be minimally symmetric at y=0
#
# average_photocurrent = (photocurrent_p2+photocurrent_p3)/2
# average_frequency = (frequency_p2+frequency_p3)/2
#
# frequency_p4 = plot_4[1:,1]
# photocurrent_p4 = plot_4[1:,2]+ d #shifts the graph to be minimally symmetric at y=0
#
# """
# snvksv
# vsm,vs
# evmelv
# lenve
# #"""
# ##############################################################################################
# # for differrent scans, there are different periods, adjust them respectively here
# ##############################################################################################
# max_1 = np.amax(plot_1[1:,0])
# max_2 = np.amax(plot_2[1:,0])
# max_3 = np.amax(plot_3[1:,0])
# max_4 = np.amax(plot_4[1:,0])
#
# start_1 = 0
# start_2 = 0
# start_3 = 0
# start_4 = 0
# period_1 = 24 #leaf
# period_2 = 25
# period_3 = 25
# period_4 = 25 #water
# end_1 = period_1 # start and end of a period
# end_2 = period_2
# end_3 = period_3
# end_4 = period_4
#
# # period for water is 25
# # period for leaf is 25
#
# ##############################################################################################
# # convert array to lists here
# ##############################################################################################
#
# photocurrent_p1_list = []
# frequency_p1_list = []
# envelope_photocurrent_p1_list = []
# envelope_frequency_p1_list = []
# log_envelope_photocurrent_p1_list = []
#
# photocurrent_p2_list = []
# frequency_p2_list = []
# envelope_photocurrent_p2_list = []
# envelope_frequency_p2_list = []
# log_envelope_photocurrent_p2_list = []
#
# photocurrent_p3_list = []
# frequency_p3_list = []
# envelope_photocurrent_p3_list = []
# envelope_frequency_p3_list = []
# log_envelope_photocurrent_p3_list = []
#
# average_photocurrent_list = []
# average_frequency_list = []
# envelope_average_photocurrent_list = []
# envelope_average_frequency_list = []
# log_envelope_average_photocurrent_list = []
#
# photocurrent_p4_list = []
# frequency_p4_list = []
# envelope_photocurrent_p4_list = []
# envelope_frequency_p4_list = []
# log_envelope_photocurrent_p4_list = []
#
# for value in photocurrent_p1: #converts array to list [for now]
#     photocurrent_p1_list.append(value)
#
# for value in frequency_p1:
#     frequency_p1_list.append(value)
#
# for value in photocurrent_p2: #converts array to list [for now]
#     photocurrent_p2_list.append(value)
#
# for value in frequency_p2:
#     frequency_p2_list.append(value)
#
# for value in photocurrent_p3: #converts array to list [for now]
#     photocurrent_p3_list.append(value)
#
# for value in frequency_p3:
#     frequency_p3_list.append(value)
#
# for value in photocurrent_p4: #converts array to list [for now]
#     photocurrent_p4_list.append(value)
#
# for value in frequency_p4:
#     frequency_p4_list.append(value)
#
#
# while start_1 < max_1-period_1 and end_1 < max_1:
#     # for plot #1
#     shortened_photocurrent_p1_list = photocurrent_p1_list[start_1:end_1]
#     shortened_frequency_p1_list = frequency_p1_list[start_1:end_1] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
#     max_photocurrent_p1 = np.amax(photocurrent_p1[start_1:end_1]) #picks out maximum value of photocurrent in one period
#     envelope_photocurrent_p1_list.append(max_photocurrent_p1) #puts maximum photocurrent in list
#     index_p1 = shortened_photocurrent_p1_list.index(max_photocurrent_p1) # gets the index corresponding to the selected photocurrent
#     envelope_frequency_p1_list.append(shortened_frequency_p1_list[index_p1])
#
#     start_1 += period_1
#     end_1 += period_1
#
# while start_2 < max_2-period_2 and end_2 < max_2:
#     # for plot #2
#     shortened_photocurrent_p2_list = photocurrent_p2_list[start_2:end_2]
#     shortened_frequency_p2_list = frequency_p2_list[start_2:end_2] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
#     max_photocurrent_p2 = np.amax(photocurrent_p2[start_2:end_2]) #picks out maximum value of photocurrent in one period
#     envelope_photocurrent_p2_list.append(max_photocurrent_p2) #puts maximum photocurrent in list
#     index_p2 = shortened_photocurrent_p2_list.index(max_photocurrent_p2) # gets the index corresponding to the selected photocurrent
#     envelope_frequency_p2_list.append(shortened_frequency_p2_list[index_p2])
#
#     start_2 += period_2
#     end_2 += period_2
#
# while start_3 < max_3-period_3 and end_3 < max_3:
#     # for plot #3
#     shortened_photocurrent_p3_list = photocurrent_p3_list[start_3:end_3]
#     shortened_frequency_p3_list = frequency_p3_list[start_3:end_3] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
#     max_photocurrent_p3 = np.amax(photocurrent_p3[start_3:end_3]) #picks out maximum value of photocurrent in one period
#     envelope_photocurrent_p3_list.append(max_photocurrent_p3) #puts maximum photocurrent in list
#     index_p3 = shortened_photocurrent_p3_list.index(max_photocurrent_p3) # gets the index corresponding to the selected photocurrent
#     envelope_frequency_p3_list.append(shortened_frequency_p3_list[index_p3])
#
#     start_3 += period_3
#     end_3 += period_3
#
# while start_4 < max_4-period_4 and end_4 < max_4:
#     # for plot #4
#     shortened_photocurrent_p4_list = photocurrent_p4_list[start_4:end_4]
#     shortened_frequency_p4_list = frequency_p4_list[start_4:end_4] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
#     max_photocurrent_p4 = np.amax(photocurrent_p4[start_4:end_4]) #picks out maximum value of photocurrent in one period
#     envelope_photocurrent_p4_list.append(max_photocurrent_p4) #puts maximum photocurrent in list
#     index_p4 = shortened_photocurrent_p4_list.index(max_photocurrent_p4) # gets the index corresponding to the selected photocurrent
#     envelope_frequency_p4_list.append(shortened_frequency_p4_list[index_p4])
#
#     start_4 += period_4
#     end_4 += period_4
#     # # for average of plot2 and plot3
#     # shortened_average_photocurrent_list = average_photocurrent_list[start:end]
#     # shortened_average_frequency_list = average_frequency_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
#     # max_average_photocurrent = np.amax(average_photocurrent[start:end]) #picks out maximum value of photocurrent in one period
#     # envelope_average_photocurrent_list.append(max_average_photocurrent) #puts maximum photocurrent in list
#     # index = shortened_average_photocurrent_list.index(max_average_photocurrent) # gets the index corresponding to the selected photocurrent
#     # envelope_average_frequency_list.append(shortened_average_frequency_list[index])
#
#
# for value in envelope_photocurrent_p1_list:
#     new_value = 20*np.log10(value)
#     log_envelope_photocurrent_p1_list.append(new_value)
#
# # for value in envelope_average_photocurrent_list:
# #     new_value = 20*np.log10(value)
# #     log_envelope_average_photocurrent_list.append(new_value)
#
# for value1, value2 in zip(envelope_photocurrent_p2_list,envelope_photocurrent_p3_list): # the zip() takes two list and iterate them simultaneously
#     average_value = (value1+value2)*0.5
#     log_average_value = 20*np.log10(average_value)
#     log_envelope_average_photocurrent_list.append(log_average_value)
#
# for value in envelope_photocurrent_p4_list:
#     new_value = 20*np.log10(value)
#     log_envelope_photocurrent_p4_list.append(new_value)
#
# print len(log_envelope_average_photocurrent_list), len(envelope_average_frequency_list)
#
# # plot of envelope photocurrent
# print 'test'
plt.figure()
plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
plt.xlabel("Frequency $GHz$")
plt.ylabel("Photocurrent $nA$")

plt.plot(Comparison_Function("water",0.6,25)[0], Comparison_Function("water",0.6,25)[1], label = 'Water Run 1', color = 'b')
plt.plot(Comparison_Function("leaf",0.2,24)[0], Comparison_Function("leaf",0.2,24)[1], label = 'Leaf Run 1', color = 'g')
# plt.plot(envelope_frequency_p2_list, log_envelope_average_photocurrent_list, label = 'Average of Reference Run', color = 'r')
# plt.plot(envelope_frequency_p1_list, log_envelope_photocurrent_p1_list, label = 'Leaf Run 1', color = 'g')
plt.legend()
plt.show()
#
