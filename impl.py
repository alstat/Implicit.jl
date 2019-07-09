import pandas as pd
import numpy as np 

raw_data = pd.read_table("data/lastfm-dataset-360K/usersha1-artmbid-artname-plays.tsv")
raw_data = raw_data.drop(raw_data.columns[1], axis=1)
raw_data.columns = ['user', 'artist', 'plays']

# Drop rows with missing values
data = raw_data.dropna()

# Convert artists names into numerical IDs
data['user_id'] = data['user'].astype("category").cat.codes
data['artist_id'] = data['artist'].astype("category").cat.codes


item_lookup = data[['artist_id', 'artist']].drop_duplicates()
item_lookup['artist_id'] = item_lookup.artist_id.astype(str)

data = data.drop(['user', 'artist'], axis=1)

# Drop any rows that have 0 plays
data = data.loc[data.plays != 0]

# Create lists of all users, artists and plays
users = list(np.sort(data.user_id.unique()))
artists = list(np.sort(data.artist_id.unique()))
plays = list(data.plays)

# Get the rows and columns for our new matrix
rows = data.user_id.astype(int)
cols = data.artist_id.astype(int)

# Contruct a sparse matrix for our users and items containing number of plays
data_sparse = sparse.csr_matrix((plays, (rows, cols)), shape=(len(users), len(artists)))