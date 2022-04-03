import streamlit.components.v1 as components
import requests


def tweet(tweet_url: str):
    # Use Twitter's oEmbed API
    # https://dev.twitter.com/web/embedded-tweets
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    text = response.json()["html"]

    return components.html(text, height=500)
