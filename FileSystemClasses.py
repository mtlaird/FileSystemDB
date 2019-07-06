import logging
from os.path import isdir, isfile
from os import listdir, stat
import hashlib
from FileSystemSql import FileSql
from sqlalchemy.exc import ProgrammingError


class File:

    def __init__(self, path, get_md5=False):

        self.logger = logging.getLogger('FileSystemDB')
        if type(path) == str:
            try:
                path = unicode(path)
            except UnicodeDecodeError:
                print "Couldn't decode path: {}".format(path)
        if isfile(path):
            self.full_path = path
            stat_results = stat(self.full_path)
            self.size = stat_results.st_size
            self.atime = stat_results.st_atime
            self.mtime = stat_results.st_mtime
            self.ctime = stat_results.st_ctime
            self.filename = self.full_path.split('/')[-1]
            self.path = '/'.join(self.full_path.split('/')[:-1]) + '/'
            if not get_md5:
                self.md5 = None
            else:
                self.md5 = self.md5sum()
            if '.' in self.filename:
                self.extension = self.filename.split('.')[-1]
            else:
                self.extension = None
            self.sql_object = FileSql(self)

    def md5sum(self):
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def add_to_db(self, session):
        try:
            self.sql_object.add_to_db(session)
        except ProgrammingError:
            print "Couldn't add file: {} ... skipping.".format(self.full_path)


class Directory:

    def __init__(self, path):

        if '\\' in path:
            path = path.replace('\\', '/')
        if type(path) == str:
            try:
                path = unicode(path)
            except UnicodeDecodeError:
                print "Couldn't decode path: {}".format(path)

        self.files = {}
        self.directories = {}
        if isdir(path):
            self.path = path
            self.get_dir_contents()

            self.size = self.get_total_size()

    def get_dir_contents(self):

        contents = listdir(self.path)
        for c in contents:

            full_path = self.path + '/' + c

            if isdir(full_path):
                self.directories[c] = Directory(full_path)
            elif isfile(full_path):
                self.files[c] = File(full_path)

    def get_total_size(self):

        size = 0

        for f in self.files:
            size += self.files[f].size

        for d in self.directories:
            size += self.directories[d].size

        return size

    def get_total_files(self):

        files = len(self.files)

        for d in self.directories:
            files += self.directories[d].get_total_files()

        return files

    def add_files_to_db(self, session):

        for f in self.files:
            self.files[f].add_to_db(session)

        for d in self.directories:
            self.directories[d].add_files_to_db(session)
