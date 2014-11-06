# mrjob Version of Tweet Word Count #

This example does the same as the tweet word count example but uses mrjob so you can also run it locally.

# Setup #

If you don't have a cluster running, you'll need to start one.  You also need a bucket for the bootstrap, input, and output.

First, you need to store the bootstrap script into S3:

    aws s3 cp bootstrap-mrjob.sh s3://mybucket/
    
The you just start the cluster with `--bootstrap-actions` to specify that script.  For example, a cluster (1 master, 2 cores, m1.medium) can be created as follows:

    aws emr create-cluster --ami-version 3.2.3 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=2,InstanceType=m1.medium --name "mrjob Test Cluster" --log-uri s3://mybucket/logs/ --enable-debugging --tags Name=emr --bootstrap-actions Path=s3://mybucket/bootstrap-mrjob.sh,Name="Setup mrjob / NLTK"    

# Running the Example Locally #

The tweets are stored as JSON and we'll need to extract the tweet text.  We can pipe that output direcly into the mrjob program:  

    python ../../tweet-wordcount/format-tweets.py ../../tweet-wordcount/microsoft-2014-10-07.json | python mrjobTweetWordCount.py

# Running the Example on EMR #

## Step 1 ##

The tweets are stored as JSON and we'll need to extract the tweet text and create an input with one line per tweet.  The `format-tweets.py` program
does this:

    mkdir -p tweet-wc/input
    python ../../tweet-wordcount/format-tweets.py ../../tweet-wordcount/microsoft-2014-10-07.json > tweet-wc/input/tweets.txt
    
Now we need to store the input:

    aws s3 sync tweet-wc s3://mybucket/tweet-wc/
    
We also need to tell mrjob how to access our account by creating a `mrjob.conf` file:

    runners:
      emr:
        aws_access_key_id: <your-key>
        aws_secret_access_key: <your-secret>
        
## Step 2 ##

We can run the job and get output locally:

    python mrjobTweetWordCount.py -c mrjob.conf -r emr --emr-job-flow-id=<jobflow-id> s3://mybucket/tweet-wc/input/
    
Note: Remember to replace <jobflow-id> with the ID of the cluster.

If you want to store the output on S3, just add `--output` and `--no-output` parameters:

    python mrjobTweetWordCount.py -c mrjob.conf -r emr  --emr-job-flow-id=<jobflow-id> --output-dir=s3://mybucket/tweet-wc/output/ --no-output s3://mybucket/tweet-wc/input/

If you do not specify a job flow identifier, a cluster will be created for you but you will have to wait for it to be setup and bootstrapped.