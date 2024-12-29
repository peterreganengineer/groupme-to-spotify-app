from datetime import datetime
import re
from groupme_client import groupmeClient
import mysql.connector

# Set up the connection
mydb = mysql.connector.connect(
    host="localhost", user="root", password="n4LB6q9Xozu9XqdP8vPF", database="groupme"
)

if mydb.is_connected():
    print("Connected to groupme db")

mycursor = mydb.cursor()

add_message_query = "INSERT INTO message (message_id,group_id,user_id,text,reaction_count,created_at,is_song) VALUES (%s,%s,%s,%s,%s,%s,%s)"

gc = groupmeClient("backend/Auth-Text-Files/GroupmeAuth.txt")

totalMessages = gc.get_group_message_count()

messages = gc.get_group_messages(limit=1, before_id=173532091886784406)
print(messages)
# find all messages that are songs
for message in messages:

    # handle groupme system messages
    if message["user_id"] == "system":
        message["user_id"] = 1

    # setup reaction_count
    message["reaction_count"] = 0
    if "reactions" in message and message["reactions"]:
        for reaction in message["reactions"]:
            message["reaction_count"] += len(reaction["user_ids"])

    # setup is_song
    if "text" in message and message["text"]:
        urls = re.findall(r"(https://open.spotify.com/track/[\w\d]+)", message["text"])
        if len(urls) > 0:
            message["is_song"] = 1
        else:
            message["is_song"] = 0
    else:
        message["text"] = ""
        message["is_song"] = 0

    # format created_at to proper MySQL datetime
    dt_object = datetime.fromtimestamp(int(message["created_at"]))
    message["created_at"] = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    print(message["created_at"])

    # Insert data into the database
    try:
        mycursor.execute(
            add_message_query,
            (
                message.get("id"),
                message.get("group_id"),
                message.get("user_id"),
                message.get("text"),
                message.get("reaction_count"),
                message.get("created_at"),
                message.get("is_song"),
            ),
        )
        print(f"Inserted message {message.get('message_id')}")
    except mysql.connector.Error as err:
        print(f"Error inserting message {message.get('message_id')}: {err}")


# Commit the transaction to the database
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()
