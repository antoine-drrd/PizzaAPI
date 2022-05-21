import csv
import datetime
import json


def read_pizzas():
    pizzas = []
    toppings = {}

    with open('pizzas.csv', newline='') as csvfile:
        pizzaReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for i, row in enumerate(pizzaReader):
            if i == 0:
                header = row
            else:
                pizza = {}
                for j, element in enumerate(row):
                    if header[j] == "price":
                        pizza[header[j]] = float(element)
                    elif header[j] == "vegetarian":
                        if element.lower() == "true":
                            pizza[header[j]] = True
                        elif element.lower() == "false":
                            pizza[header[j]] = False
                    elif header[j] == "pizza_id":
                        pizza[header[j]] = int(element)
                    elif header[j] == "name":
                        pizza[header[j]] = element
                    elif header[j] == "toppings":
                        toppings[pizza["pizza_id"]] = element.split(';')

                pizzas.append(pizza)

    return pizzas, toppings


def read_orders():
    orders = []
    header = []

    with open('orders.csv', newline='') as csvfile:
        orderReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for i, row in enumerate(orderReader):
            if i == 0:
                header = row.copy()
            else:
                order = {}
                delivery_address = {}
                for j, element in enumerate(row):
                    if header[j] == "order_id":
                        order[header[j]] = int(element)
                    elif header[j] == "customer_id":
                        order[header[j]] = int(element)
                    elif header[j] == "status":
                        order[header[j]] = element
                    elif header[j] == "ordered_at":
                        order[header[j]] = element
                    elif header[j] == "delivery_time":
                        order[header[j]] = element
                    elif header[j] == "note":
                        order[header[j]] = element
                    elif header[j] == "takeaway":
                        if element.lower() == "true":
                            order[header[j]] = True
                        else:
                            order[header[j]] = False
                    elif header[j] == "payment_type":
                        order[header[j]] = element
                    elif header[j] == "pizzas":
                        order[header[j]] = element.split(';')
                    else:  # delivery address
                        if header[j] == "street":
                            delivery_address[header[j]] = element
                        elif header[j] == "city":
                            delivery_address[header[j]] = element
                        elif header[j] == "country":
                            delivery_address[header[j]] = element
                        elif header[j] == "zipcode":
                            delivery_address[header[j]] = element

                order["delivery_address"] = delivery_address.copy()
                orders.append(order)

    return orders, header


def write_order(order, orders_header):
    with open('orders.csv', 'a', newline='') as csvfile:
        orderWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # order_id;customer_id;status;ordered_at;delivery_time;takeaway;payment_type;pizzas;note;street;city;country;zipcode
        row = orders_header.copy()
        print("row", row)

        print("header", orders_header)
        for key in order.keys():
            if key != "delivery_address":
                if key == "pizzas":
                    print("header", orders_header)
                    print(type(order[key]))
                    row[orders_header.index(key)] = ";".join([str(element) for element in order[key]])
                elif key != "time_left":
                    row[orders_header.index(key)] = order[key]
            else:
                for k in order[key].keys():
                    row[orders_header.index(k)] = order[key][k]

        orderWriter.writerow(row)


def update_orders(orders, orders_header):
    with open('orders.csv', 'w', newline='') as csvfile:
        orderWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        orderWriter.writerow(orders_header)

    for o in orders:
        write_order(o, orders_header)


def get_data_from_file():
    with open('data.json', 'r') as f:
        return json.load(f)


def update_data_file(data):
    with open('data.json', 'w') as f:
        return json.dump(data, f)


def parse_date(date_string):
    # String format :
    # 2022-05-21 13:55:48.649505
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")  # Parsing string
    return date
