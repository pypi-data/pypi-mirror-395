#
# A set of configuration values that can be
#  modified to fit customers environment
#

#
# Customer specific config
#  These are variables that most likely needed to be modified
#  to fit customers environment
#

import os
import sys

import yaml

inspecdir = os.path.join(os.getcwd(), "specs")  # default spec folder name, no /
dfuzzusrname = "cvbot@cloudvector.com"  # username to use for fuzzing
dcvconfig = os.path.join(os.getcwd(), "cv_config.yaml")  # config .yaml file for fuzzing
dspecnamec = "ob"  # default spec to use when running test, sample orangebank app shown here

# Default values: a set of default values in case nothing is customized.
dcviast_fuzz_type = "string-expansion"  # default fuzz type to use
dtestdirname = os.path.join(os.getcwd(), "tests")  # folder under which tests are saved
dfuzzdbdirname = "fuzzdb"  # folder under which fuzzdb is stroed

dsavedreportd = "savedreports"  # a folder under which reports are saved

dlogrespdname = "testrsps"  # a series of auto-generated files linked to from summary.html
dloginputdname = "testinputs"  # also auto generated input samples linked to from summary.html

dainfofname = dtestdirname + "/data/attack_info.json"  # where to find attack info

dresultdir = os.path.join(os.getcwd(), "results")  # folder to save impact test results, used for report gen
dperadir = "perattack"  # save perattack results
dperapidir = "perapi"  # save perapi test results, currently not used by test wrapper

savefailedtestreport = True  # save a copy of the failed tests that can be compared using reportcomp later
usecustomreportfname = True  # custom report name to use, by default a file failedtest.json is generated
customsavedreportfanme = "failedtest.json"  # specify the custom report name
ddiffrlogrspdirname = "testdiffrsps"  # when running reportcomp, just like testrsps, we use this dir to save resp file

# a csv file generated that can be used to show developers the findings, timestamp will be attached by default
dcsvreportfname = "fordev-sum"
dhtmlreportfname = "summary"  # name of the html file, timestamp will be attached
attachtimestamptoreport = True  # control whether to attach time stamp

apispeclist = []
# when running test, the number of patterns picked from each attack, set to 1 to avoid huge number of tests
dperattackvalueused = "1"


if os.path.exists('cv_config.yaml'):
    config = 'cv_config.yaml'
else:
    config = input("\n\tEnter the path to config file:")
if not config:
    print("Config is mandatory!")
    raise SystemExit
if not os.path.exists(config):
    print("Please check the path to Config!!")
    raise SystemExit

with open(config, encoding='utf-8') as fobj:
    ce_details = yaml.load(fobj, Loader=yaml.FullLoader)

dhostname = ce_details["execution_info"].get('dhostname', None)
usecustomlist = ce_details["execution_info"].get('usecustomlist', False)
# default max value to fuzz if running runonetest directly
dcviast_max_value_to_fuzz = ce_details["execution_info"].get('dcviast_max_value_to_fuzz', '1')

fuzzattacklist = [x.strip() for x in ce_details["execution_info"].get('fuzzattacklist', 'control-chars').split(',')]
fuzzattacklist = [x for  x in fuzzattacklist if x]
