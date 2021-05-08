import requests
import json

head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = "https://cdn-api.co-vin.in/api/v2/admin/location/"
r = requests.get(url+"states", headers=head)
slots = json.loads(r.content)

for sl in slots["states"]:
    print("ID "+str(sl["state_id"])+" NAME "+sl["state_name"])
state_id = input("\nEnter your state ID from above ")

r = requests.get(url+"districts/"+state_id, headers=head)
slots = json.loads(r.content)
for sl in slots["districts"]:
    print("ID "+str(sl["district_id"])+" NAME "+sl["district_name"])
print("\nNote down your district ID from above and change dist_id variable to this district ID in the cowin.py file ")