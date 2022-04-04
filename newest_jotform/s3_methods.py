import boto3

#This will be used as a universal variable. The s3 variable contains a s3 client object from boto3
s3 = boto3.client('s3')

def s3_form_dir_create(formID, bucket_name):
    #This try statement tries to build a directory of a specified path.
    try:
        s3.put_object(Bucket=bucket_name, Key=formID+'/')
        print('created directory: ' + formID)
    #This except statement is just in case the directory already exists or something in the creation process went wrong.
    except:
        print('directory creation error')

#This function may not be needed
'''
def s3_json_template_dir_create(formID, bucket_name):
    #This try statement creates the new directory for the jotform
    try:
        the_key = formID+'/'+'json_template'+'/'
        s3.put_object(Bucket=bucket_name, Key=the_key)
        print('created directory: ' + the_key)
        
    except:
        print('directory creation error')
'''

def s3_json_template_put(formID, file_name, bucket_name):
    print('*****************************')
    print(file_name)
    #This try statement puts a json template in the json_template directory. It will have a unique name because it has the formID as a header. 
    #There will only be 1 template per form.
    try:
        destination = 'json_templates/' + formID + '_json_template.json'
        with open(file_name, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, destination)
        data.close()
    
    #This except statement is just in case the creation of the file messes up, or if the file already exists
    except:
        print('file problem')


def s3_api_json_put(file_paths, formID, bucket_name):
    #This try statement takes all of the files from the intial api request and puts them into the s3 bucket in its specified directory
    try:
        for _ in file_paths:
            name = _.split('/')
            name = name[2].replace('.json', '')
            destination = formID + '/' + name
            with open(_, 'rb') as data:
                s3.upload_fileobj(data, bucket_name, destination)
            data.close()

    except:
        print('file problem')

def s3_webhook_json_put(tmp_path, formID, bucket_name):
    #This try statement takes the json object created from the webhook, and puts it in the directory based on formID
    try:
        name = tmp_path.split('/')
        name = name[2].replace('.json', '')
        destination = formID + '/' + name
        with open(tmp_path, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, destination)
        data.close()
        print('done uploading to s3')
    except:
        print('file problem')

def s3_bucket_dir_exist(bucket_name, formID):
    #This try statement is used to see if a bucket exists. This will be used to see if we need to utilize the api or the webhook creation method
    try: 
        s3.get_object(Bucket=bucket_name, Key=(formID+'/'))
        print('*************************************')
        print('I exist')
        return True
    except:
        print('*************************************')
        print('i dont exist')
        return False