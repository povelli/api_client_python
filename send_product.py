from povelli_api import post_data

store_id = 8
public_key = "b21305e7a8354f989fed1bf25d719264"
private_key = "e37dee6f43e1fb43c728bf7794fcc08f8c34463c"

url = "/e/agent/products/update"
domain = "dev.povelli.com"

products = [
    {
        'store_id': store_id,
        'code': '050200561009',
        'price': 5.50,
        'name': 'KitKat',
        'family': 'Candy',
        'size': '1 ct.',
        'manufacturer': ''
    },
]

success, response = post_data(domain, url, public_key, private_key, products)

print "Success: %s [%s]" % (success, response)
