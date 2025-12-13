#!/usr/bin/python

import json
import os
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from impactrun import apispecs, reportutil, runconfig
from impactrun.html_content_gen import generate_test_report
from impactrun.runconfig import apispeclist, inspecdir

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
ainfofname = runconfig.dainfofname
global data
data = {"test_spec_insights": {}, "summary": {}, "metadata_spec": []}


def moveToNoRetest(rval, api):
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
# end moveToNoRetest


def parseStdoutForInput(instdout):
    request = ''
    curl_str = 'CURL command to retry:'
    delimiter_str = '\n\n---------------------------------\n\n'
    curl_pos = instdout.find(curl_str)
    if curl_pos < 0:
        return request
    curl_req_str = instdout[curl_pos + len(curl_str):]
    del_pos = curl_req_str.find(delimiter_str)
    if del_pos < 0:
        request = curl_req_str
    else:
        request = curl_req_str[:del_pos]
    return request
# end parseStdoutForInput

#
# Given a dict of a report.json from perattack, extract per-api reports of test data
#  contains two dicts, one is "tested", one is "skipped", each skip has either
#  "no-retest"/"retest" status. No-retest can be no fuzzing needed or same attack, same api
#  test has passed/failed in another test
#


def extractAPITests(attack, severity, inreport, inainfo):
    rval = {"tested": {}, "skipped": {}}
    alltests = inreport["report"]["tests"]

    cnt = 0
    for onetest in alltests:
        cnt += 1
        name = onetest["name"]
        tname = name.split("::")[1]

        s = tname[len("test_"):]
        method = s[:s.find("_")]
        api = s[s.find("_") + 1:s.find("_for_fuzzing")].replace("__", "/").replace("9i9", "-")
        if '/' not in api:
            api = '/' + api
        if "call" not in onetest:
            continue
        # outcome can be pass/failed/skipped
        outcome = onetest["outcome"].lower()
        meta = onetest["metadata"][0]
        inobj = {"api": api, "method": method, "outcome": outcome, "attack": attack,
                 "severity": severity, "attackinfo": inainfo, "testinput": ""}

        if not outcome == "skipped":      # has a passed/failed outcome
            mdata = meta.split("::")
            inobj["resp"] = mdata[4]       # get the response code
            inobj["respmsg"] = mdata[6]
            # last one is the attack pattern file
            inobj["apatternfile"] = mdata[len(mdata)-1]
            if "stdout" in onetest["call"]:
                inputstr = parseStdoutForInput(onetest["call"]["stdout"])
                if inputstr:
                    inobj["testinput"] = inputstr
            if outcome == "failed":
                # sometimes the attack pattern file name is missing from the report
                if not inobj["apatternfile"]:
                    inobj["apatternfile"] = reportutil.patchAttackPatternFile(
                        attack)

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
            # if any api is found not to skipped, move that api from retest to no retest
            moveToNoRetest(rval, api)
            # tests sharing the same outcome is saved in a list
            if outcome in rval["tested"]:
                rval["tested"][outcome].append(inobj)
            else:
                rval["tested"][outcome] = [inobj]
    return rval


def iterateallspecs(inspeclist=[], inattacklist=[]):
    ainfo = {}
    thespeclist = inspeclist if inspeclist else runconfig.apispeclist
    theattacklist = inattacklist if inattacklist else runconfig.fuzzattacklist

    # summary test report filled in by sumPerSpec
    # failed test report by failedTestReport
    apilist_pri_report = {
        "total_tests": 0,
        "total_passed": 0,
        "total_failed": 0,
        "all_failed_apis": set(),
        "total_count": 0,
        "critical_count": 0,
        "high_count": 0,
        "medium_count": 0,
        "low_count": 0,
        "attack_category": {},
        "all_apis": set(),
        "failed_cc": 0,
        "failed_hc": 0,
        "failed_mc": 0,
        "failed_lc": 0,
    }

    for spec in thespeclist:
        spec = spec.lower()  # important, cannonical form of spec all lower case
        if not os.path.exists(resultrootn + spec):
            print(f"Failed to generate summary report: {resultrootn + spec} does not exist")
            return ""

        spec_report = {
            "apis_by_priority": {
                "p1": set(),
                "p2": set(),
                "p3": set(),
                "p4": set(),
            },
            "priority_count": {
                "p1_count": 0,
                "p2_count": 0,
                "p3_count": 0,
                "p4_count": 0
            },
            "total_tests_count": 0,
            "total_failed_count": 0,
            "total_passed_count": 0,
            "skipped_tests_count": 0,
            "all_spec_apis": set(),
            "all_failed_apis": set(),
        }
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

            originalr = resultrootn + spec + "/" + arname + "-report.json"

            if not os.path.exists(originalr):
                print(f"Cannot regenerate report for {spec}_{arname}, {originalr} does not exists")
                continue
            with open(originalr, encoding='utf-8') as f:
                areporti = json.load(f)
                f.close()

            originalhtml = resultrootn + spec + "/" + arname + ".html"
            if not os.path.exists(originalhtml):
                print(f"Cannot regenerate html report for {spec}_{arname}, {originalhtml} does not exists")
                continue
            tests = extractAPITests(a, severity, areporti, ainfo)

            # Get information for Failed Tests table
            apilist_pri_report[spec] = spec_report
            generate_test_report(apilist_pri_report, spec, tests)

    return apilist_pri_report


