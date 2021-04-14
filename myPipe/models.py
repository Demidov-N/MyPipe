import pymysql as sql

# Create your models here.
# Models are represented as classes, created manually through PyMySQL

# TODO: connect MySQL and create a cursor




class Accounts:
    """TODO: Finish the whole class"""
    """Account object, represents a user"""
    user = ""

    def __init__(self, user='none'):
        """Initialized by the user login, can find all the info from that"""
        self.user = user

    def login(self, login: str, password: str):
        #TODO Should check the fact that the account exist and there is an account at all
        if login == "RedBear" and password == '1234':
            self.user = login
            return True
        else:
            return False

    def info(self):
        """TODO: Just a SQL statement getting by user login"""
        return {
            'username': 'RedBear',
            'email': 'redbear@none.com',
            'avatar': 'redbear.png'
        }


    def channels(self) -> list:
        """Get accounts channel by its name, returns a list of channels
        TODO: define is it a list of channel objects or the list of channel names, or a dictionary"""

        return [
            {
                'name': "PIDARAS TV",
                'subscribers': 2,
                'videos': 0,
                'owner': 'RedBear',
                'avatar': 'empty.png',
                'description': "a channel about a beauiful people we are surrounded with"
            },
            {
                'name': "UEBOK TV",
                'subscribers': 30,
                'videos': 3,
                'owner': 'RedBear',
                'avatar': 'empty.png',
                'description': "a channel about a beautifl person Danya"
            }
        ]

    def subscriptions(self) -> list:
        """Get the list of subscriptions"""
        return [
            {
                'name': "PIDARAS TV",
                'subscribers': 2,
                'videos': 0,
                'owner': 'RedBear',
                'avatar': 'empty.png'
            },
            {
                'name': "UEBOK TV",
                'subscribers': 30,
                'videos': 3,
                'owner': 'RedBear',
                'avatar': 'empty.png'
            }
        ]

    def change_info(self, new_info: dict):
        pass


    def subscribe(self, channel):
        """Subscribes on the specific channel"""

    def create_channel(self, channel_info: dict):
        """Creates a video on the channel"""
        pass

    def close_account(self):
        """Deletes account and all its channel
        TODO: Deletion CASCADE of EVERYTHING"""



class Channel:
    """TODO: Finish the whole class"""
    name = ""

    def __init__(self, name: str):
        """Initializes the channel"""
        self.name = name

    def channel_info(self):
        return {
                'name': "PIDARAS TV",
                'subscribers': 2,
                'videos': 0,
                'owner': 'RedBear',
                'avatar': 'empty.png',
                'description': "a channel about a beauiful people we are surrounded with"
            }


    def videos(self, num = 10, sort_by = "time", descending = False) -> dict:
        """
        Gets the dictionary of videos presented on this channel
            num - the amount of videos presented
            sort_by - the sorting value
            descending - if should be presented in the descending order
        """
        pass

    def change_info(self, new_info: dict):
        """ Changes the info of a channel"""
        pass

    def delete_channel(self):
        """Deletes channel with ALL ITS VIDEOS"""
        pass


class Video:
    id = ""
    channel = ""

    def __init__(self, id: str, channel: str):
        self.id = id
        self.channel = channel

    def get_info(self) -> dict:
        """Gets info of a video, for the video page.
        Dictionary should have all the video info PLUS the channel name, and avatar"""

    def change_info(self):
        """Change the video info"""

    def leave_comment(self, user: Accounts, comment: str, under_comment = ""):
        """Leaves a comment under the video, and under the comment if specified"""

    def get_commments(self) -> dict:
        """Gets comments of the video
        TODO: JOIN with accounts and comments AND video"""

    def delete_video(self):
        """Deletes a video and ALL ITS COMMENTS"""
        pass

def create_user(info: dict):
    """Creates an account if possible. If not possible return false"""
    pass


def create_channel(info: dict):
    """Creates a channel with the given login name. If not possible return false"""






