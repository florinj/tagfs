#
# Copyright 2011 Markus Pielmeier
#
# This file is part of tagfs.
#
# tagfs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tagfs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tagfs.  If not, see <http://www.gnu.org/licenses/>.
#

from cache import cache
from node import Stat, ItemLinkNode, DirectoryNode
from node_untagged_items import UntaggedItemsDirectoryNode
from node_export_csv import ExportCsvFileNode
from node_export_chart import ChartImageNode

class SumTransformation(object):

    def __init__(self):
        self.sum = 0.0

    def transform(self, y):
        self.sum += y

        return self.sum

class ExportDirectoryNode(DirectoryNode):

    def __init__(self, itemAccess, parentNode):
        self.itemAccess = itemAccess
        self.parentNode = parentNode

    @property
    def name(self):
        return '.export'

    @property
    def attr(self):
        s = super(ExportDirectoryNode, self).attr

        # TODO why nlink == 2?
        s.st_nlink = 2

        # TODO write test case which tests st_mtime == itemAccess.parseTime
        s.st_mtime = self.itemAccess.parseTime
        s.st_ctime = s.st_mtime
        s.st_atime = s.st_mtime

        return s

    @property
    def items(self):
        return self.parentNode.items
    
    @property
    def _entries(self):
        yield ExportCsvFileNode(self.itemAccess, self.parentNode)

        for context in self.parentNode.contexts:
            yield ChartImageNode(self.itemAccess, self.parentNode, context, 'value', lambda y: y)
            yield ChartImageNode(self.itemAccess, self.parentNode, context, 'sum', SumTransformation().transform)
