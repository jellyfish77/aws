#!/usr/bin/env python

# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time
import os, sys

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"

# The unique hostname that &IoT; generated for 
# this device.
# HOST_NAME = "yourhostname-ats.iot.us-east-1.amazonaws.com"
HOST_NAME = "abvuq2slx5a1s-ats.iot.us-west-2.amazonaws.com"

CERTS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'certs')

# The relative path to the correct root CA file for &IoT;, 
# which you have already saved onto this device.
#ROOT_CA = os.path.join(CERTS_PATH, 'RootCA-VeriSign-Class-3-Public-Primary-Certification-Authority-G5.pem')
ROOT_CA = os.path.join(CERTS_PATH, 'AmazonRootCA1.pem')

print ROOT_CA
with open(ROOT_CA, 'r') as fin:
    print fin.read()

# The relative path to your private key file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
#PRIVATE_KEY = "../../certs/78dbb0c521-private.pem.key"
PRIVATE_KEY = os.path.join(CERTS_PATH, '78dbb0c521-private.pem.key')
print PRIVATE_KEY
with open(PRIVATE_KEY, 'r') as fin:
    print fin.read()

# The relative path to your certificate file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
#CERT_FILE = "../../certs/78dbb0c521-certificate.pem.crt"
CERT_FILE = os.path.join(CERTS_PATH, '78dbb0c521-certificate.pem.crt')
print CERT_FILE
with open(CERT_FILE, 'r') as fin:
    print fin.read()

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "MyRPi"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
    print()
    print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
        '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)

# Create, configure, and connect a shadow client.
sys.stdout.write ('Create shadow client... ')
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
print 'OK'
print 'Configure endpoint... ',
myShadowClient.configureEndpoint(HOST_NAME, 8883)
print 'OK'
print 'Configure credentials... ',
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
print 'OK'
print 'Configure disconn timeout... ',
myShadowClient.configureConnectDisconnectTimeout(10)
print 'OK'
print 'Configure op timeout... ',
myShadowClient.configureMQTTOperationTimeout(5)
print 'OK'
sys.stdout.write ('Connect... ')
sys.stdout.flush()
myShadowClient.connect()
print 'OK'

print 'Configure shadow client... ',
# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)
print 'OK'

# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
print('Generate randonm data... ')
while True:
  # Generate random True or False test data to represent
  # okay or low moisture levels, respectively.
    moisture = random.choice([True, False])
    

    if moisture:
        print 'Sending okay... ',
        myDeviceShadow.shadowUpdate(
            '{"state":{"reported":{"moisture":"okay"}}}',
            myShadowUpdateCallback, 5)
        print 'OK'
    else:
        print 'Sending low... ',
        myDeviceShadow.shadowUpdate(
            '{"state":{"reported":{"moisture":"low"}}}',
            myShadowUpdateCallback, 5)
        print 'OK'

    # Wait for this test value to be added.
    time.sleep(5)