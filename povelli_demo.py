from sys import argv
from povelli_api import send_product_updates, delete_products, get_products, get_labels, assign_labels, unassign_labels
import povelli_api

env='dev'

if env == 'prod':
    #prod keys
    store_uid = "8a13fbf48d3a4ad6b34d46f563ca2255"
    public_key = "078a5810afe84af99dd85244dff145b1"
    private_key = "3d288feb681df8550970d9b8a4db4e55510fd286"

elif env == 'dev':
    #dev keys
    store_uid = "45bd16aa782d4db9a09f6ee1f52726a9"
    public_key = "f76534228489449d904e8d0c1b8cff90"
    private_key = "977bb7f0524343a3202fb6c6806d9ea4934d1b00"
    povelli_api.API_DOMAIN = "dev.povelli.com"

elif env == 'local':
    #local keys
    store_uid = "da30b16a063d4db8b895e6ca8b11270a"
    public_key = "076c6dc54f8f40da97a79b30bb519686"
    private_key = "8de9ecd0ee5a7083383f884f14f4fc729ba0871c"
    povelli_api.API_DOMAIN = "local.povelli.com:8083"
    povelli_api.API_PROTOCOL = "http"

products = [
    {
        'store_uid': store_uid,
        'upc': '73387809768',
        'price': 5.50,
        'name': 'KitKat',
        'family': 'Candy',
        'size': '0',
        'manufacturer': '',
    },
]

labels = [
    {
        'store_uid': store_uid,
        'label_barcode': '16777459',
    }
]

label_assignments = [
    {
        'store_uid': store_uid,
        'label_barcode': '16777459',
        'product_upc': '73387809768',
        'product_size': '2 ct.',
        'template_uid': '4d315f06a2fe4e19890ed344e1ed4df8',
    }
]

if len(argv) < 2:
    print """USAGE:
    python povelli_demo [update | delete | status | label | assign]
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
