from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import warnings

warnings.simplefilter("ignore")
nltk.download('punkt')
nltk.download('stopwords')

def to_keywords(input_string):
    '''keywords from input_string.'''
    no_symbols = re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
    word_tokens = word_tokenize(no_symbols)
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    filtered_sentence = [ps.stem(w)
                         for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_sentence)
es = Elasticsearch(
    hosts=['http://172.18.0.2:9200'],
    http_auth=("elastic", "nOlNvm1Z7_8*SZQaMR*H"),
)
index_name = "xi_index20240222"
# Kibana eyJ2ZXIiOiI4LjEyLjIiLCJhZHIiOlsiMTcyLjE4LjAuMjo5MjAwIl0sImZnciI6ImIwZTVkYjYzNTYxZjkzNzQxYmJiNTNmOWRlNjU0ZjFjMjVlYTQyMzhiMDA1ZjgzZmEwYWI3ZmZmOGQ5YWQzYjkiLCJrZXkiOiJ2cWFVLUkwQnlpVTAxbkJFVHQzLTpTM250NURpc1FmQ0x0RXhQNGVxRUJRIn0=

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name)

actions = [
    {
        "_index": index_name,
        "_source": {
            "keywords": to_keywords(para),
            "text": para
        }
    }
    for para in paragraphs
]

helpers.bulk(es, actions)

def search(query_string, top_n=3):

    search_query = {
        "match": {
            "keywords": to_keywords(query_string)
        }
    }
    res = es.search(index=index_name, query=search_query, size=top_n)
    return [hit["_source"]["text"] for hit in res["hits"]["hits"]]

results = search("what skils does Xi have?", 2)
for r in results:
    print(r+"\n")
