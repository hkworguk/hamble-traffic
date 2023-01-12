# Creates the data visualisations
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from pathlib import Path
import statistics

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

# Average of all monthly summaries
def create_year_summaries(dir):
    pass


# Create an overall summary or summaries
def create_overall_summary():
    pass

def create_daily_charts(dir):

    for df_file in Path(dir).rglob('*.csv.gz'):
        render_time_series_chart(df_file,  'Hamble', 'Windhover', [('06:00:00', '19:00:00')])
        render_time_series_chart(df_file,  'Hound', 'Mallards', [('07:00:00', '09:00:00'), ('02:00:00', '04:00:00')])

# Creates a chart from agiven df and saves the rendering of it
def render_time_series_chart(df_file_name, origin, dest, time_groups=None):
    
    date = datetime.strptime(os.path.basename(df_file_name).split('.')[0], '%Y-%m-%d')

    fig_name = f'{origin}-{dest}-{str(date.date())}-ts.jpg'

    year = date.strftime('%Y')
    month = date.strftime('%b')
    
    fig_file_handle = Path('graphs/', year, month, fig_name)
    fig_file_handle.parent.mkdir(exist_ok=True, parents=True)
    
    if not os.path.isfile(fig_file_handle) or (os.path.isfile(fig_file_handle) and datetime.now().date() == date.date()):
        
        df = pd.read_csv(df_file_name)

        # Add a new column for journey time in minutes
        df['duration_mins'] = df['duration']/60
        # Add in speed/velocity
        df['speed'] = df['distance']/df['duration']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        #df['timestamp'] = df['timestamp'].apply( lambda t : t.time())

        df.drop(['origin_address', 'destination_address'], axis=1, inplace=True)
        df.drop(['origin_lat', 'orign_long'], axis=1, inplace=True)
        df.drop(['destination_lat', 'destination_long'], axis=1, inplace=True)
        #df.drop(['duration', 'distance'], axis=1, inplace=True)
        #df.set_index('timestamp', inplace=True)

        # Create frames for each journey type
        o2d = df.loc[(df['origin'] == origin) & (df['mode'] == 'driving')]
        d2o = df.loc[(df['origin'] == dest) & (df['mode'] == 'driving')]

        if len(o2d.index) == 0 or len(d2o.index) == 0: return

        o2d.set_index('timestamp', inplace=True)
        d2o.set_index('timestamp', inplace=True)

        plt.figure(figsize=[16,7])
        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

        o2d_label = f"{origin} to {dest}"
        d20_label = f"{dest} to {origin}"

        plt.plot(o2d['duration_mins'], linestyle='solid', color="green", label=f'{o2d_label} actuals')
        plt.plot(d2o['duration_mins'], linestyle='solid', color="blue", label=f'{d20_label} actuals')

        # Daily average
        # Cemex/i-Transport average based on 34mph average speed on Hamble lane...?
        # Google api/distanceMatrix distance average by Cemex speed average 34mph
        REPORTED_MEAN_SPEED = 15.1994 # m/s

        report_average_mins = (statistics.fmean([o2d['distance'].mean(), d2o['distance'].mean()])/REPORTED_MEAN_SPEED) / 60.0
 
        #print(report_average_mins)

        plt.axhline(y=report_average_mins, linestyle="dotted", color='red', label=f'Cemex/i-Transport reported average') 
        plt.axhline(y=o2d['duration_mins'].mean(), linestyle='dotted', color='green', label=f'{o2d_label} full day average')
        plt.axhline(y=d2o['duration_mins'].mean(), linestyle='dotted', color='blue', label=f'{d20_label} full day average')

        # Actual avarages when most people are out and about and observe delays
        line_styles = ['dashed', 'dashdot']
        # TODO: Add on average speeds m/s to mph

        for index, (start_time, end_time) in enumerate(time_groups):
            if start_time is not None and end_time is not None:
                plt.axhline(
                    y=o2d.between_time(start_time, end_time).mean(numeric_only=True)['duration_mins'], 
                    linestyle=line_styles[index], color="green", label=f'{o2d_label} average {start_time} and {end_time}')

                plt.axhline(
                    y=d2o.between_time(start_time, end_time).mean(numeric_only=True)['duration_mins'], 
                    linestyle=line_styles[index], color="blue", label=f'{d20_label} average {start_time} and {end_time}')
        
        plt.title(f'Journey times beteen {origin} and {dest} for {date.date()}')
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
