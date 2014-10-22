# Using NLTK in EMR #

# Setup #

You need to setup NLTK on the cluster via a bootstrap action.  These can easily be done by the `bootstrap-nltk.sh` script that installs this as you might do on your own system.

First, you need to store the script into S3:

    aws s3 cp bootstrap-nltk.sh s3://mybucket/
    
The you just use `--bootstrap-actions` to specify that script.  For example, a cluster (1 master, 2 cores, m1.medium) can be created as follows:

    aws emr create-cluster --ami-version 3.2.1 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=2,InstanceType=m1.medium --name "NLTK Test Cluster" --log-uri s3://mybucket/logs/ --enable-debugging --tags Name=emr --bootstrap-actions Path=s3://mybucket/bootstrap-nltk.sh,Name="Setup NLTK"