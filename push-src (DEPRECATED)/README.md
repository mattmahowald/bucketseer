# Push Pattern
Ideally we want to be able to set up a service which waits for google pubsub to send it data via a webhook. However, this is difficult to achieve because it requires significant work to be done to verify that we own dev-lims.freenome.net and research-lims.freenome.net.

For more details on how to do that, see:
https://www.google.com/webmasters/verification/verification?hl=en&siteUrl=https://dev-lims.freenome.net/&priorities=vfile,vmeta,vdns,vanalytics,vtagmanager&tid=recommended

After this verification step, we can then create subscribers to the appropriate Google PubSub topics which are 'push' subscribers. We then give it the dev-lims.freenome.net/bucketseer/bucket-webhook endpoint as its webhook, and every time something is added to the topic the data should be pushed to our bucketseer service. This `push-src` folder contains all the necessary code to start a very simple Flask app that handles requests to the aforementioned endpoint.

Note that this is currently NOT USED - we use a pull pattern instead because of the aforementioned overhead with regard to verification.
