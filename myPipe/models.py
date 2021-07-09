import pymysql as sql
from django.http import Http404
import datetime

"""Connection setup"""
try:
    conn = sql.connect(host='localhost', user="root", password="Qwerty123!",
                       database='mypipe', charset="utf8mb4", cursorclass=sql.cursors.DictCursor)
except sql.Error as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))



class Functions:
    """Functions that do not represent any asset, but required to create or get such"""
    def create_account(self, info):
        """Creates an account if possible. If not possible return false"""
        try:
            cur = conn.cursor()
            cur.callproc("insert_user",
                         [info.get('username'),
                          info.get('password'),
                          info.get('email'),
                          info.get('avatar'),
                          info.get('phone')])
            conn.commit()
            cur.close()
            return True

        except sql.Error as e:
            conn.rollback()
            return False

    def update_account(self, info, old_acc):
        """Creates an account if possible. If not possible return false"""
        try:
            cur = conn.cursor()
            cur.callproc("update_acct",
                         [old_acc,
                          info.get('username'),
                          info.get('password'),
                          info.get('email'),
                          info.get('avatar'),
                          info.get('phone')])
            conn.commit()
            cur.close()
            return True

        except sql.Error as e:
            raise Http404(e.args)

    def create_channel(self, info: dict):
        """Creates a channel with the given login name. If not possible return false"""
        try:
            cur = conn.cursor()
            cur.callproc("insert_channel", (info['name'], info['description'], info['owner']))
            conn.commit()
            cur.close()
            return True

        except sql.Error as e:
            conn.rollback()
            return False

    def get_videos(self):
        """Gets the videos sorted from the most viewed, limited to 9"""
        try:
            cur = conn.cursor()
            cur.callproc("most_viewed", ())
            return cur.fetchall()
        except sql.Error as e:
            raise Http404(e.args)

    def get_streams(self):
        """Gets the streams sorted from the most viewed, limited to 9"""
        try:
            cur = conn.cursor()
            cur.callproc("most_streams", ())
            return cur.fetchall()
        except sql.Error as e:
            raise Http404(e.args)

    def search_video(self, search):
        """Searches the videos"""
        try:
            cur = conn.cursor()
            cur.callproc("search_video", (search,))
            result = cur.fetchall()
            cur.close()
            return result
        except sql.Error as e:
            raise Http404("FAILED SQL STATEMENT")
            # return False

    def search_stream(self, search):
        """Searches the stream"""
        try:
            cur = conn.cursor()
            cur.callproc("search_stream", (search,))
            result = cur.fetchall()
            cur.close()
            return result
        except sql.Error as e:
            raise Http404("FAILED SQL STATEMENT")
            # return False


