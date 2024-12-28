from groupme_client import groupmeClient
import mysql.connector

# Set up the connection
mydb = mysql.connector.connect(
    host="localhost", user="root", password="n4LB6q9Xozu9XqdP8vPF", database="groupme"
)

if mydb.is_connected():
    print("Connected to groupme db")

mycursor = mydb.cursor()

add_user_query = (
    "INSERT INTO user (user_id,nickname,name,image_url) VALUES (%s,%s,%s,%s)"
)

gc = groupmeClient("backend/Auth-Text-Files/GroupmeAuth.txt")

members = gc.get_group()["members"]


# Insert data into the database
for member in members:
    try:
        mycursor.execute(add_user_query, (
            member.get("user_id"),
            member.get("nickname"),
            member.get("name"),
            member.get("image_url"),
        ))
    except mysql.connector.Error as err:
        print(f"Error inserting member {member.get('user_id')}: {err}")

# Commit the transaction to the database
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()