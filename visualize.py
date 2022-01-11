import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud

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
	def func(pct, allvalues):
		absolute = int(pct / 100.*np.sum(allvalues))
		return "{:.1f}%\n({:d}pts)".format(pct, absolute)
	# create 2 arrays to hold the categories' names and its popularity point
	categories = []
	for i in CATEGORIES.keys():
		categories.append(CATEGORIES[i])
	popularity = [0]*len(categories)
	# populate arrays with popularity point
	for i in videos.index:
		t = categories.index(CATEGORIES[int(videos.loc[i,'category_id'])])
		popularity[t] += int(videos.loc[i,'notes'])
	# create dataset and sort by total popularity
	dataset = pd.DataFrame(data={'categories': categories, 'popularity': popularity})
	dataset = dataset.groupby('categories').sum().sort_values(by=['popularity'], ascending=False)
	# take top 5 categories
	dataset_top = dataset[:5].copy()
	# one entry for all other categories
	dataset_others = pd.DataFrame(data={'popularity': [dataset['popularity'][5:].sum()]}, index=['Others'])
	# combining top 5 with others
	dataset = pd.concat([dataset_top, dataset_others])
	# plot pie chart
	colors = ['#00c2f9','#00e4b9','#feeaae','#fcb1d9','#fdfdfa','#d9ccb2']
	plt.pie(dataset['popularity'],labels=dataset.index, shadow=False,colors=colors,autopct=lambda pct: func(pct, dataset['popularity']))
	plt.show()

def plot_question_2(videos):
	# create empty string to hold all video titles later
	text = ''
	printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n'
	
	# filter all the titles to leave only printable characters
	videos['title'] = videos['title'].apply( lambda x: ''.join(filter(lambda xi: xi in printable, x)))
	# get each video title, break the words into tokens and add to 'text'
	for x in videos.index:
		title = str(videos.loc[x,'title'])
			
		tokens = title.split()
		for i in range(len(tokens)):
				tokens[i] = tokens[i].lower()
		text += ' '.join(tokens)+' '
		
	# generate word cloud
	cloud = wordcloud.WordCloud(width = 1400, height = 800, background_color ='white', min_font_size = 10).generate(text)
	# plot the word cloud
	plt.figure(figsize = (8, 14), facecolor = None)
	plt.imshow(cloud)
	plt.axis("off")
	plt.tight_layout(pad = 5) 
	plt.show()