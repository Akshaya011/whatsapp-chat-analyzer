import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extractor  = URLExtract()


def fetch_stats(user,df):

    if user != 'Overall':
        df = df[df['user'] == user]
    num_msg= df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split(' '))

    num_media = df[df['message'] == '<Media omitted>'].shape[0]

    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))
    num_links = len(links)
    return num_msg,len(words),num_media,num_links

def most_busy_user(df):
    x=df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':"percent"})
    return x,new_df
    
def create_wordcloud(user, df):
    if user != 'Overall':
        df = df[df['user'] == user]
    
    wc=WordCloud(width=500,height=500,min_font_size=10, background_color='white')
    df_wc= wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

def most_common_words(user,df):
    if user != 'Overall':
        df = df[df['user'] == user]
    temp = df[df['user'] !='group_notification']
    temp = temp[temp['message'] !='<Media omitted>' ]
    words =[]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    stop_words = stop_words.split('\n')

    for messag in temp['message']:
        for word in messag.split():
          if word not in stop_words:
            words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(user,df):
    if user != 'Overall':
        df = df[df['user'] == user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# analysing time-line
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
