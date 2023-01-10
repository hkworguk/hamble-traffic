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

def create_daily_charts(dir):

    for file in Path(dir).rglob('*.csv.gz'):

        date = datetime.strptime(os.path.basename(file).split('.')[0], '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%b')

        fig_file_name = f'{str(date.date())}-ts.jpg'

        file_handle = Path('graphs/', year, month, fig_file_name)
        file_handle.parent.mkdir(exist_ok=True, parents=True)

        if not os.path.isfile(file_handle) or (os.path.isfile(file_handle) and datetime.now().date() == date.date()):
            render_time_series_chart(file, file_handle)
        #else:
        #    print(f"Fig exists, skipping {file_handle}")

# Creates a chart from agiven df and saves the rendering of it
def render_time_series_chart(file_name, fig_file_handle):
    
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
    # Cemex/i-Transport average based on 34mph average speed on Hamble lane...?
    # Google api/distanceMatrix has distance 5606m duration 626s = 8.955 m/s = 20mph without traffic
    plt.axhline(y=6, linestyle=":", color='red', label=f'i-Transport reported average') 
    plt.axhline(y=h2w['duration_mins'].mean(), linestyle=':', color='green', label=f'{h2w_label} full day average')
    plt.axhline(y=w2h['duration_mins'].mean(), linestyle=':', color='blue', label=f'{w2h_label} full day average')

    # Actual avarages when most people are out and about and observe delays
    start_time = '06:00:00'
    end_time = '19:00:00'

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

    plt.savefig(fig_file_handle, bbox_inches='tight', dpi=150)
    #plt.show()

def main():

    DATA_DIR = 'data/'
    #create_month_summaries(DATA_DIR)
    #create_year_summaries(DATA_DIR)
    
    print('Generating Visuals')
    create_daily_charts(DATA_DIR)
    print('Visual Generation Complete')

if __name__ == '__main__':
    main()
