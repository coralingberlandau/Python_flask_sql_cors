from flask import Flask, jsonify, request
api = Flask(__name__)
import sqlite3
from flask_cors import CORS
api = Flask(__name__)
CORS(api)
con = sqlite3.connect("cars.db",check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE if not exists cars(color, model, brand)")

# usage: http://127.0.0.1:5000/  (get)
@api.route('/')
def hello():
    return 'Hello, World!'

# usage: http://127.0.0.1:5000/add_car  (post)
@api.route('/add_car' , methods=['post'])
def new_car():
    data = request.get_json()
    cur.execute(f"INSERT INTO cars VALUES('{data['color']}', '{data['model']}', '{data['brand']}')")
    con.commit()
    return jsonify({"message": "New car added", "data": data})

# usage: http://127.0.0.1:5000/get_car   (get)
@api.route('/get_car')
def get_all_cars():
    cur.execute("SELECT rowid, * FROM cars")
    rows = cur.fetchall()
    cars_list = []
    for row in rows:
        car = {
            'rowid': row[0],
            'color': row[1],
            'model': row[3],
            'brand': row[2],
        }
        cars_list.append(car)
    return jsonify(cars_list)

# usage: http://127.0.0.1:5000/update_car/<int:rowid>  (put)
@api.route('/update_car/<int:rowid>', methods=['PUT'])
def update_car(rowid):
    data = request.get_json()
    cur.execute("UPDATE cars SET color = ?, model = ?, brand = ? WHERE rowid = ?", (data['color'], data['model'], data['brand'], rowid))
    con.commit()
    return jsonify({"message": "Car updated", "data": data})

# usage: http://127.0.0.1:5000/delete_car/<int:rowid> (delete)
@api.route('/delete_car/<int:rowid>', methods=['DELETE'])
def delete_car(rowid):
    cur.execute("DELETE FROM cars WHERE rowid = ?", (rowid,))
    con.commit()
    return jsonify({"message": "Car deleted"})

if __name__ == '__main__':
    api.run(debug=True)