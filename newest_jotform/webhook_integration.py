import json
import boto3
from api_integration import spreadsheet_make

def form_id_grab(event):
    
    #This grabs the body portion(the actual webhook payload) 
    event_body = event['body']
    #This event_body payload comes in the form of a string. We turn the string into a list by splitting the string on new line characters
    event_body_split = event_body.split('\n')
    
    #This loops through all of those lines in the list to find the json object with the slug. 
    for _ in event_body_split:
        #the { character is the indicator for the jot form submission that we need
        if '{' in _:
            #assigns the jot form submission to the variable we set above
            jot_form_submission = _
            #If the object is found then it will be assigned to the jot_form_submission variable then break the loop
            break
    
    #This turns the string version of the json object into a json object.
    example_json = json.loads(jot_form_submission)
    #Grabs the slug key/value pair because it contains the formID
    formID = example_json['slug']
    #Splits the slug to find the formID
    formID = formID.split('/')
    #Assigns the form id to the formID variable
    formID = formID[1]
    #Returns the formID
    return formID
  
    
def payload_json_grab(event):
    #This grabs the date/time event 
    time = event['requestContext']['requestTime'].split(':')
    #This event_body payload comes in the form of a string. We turn the string into a list by splitting the string on new line characters
    event_body = event['body']
    
    #this is the variable that the jot form submission will live in
    jot_form_submission = ''
    
    #This event_body payload comes in the form of a string. We turn the string into a list by splitting the string on new line characters
    event_body_split = event_body.split('\n')
    
    #This loops through all of those lines in the list to find the json object with the slug. 
    for _ in event_body_split:
        #the { character is the indicator for the jot form submission that we need
        if '{' in _:
            #assigns the jot form submission to the variable we set above
            jot_form_submission = _
            #If the object is found then it will be assigned to the jot_form_submission variable then break the loop
            break
    
    #This turns the string version of the json object into a json object.
    example_json = json.loads(jot_form_submission)
    
    
    #Grabs the slug key/value pair because it contains the formID
    formID = example_json['slug']
    #Splits the slug to find the formID
    formID = formID.split('/')
    #Assigns the form id to the formID variable
    formID = formID[1]
    #This gets a unique submission identifier and stores it in a variable.
    submission_id = example_json['event_id']
    #This is the list object that is used as the return value for the function.
    return_list = []
    #This appends the date portion of the date/time variable to the return list.
    return_list.append(time[0])
    #This appends the raw json object to the return list
    return_list.append(example_json)
    #This appends the formID variable to the return list
    return_list.append(formID)
    #This appends the unique submission identifier to the return list
    return_list.append(submission_id)
    
    print('================================')
    print(return_list)
    #Returns the return_list list object
    return return_list


def json_format(return_list):
    #This variable will be used as the return value for the statement
    form_json_list = []
    #This appends the formID variable to the form_json_list
    form_json_list.append(return_list[2])
    #This appends the unique submission identifier to the form_json_list
    form_json_list.append(return_list[3])
    
    #This is a dictionary that has the month abreviation as the key and the number equivalent as the value. This is necessary to format the raw date from an abreviation 
    #to a number value to match the api date.
    month_dict = {
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }
    
    #This pre_date variable is populated with the date variable passed from the payload_json_grab function.
    pre_date = return_list[0]
    #This splits the date into separate sections(day, year, month)
    pre_date = pre_date.split('/')
    #This creates the new date object. The only variable that changes is the middle portion that uses the month portion as a key to get the numeric equivalent. 
    new_date =  pre_date[2] + '-' + month_dict[pre_date[1]]+ '-' + pre_date[0]  
    
    #This takes the unedited json object from the payload and assigns it to the raw_json variable 
    raw_json = return_list[1]
    #This creates a dictionary object and assigns the first key/value pair of date->newly made date.
    cool_dict = {"date" : new_date}
    #This for loop goes through each key/value pair in the json for the end goal of making the shorthand question values.
    for _ in raw_json:
        #This splits the key and splits it on the _
        broken_key = _.split('_')
        #This try statement is necessary because sometimes there are no underscores which would make the broken_key[1] call go out of bounds
        try:
            #This grabs the shorthand
            needed_key = broken_key[1]
            answer_list = list(raw_json[_])
            if type(raw_json[_]) == dict:
                for raw_raw_json in raw_json[_]:
                    cool_dict[raw_raw_json] = raw_json[_][raw_raw_json]
            else:
                #This takes the shorthand making it the key and giving the same value to the new key in the new dictionary.
                cool_dict[needed_key] = raw_json[_]
        #This except statement is if the key is one word without underscores
        except:
            print('One word key')
            #Takes the original key and applies it to the needed_key variable
            needed_key = broken_key[0]
            #This adds the unchanged key to its original value in the new dictionary
            cool_dict[needed_key] = raw_json[_]
    
    
    
    print('================================')
    #This adds the submission_id key/pair value into the dictionary
    cool_dict['submission_id'] = return_list[3]
    #This appends the new dictionary with the shorthand keys to the form_json_list
    form_json_list.append(cool_dict)
    print(form_json_list)
    #This returns the list of the formId variable at index 0 the unique submission identifier at index 1 and the dictionary object at index 2
    return form_json_list
        
    
    
    

