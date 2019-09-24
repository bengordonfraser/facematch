import boto3

def lambda_handler(event, context):

    bucket=''
    collectionId=''
    photo=''
    
    client=boto3.client('rekognition')

    response=client.index_faces

    response=client.index_faces(CollectionId=collectionId, ExternalImageId="bgf.jpg",
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                                

    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    
    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collectionId)

    print('Faces in collection ' + collectionId)

    tokens = "1"
    while tokens:

        faces=response['Faces']

        for face in faces:
            print (face)
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collectionId,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False

