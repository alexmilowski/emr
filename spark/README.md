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
    
    
# Wiki Page Counts #

From the [AWS Blog]http://aws.amazon.com/articles/Elastic-MapReduce/4926593393724923) :

Wikistat contains Wikipedia article traffic statistics covering a 16-month period from October 1, 2008 to February 6, 2010. The full data set is online at http://aws.amazon.com/datasets/4182. The data in Wikistat is formatted as follows:

  * Each log file is named with the date and time of collection: pagecounts-20090430-230000.gz.
  * Each line in the log file has four fields: projectcode, pagename, pageviews, and bytes.
  
A sample of the type of data stored in Wikistat is shown below.

    en Barack_Obama 997 123091092
    en Barack_Obama%27s_first_100_days 8 850127
    en Barack_Obama,_Jr 1 144103
    en Barack_Obama,_Sr. 37 938821
    en Barack_Obama_%22HOPE%22_poster 4 81005
    en Barack_Obama_%22Hope%22_poster 5 102081

Because the full Wikistat dataset is fairly large, we have excerpted a single file and copied it to the Amazon S3 bucket at https://s3.amazonaws.com/bigdatademo/sample/wiki/pagecounts-20100212-050000.gz. In our queries, we will parse the data file and sort the dataset based on number of pageviews.

Here is the python code for that same example:

    data = sc.textFile("s3://bigdatademo/sample/wiki/")
    output = data.map(lambda line: line.split(" ")).map(lambda tuple: (tuple[1],int(tuple[2]))).reduceByKey(lambda a, b: a + b)
    output.saveAsTextFile("s3://mybucket/wiki-output")
    
Try it yourself.  It takes about 5 minutes to process on small cluster.
