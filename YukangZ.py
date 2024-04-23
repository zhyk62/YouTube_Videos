"""
Yize Liu
Yukang Zhao

Process the dataset 2 and generate plots for the US videos
and comparisons of videos of four countries.
"""
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()


def change_date_format(xx_video: pd.DataFrame) -> pd.DataFrame:
    """ Convert the strange data format of original data to
        year, month, and day with integer type and add them as
        new columns of original data.
    """
    pub_year = xx_video['publish_time'].str[0:4]
    pub_month = xx_video['publish_time'].str[5:7]
    pub_day = xx_video['publish_time'].str[8:10]
    xx_video['publish_year'] = pub_year.astype(int)
    xx_video['publish_month'] = pub_month.astype(int)
    xx_video['publish_day'] = pub_day.astype(int)
    del xx_video['publish_time']

    tre_year = '20' + xx_video['trending_date'].str[0:2]
    tre_month = xx_video['trending_date'].str[6:8]
    tre_day = xx_video['trending_date'].str[3:5]
    xx_video['trending_year'] = tre_year.astype(int)
    xx_video['trending_month'] = tre_month.astype(int)
    xx_video['trending_day'] = tre_day.astype(int)
    del xx_video['trending_date']
    return xx_video


def convert_category(file_name: str, xx_video: pd.DataFrame) -> pd.DataFrame:
    """ Convert the category id into actual categories with type string.
        Create a new column that calculate the like view ratio of each video.
    """
    f = open(file_name)
    xx_json = json.load(f)
    xx_json = pd.json_normalize(xx_json['items'])
    xx_json = xx_json[['id', 'snippet.title']]
    xx_json['id'] = xx_json['id'].astype(int)
    xx_video = xx_video.merge(xx_json, left_on='category_id', right_on='id')
    xx_video.rename(columns={'snippet.title': 'title'}, inplace=True)
    del xx_video['category_id']
    del xx_video['id']
    xx_video['Like View Ratio'] = xx_video['likes'] / xx_video['views']
    return xx_video


def open_file(file_name: str, cate_file: str) -> pd.DataFrame:
    """ Open the file and filter the columns needed.
        Calculate the days from publish to trending for each video.
    """
    xx_video = pd.read_csv(file_name)
    xx_video = xx_video[['trending_date', 'category_id', 'publish_time',
                        'views', 'likes', 'dislikes', 'comment_count']]
    xx_video = change_date_format(xx_video)
    xx_video = convert_category(cate_file, xx_video)
    xx_video['days_from_pub_to_trend'
             ] = (xx_video['trending_year']-xx_video['publish_year']
                  )*365 + (xx_video['trending_month']-xx_video['publish_month']
                           )*30 + (xx_video['trending_day'
                                            ]-xx_video['publish_day'])
    return xx_video


def trending_ratio(us_video: pd.DataFrame) -> None:
    """ Plot Days from Publish to Trending  V.S.  Like-View Ratio US Videos.
    """
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=us_video[us_video['days_from_pub_to_trend'] <= 30],
                 y='Like View Ratio', x='days_from_pub_to_trend')
    plt.xlabel('Days from Publish to Trending')
    plt.ylabel('Mean Like View Ratio')
    plt.title('Days from Publish to Trending V.S. Like-View Ratio, US Videos')
    plt.savefig('us_days_ratio.png')


def us_view_and_ratio(us_video: pd.DataFrame) -> None:
    """ Plot USA Total Views and View Like Ratio by subplots.
    """
    fig, [ax1, ax2] = plt.subplots(2, figsize=(14, 6))

    l_v_rate = us_video.groupby('title')['Like View Ratio'].mean().to_frame()
    l_v_rate['title'] = l_v_rate.index
    sns.barplot(x='title', y='Like View Ratio', data=l_v_rate, ax=ax1)
    ax1.set_xticklabels(labels='')
    ax1.set_xlabel('')
    ax1.set_ylabel('Mean Like View Ratio')
    ax1.set_title('For Videos in the USA')

    tot_view_by_cate = us_video.groupby('title')['views'].mean().to_frame()
    tot_view_by_cate['title'] = tot_view_by_cate.index
    sns.barplot(x='title', y='views', data=tot_view_by_cate, ax=ax2)
    plt.xticks(rotation=-45)
    ax2.set_xlabel('')
    ax2.set_ylabel('Mean Views')
    plt.savefig('us_view_ratio.png')


