import boto3

#this is the boto3 glue clientthat will be utilized to call glue
glue = boto3.client('glue')
#This function creates a glue database where the data from the crawl will live
def db_make(formID):
    #This keeps all database names to a standard
    db_name = formID + '_db'
    #This call creates a glue database utilizing the boto3 glue module
    response = glue.create_database(
    DatabaseInput={
        'Name': db_name,
        'Description': 'This db will be used to host jotform data',
    }
    )

#This function creates a crawler that will crawl 
def crawler_make(formID):
    '''
    Schedule='string', #may only need to crawl once
    Configuration='string', h
    '''
    #this variable keeps a standard for crawler names
    crawler_name = formID + '_db_crawler'
    #this variable references the standard of Database names
    db_name = formID + '_db'
    #This is the path to the directory that needs to be crawled
    path = 's3://the-jotform-bucket/' + formID + '/'
    #This is the arn of a glue database
    db_arn = f"arn:aws:glue:us-east-1:249689120119:database/{formID}_db"
    #this is the arn for a role that can search s3 buckets, log, and access athena
    role_name = 'arn:aws:iam::249689120119:role/practice_glue_role'
    #This is the call to the glue client that creates the crawler
    response = glue.create_crawler(
    #line 24
    Name=crawler_name, #req
    #line 32
    Role=role_name, #req
    #line 26
    DatabaseName=db_name, #req
    Description='This crawler will be utilized to get data for jotform',
    Targets={
        'S3Targets': [
            {
                'Path': path,#line 28
            },
        ]
    },
    Tags={
        'Crawler': crawler_name#line 24
    }
    )
#this function starts a crawler
def start_crawler(formID):
    #this variable goes with the standard of crawler names
    crawler_name = formID + '_db_crawler'
    #this call accesses the glue clinet and uses the start_crawler module
    response = glue.start_crawler(
    Name=crawler_name
    )