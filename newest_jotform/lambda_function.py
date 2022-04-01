import json
import boto3
import s3_methods
import webhook_integration
import api_integration




def lambda_handler(event, context):
    '''
    s3_client = boto3.client('s3')
    S3_BUCKET = 'jotform-stuff'
    object_key = "test/json_template/json_template.txt"  # replace object key
    file_content = s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    print(file_content)
    '''
    #This is the form specific ID
    print('form_id_grab')
    formID = webhook_integration.form_id_grab(event)
    api_key = 'ffe10abac602b3cfc149ed8af1bc39ab'
    bucket_name = 'jotform-stuff'
    
    #The variable new_form is a boolean variable that is used to determine if it is the data from a new jotform
    print('s3_bucket_dir_exist')
    new_form = s3_methods.s3_bucket_dir_exist(bucket_name, formID)
    
    
    
    
    #dont forget to change to False
    if new_form == True:
        print('payload_json_grab')
        return_list = webhook_integration.payload_json_grab(event)
        print('json_format')
        form_json_list = webhook_integration.json_format(return_list)
        print('json_to_template_json')
        clean_json_list = webhook_integration.json_to_template_json(form_json_list, formID)
        print('template_json_create')
        path = webhook_integration.template_json_create(clean_json_list)
        print('s3_webhook_json_put')
        s3_methods.s3_webhook_json_put(path, formID, bucket_name)
        result = clean_json_list[2]
    
    else:
        print('s3_form_dir_create')
        s3_methods.s3_form_dir_create(formID, bucket_name)
        print('s3_json_template_dir_create')
        s3_methods.s3_json_template_dir_create(formID, bucket_name)
        print('api_template_build')
        template = api_integration.api_template_build(api_key, formID)
        print('api_json_template_write')
        template_path = api_integration.api_json_template_write(template)
        print('s3_json_template_put')
        s3_methods.s3_json_template_put(formID, template_path, bucket_name)
        print('submission_grab')
        api_json = api_integration.submission_grab(api_key, formID)
        print('api_write')
        api_json_paths = api_integration.api_write(api_json)
        print('s3_api_json_put')
        s3_methods.s3_api_json_put(api_json_paths, formID, bucket_name)
        result = api_json
        
    
    
    #this is the return to the webhook after the script is done with the payload, it returns the jot form submission
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
