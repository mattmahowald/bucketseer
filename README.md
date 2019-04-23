# Bucketseer
This is a service that waits on Google PubSub subscriptions which receive messages whenever a new file is added/deleted on some bucket.

It then does some actions defined by a callback on the subscription, the default action here is to append it to an internal RabbitMQ queue but we can make it do other things as well such as trigger Balrog runs. The idea behind enqueuing the message to a RabbitMQ queue is that RabbitMQ can eventually centralize our job tasks and allow us to do logging as well, so we can just use PubSub and Bucketseer as the 'entrypoint' into our pipeline when files get dumped into GCS by the NAS.

This service is currently only running in dev and is not well tested enough for production use!

# How to configure
1. Find your bucket of interest (for e.g. gs://my-bucket)
2. Create a Google PubSub topic for the bucket here (for dev): https://console.cloud.google.com/cloudpubsub/topicList?organizationId=933616597088&project=freenome-services-dev
3. Create a Subscription for the topic by clicking into the topic and clicking `Create Subscription`
4. Run the following command in your terminal (Ask @jaychia to do this if you do not have sufficient permissions) `gsutil notification create -t [TOPIC_NAME] -f json gs://[BUCKET_NAME]` - this appends a message to the topic every time a change is made to the bucket
5. Modify code in this repository by adding the subscription name and an appropriate callback to `src/main.py` (note if you are appending to a RabbitMQ queue you need to go create that queue) - this makes bucketseer watch your subscription for new mesages and run the provided callback everytime it sees a new message
6. Build your code and push it to the Docker repository, then redeploy `bucketseer` on dev.
