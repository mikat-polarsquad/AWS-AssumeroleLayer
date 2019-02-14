"""
This is mainly intent to be used as a module for other AWS python scripts or lambda functions.
"""

import boto3
import botocore
import sys

# you can assign role in the function like below
# ROLE_ARN = 'arn:aws:iam::01234567890:role/my_role'
#
# or you can pass role as an evironment varibale
# ROLE_ARN = os.environ['role_arn']
# Maybe not needed


def cli_session(profileName=None, role_arn=None, session_name=None):
    """
    If role_arn is given assumes a role and returns boto3 session
    otherwise return a regular session with the current IAM user/role
    """
    if role_arn and profileName:
        ses = boto3.Session(profile_name=profileName)
        client = ses.client('sts') # boto3.client('sts')
        response = client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
        session = boto3.Session(
            aws_access_key_id=response['Credentials']['AccessKeyId'],
            aws_secret_access_key=response['Credentials']['SecretAccessKey'],
            aws_session_token=response['Credentials']['SessionToken'])
        return session
    else:
        return boto3.Session(profile_name=profileName)

def cli_assume_role(session=None, account_id=None, role_name=None, session_name=None, region_name=None):
    sts_client = session.client('sts', region_name=region_name)
    role_arn = 'arn:aws:iam::' + account_id + ':role/' + role_name
    
    assuming_role = True
    while assuming_role is True:
        try:
            assuming_role = False
            sts_response = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name)
            assumed_session = boto3.Session(
                aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                aws_session_token=sts_response['Credentials']['SessionToken'],
                region_name=region_name)
        except botocore.exceptions.ClientError as e:
            print(e)
            sys.exit(1)

            # assuming_role = True
            # print("Retrying...")
            # time.sleep(10)
    return assumed_session

def assume_role(role_arn=None, session_name='assumed_session'):
    """
    This is to be used when module is used in Lambda.
    For example when running lambda, which needs to create/check resources with assumed role on other AWS account.
    """
    stsClient = boto3.client('sts')
    response = stsClient.assume_role( # TODO: Add some error handling
        RoleArn=role_arn,
        RoleSessionName=session_name
        # Policy='string',
        # DurationSeconds=3600, # range from 900sec to 12hours (43200sec), Default by AWS 3600sec
        # ExternalId='string',
        # SerialNumber='string',
        # TokenCode='string'
    )
    session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])
    return session
