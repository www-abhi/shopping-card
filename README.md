# Shopping Cart API

This repository contains the example code for a Shopping Cart API Assignment, using MongoDB, PyMongo, JWT authentication with Flask. The Access Token has a life of two hours post creation.

## Tasks

- Create a Cart with username and paasword and return a JWT Token.
- Adds an item to shopping cart.
- Lists all items in the shopping cart
- Finds an items in the shopping cart.
- Removes an item to shopping cart.
- Removes all item from shopping cart.

## Setup

1. Clone this repository.
2. Create a virtualenv and activate.
3. Install requirement packages.
4. Start the Flask application on your original terminal window: `flask run`.
5. Go to `http://localhost:5000/login`

## Methods

### Creating a shopping cart

```bash
curl --user "<username>:<password>" \
	--request GET \
	http://127.0.0.1:5000/login
```

###### Returns an Access Token

### Adding an item to cart

```bash
curl -X POST \
  http://localhost:5000/cart \
  -H 'Content-Type: application/json' \
  -H 'jwt-token: <access-token>' \
  -d "{
	\"name\": \"<product name>\",
	\"price\": \"<product price>\",
	\"quantity\": \"<product quantity>\"
	}"
```

### Listing all items from cart

```bash
curl -X GET \
  	http://localhost:5000/cart \
  	-H 'jwt-token: <access-token>'
```

### Get an item from cart

```bash
curl -X GET \
	http://127.0.0.1:5000/cart/<item_id> \
  	-H 'jwt-token: <access-token>'
```

### Empty the cart

```bash
curl -X DELETE \
  http://127.0.0.1:5000/cart \
  -H 'jwt-token: <access-token>'
```

### Remove an Item from Cart

```bash
curl -X DELETE \
  http://127.0.0.1:5000/cart/<item_id> \
  -H 'jwt-token: <access-token>'
```

## Some example usage for Contact API

##### Creating a shopping cart

```bash
curl --user "abhi:kumar" \
	--request GET \
	http://127.0.0.1:5000/login
```

###### Response

```JSON
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8"}
```

##### Adding an item to shopping cart

```bash
curl -X POST
http://127.0.0.1:5000/cart
	-H "jwt-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8"
	-H "Content-Type: application/json"
	-d "{
		\"name\":\"Sugar\",
		\"price\":\"50\",
		\"quantity\":\"5\"
		}"
```

###### Response

```JSON
{"message":"Item added to Cart"}
```

##### Remove an Item from Cart

```bash
curl -X DELETE \
http://127.0.0.1:5000/cart/5f437bdb0d7508fd0cc146a5
-H "jwt-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8"
```

###### Response

```JSON
{"message":"Item removed from cart"}
```

##### Empty the cart

```bash
curl -X DELETE \
http://127.0.0.1:5000/cart \
-H "jwt-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8"
```

```JSON
{"message":"All items removed"}
```

##### Get list of all items from cart

```bash
curl -X GET \
	http://127.0.0.1:5000/cart \
	-H 'jwt-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8'
```

###### Response

```JSON
[
	{
		"_id":{"$oid":"5f437fa40d7508fd0cc146a7"},"product_name":"pillow","product_price":"3000","product_quantity":"2","user_id":"5f4376d26c3328027736e52d"
	},
	{
		"_id":{"$oid":"5f4386bfadbbccf7f58778da"},"product_name":"Sugar","product_price":"50","product_quantity":"5","user_id":"5f4376d26c3328027736e52d"
	}
]
```

##### Get an item from cart

```bash
curl -X GET \
	http://127.0.0.1:5000/cart/5f437fa40d7508fd0cc146a7 \
	-H 'jwt-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTgyNjQwNTAsImlhdCI6MTU5ODI1Njg1MCwidXNlcl9pZCI6IjVmNDM3NmQyNmMzMzI4MDI3NzM2ZTUyZCJ9.UWMHbjG2sTxWyD6CjGhtbg-1KTi_kHTDQjjj3MWbUg8'
```

###### Response

```JSON
{
	"_id":{"$oid":"5f437fa40d7508fd0cc146a7"},"product_name":"pillow",
	"product_price":"3000",
	"product_quantity":"2",	"user_id":"5f4376d26c3328027736e52d"
}
```
