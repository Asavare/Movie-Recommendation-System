import pandas as pd
from sklearn.neighbors import NearestNeighbors
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
movie_ratings = ratings.merge(
    movies,
    on='movieId'
)
movie_stats = movie_ratings.groupby(
    'title'
)['rating'].agg(['mean','count'])
popular_movies = movie_stats[
    movie_stats['count'] >= 100
].sort_values(
    'mean',
    ascending=False
)
user_movie_matrix = movie_ratings.pivot_table(
    index='title',
    columns='userId',
    values='rating'
)
user_movie_matrix_filled = user_movie_matrix.fillna(0)
knn = NearestNeighbors(
    metric='cosine',
    algorithm='brute'
)

knn.fit(user_movie_matrix_filled)
genres = movies['genres'].str.get_dummies(sep='|')

movie_features = genres
content_knn = NearestNeighbors(
    n_neighbors=6,
    metric='cosine'
)

content_knn.fit(movie_features)
def recommend_content(movie_name):

    movie_index = movies[
        movies['title'].str.contains(
            movie_name,
            case=False
        )
    ].index[0]

    distances, indices = content_knn.kneighbors(
        movie_features.iloc[movie_index].values.reshape(1, -1)
    )

    recommendations = []

    for idx in indices[0][1:]:
        recommendations.append(
            movies.iloc[idx]['title']
        )

    return recommendations
def recommend_collaborative(movie_name):

    movie_title = user_movie_matrix_filled.index[
        user_movie_matrix_filled.index.str.contains(
            movie_name,
            case=False
        )
    ][0]

    movie_index = user_movie_matrix_filled.index.get_loc(
        movie_title
    )

    distances, indices = knn.kneighbors(
        user_movie_matrix_filled.iloc[movie_index]
        .values.reshape(1, -1),
        n_neighbors=6
    )

    recommendations = []

    for i in range(1, len(indices[0])):
        recommendations.append(
            user_movie_matrix_filled.index[
                indices[0][i]
            ]
        )

    return recommendations
def hybrid_recommend(movie_name):

    content_recs = recommend_content(movie_name)

    collaborative_recs = recommend_collaborative(
        movie_name
    )

    final_recommendations = []

    for movie in content_recs:
        if movie not in final_recommendations:
            final_recommendations.append(movie)

    for movie in collaborative_recs:
        if movie not in final_recommendations:
            final_recommendations.append(movie)

    return final_recommendations[:10]
def get_popular_movies():

    return list(
        popular_movies.head(10).index
    )

