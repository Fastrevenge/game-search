from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "1234"), 
    "database": os.getenv("DB_NAME", "game_catalog"),
    "port": int(os.getenv("DB_PORT", 1234))
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/games/search', methods=['GET'])
def search_games():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    try:
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)

        
        sql = """
            SELECT id, title, description, image_url,
                   MATCH(title, description) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
            FROM games
            WHERE MATCH(title, description) AGAINST (%s IN NATURAL LANGUAGE MODE)
            ORDER BY score DESC
            LIMIT 20;
        """
        
        cur.execute(sql, (query, query))
        results = cur.fetchall()

        cur.close()
        conn.close()
        return jsonify(results)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)