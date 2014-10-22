# SETUP #

Install the AWS CLI with 

    sudo pip install awscli

You may need to link to the exectuable:

    sudo ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/aws /opt/local/bin/aws
    
Then configure your system with the AWS key, secret, and default region (e.g. us-east-1).  You can leave the default output format blank.

    aws configure

You can re-run this command at any time to change the values.
    
Now you can test it by asking about your running EC2 instances (you may have none):

    aws ec2 describe-instances