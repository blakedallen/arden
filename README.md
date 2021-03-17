# Arden
Adaptive Realtime Detection and Examination Network

## Overview

An adaptive realtime detection and examination network system, 
- Edge deployment
- Visual Classification (dogs, lost children, liscence plate, surfers, etc.)
- Sharpening
- Comparison to uploaded image
- Alert user to located coordinates

The following Table summarizes the scope and topics used


| Container | Location | Tx Topic | Rx Topic | Storage | Role |
| -------------| ------------- | ------------- | ------------- | ------------- | ------------- |
| [Detector (ubuntu)](https://github.com/blakedallen/arden/tree/main/NXContainers/nxDetector)| JetsonNX  | `image`  |  `N/A` | `N/A` | Uses OpenCV to detect image from USB Camera and publish to mqtt |
| [Mqtt broker (alpine)](https://github.com/blakedallen/arden/tree/main/NXContainers/mosquitto)| JetsonNX  | `image`  |  `image`  | `N/A` | Pub/Sub local to NX |
| [Mqtt message forwarder (alpine)](https://github.com/blakedallen/arden/tree/main/NXContainers/nxToServer)| JetsonNX  | `cloud`  |  `image`  | `N/A` | Message fowarder, and knowledgeable of multiple MQTT brokers |
| [Mqtt broker (alpine)](https://github.com/blakedallen/arden/tree/main/AWSContainers/mosquitto)| AmazonAWS  | `cloud`  |  `cloud`  | `N/A` | Pub/Sub local to AWS EC2 Instance |
| [Super Resolution (ubuntu)](https://github.com/blakedallen/arden/tree/main/AWSContainers/superresolution)| AmazonAWS  | `N/A`  |  `cloud`  | `s3` | Receives data from NX and stores to S3 |

## Edge setup
dji - drone with video
use phone wifi hotspot
use battery
Jetson NX 

## Jira
https://w251-arden.atlassian.net/secure/RapidBoard.jspa?rapidView=1&projectKey=WA&selectedIssue=WA-10
