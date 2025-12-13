#!/usr/bin/python

import json
import os

from impactrun import reportutil, runconfig
from impactrun.runconfig import dloginputdname, dlogrespdname

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
ainfofname = runconfig.dainfofname


def moveToNoRetest(rval, api):
    ''' utility function: move api in skipped/retest to no-retest
        if other test on same api passed/failed
    '''
    if "retest" in rval["skipped"]:
        if api in rval["skipped"]["retest"]:
            objs = rval["skipped"]["retest"][api]
            for obj in objs:
                if obj["reason"] == "--":
                    obj["reason"] = "Test calls with same attack type has generated passed/failed outcome."
            if "no-retest" not in rval["skipped"]:
                rval["skipped"]["no-retest"] = {api: obj}
            elif api in rval["skipped"]["no-retest"]:
                rval["skipped"]["no-retest"][api].append(obj)
            else:
                rval["skipped"]["no-retest"][api] = {api: obj}
            del rval["skipped"]["retest"][api]
    if "no-retest" in rval["skipped"]:
        if api in rval["skipped"]["no-retest"]:
            if isinstance(rval["skipped"]["no-retest"][api], list):
                for each_api in rval["skipped"]["no-retest"][api]:
                    reason = each_api.get('reason')
                if reason.find("Also") < 0:
                    rval["skipped"]["no-retest"][api][0]['reason'] += (". Also test calls with same attack type has "
                                                                       "generated passed/failed outcome.")
            else:
                reason = rval["skipped"]["no-retest"][api].get('reason')
                if reason.find("Also") < 0:
                    rval["skipped"]["no-retest"][api]['reason'] += (". Also test calls with same attack type has "
                                                                    "generated passed/failed outcome.")


def parseStdoutForInput(instdout):
    debugstr = "for debugging:"
    datastr = "\'data\':"
    if instdout.find(debugstr) < 0:
        return ""
    sstr = instdout[instdout.find(debugstr) + len(debugstr):]
    if sstr.find(datastr) < 0:
        return ""
    sstr = sstr[sstr.find(datastr) + len(datastr):]
    headerstr = ", \'headers\':"
    rvalsindx = sstr.find("{")
    rvaleindx = sstr.find(headerstr)
    if rvalsindx < 0 or rvaleindx < 0:
        print(f"Debug == failed to extract inputstr from {sstr}")
        return ""
    return sstr[rvalsindx: rvaleindx]


def extractAPITests(attack, severity, inreport, inainfo):
    ''' Given a dict of a report.json from perattack, extract per-api reports of test data
        contains two dicts, one is "tested", one is "skipped", each skip has either
        "no-retest"/"retest" status. No-retest can be no fuzzing needed or same attack, same api
        test has passed/failed in another test
    '''
    rval = {"tested": {}, "skipped": {}}
    alltests = inreport["report"]["tests"]

    cnt = 0
    for onetest in alltests:
        cnt += 1
        name = onetest["name"]
        tname = name.split("::")[1]

        s = tname[len("test_"):]
        method = s[:s.find("_")]
        api = s[s.find("_") + 1: s.find("_for_fuzzing")].replace("__", "/").replace("9i9", "-")
        if "call" not in onetest:
            continue
        outcome = onetest["outcome"].lower()  # outcome can be pass/failed/skipped
        meta = onetest["metadata"][0]
        inobj = {
            "api": api, "method": method, "outcome": outcome, "attack": attack,
            "severity": severity, "attackinfo": inainfo, "testinput": ""
        }

        if not outcome == "skipped":  # has a passed/failed outcome
            mdata = meta.split("::")
            inobj["resp"] = mdata[4]  # get the response code
            inobj["respmsg"] = mdata[6]
            inobj["apatternfile"] = mdata[len(mdata)-1]  # last one is the attack pattern file
            if "stdout" in onetest["call"]:
                inputstr = parseStdoutForInput(onetest["call"]["stdout"])
                if inputstr:
                    inobj["testinput"] = inputstr
            if outcome == "failed":
                if not inobj["apatternfile"]:  # sometimes the attack pattern file name is missing from the report
                    inobj["apatternfile"] = reportutil.patchAttackPatternFile(attack)

        if outcome == "skipped":
            i = meta.find("SKIP_REASON-->")
            reason = ""
            if i > 0:
                reason = meta[i + len("SKIP_REASON-->"):meta.find("::", i)]
            if reason:
                inobj["reason"] = reason
            else:
                inobj["reason"] = "--"

            designation = "retest"
            if (reason and (reason.startswith("No values for the parameters") or
                            reason.startswith("No Parameters to fuzz"))):
                designation = "no-retest"
            if api in rval["tested"]:
                designation = "no-retest"
                if reason == "--":
                    reason = "Test calls with same attack type has generated passed/failed outcome."
                else:
                    reason += ". Also test calls with same attack type has generated passed/failed outcome."

            if designation in rval["skipped"]:
                if api in rval["skipped"][designation]:
                    rval["skipped"][designation][api].append(inobj)
                else:
                    rval["skipped"][designation][api] = [inobj]
            else:
                rval["skipped"][designation] = {api: [inobj]}
        else:
            moveToNoRetest(rval, api)  # if any api is found not to skipped, move that api from retest to no retest
            if outcome in rval["tested"]:  # tests sharing the same outcome is saved in a list
                rval["tested"][outcome].append(inobj)
            else:
                rval["tested"][outcome] = [inobj]
    return rval


