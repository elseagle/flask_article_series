
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)



def find_by_name(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return jsonify({'item': {'name': row[0], 'price': row[1]}})


@app.route('/item/<string:name>')
def get(name):
        item = find_by_name(name)
        if item:
            return item
        return jsonify({'message': 'Item not found'}), 404


@app.route('/item')
def get():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return jsonify({'items': items})


def insert(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


@app.route('/item', methods=['POST'])
def post(name):
        if find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = request.get_json()

        item = {'name': name, 'price': data['price']}

        try:
            insert(item)
        except:
            return jsonify({"message": "An error occurred inserting the item."})

        return jsonify(item)

@app.route('/item/<string:name>')
def delete_item(name):
  connection = sqlite3.connect('data.db')
  cursor = connection.cursor()

  query = "DELETE FROM items WHERE name=?"
  cursor.execute(query, (name,))

  connection.commit()
  connection.close()

  return jsonify({'message': 'Item deleted'})


def update(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

if __name__=="__main__":
    app.run(port=4098)
