from datetime import datetime
from flask import Flask,request,jsonify,render_template,redirect,url_for
from elasticsearch import Elasticsearch

app=Flask(__name__)
es = Elasticsearch()

#Inserting new items
@app.route('/api',methods=['GET','POST'])
def search():
    if request.method=='POST':
        #author=request.form['author']
        text=request.form['text']

        body={
            'text':text,
            'author':"ninja",
            'timestamp':datetime.now()
        }
        result=es.index(index="search-index",doc_type='url',id=1,body=body)
        return redirect(url_for('search_result',text=text))
    #es.indices.refresh(index="search-index")
    return render_template('index.html')

#showing the content
@app.route('/', methods=['GET'])
def index():
    if request.method=='GET':
        #return "Results"
        res = es.get(index="search-index", doc_type='url', id=1)
        return jsonify(res['_source'])
    return "neigh"

#Search results
@app.route('/result')
def search_result():
    text = request.args.get('text', None)
    return text
    


if __name__ == "__main__":
    app.run(debug=True)
