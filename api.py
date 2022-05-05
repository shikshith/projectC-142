import get_recommendations from '../ContentBasedFiltering.py'
import liked_articles from '../Storage.py'
import not_liked_articles from '../Storage.py'
import did_not_read from '../Storage.py'

@app.route("get_recommendations", methods=["POST"])
def get_recommendations():
    movie = allMovies[0]
    allMovies = allMovies[1:]
    liked_articles.append(movie)
    return jsonify({
        "status": "success"
    }), 201