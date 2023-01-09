# Creates the data visualisations
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from pathlib import Path


# creates a monthly summary
def create_month_summaries(dir):
    # If the month/year is complete and no summary exists
    # then create one if it doesn't exist
    date = datetime.now()

    for root, dirs, files in os.walk(dir):
        if not dirs:
            summary_name = f'{root}-summary.csv.gz'
            print(f'{root} is a leaf')
            print(date.date().strftime("%b"))
            
            # If it's the current month then update the extant summary
            if summary_name in files and date.date().strftime("%b") is root:
                print("Updating summary")
            else:
                print("Creating summary")


    # else create one for where we are now


def create_year_summaries(dir):
    # Average of all monthly summaries
    pass


# Create an overall summary or summaries
def create_overall_summary():
    pass


# Creates a chart from agiven df and saves the rendering of it
def render_time_series_chart(file_name):
    
    df = pd.read_csv(file_name)

    # Add a new column for journey time in minutes
    df['duration_mins'] = df['duration']/60
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    #df['timestamp'] = df['timestamp'].apply( lambda t : t.time())

    df.drop(['origin_address', 'destination_address'], axis=1, inplace=True)
    df.drop(['origin_lat', 'orign_long'], axis=1, inplace=True)
    df.drop(['destination_lat', 'destination_long'], axis=1, inplace=True)
    df.drop(['duration', 'distance'], axis=1, inplace=True)
    #df.set_index('timestamp', inplace=True)

    # Create frames for each journey type
    h2w = df.loc[(df['origin'] == 'Hamble') & (df['mode'] == 'driving')]
    w2h = df.loc[(df['origin'] == 'Windhover') & (df['mode'] == 'driving')]

    h2w.set_index('timestamp', inplace=True)
    w2h.set_index('timestamp', inplace=True)

    plt.figure(figsize=[16,7])
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

    h2w_label = "Hamble to Windhover"
    w2h_label = "Windhover to Hamble"

    plt.plot(h2w['duration_mins'], linestyle="-", color="green", label=f'{h2w_label} actuals')
    plt.plot(w2h['duration_mins'], linestyle="-", color="blue", label=f'{w2h_label} actuals')

    # Daily average
    plt.axhline(y=6, linestyle=":", color='red', label=f'i-Transport reported average') # Cemex/i-Transport average
    plt.axhline(y=h2w['duration_mins'].mean(), linestyle=':', color='green', label=f'{h2w_label} full day average')
    plt.axhline(y=w2h['duration_mins'].mean(), linestyle=':', color='blue', label=f'{w2h_label} full day average')

    # Actual avarages when most people are out and about
    #time_range = pd.date_range('06:00:00', '22:00:00', freq='H')
    start_time = '06:00:00'
    end_time = '19:00:00'
    #print(h2w.set_index('timestamp').between_time(start_time, end_time).mean()['duration_mins'])

    plt.axhline(
        y=h2w.between_time(start_time, end_time).mean()['duration_mins'], 
        linestyle="-.", color="green", label=f'{h2w_label} observed average')

    plt.axhline(
        y=w2h.between_time(start_time, end_time).mean()['duration_mins'], 
        linestyle="-.", color="blue", label=f'{w2h_label} observed average')
    
    plt.title(f'Journey times beteen {df["origin"].unique()[0]} and {df["origin"].unique()[1]} for {os.path.basename(file_name).split(".")[0]}')
    plt.xlabel('Time')
    plt.ylabel('Duration (minutes)')
    plt.legend()
    plt.grid()
    plt.legend(facecolor='lightgrey', framealpha=1)
    plt.gca().set_ylim(ymin=0)

    # Save it to the figure
    # Get the date parts to save it
    # TODO: Check this work for summaries
    date = datetime.strptime(os.path.basename(file_name).split('.')[0], '%Y-%m-%d')
    year = date.strftime('%Y')
    month = date.strftime('%b')
    file_name = f'{str(date.date())}-ts.jpg'

    file_handle = Path('graphs/', year, month, file_name)
    file_handle.parent.mkdir(exist_ok=True, parents=True)

    plt.savefig(file_handle, bbox_inches='tight', dpi=150)
    #plt.show()

def main():

    create_month_summaries('data/')
    create_year_summaries('data/')

if __name__ == '__main__':
    main()
