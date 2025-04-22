import re
import pandas as pd

def preprocess(data):
    pattern = r"(\d{2}\/\d{2}\/\d{2}),\s(\d{1,2}:\d{2}\s[ap]m)\s-\s(.+)"
    messages = []
    dates = []

    # Extract all matches
    matches = re.findall(pattern, data)

    # Populate the messages and dates lists
    for match in matches:
        date_time = f"{match[0]}, {match[1]}"  # Combine date and time
        dates.append(date_time)
        messages.append(match[2])
    
    df = pd.DataFrame({"user_msg":messages, "message_date":dates})
    df["message_date"]= pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p")
    df.rename(columns={"message_date" :"date"},inplace=True)
    
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

    df['only_date']= df['date'].dt.date
    df['month_num']= df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_msg'],inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
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