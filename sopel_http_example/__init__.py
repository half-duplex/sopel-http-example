"""sopel-http-example

https://github.com/half-duplex/sopel-http-example
Released under the EUPL-1.2
"""

from __future__ import annotations

from os import path

from flask import abort, Blueprint, render_template, request, url_for
from markupsafe import escape
import sopel_http

module_dir = path.dirname(__file__)
app = Blueprint(
    "example",
    __name__,
    static_folder=path.join(module_dir, "static"),
    static_url_path="/static/example",
    template_folder=path.join(module_dir, "templates"),
)
bot = None


def setup(newbot):
    global bot
    bot = newbot
    sopel_http.app.register_blueprint(app)


@app.route("/")
def hello():
    message = "Hello!\n"
    message += "I am in the following channels:\n"
    for channel in bot.channels.keys():
        message += """<a href="{channel_link}">{channel}</a>\n""".format(
            channel_link=url_for("example.channel", channel=channel),
            channel=escape(channel),
        )
    return message.replace("\n", "<br>\n")


# See https://github.com/half-duplex/sopel-http/issues/1
hello._sopel_callable = False


@app.route("/channel/<channel>")
def channel(channel):
    if channel not in bot.channels:
        abort(404)
    return render_template(
        "channel.j2",
        channel=channel,
        users=bot.channels[channel].privileges.keys(),
    )


channel._sopel_callable = False


@app.route("/channel/<channel>", methods=["POST"])
def channel_post(channel):
    if channel not in bot.channels:
        abort(404)
    if "user" not in request.form:
        abort(400, "User not specified")
    user = request.form["user"]
    if request.form["user"] not in bot.channels[channel].privileges:
        abort(400, "User not specified")
    bot.say("A web user says hello, " + user + "!", channel)
    return "Sent!"


channel_post._sopel_callable = False
