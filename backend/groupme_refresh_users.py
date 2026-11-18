from groupme_client import groupmeClient
import mysql.connector
import os
from dotenv import load_dotenv

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

mycursor = mydb.cursor()

add_user_query = (
    "INSERT INTO user (user_id,nickname,name,image_url) VALUES (%s,%s,%s,%s)"
)
update_user_query = "UPDATE user SET nickname = %s, name = %s, image_url = %s WHERE user_id = %s AND (nickname <> %s OR name <> %s OR image_url <> %s)"
check_user_exists_query = "SELECT COUNT(1) FROM user WHERE user_id = %s"


gc = groupmeClient()

group_data = gc.get_group()
if "error" in group_data:
    print(f"Error fetching group data: {group_data['error']}")
    exit(1)

members = group_data["members"]


# Insert data into the database
for member in members:
    try:
        mycursor.execute(check_user_exists_query, (member.get("user_id"),))
        user_exists = mycursor.fetchone()[0]
        if user_exists:
            mycursor.execute(
                update_user_query,
                (
                    member.get("nickname"),
                    member.get("name"),
                    member.get("image_url"),
                    member.get("user_id"),
                    member.get("nickname"),
                    member.get("name"),
                    member.get("image_url"),
                ),
            )
            print(f"Updated member: {member.get('nickname')}")
        else:
            mycursor.execute(
                add_user_query,
                (
                    member.get("user_id"),
                    member.get("nickname"),
                    member.get("name"),
                    member.get("image_url"),
                ),
            )
            print(f"Inserted new member: {member.get('nickname')}")
    except mysql.connector.Error as err:
        print(f"Error inserting member {member.get('nickname')}: {err}")

# Commit the transaction to the database
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()
