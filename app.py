from datetime import datetime
import xml.etree.ElementTree as ET 
from flask import Flask,request,jsonify,render_template,redirect,url_for
from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search

app=Flask(__name__)
es = Elasticsearch()



@app.before_first_request
def init():
    tree = ET.parse('sitemap.xml') 
    root = tree.getroot()
    id=0 

    for url in root.findall('url'):
        link = url.find('loc').text
        linkTemp= link.split('/')
        text=""
        for i in linkTemp:
            text+= i+" "
        print(text)
        body={
            "url":link,
            "text": text,
        }
        
        es.index(index="search-index",doc_type='url',id=id,body=body)  
        id+=1
        print(link)
    return 0      


    

# Search Items
@app.route('/api',methods=['GET','POST'])
def search():
    if request.method=='POST':
        text=request.form['text']
        body ={
            "query": {
                "multi_match":{
                    "query": "https:",
                }
            }
        }

        res = es.search(index="search-index", body=body)
        print(res)

        print(".................STONKS ............")
        for hits in res['hits']['hits']:
            print(hits['_source']['url'])

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
