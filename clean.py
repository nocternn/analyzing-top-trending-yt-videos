import numpy as np
import pandas as pd

def merge():
	# merge data
	return

def clean():
	# clean data
	return

DATES = ['2021-12-05T00:00:00Z', '2021-12-12T00:00:00Z', '2021-12-19T00:00:00Z', '2021-12-26T00:00:00Z', '2022-01-02T00:00:00Z']
REGIONS = ['US', 'GB', 'JP', 'KR', 'IN']

for date in DATES:
	for region in REGIONS:
		df = pd.read_csv('data/{0}_youtube_trending_data.csv'.format(region))
		df = df.drop(columns=['tags', 'thumbnail_link'])
		df[df['trending_date'] == date].to_csv('data/{0}.csv'.format(date[:10]), sep='\t', mode='a', encoding='utf-8', index=False)