import requests
import json
import boto3

def submission_grab(api_key, form_id):
    #The apiKey is a variable used to store the api key for the get request below.
    apiKey = api_key
    #The formID is a variable passed to the link below to grab the submissions from a specified form.
    formID = form_id
    
    #This is the url utilized for the api get request
    url = f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}&limit=1000'


    #This is the api request that grabs all of the submissions for a specified form utilizing the formID variable.
    response = requests.get(url=url).json()
 
    #This variable is assigned to the per submission poriton of the api
    submissions = response['content']

    #This will be the list of all the formatted submissions
    my_list = []

    
    #This is the loop that gets all data that you want for the json objects that will be appended to the list
    for _ in submissions:

        #this grabs all the answers that were submitted in each of the submissions
        answers = _['answers']
        #creates a dictionary that will be converted to the json object
        my_dict = {}
        #This variable below is a list that grabs essential data for each submission(id, dictionary obj)
        per_submission_list = []
        my_id = _['id']
        per_submission_list.append(my_id)
        #This grabs the date category
        date = _['created_at']
        date = date.split(' ')
        my_dict['submitted_date'] = date[0]
        
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
        #This adds the submission key value pair to the dictionary for this submission  
        my_dict['submission_id'] = _['id']
        #This adds the dictionary to the per submision list
        per_submission_list.append(my_dict)
        #This adds the list obj to the total list object
        my_list.append(per_submission_list)
            

    

    print('my List')
    print(my_list)
    #This returns the aggregate list object(the list of all submission objects)
    return my_list
    
    
def api_write(json_list):
    
    #This list variable will be used to get all of the paths to the files that are made
    path_list = []
    
    #This for loop creates the path at which the file will exist, then writes the json object to the file. It loops through all the objects within the json_list parameter. 
    for _ in json_list:
        #This variable grabs the json object from the list parameter passed.
        json_obj = _[1]
        #This variable grabs the unique identifier from the list parameter passed .
        file_name = _[0]
        #This variable makes the json object writeable to a file.
        my_obj = json.dumps(json_obj)
        #This variable is the unique path of the current submission file.
        path = f'/tmp/{file_name}.json'
        #This appends the path variable above to the path_list list object.
        path_list.append(path)
        
        #This opens up a new file with the name of the path and assigns it to a variable called myfile.
        with open(path, 'w') as myfile:
            #This call writes the json object generated above to this created file.
            myfile.write(my_obj)
        #This closes the file once written.
        myfile.close()
    print(path_list)    
    #The list of unique file paths is returned.
    return path_list
    
    
def api_template_build(api_key, form_id):
    
    '''
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
    '''
    
    #The apiKey is a variable used to store the api key for the get request below.
    apiKey = api_key
    #The formID is a variable passed to the link below to grab the submissions from a specified form.
    formID = form_id
    
    #This is the url utilized for the api get request
    url = f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}&limit=1000'


    #This is the api request that grabs all of the submissions for a specified form utilizing the formID variable.
    response = requests.get(url=url).json()
 
    #This variable is assigned to the per submission poriton of the api
    submissions = response['content']

    #This will be the list of all the formatted submissions
    my_list = []
    
    #This grabs one of the submissions from all of the jotform submissions as a template
    #If we want this to be more accurate we can grab two separate submissions down the road and compare the objects that are made.
    sample_submission = submissions[0]
    print(sample_submission)
    
    #This grabs the answers sub json object that contains all of the submissions answer entries
    the_answers = sample_submission['answers']
    #This will be the dictionary used as the template json
    template_dict = {}
    
    #This for loop loops through all of the individual question json objects within the answers json object. It will be used to add each questions shorthand, 
    #and long text to the dictionary objects. The shorthand being the key and the long text being the value.
    for answer in the_answers:
        print('=======================================')
        print(the_answers[answer])
        
        #This try statement will check to see if an answer is present. If it is then it is an actual question rather than a filler. From there,
        #it will take the long text, strip it and remove its commas. It will then make the shorthand the key and the newly formatted text the value. 
        try:
            answer_test = the_answers[answer]['answer']
            text_question = the_answers[answer]['text'].strip()
            shorthand = the_answers[answer]['name']
            template_dict[shorthand] = text_question.replace(',', '')
        #This except is just in case there is no answer present.
        except:
            print('Filler or useless question')
            pass
    
   
    print(template_dict)
    return template_dict



def api_json_template_write(template_dict):
    
    #This variable is a hardset variable of json_template. The name will not change
    file_name = 'json_template'
    #This makes the dict object parameter into a json object called my_obj
    my_obj = json.dumps(template_dict)
    #This is the path of the json template
    path = f'/tmp/{file_name}.json'
    #This creates a new file and has it as a variable of myfile
    with open(path, 'w') as myfile:
        #This writes the json object created above to the file at the specified path
        myfile.write(my_obj)
    myfile.close()
    
    #This returns the path to reference for the writing to s3 portion.
    print(path)
    return path
    
    
        
        
        
        
    
    



