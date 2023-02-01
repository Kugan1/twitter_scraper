#TWITTER_SCRAPING

#Import_required_modules
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import time
import snscrape.modules.twitter as sntwitter

def main():
    menu = ["HOME","ABOUT"]
    choice = st.sidebar.selectbox("MENU",menu)

    if choice == "HOME":
        col1,col2,col3,col4,col5=st.columns(5)
        with col2:
            st.image("https://media.giphy.com/media/SMKiEh9WDO6ze/giphy.gif")

        with col3:
            st.title('TWITTER_SCRAP')
            # Create a input 
        hashtag=st.text_input('Enter the Username or Hashtag(#example) ')
        tconut=st.number_input("Tweet count need to scraped",0,1000000)
        from_date=st.date_input("Since")
        end_date=st.date_input("Until")
        
        #create a button
        
        load=st.button('SCRAP')
        if "load_state" not in st.session_state:
            st.session_state.load_state=False
        
        if load or st.session_state.load_state :
            st.session_state.load_state=True
           
            with st.spinner("Please wait..."):
                time.sleep(3)
            
            tweets = []
            for tweet in sntwitter.TwitterSearchScraper('{}'.format(hashtag)).get_items():
                if len(tweets)== tconut:
                    break
                else:
                    tweets.append({'date': tweet.date, 'id': tweet.id, 'url': tweet.url,'tweet_content': tweet.content,'user': tweet.user.username,
                     'replyCount': tweet.replyCount, 'retweet_count': tweet.retweetCount,'language': tweet.lang, 'source': tweet.source, 'like_count': tweet.likeCount})
            df=pd.DataFrame(tweets,columns=["date","id","url","content","user","replyCount","retweetCount","language","source","likeCount"])
            
            #display DataFrame
            st.dataframe(df)

            left,right=st.columns(2)
            with right:
                connect=st.button('upload Database')
                

                if connect:
                    
                    client = MongoClient("mongodb://localhost:27017/")
                    # database
                    db = client["twitter_scrap"]
                    # collection
                    collection= db[f"{hashtag}_tweets"]
                    df.reset_index(inplace=True)

                    dict=df.to_dict(orient='records')
                    collection.insert_one({"index":"scaped data","data":dict})
                    st.success("successfully Uploaded")
            with left:
                if st.download_button(
                    "download as csv",
                    df.to_csv(),
                    file_name=f"{hashtag}_tweets_data.csv",
                    mime='text/csv'
                    ):
                    st.success("File Downloaded")

                if st.download_button(
                    "downlaod as json",
                    df.to_json(orient='records', force_ascii=False, indent=4, default_handler=str),
                    file_name=f"{hashtag}_tweets_data.json",
                    mime='application/json'
                    ):
                    st.success("File downloaded")

    if choice =="ABOUT":
        st.title("THANKYOU")

if __name__ == '__main__':
    main()