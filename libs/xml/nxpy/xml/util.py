# nxpy_xml --------------------------------------------------------------------

# Copyright Nicola Musatti 2017 - 2019
# Use, modification, and distribution are subject to the Boost Software
# License, Version 1.0. (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# See https://github.com/nmusatti/nxpy/tree/master/libs/xml. ------------------

r"""
XML utility classes and functions.

Requires at least Python 2.6. Simple import breaks on Python 2.5

"""
from __future__ import absolute_import

import nxpy.core.past

if nxpy.core.past.V_3_3.at_least():
    from collections.abc import MutableMapping, MutableSequence
else:
    from collections import MutableMapping, MutableSequence

import codecs
import re

import lxml.etree

import six

import nxpy.core.error

nxpy.core.past.enforce_at_least(nxpy.core.past.V_2_6)


def parse(src):
    r"""parse the 'src' XML file and return a DOM."""
    
    parser = lxml.etree.XMLParser(strip_cdata=False)
    tree = lxml.etree.parse(src, parser)
    return tree


def make_property(elem, key=None):
    r"""
    Create a property on the text of element 'elem' or, if the 'key' argument is given, on its
    'key' attribute.
    
    """
    if key:
        def _get(self):
            return getattr(self, elem).get(key)
        def _set(self, value):
            getattr(self, elem).set(key, value)
            self._modified = True
        return property(_get, _set)
    else:
        def _get(self):
            return getattr(self, elem).text
        def _set(self, value):
            getattr(self, elem).text = value
            self._modified = True
        return property(_get, _set)


class QName(object):
    r"""Represent a qualified name"""

    _re = re.compile(r"\{(.*)\}(.*)")
    
    def __init__(self, tag):
        m = QName._re.match(tag)
        self.url = m.group(1)
        self.tag = m.group(2)

    @property
    def text(self):
        t = []
        if len(self.url) != 0:
            t.append("{{{0}}}".format(self.url))
        t.append(self.tag)
        return "".join(t)

    def __str__(self):
        return self.text()


class Namespace(object):
    r"""
    Represent an XML namespace and provide several utility functions that help handle a
    document without namespace tags.
    
    """
    def __init__(self, url="", element=None):
        if len(url) > 0 and element is not None:
            raise nxpy.core.error.ArgumentError(
                    "Only one between url and element should be specified")
        if element is not None:
            url = QName(element.tag).url
        self.url = url
        self.nspace = "{" + url + "}" if len(url) != 0 else ""

    def find(self, element, tag):
        return element.find(self.nspace + tag)

    def findall(self, element, tag):
        return element.findall(self.nspace + tag)

    def findtext(self, element, tag, default=None):
        return element.findtext(self.nspace + tag, default)

    def get_tag(self, element):
        return element.tag[len(self.nspace):]

    def Element(self, tag, attrib={}, **extra):
        return lxml.etree.Element(self.nspace + tag, attrib, **extra)
    
    def SubElement(self, parent, tag, attrib={}, **extra):
        return lxml.etree.SubElement(parent, self.nspace + tag, attrib, **extra)


class ContainerElementMixin(Namespace):
    r"""
    Mixin class for container workalikes backed by a DOM.
    
    """
    def __init__(self, parent, root_tag, namespace=""):
        super(ContainerElementMixin, self).__init__(namespace)
        self.parent = parent
        self.root_tag = root_tag
        self.root = self.find(self.parent, self.root_tag)
        self.modified = False

    def __len__(self):
        return len(self.root) if self.root is not None else 0


class MappingElementIterator(six.Iterator):
    r"""
    Iterator over a 'MappingElement'.

    """
    def __init__(self, element):
        self.element = element
        self.iter = iter(element.root.getchildren())

    def __next__(self):
        return self.element.get_tag(six.advance_iterator(self.iter))


class MappingElement(ContainerElementMixin, MutableMapping):
    r"""
    Provide a tag/text map for the children of the 'root_tag' descendent of 'parent'. Given:

    .. code-block:: xml

        <parent>
            <root_tag>
                <key1>value1</key1>
                <key2>value2</key2>
            </root_tag>
        </parent>

    One could write::

        mappingElement["key1"] == "value1"
    
    """
    def __init__(self, parent, root_tag, namespace=""):
        ContainerElementMixin.__init__(self, parent, root_tag, namespace)

    def __getitem__(self, key):
        if self.root is None:
            raise KeyError()
        elem = self.find(self.root, key)
        if elem is None:
            raise KeyError()
        return elem.text

    def __setitem__(self, key, value):
        if self.root is None:
            self.root = self.SubElement(self.parent, self.root_tag)
        elem = self.find(self.root, key)
        if elem is None:
            elem = self.SubElement(self.root, key)
        self.modified = True
        elem.text = value

    def __delitem__(self, key):
        if self.root is None:
            raise KeyError()
        elem = self.find(self.root, key)
        if elem is None:
            raise KeyError()
        self.modified = True
        self.root.remove(elem)

    def __iter__(self):
        return MappingElementIterator(self)


