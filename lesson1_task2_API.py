import requests
from pprint import pprint
import json

#import vk
#друзья в группе

access_token_vk = '29c65581baf7b7ea74866afd97b0b687483c304b1010cea718668ce385e18561036545927fc3819ae4894'
user_id = '7785447'

vk_link = 'https://api.vk.com/method/groups.getMembers'

ver = '5.21'
group_id = '48089475'
fields = 'sex,bdate,city'
filter = 'friends'

group_params = {'group_id': group_id,
                'v': ver,
                'fields': fields,
                'filter': filter,
                'access_token': access_token_vk}

response = requests.get(vk_link,params=group_params)
if response.ok:
    data = response.json()
    pprint(data)
    with open('response_vk.json', 'w') as f:
         f.write(json.dumps(data))