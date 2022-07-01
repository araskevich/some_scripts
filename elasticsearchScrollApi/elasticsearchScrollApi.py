import requests


def loadFile(filename):
    f = open(filename, encoding=("utf-8"))
    Data = f.read()
    f.close()
    return Data


def httpPost(data):
    url = 'http://elasticsearch.example.com:9200/_search?pretty&size=5000&scroll=1m'
    headers = {'Content-type': 'application/json'}
    res = requests.post(url, data=data, headers=headers)
    return res.json()


def scrollJob(sid):
    while(True):
        headers = {'Content-type': 'application/json'}
        data = '\n{\n "scroll" : "1m", \n "scroll_id" : "' + sid + '" \n}'
        url = 'http://elasticsearch.example.com:9200/_search/scroll'
        res = requests.post(url, data=data, headers=headers)
        data = res.json()
        
        printData(data)

        if not (data['hits']['hits']):
            break


def printData(data):
    source = data['hits']['hits']
    for raw in range(len(source)):
        valueA = source[raw]['_source']['timestamp']
        valueB = source[raw]['_source']['msg'] 
        print(valueA, valueB)


def main():
    data = loadFile('kibanaSearchSample.json')
    resp = httpPost(data)

    totalHits = resp['hits']['total']
    print('totalHits = ', totalHits)

    sid = resp['_scroll_id']

    printData(resp)

    scrollJob(sid)


if __name__ == '__main__':
    main()


