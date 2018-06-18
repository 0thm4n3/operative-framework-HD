#!/usr/bin/env  python

from engine import database


def main():
    db = database.Engine("localhost", 27017)
    db.load_modules()


if __name__ == "__main__":
    main()