def summaryPerSpec(sumr, spec, newtests):
    ''' Called on a spec by spec based, summarize
        for html table display from test data captured
    '''
    if spec not in sumr:
        sumr[spec] = {
            "tapis": 0, "ttpassed": 0, "ttfailed": 0, "tCH": 0, "tM": 0,
            "tL": 0, "tI": 0, "tatype": 0, "apis": {}, "retest": {}
        }
    sele = sumr[spec]
    cumapi = sele["apis"]
    tpass = 0
    tfail = 0
    tm = 0
    tch = 0
    tl = 0
    ti = 0

    ele = newtests["tested"]
    if "passed" in ele:
        for a in ele["passed"]:
            cumapi[a["api"]] = 1
        tpass = len(ele["passed"])
    if "failed" in ele:
        for a in ele["failed"]:
            cumapi[a["api"]] = 1
            if a["severity"].lower().startswith("m"):
                tm += 1
            elif a["severity"].lower().startswith("l"):
                tl += 1
            elif a["severity"].lower().startswith("c") or a["severity"].lower().startswith("h"):
                tch += 1
            else:
                ti += 1
        tfail = len(ele["failed"])
    ele = newtests["skipped"]
    if "no-retest" in ele:
        for a in ele["no-retest"].keys():
            cumapi[a] = 1
        tpass += len(ele["no-retest"])
    if "retest" in ele:
        for a, v in ele["retest"].items():
            if a not in sele["retest"]:
                sele["retest"][a] = v
            else:
                sele["retest"][a].extend(v)

    sele["tapis"] = len(cumapi)
    sele["ttpassed"] += tpass
    sele["ttfailed"] += tfail
    sele["tCH"] += tch
    sele["tM"] += tm
    sele["tL"] += tl
    sele["tI"] += ti


