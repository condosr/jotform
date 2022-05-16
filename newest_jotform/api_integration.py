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
        #This grabs only the date portion from the date/time obj
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
            
            #This try except statement creates a dictionary based on what is passed. If the value of the key value pair is just a string/int then it will
            #Execute as normal or else it will fall into one of the specialized conditionals
            try:
                
                #this takes the long hand version of a specified question and stips the white space and assigning it to the my_name variable
                my_name = answers[answer]['text'].strip()
                #this takes the variable above and replaces all commas with nospace
                my_name = my_name.replace(',', '')
                #this conditional is necessary just in case the text field is blank
                if my_name == "":
                    #if it is blank it just takes the shorthand version instead as the name
                    my_name = answers[answer]['name']
                #This grabs the answer from the answer key/pair value
                my_answer = answers[answer]['answer']
                #This turns my_answer into a list if possible(mostly if its a string)
                try:
                    my_answer_list = list(my_answer)
                except:
                    print('not list mutable')
                #this looks to see if the first char in the string is a [. If it is, then it is a spreadsheet typed object and will be dealt with using the spreadsheet_dict function
                if my_answer_list[0] == '[':
                    #This calls the spreadsheet_dict function passing the answer and the question as parameters
                    spreadsheet_dict = spreadsheet_make(my_answer, my_name)
                    #This loops through the dictionary that is returned from the spreadsheet_dict function and adds all elements into the dictionary object
                    for spreadsheet_sub in spreadsheet_dict:
                        my_dict[spreadsheet_sub] = spreadsheet_dict[spreadsheet_sub]

                #new elif statement to catch if a answer is a dictionary type and append all the keys to the master dictionary
                elif type(my_answer) == dict:
                    for sub_answer in my_answer:
                        my_dict[sub_answer] = my_answer[sub_answer]
                #this elif statement looks to see if the answer is a list. If it is it will turn the list into a string with all answers separated by commas 
                elif type(my_answer) == list:
                    temp_string = ''
                    for element in range (len(my_answer)):
                        if len(my_answer) == 2:
                            temp_string = temp_string + my_answer[element] + ', ' + my_answer[element + 1]
                            break    
                        elif element == len(my_answer) - 1 or element == 0:
                            temp_string = temp_string + my_answer[element]
                        elif element == len(my_answer) - 2:
                            temp_string = temp_string + ', ' + my_answer[element] + ', '
                        else:
                            temp_string = temp_string + ', ' + my_answer[element]
                    my_dict[my_name] = temp_string
                #this last statement is if there is no changes needed and just adds the key/pair value of question and answer
                else:
                    my_dict[my_name] = my_answer
            
                    
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
            my_answer_list = list(answer_test)
            #this conditional is needed in case the text field is blank
            if text_question == "":
                text_question = shorthand
            #need an elif statement for json objects as value pairs
            elif type(answer_test) == dict:
                for sub_answers in answer_test:
                    template_dict[sub_answers] = sub_answers
            #elif my_answer_list[0] == '[':
                    #spreadsheet_dict = spreadsheet_make(answer_test, text_question)
                    #for spreadsheet_sub in spreadsheet_dict:
                        #template_dict[spreadsheet_sub] = spreadsheet_sub
            else:
                template_dict[shorthand] = text_question.replace(',', '')
        #to here
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
    
    
#Function is fragile and will need work on the string manipulation
def spreadsheet_make(spreadsheet_answer, spreadsheet_name):
    #This will be the list of all of the created objects
    return_dict = {}
    #This splits the string response into a character list
    the_list = list(spreadsheet_answer)
    #print('?????????????????????????????????????????????????')
    #The count is necessary to make the dictionary of the different spreadsheet submissions item with the key 1 will always be fill because that is the umbrella list
    the_count = 0
    #This will be the initial dictionary with the sloppy items
    the_dict = {} 
    #This string will capture the data between lists
    the_string = ''
    #This for loop goes through and breaks up all the lists
    for _ in range(len(the_list)):
        #this conditional looks for an open bracket signifying the start of a list(this may be troublesome if an open bracket is put into a question or answer)
        if the_list[_] ==  '[':
            #This increases the count to keep the keys for each list unique
            the_count += 1
            #This sets an initial value for each list that will be changed later
            the_dict[the_count] = 'fill'
            #Sets the string to empty string to keep the list items clean
            the_string = ''
        #This conditional catches the end of a list
        elif the_list[_] == ']':
            #this adds the string of all contents in the list to the dictionary to the key
            the_dict[the_count] = the_string
        else:
            #This adds all contents of a list to a string 
            the_string += the_list[_]
    #This for loop goes through each dictionary and turns the strings into lists(this is a risky/fragile for loop because if there is a comma within the answer it will make it a separate list item)
    for _ in the_dict:
        #This looks to make sure that we arent looking at an item that isnt list contents
        if not the_dict[_] == 'fill':
            #The entries are surroudned in double quotes that have to be removed thus the replace
            dic = the_dict[_]#.replace('"', '')
            #this turns the string into a list splitting on commas
            #print('==============')
            #print(dic)
            the_split = dic.split(',\"')
            the_splitter = []
            for o in the_split:
                yo = o.replace('"','')
                the_splitter.append(yo)

            the_dict[_] = the_splitter
    the_final_list = []
    for _ in the_dict:
        if not the_dict[_] == 'fill':
            the_final_list.append(the_dict[_])
    for _ in range(len(the_final_list[0])):
        #print('building the dictionary')
        #print(_)
        if _ == 0:
            pass
        else:
            my_key = spreadsheet_name + ' ' + the_final_list[0][_]
            #print(my_key)
            return_dict[my_key] = the_final_list[1][_]
    
    #print('*********************************************')
    #print(the_final_list)    
    print(return_dict)
    return return_dict

    
        
        
        
        
    
    



