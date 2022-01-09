import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CATEGORIES = {1: 'Film & Animation',\
	2: 'Autos & Vehicles',\
	10: 'Music',\
	15: 'Pets & Animals',\
	17: 'Sports',\
	18: 'Short Movies',\
	19: 'Travel & Events',\
	20: 'Gaming',\
	21: 'Videoblogging',\
	22: 'People & Blogs',\
	23: 'Comedy',\
	24: 'Entertainment',\
	25: 'News & Politics',\
	26: 'Howto & Style',\
	27: 'Education',\
	28: 'Science & Technology',\
	29: 'Nonprofits & Activism',\
	30: 'Movies',\
	31: 'Anime/Animation',\
	32: 'Action/Adventure',\
	33: 'Classics',\
	34: 'Comedy',\
	35: 'Documentary',\
	36: 'Drama',\
	37: 'Family',\
	38: 'Foreign',\
	39: 'Horror',\
	40: 'Sci-Fi/Fantasy',\
	41: 'Thriller',\
	42: 'Shorts',\
	43: 'Shows',\
	44: 'Trailers'}

def plot_question_1(videos):
	# Creating autocpt arguments
	def func(pct, allvalues):
		absolute = int(pct / 100.*np.sum(allvalues))
		return "{:.1f}%\n({:d} g)".format(pct, absolute)
	# create empty arrays to hold relevant data
	categories = []
	view_counts = []
	# populate arrays
	for video in videos:
		categories.append(CATEGORIES[int(video['snippet']['categoryId'])])
		try:
			view_counts.append(int(video['statistics']['viewCount']))
		except:
			view_counts.append(0)
	# create dataset and sort by total view count
	dataset = pd.DataFrame(data={'categories': categories, 'view_count': view_counts})
	dataset = dataset.groupby('categories').sum().sort_values(by=['view_count'], ascending=False)
	# take top 5 categories
	dataset_top = dataset[:5].copy()
	# one entry for all other categories
	dataset_others = pd.DataFrame(data={'view_count': [dataset['view_count'][5:].sum()]}, index=['Others'])
	# combining top 5 with others
	dataset = pd.concat([dataset_top, dataset_others])
	# plot
	dataset.plot(kind='pie', subplots=True,\
		legend=False,\
		shadow=True,\
		autopct=lambda pct: func(pct, dataset['view_count'])\
	)
	plt.show()

def plot_question_2(videos):
	# create empty arrays to hold relevant data
	categories = []
	likes_count = []
	dislikes_count = []
	comments_count = []
	# populate arrays
	for video in videos:
		categories.append(CATEGORIES[int(video['snippet']['categoryId'])])
		try:
			likes_count.append(int(video['statistics']['likeCount']))
		except:
			likes_count.append(0)
		try:
			dislikes_count.append(int(video['statistics']['dislikeCount']))
		except:
			dislikes_count.append(0)
		try:
			comments_count.append(int(video['statistics']['commentCount']))
		except:
			comments_count.append(0)
	# create dataset and sort by total view count
	dataset = pd.DataFrame(data={'categories': categories,\
		'Likes': likes_count,\
		'Dislikes': dislikes_count,\
		'Comments': comments_count\
	})
	dataset = dataset.groupby('categories').sum().sort_values(\
		by=['Likes', 'Dislikes', 'Comments'], ascending=False)
	# plot
	dataset.plot(kind="barh", stacked=True)
	plt.show()