from flask import Flask, render_template, request
import engine

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    fields = request.args.getlist('fields')
    genres = request.args.getlist('genres')
    
    if query is None:
        return render_template('index.html')
    else:
        results = engine.search(query, fields, genres)
        
        return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
    engine.close()