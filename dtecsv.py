#!/usr/bin/env python3

"""
1. Go to:

https://usage.dteenergy.com/?interval=hour

2. Download CSV

3. Run:
python dtecsv.py .\electric_usage_report_05-31-2021_to_06-05-2021.csv
"""

import csv
import datetime

import click
import matplotlib.pyplot as plt

x = []
y = []


@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """
    Will plot data from DTE Energy CSV
    :param file: DTE CSV file
    """
    with open(file, 'r') as file:
        lines = csv.reader(file)
        next(lines)  # Skip first line that is header
        for row in lines:
            rawdate = row[1] + ' ' + row[2]  # 05/15/2021 11:00 AM
            # date = datetime.datetime.strptime(rawdate, "%m/%d/%Y %I:00 %p").strftime("%Y-%m-%d %H:00")
            date = datetime.datetime.strptime(rawdate, "%m/%d/%Y %I:00 %p").strftime("%b %d %H:00")
            x.append(date)
            y.append(float(row[3]))

    # Risize the figure (optional)
    plt.figure(figsize=(18, 9))

    # Plot the x and y values on the graph
    plt.plot(x, y)

    # Here you specify the ticks you want to display
    # You can also specify rotation for the tick labels in degrees or with keywords.
    plt.xticks(x[::2], rotation='vertical')

    # Add margins (padding) so that markers don't get clipped by the axes
    plt.margins(0.2)

    # Display the graph
    plt.show()


if __name__ == '__main__':
    main()
