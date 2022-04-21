import json
import boto3
import s3_methods
import webhook_integration
import api_integration




def lambda_handler(event, context):
    
    #This is the form specific ID
    print('form_id_grab')
    #print(event)
    formID = webhook_integration.form_id_grab(event)
    #This is the api key needed to interact with the jotform api
    api_key = 'ffe10abac602b3cfc149ed8af1bc39ab'
    #This is the bucket where all the jotform submissions go
    bucket_name = 'the-jotform-bucket'
    
    
    '''
    The existing_form variable references the s3_bucket_dir_exist function. 
    This function returns a boolean value and determines whether it is 
    the first time this jotform has dropped a payload into our aws environment.
    '''
    print('s3_bucket_dir_exist')
    #existing_form = s3_methods.s3_bucket_dir_exist(bucket_name, formID)
    existing_form = False
    
    
    
    #This conditional is if the directory exists. If it does then utilize the webhook for the newest entry.
    if existing_form == True:
        print('payload_json_grab')
        #This variable references the payload_json_grab function which is a part of webhook_integration.py review line 21 webhook_integration.py
        return_list = webhook_integration.payload_json_grab(event)
        
        print('json_format')
        #This variable references the json_format function which is a part of webhook_integration.py review line 56 webhook_integration.py
        form_json_list = webhook_integration.json_format(return_list)
        
        print('json_to_template_json')
        #This variable references the json_to_template_json function which is a part of the webhook_integration.py review line 104 webhook_integration.py
        clean_json_list = webhook_integration.json_to_template_json(form_json_list, formID)
        
        print('template_json_create')
        #This variable references the template_json_create function which is a part of the webhook_integration.py review line 127 webhook_integration.py
        path = webhook_integration.template_json_create(clean_json_list)
        
        print('s3_webhook_json_put')
        #This variable references the s3_webhook_json_put function which is a part of the s3_methods.py review line 48 s3_methods.py
        #s3_methods.s3_webhook_json_put(path, formID, bucket_name)
        
        result = clean_json_list[2]
    
    else:
        #This call below references teh s3_form_dir_create function within the s3_methods.py file. It creates the directory all of the json objects submissions will go.
        print('s3_form_dir_create')
        #s3_methods.s3_form_dir_create(formID, bucket_name)
        
        #This variable references the api_template_build function within the api_integration.py file. It builds the json template for a specific form.
        print('api_template_build')
        template = api_integration.api_template_build(api_key, formID)
        
        #The below variable references teh api_json_template_write function within the api_integration.py file. It writes the json template created in the previous function to a temporary directory.
        print('api_json_template_write')
        template_path = api_integration.api_json_template_write(template)
        
        #May want to do somethign just in case the template gets deleted...
        #This call below references the s3_json_template_put function within the s3_methods.py file. It puts the json template for a specified form within the template directory.
        print('s3_json_template_put')
        #s3_methods.s3_json_template_put(formID, template_path, bucket_name)
        
        #This variable references the submission_grab function within the api_integration.py file. It goes through and grabs all the previous submissions utilizing the api, 
        #and creates json objects for each submission
        print('submission_grab')
        api_json = api_integration.submission_grab(api_key, formID)
        
        #This variable references teh api_write function within the api_integration.py file. It goes through the list of generated json objects from the previous function, 
        #and writes them all to a temporary directory.
        print('api_write')
        api_json_paths = api_integration.api_write(api_json)
        
        #This call below references the api_json_put function within the s3_methods.py file. It goes through the list of temporary paths for the files created in the previous
        #function and puts all of those files within the s3 bucket. The files are put within the directory created in the first function call for the specified form.
        print('s3_api_json_put')
        #s3_methods.s3_api_json_put(api_json_paths, formID, bucket_name)
        result = api_json
        
    
    
    #this is the return to the webhook after the script is done with the payload, it returns the jot form submission
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

the_event = {'resource': '/jotform_use', 'path': '/jotform_use', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'content-type': 'multipart/form-data; boundary=------------------------7416142be687625b', 'Host': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'X-Amzn-Trace-Id': 'Root=1-62619a76-11dad9e344dc383928d8de28', 'X-Forwarded-For': '104.154.176.199', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'content-type': ['multipart/form-data; boundary=------------------------7416142be687625b'], 'Host': ['07rw8uplje.execute-api.us-east-1.amazonaws.com'], 'X-Amzn-Trace-Id': ['Root=1-62619a76-11dad9e344dc383928d8de28'], 'X-Forwarded-For': ['104.154.176.199'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '9i9u7u', 'resourcePath': '/jotform_use', 'httpMethod': 'POST', 'extendedRequestId': 'Q8USiFX4IAMFzaw=', 'requestTime': '21/Apr/2022:17:55:02 +0000', 'path': '/prod/jotform_use', 'accountId': '249689120119', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': '07rw8uplje', 'requestTimeEpoch': 1650563702449, 'requestId': '3ee9cfa7-9afa-4e3a-8ef4-670aae333937', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '104.154.176.199', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': None, 'user': None}, 'domainName': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'apiId': '07rw8uplje'}, 'body': '--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="formID"\r\n\r\n221104905354144\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="submissionID"\r\n\r\n5263729025226645533\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="webhookURL"\r\n\r\nhttps://07rw8uplje.execute-api.us-east-1.amazonaws.com/prod/jotform_use\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="ip"\r\n\r\n162.207.116.225\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="formTitle"\r\n\r\nClone of Physical Abilities JotForm Test Chev Work\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="pretty"\r\n\r\nGymnast Name:scott condo, Age:22, Skill Level:1, Coach Name:Elgin, Right Leg Flex:1, Left Leg Flex:1, Shoulder Flexibility :1, Coach Name:Elgin, 1) Leg Lifts (Max points: 10):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 2) Cast to Handstand (Max points: 15):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 3) Press to Handstand (Max points: 10):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 4) Handstand Hold (Max points: 10):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 5) Rope Climb (Max points: 12):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 5) Levers (Max points: 15):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 6) Pull Ups (Max points: 10):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 7) Stick (Max points: 6):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]], 8) Run (Max points: 6):[["#","Count/Time","Faults","Adjusted Final Score"],[1,"1","1","1"]]\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="username"\r\n\r\nbearcognition\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="rawRequest"\r\n\r\n{"slug":"submit\\/221104905354144\\/","q3_gymnastName":{"first":"scott","last":"condo"},"q42_age":"22","q41_skillLevel":"1","q18_coachName":"Elgin","q19_rightLeg":"1","q20_leftLeg":"1","q21_shoulderFlexibility":"1","q22_coachName22":"Elgin","q48_typeA48":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q49_2Cast":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q50_3Press":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q51_4Handstand":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q52_5Rope":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q53_5Levers":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q54_6Pull":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q55_7Stick":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","q56_8Run":"[[\\"#\\",\\"Count\\/Time\\",\\"Faults\\",\\"Adjusted Final Score\\"],[1,\\"1\\",\\"1\\",\\"1\\"]]","event_id":"1650563650478_221104905354144_lm919z5","path":"\\/submit\\/221104905354144"}\r\n--------------------------7416142be687625b\r\nContent-Disposition: form-data; name="type"\r\n\r\nWEB\r\n--------------------------7416142be687625b--\r\n', 'isBase64Encoded': False}
the_context = 'shween'
lambda_handler(the_event, the_context)
