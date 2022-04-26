import json
import crawler_funk
def lambda_handler(event, context):
    print(event)
    formID = event['formID']
    try:
        crawler_funk.db_make(formID)
    except:
        print('db already made')
    try:
        crawler_funk.crawler_make(formID)
    except:
        print('crawler already made')
    try:
        crawler_funk.start_crawler(formID)
    except:
        print('oops crawler didnt run')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }