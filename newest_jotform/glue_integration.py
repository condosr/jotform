import boto3


glue = boto3.client('glue')
def db_make(formID):
    db_name = formID + '_db'
    response = glue.create_database(
    DatabaseInput={
        'Name': db_name,
        'Description': 'This db will be used to host jotform data',
    }
    )

def crawler_make(formID):
    '''
    Schedule='string', #may only need to crawl once
    Configuration='string', h
    '''
    crawler_name = formID + '_db_crawler'
    db_name = formID + '_db'
    path = 's3://jotform-stuff/' + formID + '/'
    db_arn = f"arn:aws:glue:us-east-1:708508995810:database/{formID}_db"
    role_name = 'arn:aws:iam::708508995810:role/practice_glue_role'
    response = glue.create_crawler(
    Name=crawler_name, #req
    Role=role_name, #req
    DatabaseName=db_name, #req
    Description='This crawler will be utilized to get data for jotform',
    Targets={
        'S3Targets': [
            {
                'Path': path,
            },
        ]
    },
    Tags={
        'Crawler': crawler_name
    }
    )

def start_crawler(formID):
    crawler_name = formID + '_db_crawler'
    response = glue.start_crawler(
    Name=crawler_name
    )


    import boto3


glue = boto3.client('glue')
def db_make(formID):
    db_name = formID + '_db'
    response = glue.create_database(
    DatabaseInput={
        'Name': db_name,
        'Description': 'This db will be used to host jotform data',
    }
    )

def crawler_make(formID):
    '''
    Schedule='string', #may only need to crawl once
    Configuration='string', h
    '''
    crawler_name = formID + '_db_crawler'
    db_name = formID + '_db'
    path = 's3://jotform-stuff/' + formID + '/'
    db_arn = f"arn:aws:glue:us-east-1:708508995810:database/{formID}_db"
    role_name = 'arn:aws:iam::708508995810:role/practice_glue_role'
    response = glue.create_crawler(
    Name=crawler_name, #req
    Role=role_name, #req
    DatabaseName=db_name, #req
    Description='This crawler will be utilized to get data for jotform',
    Targets={
        'S3Targets': [
            {
                'Path': path,
            },
        ]
    },
    Tags={
        'Crawler': crawler_name
    }
    )

def start_crawler(formID):
    crawler_name = formID + '_db_crawler'
    response = glue.start_crawler(
    Name=crawler_name
    )