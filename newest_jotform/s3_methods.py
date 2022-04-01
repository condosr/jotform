import boto3

s3 = boto3.client('s3')

def s3_form_dir_create(formID, bucket_name):
    try:
        s3.put_object(Bucket=bucket_name, Key=formID+'/')
        print('created directory: ' + formID)
    except:
        print('directory creation error')

def s3_json_template_dir_create(formID, bucket_name):
    #This try statement creates the new directory for the jotform
    try:
        the_key = formID+'/'+'json_template'+'/'
        s3.put_object(Bucket=bucket_name, Key=the_key)
        print('created directory: ' + the_key)
        
    except:
        print('directory creation error')

def s3_json_template_put(formID, file_name, bucket_name):
    print('*****************************')
    print(file_name)
    try:
        destination = formID + '/' + 'json_template' + '/' + 'json_template'
        with open(file_name, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, destination)
        data.close()
        
    except:
        print('file problem')

def s3_api_json_put(file_paths, formID, bucket_name):
    #This try statement takes all of the files and puts them into the s3 bucket in its specified directory
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
    try: 
        s3.get_object(Bucket=bucket_name, Key=(formID+'/'))
        print('*************************************')
        print('I exist')
        return True
    except:
        print('*************************************')
        print('i dont exist')
        return False