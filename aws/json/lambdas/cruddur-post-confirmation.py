import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print(user)
    display_name = user['name']
    email = user['email']
    handle = user['preferred_username']
    cognito_user_id = user['sub']
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        sql = f"""
        INSERT INTO users (display_name, email, handle, cognito_user_id) 
        VALUES('{display_name}', '{email}', '{handle}', '{cognito_user_id}')
        """
        print(sql)
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
    