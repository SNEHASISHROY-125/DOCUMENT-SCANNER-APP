import codegen as mn
from datetime import datetime

# print(mn.ean13_data)

# mn.generate_qr_code("https://fudemy.me")

# print('abdcfgrt'.isdigit())
def get_time() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

l = [9,0,'d']
l.insert(2,1)
print(l)