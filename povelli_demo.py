from sys import argv
from povelli_api import send_product_updates, delete_products, get_products, get_labels, assign_labels, unassign_labels

store_uid = "45bd16aa782d4db9a09f6ee1f52726a9"
public_key = "f76534228489449d904e8d0c1b8cff90"
private_key = "977bb7f0524343a3202fb6c6806d9ea4934d1b00"

products = [
    {
        'store_uid': store_uid,
        'upc': '050200561009',
        'price': 5.50,
        'name': 'KitKat',
        'family': 'Candy',
        'size': '1 ct.',
        'manufacturer': '',
    },
]

labels = [
    {
        'store_uid': store_uid,
        'label_barcode': '33554474',
    }
]

label_assignments = [
    {
        'store_uid': store_uid,
        'label_barcode': '33554474',
        'product_upc': '050200561009',
        'product_size': '2 ct.',
        'template_uid': '4d315f06a2fe4e19890ed344e1ed4df8',
    }
]

if len(argv) < 2:
    print """USAGE:
    python povelli_demo [update | delete | status]
"""
    exit(0)

elif argv[1] == 'update':
    success, response = send_product_updates(public_key, private_key, products)

elif argv[1] == 'delete':
    success, response = delete_products(public_key, private_key, products)

elif argv[1] == 'status':
    success, response = get_products(public_key, private_key, products)

elif argv[1] == 'label':
    success, response = get_labels(public_key, private_key, labels)

elif argv[1] == 'assign':
    success, response = assign_labels(public_key, private_key, label_assignments)

elif argv[1] == 'unassign':
    success, response = unassign_labels(public_key, private_key, labels)

print "Success: %s [%s]" % (success, response)