class Accounts:
    """Account object, represents a user"""
    user = ""

    def __init__(self, user='none'):
        """Initialized by the user login, can find all the info from that as it is primary key"""
        self.user = user

    def login(self, login: str, password: str):
        """Attemts to login into the website. Returns if the login was successful"""
        try:
            cur = conn.cursor()
            cur.execute("select attempt_login(%s, %s) as total", (login, password))
            result = cur.fetchall()[0]['total']
            cur.close()
            return result
        except sql.Error as e:
            raise Http404(e.args)

    def info(self):
        """Gets the info of the account"""
        try:
            cur = conn.cursor()
            stmt = 'select * from users where username = %s'
            cur.execute(stmt, (self.user,))
            row = cur.fetchall()
            row = row[0]
            cur.close()

            return row
        except sql.Error as e:
            raise Http404(e.args)

    def subscribed(self, channel):
        """Checks if the user is subscribed to the channel"""
        try:
            cur = conn.cursor()
            cur.callproc("is_subscribed", (channel, self.user))
            row = cur.fetchall()[0]["result"]
            cur.close()
            return row
        except sql.Error as e:
            raise Http404(e.args)

    def channels(self) -> list:
        """Get accounts channel by its name, returns a list of channels"""
        try:
            cur = conn.cursor()
            cur.callproc("retrieve_channels", (self.user,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except sql.Error as e:
            raise Http404("SQL STATEMENT FAILED")

    def subscriptions(self) -> list:
        """Get the list of subscriptions"""
        try:
            cur = conn.cursor()
            cur.callproc("get_subscriptions", (self.user,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except sql.Error as e:
            raise Http404("SQL STATEMENT FAILED")

    def history(self):
        """Get the history of watched videos, ordered from the recent"""
        try:
            cur = conn.cursor()
            cur.callproc("get_history", (self.user,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except sql.Error as e:
            raise Http404(e.args)

    def stream_history(self):
        """Get the history of watched streams, ordered from the recent"""
        try:
            cur = conn.cursor()
            cur.callproc("get_stream_history", (self.user,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except sql.Error as e:
            raise Http404(e.args)

    def subscribe(self, channel: str):
        """Subscribes on the specific channel"""
        try:
            cur = conn.cursor()
            date = datetime.datetime.now()
            cur.callproc("insert_sub", (self.user, channel, date))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)

    def unsubscribe(self, channel):
        """Unsubscribes on the specific channel"""
        try:
            cur = conn.cursor()
            date = datetime.datetime.now()
            cur.callproc("remove_sub", (self.user, channel))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)

    def create_channel(self, channel_info: dict):
        """Creates a channel on the account"""
        try:
            cur = conn.cursor()
            cur.callproc('insert_channel', (channel_info['name'], channel_info['description'],
                                            self.user, channel_info["avatar"]))
            res = cur.fetchall()[0]['res']
            conn.commit()
            cur.close()
            return res
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)

    def close_account(self):
        """Deletes account and all its channel """
        try:
            cur = conn.cursor()
            stmt = "DELETE FROM users WHERE username = '%s';" % self.user
            cur.execute(stmt)
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)


class Channel:
    """Represents the channel asset"""
    name = ""

    def __init__(self, name: str):
        """Initializes the channel with its name, as it is a primary key"""
        self.name = name

    def channel_info(self):
        """Gets an info about the channel"""
        try:
            cur = conn.cursor()
            stmt = "Select * from channel where name = %s;"
            cur.execute(stmt, (self.name))
            row = cur.fetchall()[0]
            return row
        except sql.Error as e:
            raise Http404(e.args)

    def videos(self, num=10, descending=False) -> dict:
        """
        Gets the dictionary of videos presented on this channel
            num - the amount of videos presented
            sort_by - the sorting value
            descending - if should be presented in the descending order
        """
        try:
            cur = conn.cursor()
            cur.callproc('retrieve_videos', (self.name, num, descending))
            rows = cur.fetchall()
            return rows
        except sql.Error as e:
            raise Http404(e.args)

    def streams(self):
        """Gets all the streams of the channel"""
        try:
            cur = conn.cursor()
            cur.callproc("get_streams", (self.name,))
            rows = cur.fetchall()
            return rows
        except sql.Error as e:
            raise Http404(e.args)


    def delete_channel(self):
        """Deletes channel with ALL ITS VIDEOS"""
        try:
            cur = conn.cursor()
            stmt = "DELETE FROM channel WHERE name = '%s';" % self.name
            cur.execute(stmt)
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)

    def create_video(self, video: dict):
        try:
            cur = conn.cursor()
            cur.callproc("insert_video",
                         (video["name"],
                          video["description"],
                          video["channel"],
                          video["location"],
                          datetime.datetime.now(),
                          video["type"]))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)


    def create_stream(self, info: dict):
        """Creates a stream on the channel"""
        try:
            cur = conn.cursor()
            cur.callproc("insert_stream",
                         (info["name"],
                          info["description"],
                          info["channel"],
                          info["location"],
                          datetime.datetime.now(),
                          info["type"]))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)


class Content:
    """Represents any type of the content based on the content id"""
    def __init__(self, id: int):
        self.id = id

    def get_info(self) -> dict:
        """Gets info of a video content, including the channel name, and avatar"""
        try:
            cur = conn.cursor()
            cur.callproc("get_video", (self.id,))
            row = cur.fetchone()
            cur.close()
            return row
        except sql.Error as e:
            raise Http404(e.args)

    def stream_info(self) -> dict:
        """Gets info of a stream, for the video page, including the channel name, and avatar"""
        try:
            cur = conn.cursor()
            cur.callproc("get_stream", (self.id,))
            row = cur.fetchone()
            cur.close()
            return row
        except sql.Error as e:
            raise Http404(e.args)

    def view_video(self, account):
        """Saves the content in the history of account"""
        try:
            cur = conn.cursor()
            cur.callproc("view", (account, self.id, datetime.datetime.now()))
            conn.commit()
            cur.close()
        except sql.Error as e:
            raise Http404(e.args)

    def toggle_stream(self):
        """Toggles the stream"""
        try:
            cur = conn.cursor()
            cur.callproc("toggle_stream", (self.id,))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404('FAILED SQL STATEMENT')

    def change_info(self, new_info):
        """Change the video info"""
        try:
            cur = conn.cursor()
            cur.callproc('update_content', (self.id, new_info['name'],
                                            new_info['description']))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404('FAILED SQL STATEMENT')

    def leave_comment(self, account, comment: str, under_comment: int):
        """Leaves a comment under the video, and under the comment if specified"""
        try:
            cur = conn.cursor()
            date = datetime.date.today()
            cur.callproc("insert_comment", (self.id, account, date, comment, under_comment))
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404(e.args)

    def get_commments(self) -> dict:
        """Gets comments of the video, including the account avatar and name"""
        try:
            cur = conn.cursor()
            cur.callproc("get_comments", (self.id,))
            rows = cur.fetchall()
            return rows
        except sql.Error as e:
            raise Http404(e.args)

    def get_comment_replies(self):
        """Gets comment replies of the video, including the account avatar and name"""
        try:
            cur = conn.cursor()
            cur.callproc("get_replies", (self.id,))
            rows = cur.fetchall()
            return rows
        except sql.Error as e:
            raise Http404(e.args)

    def delete_video(self):
        """Deletes a video and ALL ITS COMMENTS"""
        try:
            cur = conn.cursor()
            stmt = "DELETE FROM content WHERE id = %d ;" % self.id
            cur.execute(stmt)
            conn.commit()
            cur.close()
        except sql.Error as e:
            conn.rollback()
            raise Http404("FAILED SQL STATEMENT")
