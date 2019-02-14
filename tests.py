"""
This is mainly intent to be used as a module for other AWS python scripts or lambda functions.
"""

import boto3
import botocore
import sys
import os
from python import assume_role as ar

# Some basic test to aquire an assumed session.
def main():
    session = ar.assume_role(os.environ['ASSUME_ROLE_ARN'])
    print("Assumed Role succesfully!")
    print("Session: {}".format(session))
    exit()


if __name__ == '__main__':
    main()