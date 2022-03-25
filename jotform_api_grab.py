import requests
from requests.auth import HTTPBasicAuth

def submission_grab():
    apiKey = "ffe10abac602b3cfc149ed8af1bc39ab"
    formID = "220585366483160"

    url = f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}&limit=1000'


    #this is used to create the json object and the data needed exists in the data->items key pairs
    response = requests.get(url=url).json()
 
    #this subs into the key value that has all submissions
    submissions = response['content']
    #print(submissions)

    #This will be the list of all the formatted submissions
    my_list = []

    #This is the loop that gets all data that you want for the json objects that will be appended to the list
    for _ in submissions:
        print('--------------------------------------------------')
        print(_)
        #this grabs all the answers that were submitted in the submission
        answers = _['answers']
        #creates a dictionary that will be converted to the json object
        my_dict = {}
        per_submission_list = []
        my_id = _['id']
        per_submission_list.append(my_id)
        #This grabs the date category
        date = _['created_at']
        date = date.split(' ')
        my_dict['date'] = date[0]
        
        #this gets the form id which will be uniform for all submissions of the same form type
        my_dict['form_id'] = _['form_id']

        #This will be used to format the answer data to get the fields we want
        for answer in answers:
            
            '''
            This try statement is used to see if there is a name and answer category because 
            some of the answer entries dont have both. Lucky for our use the only ones we 
            need are the entries that have both.
            '''

            try:
                my_name = answers[answer]['name']
                my_answer = answers[answer]['answer']
                alter_name = ''
                
                #This is used to grab the data, if it passes this conditional that is looking for ascii values then it just makes the key name the name of the given name
                if ord(my_name[0]) < 48 or ord(my_name[0]) > 57 :
                    #print('im here')
                    #print(my_name)
                    my_dict[my_name] = my_answer
                
                #This ascii arithmetic is used to get just the number values of the questions.
                else:
                    for letter in my_name:
                        if ord(letter) < 48 or ord(letter) > 57:
                            break
                        else:
                            alter_name += letter
                    my_dict[alter_name] = my_answer
                    
            #The except part is just necessary just in case an entry doesnt have a name only an answer or vice versa.
            except:
                pass
        my_dict['submission_id'] = _['id']
        per_submission_list.append(my_dict)
        my_list.append(per_submission_list)
            

    #print(my_list)

    
    for _ in my_list:
        print('----------------------------')
        print(_)
        print('----------------------------')
    print(len(my_list))

    

submission_grab()