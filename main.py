import datetime
import pytz

import flask as f
from data import *

app = f.Flask(__name__)

data = {}

pizzas = []
toppings = {}
orders = []
orders_header = []
expected_order_request_body_keys = ["pizzas", "takeaway",  "payment_type", "customer_id", "note",
                                    "delivery_address", "street", "city", "country", "zipcode"]

@app.route('/')
def hello_world():
    return "Welcome to Group 19's Pizza API!"


@app.route('/pizza')
def get_pizzas():
    return f.jsonify(pizzas)  # Built-in function for json


@app.route('/pizza/<pizza_id>')
def get_pizza_by_id(pizza_id, include_toppings=True):
    pizza_id = int(pizza_id)

    for d in pizzas:
        if d['pizza_id'] == pizza_id:
            pizza = d.copy()
            if include_toppings:
                pizza['toppings'] = toppings[pizza_id]
            return pizza

    return f.jsonify({"message": "Pizza not found"}), 404


@app.route('/order', methods=['POST'])
def post_order():
    order = {}
    delivery_address = {}

    body = f.request.json

    if len(body) + len(body["delivery_address"]) != len(expected_order_request_body_keys):
        return f.jsonify({"message": "The format of the object is not valid: missing parameter"}), 400

    for d in body.items():
        if d[0] != "delivery_address":
            if d[0] not in expected_order_request_body_keys:
                return f.jsonify({"message": "The format of the object is not valid: incorrect parameter"}), 400

            if d[0] == "pizzas":
                for pizza in d[1]:
                    print(pizza)
                    if pizza >= len(pizzas):
                        return f.jsonify({"message": "The format of the object is not valid: incorrect pizza id"}), 400

            order[d[0]] = d[1]
        else:
            for d1 in d[1].keys():
                delivery_address[d1] = d[1][d1]

    order["delivery_address"] = delivery_address.copy()
    order["order_id"] = data["current_order_id"]
    order["status"] = "In Progress"
    order["ordered_at"] = datetime.datetime.now()
    order["delivery_time"] = datetime.datetime.now() + datetime.timedelta(minutes=10)

    print(datetime.datetime.now())

    data["current_order_id"] += 1
    update_data_file(data)

    write_order(order, orders_header)

    keys = ['order', 'ordered_at', 'delivery_time']
    return f.jsonify({k: (order if k == "order" else order[k]) for k in keys})


@app.route('/order/<order_id>')
def get_order_by_id(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return f.jsonify({"message": "Invalid ID supplied"}), 400

    orders, all_headers = read_orders()

    for order in orders:
        if order["order_id"] == order_id:

            return f.jsonify({x: (order[x] if x != "pizzas" else [get_pizza_by_id(int(p), include_toppings=False) for p in order[x]]) for (x, y) in order.items()})

    return f.jsonify({"message": "Order_ID not found"}), 404


@app.route('/order/deliverytime/<order_id>')
def get_order_by_delivery_time(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return f.jsonify({"message": "Invalid ID supplied"}), 400

    orders, headers = read_orders()

    for order in orders:
        if order["order_id"] == order_id:
            order["time_left"] = str(parse_date(order["delivery_time"]) - datetime.datetime.now())

            if parse_date(order["delivery_time"]) < datetime.datetime.now():
                order["status"] = "Delivered"
                update_orders(orders, orders_header)
                return f.jsonify({"message": "Order already delivered"}), 400

            keys = ['order', 'ordered_at', 'delivery_time', 'time_left']
            return f.jsonify({k: (order if k == "order" else order[k]) for k in keys})

    return f.jsonify({"message": "Order not found"}), 404


@app.route("/order/cancel/<order_id>", methods=['PUT'])
def cancel_order(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return f.jsonify({"message": "Invalid ID supplied"}), 400

    orders, headers = read_orders()

    for order in orders:
        if order["order_id"] == order_id:
            time_since_order = datetime.datetime.now() - parse_date(order["ordered_at"])
            if order["status"] == "Cancelled" or datetime.datetime.now() > parse_date(order["delivery_time"]):
                if order["status"] != "Cancelled":
                    order["status"] = "Delivered"
                    update_orders(orders, orders_header)
                return f.jsonify({"message": "Unable to cancel an already cancelled or delivered order"}), 412

            if time_since_order > datetime.timedelta(minutes=5):
                return f.jsonify({"message": "Unable to cancel your order after 5 minutes have elapsed"}), 412

            order["status"] = "Cancelled"
            update_orders(orders, orders_header)
            return f.jsonify(order)

    return f.jsonify({"message": "Order not found"}), 404


if __name__ == '__main__':  # main running file
    pizzas, toppings = read_pizzas()
    orders, orders_header = read_orders()
    data = get_data_from_file()
    print(orders_header)
    print(pizzas)
    app.run()
