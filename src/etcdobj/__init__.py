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
A simplistic etcd orm.
"""

from etcdobj.fields import Field


__version__ = '0.0.0'


class EtcdObj(object):

    _fields = []

    def __new__(cls, **kwargs):
        cls = super(EtcdObj, cls).__new__(cls, **kwargs)
        for key in dir(cls):
            if not key.startswith('_'):
                attr = getattr(cls, key)
                if issubclass(attr.__class__, Field):
                    cls._fields.append(key)
                    if key in kwargs.keys():
                        attr.value = kwargs[key]
        return cls

    def __init__(self, **kwargs):
        """
        Creates a new instance. Required for __new__.
        """
        pass

    def __setattr__(self, name, value):
        """
        Overridden setattr to catch fields or pass along if not a field.

        :param name: The name of the field.
        :type name: str
        :param value: The value to set on name.
        :type value: any
        """
        attr = object.__getattribute__(self, name)
        if name in self._fields:
            attr.value = value
        else:
            object.__setattr__(self, name, value)

    def __getattribute__(self, name):
        """
        Overridden  getattribute to catch fields or pass along if not a field.

        :param name: The name of the field.
        :type name: str
        :returns: The value of the field or attribute
        :rtype: any
        :raises: AttributeError
        """
        if name in object.__getattribute__(self, '_fields'):
            return object.__getattribute__(self, name).value
        else:
            return object.__getattribute__(self, name)

    def render(self):
        """
        Renders the instance into a structure for settings in etcd.

        :returns: The structure to use for setting.
        :rtype: list(dict{key=str,value=any})
        """
        rendered = []
        for x in self._fields:
            items = object.__getattribute__(self, x).render()
            if type(items) != list:
                items = [items]
            for i in items:
                i['key'] = '/{0}/{1}'.format(self.__name__, i['key'])
                rendered.append(i)
        return rendered
