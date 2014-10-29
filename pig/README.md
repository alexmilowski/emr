# Running a PIG Script #

This example comes from the [AWS EMR/PIG User Guide](http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-pig-launch.html) but was 
tweaked to fix a problem.  The `piggybank.jar` seems to no longer be in the same place on the filesystem.  Instead, the script has been changed
to load it from S3 directly.

The example processes web server log files and the example input is located here:

    aws s3 ls s3://elasticmapreduce/samples/pig-apache/input/
    

# Setup #

If you don't have a cluster running, you'll need to start one (see main setup page).  You also need a bucket for the code, input, and output.

# Running the Example #

# Step 1 #

We need to store the pig script into our bucket:

    aws s3 cp reports.pig s3://mybucket/

# Step 2 #    
    
Add the step to run the PIG script:

    aws emr add-steps --cluster-id <your-id> --steps Type=PIG,Name="PIG Log Files",ActionOnFailure=CONTINUE,Args=[-f,s3://mybucket/reports.pig,-p,INPUT=s3://elasticmapreduce/samples/pig-apache/input,-p,OUTPUT=s3://mybucket/pig/output]

This command returns the step id that you can use for further monitoring.  If you use an 'm1.medium' instance type, this job should take 10 minutes to process and 13 minutes of elapsed time.

You can monitor its progress from the console or via:

    aws emr describe-step --cluster-id <cluster-id> --step-id <step-id>
    
# Step 3 #

Sync the output:

   aws s3 sync s3://mybucket/pig/output/ output/
   
You should now have 8 files:

    output/total_requests_bytes_per_hour/_SUCCESS
    output/total_requests_bytes_per_hour/part-r-00000
    output/top_50_search_terms_from_bing_google/_SUCCESS
    output/top_50_search_terms_from_bing_google/part-r-00000
    output/top_50_ips/_SUCCESS
    output/top_50_ips/part-r-00000
    output/top_50_external_referrers/_SUCCESS
    output/top_50_external_referrers/part-r-00000
    