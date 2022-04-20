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
        s3_methods.s3_webhook_json_put(path, formID, bucket_name)
        
        result = clean_json_list[2]
    
    else:
        #This call below references teh s3_form_dir_create function within the s3_methods.py file. It creates the directory all of the json objects submissions will go.
        print('s3_form_dir_create')
        s3_methods.s3_form_dir_create(formID, bucket_name)
        
        #This variable references the api_template_build function within the api_integration.py file. It builds the json template for a specific form.
        print('api_template_build')
        template = api_integration.api_template_build(api_key, formID)
        
        #The below variable references teh api_json_template_write function within the api_integration.py file. It writes the json template created in the previous function to a temporary directory.
        print('api_json_template_write')
        template_path = api_integration.api_json_template_write(template)
        
        #May want to do somethign just in case the template gets deleted...
        #This call below references the s3_json_template_put function within the s3_methods.py file. It puts the json template for a specified form within the template directory.
        print('s3_json_template_put')
        s3_methods.s3_json_template_put(formID, template_path, bucket_name)
        
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
        s3_methods.s3_api_json_put(api_json_paths, formID, bucket_name)
        result = api_json
        
    
    
    #this is the return to the webhook after the script is done with the payload, it returns the jot form submission
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

the_event = {'resource': '/jotform_use', 'path': '/jotform_use', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'content-type': 'multipart/form-data; boundary=------------------------14248c4431cd1012', 'Host': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'X-Amzn-Trace-Id': 'Root=1-625ebb4e-597fc7a173247bcd08c38348', 'X-Forwarded-For': '34.67.64.5', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'content-type': ['multipart/form-data; boundary=------------------------14248c4431cd1012'], 'Host': ['07rw8uplje.execute-api.us-east-1.amazonaws.com'], 'X-Amzn-Trace-Id': ['Root=1-625ebb4e-597fc7a173247bcd08c38348'], 'X-Forwarded-For': ['34.67.64.5'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '9i9u7u', 'resourcePath': '/jotform_use', 'httpMethod': 'POST', 'extendedRequestId': 'Q1I0PER6oAMFy_A=', 'requestTime': '19/Apr/2022:13:38:22 +0000', 'path': '/prod/jotform_use', 'accountId': '249689120119', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': '07rw8uplje', 'requestTimeEpoch': 1650375502134, 'requestId': '4a3da23a-fb85-4e7e-90c0-7cf34730c77d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '34.67.64.5', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': None, 'user': None}, 'domainName': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'apiId': '07rw8uplje'}, 'body': '--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="formID"\r\n\r\n220795483570059\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="submissionID"\r\n\r\n5261847016602722900\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="webhookURL"\r\n\r\nhttps://07rw8uplje.execute-api.us-east-1.amazonaws.com/prod/jotform_use\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="ip"\r\n\r\n70.186.130.66\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="formTitle"\r\n\r\nPhysical Abilities Test\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="pretty"\r\n\r\nGymnast Name:Scott Condo, Age:22, Current Level:Novice, Date:04 19 2022, :Array Array Array, :Array Array Array Array Array Array Array Array Array\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="username"\r\n\r\nbearcognition\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="rawRequest"\r\n\r\n{"slug":"submit\\/220795483570059\\/","q3_gymnastName":{"first":"Scott","last":"Condo"},"q4_age":"22","q5_currentLevel":"Novice","q17_date":{"month":"04","day":"19","year":"2022"},"q15_typeA15":[["3","elgin"],["4","elgin"],["5","elgin"]],"q14_typeA":[["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"],["1","1","1","elgin"]],"event_id":"1650375370811_220795483570059_KKv0Erp","path":"\\/submit\\/220795483570059"}\r\n--------------------------14248c4431cd1012\r\nContent-Disposition: form-data; name="type"\r\n\r\nWEB\r\n--------------------------14248c4431cd1012--\r\n', 'isBase64Encoded': False}
the_context = 'shween'
lambda_handler(the_event, the_context)
