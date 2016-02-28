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
All fields.
"""


class Field(object):

    def __init__(self, name):
        self.name = name
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._set_value(value)

    def _set_value(self, value):
        self._value = value

    def render(self):
        return {'key': self.name, 'value': self._value}


class _CastField(Field):
    _caster = None

    def _set_value(self, value):
        self._value = self._caster(value)


class IntField(_CastField):
    _caster = int


class StrField(_CastField):
    _caster = str


class UnicodeField(_CastField):
    _caster = unicode


class DictField(Field):

    def _set_value(self, value):
        if type(value) != dict:
            raise TypeError('Must use dict')
        super(DictField, self)._set_value(value)

    def render(self):
        rendered = []
        for x in self._value.keys():
            rendered.append({
                'key': '{0}/{1}'.format(self.name, x),
                'value': self._value[x]})
        return rendered
