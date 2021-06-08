#!/usr/bin/env python3

"""
1. Go to:

https://usage.dteenergy.com/?interval=hour

2. Get link

3. Run:
python dtefeed.py https://usagedata.dteenergy.com/link/5E7B7FCB-D720-F3BB-BCC1-4AEA54F58DAC
"""

import datetime
import click
import requests
import matplotlib.pyplot as plt

import pandas as pd

import greenbutton as gb
import io

x = []
y = []


@click.command()
@click.argument('uri')
def main(uri):
    """
    Will plot data from DTE Energy XML feed
    :param uri: URL for sharing from usage.dteenergy.com
    """

    r = requests.get(uri)

    with io.BytesIO(r.content) as ramfile:
        df = gb.dataframe_from_xml(ramfile)

    # Plot last x hours
    hours = 48
    latest = df[df['Start Time'] >= (pd.to_datetime("today") - pd.Timedelta(hours=hours))]
    print(latest)
    latest.plot(x='Start Time', y='Wh')
    plt.title('Last ' + str(hours) + ' hours')
    plt.show()

    # Plot daily use
    df_use_by_day = df.groupby(lambda xa: df['Start Time'].loc[xa].date()).sum()
    plt.plot(df_use_by_day.Wh)
    plt.grid()
    plt.ylabel("Wh")
    plt.title("Daily use")
    plt.show()

    # Plot nightly use (23:00 to 5:00)
    df_night_use = gb.filter_by_time_of_day(df, datetime.time(23, 0), datetime.time(5, 0))
    df_night_use_by_day = df_night_use.groupby(lambda x: df_night_use['Start Time'].loc[x].date()).sum()
    plt.plot(df_night_use_by_day.Wh)
    plt.grid()
    plt.ylabel("Wh")
    plt.title("23:00 to 5:00 use")
    plt.show()
    #
    # Boxplot to show distribution in hourly use across all data
    gb.boxplot_use_by_hour(df)
    plt.ylabel("Wh")
    plt.title("Average daily use by hour")
    plt.show()


if __name__ == '__main__':
    main()