def get_most_frequent_attack(report_json):
    attack_category_json = report_json['attack_category']
    if not attack_category_json:
        return {}
    sorted(attack_category_json.items(), key=lambda item: 'count')
    res = list(attack_category_json.keys())[0]
    val = attack_category_json[res]
    freq_dict = {
        'attack': res,
        'failed_test': val['count'],
        'num_of_apis': len(val['p1_apis']) + len(val['p2_apis']) + len(val['p3_apis']) + len(val['p4_apis'])
    }
    return freq_dict


def get_attack_catogery_count(report_json):
    res = {}
    attack_category = report_json.get('attack_category', {})
    for key, value in attack_category.items():
        res[key] = {}
        res[key]['all_apis_count'] = len(value.get('all_apis', set()))
        if len(value.get('p1_apis', set())):
            res[key]['pri_count'] = len(value['p1_apis'])
            res[key]['priority'] = 'Critical'
        elif len(value.get('p2_apis', set())):
            res[key]['pri_count'] = len(value['p2_apis'])
            res[key]['priority'] = 'High'
        elif len(value.get('p3_apis', set())):
            res[key]['pri_count'] = len(value['p3_apis'])
            res[key]['priority'] = 'Medium'
        else:
            res[key]['pri_count'] = len(value['p4_apis'])
            res[key]['priority'] = 'Low'
    return res


def get_spec_details(report_json):
    res = {}
    api_count = 0
    apispeclist = apispecs.apispeclist
    for spec in apispeclist:
        res[spec] = report_json[spec]
        pri = report_json[spec]['apis_by_priority']
        api_count = len(pri['p1']) + len(pri['p2']) + len(pri['p3']) + len(pri['p4'])
        res[spec]['api_count'] = api_count
        res[spec]['count_by_api_priority'] = {
            'p1': len(pri['p1']),
            'p2': len(pri['p2']),
            'p3': len(pri['p3']),
            'p4': len(pri['p4'])
        }
        res[spec]['all_apis_count'] = len(report_json[spec]['all_spec_apis'])
        res[spec]['failed_apis_count'] = len(
            report_json[spec]['all_failed_apis'])
        api_details = {}
        for api_key, value in report_json.get(spec, {}).items():
            if '/' in api_key:
                values_list = []
                for _, info in value.items():
                    if info.get('pri', '') == 'p1':
                        info['pri'] = 1
                    elif info.get('pri', '') == 'p2':
                        info['pri'] = 2
                    elif info.get('pri', '') == 'p3':
                        info['pri'] = 3
                    else:
                        info['pri'] = 4
                    values_list.append(info)
                api_details[api_key] = values_list
        res[spec]['api_details'] = api_details
    return res


