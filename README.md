# acotourplanner
Tour planner application using Ant Colony optimization technique

We have developed tour planner which uses Ant colony optimization technique to generate optimized tour plane.
Refer to following papers for better understanding of Ant colony optimization
1. M. Dorigo, M. Birattari and T. Stutzle, ”Ant colony optimization,” in IEEE Computational Intelligence Magazine, vol. 1, no. 4, pp. 28-39, Nov. 2006,   doi: 10.1109/MCI.2006.329691.
2. Dorigo M, Gambardella LM. Ant colonies for the travelling salesman problem. biosystem.1997 Jul 1;43(2):73-81.

As we know, in travelling salesman problem, we start from a source and we need to visit different cities and return back to source in optimized way. Our application can be used for the following use cases
1. Delivery agent starting from a warehouse need to deliver items to multiple locations and return back to warehouse 
2. Person starting from his house need to visit multiple locations to invite friends/relatives for a function.

Using the various APIs provided by Google maps/AWS and ArcGIS, we have deployed a website developed using Python Flask that takes a user’s starting position as well as the locations that they want to visit as input and as an output provides the optimal path the user should take to minimize time. This path is based on the real time traffic conditions.

You can use either Google maps or AWS location services for getting real time traffic data. We strongly recommend using Google maps service as we found it is more fast,accurate and useful than AWS location services

* Using Google maps

Steps
1. You need to have Google cloud platform account and GCP project created. Refer - https://cloud.google.com/apigee/docs/hybrid/v1.2/precog-gcpaccount
2. Enable Distance matrix API for your created project. Refer - https://developers.google.com/maps/documentation/distance-matrix/cloud-setup
3. Copy the obtained key to the file keyfile.txt
4. Use nohup python3 app.py & to run application. This code will use Google maps service for fetching real time traffic data.
5. Access app on web browser through http://hostname:5000/home

* Using AWS location services

Steps
1. You need to have active AWS account. Refer - https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html
2. Download and configure aws cli on the server . Refer - https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
3. Use nohup python3 app_aws.py & to run application. This code will use AWS Geolocation service for fetching real time traffic data.
4. Access app on web browser through http://hostname:5000/home


