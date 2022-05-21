# PizzaAPI
Basic API for order managment. Allows a user to place an order containing a list of pizzas id, see an existing order giving its id, cancel an order, and more.

## end points list:

* __GET /pizza__
returns the list of all available pizzas

* __GET /pizza/<pizza_id>__
returns a specific pizza including its toppings.

* __POST /order__
places an order.  
required body:
```json
{
    "pizzas": [],
    "takeaway": true,
    "payment_type": "",
    "customer_id": 0,
    "note": "",
    "delivery_address": {
        "street": "",
        "city": "",
        "country": "",
        "zipcode": ""
    }
}
```

* __GET /order/<order_id>__
returns information about the given order

* __PUT /order/cancel/<order_id>__
cancels the given order. (sets the status to 'Cancelled')

* __GET /order/deliverytime/<order_id>__
returns information about the given order including the time left before delivery

