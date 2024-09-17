import pandas as pd
# import plotly.graph_objs as go
import plotly.express as px


def plot_util(fnd,mind,maxd):
    # Step 1: Load the CSV data into a DataFrame
    directory = r'R:/PE/DATA/' #remove leading /
    df = pd.read_csv(fnd)

    # Create a pivot table to aggregate Time_Difference_Hours per location per recipe
    df_pivot = df.pivot_table(values='Time_Difference_Hours', index='Location', columns='recipe', aggfunc='sum', fill_value=0)
    #print(df_pivot)
    # Normalize the pivot table to make it 100% stacked
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100
    #print(df_pivot_percentage)
    # quit()
    # Create the 100% stacked bar chart
    fig = px.bar(df_pivot_percentage, 
                x=df_pivot_percentage.index, 
                y=df_pivot_percentage.columns, 
                title="ATP Utilization: "+mind.strftime('%m-%d-%Y')+' to '+maxd.strftime('%m-%d-%Y'), 
                labels={"value": "Percentage (%)", "Location": "Location", "recipe": "Recipe"},
                height=600)

    # Update layout for better appearance
    fig.update_layout(barmode='stack', yaxis_title='Percentage (%)')

    # Show the plot
    # fig.show()
    fig.write_html(r'R:/PE/REPORTS/ATP/utilization.html')