class SequenceElement(ContainerElementMixin, MutableSequence):
    r"""
    Provide a sequence of the values of the children tagged 'element_tag' of the 'root_tag' 
    descendent of 'parent'. Given:

    .. code-block:: xml

        <parent>
            <root_tag>
                <tag>value1</tag>
                <tag>value2</tag>
            </root_tag>
        </parent>

    One could write::

        sequenceElement[1] == "value2"
    
    """
    def __init__(self, parent, root_tag, element_tag, namespace="", indent="    "):
        ContainerElementMixin.__init__(self, parent, root_tag, namespace)
        self.element_tag = element_tag
        self.indent = indent
        self.elements = []
        i = 0
        if self.root is not None:
            for e in self.root:
                if e.tag is not lxml.etree.Comment and self.get_tag(e) == self.element_tag:
                    self.elements.append([i, e])
                i += 1

    def __len__(self):
        return len(self.elements) if self.elements is not None else 0

    def __getitem__(self, index):
        if self.root is None:
            raise IndexError()
        return self.elements[index][1].text

    def __setitem__(self, index, value):
        if self.root is None:
            if index != 0:
                raise IndexError()
            self.root = self.SubElement(self.parent, self.root_tag)
        elif index > len(self.root):
            raise IndexError()
        elem = None
        try:
            elem = self.elements[index][1]
        except IndexError:
            elem = self.SubElement(self.root, self.element_tag)
            self.elements.append([len(self.root) - 1, elem])
        elem.text = value
        self.modified = True

    def __delitem__(self, index):
        if self.root is None:
            raise IndexError()
        del self.root[self.elements[index][0]]
        del self.elements[index]
        for i in range(index, len(self.elements)):
            self.elements[i][0] -= 1
        self.modified = True

    def insert(self, index, value):
        if index > len(self.elements):
            raise IndexError()
        if self.root is None:
            self.root = self.SubElement(self.parent, self.root_tag)
        elem = self.Element(self.element_tag)
        elem.text = value
        elem.tail = self.root.tail + self.indent
        if index == len(self.elements):
            self.root.append(elem)
            self.elements.append([len(self.root) - 1, elem])
        else:
            self.root.insert(self.elements[index][0], elem)
            self.elements.insert(index, [self.elements[index][0], elem])
            for i in range(index + 1, len(self.elements)):
                self.elements[i][0] -= 1
        self.modified = True


class Writer(object):
    r"""
    Pretty-print an XML tree.
 
    """
    _name_re = re.compile(r"<([^\s]+)")
    _tag_re = re.compile(r"(</?)[^:]+:((:?[^>]+>)|(:?[^/]+/>))")
    _empty_re = re.compile(r"<([^/^>^ ]*)\s*/>")

    def __init__(self, root_tag, attributes=None, tab_size=0):
        self.root_tag = root_tag
        self.tab_size = tab_size
        self.attributes = attributes
        self.name = self._name_re.search(self.root_tag).group(1)
        self._root_re = re.compile(r"(<" + self.name + r"[^>]+>)")

    def marshal(self, node):
        s = None
        if nxpy.core.past.V_2_7.at_most():
                s = lxml.etree.tostring(node)
        else:
                s = lxml.etree.tostring(node, encoding="unicode")
        s = self._root_re.sub(self.root_tag, s, 1)
        s = self._empty_re.sub(r"<\1 />", s)
        if self.tab_size > 0:
            s = s.replace("\t", " " * self.tab_size)
        if self.attributes is not None:
            d = ( '<?xml version="' + self.attributes.get("version", "1.0") + 
                    '" encoding="' + self.attributes.get("encoding", "UTF-8") + '"')
            if "standalone" in self.attributes:
                d += ' standalone="' + self.attributes["standalone"] + '"'
            d += "?>\n"
            s = d + s
        return s + "\n\n"

    def write(self, node, where):
        f = open(where, "w+") if isinstance(where, six.string_types) else where
        try:
            f.write(self.marshal(node))
        finally:
            f.close()