def sumRetests(sumr):
    ''' Saved skipped case into a json file for later retest '''
    rtestauth = {}
    rtestother = {}
    rhtml = "<table>\n<tr>\n"
    rhtml += "<th>SpecName</th>\n"
    rhtml += "<th>N of tests skipped due to 401 failed Authorization.</th>\n"
    rhtml += "<th>N of tests skipped due to other exceptions</th>\n"
    rhtml += "</tr>\n"
    for (spec, t) in sumr.items():
        rhtml += "\n<tr><td>" + spec + "</td>\n"
        r401 = 0
        rother = 0
        if "retest" in t:
            for _, v in t["retest"].items():
                for at in v:
                    if at["reason"].startswith("Status code is 401"):
                        if spec in rtestauth:
                            rtestauth[spec].append(at)
                        else:
                            rtestauth[spec] = [at]
                        r401 += 1
                    else:
                        if spec in rtestother:
                            rtestother[spec].append(at)
                        else:
                            rtestother[spec] = [at]
                        rother += 1

        rhtml += "\n<td>" + str(r401) + "</td>\n"
        rhtml += "\n<td>" + str(rother) + "</td>\n"
    rhtml += "</table>\n"
    f = open("retest-auth.json", "w+", encoding='utf-8')
    json.dump(rtestauth, f)
    f.close()
    f = open("retest-exceptions.json", "w+", encoding='utf-8')
    json.dump(rtestother, f)
    f.close()
    return rhtml


def failedTestReport(failedr, spec, newtests):
    '''
    for a particular spec, analyze all failed tests
    group them into a list of 4 priorties
    * returned data + severity Critical or H, P1
    * returned data, other severity           P2
    * no returned data, C or H severity,      P3
    * all others                              P4

    failedr(eport) is a structure
    /spec/api/[p1,p2,p3,p4] at which
        /method(get,post,delete)/
            ({response-code:[attacks]}, {attackname:[attack-patternfiles]})
    '''
    ele = newtests["tested"]
    if "failed" in ele:
        if spec not in failedr:
            failedr[spec] = {}
        sele = failedr[spec]

        for a in ele["failed"]:
            pri = 4
            api = a["api"]
            sev = a["severity"]
            rsp = a["resp"]
            att = a["attack"]
            m = a["method"]
            attf = a["apatternfile"]

            if rsp and rsp.startswith("200-->"):
                if len(rsp) > len("200-->[]") and (not rsp == "200-->null"):
                    if sev.lower().startswith("c") or sev.lower().startswith("h"):
                        pri = 1
                    else:
                        pri = 2
            if sev.lower().startswith("c") or sev.lower().startswith("h"):
                if pri > 3:
                    pri = 3
            orgele = {}
            if api in sele:
                orgele = sele[api][pri-1]
            else:
                sele[api] = [{}, {}, {}, {}]
                orgele = sele[api][pri-1]

            rsp = rsp.lower()
            if m.lower() in orgele:
                (morgele, afdic) = orgele[m.lower()]
                if rsp in morgele:
                    if att not in morgele[rsp]:
                        morgele[rsp].append(att)
                else:
                    morgele[rsp] = [att]
                if attf:
                    if att in afdic:
                        if attf not in afdic[att]:
                            afdic[att].append(attf)
                    else:
                        afdic[att] = [attf]
            else:
                if attf:
                    orgele[m.lower()] = ({rsp: [att]}, {att: [attf]})
                else:
                    orgele[m.lower()] = ({rsp: [att]}, {})


