
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

movies_table = os.environ['MOVIES_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(movies_table)

def getMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] 
    array_path = path.split("/") 
    movie_id = array_path[-1]
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(movie_id)
    )
    item = response['Items']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
def putMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/user/123"
    array_path = path.split("/") # ["", "user", "123"]
    movie_id = array_path[-1]
    
    body = event["body"] #"{\n\t\"name\": \"Jack\",\n\t\"last_name\": \"Click\",\n\t\"age\": 21\n}"
    body_object = json.loads(body)
    
    
    table.put_item(
        Item={
            'pk': "movie_" + getNextMovieId(),
            'sk': body_object['room'], 
            'title': movie_id,
            'actors': body_object['actors'],
            'year': body_object['year'],
            'capacity': "1000",
            '3D': body_object['3D'],
            'availability': "1000"
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Movie Saved')
    }

def roomsPerDay(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/user/123"
    array_path = path.split("/") # ["", "user", "123"]
    movie_id = array_path[-1]
    
    # response = table.get_item(
    #     Key={
    #         'pk': movie_id,
    #         'sk': 'age'
    #     }
    # )
    # item = response['Item']
    # print(item)
    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }
    
def getNextMovieId():
    rooms = table.scan(
        FilterExpression=Attr('pk').contains("movie_") and Attr('sk').contains("room_"))
    size = len(rooms['Items'])
    size = size + 1
    return str(size)

def getRoomAndMovieID(title):
    aux = []
    rooms = table.scan(
        FilterExpression=Attr('pk').contains("movie_") and Attr('sk').contains("room_"))
    for i in getMovies():
        if i['title'] == title:
            aux.append(i['pk'])
            aux.append(i['sk'])
    return aux

def getAvailability(title):
    rooms = table.scan(
        FilterExpression=Attr('title').eq(title))
    for i in getMovies():
        if i['title'] == title:
            aux = i[tickets]
    return aux
