from __future__ import print_function

import boto3
import random

print('Loading function')
cw = boto3.client('cloudwatch')


def monitor_response_time(event, context):
    elapsed_time = -1
    try:
        elapsed_time = test_response()
        put_cloudwatch_metric('response_time', elapsed_time, get_current_region(context))
    except Exception as e:
        print("Exception: " + str(e))
    return elapsed_time


def monitor_hook_delivery_time(event, context):
    elapsed_time = -1
    try:
        elapsed_time = test_hook()
        put_cloudwatch_metric('hook_delivery_time', elapsed_time, get_current_region(context))
    except Exception as e:
        print("Exception: " + str(e))
    return elapsed_time


def test_response():
    return random.randint(100, 500)


def test_hook():
    return random.randint(500, 2000)


def get_current_region(context):
    return context.invoked_function_arn.split(":")[3]


def put_cloudwatch_metric(metric_name, value, region):
    print("Sending custom metrics {0}:{1}ms".format(metric_name, value))
    cw.put_metric_data(
        Namespace='Custom/APM',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': 'Milliseconds',
            'Dimensions': [
                {
                    'Name': 'Region',
                    'Value': region
                }
            ]
        }]
    )
