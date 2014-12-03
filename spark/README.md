# Using Spark in EMR #

This example goes through starting a cluster with Spark installed and running a number of examples.

# Setup #

First, you need to start a cluster and install Spark.  Fortunately, AWS has setup a bootstrap action for this and so all you need to do is point to it:

    aws emr create-cluster --ami-version 3.2.1 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=2,InstanceType=m1.medium --name SparkCluster --enable-debugging --tags Name=emr --bootstrap-actions Path=s3://support.elasticmapreduce/spark/install-spark --ec2-attributes KeyName=mykey --log-uri s3://mybucket/logs/ 
    

# Word Count Example #

Because everyone loves the word count example!

## Step 1 ##

You'll be running the spark client on the master.  Login to to your master by finding the public DNS (e.g. ec2-nn-nn-nn-nn.compute-1.amazonaws.com) using your key:

    ssh hadoop@ec2-nn-nn-nn-nn.compute-1.amazonaws.com -i mykey.pem

## Step 2 ##

Run the python client for Spark:

    MASTER=yarn-client /home/hadoop/spark/bin/pyspark
    
and then wait till you see:

    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /__ / .__/\_,_/_/ /_/\_\   version 1.1.0
          /_/
    
    Using Python version 2.6.9 (unknown, Mar 28 2014 00:06:37)
    SparkContext available as sc.
    >>> 

## Step 3 ##

Load a reference to your data:

   data = sc.textFile("s3://elasticmapreduce/samples/wordcount/input")
   
## Step 4 ##

Setup your job:

    counts = data.flatMap(lambda line: line.split(" ")) \
                .map(lambda word: (word, 1)) \
                .reduceByKey(lambda a, b: a + b)
                
## Step 5 ##

Run the job by saving it back to S3:

    counts.saveAsTextFile("s3://mybucket/spark-output/")
    
