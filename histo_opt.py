"""
This script animates a histogram that reads data from a file and dynamically updates it. 
The histogram's properties such as the number of bins, color, and range can be configured 
using command-line arguments.

Inputs:
  - file: The path to the CSV file containing the data.


Example Usage:

python3 histo_opt.py MeasurementLog2024912.csv & 

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse


def read_data(filePath,data):
      # Initialize an empty list to store the data
    try:
        with open(filePath, 'r') as fhand:
            i = 0  # Counter to skip the first line (header)
            for i,line in enumerate(fhand):
                if i == 0 or i<len(data):  # Skip the first line
                    continue
                info = line.split(',')
                if len(info) > 1:
                    try:
                        
                        data.append(float(info[1]))  # Append the data from the second column
                    except ValueError:
                        continue  # Skip lines that cannot be converted to float
    except (FileNotFoundError, IOError):
        print(f"Error: The file '{filePath}' could not be found or opened.")
        sys.exit(1)  # Exit the script with an error code



class DynamicHistogramApp(QMainWindow):
    def __init__(self,file_path):
        super().__init__()
        
        self.data = []
        
        self.setWindowTitle("Dynamic Histogram")
        self.setGeometry(100, 100, 800, 600)

        # Enable resizing
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create a FigureCanvas (matplotlib widget for PyQt)
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a layout for control buttons
        controls_layout = QHBoxLayout()

        # File input 
        self.file_input = file_path

        # Max range input field
        self.max_range_input = QLineEdit(self)
        self.max_range_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.max_range_input.setPlaceholderText("Enter Max Range (e.g., 1500000)")
        controls_layout.addWidget(self.max_range_input)

        # Min range input field
        self.min_range_input = QLineEdit(self)
        self.min_range_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.min_range_input.setPlaceholderText("Enter Min Range (e.g., 0)")
        controls_layout.addWidget(self.min_range_input)

        # Number of bins input field
        self.bins_input = QLineEdit(self)
        self.bins_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.bins_input.setPlaceholderText("Enter Number of Bins (e.g., 20)")
        controls_layout.addWidget(self.bins_input)

        # Color input field
        self.color_input = QLineEdit(self)
        self.color_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.color_input.setPlaceholderText("Enter Color (e.g., b, g, r)")
        controls_layout.addWidget(self.color_input)

        # Button to update the histogram
        self.update_button = QPushButton("Update Histogram", self)
        self.update_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.update_button.clicked.connect(self.update_histogram)
        controls_layout.addWidget(self.update_button)

        # Add the controls layout to the main layout
        layout.addLayout(controls_layout)

        self.status_label = QLabel(self)
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.status_label)
        
        # Setup QTimer to update the histogram every 10 seconds (10000 milliseconds)
        self.update_histogram()
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # 10 seconds
        self.timer.timeout.connect(self.update_histogram)
        self.timer.start()  # Start the timer


    def update_histogram(self):
        """
        Update the histogram plot based on the user inputs.
        """
        max_range = float(self.max_range_input.text()) if self.max_range_input.text() else 1500000
        min_range = float(self.min_range_input.text()) if self.min_range_input.text() else 0
        bins = int(self.bins_input.text()) if self.bins_input.text() else 20
        color = self.color_input.text() if self.color_input.text() else 'b'
        
        # Read new data
        read_data(self.file_input, self.data)

        # Plot the histogram
        self.ax.clear()
        n, bin_edges, patches = self.ax.hist(self.data, bins=bins, color=color, range=(min_range, max_range), rwidth=0.7, histtype='bar')

        self.ax.set_xlabel('Value', fontsize=15)
        self.ax.set_ylabel('Frequency', fontsize=15)

        # Add a legend with the label 'Histogram'
        for patch in patches:
            patch.set_label('Histogram')  # Explicitly set the label for each bar
            break
        self.ax.legend(loc='best', fontsize=12)

        # Set the x-axis ticks and labels
        self.ax.set_xticks(bin_edges[:-1])  # bin_edges contains the edges of the bins
        self.ax.set_xticklabels([f'{int(x)}' for x in bin_edges[:-1]], rotation=70)

        # Add value labels if required
        for b, v in zip(bin_edges[:-1], n):
            if v > 0:
                self.ax.text(b + (bin_edges[1] - bin_edges[0]) / 2, v, f'{int(v)}', ha='center', va='bottom', fontsize=7, fontweight='bold')

        self.status_label.setText(f"Updated histogram for {len(self.data)} entries.")
        self.canvas.draw()




def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Dynamic Histogram Plotter.")
    parser.add_argument('file', type=str, help="Path to the CSV file to read data from.")
    return parser.parse_args()

def main():
    """
    Run the PyQt5 application.
    """
    args = parse_arguments()

    app = QApplication(sys.argv)
    window = DynamicHistogramApp(args.file)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
