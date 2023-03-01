import streamlit as st
import preprocssing
import helper
import matplotlib.pyplot as plt
import pandas as pd,seaborn as sns
st.sidebar.title("WHATSAPP CHAT ANALYZER")
st.title("MAKE INSIGHTS OUT OF YOUR DATA")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocssing.preprocessor(data)

    #st.dataframe(df)


    users_list=df['user'].unique().tolist()

    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,'Overall Users')

    
    user_selected=st.sidebar.selectbox("Analyses w.r.to",users_list)

    choice=st.sidebar.selectbox("Analysis On",['Full Data','Custom Range'])

    if(choice!="Full Data"):
        startdate=st.sidebar.date_input("Enter the Start date")
        enddate=st.sidebar.date_input("Enter the end date")

        startdate = pd.to_datetime(startdate).date()
        enddate = pd.to_datetime(enddate).date()
    else:
        startdate=pd.to_datetime(df['just_date'][0]).date()
        enddate=pd.to_datetime(df['just_date'][df.shape[0]-1]).date()

    

    # print(startdate)
    # print(enddate)


    if(st.sidebar.button("Start Analysis")):
        
        total_messages,total_media,total_links=helper.fetch_analysis(user_selected,df,startdate,enddate)


        st.title("GENERAL STATISTICS")
        c1,c2,c3=st.columns(3)

        
        with c1:
            st.header("TotalMessages")
            st.title(total_messages)

        with c2:
            st.header("Media Shared")
            st.title(total_media)

        with c3:
            st.header("Links Shared")
            st.title(total_links)


        st.title("WORDCLOUD")
        wc_img=helper.create_wordcloud(user_selected,df,startdate,enddate)

        fig,ax=plt.subplots()
        ax.imshow(wc_img)
        st.pyplot(fig)


        st.title("MOST COMMON WORDS")

        common_words_df=helper.most_common_words(user_selected,df,startdate,enddate)

        fig,ax=plt.subplots()

        ax.barh(common_words_df[0],common_words_df[1],color='lightgreen')
        st.pyplot(fig)
        #st.dataframe(common_words_df)


        st.title("EMOJI ANALYSIS")

        emojis=helper.emoji_count(user_selected,df,startdate,enddate)

        if(isinstance(emojis,pd.DataFrame)):
            # c1,c2=st.columns(2)

            # with c1:
            st.dataframe(emojis)
        else:
            st.text("No Emojis used")

        # with c2:
        #     fig,ax=plt.subplots()
        #     ax.barh(emojis[0],emojis[1])
        #     st.pyplot(fig)


        st.title("MONTHLY CHAT ANALYSIS")

        timeline_df=helper.timeline_plot(user_selected,df,startdate,enddate)

        fig,ax=plt.subplots()
        ax.plot(timeline_df['monthandyear'],timeline_df['msgs'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        st.title("DAY WISE CHAT ANALYSIS")

        day_wise_df=helper.day_wise_plot(user_selected,df,startdate,enddate)

        fig,ax=plt.subplots()
        ax.bar(day_wise_df.index,day_wise_df.values,color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("MONTH WISE CHAT ANALYSIS")

        month_wise_df=helper.month_wise_plot(user_selected,df,startdate,enddate)

        fig,ax=plt.subplots()
        ax.bar(month_wise_df.index,month_wise_df.values,color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("Activity Heat Map")

        user_heatmap = helper.heatmap(user_selected,df,startdate,enddate)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)







        if(user_selected=="Overall Users"):

            st.title("GROUP STATISTICS")

            top_5_users,percent_df=helper.fetch_group_analysis(df,startdate,enddate)
            users=top_5_users.index
            values=top_5_users.values
            
           
            c1,c2=st.columns(2)

            with c1:
                st.header("Most Frequent Users")
                fig, ax=plt.subplots()

                ax.bar(users,values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with c2:
                st.header("Percentage of msgs")
                st.dataframe(percent_df)


        
                

                    










        
        

    

