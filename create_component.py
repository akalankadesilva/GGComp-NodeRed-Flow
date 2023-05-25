import json
import os
import boto3
import sys

gg_client = boto3.client('greengrassv2')
app_name = os.environ['APP_NAME']
bucket_name = os.environ['BUCKET_NAME']
bucket_key = os.environ['BUCKET_KEY']

artifact_name = sys.argv[1]
 
component_list = gg_client.list_components(
    scope='PRIVATE',
    maxResults=100
)

found = False; 
current_component = {}
current_version = '1.0.0'
for component in component_list['components']:
    if component['componentName'] == app_name:
        found = True;
        current_component = component
        current_version = component['latestVersion']['componentVersion']
        
version_numbers = current_version.split(".")
major = version_numbers[0]
minor = version_numbers[1]
patch = version_numbers[2]
patch = str(int(patch) + 1)

recipe_file = open("recipe.json", "r")
recipe = recipe_file.read()
recipe_obj = json.loads(recipe)
recipe_obj['ComponentVersion'] = major + '.' + minor + '.' + patch
recipe_obj['ComponentName'] = app_name
recipe_obj['Manifests'][0]['Artifacts'][0]['URI'] = "s3://" + bucket_name + "/" + bucket_key + "/" + artifact_name
updated_recipe = json.dumps(recipe_obj)


gg_client.create_component_version( inlineRecipe = updated_recipe)
    
