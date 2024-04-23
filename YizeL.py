"""
Yize Liu
Yukang Zhao

This python file includes anlysis of top 1000 YouTuber
and also their incomes.
Each funciton provides different visulizaitons to our
project.
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def youTuber_table(html: str) -> pd.DataFrame:
    """
    This function takes in a html string and returns
    a dataframe. It will read in the html link and
    convert it to dataframe. It will also clean and convert
    any necessary variables of the table.
    """
    table = pd.read_html(html)
    t1 = table[1].rename(columns={0: 'rank', 1: 'Youtuber',
                                  2: 'income', 3: 'subscribers',
                                  4: 'income / subscribers',
                                  5: 'video views', 6: 'category',
                                  7: 'started'})
    youtuber_income = table[0].append(t1)
    youtuber_income['income'] = youtuber_income['income'].str.strip(' $M')
    youtuber_income['income'] = youtuber_income['income'].astype(float)
    youtuber_income['income / subscribers'] = youtuber_income[
        'income / subscribers'].str.strip('$M')
    youtuber_income['income / subscribers'] = youtuber_income[
        'income / subscribers'].astype(float)
    return youtuber_income


def income_top10(df: pd.DataFrame) -> None:
    """
    This function takes in a dataframe as an input.
    It will generate the plot of top 10 YouTuber
    incomes.
    """
    sns.catplot(x='Youtuber', y='income', kind='bar',
                data=df.nlargest(10, 'income'), aspect=4)
    plt.ylabel('Income($million)', fontsize=15)
    plt.xticks(fontsize=12, rotation=-35)
    plt.xlabel('Youtuber', fontsize=15)
    plt.yticks(fontsize=12)
    plt.title("top 10 income youtubers", fontsize=20)
    plt.savefig('top10_Income_YouTubers.png')


def income_per_subscriber(df: pd.DataFrame) -> None:
    """
    This function will take a dataframe as an input.
    It will generate the plot of top 10 YouTuber's
    Income/Subscribers.
    """
    sns.catplot(x='Youtuber', y='income / subscribers', kind='bar',
                data=df.nlargest(10, 'income / subscribers'), aspect=4)
    plt.ylabel('Income/subscribers($million)', fontsize=15)
    plt.xticks(fontsize=12)
    plt.xlabel('Youtuber', fontsize=15)
    plt.yticks(fontsize=12)
    plt.title("top 10 income/subscribers youtubers", fontsize=20)
    plt.savefig('top_10_Income_Subscribers.png')


def pie_chart_category(df: pd.DataFrame) -> None:
    """
    This function will take a dataframe as an input.
    It will generate a plot of total income by each
    category.
    """
    income_by_category = df.groupby('category')['income'].sum()
    income_by_category = income_by_category.reset_index()
    labels = list(income_by_category['category'])
    plt.pie(income_by_category['income'], labels=labels)
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    plt.title('Which category made the most money in total')
    plt.savefig('total_income_by_category.png')


def counts_category(df: pd.DataFrame) -> None:
    """
    This function will take a dataframe as an input.
    It will generate a plot of total counts of each
    category.
    """
    sns.catplot(x='category', kind='count', data=df, aspect=4)
    plt.xticks(rotation=-35, fontsize=12)
    plt.xlabel('Category', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.title('Counts Of Each Category')
    plt.savefig('total_counts_of_each_category.png')


def income_mean(youtuber_income: pd.DataFrame) -> None:
    """
    This function will take a dataframe as an input.
    It will generate a plot of mean income of each
    category.
    """
    income_min = youtuber_income.groupby('category')['income'].min()
    income_max = youtuber_income.groupby('category')['income'].max()
    income_min = list(income_min)
    income_max = list(income_max)
    values_to_delete = income_min + income_max
    rows_to_delete = youtuber_income[youtuber_income[
        'income'].isin(values_to_delete)]
    youtuber_income_deleted = youtuber_income.drop(rows_to_delete.index)
    youtuber_income_deleted = youtuber_income_deleted.groupby(
        'category')['income'].mean()
    youtuber_income_deleted = youtuber_income_deleted.reset_index()
    labels = list(youtuber_income_deleted['category'])
    plt.pie(youtuber_income_deleted['income'], labels=labels)
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    plt.title('Which category has the greatest revenue value')
    plt.savefig('category_income_mean.png')


def top1000(csv_file: str) -> pd.DataFrame:
    """
    This function takes a csv file as an input.
    It will read the file and return the pandas
    data frame as output.
    """
    top_1000 = pd.read_csv(csv_file)
    top_1000 = top_1000[top_1000['Video Count'] != '0']
    err = ('https://us.youtubers.me/global/all/'
           'top-1000-most_subscribed-youtube-channels')
    top_1000 = top_1000[top_1000['Category'] != err]
    top_1000['Video Views'] = [int(i.replace(',', '')) for i in top_1000[
        'Video Views']]
    top_1000['Video Count'] = [int(i.replace(',', '')) for i in top_1000[
        'Video Count']]
    top_1000['Subscribers'] = [int(i.replace(',', '')) for i in top_1000[
        'Subscribers']]
    return top_1000


def top1000_counts(df: pd.DataFrame) -> None:
    """
    This function will take a data frame as an input.
    It will plot the total counts of each category in the
    top 1000 YouTubers.
    """
    sns.catplot(x='Category', kind='count', data=df, aspect=4)
    plt.xticks(rotation=-35, fontsize=12)
    plt.xlabel('Category', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.title('plot of the total counts of each Category', fontsize=20)
    plt.savefig('total_counts_of_top1000.png')


def top1000_views(df: pd.DataFrame) -> None:
    """
    This function will take a data frame as an input.
    It will plot the total views of the top 1000 YouTubers
    by category.
    """
    total_views = df.groupby('Category')['Video Views'].sum()
    total_views = total_views.reset_index()
    sns.catplot(x='Category', y='Video Views', kind='bar',
                data=total_views, aspect=4)
    plt.xticks(rotation=-35, fontsize=12)
    plt.xlabel('Category', fontsize=15)
    plt.ylabel('Video Views', fontsize=15)
    plt.title('plot of the total views of each Category', fontsize=20)
    plt.savefig('total_views_of_top1000.png')


def subscriber_video(top_1000: pd.DataFrame) -> None:
    """
    This function will take a data frame as an input.
    It will choose the year from 2009-2019 and calculate
    the log ratio of subscribers divided by video count.
    It will then plot the statistic by each category.
    """
    year_trend = list()
    # Each category from 2009 - 2019
    for i in range(11):
        data = top_1000[top_1000['Started'] == i+2009]
        is_music = data['Category'] == 'Music'
        is_enter = data['Category'] == 'Entertainment'
        is_game = data['Category'] == 'Gaming'
        is_peo = data['Category'] == 'People & Blogs'
        is_edu = data['Category'] == 'Education'
        data = data[is_music | is_enter | is_game | is_peo | is_edu]
        # Calculate how many subscribers increased per video
        best_cate = dict(np.log(data.groupby('Category')[
            'Subscribers'].sum() / data.groupby('Category')[
            'Video Count'].sum()))
        year_trend.append(best_cate)
    new_df = pd.DataFrame(year_trend)
    sns.relplot(data=new_df, kind='line')
    plt.xticks(ticks=np.arange(11), labels=np.arange(11)+2009)
    plt.xlabel('Year')
    plt.ylabel('Subscribers(log)')
    plt.savefig('subscriber_increase_per_video.png')


def main():
    html = ('https://us.youtubers.me/global/all/'
            'the-highest-paid-youtubers-of-2021')
    df1 = youTuber_table(html)
    income_top10(df1)
    income_per_subscriber(df1)
    pie_chart_category(df1)
    counts_category(df1)
    income_mean(df1)

    df2 = top1000('topSubscribed.csv')
    top1000_counts(df2)
    top1000_views(df2)
    subscriber_video(df2)


if __name__ == '__main__':
    main()
