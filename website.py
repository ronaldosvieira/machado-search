from flask import Flask, render_template, request, url_for
import engine

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    fields = request.args.getlist('fields')
    genres = request.args.getlist('genres')
    page = request.args.get('page')
    
    if not page:
        page = 1
    
    if not query:
        return render_template('index.html')
    else:
        results = engine.search(query, fields, genres, int(page))
        
        return render_template('results.html', results=results)

def url_for_page(page=None, query=None):
    args = request.args.to_dict(flat=False)
    
    if page:
        args['page'] = page
    
    if query:
        args['query'] = query
        
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_page'] = url_for_page
    
if __name__ == "__main__":
    app.run(debug=True)
    engine.close()