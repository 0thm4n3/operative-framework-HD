#!/usr/bin/env  python

from engine import session, database
import subprocess


def main():
    db = database.Engine("localhost", 27017)
    print db.load_modules()
    #s = session.Sess("AUWU4M5V")
    #s.testing()
    #load = s.load_session()
    #print load.export
    #random_id = "BD9UV8KB"
    #try:
    #    subprocess.Popen(['/usr/bin/python', 'external.py', '-s', random_id, '-i', random_id], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #except subprocess.CalledProcessError as e:
    #    print e


if __name__ == "__main__":
    main()
