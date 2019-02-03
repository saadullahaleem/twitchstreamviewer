**Streams and Events Viewer:**

This app lets a user log in with their twitch account and set their favorite streamer to view their live stream and events as they happen.

**Tools used:**
- I used Django with it's templating engine for the complete application.
- Django channels used for the websockets.
- The latest version of Twitch's API for authentication and events.

**Approach**:
- The [OAuth Implicit Code Flow](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#oauth-implicit-code-flow)  as described in Twitch Developer docs is used to authenticate users to the app using their twitch accounts.
- After a user logs in, they're presented with a page that lets them set their favorite streamer.  
-  The new Twitch provides a webhook for instant notification of follows as they occur. I've used this webhook which in turn notifies a callback URL on this application. The callback URL saves the event to the database and then pushes it to the websockets room of the streamer.
- The user is redirected to the stream page which has the embedded stream along with a list of 10 most recent follows that the user has received. 
- These events are initially fetched through the database but the new ones are pushed through the websocket as they happen.
