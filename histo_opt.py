"""
This script animates a histogram that reads data from a file and dynamically updates it. 
The histogram's properties such as the number of bins, color, and range can be configured 
using command-line arguments.

Inputs:
  - file: The path to the CSV file containing the data.
  - maxrange: Maximum range of the histogram (default: 1,500,000).
  - minrange: Minimum range of the histogram (default: 0).
  - binlength: Length of each bin (used if 'bins' is not specified, default: 0).
  - bins: Number of bins in the histogram (used if 'binlength' is not specified, default: 0).
  - color: Color of the histogram bins (default: 'b' for blue).
  - values: If 'true', displays the count of values in each bin (default: 'true').

Example Usage:

python3 histo_opt.py file=MeasurementLog2024912.csv maxrange=2000 minrange=0 bins=20 color=b values=true

"""

import matplotlib
matplotlib.use('TkAgg')  # Set to an interactive backend
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sys

def read_data(filePath):
    data = []  # Initialize an empty list to store the data
    try:
        with open(filePath, 'r') as fhand:
            i = 0  # Counter to skip the first line (header)
            for line in fhand:
                if i == 0:  # Skip the first line
                    i += 1
                    continue
                info = line.split(',')
                if (len(info) > 1):
                  try:
                      data.append(float(info[1]))  # Append the data from the second column
                  except ValueError:
                      continue  # Skip lines that cannot be converted to float
    except (FileNotFoundError, IOError):
        print(f"Error: The file '{filePath}' could not be found or opened.")
        display_help()  # Display help text if file is not found
        sys.exit(1)  # Exit the script with an error code
    return data

def plot_histogram(config):
    """
    Plots the histogram based on the provided configuration.
    Args:
    - config (dict): Configuration dictionary containing histogram settings.
    """
    data = read_data(config['file'])
    maxrange = config['maxrange']
    minrange = config['minrange']
    color = config['color']
    entries = len(data)

    # Determine number of bins and bin length
    if config['bins'] == 0 and config['binlength'] > 0:
        bin_length = config['binlength']
        nbins = int((maxrange - minrange) / bin_length)
    elif config['binlength'] == 0 and config['bins'] > 0:
        nbins = config['bins']
        bin_length = (maxrange - minrange) / nbins
    else:
        raise ValueError("Either the number of bins or the bin length must be specified.")

    # Plot the histogram
    plt.clf()  # Clear the figure to prepare for new plot
    values, bins, _ = plt.hist(data, bins=nbins, color=color, range=(minrange, maxrange), 
                               rwidth=0.7, histtype='bar', label=f'Entries: {entries}\nMax Range: {maxrange}\nMin Range: {minrange}\nBin Length: {bin_length}\nBins: {nbins}')
    
    plt.xlabel('Value', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.legend(loc='best', fontsize=12)
    plt.xticks(bins, rotation=70)

    if config['values'] == 'true':
        for b, v in zip(bins, values):
            if v > 0:
                plt.text(b + bin_length / 2, v, f'{int(v)}', ha='center', va='bottom', fontsize=7, fontweight='bold')

def draw_histogram(i, config):
    """
    Updates the histogram plot for animation.
    Args:
    - i (int): Frame index for animation.
    - config (dict): Configuration dictionary.
    """
    plot_histogram(config)

def parse_args():
    """
    Parses command-line arguments into a configuration dictionary.
    
    Returns:
    - config (dict): Configuration dictionary.
    """
    config = {
        'binlength': 0,
        'maxrange': 1500000.0,
        'minrange': 0,
        'color': 'b',
        'values': 'true',
        'bins': 0
    }

    # Parse command-line arguments
    for arg in sys.argv[1:]:
        try:
            key, value = arg.split('=')
            if key.lower() in ['binlength', 'maxrange', 'minrange']:
                config[key] = float(value)
            elif key.lower() in ['file', 'color', 'values']:
                config[key] = value
            elif key.lower() == 'bins':
                config[key] = int(value)
        except ValueError:
            print(__doc__)
            sys.exit(f"Invalid argument format: {arg}")

    return config

def main():
    """
    Main function to run the script.
    """
    config = parse_args()
    fig, ax = plt.subplots()
    fps = 120

    # Keep a reference to the animation
    ani = FuncAnimation(fig, draw_histogram, fargs=(config,), frames=fps, repeat=True)
    plt.show()

if __name__ == "__main__":
    main()
