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
    existing_form = True
    
    
    
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

the_event = {'resource': '/jotform_use', 'path': '/jotform_use', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'content-type': 'multipart/form-data; boundary=------------------------b6726c32637fdf4e', 'Host': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'X-Amzn-Trace-Id': 'Root=1-6266b547-02df53cb2f1be55407e2f325', 'X-Forwarded-For': '35.239.114.60', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'content-type': ['multipart/form-data; boundary=------------------------b6726c32637fdf4e'], 'Host': ['07rw8uplje.execute-api.us-east-1.amazonaws.com'], 'X-Amzn-Trace-Id': ['Root=1-6266b547-02df53cb2f1be55407e2f325'], 'X-Forwarded-For': ['35.239.114.60'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '9i9u7u', 'resourcePath': '/jotform_use', 'httpMethod': 'POST', 'extendedRequestId': 'RJFDJGxhoAMFXnQ=', 'requestTime': '25/Apr/2022:14:50:47 +0000', 'path': '/prod/jotform_use', 'accountId': '249689120119', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': '07rw8uplje', 'requestTimeEpoch': 1650898247194, 'requestId': '5054880c-61eb-4f60-bcb3-456fa7732cbf', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '35.239.114.60', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': None, 'user': None}, 'domainName': '07rw8uplje.execute-api.us-east-1.amazonaws.com', 'apiId': '07rw8uplje'}, 'body': '--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="formID"\r\n\r\n221144600480140\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="submissionID"\r\n\r\n5267074469613966508\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="webhookURL"\r\n\r\nhttps://07rw8uplje.execute-api.us-east-1.amazonaws.com/prod/jotform_use\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="ip"\r\n\r\n71.68.176.169\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="formTitle"\r\n\r\nClone of test form for fivetran\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="pretty"\r\n\r\nName:scott condo, Athlete ID:8675309, 1.  I struggle to consistently train at a high level of intensity.:Never, 2.  When feeling sluggish, I often perform worse.:Seldom, 3.  I often view practices as unhelpful or a waste of time.:Never, 4.  I struggle to feel motivated as an athlete.:Always, 5.  When I fail to reach my goal, I lose motivation to keep trying.:At Times, 6.  I find it hard to motivate myself for training.:Seldom, 7.  I tend to struggle with seeing value in our training sessions.:Often, 8.  I don\'t really notice when I feel a little stressed during games.:Always, 9.  I\'m not sure what causes poor performance.:Never, 10.  I don\'t really know how to mentally prepare for a game.:Seldom, Name:Scott  Condo, Email:scottcondo13@gmail.com, Address:244 wicked wasp lane  chairman  CA 63442, Phone Number:(202) 414-9834, eazy point:Monday, Apr 25, 2022 04:00 PM-05:00 PM America/New_York (GMT-04:00), the goodz:<table align="left" cellpadding="0" cellspacing="0" border="0"><tr><td><ul style=\'padding-left:10px\'><li>Product Name (Amount: 10.00 USD, Quantity: 1) </li></ul>Total: $10.00<br></td></tr></table>, favorite song?:total eclipse of the heart, quick what color are my underwear?:brown, what is the move?:weak knees, which limb do you like the most?:left arm, which state is coolest?:kansas, how many licks does it take to get to the center of a tootsie pop?:332, Time:05:55 05 55 AM, how awesome is the tech team?:5, how cool is scott?:1, Type a question:3\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="username"\r\n\r\nbearcognition\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="rawRequest"\r\n\r\n{"slug":"submit\\/221144600480140\\/","q28_name":{"first":"scott","last":"condo"},"q3_athleteId":"8675309","q13_1I":"Never","q19_2When":"Seldom","q20_3I":"Never","q21_4I":"Always","q22_5When22":"At Times","q23_6I":"Seldom","q24_7I24":"Often","q25_8I25":"Always","q26_9Im":"Never","q27_10I":"Seldom","q31_name31":{"first":"Scott ","last":"Condo"},"q32_email":"scottcondo13@gmail.com","q33_address":{"addr_line1":"244 wicked wasp lane","addr_line2":"","city":"chairman ","state":"CA","postal":"63442"},"q34_phoneNumber":{"full":"(202) 414-9834"},"q36_eazyPoint":{"date":"2022-04-25 16:00","duration":"60","timezone":"America\\/New_York (GMT-04:00)"},"payment_total_checksum":"10","q37_theGoodz":{"0":{"id":"1000"},"special_1000":{"item_0":"1"},"products":[{"productName":"Product Name","unitPrice":10,"currency":"USD","quantity":1,"subTotal":10}],"totalInfo":{"totalSum":10,"currency":"USD"}},"q38_favoriteSong":"total eclipse of the heart","q39_quickWhat":"brown","q41_whatIs":"weak knees","q42_whichLimb":"left arm","q43_whichState":["kansas"],"q44_howMany":"332","q45_time":{"timeInput":"05:55","hourSelect":"05","minuteSelect":"55","ampm":"AM"},"q48_howAwesome":"5","q49_howCool":"1","q47_typeA47":"3","event_id":"1650897326645_221144600480140_aGu8qm7","path":"\\/submit\\/221144600480140"}\r\n--------------------------b6726c32637fdf4e\r\nContent-Disposition: form-data; name="type"\r\n\r\nWEB\r\n--------------------------b6726c32637fdf4e--\r\n', 'isBase64Encoded': False}
the_context = 'shween'
lambda_handler(the_event, the_context)
