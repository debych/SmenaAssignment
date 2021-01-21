import requests
import re


def getFilename_fromCd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


# data = {"id": 123123123123123,
#         "price": 655,
#         "items": [{"name": "Ролли",
#                    "quantity": 2,
#                    "unit_price": 322},
#                   {"name": "Нереальная питса",
#                    "quantity": 1,
#                    "unit_price": 333}],
#         "address": "дабадбадбадб",
#         "client": {"name": "Кекер",
#                    "phone": 9173332222},
#         "point_id": 2}
# r = requests.post('http://localhost/api/create_checks/', json=data)
# print(r.json(), r.status_code)

kitchen_printer_key = '12312j82d1p98d981'
client_printer_key = '1q1q1q1q1q1q1'

r = requests.get('http://localhost/api/new_checks/{}'.format(kitchen_printer_key))
print(r.json(), r.status_code)
if r.status_code == 200:
    checks_id = r.json()['checks']
    for check_id in checks_id:
        r = requests.get('http://localhost/api/check/{}/{}'.format(kitchen_printer_key, check_id))
        filename = getFilename_fromCd(r.headers.get('content-disposition'))
        open(filename, 'wb').write(r.content)
else:
    print(r.json())

# r = requests.get('http://localhost/api/check/{}/{}'.format(kitchen_printer_key, '24'))
# if r.status_code == 200:
#     filename = getFilename_fromCd(r.headers.get('content-disposition'))
#     open(filename, 'wb').write(r.content)
# else:
#     print(r.json())

#
# r = requests.get('http://localhost/api/new_checks/{}'.format(client_printer_key))
# checks_id = r.json()['checks']
# for check_id in checks_id:
#     r = requests.get('http://localhost/api/check/{}/{}'.format(client_printer_key, check_id))
#     filename = getFilename_fromCd(r.headers.get('content-disposition'))
#     open(filename, 'wb').write(r.content)
