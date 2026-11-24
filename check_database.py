
from database import get_all_data

records = get_all_data()

print("Total stock records:", len(records))

for record in records[:5]:
    print(record)