def generate_html_report(result_report_json, filename, customer_name='N/A'):
    frequent_attack = get_most_frequent_attack(result_report_json)
    category_counts = get_attack_catogery_count(result_report_json)
    spec_details = get_spec_details(result_report_json)

    # # old report
    # root = os.path.dirname(os.path.abspath(__file__))
    # templates_dir = os.path.join(root, 'templates')
    # env = Environment(loader=FileSystemLoader(templates_dir))
    # template = env.get_template('index.html')

    # old_report_dir = os.path.join(os.getcwd(), "old_report")
    # if os.path.exists(old_report_dir):
    #     shutil.rmtree(old_report_dir)
    # shutil.copytree(os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates/assets"),
    #                 os.path.join(old_report_dir, "assets"))
    # html_file = os.path.join(old_report_dir, filename)

    # with open(html_file, 'w', encoding='utf-8') as fh:
    #     fh.write(template.render(
    #         num_spec_files=len(apispecs.apispeclist),
    #         num_total_apis=len(result_report_json.get('all_apis')),
    #         num_dst_hosts=1,  # TODO: len(runconfig.dhostname)
    #         num_attack_categ=len(runconfig.fuzzattacklist),

    #         total_attack_vectors=result_report_json.get('total_count'),
    #         total_critical_av_count=result_report_json.get('critical_count'),
    #         total_high_av_count=result_report_json.get('high_count'),
    #         total_medium_av_count=result_report_json.get('medium_count'),
    #         total_low_av_count=result_report_json.get('low_count'),
    #         av_count_list=[result_report_json.get('critical_count'), result_report_json.get('high_count'),
    #                        result_report_json.get('medium_count'), result_report_json.get('low_count')],

    #         total_vul_apis=len(result_report_json.get('all_failed_apis')),

    #         total_tests=result_report_json.get('total_tests'),
    #         passed_count=result_report_json.get('total_passed'),
    #         failed_count=result_report_json.get('total_failed'),

    #         failed_critical_count=result_report_json.get('failed_cc'),
    #         failed_high_count=result_report_json.get('failed_hc'),
    #         failed_medium_count=result_report_json.get('failed_mc'),
    #         failed_low_count=result_report_json.get('failed_lc'),

    #         attack_category=category_counts,
    #         spec_details=spec_details,
    #         frequent_attack=frequent_attack
    #     ))

    # new report
    root = os.path.dirname(os.path.abspath(__file__))
    sfs = []
    for _, _, spec_file in os.walk(inspecdir):
        sfs.extend(spec_file)
        break

    new_templates_dir = os.path.join(root, 'new_templates')
    new_env = Environment(loader=FileSystemLoader(new_templates_dir))
    new_template = new_env.get_template('index.html')

    new_report_dir = os.path.join(os.getcwd(), "new_report")
    if os.path.exists(new_report_dir):
        shutil.rmtree(new_report_dir)
    shutil.copytree(new_templates_dir, new_report_dir)
    os.remove(os.path.join(new_report_dir, 'index.html'))
    html_file = os.path.join(new_report_dir, filename)

    with open(html_file, 'w', encoding='utf-8') as fh:
        fh.write(new_template.render(
            customer_name = customer_name,
            spec_filename = sfs[0] if len(sfs) == 1 else "specs.zip",
            created_time = datetime.now().strftime("%B %d, %Y %H:%M:%S"),
            num_spec_files=len(apispecs.apispeclist),
            num_total_apis=len(result_report_json.get('all_apis')),
            num_dst_hosts=1,  # TODO: len(runconfig.dhostname)
            num_attack_categ=len(runconfig.fuzzattacklist),


            total_attack_vectors=result_report_json.get('total_count'),
            total_critical_av_count=result_report_json.get('critical_count'),
            total_high_av_count=result_report_json.get('high_count'),
            total_medium_av_count=result_report_json.get('medium_count'),
            total_low_av_count=result_report_json.get('low_count'),
            av_count_list=[result_report_json.get('critical_count'), result_report_json.get('high_count'),
                           result_report_json.get('medium_count'), result_report_json.get('low_count')],

            total_vul_apis=len(result_report_json.get('all_failed_apis')),

            total_tests=result_report_json.get('total_tests'),
            passed_count=result_report_json.get('total_passed'),
            failed_count=result_report_json.get('total_failed'),

            failed_critical_count=result_report_json.get('failed_cc'),
            failed_high_count=result_report_json.get('failed_hc'),
            failed_medium_count=result_report_json.get('failed_mc'),
            failed_low_count=result_report_json.get('failed_lc'),

            attack_category=category_counts,

            spec_details=spec_details,
            frequent_attack=frequent_attack
        ))
    return


def main():
    print("\n\n")
    print(r"***************************************************************")
    print(r"**                                                           **")
    print(r"**  / ___| | ___  _   _  __| \ \   / /__  ___| |_ ___  _ __  **")
    print(r"** | |   | |/ _ \| | | |/ _` |\ \ / / _ \/ __| __/ _ \| '__| **")
    print(r"** | |___| | (_) | |_| | (_| | \ V /  __/ (__| || (_) | |    **")
    print(r"**  \____|_|\___/ \__,_|\__,_|  \_/ \___|\___|\__\___/|_|    **")
    print(r"**                                                           **")
    print(r"**      (c) Copyright 2018 & onward, CloudVector             **")
    print(r"**                                                           **")
    print(r"**  For license terms, refer to distribution info            **")
    print(r"***************************************************************")

    print("*****" * 20)
    print("CloudVector IAST - Report Generation plugin")
    print("*****" * 20)

    reportutil.init()
    result_report = iterateallspecs(apispeclist, runconfig.fuzzattacklist)
    generate_html_report(result_report, "sample.html")


if __name__ == "__main__":
    # execute only if run as a script
    main()
