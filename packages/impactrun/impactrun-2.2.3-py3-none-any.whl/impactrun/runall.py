#!/usr/bin/python

import sys
import time
from datetime import datetime

from impactrun import reportutil, runconfig, sumreport
from impactrun.htmlreportgenerator import generate_html_report, iterateallspecs
from impactrun.runconfig import fuzzattacklist
from impactrun.runperattack import perattackcall


def processFnames(inargv, postfix, defaultf, defaultt):
    ''' process argv, to figure out whether custom
        output file exists and whether timestamps should be added
    '''
    for report in inargv:
        if report.endswith(postfix):
            return (report, False, False)
    return (defaultf, defaultt, True)


def main(regen, customer_name='N/A'):
    csvfname = runconfig.dcsvreportfname
    htmlfname = runconfig.dhtmlreportfname
    addhtmltstamp = runconfig.attachtimestamptoreport
    addcsvtstamp = runconfig.attachtimestamptoreport

    usagestr = ("\nUsage: [--regen-report or -r] [an .html report filename: Default " +
                runconfig.dhtmlreportfname + "-<timestamp>] [a .csv report filename: Default " +
                runconfig.dcsvreportfname + "<timestamp>] (Timestamp will not be added to user specified " +
                "filenames; can specify one or both custom report name as long as .html/.csv postfixes are " +
                "specified.)\n")

    if regen:
        (htmlfname, addhtmltstamp, notfound1) = processFnames(regen, ".html", htmlfname, addhtmltstamp)
        (csvfname,  addcsvtstamp,  notfound2) = processFnames(regen, ".csv",  csvfname,  addcsvtstamp)
        if notfound1 and notfound2:
            print(usagestr)
            return

    tnow = datetime.now()
    tstamp = tnow.strftime("%Y%m%d%H%M%S")
    if addhtmltstamp:
        htmlfname = htmlfname + "-" + tstamp + ".html"
    if addcsvtstamp:
        csvfname = csvfname + "-" + tstamp + ".csv"

    reportutil.init()

    print(f"Testing APIs and generating html report in {htmlfname} and csv report in {csvfname}")
    hs = ("<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px dotted black;\n border-collapse: collapse}"
          "</style>\n<title>API Test Report Summary</title></head><body><br>\n")
    print("Starting API Tests: Testing all APIs in a spec one fuzz attack type at a time")
    perattackcall(regen, runconfig.apispeclist, fuzzattacklist)

    (rsum, detail, rfailed, rskipped) = sumreport.sumperattack(csvfname, runconfig.apispeclist, fuzzattacklist)

    f = open(htmlfname, "w+", encoding='utf-8')
    f.write(hs)
    if rsum:
        f.write("\n<h2>Test Summary</h2><br>\n" + rsum)
    if rfailed:
        f.write("\n<h3>Failed Test Reports Per API</h3><br>\n" + rfailed)
    if detail:
        f.write("\n<h2>Detailed Per Attack Test Report</h2><br>\n" + detail)
    if rskipped:
        f.write("\n<h3>Skipped Test Reports Per Spec</h3><br>\n" + rskipped)
#    if ra:
#        hs += "\n<h3>Reports Per Attack</h3><br>\n" + ra
#    if rb:
#        hs += "\n<h3>Reports Per API</h3><br>\n" + rb

    f.write("\n\n</body></html>")
    f.close()

    result_report = iterateallspecs(runconfig.apispeclist, runconfig.fuzzattacklist)
    generate_html_report(result_report, "report_summary_" + str(time.time()) + ".html", customer_name)


if __name__ == "__main__":
    main()
