import re
import pandas as pd

def preprocessor(data)->pd.DataFrame:

    lines=data.split("\n")
    x=lines[0]
    check=0
    if(("am" in x) or("pm" in x) or ("AM" in x) or ("PM" in x)):
        pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[aAPp][mM]\s-\s'
        check=1
    else:
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_msg':messages,'msg_date':dates})
    x=dates[0]
    if((len(x[6:-12])<4) and (check==1)):
        df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%y, %I:%M %p - ')
    elif((len(x[6:-10])<4) and (check==0)):
        df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%y, %H:%M - ')
    elif((len(x[6:-10])>=4) and (check==0)):
        df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%Y, %H:%M - ')
    else:
        df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%Y, %I:%M %p - ')

        
    users = []
    messages = []
    for message in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['msgs']=messages

    df.drop(['user_msg'],inplace=True,axis=1)

    df.rename(columns={'msg_date':'date'},inplace=True)
    df['just_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period



    return df
    


# import re
# import pandas as pd

# def preprocessor(data)->pd.DataFrame:
#     pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[aAPp][mM]\s-\s'
#     messages=re.split(pattern,data)[1:]
#     dates=re.findall(pattern,data)
#     df=pd.DataFrame({'user_msg':messages,'msg_date':dates})
#     x=dates[1][6:]
#     if(len(x[:-13])==2):
#         df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%y, %I:%M %p - ')
#     else:
#         df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%Y, %I:%M %p - ')
# #     df=pd.DataFrame({'user_msg':messages,'msg_date':dates})
# #     df['msg_date']=pd.to_datetime(df['msg_date'],format='%d/%m/%Y, %I:%M %p - ')
#     users = []
#     messages = []
#     for message in df['user_msg']:
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])
#     df['user']=users
#     df['msgs']=messages

#     df.drop(['user_msg'],inplace=True,axis=1)

#     df.rename(columns={'msg_date':'date'},inplace=True)
#     df['just_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute


#     return df
    
