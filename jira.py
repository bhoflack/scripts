#!/usr/bin/env python

"""
Script responsible for logging work to the melexis jira server.
"""

import SOAPpy
import SOAPpy.Types
import datetime
import os
import sys
import time

from optparse import OptionParser

CONFIG = os.path.expanduser('~/.jira')

def logwork(soap, auth, issue, timeSpent, comment = '', startdate=datetime.date.today()):
    dateObj = SOAPpy.Types.dateTimeType((startdate.year, startdate.month, startdate.day, 0, 0, 0))
    worklog = {'comment': comment,
               'timeSpent': timeSpent,
               'startDate': dateObj}
    soap.addWorklogAndRetainRemainingEstimate(auth, issue, worklog)

def main():
    o = {'username': None, 'password': None}
    if os.path.exists(CONFIG):
        o = dict(line.strip().split('=') for line in open(CONFIG))

    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username",
                      help="The username to login to jira", default=o['username'])
    parser.add_option("-p", "--password", dest="password",
                      help="The password to login to jira", default=o['password'])
    parser.add_option("-i", "--issue", dest="issue",
                      help="The jira issue number")
    parser.add_option("-c", "--comment", dest="comment",
                      help="The comment to log")
    parser.add_option("-t", "--time", dest="time",
                      help="The amount of time to log")

    (options, args) = parser.parse_args()

    if options.username == None or options.password == None or options.issue == None or options.time == None:
        usage()
        sys.exit(2)

    soap = SOAPpy.WSDL.Proxy('http://extranet.admin.elex.be:8080/jira/rpc/soap/jirasoapservice-v2?wsdl')
    auth = soap.login(options.username, options.password)
    logwork(soap, auth, options.issue, options.time, options.comment)

if __name__ == '__main__':
    main()
