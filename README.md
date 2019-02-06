# Streams and Events Viewer
This app lets a user log in with their twitch account and set their favorite streamer to view their live stream and events as they happen. if you were to go ahead and open a stream in this application and then follow that streamer, you would see that that event is pushed to the streaming page in real-time.

**Tools used:**
- I used Django with it's templating engine for the complete application.
- Django channels used for the websockets.
- The latest version of Twitch's API for authentication and events.

**Approach:**
- The [OAuth Implicit Code Flow](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#oauth-implicit-code-flow)  as described in Twitch Developer docs is used to authenticate users to the app using their twitch accounts.
- After a user logs in, they're presented with a page that lets them set their favorite streamer.  
-  The new Twitch provides a webhook for instant notification of follows as they occur. I've used this webhook which in turn notifies a callback URL on this application. The callback URL saves the event to the database and then pushes it to the websockets room of the streamer.
- The user is redirected to the stream page which has the embedded stream along with a list of 10 most recent follows that the user has received. 
- These events are initially fetched through the database but the new ones are pushed through the websocket as they happen.

Additionally, I also wanted to have cheers/bits received through viewers as events by using Twitch's [IRC interface](https://dev.twitch.tv/docs/irc/). I've made a bot that listens to the incoming chat messages and filters out the ones with cheers but incorporating it would have required either celery or python-rq for which I didn't have any time left. If you'd like to check out how the IRC interface is used to notify when bits/cheers are received, you can view the sample code in [this repo.](https://github.com/saadullahaleem/twitch-chat-bot/blob/master/bot.py)

**Answers to Questions:**

> -   How would you deploy the above on AWS? (ideally a rough architecture diagram will help)

I'd use Amazon's RDS and ElastiCache for PostGreSQL and Redis respectively. I'll use Elastic Container Service to run containerized instances of our server.

                                     +------------------------------------------------+      
                                     |                                                |
                                     |                                                |
                               +-----+------+                                         |
                               |            |                                         |
                               |  Container +-----------------+                       |
              +---------------->  running   |                 |                       |
              |                |  Server    |                 |                       |
      +-------+------+         |  Instance  |         +-------v-------+      +--------v------+
      |              |         |            |         |               |      |               |
      |     Load     |         +------------+         |    Amazon     |      |     Amazon    |
      |   Balancer   |                                |  ElastiCache  |      |      RDS      |
      |              |         +------------+         |               |      |               |
      |              |         |            |         |               |      |               |
      +-------+------+         |  Container |         +-------^-------+      +--------^------+
              |                |  running   |                 |                       |
              +---------------->  server    |                 |                       |
                               |  instance  +-----------------+                       |
                               |            |                                         |
                               +-----+------+                                         |
                                     |                                                |
                                     |                                                |
                                     +------------------------------------------------+


> -   Where do you see bottlenecks in your proposed architecture and how would you approach scaling this app starting from 100 reqs/day to 900MM reqs/day over 6 months?

For something like 900M reqs/day, an event-sourcing based approach could be far more effective. We could also use Server Sent Events (SSE) here since data is only being pushed by the server and not the other way around. Also, I've only used PostgreSQL because of how well it plays with my framework of choice here. If I were to write this application for production, I'd use something like elixir paired with a real-time database.

If we were to scale this application, we'll need to scale out Redis into a cluster to support scaling of websockets which we're using for real-tme updates. We'll need to be careful with our load-balancing of websockets (we'll need TCP proxies instead of HTTP ones).

 We'll also need to implement caching and have multiple instances of our server behind a load balancer.
