#!/usr/bin/env python3
import secrets
import praw
# import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Returns tuples containing keyword count, weighted score, post info dict of matching posts

SUBREDDIT_TO_EXPLORE = 'webdev'
NUM_POSTS_TO_EXPLORE = 10
SCORE_WEIGHT = 3
COMMENT_WEIGHT = 1
# The following is the minimum relevant weighted score to be a match,
# where weighted score = SCORE_WEIGHT * score + COMMENT_WEIGHT * num comments
MIN_RELEVANT_WEIGHTED_SCORE = 20
# The following tuple contains 1. list of required terms/stems, 2. list of secondary terms,
# 3. min number of secondary terms needed to be a match
KEYWORDS_GROUP = ([], ['angular', 'python', 'security', 'nodejs', 'new', 'mean'], 1)
matching_posts_info_string = ""
# Returns a count of secondary terms if is relevant, -1 otherwise


def get_keyword_count(str):
    keyword_count = 0
    required, secondary, min_secondary = KEYWORDS_GROUP
    for required_term in required:
        if required_term not in str:
            return -1
    for secondary_term in secondary:
        if secondary_term in str:
            # A secondary term was found, so add to keyword_count
            keyword_count += 1
    if keyword_count < min_secondary:
        return -1
    return keyword_count


def get_reddit_posts():
    # Authenticate
    reddit = praw.Reddit(client_id=secrets.MY_CLIENT_ID,
                         client_secret=secrets.MY_CLIENT_SECRET,
                         user_agent=secrets.MY_USER_AGENT,
                         username=secrets.MY_REDDIT_USERNAME,
                         password=secrets.MY_REDDIT_PASSWORD)
    # Designate subreddit to explore
    subreddit = reddit.subreddit(SUBREDDIT_TO_EXPLORE)
    matching_posts_info = []
    # Explore rising posts in subreddit and store info if is relevant and popular enough
    # Tip: You could also explore top posts, new posts, etc.
    # See https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#obtain-submission-instances-from-a-subreddit
    for submission in subreddit.rising(limit=NUM_POSTS_TO_EXPLORE):
        keyword_count = get_keyword_count(submission.title.lower())
        weighted_score = SCORE_WEIGHT * submission.score + \
            COMMENT_WEIGHT * len(list(submission.comments))
        # if keyword_count != -1 and weighted_score > MIN_RELEVANT_WEIGHTED_SCORE:
        post_dict = {'title': submission.title,
                     'score': submission.score,
                     'url': submission.url,
                     'comment_count': len(list(submission.comments))}
        matching_posts_info.append(
            (keyword_count, weighted_score, post_dict))
        global matching_posts_info_string
        matching_posts_info_string += matching_posts_info_string + post_dict.get('title').replace(" ", "_") + '?' + post_dict.get('url')  + ' '
    # Sort asc by the keyword count, then desc by weighted score (can't sort by post_dict)
    # matching_posts_info.sort(key=lambda x: (x[0], -1 * x[1]))
    return matching_posts_info
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

if __name__ == "__main__":
    matching_posts_info = get_reddit_posts()
    # writing results to a file
    # print(matching_posts_info_string)
    with open("./node/posts.dat", "w") as file:
        file.write(deEmojify(matching_posts_info_string))
    # bashCommand = "node index.js " + matching_posts_info_string + secrets.PASS_GMAIL 
    os.system("cd node && node index.js")

