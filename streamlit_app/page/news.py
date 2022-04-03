import streamlit as st


def news_content(sidebar_container):
    st.header("News")
    tweets_urls = ["https://twitter.com/HubGeology/status/1508093539825057793",
                   "https://twitter.com/ipma_pt/status/1506630852092076036",
                   "https://twitter.com/ReutersScience/status/1507488784560144388",
                   "https://twitter.com/SotisValkan/status/1508064426808782855"]

    tweet_cols = st.columns(len(tweets_urls))
    for idx, c in enumerate(tweet_cols):
        with c:
            st.tweet(tweets_urls[idx])
