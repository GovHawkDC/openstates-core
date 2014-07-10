#!/usr/bin/env python
import os
import re
import csv

PWD = os.path.abspath(os.path.dirname(__file__))
OCD_DIVISION_CSV = os.path.join(PWD, 'division-ids/identifiers/country-{}.csv')


class Division(object):
    _cache = {}

    @classmethod
    def get(self, division, from_csv=None):
        if division not in self._cache:
            # figure out the source
            if not from_csv:
                country = re.findall(r'country:(\w{2})', division)[0]
                from_csv = OCD_DIVISION_CSV.format(country)

            # load division and all children
            for row in csv.DictReader(open(from_csv)):
                if row['id'].startswith(division):
                    same_as = row.pop('sameAs', None)
                    if same_as:
                        #divisions[same_as].names.append(row['id'])
                        continue
                    #same_as_note = row.pop('sameAsNote', None)
                    Division(**row)

        return self._cache[division]

    def __init__(self, id, name, **kwargs):
        self._cache[id] = self
        self.id = id
        self.name = name
        valid_through = kwargs.pop('validThrough', None)
        if valid_through:
            self.valid_through = valid_through

        # set parent and _type
        parent, own_id = id.rsplit('/', 1)
        if parent == 'ocd-division':
            self.parent = None
        else:
            self.parent = self._cache.get(parent)
            if self.parent:
                self.parent._children.append(self)
            else:
                # TODO: keep a list of unassigned parents for later reconciliation
                pass

        self._type = own_id.split(':')[0]

        # other attrs
        self.attrs = kwargs
        self.names = []
        self._children = []

    def children(self, _type=None):
        for d in self._children:
            if not _type or d._type == _type:
                yield d

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)