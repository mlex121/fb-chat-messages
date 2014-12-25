#!/usr/bin/python
"""This is a quick script I wrote up to count how many messages each
of my friends posted in a big group chat.

This script depends on the Facebook Platform Python SDK found here:
    https://github.com/pythonforfacebook/facebook-sdk
"""

from __future__ import division

import argparse
import facebook
import json
import time

from collections import defaultdict
from urlparse import urlsplit


def main():
    """Uses the Facebook Graph API to get chat messages for the given ID
    and prints the number of messages each chat participant posted.

    Will write the chat messages in JSON format to a file if specified.
    """

    args = get_arguments()

    data = []
    graph = facebook.GraphAPI(args.token)
    chat_id = args.chat_id

    try:
        comments = graph.get_object(chat_id + "/comments")
    except facebook.GraphAPIError as e:
        print e
    else:
        more_comments = True
        while more_comments:
            comments_data = comments.get('data', [])
            data.extend(comments_data)
            paging_next = comments.get('paging', {}).get('next')
            if paging_next:
                next_page_query = urlsplit(paging_next)[3]

                # Prevents hammering the Graph API and getting
                # locked out.
                time.sleep(args.timeout)
                comments = graph.get_object(
                    chat_id + "/comments?" + next_page_query)
            else:
                more_comments = False

    if len(data) and args.output_file:
        with open(args.output_file, 'w+') as f:
            f.write(json.dumps(data))

    print_results(data)


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Grabs messages in a given Facebook chat and provides a '
                    'numerical break-down of the participants\' messages.')

    parser.add_argument('token',
                        help='A Facebook access token. Can be retrieved from '
                             ' the Graph API Explorer: '
                             'https://developers.facebook.com/tools/explorer')
    parser.add_argument('chat_id',
                        help='The Facebook ID of the chat you want to analyze.'
                             ' You can get these IDs from /me/inbox.')
    parser.add_argument('-o', '--output_file',
                        help='Writes the chat messages in JSON format to the '
                             'specified file.')
    parser.add_argument('-t', '--timeout',
                        default=1,
                        help='Provide a timeout (in seconds) between '
                             'successive Graph API calls to prevent being '
                             'locked out due to too many. Defaults to 1.')

    return parser.parse_args()

def print_results(data):
    """Print the number of messages for each user in the chat.

    Calculate how many messages each participant in the chat has sent,
    along with what percentage of the chat's messages are theirs.
    """
    mapping = defaultdict(lambda: {'count': 0, 'ratio': 0})

    for comment in data:
        # Sometimes there are chats which are missing a 'from' field in
        # the messages.
        try:
            author = comment['from']['name']
        except KeyError as e:
            author = '<UNKNOWN_AUTHOR>'
        mapping[author]['count'] += 1

    for key, value in mapping.items():
        value['ratio'] = value['count'] / len(data)
        print "{}: {} messages ({:.2%} of the chat)".format(
            key, value['count'], value['ratio'])


if __name__ == '__main__':
    main()
