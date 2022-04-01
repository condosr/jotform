print('event deets')
    print(event)
    print('end of event deets')
    s3 = boto3.client('s3')
    bucket_name = 'jotform-stuff'
    api_key = 'ffe10abac602b3cfc149ed8af1bc39ab'
    
    #gets the in initial data in list in the form of list
    submission_list = submission_retrival(event)
    
    #This is the json_build function that exists in file_build.py 
    submission_json = json_build(submission_list)
    
    #This is the json_write function that exists in the file_build.py
    file_name = json_write(submission_json)
    
    #The key is used for the file name inside of s3
    key = submission_json[0]
    
    #This variable is used do determine what directory the data will go into
    jot_form_id = submission_list[2]
    
    #The variable new_form is a boolean variable that is used to determine if it is the data from a new jotform
    new_form = False
    
    #This try statement is to see if a specified directory exists, if it does, then it is the data from an existing jotform if not it is a new jotform and all prior submissions need to be synced
    try: 
        s3.get_object(Bucket=bucket_name, Key=(jot_form_id+'/'))
        print(jot_form_id)
        print('I exist')
    except:
        print('i dont exist')
        new_form = True
    
    #This conditional is if the payload is from a jotform with data already in s3
    if new_form == False:    
        
        #This try statement is used to put the file made and put into temporary directory, and moves it to s3 with the name specified as event_id from the key variable above. If it doesnt work it throws a file problem exception.
        try:
            destination = jot_form_id + '/' + key
            with open(file_name, 'rb') as data:
                s3.upload_fileobj(data, bucket_name, destination)
            data.close()
            #print('done uploading to s3')
        except:
            print('file problem')
            
    #This conditional is if the payload is from a jotform that doesnt already have data in an s3 bucket
    if new_form == True:
        
        #This try statement creates the new directory for the jotform
        try:
            s3.put_object(Bucket=bucket_name, Key=(jot_form_id+'/'))
            print('created directory: ' + jot_form_id)
        except:
            print('directory creation error')
            
        #This try statement utilizes the api function i made that makes an aggregated list of all submissions in a specified jotform
        try:
            all_submissions = submission_grab(api_key, jot_form_id)
        except:
            print('api problem')
        
        #This try statement makes all of the files for all the jotform submissions then puts all of the paths in a list
        try:
            file_paths = api_write(all_submissions)
        except:
            print('file write error')
        
        #This try statement takes all of the files and puts them into the s3 bucket in its specified directory
        try:
            for _ in file_paths:
                name = _.split('/')
                name = name[2].replace('.json', '')
                #print(name)
                destination = jot_form_id + '/' + name
                with open(_, 'rb') as data:
                    s3.upload_fileobj(data, bucket_name, destination)
                data.close()
                #print(f'done uploading {_} to s3')
        except:
            print('file problem')