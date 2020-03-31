 
import json
import boto3
import pprint

def lambda_handler(event, context):
    # TODO implement
    client_obj_asg = boto3.client('application-autoscaling',region_name='us-east-1')
    client_obj_ecs = boto3.client('ecs',region_name='us-east-1')
    #pprint.pprint(dir(client_obj_asg))
    
    #retrieving cluster names from Cluster ARN's
    cluster_name=[]
    for each_clusterarn in client_obj_ecs.list_clusters()['clusterArns']:
        cluster_name.append(each_clusterarn.split('/')[-1])
    
        
    pprint.pprint(cluster_name)
    
    #retrieving Service Name Details
    for each_clustername in cluster_name:
        service_response = client_obj_ecs.list_services(
        cluster=each_clustername,
        launchType='FARGATE',)
        if len(service_response['serviceArns']) != 0:
            for each_servicearn in service_response['serviceArns']:         
                service_name='service'+'/'+each_clustername+'/'+each_servicearn.split('/')[-1]
                print(service_name)
                
    
    
    response_service = client_obj_ecs.list_services(
    cluster='cluster-367855',
    launchType='FARGATE',)
    pprint.pprint(response_service['serviceArns'])
    response_scaling = client_obj_asg.register_scalable_target(
    ServiceNamespace='ecs',
    ResourceId='service/cluster-367855/367855_service',
    #ResourceId=response_service['serviceArns'],
    ScalableDimension='ecs:service:DesiredCount',
    MinCapacity=0,
    MaxCapacity=0,)

    
    pprint.pprint(response_scaling)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
