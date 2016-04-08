# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3)The name of the author may not be used to
#     endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Quick example.
"""

import json  # Imported for formatting

from etcdobj import EtcdObj, Server, fields


class Example(EtcdObj):
    """
    An example object with a few fields. Note that it must subclass EtcdObj.
    """

    __name__ = 'example'  # The parent key
    # Fields all take a name that will be used as their key
    anint = fields.IntField('anint')
    astr = fields.StrField('astr')
    adict = fields.DictField('adict')


# Data can be set via the constructor
e = Example(adict={'test': 'value', 'second': 'one'})
# Or set/updated via direct set
e.anint = '10'
e.astr = 200

# Render shows a list of the etcd key and the value
print("Original rendering of Example")
print(json.dumps(e.render(), indent=2))
# Output:
# [
#   {
#     "value": "value",
#     "dir": true,
#     "name": "adict",
#     "key": "/example/adict/test"
#   },
#   {
#     "value": "one",
#     "dir": true,
#     "name": "adict",
#     "key": "/example/adict/second"
#   },
#   {
#     "value": 10,
#     "dir": false,
#     "name": "anint",
#     "key": "/example/anint"
#   },
#   {
#     "value": "200",
#     "dir": false,
#     "name": "astr",
#     "key": "/example/astr"
#   }
# ]

# Saving to etcd
server = Server(etcd_kwargs={'port': 2379})
server.save(e)

# Retrieving from etcd
from_etcd = server.read(Example())
print("Result read back from etcd")
print(json.dumps(from_etcd.render(), indent=2))
# Output:
# [
#   {
#     "value": "value",
#     "dir": true,
#     "name": "adict",
#     "key": "/example/adict/test"
#   },
#   {
#     "value": "one",
#     "dir": true,
#     "name": "adict",
#     "key": "/example/adict/second"
#   },
#   {
#     "value": 10,
#     "dir": false,
#     "name": "anint",
#     "key": "/example/anint"
#   },
#   {
#     "value": "200",
#     "dir": false,
#     "name": "astr",
#     "key": "/example/astr"
#   }
# ]
