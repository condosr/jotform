import json
import boto3

def form_id_grab(event):
    event_body = event['body']
    event_body_split = event_body.split('\n')
    for _ in event_body_split:
        #the { character is the indicator for the jot form submission that we need
        if '{' in _:
            #assigns the jot form submission to the variable we set above
            jot_form_submission = _
            #sets the done variable to true not allowing the conditional to activate
            #done = True
            break
    example_json = json.loads(jot_form_submission)
    formID = example_json['slug']
    formID = formID.split('/')
    formID = formID[1]
    return formID
    
def payload_json_grab(event):
    # event['body'] is the total jot form submission payload
    time = event['requestContext']['requestTime'].split(':')
    event_body = event['body']
    
    #this is the variable that the jot form submission will live in
    jot_form_submission = ''
    
    #split the payload into a list of strings using the new line character
    event_body_split = event_body.split('\n')
    
    for _ in event_body_split:
        #the { character is the indicator for the jot form submission that we need
        if '{' in _:
            #assigns the jot form submission to the variable we set above
            jot_form_submission = _
            #sets the done variable to true not allowing the conditional to activate
            #done = True
            break
    print('-------------------------------------------------------------')
    print(jot_form_submission)
    example_json = json.loads(jot_form_submission)
    print(example_json)
    print(time)
    
    print('-------------------------------------------------------------')
    formID = example_json['slug']
    formID = formID.split('/')
    formID = formID[1]
    submission_id = example_json['event_id']
    return_list = []
    return_list.append(time[0])
    return_list.append(example_json)
    return_list.append(formID)
    return_list.append(submission_id)
    
    print('================================')
    print(return_list)
    return return_list

def json_format(return_list):
    form_json_list = []
    form_json_list.append(return_list[2])
    form_json_list.append(return_list[3])
    
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
    #print('date stuff =================================')
    #print(return_list[0])
    pre_date = return_list[0]
    pre_date = pre_date.split('/')
    new_date =  pre_date[2] + '-' + month_dict[pre_date[1]]+ '-' + pre_date[0]  
    #print('this is the new date =======================================')
    #print(new_date)
    
    raw_json = return_list[1]
    cool_dict = {"date" : new_date}
    for _ in raw_json:
        broken_key = _.split('_')
        try:
            needed_key = broken_key[1]
            cool_dict[needed_key] = raw_json[_]
        except:
            print('no change needed')
            needed_key = broken_key[0]
            cool_dict[needed_key] = raw_json[_]
    form_json_list.append(cool_dict)
    
    print('================================')
    
    cool_dict['submission_id'] = return_list[3]
    print(form_json_list)
    return form_json_list
        
    
    
    

def json_to_template_json(form_json_list, formID):
    clean_json_list = []
    clean_json_list.append(form_json_list[0])
    clean_json_list.append(form_json_list[1])
    raw_json = form_json_list[2]
    clean_json = {}
    
    s3_client = boto3.client('s3')
    S3_BUCKET = 'jotform-stuff'
    object_key = f"{formID}/json_template/json_template"  # replace object key
    #when loading in the json template, all key/value pairs must be in double quotes not single
    file_content = json.loads(s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read())
    print(json.dumps(file_content))
    
    for _ in file_content:
        clean_json[file_content[_]] = raw_json[_]
    clean_json_list.append(clean_json)
    clean_json['submission_id'] = form_json_list[1]
    print(clean_json_list)
    return clean_json_list

def template_json_create(clean_json_list):
    json_list = clean_json_list[2]
    file_name = clean_json_list[1]
    print('about to write')
    my_obj = json.dumps(json_list)
    path = f'/tmp/{file_name}.json'
    with open(path, 'w') as myfile:
        myfile.write(my_obj)
    myfile.close()
    print('file has been written')
    return path
    