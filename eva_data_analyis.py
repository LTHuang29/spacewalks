import matplotlib.pyplot as plt
import pandas as pd

# https://data.nasa.gov/resource/eva.json (with modifications)

def read_json_to_dataframe(input_file):
    """
    read_json_to_dataframe reads data from a JSON file and converts it into a cleaned Pandas DataFrame.

    Args:
        input_file (json): The path to the input JSON file.

    Returns:
        eva_df: The cleaned and processed Pandas DataFrame.
    """
    print("Reading data from JSON file {input_file}")
    #read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    #Clean the data by removing any rows where duration is missing or date is missing
    eva_df.dropna( axis=0, subset=['duration','date'], inplace=True)
    return eva_df

def write_dataframe_to_csv(df, output_file):
    """
    write the given Pandas DataFrame to a CSV file for later analysis.

    Args:
        df (pd.DataFrame): The Pandas DataFrame to be saved.
        output_file (str): The path to the output CSV file.
    """
    print(f'Saving to CSV file {output_file}')
    #save dataframe to CSV file for later analysis
    df.to_csv(output_file, index=False, encoding='utf-8')

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/6  # there is an intentional bug on this line (should divide by 60 not 6)
    return duration_hours


def add_duration_hours(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy

def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot the cumulative time spent in space over years.

    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Generate a plot of cumulative time spent in space over years and
    save it to the specified location

    Args:
        df (pd.DataFrame): The input dataframe.
        graph_file (file or str): The file object or path to the output graph file.

    Returns:
        None
    """
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    df = add_duration_hours(df)
    df['cumulative_time'] = df['duration_hours'].cumsum()
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def main(input_file, output_file, graph_file):
    print("--Start--")
    input_file= open(input_file, 'r', encoding='ascii')
    output_file = open(output_file,'w', encoding='utf-8')
    graph_file = graph_file
    #read the data from JSON file
    eva_df = read_json_to_dataframe(input_file)
    #save the data to CSV file for later analysis
    write_dataframe_to_csv(eva_df, output_file)
    #sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_df.sort_values('date', inplace=True)

    #plot cumulative time spent in space over years
    plot_cumulative_time_in_space(eva_df, graph_file)
    print("--END--")

if __name__ == "__main__":

    input_file = './eva_data.json'
    output_file = './eva_data.csv'
    graph_file = './cumulative_eva_graph.png'
    main(input_file, output_file, graph_file)