from sys import argv
import traceback
import csv
import chardet
import povelli_api

def read_csv(csv_filename):
    with open(csv_filename, 'r') as product_file:
        content = product_file.read()
    
        try:
            encoding = chardet.detect(content)['encoding']
            if encoding != 'utf-8':
                content = content.decode(encoding, 'replace').encode('utf-8')
        except:
            print(traceback.format_exc())

        first_line = content.partition("\n")[0]
        dialect = csv.Sniffer().sniff(first_line)
        #dialect.delimiter = ','
        dialect.skipinitialspace = True

        row_count = 0
        for row in csv.DictReader(content.splitlines(), dialect=dialect, restkey='-unknown-', restval=''):
            row_count += 1
            yield row

def format_row(store_uid, row):
    product = {
            'store_uid': store_uid,
            'upc': row.get('upc'),
            'price': row.get('price'),
            'name': row.get('name'),
            'family': row.get('family', ''),
            'size': row.get('size'),
        }
    return product
    
    
try:
    _, private_key, public_key, store_uid, csv_filename = argv
except ValueError:
    print("USAGE:\n\tpython %s <private_key> <public_key> <store_uid> <csv_file_path>" % argv[0])
    exit(-1)

products = []
for row in read_csv(csv_filename):
    products += [format_row(store_uid, row)]
    
print ("Uploading %s products..." % len(products))

success, response = povelli_api.send_product_updates(public_key, private_key, products)

print (response)
print ("Done [success=%s]" % success)
