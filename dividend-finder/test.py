import json
import logging
import os
import sys
import time
import boto3

boto_session = boto3.session.Session(profile_name='staging', region_name='us-east-1')
client = boto_session.client('route53')


def get_health_checks():
    paginator = client.get_paginator('list_health_checks')
    response_iterator = paginator.paginate()
    health_checks = []
    for page in response_iterator:
        print(json.dumps(page))
        health_checks = health_checks + page['HealthChecks']
    return health_checks


def get_health_check_id(existing_health_checks, zone):
    return [health_check['Id'] for health_check in existing_health_checks
            if (zone in health_check.get('CallerReference', ''))]


def delet_health_checks(health_checks_list, zone):
    for health_check_id in get_health_check_id(health_checks_list, zone):
        print(health_check_id)
        try :
            client.delete_health_check(HealthCheckId=health_check_id)
        except:
            pass


health_checks = get_health_checks()
delet_health_checks(health_checks, 'us-east-1d')
