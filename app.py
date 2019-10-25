from datetime import datetime
import xml.etree.ElementTree as ET 
from flask import Flask,request,jsonify,render_template,redirect,url_for
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app=Flask(__name__)
es = Elasticsearch()



@app.before_first_request
def init():
    tree = ET.parse('sitemap.xml') 
    root = tree.getroot()
    id=0 

    for url in root.findall('url'):
        link = url.find('loc').text
        body={
            "url":link,
        }
        
        es.index(index="search-index",doc_type='url',id=1,body=body)  
        id+=1
        print(link)
    return 0      


    


#Inserting new items
@app.route('/api',methods=['GET','POST'])
def search():
    if request.method=='POST':
        text=request.form['text']
        s = Search().using(es).query("match", title="react")
        #print(s.to_dict())
        response = s.execute()
        #print(s.to_dict())
        for hit in s:
            print(hit.title)
            return redirect(url_for('search_result',text=hit.title))

        #author=request.form['author']
        # text=request.form['text']

        # body={
        #     'text':text,
        #     'author':"ninja",
        #     'timestamp':datetime.now()
        # }
        # result=es.index(index="search-index",doc_type='url',id=1,body=body)
        #return redirect(url_for('search_result'))
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
    init()
    app.run(debug=True)