def genPRows(pri, ftxt, color, t, fnum, prevrows, apidef, respdname=dlogrespdname):
    ''' A utility function, just generate for each priority html table rows '''
    ptext = "<b><font color=\"" + color + "\">" + pri + "</font></b>"
    rhtml = ""
    totalrows = 0
    aprefix = runconfig.dfuzzdbdirname + "/"
    for m, rvec in t.items():
        paramstr = ""
        if m not in apidef:
            print(f"Skipping param reporting method {m} not defined in apispec")
        else:
            #import pdb;pdb.set_trace()
            if 'parameters' in apidef[m]:
                for p in apidef[m]["parameters"]:
                    paramstr += p["name"] + ", "
                if paramstr:
                    paramstr = paramstr[:len(paramstr) - 2]

        (rt, adic) = rvec
        for r, ats in rt.items():
            atxt = ("<font size=\"-2\">HTTP method <b>" + m + "</b>; API parameters \"fuzzed\" with attack "
                    "patterns: <b>(" + paramstr + ")</b>." + ftxt + "<br>")
            rtxt = ""
            if len(r) > 20:
                if not os.path.exists(respdname):
                    os.mkdir(respdname)
                fnum += 1
                fname = respdname + "/resp" + str(fnum) + ".txt"
                f = open(fname, "w+", encoding='utf-8')
                f.write(r)
                f.close()
                rtxt = "<a href=\"" + fname + "\">response message log</a>"
            else:
                rtxt = r
            atxt += "Attacks(" + str(len(ats)) + ") with links to test fuzz pattern file:"
            for a in ats:
                anametxt = a
                if a in adic:
                    if adic[a]:
                        if len(adic[a]) == 1:
                            anametxt = " <a href=\"" + aprefix + adic[a][0] + "\">" + a + "</a>"
                        elif len(adic[a]) > 1:
                            anametxt += "["
                            indx = 1
                            for af in adic[a]:
                                anametxt += " <a href=\"" + aprefix + af + "\">" + str(indx) + "</a> "
                                indx += 1
                            anametxt += "]"
                atxt += anametxt + ", "
            atxt = atxt[:len(atxt)-1]
            atxt += "</font>\n"
            tr = ""
            if prevrows > 0:
                tr = "<tr>"
            else:
                prevrows += 1
            rhtml += (tr + "<td>" + ptext + "</td><td>" + atxt + "</td><td><font size=\"-2\">" + rtxt +
                      "</font></td></tr>\n")
            totalrows += 1
    return (rhtml, fnum, totalrows)


