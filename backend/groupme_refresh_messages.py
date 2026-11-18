from datetime import datetime
import re
import time
import os
from dotenv import load_dotenv
from groupme_client import groupmeClient
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Set up the connection
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

if mydb.is_connected():
    print("Connected to groupme db")

add_message_query = "INSERT INTO message (message_id,group_id,user_id,text,reaction_count,created_at,is_song) VALUES (%s,%s,%s,%s,%s,%s,%s)"

gc = groupmeClient()

totalMessages = gc.get_group_message_count()


def fetch_and_add_latest(mydb):

    # get the latest groupme message in the db
    get_latest_message_query = (
        "SELECT message_id FROM groupme.message ORDER BY created_at DESC LIMIT 1"
    )
    mycursor = mydb.cursor()
    mycursor.execute(get_latest_message_query)
    latest_message_id = mycursor.fetchone()[0]

    # get newly sent messages
    while True:
        limit = 20
        messages = gc.get_group_messages(limit=limit, after_id=latest_message_id)

        if "error" in messages:
            break
        elif not messages:
            print("No more messages found.")
            break
        else:
            latest_message_id = messages[len(messages) - 1]["id"]
            add_messages_to_db(messages, mycursor)

    # Commit the transaction to the database
    mydb.commit()

    # Close the cursor and connection
    mycursor.close()


def fetch_and_add_all(mydb):

    # get the latest groupme message in the db
    get_first_message_query = (
        "SELECT message_id FROM groupme.message ORDER BY created_at ASC LIMIT 1"
    )
    mycursor = mydb.cursor()
    mycursor.execute(get_first_message_query)
    first_message_id = mycursor.fetchone()[0]

    # get newly sent messages
    while True:
        limit = 20
        messages = gc.get_group_messages(limit=limit, before_id=first_message_id)

        if "error" in messages:
            # added in extra retry for groupme rate limiting
            time.sleep(10)
            messages = gc.get_group_messages(limit=limit, before_id=first_message_id)
            if "error" in messages:
                break
        elif not messages:
            print("No more messages found.")
            break
        else:
            first_message_id = messages[len(messages) - 1]["id"]
            add_messages_to_db(messages, mycursor)

    # Commit the transaction to the database
    mydb.commit()

    # Close the cursor and connection
    mycursor.close()


def add_messages_to_db(messages, mycursor):

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
            urls = re.findall(
                r"(https://open.spotify.com/track/[\w\d]+)", message["text"]
            )
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
            print(
                f"Inserted message -- id: {message.get('id')}, text: {message.get('text')}"
            )
        except mysql.connector.Error as err:
            print(f"Error inserting message {message.get('message_id')}: {err}")


fetch_and_add_latest(mydb)

# uncomment to fetch all instead of latest
# fetch_and_add_all(mydb)

mydb.close()
