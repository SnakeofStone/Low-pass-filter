import csv
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import angle

# Constants
X = 0
Y = 1

# Load values from the csv file and store them in two different lists, one
# for each axis
with open('Datapoints.csv', 'r', newline='') as datapoints_file:
    csv_reader = csv.reader(datapoints_file, delimiter=',')
    x_angle = []
    y_angle = []
    for row in csv_reader:
        x_angle.append(int(row[0]))
        y_angle.append(int(row[1]))

# Convert to numpy matrix
angles = np.array([x_angle, y_angle])
#angles = angles[:, :50]    # Get a slice from the matrix for testing

# Compute the mean of each axis
mean = np.array([
    1/angles[X].size * np.sum(angles[X]),
    1/angles[Y].size * np.sum(angles[Y])
])
mean = np.around(mean, decimals=2)

# Compute the standard deviation
sigma = np.array([
    1/(angles[X].size - 1) * np.sum((angles[X] - mean[X])**2),
    1/(angles[Y].size - 1) * np.sum((angles[Y] - mean[Y])**2)
])
sigma = np.sqrt(sigma)
sigma = np.around(sigma, decimals=2)

# Apply low pass filter to signals
delta_t = 1e-3
filtered = np.zeros(angles.shape)

alfa = 0.3

filtered[:, 0] = alfa * angles[:, 0]            # Store first value of each
                                                # axis multiplied by alfa

for i in range(1, angles.shape[1]):             # Low-pass filter
    filtered[:, i] = alfa * angles[:, i] + (1 - alfa) * filtered[:, i-1]

# Compute mean and sigma of filtered signals
filtered_mean = np.array([
    1/filtered[X].size * np.sum(filtered[X]),
    1/filtered[Y].size * np.sum(filtered[Y])
])
filtered_mean = np.around(mean, decimals=2)

# Compute the standard deviation
filtered_sigma = np.array([
    1/(filtered[X].size - 1) * np.sum((filtered[X] - filtered_mean[X])**2),
    1/(filtered[Y].size - 1) * np.sum((filtered[Y] - filtered_mean[Y])**2)
])
filtered_sigma = np.sqrt(filtered_sigma)
filtered_sigma = np.around(filtered_sigma, decimals=2)


# Plot the data
def plot_data(angles, filtered):
    n = np.arange(0, len(angles[X]))

    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.plot(n, angles[X], linewidth=0.5, color="#14D7F4") #14D7F4 - Cyan
    ax1.plot(n, filtered[X], linewidth=0.5, color="#0673D6") #0673D6 - Dark blue
    ax1.legend(["Raw data: $\mu = {}, \sigma$ = {}".format(mean[X], sigma[X]),
                "Filtered data: $\mu = {}, \sigma$ = {}".format(filtered_mean[X], 
                                                                filtered_sigma[X])])
    ax1.set_xlabel("samples (n)")
    ax1.set_ylabel("x angle (deg)")
    ax1.grid(True)

    ax2.plot(n, angles[Y], linewidth=0.5, color="#4DC105") #0F8600 - Dark green; #4DC105 - Lime green
    ax2.plot(n, filtered[Y], linewidth=0.5, color="#0F8600")
    ax2.legend(["Raw data: $\mu = {}, \sigma$ = {}".format(mean[Y], sigma[Y]),
                "Filtered data: $\mu = {}, \sigma$ = {}".format(filtered_mean[Y], 
                                                                filtered_sigma[Y])])
    ax2.set_xlabel("samples (n)")
    ax2.set_ylabel("y angle (deg)")
    ax2.grid(True)

    plt.show()

plot_data(angles, filtered)
