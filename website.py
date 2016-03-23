from flask import Flask, render_template, request
import engine

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    
    if query is None:
        return render_template('index.html')
    else:
        return engine.search(query)

if __name__ == "__main__":
    app.run(debug=True)