def processFailedTests(failedr, sumr={}, fnum=1, respdname=dlogrespdname):
    '''
    Generate a fordev-apis.html report
    response data longer than 20 characters are saved
    in a txt file, pointed to from report html under
    <dlogrespdname> defined in runconfig

    A large table of spec->api->P->Details report and
    A summary table showing the number of failed/passed/skipped for each spec
    '''
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0

    rhtml = ""
    rhtml += "<br><table>\n<tr>\n"
    rhtml += "<th>SpecName</th>\n"
    rhtml += "<th>APIs</th>\n"
    rhtml += "<th>Priorities</th>\n"
    rhtml += "<th>Test Details</th>\n"
    rhtml += "<th>Response Data</th>\n"
    rhtml += "</tr>\n"

    sumhtml = ""

    for spec, a in failedr.items():
        apaths = reportutil.getPathsFromSpec(spec)
        if not apaths:
            print(f"Skipping reporting on spec {spec}, no valid spec with api paths element found")
            continue

        srow = 0
        rahtml = ""
        firstapi = True
        sp1 = 0
        sp2 = 0
        sp3 = 0
        sp4 = 0
        for api, t in a.items():
            apidef = {}
            apiname = api
            for p, adef in apaths.items():
                if reportutil.matchAPIPath(api, p):
                    apidef = adef
                    apiname = p
                    break
            if not apidef:
                print(f"No parameter info for failed test reporting on spec {spec}, api {api}, no api def found")
                continue
            r2html = ""
            rrow = 0
            if len(t[0]) > 0:
                (rtxt, fnum, r) = genPRows("P1", ("Service failed to reject but returns 200 OK with data instead. "
                                                  "Fuzz attacks are in high severity catagory."),
                                           "red", t[0], fnum, rrow, apidef, respdname)
                r2html += rtxt
                rrow += r
                p1 += r
                sp1 += r
            if len(t[1]) > 0:
                (rtxt, fnum, r) = genPRows("P2", ("Service failed to reject but returns 200 OK with data instead. "
                                                  "Fuzz attacks are in medium/low severity catagory."),
                                           "brown", t[1], fnum, rrow, apidef, respdname)
                r2html += rtxt
                rrow += r
                p2 += r
                sp2 += r
            if len(t[2]) > 0:
                (rtxt, fnum, r) = genPRows("P3", ("Service failed to reject but return 200 OK with empty response. "
                                                  "Service might have processed attack input. Fuzz attacks are in "
                                                  "high severity catagory."),
                                           "blue", t[2], fnum, rrow, apidef, respdname)
                r2html += rtxt
                rrow += r
                p3 += r
                sp3 += r
            if len(t[3]) > 0:
                (rtxt, fnum, r) = genPRows("P4", ("Service failed to reject but return 200 OK with empty response. "
                                                  "Service might have processed attack input. Fuzz attacks are in "
                                                  "medium/low severity catagory."),
                                           "black", t[3], fnum, rrow, apidef, respdname)
                r2html += rtxt
                rrow += r
                p4 += r
                sp4 += r

            srow += rrow
            tr = ""
            if not firstapi:
                tr = "<tr>"
            else:
                firstapi = False
            rahtml += tr + "<td rowspan=\"" + str(rrow) + "\"><font size=\"-1\">" + apiname + "</font></td>\n"
            rahtml += r2html

        rhtml += "<tr><td rowspan=\"" + str(srow) + "\">" + spec + "</td>\n"
        rhtml += rahtml

        if spec in sumr:
            t = sumr[spec]
            sumhtml += "\n<tr><td>" + spec + "</td>\n"
            sumhtml += "<td>" + str(t["tapis"]) + "</td>\n"
            sumhtml += "<td><font color=\"red\">" + str(sp1) + "</font></td>\n"
            sumhtml += "<td><font color=\"brown\">" + str(sp2) + "</font></td>\n"
            sumhtml += "<td><font color=\"blue\">" + str(sp3) + "</font></td>\n"
            sumhtml += "<td><font color=\"black\">" + str(sp4) + "</font></td>\n"
            sumhtml += "<td>" + str(t["tatype"]) + "</td>\n"
            sumhtml += "<td><font color=\"red\">" + str(t["ttfailed"]) + "</font></td>\n"
            sumhtml += "<td><font color=\"green\">" + str(t["ttpassed"]) + "</font></td>\n"
            sumhtml += "</tr>\n"
    rhtml += "</table>"

    goodspecs = []
    for (spec, t) in sumr.items():
        if spec not in failedr:
            sumhtml += "\n<tr><td>" + spec + "</td>\n"
            sumhtml += "<td>" + str(t["tapis"]) + "</td>\n"
            sumhtml += "<td><font color=\"red\">0</font></td>\n"
            sumhtml += "<td><font color=\"brown\">0</font></td>\n"
            sumhtml += "<td><font color=\"blue\">0</font></td>\n"
            sumhtml += "<td><font color=\"black\">0</font></td>\n"
            sumhtml += "<td>" + str(t["tatype"]) + "</td>\n"
            sumhtml += "<td><font color=\"red\">" + str(t["ttfailed"]) + "</font></td>\n"
            sumhtml += "<td><font color=\"green\">" + str(t["ttpassed"]) + "</font></td>\n"
            sumhtml += "</tr>\n"
            goodspecs.append(spec)
    if sumr:
        print("Total issues: p1 {p1}, p2 {p2}, p3 {p3}, p4 {p4}")
        print("Specs with no issues found: {goodspecs}")
    return rhtml, sumhtml, fnum


def genCSVPRows(spec, api, pri, t, apidef):
    ''' A utility function, just generate for each priority
        using the definition a row for csv
    '''
    csvrows = []
    for m, rvec in t.items():
        n = 0
        aliststr = ""
        rt, _ = rvec
        for _, al in rt.items():
            n += len(al)
            for x in al:
                aliststr += x + "|"
        if m not in apidef:
            print(f"Skipping csv reporting on spec {spec}, api {api}, method {m} not defined in apispec")
            continue
        paramstr = ""
        if 'parameters' in apidef[m]:
            for p in apidef[m]["parameters"]:
                paramstr += p["name"] + " |"
            if paramstr:
                paramstr = paramstr[:len(paramstr) - 1]
        csvtxt = (spec + "," + api + "," + pri + ", Test: HTTP method=" + m + " on API setting parameter(s) (" +
                  paramstr + ") value to fuzz attack pattern. Service should have rejected but return 200 OK. , "
                  "Success attacks:number of attacks= " + str(n) + " (" + aliststr + ") Fuzz patterns in fuzzdb,\n ")

        csvrows.append(csvtxt)
    return csvrows


