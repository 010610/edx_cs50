# -*- coding: UTF-8 -*-

import os
import datetime
import urllib.parse
from flask import Flask, flash, render_template, redirect, session, request, url_for, jsonify
from flask_socketio import SocketIO, emit
from jinja2 import Markup
import logging


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)


users = dict()
channels = dict()


@app.route("/")
def index():
    if session.get("act_user") is None:
        return redirect(url_for("login"))
    else:
        return get_channels()
    # return render_template(
    #     "channels.html", act_user=session.get("act_user"), channels=channels.keys())


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return get_channels()
    elif request.method == "POST":
        usernm = request.form.get("displayName")
        if usernm not in users.keys():
            flash(Markup(
                """<i class='fa fa-2x fa-info-circle'></i>
                New username %s created.""" % (usernm)), 'info')
            users[usernm] = None

        session['act_user'] = usernm
        # return render_template(
        #     "channels.html", act_user=session.get("act_user"), channels=channels)
        return(redirect(url_for("get_channels")))


@app.route("/logout")
def logout():
    session.pop('act_user', None)
    flash(Markup(
        """<i class='fa fa-2x fa-check-square-o'></i>
        You have logged out."""), 'success')
    return redirect(url_for("index"))


@app.route("/channels", methods=['GET'])
def get_channels():
    last_visit=users.get(session.get("act_user"))
    if last_visit not in channels.keys():
        last_visit = None
    return render_template(
        "channels.html", act_user=session.get("act_user"), 
        channels=[{'name':k, 'created':channels[k]['created']} for k in channels], 
        last_visit=last_visit)


@app.route("/channels", methods=['POST'])
def set_channels():
    new_channel = request.form.get("new_channel")
    if new_channel is not None:
        if new_channel in channels.keys():
            flash(Markup(
                """<i class='fa fa-2x fa-warning'></i>
                Channel %s already exists.""" % (new_channel)), 
                'warning')
        else:
            flash(Markup(
                """<i class='fa fa-2x fa-check-square-o'></i>
                The new channel %s has been created.""" % (new_channel)),
                'success')
            channels[new_channel] = {"created": datetime.datetime.now(), "chats":[]}
        return redirect(url_for("get_channels"))
    else:
        pass


@app.route("/channel/<channel>", methods=['GET'])
def get_channel(channel):
    if session.get('act_user') is None:
        flash(Markup(
            """<i class='fa fa-2x fa-exclamation-circle'></i>
            You are not logged in."""), 'danger')
        return redirect(url_for("index"))
    
    users[session.get('act_user')] = channel
    return render_template(
        "channel.html", act_user=session.get("act_user"), channel=channel,
        chats=channels[channel]['chats'])


@socketio.on("connect")
def send_username():
    emit('send username', {'act_user': session.get('act_user'), 
         'act_channel': users.get(session.get('act_user'))})


@socketio.on("send msg")
def emit_msg(data):
    if data['msg'] != '':
        channel = data['channel']
        chats = channels[channel]['chats']
        chats.append([data['user'], data['time'], data['msg']])
        if len(chats) > 100:
            chats = chats[(len(chats)-100):]
        channels[channel]['chats'] = chats
        # with open('C:/users/a303821/desktop/out.txt') as f:
        #     f.write(' + '.join([str(e) for e in chats]))
        emit('emit msg', 
             {'user': data['user'], 'time': data['time'], 'msg': data['msg']},
             broadcast=True)


@socketio.on("del msg")
def del_msg(data):
    channel = urllib.parse.unquote(data['channel'])
    chats = channels[channel]['chats']
    app.logger.info(str(chats))
    for i in range(len(chats)):
        app.logger.info([data['user'], data['time']])
        if chats[i][0] == data['user'] and chats[i][1] == data['time']:
            channels[channel]['chats'].pop(i)
            break
    


if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler("flask.log", encoding="UTF-8")
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    socketio.run(app)
