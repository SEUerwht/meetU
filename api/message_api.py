from flask import Blueprint, request, redirect
from model.User import User
from util.Response import response
from util.operate_token import operate_token
import util.config as config
from util.redis import redis_db
from model.BaseModel import db

message_bp = Blueprint("message_bp", __name__, url_prefix='/message')


@message_bp.route('/send_message')
def send_message():
    pass


@message_bp.route('/get_sender_message')
def get_sender_message():
    pass


@message_bp.route('/get_receiver_message')
def get_receiver_message():
    pass
