from flask import Flask, jsonify, request

app = Flask(__name__)

store =  
    {
        "item": [
            {
                "name": 'Book',
                "price": 99.99
            }
        ]
    }

	
@app.route('/item')
def get_item():
    
    return jsonify({"items": store})

@app.route('/item', methods=['POST'])
def create_item():
    r = request.get_json()
    new_item = {
               "name": r['name'],
               "price":r['price']
           }
    store['item'].append(new_item)

    return jsonify(new_item)

@app.route('/item/<string:name>')
def get_item(name):
    for item in store['items']:
        if name == item['name']:
            return jsonify({"item":item})

@app.route('/item/<string:name>')
def delete_item(name):
    for item in store['items']:
        if name == item['name']:
            store['items'].remove(item)
            return jsonify({"message":"item['name'] has been deleted"})

app.run(port=4098)