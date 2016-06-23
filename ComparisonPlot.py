import numpy as np
import matplotlib.pyplot as plt

plot_1 = np.loadtxt("leaf.dat")
plot_2 = np.loadtxt("reference_scan2.dat")
plot_3 = np.loadtxt("reference_scan2.1.dat")
###
# vertical shift of the plot to make it symmettrical about x axis [DEFAULT = 0]
a = 0.2
b = 0.4
c = 0.4
####
frequency_p1 = plot_1[1:,1]
photocurrent_p1 = plot_1[1:,2]+ a #shifts the graph to be minimally symmetric at y=0

frequency_p2 = plot_2[:,1]
photocurrent_p2 = plot_2[:,2]+ b #shifts the graph to be minimally symmetric at y=0

frequency_p3 = plot_3[:,1]
photocurrent_p3 = plot_3[:,2]+ c #shifts the graph to be minimally symmetric at y=0

average_photocurrent = (photocurrent_p2+photocurrent_p3)/2
average_frequency = (frequency_p2+frequency_p3)/2


start = 0
end = 24 # start and end of a period
period = 24

photocurrent_p1_list = []
frequency_p1_list = []
envelope_photocurrent_p1_list = []
envelope_frequency_p1_list = []
log_envelope_photocurrent_p1_list = []

photocurrent_p2_list = []
frequency_p2_list = []
envelope_photocurrent_p2_list = []
envelope_frequency_p2_list = []
log_envelope_photocurrent_p2_list = []

photocurrent_p3_list = []
frequency_p3_list = []
envelope_photocurrent_p3_list = []
envelope_frequency_p3_list = []
log_envelope_photocurrent_p3_list = []

average_photocurrent_list = []
average_frequency_list = []
envelope_average_photocurrent_list = []
envelope_average_frequency_list = []
log_envelope_average_photocurrent_list = []


for value in photocurrent_p1: #converts array to list [for now]
    photocurrent_p1_list.append(value)

for value in frequency_p1:
    frequency_p1_list.append(value)

for value in photocurrent_p2: #converts array to list [for now]
    photocurrent_p2_list.append(value)

for value in frequency_p2:
    frequency_p2_list.append(value)

for value in photocurrent_p3: #converts array to list [for now]
    photocurrent_p3_list.append(value)

for value in frequency_p3:
    frequency_p3_list.append(value)


# for value in average_photocurrent: #converts array to list [for now]
#     average_photocurrent_list.append(value)
#
# for value in average_frequency:
#     average_frequency_list.append(value)

while start < 48291 and end < 48334:
    # for plot #1
    shortened_photocurrent_p1_list = photocurrent_p1_list[start:end]
    shortened_frequency_p1_list = frequency_p1_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
    max_photocurrent_p1 = np.amax(photocurrent_p1[start:end]) #picks out maximum value of photocurrent in one period
    envelope_photocurrent_p1_list.append(max_photocurrent_p1) #puts maximum photocurrent in list
    index_p1 = shortened_photocurrent_p1_list.index(max_photocurrent_p1) # gets the index corresponding to the selected photocurrent
    envelope_frequency_p1_list.append(shortened_frequency_p1_list[index_p1])

    # for plot #2
    shortened_photocurrent_p2_list = photocurrent_p2_list[start:end]
    shortened_frequency_p2_list = frequency_p2_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
    max_photocurrent_p2 = np.amax(photocurrent_p2[start:end]) #picks out maximum value of photocurrent in one period
    envelope_photocurrent_p2_list.append(max_photocurrent_p2) #puts maximum photocurrent in list
    index_p2 = shortened_photocurrent_p2_list.index(max_photocurrent_p2) # gets the index corresponding to the selected photocurrent
    envelope_frequency_p2_list.append(shortened_frequency_p2_list[index_p2])

    # for plot #3
    shortened_photocurrent_p3_list = photocurrent_p3_list[start:end]
    shortened_frequency_p3_list = frequency_p3_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
    max_photocurrent_p3 = np.amax(photocurrent_p3[start:end]) #picks out maximum value of photocurrent in one period
    envelope_photocurrent_p3_list.append(max_photocurrent_p3) #puts maximum photocurrent in list
    index_p3 = shortened_photocurrent_p3_list.index(max_photocurrent_p3) # gets the index corresponding to the selected photocurrent
    envelope_frequency_p3_list.append(shortened_frequency_p3_list[index_p3])

    # # for average of plot2 and plot3
    # shortened_average_photocurrent_list = average_photocurrent_list[start:end]
    # shortened_average_frequency_list = average_frequency_list[start:end] # shortened list helps to select the right photocurrent and frequency WITHIN the start and end boundaries
    # max_average_photocurrent = np.amax(average_photocurrent[start:end]) #picks out maximum value of photocurrent in one period
    # envelope_average_photocurrent_list.append(max_average_photocurrent) #puts maximum photocurrent in list
    # index = shortened_average_photocurrent_list.index(max_average_photocurrent) # gets the index corresponding to the selected photocurrent
    # envelope_average_frequency_list.append(shortened_average_frequency_list[index])

    start += period
    end += period

for value in envelope_photocurrent_p1_list:
    new_value = 20*np.log10(value)
    log_envelope_photocurrent_p1_list.append(new_value)

# for value in envelope_average_photocurrent_list:
#     new_value = 20*np.log10(value)
#     log_envelope_average_photocurrent_list.append(new_value)

for value1, value2 in zip(envelope_photocurrent_p2_list,envelope_photocurrent_p3_list): # the zip() takes two list and iterate them simultaneously
    average_value = (value1+value2)*0.5
    log_average_value = 20*np.log10(average_value)
    log_envelope_average_photocurrent_list.append(log_average_value)

print len(log_envelope_average_photocurrent_list), len(envelope_average_frequency_list)
# print 'average = ', envelope_average_photocurrent_list[95:105]
# print 'run 2 = ', envelope_photocurrent_p2_list[95:105]
# print 'run 3 = ', envelope_photocurrent_p3_list[95:105]
# print 'log =', log_envelope_average_photocurrent_list[95:105]


# plot of envelope photocurrent

plt.figure()
# plt.xlim(550,570)
plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
plt.xlabel("Frequency $GHz$")
plt.ylabel("Photocurrent $nA$")
plt.plot(envelope_frequency_p2_list, log_envelope_average_photocurrent_list, label = 'Average of 2nd Run', color = 'r')
# plt.plot(envelope_frequency_p1_list, log_envelope_photocurrent_p1_list, label = 'Leaf Run 1', color = 'g')
plt.legend()
plt.show()