def us_day_from_pub_to_trend(us_video: pd.DataFrame) -> None:
    """ Plot the Days from Publish to Trending vs. Number of Videos, for US
        videos.
    """
    pub_to_trend = us_video.groupby('days_from_pub_to_trend'
                                    )['title'].count().to_frame()
    pub_to_trend = pub_to_trend.groupby(np.where(pub_to_trend.index > 30, 31,
                                                 pub_to_trend.index)).sum()
    pub_to_trend['day'] = pub_to_trend.index
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=pub_to_trend[pub_to_trend['day'] <= 30],
                 y='title', x='day')
    plt.xlabel('Days from Publish to Trending')
    plt.ylabel('Number of Videos')
    plt.title('How Long a Video Takes From Publish to Trending, US Videos')
    plt.savefig('pub_to_trend_video_num.png')


def merge_data(us_video: pd.DataFrame, ca_video: pd.DataFrame,
               fr_video: pd.DataFrame, in_video: pd.DataFrame) -> pd.DataFrame:
    """ Merge the data for all four countries by category for further
        comparison.
    """
    us_l_v_rate = us_video.groupby('title'
                                   )[['Like View Ratio', 'views']].mean()
    ca_l_v_rate = ca_video.groupby('title'
                                   )[['Like View Ratio', 'views']].mean()
    fr_l_v_rate = fr_video.groupby('title'
                                   )[['Like View Ratio', 'views']].mean()
    in_l_v_rate = in_video.groupby('title'
                                   )[['Like View Ratio', 'views']].mean()

    us_ca = us_l_v_rate.merge(ca_l_v_rate, left_on='title',
                              right_on='title', how='outer')
    us_ca.rename(columns={'Like View Ratio_x': 'USA_ratio',
                          'Like View Ratio_y': 'Canada_ratio',
                          'views_x': 'USA_view',
                          'views_y': 'Canada_view'}, inplace=True)
    fr_in = fr_l_v_rate.merge(in_l_v_rate, left_on='title',
                              right_on='title', how='outer')
    fr_in.rename(columns={'Like View Ratio_x': 'France_ratio',
                          'Like View Ratio_y': 'India_ratio',
                          'views_x': 'France_view', 'views_y': 'India_view'},
                 inplace=True)
    us_ca_fr_in = us_ca.merge(fr_in, left_on='title', right_on='title',
                              how='outer')
    us_ca_fr_in['title'] = us_ca_fr_in.index
    return us_ca_fr_in


def mean_like_view_ratio(us_ca_fr_in: pd.DataFrame) -> None:
    """ Plot mean like view ratio by category of each country.
    """
    us_ca_fr_in.plot(x="title", y=["USA_ratio", "Canada_ratio", 'France_ratio',
                                   'India_ratio'], kind="bar", figsize=(16, 8))
    plt.xticks(rotation=-45)
    plt.xlabel('Category')
    plt.ylabel('Mean Like View Ratio')
    plt.title('Mean Like View Ratio by Category')
    plt.savefig('ratio_by_cate_all.png')


def mean_views(us_ca_fr_in: pd.DataFrame) -> None:
    """ Plot the mean views by category in each country in 4 subplots.
    """
    fig, [ax1, ax2, ax3, ax4] = plt.subplots(4, figsize=(15, 10))
    sns.barplot(x='title', y='USA_view', data=us_ca_fr_in, ax=ax1)
    ax1.set_xticklabels(labels='')
    ax1.set_xlabel('')
    ax1.set_title('Mean Views by Category in Each Country')

    sns.barplot(x='title', y='Canada_view', data=us_ca_fr_in, ax=ax2)
    ax2.set_xticklabels(labels='')
    ax2.set_xlabel('')

    sns.barplot(x='title', y='France_view', data=us_ca_fr_in, ax=ax3)
    ax3.set_xticklabels(labels='')
    ax3.set_xlabel('')

    sns.barplot(x='title', y='India_view', data=us_ca_fr_in, ax=ax4)
    plt.xticks(rotation=-45)
    plt.xlabel('Category')
    plt.savefig('mean_views_per_cate_all.png')


def main():
    us_file = 'USvideos.csv'
    us_cate_file = 'US_category_id.json'
    us_video = open_file(us_file, us_cate_file)

    fr_file = 'FRvideos.csv'
    fr_cate_file = 'FR_category_id.json'
    fr_video = open_file(fr_file, fr_cate_file)

    ca_file = 'CAvideos.csv'
    ca_cate_file = 'CA_category_id.json'
    ca_video = open_file(ca_file, ca_cate_file)

    in_file = 'INvideos.csv'
    in_cate_file = 'IN_category_id.json'
    in_video = open_file(in_file, in_cate_file)

    trending_ratio(us_video)
    us_view_and_ratio(us_video)
    us_day_from_pub_to_trend(us_video)
    us_ca_fr_in = merge_data(us_video, ca_video, fr_video, in_video)
    mean_like_view_ratio(us_ca_fr_in)
    mean_views(us_ca_fr_in)


if __name__ == '__main__':
    main()
