#    karmabot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    karmabot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with karmabot.  If not, see <http://www.gnu.org/licenses/>.


from twisted.words.protocols.irc import IRCClient
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet import reactor

class karmabot(IRCClient):
    bot_name = "karmabot"
    channel = "#qalthos-test"
    versionNum = 1
    sourceURL = "http://gitorious.com/~jlew"
    lineRate = 1

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)
        self.factory.add_bot(self)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        print "Joined %s" % channel

    def left(self, channel):
        """This will get called when the bot leaves the channel."""
        print "Left %s" % channel

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            return

        # Message said in channel to the bot
        elif msg.startswith(user + '--'):
            self.msg(channel, "{}--".format(user))

        elif msg.startswith(user + '++'):
            import random
            adjective = random.choice(['stuck up', 'arrogant', 'pompous',
                                       'self important', 'conceited'])
            self.msg(channel, "{}: don't be {}...".format(user, adjective))

        elif msg.startswith(self.nickname):
            msg = msg.split(' ', 2)
            if len(msg) > 1 and msg[1] == 'help':
                self.msg(channel, '{}: {} is not here to help.'.format(user, self.nickname))


class karmabotFactory(ReconnectingClientFactory):
    active_bot = None

    def __init__(self, protocol=karmabot):
        self.protocol = protocol
        self.channel = protocol.channel
        IRCClient.nickname = protocol.bot_name
        IRCClient.realname = protocol.bot_name

    def add_bot(self, bot):
        self.active_bot = bot


if __name__ == '__main__':
    # create factory protocol and application
    f = karmabotFactory()

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
