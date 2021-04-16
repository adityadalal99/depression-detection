import tweepy
from dotenv import load_dotenv
import os
import db_queries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


def send_email(user_id,depressive_tweets_id):
    ngo_mail = db_queries.get_ngo_for_mail(user_id)
    email_content = "<html><body>"
    for twee_id in depressive_tweets_id:
        email_content += get_tweet_html(twee_id, user_id)
    email_content += "</body></html>"
    sender_mail = os.getenv('EMAIL_ID')
    password = os.getenv('EMAIL_PASSWORD')
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_mail
    message["To"] = ngo_mail
    part2 = MIMEText(email_content, "html")
    message.attach(part2)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("Login successful")
    print(email_content)
    print(ngo_mail)
    server.sendmail(sender_mail, ngo_mail, message.as_string())
    print("Email sent successfully")


def get_tweet_html(tweet_id, user_id):
    #TODO user kaa naam lekke aa to put it in the start of mail kii yee naam kaa banda kamzor hai
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    api = tweepy.API(auth)
    tweet_url = os.getenv('TWEET_URL')
    tweet_url = tweet_url + tweet_id
    result = api.get_oembed(tweet_url, omit_script=True)
    print(result)
    html = result['html'].strip()
    return html


#get_tweet_html('463440424141459456',1)