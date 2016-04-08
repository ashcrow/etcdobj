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
Unittests for the main etcdobj module.
"""

from mock import MagicMock

from . import TestCase, TestingObj

import etcdobj


class Test_Server(TestCase):
    """
    Tests for _Server
    """

    def test_creation_and_verify_client(self):
        """
        Verify _verify_client works as expected.
        """
        # Validate the client must have the proper methods
        self.assertRaises(ValueError, etcdobj._Server, dict())

        # No error when the proper methods are available
        server = etcdobj._Server(self.client)
        self.assertEquals(self.client, server.client)

    def test_save(self):
        """
        Verify save works as expected.
        """
        server = etcdobj._Server(self.client)
        server.save(self.testing_obj)
        # We should have one write
        self.client.write.assert_called_once_with('/testing/anint', 10)

    def test_read(self):
        """
        Verify read works as expected.
        """
        server = etcdobj._Server(self.client)
        self.client.read.return_value = MagicMock(value="10")

        # Create the object with different data
        to = server.read(TestingObj(anint=1))
        # We should have one read
        self.client.read.assert_called_once_with('/testing/anint')
        # And it should have set the data to 10
        self.assertEquals(10, to.anint)
