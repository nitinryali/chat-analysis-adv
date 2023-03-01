from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import nltk
nltk.download('stopwords')
import emoji
stopwords = nltk.corpus.stopwords.words('english')
extract=URLExtract()


def fetch_analysis(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]
    
    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
    total_msgs=df.shape[0]

    media_df=df[df['msgs']=='<Media omitted>\n']
    total_media=media_df.shape[0]


    links=[]

    for msg in df['msgs']:
        links.extend(extract.find_urls(msg))

    total_links=len(links)

    return total_msgs,total_media,total_links

#Group Analysis
def fetch_group_analysis(df,startdate,enddate):
    # startdate = pd.to_datetime(startdate).date()
    # enddate = pd.to_datetime(enddate).date()
    new_df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
    top_users_df=new_df['user'].value_counts().head()

    percentage_df=(round((new_df['user'].value_counts()/new_df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'}))

    return top_users_df,percentage_df


def create_wordcloud(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]

    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    temp=df[df['user']!="group_notification"]
    new_df=temp[temp['msgs']!="<Media omitted>\n"]

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)


    wc=WordCloud(width=300,height=300,min_font_size=10,background_color='white')
    new_df['msgs']=new_df['msgs'].apply(remove_stopwords)
    wc_img=wc.generate(new_df['msgs'].str.cat(sep=" "))

    return wc_img


def most_common_words(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]

    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
    temp=df[df['user']!="group_notification"]
    temp=temp[temp['msgs']!="<Media omitted>\n"]

    words=[]

    for msg in temp['msgs']:
        for word in msg.lower().split():
            if word not in stopwords and not emoji.distinct_emoji_list(word):
                words.append(word)

    common_words_df=pd.DataFrame(Counter(words).most_common(10))

    return common_words_df


def emoji_count(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]

    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    emojis=[]

    for msg in df['msgs']:
        if(emoji.distinct_emoji_list(msg)):
            emojis.append(emoji.distinct_emoji_list(msg))

    new_emojis=[]
    emoji_meaning=[]
    for i in emojis:
        for j in i:
            new_emojis.append(j)

    if(len(new_emojis)!=0):
        emoji_df=pd.DataFrame(Counter(new_emojis).most_common(10))
        for k in emoji_df[0]:
            emoji_meaning.append(emoji.demojize(k))
            
        emoji_df.rename(columns={0:'Emoji',1:'Count'},inplace=True)
        emoji_df['meaning']=emoji_meaning
        return emoji_df
    
    return 0


def timeline_plot(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]

    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    new_df=df.groupby(['year','month_num','month']).count()['msgs'].reset_index()
    monthandyear=[]
    for i in range(new_df.shape[0]):
        monthandyear.append(new_df['month'][i]+"-"+str(new_df['year'][i]))
    new_df['monthandyear']=monthandyear

    return new_df


def day_wise_plot(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]

    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    #new_df=df.groupby(['day_name']).count()['msgs'].reset_index()

    new_df=df['day_name'].value_counts()

    return new_df


def month_wise_plot(user_selected,df,startdate,enddate):
    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]
    
    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    #new_df=df.groupby(['day_name']).count()['msgs'].reset_index()

    new_df=df['month'].value_counts()

    return new_df



def heatmap(user_selected,df,startdate,enddate):

    if(user_selected!='Overall Users'):
        df=df[df['user']==user_selected]
    
    df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='msgs', aggfunc='count').fillna(0)

    return user_heatmap







    


    



    


# from urlextract import URLExtract
# from wordcloud import WordCloud
# import pandas as pd
# from collections import Counter
# import nltk
# nltk.download('stopwords')
# import emoji
# stopwords = nltk.corpus.stopwords.words('english')
# extract=URLExtract()


# def fetch_analysis(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]
    
#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
#     total_msgs=df.shape[0]

#     media_df=df[df['msgs']=='<Media omitted>\n']
#     total_media=media_df.shape[0]


#     links=[]

#     for msg in df['msgs']:
#         links.extend(extract.find_urls(msg))

#     total_links=len(links)

#     return total_msgs,total_media,total_links

# #Group Analysis
# def fetch_group_analysis(df,startdate,enddate):
#     # startdate = pd.to_datetime(startdate).date()
#     # enddate = pd.to_datetime(enddate).date()
#     new_df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
#     top_users_df=new_df['user'].value_counts().head()

#     percentage_df=(round((new_df['user'].value_counts()/new_df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'}))

#     return top_users_df,percentage_df


# def create_wordcloud(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]

#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

#     temp=df[df['user']!="group_notification"]
#     new_df=temp[temp['msgs']!="<Media omitted>\n"]

#     def remove_stopwords(message):
#         y=[]
#         for word in message.lower().split():
#             if word not in stopwords:
#                 y.append(word)
#         return " ".join(y)


#     wc=WordCloud(width=300,height=300,min_font_size=10,background_color='white')
#     new_df['msgs']=new_df['msgs'].apply(remove_stopwords)
#     wc_img=wc.generate(new_df['msgs'].str.cat(sep=" "))

#     return wc_img


# def most_common_words(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]

#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]
#     temp=df[df['user']!="group_notification"]
#     temp=temp[temp['msgs']!="<Media omitted>\n"]

#     words=[]

#     for msg in temp['msgs']:
#         for word in msg.lower().split():
#             if word not in stopwords and not emoji.distinct_emoji_list(word):
#                 words.append(word)

#     common_words_df=pd.DataFrame(Counter(words).most_common(10))

#     return common_words_df


# def emoji_count(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]

#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

#     emojis=[]

#     for msg in df['msgs']:
#         if(emoji.distinct_emoji_list(msg)):
#             emojis.append(emoji.distinct_emoji_list(msg))

#     new_emojis=[]
#     emoji_meaning=[]
#     for i in emojis:
#         for j in i:
#             new_emojis.append(j)

#     if(len(new_emojis)!=0):
#         emoji_df=pd.DataFrame(Counter(new_emojis).most_common(10))
#         for k in emoji_df[0]:
#             emoji_meaning.append(emoji.demojize(k))
            
#         emoji_df['meaning']=emoji_meaning
#         return emoji_df
    
#     return 0


# def timeline_plot(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]

#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

#     new_df=df.groupby(['year','month_num','month']).count()['msgs'].reset_index()
#     monthandyear=[]
#     for i in range(new_df.shape[0]):
#         monthandyear.append(new_df['month'][i]+"-"+str(new_df['year'][i]))
#     new_df['monthandyear']=monthandyear

#     return new_df


# def day_wise_plot(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]

#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

#     #new_df=df.groupby(['day_name']).count()['msgs'].reset_index()

#     new_df=df['day_name'].value_counts()

#     return new_df


# def month_wise_plot(user_selected,df,startdate,enddate):
#     if(user_selected!='Overall Users'):
#         df=df[df['user']==user_selected]
    
#     df=df[(df['just_date']>=startdate) & (df['just_date']<=enddate)]

#     #new_df=df.groupby(['day_name']).count()['msgs'].reset_index()

#     new_df=df['month'].value_counts()

#     return new_df







    


    



    

