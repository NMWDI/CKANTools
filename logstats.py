# ===============================================================================
# Copyright 2020 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import gzip
import os
import re
from collections import Counter

SEARCH = re.compile(r'GET \/dataset\?q=(?P<term>[^&\ ]+)')
DOWNLOAD = re.compile('download')


def sextract(collection, m, l):
    collection[m.group('term').replace('+', ' ')] += 1


def dextract(collection, m, l):
    pass


def report(collection):
    report_(collection['search'], 'Search Terms')
    print
    report_(collection['download'], 'Downloads')


def report_(collection, title):
    print title
    print '======================================='
    for k, v in collection.most_common():
        print '{:<40s}: {}'.format(k, v)


def analyze(collection, l):
    for r, tag, extract, collection in ((SEARCH, 'search', sextract, collection['search']),
                                        (DOWNLOAD, 'download', dextract, collection['download'])):
        m = r.search(l)

        if m:
            return extract(collection, m, l)


def main():
    root = '/var/log/apache2/'
    paths = ['ckan_default.custom.log',
             'ckan_default.custom.log.1',
             ]
    paths += ['ckan_default.custom.log.{}.gz'.format(i+1) for i in range(20)]

    collection = {'search': Counter(), 'download': Counter()}
    for path in paths:
        path = os.path.join(root, path)
        if os.path.isfile(path):
            print 'checking {}'.format(path)

            if path.endswith('.gz'):
                opener = gzip.open
            else:
                opener = open

            with opener(path, 'r') as rfile:
                for line in rfile:
                    analyze(collection, line.strip())

    report(collection)


if __name__ == '__main__':
    main()
# ============= EOF =============================================
