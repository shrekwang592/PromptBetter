from abc import ABCMeta, abstractmethod
from enum import Enum
import time

class UserService(object):
    def __init__(self):
        self.users_by_id = {}    

    def add_user(self, user_id, name, pass_hash):
        if user_id in self.users_by_id:
            raise ValueError("User already exists.")
        self.users_by_id[user_id] = User(user_id, name, pass_hash)
    
    def remove_user(self, user_id):
        if user_id in self.users_by_id:
            del self.users_by_id[user_id]
        else:
            raise ValueError("User not found.")
    
    def add_friend_request(self, from_user_id, to_user_id):
        if from_user_id not in self.users_by_id or to_user_id not in self.users_by_id:
            raise ValueError("One of the users does not exist.")
        from_user = self.users_by_id[from_user_id]
        to_user = self.users_by_id[to_user_id]
        from_user.send_friend_request(to_user.user_id)
        to_user.receive_friend_request(from_user.user_id)
    
    def approve_friend_request(self, from_user_id, to_user_id):
        from_user = self.users_by_id[from_user_id]
        to_user = self.users_by_id[to_user_id]
        from_user.approve_friend_request(to_user.user_id)
    
    def reject_friend_request(self, from_user_id, to_user_id):
        from_user = self.users_by_id[from_user_id]
        to_user = self.users_by_id[to_user_id]
        from_user.reject_friend_request(to_user.user_id)

class User(object):
    def __init__(self, user_id, name, pass_hash):
        self.user_id = user_id
        self.name = name
        self.pass_hash = pass_hash
        self.friends_by_id = {}  # key: friend id, value: User
        self.friend_ids_to_private_chats = {}  # key: friend id, value: private chats
        self.group_chats_by_id = {}  # key: chat id, value: GroupChat
        self.received_friend_requests_by_friend_id = {}  # key: friend id, value: AddRequest
        self.sent_friend_requests_by_friend_id = {}  # key: friend id, value: AddRequest

    def send_friend_request(self, friend_id):
        if friend_id in self.friends_by_id:
            return "Already friends"
        if friend_id in self.sent_friend_requests_by_friend_id:
            return "Friend request already sent"
        add_request = AddRequest(self.user_id, friend_id, RequestStatus.UNREAD, time.time())
        self.sent_friend_requests_by_friend_id[friend_id] = add_request
        
    def receive_friend_request(self, friend_id):
        add_request = AddRequest(friend_id, self.user_id, RequestStatus.UNREAD, time.time())
        self.received_friend_requests_by_friend_id[friend_id] = add_request
    
    def message_user(self, friend_id, message):
        if friend_id not in self.friends_by_id:
            raise ValueError("Can only message friends.")
        chat = PrivateChat(self.user_id, friend_id)
        chat.messages.append(Message(None, message, time.time()))  # Assuming None for message_id

    def message_group(self, group_id, message):
        if group_id not in self.group_chats_by_id:
            raise ValueError("Group Chat not found.")
        chat = self.group_chats_by_id[group_id]
        chat.messages.append(Message(None, message, time.time()))  # Assuming None for message_id

    def approve_friend_request(self, friend_id):
        if friend_id not in self.received_friend_requests_by_friend_id:
            raise ValueError("No friend request found.")
        request = self.received_friend_requests_by_friend_id[friend_id]
        if request.request_status == RequestStatus.ACCEPTED:
            return
        request.request_status = RequestStatus.ACCEPTED
        friend = self.friends_by_id[request.from_user_id]
        self.friends_by_id[friend_id] = friend
        friend.friends_by_id[self.user_id] = self

    def reject_friend_request(self, friend_id):
        if friend_id not in self.received_friend_requests_by_friend_id:
            raise ValueError("No friend request found.")
        request = self.received_friend_requests_by_friend_id[friend_id]
        request.request_status = RequestStatus.REJECTED

# Assuming the abstract method here to demonstrate additional functionality
class Chat(metaclass=ABCMeta):
    def __init__(self, first_user, second_user):
        super(PrivateChat, self).__init__()
        self.users.append(first_user)
        self.users.append(second_user)

    @abstractmethod
    def post_message(self, user, message_text):
        pass  # define in subclasses

class PrivateChat(Chat):
    def __init__(self, first_user, second_user):
        super(PrivateChat, self).__init__()
        self.users.append(first_user)
        self.users.append(second_user)

    def post_message(self, user, message_text):
        if user not in self.users:
            raise ValueError("User not in the chat.")
        self.messages.append(Message(None, message_text, time.time()))
        
class GroupChat(Chat):
    def __init__(self, chat_id):
        super(GroupChat, self).__init__(chat_id)
        self.users = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)  # Add the user to the chat if they're not already in it
        else:
            print(f"{user.name} is already a part of this chat.")
        
    def remove_user(self, user):  
        if user in self.users:
            self.users.remove(user)  # Remove the user from the chat if they're in it
        else:
            print(f"{user.name} is not a part of this chat.")
            
    def post_message(self, user, message_text):
        if user not in self.users:
            raise ValueError("User not in the chat.")
        self.messages.append(Message(None, message_text, time.time()))
        
# Assuming 'PrivateChat' and 'GroupChat' will directly use the post_message method to add messages

from enum import Enum

class RequestStatus(Enum):
    UNREAD = 0
    READ = 1
    ACCEPTED = 2
    REJECTED = 3

class Message(object):
    def __init__(self, message_id, message, timestamp):
        self.message_id = message_id
        self.message = message
        self.timestamp = timestamp

class AddRequest(object):
    def __init__(self, from_user_id, to_user_id, request_status, timestamp):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.request_status = request_status
        self.timestamp = timestamp