from flask import flash, session
import mysql.connector




def connect_db():
    config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 8889,
    'database': 'monmangaorg',
    'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(prepared=True)
    return cnx, cursor


def check_user_exist(username):
    cnx, cursor = connect_db()
    query_check_user= """ SELECT * from users WHERE USERNAME = %s """
    cursor.execute(query_check_user, (username,))
    results= cursor.fetchall()
    print(results)
    if len(results) != 0:
        return True

    else:
        return False

def get_user(username):
    cnx, cursor = connect_db()
    query_check_user= """ SELECT * from users WHERE USERNAME = %s """
    cursor.execute(query_check_user, (username,))
    results= cursor.fetchall()
    if len(results) != 0:
        cnx.close()
        return results[0]
    else:
        cnx.close()
        flash('Wrong username', category='alert')
        return 0

def add_user(username, password):
    query_add_user=""" INSERT INTO `users` (`USERNAME`, `PASSWORD`) VALUES (%s,%s) """
    cnx, cursor = connect_db()
    if not check_user_exist(username):
        print('adding user')
        cursor.execute(query_add_user, (username, password))
        cnx.commit()
        cnx.close()
        flash(f'Account created', category='success')
        session['USERNAME'] = get_user(username)[0]
        print(session['USERNAME'])
    else:
        cnx.close()
        flash('Username already taken please change', category='alert')

def get_manga_list(username):
    query = """SELECT * FROM mangas WHERE id_manga IN (SELECT id_manga FROM subscriber WHERE subscriber.id_user = %s);"""

    pass

def add_manga(title):
    query = """INSERT INTO mangas VALUES (%s)"""

def follow_manga(username, id_manga):
    pass

def unfollow_manga(username, id_manga):
    pass