import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import emoji

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data =  uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt ",user_list)
    if st.sidebar.button('Show Analysis'):
        num_msg,words,num_media,num_links = helper.fetch_stats(selected_user,df)

        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total message")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("media shared")
            st.title(num_media)
        with col4:
            st.header("links shared")
            st.title(num_links)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        if selected_user == 'Overall':
            x,new_df = helper.most_busy_user(df)
            st.title('Most Busy Users')
            
            col1,col2=st.columns(2)
            with col1:
                fig,ax = plt.subplots()
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.title('Shared %')
                st.dataframe(new_df)
        
        # Display the word cloud
        df_wc = helper.create_wordcloud(selected_user,df)
        st.title("WordCloud")
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words dataframe showing

        most_common_df = helper.most_common_words(selected_user,df)
        
        st.title("Most common words by "+ selected_user)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)


        #  emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2  = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
