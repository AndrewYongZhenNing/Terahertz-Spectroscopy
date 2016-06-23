import numpy as np
import matplotlib.pyplot as plt

plot = np.loadtxt("leaf.dat")
frequency = plot[1:,1]
photocurrent = plot[1:,2]+ 0.2 #+0.4 #shifts the graph to be minimally symmetric at y=0, 0.2 for leaf
#
# direct plot

# plt.figure()
# plt.xlim(50,1550)
# # plt.ylim(0,80)
# plt.title("Plot of Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
# plt.xlabel("Frequency $GHz$")
# plt.ylabel("Photocurrent $nA$")
# plt.plot(frequency,photocurrent)
# plt.show()

start = 0
end = 24 # start and end of a period
period = 24 #0.04
photocurrent_list = []
frequency_list = []
envelope_photocurrent_list = []
envelope_frequency_list = []
log_envelope_photocurrent_list = []

for value in photocurrent: #converts array to list [for no  w]
    photocurrent_list.append(value)

for value in frequency:
    frequency_list.append(value)

while start < 48306 and end < 48334:
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

# print envelope_photocurrent_list[400],envelope_photocurrent_list[600], log_envelope_photocurrent_list[400:600] #envelope_frequency_list[700:800]


# plot of envelope photocurrent

plt.figure()
# plt.xlim(0,1600)
# plt.ylim(0,70)
plt.title("Logarithmic Plot of Envelope Tetrahertz Photocurrent(nA) vs Frequency(GHz)")
plt.xlabel("Frequency $GHz$")
plt.ylabel("Photocurrent $nA$")
plt.plot(envelope_frequency_list, log_envelope_photocurrent_list, color = 'g')
# plt.plot(frequency_list, photocurrent_list, color = 'g')
plt.show()
