# Copyright 2016 Yanis Guenane <yguenane@redhat.com>
# Author: Yanis Guenane <yguenane@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dci import stores
from dci.common import exceptions
from dci.stores import files_utils

import os
import errno


class FileSystem(stores.Store):

    def __init__(self, conf):
        self.path = conf['path']
        self.container = conf['container']

    def delete(self, filename):
        try:
            os.remove(os.path.join(self.path, self.container, filename))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise exceptions.StoreExceptions('An error occured while '
                                                 'deleting %s\n with error %s'
                                                 % (filename, str(e)))

    def get(self, filename):
        file_path = os.path.join(self.path, self.container, filename)
        try:
            return ([], open(file_path, 'r'))
        except IOError as e:
            raise exceptions.StoreExceptions('An error occured while '
                                             'accessing %s\n with error %s'
                                             % (filename, str(e)))

    def head(self, filename):
        file_path = os.path.join(self.path, self.container, filename)
        file_size = os.path.getsize(file_path)
        md5 = files_utils.md5Checksum(file_path)
        return {'content-length': file_size, 'etag': md5,
                'content-type': 'test'}

    def upload(self, filename, iterable, pseudo_folder=None,
               create_container=True):
        file_path = os.path.join(self.path, self.container, filename)
        path = os.path.dirname(file_path)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(file_path, 'wb') as f:
            while True:
                data = iterable.read(1024)
                if not data:
                    break
                f.write(data)
