def Getauthor(x):
  for i in x:
    if i["job"] == 'authorPersonId':
      return i['name']
    return np.nan

df1['authorPersonId'] = df1['crew'].apply(Getauthor)

def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        return names
    return []


features = ['cast', 'keywords', 'genres']
for feature in features:
    df1[feature] = df1[feature].apply(get_list)


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'authorPersonId', 'genres']
for feature in features:
    df1[feature] = df1[feature].apply(clean_data)

    
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df1['soup'] = df1.apply(create_soup, axis=1)

from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df1['soup'])

from sklearn.metrics.pairwise import cosine_similarity
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df1 = df1.reset_index()
indices = pd.Series(df1.index, index=df1['original_title'])

def get_recommendations(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df1['original_title'].iloc[movie_indices]

