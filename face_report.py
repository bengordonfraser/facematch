from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import sys

print('Loading function')


#   Variables

rekognition = boto3.client('rekognition')
sns = boto3.client('sns')
s3 = boto3.client('s3')
result = ""
indexed = ""
similarity = ""
imageid = ""


#   Helper functions

def GetFaceSearch(jobId):
    response = rekognition.get_face_search(
    JobId=jobId,
    MaxResults=123,
    SortBy='INDEX')
    return response

def SnsPublish(sms):
    response = sns.publish(
    TopicArn='',
    Message=sms,
    Subject='Notification from bgfFaceSearchSMS')


#   Main function

def lambda_handler(event, context):
    
    maxsimilarity = 0
 
    
#   Process event package and extract metadata

    message = event.items()                
    for item in message:
        layer = json.dumps(item[1])
        jobId = json.loads(layer)
        body = (jobId[0])
        payload = body['Sns']
        msgstr = payload['Message']
        msgdict = json.loads(msgstr)
        jobId = msgdict['JobId']
        video = msgdict['Video']['S3ObjectName']
        videotag = video[:-3]
    print ("JobId:"+jobId+"     Video:"+video)
    
    
#   Call Rekognition with GetFaceSearch() and process response

    response = GetFaceSearch(jobId)
    responsejson = json.dumps(response)
    responsedict = json.loads(responsejson)
    

#   Status check 

    status = response['JobStatus']
    if status == "SUCCEEDED":
        print (status)
    else:print (status)
    
    
#   Log Rekognition response

    print (responsejson)
    

#   Extract matches and data from response

    for persons in responsedict['Persons']:
        if 'FaceMatches' in persons:
            try:
                facematch = (persons['FaceMatches'])
                similarity = facematch[0]['Similarity']
                faceid = facematch[0]['Face']['ExternalImageId']
                print (("FaceMatches:  Id=" + faceid), ("Similarity=" + str(similarity)))
                if similarity > maxsimilarity:
                    maxsimilarity = round(similarity, 1)
            except:next

            
#   Construct notifications then call SnsPublish()            
            
    if maxsimilarity != 0:
        #similarity = similarity/detections
        sms = "An event " + video + " has been captured, containing a match to the index image:[" + faceid + "], detected with MaxSimilarity=" + str(maxsimilarity) + "%. The video can be viewed in a streaming player with this URL: https://d2z933d9b2c3qm.cloudfront.net/output/dash/" + videotag +"mpd"
        SnsPublish(sms)
        print("------sending notification-----")
        print(sms)
        
    if maxsimilarity < 80:
        sms = "An event " + video + " has been captured, containing an unknown person. The video can be viewed in a streaming player with this URL: https://d2z933d9b2c3qm.cloudfront.net/output/dash/" + videotag +"mpd"
        SnsPublish(sms)
        print("------sending notification-----")
        print(sms)
    
    
#   Copy file from Uploads bucket to VOD bucket for transcoding and serverless delivery    
    
    copy_source = {'Bucket':'', 'Key':video}
    s3.copy(copy_source, '', 'input/'+video)
    print("Copied video file to VOD input folder for transcoding.")
    