def get_attack_by_category(failed_test):
    ''' A utility function to parse tests by attack category '''
    result = ""
    api_set = set()
    for test_case in failed_test:
        api = test_case.get('api', '')
        if api in api_set:
            continue
        api_set.add(api)
        result += test_case.get('attack', '') + ',' + api + ',' + test_case.get('severity', '') + ',' + '\n'
    return result


def sumFailedTestsToCSV(csvfname, failedr, failed_tests):
    ''' pick specs, apis, and failed test severities,
        load from original specs the parameters to provide a
        how to fix report for each of the vulnerabilities
    '''
    allrows = [[], [], [], []]
    for spec, a in failedr.items():
        apaths = reportutil.getPathsFromSpec(spec)
        if not apaths:
            print(f"Skipping reporting on spec {spec}, no valid spec with paths element found")
            continue

        for api, t in a.items():
            apidef = {}
            apiname = ""
            for p, adef in apaths.items():
                if reportutil.matchAPIPath(api, p):
                    apidef = adef
                    apiname = p
                    break
            if not apidef:
                print(f"Skipping csv reporting on spec {spec}, api {api}, no api def found")
                continue

            if len(t[0]) > 0:
                allrows[0].extend(genCSVPRows(spec, apiname, "1", t[0], apidef))
            if len(t[1]) > 0:
                allrows[1].extend(genCSVPRows(spec, apiname, "2", t[1], apidef))
            if len(t[2]) > 0:
                allrows[2].extend(genCSVPRows(spec, apiname, "3", t[2], apidef))
            if len(t[3]) > 0:
                allrows[3].extend(genCSVPRows(spec, apiname, "4", t[3], apidef))
    csv = "API Fuzz Attack Security Testing Report, , , , ,\n"
    csv += ", , , , ,\n"
    csv += (",Test Method:, ,APIs are invoked with input parameter values set to invalid patterns from known "
            "attacks of various types. Service is considered potentially vulnerable if it responds with 200 Ok "
            "or worse with data., ,\n")
    csv += ", , , , ,\n"
    csv += ",Priority of potential vulnerabilities:, , , ,\n"
    csv += ", ,P1, Data returned from service. Attack(s) tested are considered of Critical or High severity, ,\n"
    csv += ", ,P2, Data returned from service. Attack(s) tested are considered of Medium or lower severity, ,\n"
    csv += (", ,P3, No Data returned from service. Attack(s) tested are considered of Critical or High severity. "
            "Attack input can still cause damage as service appears to have processed it, ,\n")
    csv += (", ,P4, No Data returned from service. Attack(s) tested are considered of Medium or lower severity. "
            "Safety check is still recommended, ,\n")
    csv += ", , , , ,\n"
    n = 0
    tmpcsv = ""
    pcnts = [0, 0, 0, 0]
    for pr in allrows:
        pcnts[n] = len(pr)
        n += 1
        for r in pr:
            tmpcsv += r
    csv += ",Vulnerabilities Found:, , , ,\n"
    n = 1
    for c in pcnts:
        csv += ", ,P" + str(n) + ":," + str(c) + ", ,\n"
        n += 1
    csv += ", , , , ,\n"
    csv += "Specification Name, API Name, Severity, Test Info for Repro/Fix , Fuzz Attack Info,\n"
    csv += tmpcsv

    csv += ", , , , ,\n"
    csv += ",Attack by categories:, , , ,\n"
    csv += ", , , , ,\n"
    res = get_attack_by_category(failed_tests)
    if res:
        csv += "Attack Categery, API, Severity,\n"
        csv += res

    f = open(csvfname, "w+", encoding='utf-8')
    f.write(csv)
    f.close()


