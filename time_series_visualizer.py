import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df.index, df['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = [d.year for d in df_bar.index]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_bar['Months'] = pd.Categorical([d.strftime('%b') for d in df_bar.index], categories=months, ordered=True)
    df_bar = df_bar.groupby(['Years', 'Months'], sort=False)['value'].mean().round().unstack()

    # Draw bar plot
    ax = df_bar.plot.bar(figsize=(20, 10), rot=0, fontsize=20)
    fig = ax.get_figure()

    ax.set_xlabel('Years', fontdict={'size': 32})
    ax.set_ylabel('Average Page Views', fontdict={'size': 32})
    ax.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], title='Months', fontsize=20, title_fontsize='32')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box['month'] = pd.Categorical([d.strftime('%b') for d in df_box.date], categories=months, ordered=True)

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    sns.boxplot(data=df_box, x='year', y='value', hue="year", ax=ax1)
    sns.boxplot(data=df_box, x='month', y='value', hue="month", ax=ax2)
    plt.show(block=False)
    
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