class PreservingWriter(object):
    r"""
    Write an XML tree back to the file it was parsed from, keeping that file's formatting.

    *src* is the path of the original file. lxml keeps text, comments and indentation within the
    root element, but loses what lies outside it and a few lexical details; this class restores
    the XML declaration and anything else that precedes the root element, the original root start
    tag (as long as its attributes and namespaces are unchanged), whatever follows the root
    element, the line terminators, the encoding and the empty element style (``<a/>`` vs.
    ``<a />``).

    """
    _prolog_re = re.compile(r"(?:\s+|<\?.*?\?>|<!--.*?-->|<!DOCTYPE[^\[>]*(?:\[.*?\])?\s*>)",
            re.DOTALL)
    _start_tag_re = re.compile(r"""<([^\s/>]+)(?:\s+[^\s=]+\s*=\s*(?:"[^"]*"|'[^']*'))*\s*(/?)>""")
    _encoding_re = re.compile(r"""^<\?xml[^>]*encoding\s*=\s*["']([^"']+)["']""")
    _markup_re = re.compile(r"<!--.*?-->|<!\[CDATA\[.*?\]\]>|<\?.*?\?>|<[^<>]*?(\s*)/>", 
            re.DOTALL)

    def __init__(self, src):
        with open(src, "rb") as f:
            data = f.read()
        self.bom = data.startswith(codecs.BOM_UTF8)
        if self.bom:
            data = data[len(codecs.BOM_UTF8):]
        m = self._encoding_re.match(data.decode("ascii", "replace"))
        self.encoding = m.group(1) if m else "UTF-8"
        text = data.decode(self.encoding)
        self.newline = "\r\n" if "\r\n" in text else "\n"
        text = text.replace("\r\n", "\n")
        pos = 0
        m = self._prolog_re.match(text, pos)
        while m:
            pos = m.end()
            m = self._prolog_re.match(text, pos)
        m = self._start_tag_re.match(text, pos)
        if m is None:
            raise nxpy.core.error.ArgumentError(src + ": root element not found")
        self.prolog = text[:pos]
        self.start_tag = m.group(0)
        if m.group(2):
            self.epilog = text[m.end():]
        else:
            end_tags = list(re.finditer(r"</" + re.escape(m.group(1)) + r"\s*>", text))
            self.epilog = text[end_tags[-1].end():] if end_tags else ""
        spaced = 0
        unspaced = 0
        for e in self._markup_re.finditer(text):
            if e.group(1) is not None:
                if e.group(1):
                    spaced += 1
                else:
                    unspaced += 1
        self.spaced_empty = spaced > unspaced

    def _same_start_tag(self, node):
        tag = self.start_tag
        if not tag.endswith("/>"):
            tag += "</" + self._start_tag_re.match(tag).group(1) + ">"
        orig = lxml.etree.fromstring(tag)
        return ( orig.tag == node.tag and dict(orig.attrib) == dict(node.attrib) and
                 orig.nsmap == node.nsmap )

    def _space_empty(self, m):
        s = m.group(0)
        if m.group(1) is not None and not m.group(1):
            s = s[:-2] + " />"
        return s

    def marshal(self, node):
        s = lxml.etree.tostring(node, encoding=six.text_type, with_tail=False)
        if self._same_start_tag(node):
            s = self._start_tag_re.sub(lambda m: self.start_tag, s, 1)
        if self.spaced_empty:
            s = self._markup_re.sub(self._space_empty, s)
        return self.prolog + s + self.epilog

    def write(self, node, where):
        r"""
        Write *node* to *where*, a path or a file object. Paths and binary files receive the
        original encoding and line terminators; text files receive text with ``\n`` line
        terminators, which their own encoding and newline translation then apply to.

        """
        s = self.marshal(node)
        if isinstance(where, six.string_types):
            f = open(where, "wb")
        else:
            f = where
        try:
            if isinstance(where, six.string_types) or "b" in getattr(f, "mode", ""):
                if self.newline != "\n":
                    s = s.replace("\n", self.newline)
                data = s.encode(self.encoding, "xmlcharrefreplace")
                if self.bom:
                    data = codecs.BOM_UTF8 + data
                f.write(data)
            else:
                f.write(s)
        finally:
            f.close()
