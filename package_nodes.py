import json
import os
import boto3

all_env_vars = os.environ

for env_var in all_env_vars:

    if env_var.startswith("CODEBUILD_SRC_DIR_") and os.path.exists(os.environ[env_var] + "/package.json"):
        os.system("cd " + os.environ[env_var] + " && npm pack") 
        os.system("cp " + os.environ[env_var] + "/*.tgz nodes/")       

 
