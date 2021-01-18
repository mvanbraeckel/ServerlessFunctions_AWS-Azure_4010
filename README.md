# ServerlessFunctions_AWS-Azure_4010
Serverless Functions are triggered when a new file is added to a storage bucket/container, then a log entry is made on a logfile and the file is copied to a “backup” bucket/container on AWS or Azure (Cloud Computing course A2)

# Info

- Name: Mitchell Van Braeckel
- Student ID: 1002297
- Course: CIS*4010 Cloud Computing
- Assignment: 3
- Brief: Serverless Functions
- Due: (Extended) Nov 30, 2020

## Cloud System 1: AWS

- Name & Location of Bucket where new file addition triggers function: `a3cis4010-mvanbrae` on AWS S3
- Name and Location of Bucket where the file is copied/backed up: `copytwomvanbrae` on AWS S3
- Name of the file in the A3 repo containing the function code: `lambda_function.py`
- Programming language used: Python 3

### Brief description of how the serverless AWS function was set up

The following can be done entirely via the AWS Console:

1. Precondition - Create 2 buckets via S3 AWS Console:

   - `a3cis4010-mvanbrae` as source bucket (ie. so it is tracked with a trigger)
   - `copytwomvanbrae` as destination bucket (ie. where the backup copy of an upload is stored)

2. Precondition - Using the AWS Console, create an AWS Lambda Function:

   - Use the blueprint `s3-get-object-python`
   - Configure it with the name `a3cis4010-function`
   - Create a new role with basic Lambda permissions (option in initial configuration)
   - Set the S3 bucket trigger to the source bucket for all object create events

3. Precondition - Configure generated template Lambda function code; **(see `lambda_function.py`)**:

   - Modify it to also copy a backup of the upload to the destination bucket
   - Improve logs: bucket, key (filename), content type (of the upload)
   - Also log successful copy to backup destination bucket

4. Precondition - Ensure the Lambda function created has the trigger for the S3 source bucket enabled:

5. Precondition - Create IAM Policy for the AWS Lambda function role & attach the AWS Lambda function role:

   - Choose S3 service for all S3 actions and all resources
   - Review policy, set the name to `a3cis4010-policy`, then create the IAM Policy
   - Attach the *a3cis4010-function-role* linked to the AWS Lambda function (created in precondition 2) to the created IAM Policy

### Cloud System 1 Usage

- Upload any file to source AWS S3 bucket `a3cis4010-mvanbrae` using AWS Console
- Check associated AWS CloudWatch Logs Log groups for the AWS Lambda Function (ie. `/aws/lambda/a3cis4010-function`)
  - View the Log stream entries to see the logs for uploads, including:
    - 'Loading function...'
    - BUCKET: "", KEY: "", CONTENT_TYPE: ""
    - the entire response from the upload
    - successful backup copied to another bucket
    - any errors that may occur
- Afterwards, look at destination for backup copies, AWS S3 bucket `copytwomvanbrae`, using AWS Console to see the uploads are present and copied over successfully

## Cloud System 2: Azure

- Name & Location of Container where new file addition triggers function: `sample-workitems` on Azure resource group storage account related to the function app
- Name and Location of Container where the file is copied/backed up: `copytwomvanbrae` on Azure resource group storage account related to the function app
- Name of the file in the A3 repo containing the function code: `run.csx` & `function.json`
- Programming language used: .NET Core / C# Script

### Brief description of how the serverless Azure function was set up

The following can be done entirely via the Azure portal:

1. Precondition - Create the Azure Function App (and its resource group):

   - Create a new resource group as `a3cis4010`
   - Select the function app name as `a3cis4010-function-mvanbrae`
   - Select the runtime stack (ie. programming language) as ".NET CORE" (specifically for C# Script in our case)
   - Choose the region as "East US"
   - Use default hosting (storage account name, OS, and plan) and monitoring (insights) config settings, then review and create (the new function app in a new resource group)
   - After the deployment succeeds, go to the resource

2. Precondition - Create an Azure Blob storage triggered function:

   - From the created Azure Function app (created in precondition 1), go to Functions section and create/add a new Azure Blob storage triggered function
   - Use the "Azure Blob Storage trigger" template
   - Choose the blob trigger function name as `log-and-backup-uploads`
   - Set the path as the source container with suffix `/{name}` (refers to upload file name) and the storage account connect as "AzureWebJobsStorage"

3. Precondition - Create 2 containers via Azure Portal in the same resource group storage account (created in precondition 1)

   - `sample-workitems` as source container (ie. so it is tracked with a trigger as input source)
   - `copytwomvanbrae` as destination container (ie. where the backup copy of an upload is stored / output destination from the trigger)

4. Precondition - Modify generated template function trigger code (created in precondition 2) **(see `run.csx`)** and its related bindings **(see `function.json`)**:

   - Go to the "Code + Test" section of the created blob trigger function
   - Select `run.csx` from the file dropdown list:
     - Add parameters to the `Run()` function for the input and output blobs
     - Improve log line and set the output blob to the input blob inside the `Run()` function
   - Select `function.json` from the file dropdown list:
     - Ensure blob trigger binding is for path `<source-container-name>/{name}` (other settings should be fine)
     - Add 2 bindings similar to the blob trigger binding for the input and output blobs
       - the difference is the type is "blob" and direction is "in" or "out" respectively, noting that the output blob path is for `<dest-container-name>/{name}` instead

### Cloud System 2 Usage

- Open the blob trigger function (ie. `/aws/lambda/a3cis4010-function`, created in precondition 2) and go to the "Code + Test" section
- Expand "Logs" at the bottom of the page (ensure that log streaming isn't paused) to view the logs from the blob trigger function (looks like a non-interactive terminal)
- In another tab/window, go to the source container (ie. `sample-workitems`) for the function app and similarly open another tab/window for the destination container (ie. `copytwomvanbrae`)
- Upload any file to source container using Azure portal second tab
- Check associated Logs in the first Azure portal tab to see (in blue) the uploads being logged, including: name, size in bytes
- Afterwards, look at destination for backup copies, third Azure portal tab, using to see the uploads are present and copied over successfully
