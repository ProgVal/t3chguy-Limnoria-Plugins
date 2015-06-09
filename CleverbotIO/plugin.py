###
# Copyright (c) 2015, Michael Daniel Telatynski <postmaster@webdevguru.co.uk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import requests
from supybot.commands import *
import supybot.utils as utils
import supybot.plugins as plugins
import supybot.callbacks as callbacks

import re

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('CleverbotIO')
except ImportError:
    _ = lambda x: x


class CleverbotIO(callbacks.Plugin):
    """CleverbotIO API Interface"""
    threaded = True
    public = True
    botNick = False

    def __init__(self, irc):
        self.__parent = super(CleverbotIO, self)
        self.__parent.__init__(irc)
        conf.supybot.plugins.CleverbotIO.botName.addCallback(self._configCallback)
        conf.supybot.plugins.CleverbotIO.appUser.addCallback(self._configCallback)
        conf.supybot.plugins.CleverbotIO.appKey.addCallback(self._configCallback)
        self._createBot()

    def _configCallback(self, name=None):
        self.log.info('one of the configs changed (%s)' % name)

    _createUrl = 'https://cleverbot.io/1.0/create'
    def _createBot(self):
        payload = {
            'user': self.registryValue('appUser'),
            'key': self.registryValue('appKey'),
            'nick': self.registryValue('botName')
        }
        r = requests.post(self._createUrl, data=payload)
        j = r.json()
        if j.status == 'success':
            self.botNick = j.nick
        print(j.status)

    _queryUrl = 'https://cleverbot.io/1.0/ask'
    def _queryBot(self, query):
        payload = {
            'user': self.registryValue('appUser'),
            'key': self.registryValue('appKey'),
            'nick': self.botNick,
            'text': query
        }
        r = requests.post(self._queryUrl, data=payload)
        j = r.json()
        if j.status == 'success':
            print(j.response)


    def cleverbotio(self, irc, msg, args, text):
        """Manual Call to the Cleverbot.io API"""
        print(text)

    cleverbotio = wrap(cleverbotio, ['text'])

Class = CleverbotIO


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
