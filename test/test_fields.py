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
Unittests for fields.
"""

from mock import MagicMock

from . import TestCase, TestingObj

from etcdobj import fields


class TestField(TestCase):
    """
    Tests for base Field class.
    """

    def setUp(self):
        """
        Executes before each test.
        """
        self.instance = fields.Field('test')

    def test_creation(self):
        """
        Verify creation of instance works as expected.
        """
        self.assertEquals('test', self.instance.name)
        self.assertEquals(None, self.instance.value)

    def test_value_setting(self):
        """
        Verify updating the value works.
        """
        self.assertEquals(None, self.instance.value)
        self.instance.value = 'change'
        self.assertEquals('change', self.instance.value)

    def test_rendering(self):
        """
        Verify rendering of the field works.
        """
        self.instance.value = 'change'
        rendered = self.instance.render()
        expected = {
            'name': 'test',
            'key': 'test',
            'value': 'change',
            'dir': False,
        }
        self.assertEquals(expected, rendered)


class TestIntField(TestCase):
    """
    Tests for IntField.
    """

    def setUp(self):
        """
        Executes before each test.
        """
        self.instance = fields.IntField('test')

    def test_casting(self):
        """
        Verify IntField casts properly.
        """
        self.instance.value = '10'
        self.assertEquals(10, self.instance.value)

        self.assertRaises(
            ValueError,
            self.instance._set_value,
            'error',
        )


class TestStrField(TestCase):
    """
    Tests for StrField.
    """

    def setUp(self):
        """
        Executes before each test.
        """
        self.instance = fields.StrField('test')

    def test_casting(self):
        """
        Verify StrField casts properly.
        """
        self.instance.value = 10
        self.assertEquals('10', self.instance.value)


class TestDictField(TestCase):
    """
    Tests for DictField.
    """

    def setUp(self):
        """
        Executes before each test.
        """
        self.instance = fields.DictField('test', {'a': int, 'b': str})

    def test_casting(self):
        """
        Verify StrField casts properly.
        """
        # We must have a dict
        self.assertRaises(
            TypeError,
            self.instance.value,
            "error"
        )

        # Test internal casting when a caster is provided
        self.instance.value = {'a': '10', 'b': 10}
        self.assertEquals({'a': 10, 'b': '10'}, self.instance.value)
