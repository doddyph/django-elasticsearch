import csv
import json
import urllib
from django.http import JsonResponse
from elasticsearch import Elasticsearch

ES_HOST = {"host": "localhost", "port": 9200}
FILE_URL = "http://apps.sloanahrens.com/qbox-blog-resources/kaggle-titanic-data/train.csv"
INDEX_NAME = 'titanic'
DOC_TYPE_NAME = 'passenger'
ID_FIELD = 'passengerid'


def api_elastic_sample_build_an_index(request):
    response = urllib.urlopen(FILE_URL)
    csv_file_object = csv.reader(response)
    header = csv_file_object.next()
    header = [item.lower() for item in header]

    es = Elasticsearch(hosts=[ES_HOST])

    if es.indices.exists(INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    es.indices.create(index=INDEX_NAME, body=request_body)

    bulk_data = []
    for row in csv_file_object:
        data_dict = {}

        for i in range(len(row)):
            data_dict[header[i]] = row[i]

        op_dict = {
            "index": {
                "_index": INDEX_NAME,
                "_type": DOC_TYPE_NAME,
                "_id": data_dict[ID_FIELD]
            }
        }

        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
    es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)

    return JsonResponse({'status': 'Build a sample an Elastic index done.'})


class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def api_elastic_mapping(request):
    es = Elasticsearch(hosts=[ES_HOST])

    mapping_res = es.indices.get_mapping()
    mapping = []

    for key, value in mapping_res.iteritems():
        obj = Object()
        obj.fields = []
        obj.index = key

        for key2, value2 in value['mappings'].iteritems():
            obj.type = key2

            for key3, value3 in value2['properties'].iteritems():
                obj2 = Object()
                obj2.name = key3
                obj2.type = value3['type']
                obj.fields.append(obj2)

        mapping.append(json.loads(obj.to_JSON()))

    return JsonResponse(mapping, safe=False)