def sumToHTMLTRs(sumr):
    ''' utility to generate raws for summary report due to change, the sum table is
        now generated by processFailedTests
        Keep to reorg retest for now
    '''
    rtests = {}
    for (spec, t) in sumr.items():
        if t["retest"]:
            for _, v in t["retest"].items():
                if spec in rtests:
                    rtests[spec].extend(v)
                else:
                    rtests[spec] = v


def genInputReportFile(tests, fnum):
    ''' utility: take a list of tests objects, if testinput key is there,
        generate a list of input string that is used for the testing, return a link
    '''
    r = ""
    for t in tests:
        if t["testinput"]:
            r += t["testinput"] + "\n"
    if not r:
        print("No test input found for failed tests")
        return ""
    if not os.path.exists(dloginputdname):
        os.mkdir(dloginputdname)
    fname = dloginputdname + "/input" + str(fnum) + ".txt"
    f = open(fname, "w+", encoding='utf-8')
    f.write(r)
    f.close()
    return "<a href=\"" + fname + "\">"


def sumperattack(csvfname, inspeclist=[], inattacklist=[]):
    ''' walk the perattack reports.json and generate a per spec summary '''
    ainfo = {}
    rhtml = "<br><table>\n<tr>\n"
    rhtml += "<th rowspan=\"2\">Spec Name</th>\n"
    rhtml += "<th rowspan=\"2\">N of APIs</th>\n"
    rhtml += "<th colspan=\"4\">N of API Issues By Priority</th>\n"
    rhtml += "<th rowspan=\"2\">N of Different Attack Types Tested</th>\n"
    rhtml += "<th colspan=\"2\">N of Attack Tests By Passed/Failed Results</th>\n"
    rhtml += "</tr><tr>\n"
    rhtml += "<th><font color=\"red\">P1</font></th>\n"
    rhtml += "<th><font color=\"brown\">P2</font></th>\n"
    rhtml += "<th><font color=\"blue\">P3</font></th>\n"
    rhtml += "<th><font color=\"black\">P4</font></th>\n"
    rhtml += "<th><font color=\"red\">Failed</font></th>\n"
    rhtml += "<th><font color=\"green\">Passed</font></th>\n"
    rhtml += "</tr>\n"

    detailhtml = "<br><table>\n<tr>\n"
    detailhtml += "<th>Spec Name</th>\n"
    detailhtml += "<th>Attack Type</th>\n"
    detailhtml += "<th>Attack Severity</th>\n"
    detailhtml += "<th>N of Tests Failed</th>\n"
    detailhtml += "<th>N of Tests Passed </th>\n"
    detailhtml += "<th>Compliance Classification Affected</th>\n"
    detailhtml += "</tr>\n"

    thespeclist = inspeclist if inspeclist else runconfig.apispeclist
    theattacklist = inattacklist if inattacklist else runconfig.fuzzattacklist

    sumr = {}  # summary test report filled in by sumPerSpec
    failedr = {}  # failed test report by failedTestReport

    inputfilenum = 0
    for spec in thespeclist:
        spec = spec.lower()  # important, cannonical form of spec all lower case
        if not os.path.exists(resultrootn + spec):
            print(f"Failed to generate summary report: {resultrootn + spec} does not exist")
            return ""

        an = 0
        firstattack = True
        srow = 0
        dahtml = ""
        for a in theattacklist:
            arname = a
            if arname.find("/"):
                arname = arname.replace("/", "_")

            if not ainfo:
                ainfo = reportutil.findAttackInfoObjs(theattacklist)
            if a not in ainfo:
                print(f"Attack info not found for {a} in attackinfo: {ainfo}")
                continue
            severity = ainfo[a][0]
            classification = ainfo[a][1]["classification"]

            originalr = resultrootn + spec + "/" + arname + "-report.json"

            if not os.path.exists(originalr):
                print(f"cannot regenerate report for {spec + '_' + arname} , {originalr} does not exists")
                continue
            with open(originalr, encoding='utf-8') as f:
                areporti = json.load(f)

            originalhtml = resultrootn + spec + "/" + arname + ".html"
            if not os.path.exists(originalhtml):
                print(f"cannot regenerate html report for {spec + '_' + arname}, {originalhtml} does not exists")
                continue
            tests = extractAPITests(a, severity, areporti, ainfo)

            npassed = 0
            nfailed = 0
            inputlink = ""
            if "passed" in tests["tested"]:
                npassed = len(tests["tested"]["passed"])
            if "failed" in tests["tested"]:
                nfailed = len(tests["tested"]["failed"])
                if nfailed > 0:
                    inputlink = genInputReportFile(tests["tested"]["failed"], inputfilenum)
                    inputfilenum += 1
            tr = ""
            if not firstattack:
                tr = "<tr>"
            else:
                firstattack = False
            dahtml += tr + "<td><a href=\"" + originalhtml + "\">" + a + "</a></td>"
            dahtml += "<td>" + severity + "</td>"
            if inputlink:
                dahtml += "<td>" + inputlink + "<font color=\"red\">" + str(nfailed) + "</font></a></td>"
            else:
                dahtml += "<td><font color=\"red\">" + str(nfailed) + "</font></td>"
            dahtml += "<td><font color=\"green\">" + str(npassed) + "</font></td>"
            dahtml += "<td><font size=\"-2\">" + classification + "</font></td></tr>\n"
            srow += 1
            summaryPerSpec(sumr, spec, tests)
            failedTestReport(failedr, spec, tests)
            an += 1
        detailhtml += "<tr><td rowspan=\"" + str(srow) + "\">" + spec + "</td>\n"
        detailhtml += dahtml
        sumr[spec]["tatype"] = an
    detailhtml += "</table>\n"
    sumToHTMLTRs(sumr)

    rskipped = sumRetests(sumr)
    fthtml, sumhtml, _ = processFailedTests(failedr, sumr)
    rhtml += sumhtml
    rhtml += "</table>\n"
    rhtml += "<h4>Priorities</h4><UL>\n"
    rhtml += ("<LI><font color=\"red\"><b>P1</b></font>: When an API is called with parameter value set to "
              "patterns that were associated with known attacks that can cause critical/high severity damages, the "
              "API returns 200 OK with data. It appears that the app not only processes the fuzz parameter but also "
              "is at risk of leaking data.\n")
    rhtml += ("<LI><font color=\"brown\"><b>P2</b></font>: When an API is called with parameter value set to "
              "patterns that were associated with known attacks that can cause medium/low severity damages, the "
              "API returns 200 OK with data. It appears that the app not only processes the fuzz parameter but also "
              "is at risk of leaking data.\n")
    rhtml += ("<LI><font color=\"blue\"><b>P3</b></font>: When an API is called with parameter value set to "
              "patterns that were associated with known attacks that can cause critical/high severity damages, the "
              "API returns 200 OK with no data. Though it does not appear that the app is at risk of leaking data, "
              "the app might have processed the fuzzed input, which can cause subsequent security issues.\n")
    rhtml += ("<LI><font color=\"black\"><b>P4</b></font>: When an API is called with parameter value set to "
              "patterns that were associated with known attacks that can cause medium/low severity damages, the API "
              "returns 200 OK with no data. Though it does not appear that the app is at risk of leaking data, the "
              "app might have processed the fuzzed input, which can cause subsequent security issues.\n")
    rhtml += "</UL>\n"
    failed_tests = tests.get('tested', {}).get('failed', [])
    sumFailedTestsToCSV(csvfname, failedr, failed_tests)
    if runconfig.savefailedtestreport:
        if runconfig.usecustomreportfname:
            f = open(runconfig.customsavedreportfanme, "w+", encoding='utf-8')
            json.dump(failedr, f)
            f.close()
    return (rhtml, detailhtml, fthtml, rskipped)


def main():
    reportutil.init()
    sumperattack(runconfig.apispeclist, runconfig.fuzzattacklist)


if __name__ == "__main__":
    main()
