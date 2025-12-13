#!/usr/bin/python

import os
import shutil
import sys

from impactrun import impact_core
from impactrun.runconfig import dcviast_fuzz_type, dhostname, dspecnamec, dtestdirname


def runtest(specnamec, perapifname, targethost, resulthtml,
            cviast_fuzz_type="All", cviast_max_value_to_fuzz="1"):
    ''' specnamec is specname w capital letters
        return a link to the result
    '''
    fulltestname = dtestdirname
    if not specnamec:
        specnamec = dspecnamec

    specnamel = specnamec.lower()
    testdirname = specnamel + "_tests"
    if perapifname:
        fulltestname = testdirname + "/" + perapifname
    else:
        fulltestname = testdirname

    if not targethost:
        targethost = dhostname
    if not targethost:
        return ""

    if not cviast_fuzz_type:
        cviast_fuzz_type = dcviast_fuzz_type

    os.environ["CVIAST_FUZZ_TYPE"] = cviast_fuzz_type
    os.environ["CVIAST_MAX_VALUE_TO_FUZZ"] = cviast_max_value_to_fuzz

    sys.argv = ["impact", "--execute", fulltestname, "--host=" + targethost]
    if resulthtml:
        sys.argv.append("--report-out=" + resulthtml)

    # create attack_info.json if it does not exists
    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("tests/data"):
        os.mkdir("tests/data")
    if not os.path.exists("test/data/attack_info.json"):
        shutil.copy(testdirname + "/data/attack_info.json", "tests/data/")

    print(f"Type {cviast_fuzz_type} (max={cviast_max_value_to_fuzz}) calling cloudvector main with this arg {sys.argv}")
    impact_core.main()


def getAllAttacks(adir):
    adict = {}
    for root, dirs, _ in os.walk(adir):
        for d in dirs:
            rname = ""
            attackname = ""
            if len(root) > len(adir):
                rname = root[len(adir):]
            if rname and rname in adict:
                del adict[rname]
            if rname:
                attackname = rname + "/" + d
            else:
                attackname = d
            adict[attackname] = 1
    return list(adict.keys())


speclist = ["CpmGateway", "TelemetryGateway"]
attacklist = ['xml', 'json']
