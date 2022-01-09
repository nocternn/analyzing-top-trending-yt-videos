import numpy as np
import pandas as pd

DATES = ['2021-12-05T00:00:00Z', '2021-12-12T00:00:00Z', '2021-12-19T00:00:00Z', '2021-12-26T00:00:00Z', '2022-01-02T00:00:00Z']
REGIONS = ['US', 'GB', 'JP', 'KR', 'IN']
datasets_filenames = ["data/2021-12-05.csv","data/2021-12-12.csv","data/2021-12-19.csv","data/2021-12-26.csv","data/2022-01-02.csv","data/2022-01-09.csv"]

def merge(filenames):
	list_of_df = []
	for filename in filenames:
		current_df = pd.read_csv(filename,sep='	')
		list_of_df.append(current_df)

	all_df = pd.concat(list_of_df)
	all_df.reset_index(drop=True, inplace=True)
	return all_df

def clean(dataset):
	clean_df = dataset.copy(deep=True)

    # Replace NaN in description with space
	clean_df["description"].fillna(" ", inplace=True)
    # Delete all rows with a missing values if any
	clean_df.dropna(inplace=True)

    # Only keep rows with comments_disbled == FALSE
	clean_df = clean_df[(clean_df['comments_disabled'] == 'False')]

    # create new empty column
	clean_df['notes'] = " "

    # rename column to match snake case
	clean_df.rename(columns={'channelTitle': 'channel_title',
                             'publishedAt': 'published_at',
                             'channelId': 'channel_id',
							 'categoryId' : 'category_id'}, inplace=True)

    # delete non-relevant columns
	clean_df.drop(['comments_disabled'], axis=1, inplace=True)

	clean_df = clean_df.reindex(columns=['video_id', 'title', 'published_at', 'channel_id', 'channel_title',
                                         'category_id', 'trending_date', 'view_count', 'likes', 'dislikes', 
										 'comment_count', 'ratings_disabled', 'description', 'notes'])

	clean_df.reset_index(drop=True, inplace=True)

	return clean_df

temp = pd.read_csv('data/2022-01-09.csv',sep='	')
#temp = clean(temp)
print(temp.loc[1,:])


"""
combined_df = merge(datasets_filenames)
print(combined_df.shape)
print(combined_df.columns)

clean_df = clean(combined_df)
print(clean_df.shape)
print(clean_df.columns)
#clean_df.to_csv('data/clean.csv')
"""

