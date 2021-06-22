#!/usr/bin/env python3

"""
1. Go to:

https://usage.dteenergy.com/?interval=hour

2. Get link

3. Run:
python dtefeed.py --hours 48 --hdist https://usagedata.dteenergy.com/link/5E7B7FCB-D720-F3BB-BCC1-4AEA54F58DAC
"""

import datetime
import io

import click
import matplotlib.pyplot as plt
import pandas as pd
import requests

import greenbutton as gb

x = []
y = []


@click.command()
@click.argument('uri')
@click.option('-h', '--hours', type=int)
@click.option('--days', type=int)
@click.option('--hdist', default=False, is_flag=True)
@click.option('--night', default=False, is_flag=True)
@click.option('-d', '--debug', default=False, is_flag=True)
def main(uri, hours, debug=False, hdist=False, night=False, days=365):
    """
    Will plot data from DTE Energy XML feed
    :param uri: URL for sharing from usage.dteenergy.com
    :param hours: Get data for last x hours
    :param days: Get data for last x days
    :param hdist: Hourly distribution
    :param night: Night hourly distribution
    :param debug: Debug mode
    """

    session = requests.Session()
    r = session.get(uri)

    # Global canvas size in inches: Width, Height
    plt.rcParams['figure.figsize'] = 15, 6

    if debug:
        print('Data received from', uri, 'took', r.elapsed)

    with io.BytesIO(r.content) as ramfile:
        df = gb.dataframe_from_xml(ramfile)
        dfi = df.set_index(pd.DatetimeIndex(df['Start Time']))  # Indexed version
        # df['Start Time'] = pd.to_datetime(df['Start Time'])
        if debug:
            print(df.info(verbose=True))

    # Plot last x hours
    if hours and hours > 0:
        latest = dfi.copy()
        latest['Start Time'] = latest['Start Time'].dt.tz_localize('utc').dt.tz_convert('US/Eastern')
        latest = latest[latest['Start Time'] >= (pd.Timestamp.now(tz='US/Eastern') - pd.Timedelta(hours=hours))]
        print('Last', hours, 'records requested but', len(latest.index), 'found')
        print('Data availability for current day may be delayed')
        print(latest)
        latest.plot(x='Start Time', y='Wh')
        plt.title('Last ' + str(hours) + ' hours')
        plt.show()

    # Plot daily use

    if days and days > 0:
        hours = days * 24
        latest = dfi.copy()
        latest['Start Time'] = latest['Start Time'].dt.tz_localize('utc').dt.tz_convert('US/Eastern')
        latest = latest[latest['Start Time'] >= (pd.Timestamp.now(tz='US/Eastern') - pd.Timedelta(hours=hours))]
        print('Last', hours, 'records requested but', len(latest.index), 'found')
        print('Data availability for current day may be delayed')
        df_use_by_day = latest.groupby(lambda xa: latest['Start Time'].loc[xa].date()).sum()
        # plt.plot(df_use_by_day.Wh)
        plt.bar(df_use_by_day.Wh.index, df_use_by_day.Wh)
        # plt.grid()
        plt.ylabel("Wh")
        plt.title("Daily use")
        plt.show()

    # Plot nightly use (23:00 to 5:00)
    if night:
        df_night_use = gb.filter_by_time_of_day(dfi, datetime.time(23, 0), datetime.time(5, 0))
        df_night_use_by_day = df_night_use.groupby(lambda xa: df_night_use['Start Time'].loc[xa].date()).sum()
        plt.plot(df_night_use_by_day.Wh)
        # plt.grid()
        plt.ylabel("Wh")
        plt.title("23:00 to 5:00 use")
        plt.show()

    # Boxplot to show distribution in hourly use across all data
    if hdist:
        gb.boxplot_use_by_hour(df)
        plt.ylabel("Wh")
        plt.title("Average daily use by hour")
        plt.show()


if __name__ == '__main__':
    main()
