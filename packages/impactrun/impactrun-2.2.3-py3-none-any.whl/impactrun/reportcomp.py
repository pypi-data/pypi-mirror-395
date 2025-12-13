#!/usr/bin/python

import json
import sys

from impactrun import runconfig
from impactrun import reportutil
from impactrun import sumreport


def compareAttackVectors(newv, oldv):
    ''' at the leaf level of a failed test report
        there is a vector of two dictionaries
        compare them to find net new, net old
    '''
    newr, newa = newv
    oldr, olda = oldv

    commonr = {}
    commona = {}

    for r, alist in newr.items():
        if r in oldr:  # common r
            for a in alist:
                if a in oldr[r]:
                    if r in commonr:
                        commonr[r].append(a)
                    else:
                        commonr[r] = [a]
                    if a in newa:
                        commona[a] = newa[a]
                    elif a in olda:
                        commona[a] = olda[a]
    for r, alist in commonr.items():
        for a in alist:
            oldr[r].remove(a)  # 'pop' common attack from oldr and newr
            newr[r].remove(a)
        if len(newr[r]) <= 0:
            del newr[r]
        if len(oldr[r]) <= 0:
            del oldr[r]
    return commonr, commona


def compareDicts(d1, d2):
    rval = []
    for k in d1.keys():
        if k in d2:
            rval.append(k)
    return rval


def diffFTests(newtestr, oldtestr):
    ''' comparing a new test report to old test report
        failed tests in oldtestr, but not in new tests will be considered "fixed"
        tests in new tests but not in old tests will be considered "new" finding
        tests in both will be considered persisted
    '''
    commonfound = {}
    commonspecs = compareDicts(newtestr, oldtestr)
    if not commonspecs:  # no specs in common
        return (newtestr, oldtestr, {})
    for spec in commonspecs:
        commonfound[spec] = {}
        commonapis = compareDicts(newtestr[spec], oldtestr[spec])
        if not commonapis:  # new/old has no apis in common
            continue
        for api in commonapis:
            commonfound[spec][api] = [{}, {}, {}, {}]
            newpl = newtestr[spec][api]
            oldpl = oldtestr[spec][api]
            indx = 0
            nonewapi = True
            nooldapi = True
            nocomapi = True
            while indx < 4:
                newp = newpl[indx]
                oldp = oldpl[indx]
                commonmethods = compareDicts(newp, oldp)
                if not commonmethods:
                    indx += 1
                    continue
                for m in commonmethods:
                    cr, ca = compareAttackVectors(newp[m], oldp[m])
                    if not cr:  # nothing in common
                        continue
                    commonfound[spec][api][indx][m] = (cr, ca)
                    nocomapi = False
                    (r, _) = newp[m]
                    if len(r) <= 0:
                        del newp[m]
                    (r, _) = oldp[m]
                    if len(r) <= 0:
                        del oldp[m]
                if len(newp) > 0:  # if anything left after processing
                    nonewapi = False
                if len(oldp) > 0:
                    nooldapi = False
                indx += 1
            if nonewapi:
                del newtestr[spec][api]
            if nooldapi:
                del oldtestr[spec][api]
            if nocomapi:
                del commonfound[spec][api]

        if len(newtestr[spec]) <= 0:
            del newtestr[spec]
        if len(oldtestr[spec]) <= 0:
            del oldtestr[spec]
        if len(commonfound[spec]) <= 0:
            del commonfound[spec]
    return commonfound


def compareReports(newftestfname, oldftestfname, reportfname):
    newtests = {}
    oldtests = {}
    with open(newftestfname, encoding='utf-8') as f:
        newtests = json.load(f)
        f.close()
    with open(oldftestfname, encoding='utf-8') as f:
        oldtests = json.load(f)
        f.close()
    commontests = diffFTests(newtests, oldtests)
    fnum = 1
    sumr = {}
    nhtml = ""
    ohtml = ""
    chtml = ""
    if newtests:
        (nhtml, _, fnum) = sumreport.processFailedTests(newtests, sumr, fnum, runconfig.ddiffrlogrspdirname)
    if oldtests:
        (ohtml, _, fnum) = sumreport.processFailedTests(oldtests, sumr, fnum, runconfig.ddiffrlogrspdirname)
    if commontests:
        (chtml, _, fnum) = sumreport.processFailedTests(commontests, sumr, fnum, runconfig.ddiffrlogrspdirname)
    hs = ("<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px dotted black;\n border-collapse: collapse}</style>"
          "\n<title>API Tests Comparison Report</title></head><body><br>Comparing: <ol>\n")
    hs += "\n <li>Current  test report: " + newftestfname + " \n"
    hs += "\n <li>Previous test report: " + newftestfname + " \n</ol>\n"
    f = open(reportfname, "w+", encoding='utf-8')
    f.write(hs)
    if nhtml:
        f.write("\n<h2>New Failed Tests</h2><br>\n" + nhtml)
    else:
        f.write("\n<h2>No New Failed Test.</h2><br>\n")

    if ohtml:
        f.write("\n<h2>Previously Failed Tests Fixed</h2><br>\n" + ohtml)
    else:
        f.write("\n<h2>No Fixed Previously Failed Test.</h2><br>\n")

    if chtml:
        f.write("\n<h2>Failed Tests In Both Test Reports</h2><br>\n" + chtml)
    else:
        f.write("\n<h2>Two Test Reports Have No Failed Tests In Common.</h2><br>\n")

    f.close()


def main():
    reportutil.init()
    usagestr = ("\n Usage: diff <newtest.json> <oldtest.json> <report.html> \n   Show diff of two saved test .json "
                "results and generate an html report. \n")

    if len(sys.argv) == 5:
        if not sys.argv[1] == "diff":
            print(usagestr)
            return
        compareReports(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(usagestr)


if __name__ == "__main__":
    main()
