import requests
import json
import boto3

def submission_grab(api_key, form_id):
    apiKey = api_key
    formID = form_id

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
        my_dict['submission_id'] = _['form_id']

        #This will be used to format the answer data to get the fields we want
        name_coming = False
        for answer in answers:
            
            '''
            This try statement is used to see if there is a name and answer category because 
            some of the answer entries dont have both. Lucky for our use the only ones we 
            need are the entries that have both.
            '''
            name_coming = False
            #print('111111111111111111111111111111111111111111111111111')
            
            try:
                #print('................................................')
                
                my_name = answers[answer]['text'].strip()
                my_name = my_name.replace(',', '')
                my_answer = answers[answer]['answer']
                my_dict[my_name] = my_answer
                #print('................................................')
                    
            #The except part is just necessary just in case an entry doesnt have a name only an answer or vice versa.
            except:
                pass
            
        my_dict['submission_id'] = _['id']
        per_submission_list.append(my_dict)
        my_list.append(per_submission_list)
            

    

    print('my List')
    print(my_list)
    
    return my_list
    
    
def api_write(json_list):
    path_list = []
    for _ in json_list:
        json_obj = _[1]
        file_name = _[0]
        my_obj = json.dumps(json_obj)
        path = f'/tmp/{file_name}.json'
        path_list.append(path)
        
        with open(path, 'w') as myfile:
            myfile.write(my_obj)
        myfile.close()
    print(path_list)    
    return path_list
    
    
def api_template_build(api_key, form_id):
    apiKey = api_key
    formID = form_id

    url = f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}&limit=1000'

    #this is used to create the json object and the data needed exists in the data->items key pairs
    response = requests.get(url=url).json()
 
    #this subs into the key value that has all submissions
    submissions = response['content']
    #print(submissions)

    #This will be the list of all the formatted submissions
    my_list = []
    sample_submission = submissions[0]
    print(sample_submission)
    the_answers = sample_submission['answers']
    template_dict = {}
    for answer in the_answers:
        #print('=======================================')
        #print(_[answer])
        try:
            answer_test = the_answers[answer]['answer']
            text_question = the_answers[answer]['text'].strip()
            shorthand = the_answers[answer]['name']
            template_dict[shorthand] = text_question.replace(',', '')
        except:
            pass
    
    #for _ in submissions:

        #this grabs all the answers that were submitted in the submission
        #answers = _['answers']
        #creates a dictionary that will be converted to the json object
        #template_dict = {}
        #for answer in _:
            #print('=======================================')
            #print(_[answer])
            #try:
                #answer_test = _[answer]['answer']
                #text_question = _[answer]['text'].strip()
                #template_dict[_[answer]['name']] = text_question.replace(',', '')
            #except:
                #pass
    print(template_dict)
    return template_dict



def api_json_template_write(template_dict):
    file_name = 'json_template'
    my_obj = json.dumps(template_dict)
    path = f'/tmp/{file_name}.json'
    with open(path, 'w') as myfile:
        myfile.write(my_obj)
    myfile.close()
    
    print(path)
    return path
    
    
        
        
        
        
    
    



