import requests
import os
from requests.auth import HTTPBasicAuth
import json


#yup = requests.get('https://api.planningcenteronline.com/people/v2', auth=('947f0f7e737cb7846eb65850d0eed067b4eed0786b055694a9d2a7a6a27e5e39', ''))
#print(yup)
apiKey = "ffe10abac602b3cfc149ed8af1bc39ab"
formID = "220585366483160"

# Create Base64 Encoded Basic Auth Header
#auth = HTTPBasicAuth(api_key, api_secret)

'''
headers = {
'Authorization': 'Basic ' + api_key,
'Content-Type': 'application/json'
}
'''

limit = 1000
#params = {"limit": limit}
#json_practice ={"url": "https://q0i6ebd0cj.execute-api.us-east-1.amazonaws.com/prod/fivetran_webhooks", "events": ["status"], "active": True}
#api url
url = f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}'


#this is used to create the json object and the data needed exists in the data->items key pairs
response = requests.get(url=url).json()

submissions = response['content']
my_list = []
for _ in submissions:
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    answers = _['answers']
    #print(answers)
    my_dict = {}
    date = _['created_at']
    date = date.split(' ')

    my_dict['date'] = date[0]
    my_dict['form_id'] = _['form_id']
    for answer in answers:
        
        try:
            my_name = answers[answer]['name']
            my_answer = answers[answer]['answer']
            alter_name = ''
            
            if ord(my_name[0]) < 48 or ord(my_name[0]) > 57 :
                #print('im here')
                print(my_name)
                my_dict[my_name] = my_answer
            else:
                for letter in my_name:
                    if ord(letter) < 48 or ord(letter) > 57:
                        #print('reached a letter loser')
                        break
                    else:
                        #print('add to alter')
                        alter_name += letter
                my_dict[alter_name] = my_answer
                print(alter_name)

            print(my_answer)
            print('---------------------------------------')
        except:
            pass
    my_dict['submission_id'] = _['id']
    my_list.append(my_dict)
        
    
    
#print(type(submissions))
#fun_stuff = response['data']
#fun_fun_stuff = r['attributes']['name']
'''
for _ in fun_stuff: 

    print('++++++++++++++++++++++++++++++++++++++++++++++')
    print(_)
    print('++++++++++++++++++++++++++++++++++++++++++++++')
'''
'''
for _ in response['content']:
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    print(_)
    print('++++++++++++++++++++++++++++++++++++++++++++++')
'''

print(my_list)