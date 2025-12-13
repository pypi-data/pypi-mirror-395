#!/usr/bin/python

import json
import yaml
import os
import shutil
from impactrun import runconfig
from impactrun import apispecs

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
ainfofname = runconfig.dainfofname
specdname = runconfig.inspecdir

attackinfo = {}  # attack info matching attackname to info
apidef = {}  # api info matching spec->api(which is basepath + path-> path info


def init(inainfofname="", specdir=""):
    ''' called by main function to load a few global variables
        to store attack info, api definitions, and test results
        test results are saved for future comparision
    '''
    print("Initializion")
    if not inainfofname:
        inainfofname = ainfofname

    print(f"Loading Attack Info from {inainfofname}")
    if not os.path.exists(inainfofname):
        print(f"No attack info file {inainfofname}, loading from fuzzing test")
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if not os.path.exists("tests/data"):
            os.mkdir("tests/data")
        if not os.path.exists("savedattackinfo/attack_info.json"):
            print("Missing attack_info file, please run fuzzallspec.py to generate fuzzing test and test files")
            file_path = 'templates/data/attack_info.json'
            with open(file_path, encoding='utf-8') as data_file:
                data = json.load(data_file)
                with open('tests/data/attack_info.json', 'w', encoding='utf-8') as fd:
                    json.dump(data, fd)
        else:
            shutil.copy("savedattackinfo/attack_info.json", "tests/data/")

    ainfo = {}
    with open(inainfofname, encoding='utf-8') as f:
        ainfo = json.load(f)
        f.close()
    if "info" in ainfo:
        for (a, x) in ainfo["info"].items():
            attackinfo[a] = x
    else:
        print("Problem with attackinfo, no 'info' key found")

    if not specdir:
        specdir = specdname
    print("Loading api spec info")
    sfs = []
    for _, _, filename in os.walk(specdir):
        sfs.extend(filename)

    for sfname in sfs:
        aspec = {}
        if  sfname.endswith(".json"):
            with open(specdir + "/" + sfname, "r", encoding='utf-8') as f:
                aspec = json.load(f)
                f.close()
        elif sfname.endswith(".yaml") or sfname.endswith(".yml"):
            with open(specdir + "/" + sfname, "r", encoding='utf-8') as f:
                aspec = yaml.safe_load(f)
                f.close()
        else:
            print("Invalid file extension")
            exit()

        if not aspec or "paths" not in aspec:
            print(f"Failed to load api spec from {sfname}, spec does not contain required 'paths' element")
            continue
        else:
            spec = sfname[:-len(".json")].lower()
            bpath = ""
            if "basePath" in aspec:
                bpath = aspec["basePath"]
            elif "basepath" in aspec:
                bpath = aspec["basepath"]
            rval = {}
            for p, adef in aspec["paths"].items():
                newp = bpath + p
                if bpath.endswith("/") and p[0] == "/":
                    newp = bpath + p[1:]
                elif not bpath.endswith("/") and not p[0] == "/":
                    newp = bpath + "/" + p
                rval[newp] = adef
            apidef[spec] = rval

    if not runconfig.usecustomlist:
        runconfig.apispeclist = apispecs.apispeclist

    resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
    if not os.path.exists(resultrootn):
        os.makedirs(resultrootn, exist_ok=True)
    for f in os.listdir(resultrootn):
        if not f.lower() == f:
            if not f[:1] == ".":
                print(f"Rename {resultrootn + f} to {resultrootn + f.lower()} lower case")
                os.rename(resultrootn + f, resultrootn + f.lower())


def findAttackInfoObjs(inattacklist=[]):
    ''' return a list of mapping between attacknames and severity '''
    rval = {}
    ainfo = attackinfo
    for aname in ainfo.keys():
        for a in inattacklist:
            if a.startswith(aname) or a.startswith(aname.replace("_", "-")):
                for _, subinfo in ainfo[aname].items():
                    rval[a] = [subinfo["severity"], subinfo]
                    break
    return rval


def patchAttackPatternFile(attack):
    ''' a patch work around, test metadata sometime does not show the
        attack file used when it mistakens a test as skipped
        search the fuzzdb attack directory, look for the matching attack file name
        for use of a link for reporting
    '''
    dbd = runconfig.dfuzzdbdirname + "/"
    attd = "attack/" + attack + "/"
    if not os.path.exists(dbd + attd):
        return ""
    for f in os.listdir(dbd + attd):
        if not f.endswith(".md"):
            return attd + f
    return ""


def matchAPIPath(a, p):
    ''' utility api spec loading functions
        a is api name found in test name
        p is what is in the spec, may contain parameters {}
    '''
    return a.lower() in p.lower().replace("{", "").replace("}", "")


def getPathsFromSpec(spec):
    spec = spec.lower()
    if spec in apidef:
        return apidef[spec]
    else:
        return {}


def main():
    init()
    print("Attack info")
    for aname, _ in attackinfo.items():
        print(f" '{aname}' ")
    print("API info")
    for spec, a in apidef.items():
        print(f"spec: '{spec}'")
        for p, _ in a.items():
            print(f" {p} ")


if __name__ == "__main__":
    main()
