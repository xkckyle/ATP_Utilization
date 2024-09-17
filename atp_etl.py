
import os
from datetime import datetime
import pandas as pd

def grab_dr():
    # Specify the directory you want to pull files from
    directory = 'temp/' #remove leading /

    # List to store CSV file names and their modification times
    csv_file_list = []

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Get the full file path
        file_path = os.path.join(directory, filename)

        # Check if it's a file and ends with '.csv'
        if os.path.isfile(file_path) and len(filename)>16:
            if(filename[:16]=='ATP Donor Report'):
                # Get the last modified time in seconds since the epoch
                mod_time = os.path.getmtime(file_path)
                # Convert the modification time to a human-readable format
                readable_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S') # '%m-%d-%Y %H:%M:%S'


                # if(filename.endswith('.csv')):
                    # Append the CSV file path and modification time to the list
                    # csv_file_list.append((file_path, readable_time))
                if(filename.endswith('.xlsx')):
                    # add to list of csv's
                    newn=file_path[:-4]+'csv' # don't change the name yet
                    csv_file_list.append((newn, readable_time)) # don't change the name yet
                    # xlsx
                    df = pd.read_excel(file_path, header=6)#, usecols='D:')
                    # fix
                    df = df.drop(df.columns[[0, 1, 6,7]], axis=1)
                    df.columns = df.columns.str.strip()
                    df.columns = df.columns.str.replace(' ', '_')
                    # add
                    # df.ffill((newn[16:-4], readable_time))
                    # export
                    df.to_csv(newn)
                    

    # quit()

    # Sort the list by the modification time (ascending)
    csv_file_list.sort(key=lambda x: x[1])

    # List to store DataFrames
    dataframes = []

    # Load each CSV into a DataFrame and add it to the list
    for fn, mod_time in csv_file_list:
        df = pd.read_csv(fn)  # Read the CSV file into a DataFrame

        #
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '_')
            
        # add
        df['recipe'] = os.path.basename(fn[22:-4])  # Add a column with the filename
        df['last_modified'] = mod_time  # Add a column with the modification time

        # Ensure the 'Start_Time' and 'End_Time' columns are in datetime format
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%Y-%m-%d %H:%M:%S') #''%m-%d-%Y %I:%M:%S %p'
        df['End_Time'] = pd.to_datetime(df['End_Time'], format='%Y-%m-%d %H:%M:%S')#'%m-%d-%Y %I:%M:%S %p')

        # Create a new column that calculates the time difference in hours
        df['Time_Difference_Hours'] = (round((df['End_Time'] - df['Start_Time']).dt.total_seconds() / 3600,2))

        dataframes.append(df)  # Append the DataFrame to the list

    # Concatenate all DataFrames into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Sort the combined DataFrame by the last modified date
    combined_df = combined_df.sort_values(by='last_modified', ascending=True)

    # export
    combined_df.to_csv('temp/ATP-DR-all.csv')

    # get DATE_RANGE
    mind = combined_df['Start_Time'].min(); print(mind)
    maxd = combined_df['Start_Time'].max(); print(maxd)
    DATE_RANGE = ((maxd-mind) / pd.Timedelta(hours=1))

    # Group by 'recipe' and 'Location' (renamed to 'event') and sum 'Time_Difference_Hours'
    summary_df = combined_df.groupby(['recipe', 'Location'], as_index=False)['Time_Difference_Hours'].sum().round(1)

    # Rename 'Location' to 'event'
    # summary_df.rename(columns={'Location': 'event'}, inplace=True)

    # quit()

    # Load the additional CSV files: 'holidays.csv' and 'shutdowns.csv'
    downtimes = pd.read_csv('config/downtimes.csv')
    print(downtimes)
    # append
    for l in summary_df['Location'].unique():
        #add downtimes recipe , Locaiton, Time_Difference_Hours
        for i,r in downtimes.iterrows():
            if(DATE_RANGE>300):
                summary_df.loc[len(summary_df)] = [r[1],l,r[2]]
            else:
                summary_df.loc[len(summary_df)] = [r[1],l,round(r[2]*(DATE_RANGE/(365*24)),1)]
                
        # add unused
        runt = summary_df[summary_df['Location']==l]['Time_Difference_Hours'].sum()
        unused = (DATE_RANGE)-runt
        summary_df.loc[len(summary_df)] = ['idle',l,unused]

    # export
    summary_df.to_csv('temp/atp-summ.csv') ; print('summary saved!')

    # Append the 'holidays.csv' and 'shutdowns.csv' DataFrames to the summary DataFrame
    # summary_df = pd.concat([summary_df, holidays_df, shutdowns_df], ignore_index=True)

    # Display the final summary table
    # print(summary_df)