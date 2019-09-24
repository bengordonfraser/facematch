from __future__ import print_function

#   SDK modules to import 

import boto3
from decimal import Decimal
import json
import urllib
import sys


#   Service assignments

rekognition = boto3.client('rekognition')
sns = boto3.client('sns')


#   Declare variables

jobID = ""
key = ""
bucket = ""
queue_url = ''
bgfFaceSearchRekognitionServiceRole = ''
bgfFaceSearchSNS = ''
matchthreshold = 80 

#   Main function

def lambda_handler(event, context):

    
#   Get variables from event    
    
    bucket = (event['Records'][0]['s3']['bucket']['name'])
    key = (event['Records'][0]['s3']['object']['key'])


#   Call Rekognition with event and credentials
#   Pass event data to be included in SNS message
    
    response = rekognition.start_face_search(
    Video={'S3Object':{'Bucket':bucket,'Name':key}},
    FaceMatchThreshold=matchthreshold,
    JobTag=key,
    CollectionId="ourfacescollection",
    NotificationChannel={
        'SNSTopicArn': bgfFaceSearchSNS,
        'RoleArn': bgfFaceSearchRekognitionServiceRole})
    print ("Processed video: " + key)
    return response
