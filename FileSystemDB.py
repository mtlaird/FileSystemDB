from FileSystemClasses import Directory
from FileSystemSql import create_database
import sys

if __name__ == '__main__':

    Session = create_database('db')
    session = Session()

    directory_name = sys.argv[1]

    print "Creating directory object for directory {} ...".format(directory_name)
    directory = Directory(directory_name)

    print "Total directory size: {}".format(directory.get_total_size())
    print "Total files: {}".format(directory.get_total_files())

    print "Adding files to database ..."
    directory.add_files_to_db(session)

    print "Complete!"