def json_to_template_json(form_json_list, formID):
    #This will be the list that is returned at the end of the function
    clean_json_list = []
    #This appends the formID to the clean_json_list
    clean_json_list.append(form_json_list[0])
    #This appends the unique submission identifier to the clean_json_list
    clean_json_list.append(form_json_list[1])
    
    #This variable is now the new dictionary object
    raw_json = form_json_list[2]
    #This adds the date object to a variable
    date = raw_json['date']
    #This will be the final json object that is made
    clean_json = {}
    
    #This creates a s3 client object and assigns it to the variable s3_client
    #s3_client = boto3.client('s3')
    #This is the name of the bucket where the json template lives
    S3_BUCKET = 'the-jotform-bucket'
    #This object key is the path to the template for the specified form.
    object_key = "json_templates/" + formID + "_json_template.json"  # replace object key
    #when loading in the json template, all key/value pairs must be in double quotes not single
    #file_content = json.loads(s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read())
    #this is for local testing after testing comment out line below then shift all code from the return up to here <- 1 tab
    with open('C:\\Users\\Scott\\Documents\\GitHub\\jotform\\newest_jotform\\resources\\template\\json_template.json', 'r') as local:
        
        file_content = json.loads(local.read())
        #print(json.dumps(file_content))
        #print(len(file_content))
        #print(len(raw_json))
        
        #This goes through and transforms the shorthand keys into the long text versions of each question
        for _ in file_content:
            #print(_)
            #print(file_content[_])
            #print(raw_json[_])
            answer_list = list(raw_json[_])
            if answer_list[0] == '[':
                pass
            else:
                clean_json[file_content[_]] = raw_json[_]
        for _ in raw_json:
            answer_list = list(raw_json[_])
            if answer_list[0] == '[':
                text_question = file_content[_]
                spreadsheet_dict = spreadsheet_make(raw_json[_], text_question)
                for spreadsheet_sub in spreadsheet_dict:
                    clean_json[spreadsheet_sub] = spreadsheet_dict[spreadsheet_sub]
        #This appends the new json object with the long text keys to the clean_json_list
        clean_json_list.append(clean_json)
        #This adds the submission_id key/value pair to the new dictionary
        clean_json['submission_id'] = form_json_list[1]
        #This adds the date key/value pair to the new dictionary 
        clean_json['submitted_date'] = date
        print(clean_json_list)
        #This returns the clean_json_list object with the formID variable at index[0] unique submission id variable at index[1] and the new json object at index[2]
        return clean_json_list



def template_json_create(clean_json_list):
    #This grabs the clean json list and assigns it to the variable json_list
    json_list = clean_json_list[2]
    #This takes the unique identifier and assigns it to the variable file_name
    file_name = clean_json_list[1]
    
    print('about to write')
    #This turns the dictionary object(json_list) into a writeable json object
    my_obj = json.dumps(json_list)
    #This creates a unique path to the file that is about to be created
    #uncomment this after
    #path = f'/tmp/{file_name}.json'
    path = f'C:\\Users\\Scott\\Documents\\GitHub\\jotform\\newest_jotform\\resources\\exmaple_json\\{file_name}.json'
    #This creates a new file with the unique path and assigns it to the variable myfile
    with open(path, 'w') as myfile:
        #This writes the json object to myfile
        myfile.write(my_obj)
    #This closes and saves the file
    myfile.close()
    print('file has been written')
    #This function returns the path to be referenced by the s3_functions
    return path



    

    