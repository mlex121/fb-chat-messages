FB Chat Breakdown
=================

This is a quick script I wrote up to count how many messages each of my friends
posted in a big group chat.

This script depends on the Facebook Platform Python SDK found here:
https://github.com/pythonforfacebook/facebook-sdk

It uses the Graph API to page through an entire conversation and count the
number of messages each participant has sent. The entire chat can be written to
an output file if desired.

Step-by-Step Instructions
-------------------------

1. Go to the Facebook Graph API Explorer
(https://developers.facebook.com/tools/explorer) and sign in if you haven't yet
done so.

2. Click "Get Access Token", go to the "Extended Permissions" tab, and ensure
that "read_mailbox" is checked.

3. Click "Get Access Token", follow any instructions that appear, then copy the
access token from the text box.

4. In the text box with containing the query, replace the contents with
'/me/inbox' and submit.

5. Find the conversation you want to analyze in the query results and copy its
'id' field.

6. Run the script using the access token and chat ID as the parameters.

Usage
-----

```
get_chat_messages.py [-h] [-o OUTPUT_FILE] [-t TIMEOUT] token chat_id

positional arguments:
  token                 A Facebook access token. Can be retrieved from the
                        Graph API Explorer:
                        https://developers.facebook.com/tools/explorer
  chat_id               The Facebook ID of the chat you want to analyze. You
                        can get these IDs from /me/inbox.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Writes the chat messages in JSON format to the
                        specified file.
  -t TIMEOUT, --timeout TIMEOUT
                        Provide a timeout (in seconds) between successive
                        Graph API calls to prevent being locked out due to too
                        many. Defaults to 1.
```
