#!/usr/bin/python

import os
import shutil
import sys

from impactrun import runconfig, runonetest
from impactrun.impact_core import ImpactCore

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"


def perattackcall(regenreport, inspeclist=[], inattacklist=[]):
    rhtml = "<table><tr><th>API Specification</th><th>Per Attack Reports</th></tr>\n"
    thespeclist = inspeclist if inspeclist else runconfig.apispeclist
    theattacklist = inattacklist if inattacklist else runconfig.fuzzattacklist
    for spec in thespeclist:
        spec = spec.lower()  # important: use all lower case cannonical form
        if not os.path.exists(resultrootn + spec):
            os.mkdir(resultrootn + spec)

        rhtml += "\n<tr><td>" + spec + "</td>\n"
        rhtml += "\n<td><b>Report Based on Each Attack Type:</b><ul>"
        for a in theattacklist:
            arname = a
            if arname.find("/"):
                arname = arname.replace("/", "_")

            if not regenreport:
                runonetest.runtest(spec, "", runconfig.dhostname, resultrootn + spec + "/" + arname + ".html",
                                   a, runconfig.dperattackvalueused)

                if os.path.exists("report.json"):
                    shutil.copy("report.json", resultrootn + spec + "/" + arname + "-report.json")
            else:
                originalr = resultrootn + spec + "/" + arname + "-report.json"
                if os.path.exists(originalr):
                    shutil.copy(originalr, "report.json")
                else:
                    print(f"Cannot regenerate report for {spec}_{arname}, {originalr} does not exists")
                    continue

                print(f"Spec_API {spec}_{arname}, regenerating html report to {resultrootn + spec}/{arname}.html")

                if not os.path.exists("tests"):
                    os.mkdir("tests")
                if not os.path.exists("tests/data"):
                    os.mkdir("tests/data")
                if not os.path.exists("mytests/attack_info.json"):
                    if not os.path.exists(spec.lower() + "_tests/data/attack_info.json"):
                        print(f"Missing attack_info {spec.lower()}_tests/data/attack_info.json, please run fuzzing "
                              f"or make sure mytests/attack_info.json exists")
                    else:
                        shutil.copy(spec + "_tests/data/attack_info.json", "tests/data/")
                else:
                    shutil.copy("mytests/attack_info.json", "tests/data/")
                ImpactCore.generate_fuzz_report(resultrootn + spec + "/" + arname + ".html")

            rhtml += "\n<li><a href=\"" + resultrootn + spec + "/" + arname + ".html" + "\">" + arname + "</a>"
        rhtml += "\n</ul>\n</td></tr>\n"
    rhtml += "</table>\n"
    return rhtml


def main():
    r = ""
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("regen"):
            r = perattackcall(True)
        else:
            print("Usage: [Optional flag regenreport to just regenerate the reports, run all tests on a per API basis")
            return
    else:
        r = perattackcall(False)
    print(r)


if __name__ == "__main__":
    main()
