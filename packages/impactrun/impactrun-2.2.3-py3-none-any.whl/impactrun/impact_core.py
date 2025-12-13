#!/usr/bin/python

# /***************************************************************\
# **                                                           **
# **  / ___| | ___  _   _  __| \ \   / /__  ___| |_ ___  _ __  **
# ** | |   | |/ _ \| | | |/ _` |\ \ / / _ \/ __| __/ _ \| '__| **
# ** | |___| | (_) | |_| | (_| | \ V /  __/ (__| || (_) | |    **
# **  \____|_|\___/ \__,_|\__,_|  \_/ \___|\___|\__\___/|_|    **
# **                                                           **
# **      (c) Copyright 2018 & onward, CloudVector             **
# **                                                           **
# **  For license terms, refer to distribution info            **
# \***************************************************************/

from base64 import encode
from collections.abc import Mapping
import datetime
import json
import os
import re
import shutil
import time
import getpass
import sys
from copy import deepcopy
from urllib.parse import urlparse

import prance
import pytest
import requests
import urllib3
import yaml
from cvapianalyser import CommunityEdition
from dictor import dictor
from jinja2 import Template
from impactrun import OpenApiSpecDiff

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HTTP_RESPONSE_CODES = ["100", "101", "200", "201", "202", "203", "204", "205", "206", "300", "301", "302", "303",
                       "304", "305", "306", "307", "400", "401", "402", "403", "404", "405", "406", "407", "408",
                       "409", "410", "411", "412", "413", "414", "415", "416 ", "417", "500", "501", "502", "503",
                       "504", "505"]

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
fuzz_words_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join('fuzzdb', 'attack'))
fuzz_types = [os.path.join("fuzzdb", "attack")]
supoorted_fuzz_types = [_ for _ in os.listdir(fuzz_words_dir) if "README" not in _]
ANOMOLY_THRESHOLD = 1.07142
RESERVED_PARAMETERS = ["$RESPONSE_ERROR", "$CV_EVENT_ID", "$headers"]
test_data_generation_summary = []


def update_nested_dict(key, value, dictionary):
    for k, v in dictionary.items():
        if k == key:
            dictionary[key] = value
        elif isinstance(v, dict):
            for result in update_nested_dict(key, value, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in update_nested_dict(key, value, d):
                        yield result


def keypaths(nested):
    for key, value in nested.items():
        if isinstance(value, Mapping):
            for subkey, subvalue in keypaths(value):
                yield [key] + subkey, subvalue
        else:
            yield [key], value


def key_lookup(key, var):
    paths = []
    for k, _ in keypaths(var):
        if key in k:
            if k:
                paths.append(".".join(k))
    return paths


class ImpactCore(object):
    """ Library for creating pytest functional and fuzz test cases for a given Open API spec """

    def __init__(self, APISpecOne, APISpecTwo, ce_host, ce_username, ce_password, config_file, cover_only_diff="n",
                 input_params_file=None, do_fuzz=False):
        custom_validations = None
        self.static_headers_from_cfg = {}
        self.cv_config = {}
        self.impact_to_auth_info = {}
        self.params_from_spec = {}
        self.respcodes_from_spec = {}
        self.params_details_from_spec = {}
        self.events_to_ignore = {}
        self.api_with_array_payload = []
        self.param_values_to_pick = {}
        self.response_schema_to_validate = {}
        self.headers_from_spec = {}
        if config_file:
            if os.path.exists(config_file):
                self.cv_config = self._parse_cv_config(config_file)
                ce_host = None
                ce_username = None
                if "ce_setup" in self.cv_config:
                    ce_host = self.cv_config["ce_setup"]["ce_host"]
                    ce_username = self.cv_config["ce_setup"]["ce_username"]
                custom_validations = self.cv_config.get("custom_validations", {})
                self.static_headers_from_cfg = self.cv_config.get("static_headers")
                if self.cv_config.get("authentication"):
                    self.impact_to_auth_info = self.cv_config.get("authentication")
                self.events_to_ignore = self.cv_config.get("headers_to_ignore_cv_events", {})
        if str(self.cv_config.get("generate_tests_for_response_codes", "Y")).lower() == "y":
            self.generate_tests_for_respcodes = True
        else:
            self.generate_tests_for_respcodes = False

        if APISpecOne:
            self.apispec_one_path = APISpecOne
        else:
            self.apispec_one_path = None
        self.apispec_two_path = APISpecTwo
        if ".txt" not in self.apispec_two_path:
            try:
                self.openapispec_obj = OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path)
            except prance.ValidationError:
                raise

        self.ceobj = None
        if ce_host:
            self.ceobj = CommunityEdition.CommunityEdition(ce_host, ce_username, ce_password)

        if not ce_host and self.apispec_two_path != "_tmpswp.txt" and ".txt" in self.apispec_two_path:
            print("Need either a valid OpenAPI Spec or Cloudvector controller to collect enough API data to create "
                  "tests!")
            raise SystemExit
        print("IMPACT - For APIShark events")
        # self.regenerate_traffic(self._get_changed_apis())
        self.input_json = {}
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if do_fuzz:
            if not os.path.exists((os.path.join(os.getcwd(), "fuzzdb"))):
                shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fuzzdb"),
                                os.path.join(os.getcwd(), "fuzzdb"))
        self.params_captured_in_traffic = {}
        self.prepped_spec = []
        if ".txt" not in self.apispec_two_path:
            changed_apis = self._get_changed_apis()
            if "changed" in changed_apis:
                apis_to_check = changed_apis["changed"]
            if "new" in changed_apis:
                apis_to_check.update(changed_apis["new"])
            if self.apispec_one_path:
                self.prepped_spec = self._prepare_spec_for_test_generation(self.apispec_two_path, changed_apis)
            else:
                self.prepped_spec = self._prepare_spec_for_test_generation(self.apispec_two_path)
        else:
            with open(self.apispec_two_path, encoding='utf-8') as fobj:
                apis_to_check = {str(_).replace("\n", ""): "" for _ in fobj.readlines()}
        self.input_json = {}
        self.assertions_map = {}

        cv_events = []
        if self.ceobj:
            for _ in ["2", "4", "5"]:
                print("Scanning Cloudvector dashboard for Status code " + str(_) + "**")
                cv_events += self._process_event_data(apis_to_check, filters_to_query={"http_rsp_status_code": _})
            print("done collecting events data from APIShark. (Total Events: " + str(len(cv_events)) + ")")

        cv_events += self.prepped_spec
        if cover_only_diff == "y":
            self._process_param_diff(apis_to_check, True)

        with open("tests/params_captured.json", "w+", encoding='utf-8') as fobj:
            json.dump(self.params_captured_in_traffic, fobj, indent=4)
        self.create_pyfixtures()
        if ce_host and not do_fuzz:
            self.create_pytest_methods(cv_events, custom_validations)
        if do_fuzz:
            self.create_fuzz_test_methods(cv_events)
        self.create_assertions(fuzzing=do_fuzz)

    def _load_input_from_files(self, input_file):
        input_vars = {}
        content = []
        if os.path.exists(input_file):
            with open(input_file, encoding='utf-8') as fobj:
                content = fobj.readlines()
        for each in content:
            if "=" in each:
                key, value = each.split("=")
                if "[" in value and "]" in value:
                    value = eval(value)
                else:
                    value = [value]
                input_vars[str(key).strip()] = value
        return input_vars

    def _prepare_spec_for_test_generation(self, input_spec, specific_apis=None):
        parsed_new_spec = self._get_spec_parsed(input_spec)
        params_info_from_spec = {}
        apis_from_spec = []
        if "servers" in parsed_new_spec:
            baseurl = parsed_new_spec["servers"][0]["url"]
            host = urlparse(baseurl).netloc
            if host:
                baseurl = baseurl.split(host)[1:]
        else:
            baseurl = parsed_new_spec.get("host", "") + parsed_new_spec.get("basePath", "")
            host = parsed_new_spec.get("host")
        if isinstance(baseurl, list):
            baseurl = baseurl[0]
        if parsed_new_spec:
            for api, info in parsed_new_spec["paths"].items():
                if specific_apis:
                    if api not in specific_apis:
                        continue
                if api not in self.respcodes_from_spec:
                    self.respcodes_from_spec[api] = {}
                for method, minfo in info.items():
                    if method in ["parameters"] or str(method).lower() not in ["get", "post", "put", "patch", "delete"]:
                        continue

                    x = {}
                    x["method"] = method.lower()
                    x["host"] = host
                    x["header"] = {}
                    x["params"] = []
                    x["detailed_params"] = {}
                    x["body"] = {}
                    x["rsp_body"] = {}
                    x["url"] = ""
                    x["api_queried"] = api
                    x["http-req-url"] = api
                    if baseurl:
                        x["url"] = baseurl + api
                    if host:
                        x["url"] = host + baseurl + api
                    x["url"] = baseurl + api
                    base_url_and_api = api  # x["url"]
                    if base_url_and_api not in params_info_from_spec:
                        params_info_from_spec[base_url_and_api] = {}
                    if method not in params_info_from_spec[base_url_and_api]:
                        params_info_from_spec[base_url_and_api][method] = {"required": [], "optional": []}

                    if api not in self.param_values_to_pick:
                        self.param_values_to_pick[api] = {"200": {}}
                    if method not in self.param_values_to_pick[api]["200"]:
                        self.param_values_to_pick[api]["200"][method] = {}

                    if api not in self.response_schema_to_validate:
                        self.response_schema_to_validate[api] = {"200": {}}
                    if method not in self.response_schema_to_validate[api]["200"]:
                        self.response_schema_to_validate[api]["200"][method] = {}
                    for ky in key_lookup("schema", minfo):
                        if "200" in ky and ".required" in ky:
                            self.response_schema_to_validate[api]["200"][method] = dictor(minfo, ky)

                    try:
                        for y in key_lookup("enum", minfo):
                            if str(y).startswith("response"):
                                continue
                            enum_name = y
                            if "enum" in enum_name:
                                enum_name = enum_name.split(".")
                                pos = enum_name.index("enum")
                                enum_type = ""
                                if enum_name[pos - 1] == "items":
                                    enum_type = []
                                    pos = pos - 2
                                else:
                                    pos = pos - 1
                                enum_name = enum_name[pos]
                            if isinstance(enum_type, str):
                                val = "::".join(dictor(minfo, y))
                            else:
                                val = dictor(minfo, y)
                            self.param_values_to_pick[api]["200"][method][enum_name] = val
                    except Exception:
                        pass

                    for _ in x["url"].split("/"):
                        if "{" in _ and "}" in _:
                            _ = str(_).replace("{", "").replace("}", "")
                            x["params"].append(_)
                    if x["http-req-url"] not in self.respcodes_from_spec:
                        self.respcodes_from_spec[x["http-req-url"]] = {}
                    self.respcodes_from_spec[x["http-req-url"]][method] = list(minfo.get("responses").keys())
                    x["url"] = x["url"].replace("{", "{{").replace("}", "}}")

                    for _ in minfo.get("parameters", []):
                        try:
                            for ky in key_lookup("schema", _):
                                if "200" in ky and ".required" in ky:
                                    self.response_schema_to_validate[api]["200"][method] = dictor(_, ky)
                        except Exception:
                            pass

                        try:
                            for y in key_lookup("enum", _):
                                if str(y).startswith("response"):
                                    continue
                                enum_name = _.get("name")

                                if "enum" in enum_name:
                                    enum_name = enum_name.split(".")
                                    pos = enum_name.index("enum")
                                    enum_type = ""
                                    if enum_name[pos - 1] == "items":
                                        enum_type = []
                                        pos = pos - 2
                                    else:
                                        pos = pos - 1
                                    enum_name = enum_name[pos]
                                if isinstance(enum_type, str):
                                    val = "::".join(dictor(_, y))
                                else:
                                    val = dictor(_, y)
                                self.param_values_to_pick[api]["200"][method][enum_name] = val
                        except Exception:
                            pass
                        if isinstance(_, list):
                            self.api_with_array_payload.append(x["url"])
                            self.api_with_array_payload.append(x["http-req-url"])
                            x["params"].append([])
                            params_details_from_spec = {}
                            for each in _:
                                if each.get("required", True):
                                    if isinstance(each.get("required"), bool):
                                        params_info_from_spec[base_url_and_api][method]["required"].append(each.get("name"))
                                    else:
                                        params_info_from_spec[base_url_and_api][method]["required"] += each.get("required",
                                                                                                                [])
                                else:
                                    params_info_from_spec[base_url_and_api][method]["optional"].append(each.get("name"))
                                params_info_from_spec[base_url_and_api][method]["required"] = list(
                                    set(params_info_from_spec[base_url_and_api][method]["required"]))
                                params_info_from_spec[base_url_and_api][method]["optional"] = list(
                                    set(params_info_from_spec[base_url_and_api][method]["optional"]))

                                if each.get("in") == "header":
                                    x["header"][each.get("name")] = ""
                                    u = api
                                    u = u.split("?")[0]
                                    u = u.replace("{{", "").replace("}}", "").replace("{", "").replace("}", "")
                                    if u not in self.headers_from_spec:
                                        self.headers_from_spec[u] = {}
                                    if method not in self.headers_from_spec[u]:
                                        self.headers_from_spec[u][method] = []
                                    if each.get("name") not in self.headers_from_spec[u][method]:
                                        self.headers_from_spec[u][method].append(each.get("name"))

                                    u = x["url"]
                                    u = u.split("?")[0]
                                    u = u.replace("{{", "").replace("}}", "").replace("{", "").replace("}", "")
                                    if u not in self.headers_from_spec:
                                        self.headers_from_spec[u] = {}
                                    if method not in self.headers_from_spec[u]:
                                        self.headers_from_spec[u][method] = []
                                    if each.get("name") not in self.headers_from_spec[u][method]:
                                        self.headers_from_spec[u][method].append(each.get("name"))
                                elif each.get("in") == "query":
                                    if "?" not in x["url"]:
                                        x["url"] += ("?" + each.get("name") + "={{" +
                                                    each.get("name").replace(".", "_") + "}}")
                                    else:
                                        x["url"] += ("&" + each.get("name") + "={{" +
                                                    each.get("name").replace(".", "_") + "}}")
                                    x["params"][0].append(each.get("name"))
                                else:
                                    if each.get("name"):
                                        x["params"][0].append(each.get("name"))
                                        x["body"][each.get("name")] = ""

                                if each.get("value"):
                                    params_details_from_spec[str(each.get("name"))] = each.get("value")
                            if api not in self.params_from_spec:
                                self.params_from_spec[api] = {}
                            self.params_from_spec[api][method] = [{_: [] for _ in x["params"][0]}]
                            self.params_details_from_spec = [params_details_from_spec]
                        else:
                            params_details_from_spec = {}
                            if _.get("required", True):
                                if isinstance(_.get("required"), bool):
                                    params_info_from_spec[base_url_and_api][method]["required"].append(_.get("name"))
                                else:
                                    params_info_from_spec[base_url_and_api][method]["required"] += _.get("required", [])
                            else:
                                params_info_from_spec[base_url_and_api][method]["optional"].append(_.get("name"))
                            params_info_from_spec[base_url_and_api][method]["required"] = list(
                                set(params_info_from_spec[base_url_and_api][method]["required"]))
                            params_info_from_spec[base_url_and_api][method]["optional"] = list(
                                set(params_info_from_spec[base_url_and_api][method]["optional"]))

                            if _.get("in") == "header":
                                x["header"][_.get("name")] = ""
                                u = api
                                u = u.split("?")[0]
                                u = u.replace("{{", "").replace("}}", "").replace("{", "").replace("}", "")
                                if u not in self.headers_from_spec:
                                    self.headers_from_spec[u] = {}
                                if method not in self.headers_from_spec[u]:
                                    self.headers_from_spec[u][method] = []
                                if _.get("name") not in self.headers_from_spec[u][method]:
                                    self.headers_from_spec[u][method].append(_.get("name"))

                                u = x["url"]
                                u = u.split("?")[0]
                                u = u.replace("{{", "").replace("}}", "").replace("{", "").replace("}", "")
                                if u not in self.headers_from_spec:
                                    self.headers_from_spec[u] = {}
                                if method not in self.headers_from_spec[u]:
                                    self.headers_from_spec[u][method] = []
                                if _.get("name") not in self.headers_from_spec[u][method]:
                                    self.headers_from_spec[u][method].append(_.get("name"))
                            elif _.get("in") == "query":
                                if "?" not in x["url"]:
                                    x["url"] += "?" + _.get("name") + "={{" + _.get("name").replace(".", "_") + "}}"
                                else:
                                    x["url"] += "&" + _.get("name") + "={{" + _.get("name").replace(".", "_") + "}}"
                                x["params"].append(_.get("name"))
                            else:
                                if _.get("name"):
                                    x["params"].append(_.get("name"))
                                    x["body"][_.get("name")] = ""
                            if _.get("value"):
                                params_details_from_spec[str(_.get("name"))] = _.get("value")
                            if api not in self.params_from_spec:
                                self.params_from_spec[api] = {}
                            self.params_from_spec[api][method] = {_: [] for _ in x["params"]}
                            self.params_details_from_spec = [params_details_from_spec]
                    apis_from_spec.append([x, None])

        if not os.path.exists("tests/data"):
            os.mkdir("tests/data")
        if os.path.exists("tests/data/params_info_from_spec.json"):
            os.remove("tests/data/params_info_from_spec.json")
        if os.path.exists("tests/data/param_values_to_pick.json"):
            os.remove("tests/data/param_values_to_pick.json")
        if os.path.exists("tests/data/resp_to_validate.json"):
            os.remove("tests/data/resp_to_validate.json")
        if os.path.exists("tests/data/headers_from_spec.json"):
            os.remove("tests/data/headers_from_spec.json")

        params_info_from_spec_json_file = os.path.join(os.path.join("tests", "data"), "params_info_from_spec.json")
        with open(params_info_from_spec_json_file, "w+", encoding='utf-8') as _file:
            json.dump(params_info_from_spec, _file)

        param_values_to_pick_json_file = os.path.join(os.path.join("tests", "data"), "param_values_to_pick.json")
        with open(param_values_to_pick_json_file, "w+", encoding='utf-8') as _file:
            json.dump(self.param_values_to_pick, _file)

        resp_to_validate_json_file = os.path.join(os.path.join("tests", "data"), "resp_to_validate.json")
        with open(resp_to_validate_json_file, "w+", encoding='utf-8') as _file:
            json.dump(self.response_schema_to_validate, _file)

        headers_from_spec_json_file = os.path.join(os.path.join("tests", "data"), "headers_from_spec.json")
        with open(headers_from_spec_json_file, "w+", encoding='utf-8') as _file:
            json.dump(self.headers_from_spec, _file)

        self.api_with_array_payload = list(set(self.api_with_array_payload))
        return apis_from_spec

    def _parse_cv_config(self, path):
        with open(path, encoding='utf-8') as fobj:
            config = yaml.load(fobj, Loader=yaml.FullLoader)
        return config

    def _scan_input_spec(self, input_path):
        input_spec = self._get_spec_parsed(input_path)
        if "servers" in input_spec:
            baseurl = input_spec["servers"][0]["url"]
            host = urlparse(baseurl).netloc
            if host:
                baseurl = baseurl.split(host)[1:]

        else:
            baseurl = input_spec.get("host", "") + input_spec.get("basePath", "")
            host = input_spec.get("host")
        if isinstance(baseurl, list):
            baseurl = baseurl[0]
        if baseurl == "/":
            baseurl = ""
        params_info = {}
        if input_spec:
            for api, info in input_spec["paths"].items():
                api = baseurl + api
                if api not in params_info:
                    params_info[api] = {}
                for method, paraminfo in info.items():
                    params = []
                    if method not in params_info[api]:
                        params_info[api][method] = []
                    for each in paraminfo.get("parameters", []):
                        if each.get("in") != "header":
                            params.append(each.get("name"))
                    params_info[api][method] = params
            
        return params_info

    def _get_spec_parsed(self, input_path):
        return self.openapispec_obj.scan_input_spec(self.openapispec_obj.parse_spec(input_path))

    def _get_changed_apis(self):
        return self.openapispec_obj.diff

    def _process_param_diff(self, changed_apis, only_diff):
        if only_diff:
            self.params_captured_in_traffic = {}
        for api, info in changed_apis.items():
            iflag = True
            for method, params in info.items():
                if only_diff and iflag:
                    self.params_captured_in_traffic = {api: {"200": {str(method).lower(): []}}}
                    iflag = False
                all_params = {}
                for param in params:
                    if api in self.params_captured_in_traffic:
                        if only_diff and iflag:
                            all_params[param.get("name")] = ""
                self.params_captured_in_traffic[api]["200"][str(method).lower()].append(all_params)

    def _get_fuzz_details(self, fuzz_type):
        fuzz_values = []
        fuzz_values.append({"path": 'os.path.join("fuzzdb","attack")',
                            "fuzz_type": fuzz_type})
        return fuzz_values

    def _get_hosts_input(self, hosts):
        print("Select the host to create the tests for:")
        for _ in range(1, len(hosts) + 1):
            print(str(_) + " - " + str(hosts[_]))
        pos = input("Select the host : ")
        return hosts[int(pos) - 1]

    def create_pyfixtures(self):
        print("creating Pytest fixtures")
        with open(os.path.join(templates_dir, 'conftest.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())
        if not os.path.exists("tests"):
            os.mkdir("tests")
        auth_api = "/xyz"
        auth_api_headers = {}
        auth_api_payload = {}
        auth_api_response_key = ""
        auth_prefix = ""
        auth_inputs = ["host"]
        if self.impact_to_auth_info:
            auth_api = self.impact_to_auth_info.get("api_url")
            auth_api_headers = self.impact_to_auth_info.get("headers", {})
            auth_api_payload = self.impact_to_auth_info.get("payload", {})
            for k, v in auth_api_headers.items():
                template_found = re.search(r"\[\'([A-Za-z0-9_]+)\'\]", str(v))
                if template_found:
                    auth_inputs.append(template_found.group(1))
                    auth_api_headers[k] = auth_inputs[-1]
            for k, v in auth_api_payload.items():
                template_found = re.search(r"\[\'([A-Za-z0-9_]+)\'\]", str(v))
                if template_found:
                    auth_inputs.append(template_found.group(1))
                    auth_api_payload[k] = auth_inputs[-1]
            auth_api_response_key = self.impact_to_auth_info.get("response_key", "")
            auth_type = self.impact_to_auth_info.get("type", "basic").lower()
            if auth_type == "basic":
                auth_prefix = ""
            elif auth_type == "bearer":
                auth_prefix = "Bearer"
            else:
                auth_prefix = auth_type
        nested_params = {}
        more_params = []

        if isinstance(self.params_details_from_spec, dict):
            for param, info in self.params_details_from_spec.items():
                _params = []
                try:
                    if isinstance(info, dict):
                        for k, v in keypaths(info):
                            more_params.append(k[-1])
                            _params.append(k[-1])
                    elif isinstance(info, list):
                        for each in info:
                            for k, v in keypaths(each):
                                more_params.append(k[-1])
                                _params.append(k[-1])
                except Exception:
                    pass
                if _params:
                    nested_params[param] = _params
                more_params = list(set(more_params))
            for k, v in keypaths(self.params_details_from_spec):
                if isinstance(v, list):
                    for each in v:
                        if isinstance(each, dict):
                            for a, b in keypaths(each):
                                list(update_nested_dict(a[-1], "$_.get('" + a[-1] + "')$", each))
                        else:
                            list(update_nested_dict(k[-1], "$_.get('" + k[-1] + "')$", self.params_details_from_spec))
                elif isinstance(v, dict):
                    list(update_nested_dict(a[-1], "$_.get('" + a[-1] + "')$", v))
        elif isinstance(self.params_details_from_spec, list):
            for each in self.params_details_from_spec:
                for param, info in each.items():
                    _params = []
                    if isinstance(info, dict):
                        for k, v in keypaths(info):
                            more_params.append(k[-1])
                            _params.append(k[-1])
                    elif isinstance(info, list):
                        for each in info:
                            if isinstance(each, dict):
                                for k, v in keypaths(each):
                                    more_params.append(k[-1])
                                    _params.append(k[-1])
                    if _params:
                        nested_params[param] = _params
                    more_params = list(set(more_params))

                if isinstance(each, dict):
                    for k, v in keypaths(each):
                        if isinstance(v, list):
                            for e in v:
                                if isinstance(e, dict):
                                    for a, b in keypaths(e):
                                        list(update_nested_dict(a[-1], "$_.get('" + a[-1] + "')$", e))
                                else:
                                    list(update_nested_dict(k[-1], "$_.get('" + k[-1] + "')$",
                                                            each))
                        elif isinstance(v, dict):
                            list(update_nested_dict(k[-1], "$_.get('" + k[-1] + "')$", v))
                        else:
                            each[k[-1]] = "$" + k[-1] + "$"
            nested_params = [nested_params]

        params_for_fixtures = []
        for api, info in self.params_captured_in_traffic.items():
            for rspcode, minfo in info.items():
                for method, plist in minfo.items():
                    for each in plist:
                        if isinstance(each, str):
                            if each not in params_for_fixtures and each not in RESERVED_PARAMETERS:
                                params_for_fixtures.append(each)
                        elif isinstance(each, dict):
                            for _ in each.keys():
                                if _ not in params_for_fixtures and _ not in RESERVED_PARAMETERS:
                                    params_for_fixtures.append(_)

        for api, info in self.params_from_spec.items():
            for method, params_info in info.items():
                for param in params_info:
                    if isinstance(param, dict):
                        for _ in param.keys():
                            if _ not in params_for_fixtures and _ not in RESERVED_PARAMETERS:
                                params_for_fixtures.append(_)
                    elif isinstance(param, str):
                        if param not in params_for_fixtures and param not in RESERVED_PARAMETERS:
                            params_for_fixtures.append(param)

        with open("tests/conftest.py", 'w+', encoding='utf-8') as fh:
            fh.write(template.render(api_info=list(set(params_for_fixtures)),
                                     api_detailed_info=self.params_details_from_spec,
                                     nested_params=nested_params, AUTH_API=auth_api, more_params=more_params,
                                     AUTH_API_HEADERS=auth_api_headers, AUTH_API_PAYLOAD=json.dumps(auth_api_payload),
                                     AUTH_RESP_KEY=auth_api_response_key, AUTH_INPUTS=auth_inputs,
                                     TOKEN_PREFIX=auth_prefix))

        with open(os.path.join(templates_dir, 'cvutils.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())

        with open("tests/cvutils.py", 'w+', encoding='utf-8') as fh:
            fh.write(template.render(fuzz_supported=supoorted_fuzz_types))

        print("done creating pytest fixtures (conftest.py)")

    def create_fuzzfixtures(self):
        print("creating fuzz-lightyear fixtures")
        with open(os.path.join(templates_dir, 'fuzz_fixtures.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())
        code = template.render(api_info=self.params_captured_in_traffic)
        print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        with open("tests/fuzz_fixtures.py", 'w+', encoding='utf-8') as fh:
            fh.write(template.render(api_info=self.params_captured_in_traffic))
        print("done creating fuzz-lightyear fixtures (fuzz_fixtures.py)")

    def create_assertions(self, fuzzing):
        print("creating assertion methods")
        with open(os.path.join(templates_dir, 'assertions.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if fuzzing:
            threshold = ANOMOLY_THRESHOLD
        else:
            threshold = 0
        with open("tests/assertions.py", 'w+', encoding='utf-8') as fh:
            fh.write(template.render(assertions=self.assertions_map, ANOMALY_THRESHOLD=threshold))
        print("done creating assertions (assertions.py)")

    def _create_assertions_map(self, url, params, req_payload, resp_payload):
        assertions_map = {}
        if url not in self.assertions_map:
            url = \
                url.replace("//", "/").replace("/", "__").replace("{", "").replace("}", "").replace(" ", "").split("?")[
                    0]
            if url.startswith("__"):
                url = "_" + url[2:]
            self.assertions_map[url] = {}
        if None in params:
            params.remove(None)

        for param in params:
            paths_in_req = key_lookup(param, req_payload)
            paths_in_rsp = key_lookup(param, resp_payload)

            paths_in_req = [_ for _ in paths_in_req if _ != ""]
            paths_in_rsp = [_ for _ in paths_in_rsp if _ != ""]

            if paths_in_req and paths_in_rsp:
                assertions_map.update({
                    param:
                        {
                            "req": paths_in_req,
                            "resp": paths_in_rsp
                        }
                })
        self.assertions_map[url].update(assertions_map)

    def _create_custom_validations(self, params_to_validate, info):
        validations = []
        for method, minfo in info.items():
            actual_params = minfo.get("params")
            for param in actual_params:
                if param in params_to_validate:
                    for condition, to_check in params_to_validate[param].items():
                        if condition == "missing":
                            validations.append([str(param) + "_missing", str(param) + "_arg = ''", to_check])
                        elif condition == "invalid":
                            validations.append([str(param) + "_invalid", str(param) + "_arg = 'iamdummy'", to_check])
        return validations

    def _process_cv_events(self, cv_events):
        apis_to_be_tested = {}
        host_url = ""

        try:
            new_spec_info = self._scan_input_spec(self.apispec_two_path)
            hosts = new_spec_info.get("servers", {}).get("url", [])
        except AttributeError:
            new_spec_info = {}
            hosts = []

        for _ in cv_events:
            event = _[0]
            if _[1]:
                if int(_[1]["attributes"]["http_rsp_status_code"]) not in range(200, 299):
                    continue
            if event["url"]:
                if event["host"]:
                    host_url = str(event["host"]).lower()
                    hosts.append(host_url)
                else:
                    host_url = ""
                without_dot_api = (str(event["http-req-url"]).lstrip("/").replace("/", "__")
                       .replace(" ", "").replace(host_url, "").split("?")[0])
                api = (str(event["http-req-url"]).lstrip("/").replace(".", "dot").replace("/", "__")
                       .replace(" ", "").replace(host_url, "").split("?")[0])

                if event["api_queried"] in api and len(api.split(event["api_queried"])) > 1:
                    continue

                if api not in apis_to_be_tested:
                    apis_to_be_tested[api] = {}
                method = event["method"].lower()

                if method not in apis_to_be_tested[api]:
                    apis_to_be_tested[api][method] = {}
                if self.static_headers_from_cfg:
                    for k, v in self.static_headers_from_cfg.items():
                        event["header"][k] = str(v)
                if "header" not in apis_to_be_tested[api][method]:
                    apis_to_be_tested[api][method]["header"] = {}
                apis_to_be_tested[api][method]["header"].update(event["header"])
                header_from_event = deepcopy(apis_to_be_tested[api][method]["header"])
                for key in header_from_event:
                    apiname = ("/" + without_dot_api.replace("{", "").replace("}", "")
                               .replace("{{", "").replace("}}", "").replace("__", "/"))
                    if api in self.headers_from_spec and method in self.headers_from_spec[apiname] and key not in self.headers_from_spec[apiname][method]:
                        header_from_event[key] = "TBD"
                header_from_event = {k: v for k, v in header_from_event.items() if v != "TBD"}
                apis_to_be_tested[api][method]["header"] = header_from_event
                # apis_to_be_tested[api][method]["header"].update(header_from_event)
                apis_to_be_tested[api][method]["url"] = event["url"].replace(host_url, "")
                apis_to_be_tested[api][method]["url_from_spec"] = event["api_queried"]

                if apis_to_be_tested[api][method].get("params"):
                    known_params = apis_to_be_tested[api][method].get("params")
                else:
                    known_params = []

                if apis_to_be_tested[api][method].get("params"):
                    apis_to_be_tested[api][method]["params"] += new_spec_info.get(
                        str(event["http-req-url"]).replace("//", "/"), {}).get(method, [])
                else:
                    apis_to_be_tested[api][method]["params"] = new_spec_info.get(
                        str(event["http-req-url"]).replace("//", "/"), {}).get(method, [])

                params_in_traffic = event.get("body", {}).keys()

                for _ in params_in_traffic:
                    if _ not in apis_to_be_tested[api][method]["params"]:
                        apis_to_be_tested[api][method]["params"].append(_)

                if apis_to_be_tested[api][method]["params"] is None:
                    apis_to_be_tested[api][method]["params"] = []

                apis_to_be_tested[api][method]["params"] = list(set(apis_to_be_tested[api][method]["params"]))
                apis_to_be_tested[api][method]["params"].append("host")
                apis_to_be_tested[api][method]["params"].append("url_prefix")
                apis_to_be_tested[api][method]["params"].append("access_token")
                apis_to_be_tested[api][method]["params"] = list(set(apis_to_be_tested[api][method]["params"]))

                self._create_assertions_map(event["http-req-url"].replace(host_url, ""),
                                            apis_to_be_tested[api][method]["params"], event["body"],
                                            event["rsp_body"])
        return host_url, apis_to_be_tested

    def create_pytest_methods(self, cv_events, custom_validations):
        params_for_custom_validations = custom_validations.get("request_params")

        files_created = set()
        print("creating Pytest test methods")

        with open(os.path.join(templates_dir, 'test_api.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())

        host_url, apis_to_be_tested = self._process_cv_events(cv_events)

        for k, v in apis_to_be_tested.items():
            for i, j in v.items():
                if len([_ for _ in j.get("params", []) if _ not in ['url_prefix', 'headers_from_cv_events',
                                                                    'host', 'access_token']]) <= 0:
                    apis_to_be_tested[k][i]["params"].append("headers_from_cv_events")
            # code = template.render(api_info=apis_to_be_tested[k], api_name=k, host_url=host_url)
            filename = str(k).replace("/", "_").replace("{", "").replace("}", "")
            if not os.path.exists("tests"):
                os.mkdir("tests")
            if params_for_custom_validations:
                extra_validations = self._create_custom_validations(params_for_custom_validations,
                                                                    apis_to_be_tested[k])
            else:
                extra_validations = []

            api_name = "/" + str(k.replace("__", "_").replace("_", "/"))
            if self.generate_tests_for_respcodes:
                status_codes_for_api = self.respcodes_from_spec.get(api_name, {})
            else:
                status_codes_for_api = {}
            with open("tests/test_" + str(filename) + ".py", 'w+', encoding='utf-8') as fh:
                fh.write(template.render(apis_metadata=apis_to_be_tested[k], api_name=k, host_url=host_url,
                                         custom_validations=extra_validations, STATUS_CODES=status_codes_for_api,
                                         TEST_MANAGEMENT=self.cv_config.get("upload_result_to"),
                                         api_response_schema=self.response_schema_to_validate[api_name].get("200", {}),
                                         apis_with_array_payloads=self.api_with_array_payload))
            files_created.add("test_" + str(filename))
        print("done creating pytest methods: " + str(files_created))

    def create_fuzz_test_methods(self, cv_events):
        files_created = set()
        print("creating Pytest test methods for fuzzing")
        host_url, apis_to_be_tested = self._process_cv_events(cv_events)

        statefull = 0
        if not self.ceobj:
            statefull = 0
        else:
            if os.environ.get("IMPACT_STATEFUL_FUZZ", "3") in ["0", "1"]:
                statefull = int(os.environ.get("IMPACT_STATEFUL_FUZZ"))

        if os.path.exists("tests/data"):
            shutil.rmtree("tests/data")
        # if os.path.exists("tests/data/"):
        #     os.remove("tests/data/")
        shutil.copytree(os.path.join(templates_dir, "data"), "tests/data/")
        for type in fuzz_types:
            fuzzing_details = self._get_fuzz_details(type)
            with open(os.path.join(templates_dir, 'fuzz_test.j2'), encoding='utf-8') as file_:
                template = Template(file_.read())
            for k, v in apis_to_be_tested.items():
                for method, info in v.items():
                    if not info["params"]:
                        continue
                filename = str(k).replace("/", "_").replace("{", "").replace("}", "") + "_for_fuzzing"
                #filename = str(k).replace("/", "_").replace("{", "").replace("}", "") + "_for_fuzzing"
                #filename = filename.strip
                if not os.path.exists("tests"):
                    os.mkdir("tests")

                with open("tests/test_" + str(filename) + ".py", 'w+', encoding='utf-8') as fh:
                    fh.write(template.render(apis_metadata=apis_to_be_tested[k], api_name=k, host_url=host_url,
                                             fuzzing_details=fuzzing_details, fuzz_type=str(type),
                                             stateful_fuzz=statefull, fuzz_supported=supoorted_fuzz_types))
                files_created.add("test_" + str(filename))

        print("done creating pytest methods for fuzzing: " + str(files_created))

    def validate_pycode_for_syntax(self, code):
        code = str(code).replace(" ", "%20").replace("\n", "%0")
        headers = {
            'authority': 'extendsclass.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://extendsclass.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://extendsclass.com/python-tester.html',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '__gads=ID=da612839d6fc1303:T=1590622404:S=ALNI_MaEgA77keI5Spn5CckEF15zogbT6A; '
                      'PHPSESSID=123dabd5a795c756d1a5f45837f3217d; SERVERID100401=15211|Xs75G|Xs74y',
        }

        data = {
            '$source': code
        }
        response = requests.post('https://extendsclass.com/python-tester-source', headers=headers, data=data)
        print(response.text)
        return response.json()

    def _process_event_data(self, apis_to_check=[], filters_to_query={}):
        print("collecting events data from APIShark")
        cv_requests = []
        events = self.ceobj.get_all_raw_events(apis_to_check, **filters_to_query)
        processed_events = 0
        for event in events:
            for k, v in self.events_to_ignore.items():
                if event["attributes"]["event_json"].get("http-req-header-" + str(k), "") == str(v):
                    print("ignoring the event as it contains " + str(k) + " = " + str(v))
                    continue
            if "http-req-header-Cv-Fuzzed-Event" in event["attributes"]["event_json"]:
                continue
            if int(str(event["attributes"]["http_rsp_status_code"]).split(" ")[0]) == 0:
                continue
            # if apis_to_check:
            #     iflag = False
            #     for _ in apis_to_check:
            #         if str(_).lower() in str(event["attributes"]["http_path"]).lower():
            #             iflag = True
            #             params_to_add = apis_to_check[_]
            #         if iflag:
            #             break
            #
            #     if not iflag:
            #         continue

            request = {"url": str(event["attributes"]["http_path"]),
                       "method": str(event["attributes"]["http_method"]).lower()}
            header = {}
            req_params_found = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-req-header" in k:
                    if k == "http-req-headers-params":
                        continue
                    header[str(k).replace("http-req-header-", "")] = v
                if k in ["http-req-body-params", "http-req-query-params"]:
                    if v:
                        for param in v:
                            req_params_found[param] = {}

            for param in req_params_found:
                if "http-req-body-" + str(param) in event["attributes"]["event_json"]:
                    req_params_found[param] = event["attributes"]["event_json"]["http-req-body-" + str(param)]
                elif "http-req-query-" + str(param) in event["attributes"]["event_json"]:
                    req_params_found[param] = event["attributes"]["event_json"]["http-req-query-" + str(param)]

            rsp_params_found = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-rsp-header" in k:
                    if k == "http-rsp-headers-params":
                        continue
                    header[str(k).replace("http-rsp-header-", "")] = v
                if k in ["http-rsp-body-params", "http-rsp-query-params"]:
                    if v:
                        for param in v:
                            rsp_params_found[param] = {}

            for param in rsp_params_found:
                if "http-rsp-body-" + str(param) in event["attributes"]["event_json"]:
                    rsp_params_found[param] = event["attributes"]["event_json"]["http-rsp-body-" + str(param)]
                elif "http-rsp-query-" + str(param) in event["attributes"]["event_json"]:
                    rsp_params_found[param] = event["attributes"]["event_json"]["http-rsp-query-" + str(param)]

            request["host"] = event["attributes"]["event_json"]["http-req-host"]
            request["http-req-url"] = event.get("api_queried", event["attributes"]["event_json"]["http-req-url"])
            request["api_queried"] = event.get("api_queried")
            request["header"] = header
            request["body"] = req_params_found
            request["rsp_body"] = rsp_params_found
            request["method"] = str(event["attributes"].get("http_method")).lower()
            request["rsp_code"] = str(event["attributes"]["http_rsp_status_code"]).split(" ")[0]
            if request["rsp_code"] not in [200, 201]:
                request["rsp_error"] = event["attributes"]["event_json"].get("http-rsp-body-error")
            url = event["attributes"]["http_path"]

            if self.static_headers_from_cfg:
                for k, v in self.static_headers_from_cfg.items():
                    request["header"][k] = str(v)
            api_queried = event.get("api_queried")
            url = api_queried
            # if api_queried:
            #     if "{" in api_queried:
            #         api_queried = api_queried.split("/")
            #         api_queried.remove("")
            #         event_url = url.split("/")
            #         event_url.remove("")
            #         print(">>>>", api_queried, event_url)
            #         if api_queried[0] in event_url:
            #             start_index = event_url.index(api_queried[0])
            #             for p in api_queried[1:]:
            #                 if p.startswith("{"):
            #                     req_params_found[p.replace("{","").replace("}","")] = event_url[start_index + 1]
            #                 start_index += 1
            #             url = "/".join(event_url[:event_url.index(api_queried[0])]) + event.get("api_queried")
            #             if not url.startswith("/"):
            #                 url = "/" + url
            #             request["http-req-url"] = url
            #             url = url.replace("{","").replace("}","")
            if str(url) not in self.params_captured_in_traffic:
                self.params_captured_in_traffic[url] = {}
            if str(request["rsp_code"]) not in self.params_captured_in_traffic[url]:
                self.params_captured_in_traffic[url].update({str(request["rsp_code"]): {}})
            if str(request["method"]) not in self.params_captured_in_traffic[url][request["rsp_code"]]:
                self.params_captured_in_traffic[url][request["rsp_code"]].update({str(request["method"]): []})
            params_found = {}
            for param, value in req_params_found.items():
                params_found[param] = value
            params_found["header"] = header
            params_found["header"]["Authorization"] = ""
            if params_found:
                if request["rsp_code"] not in [200, 201]:
                    params_found["$RESPONSE_ERROR"] = request.get("rsp_error")
                    params_found["$CV_EVENT_ID"] = "CV-EVENT-" + str(event["id"])
                self.params_captured_in_traffic[str(url)][request["rsp_code"]][request["method"]].append(params_found)
            cv_requests.append([request, event])
            processed_events += 1
        print("No. of events processed from Cloudvector Enterprise Dashboard: " + str(processed_events))
        return cv_requests

    @staticmethod
    def _parse_spaarc_report():
        if not os.path.exists(os.path.join(os.getcwd(), 'spaarc_report.json')):
            return
        with open(os.path.join(os.getcwd(), 'spaarc_report.json'), encoding='utf-8') as file_:
            spaarc_info = json.load(file_).get("files")
        spaarc_findings = {}
        for file, api_info in spaarc_info.items():
            for api_name, info in api_info.get("apis", {}).items():
                api_name = api_name.split(":")[-1]
                if api_name not in spaarc_findings:
                    spaarc_findings[api_name] = info.get("violations", [])
                else:
                    spaarc_findings[api_name] += info.get("violations", [])
        return spaarc_findings

    @staticmethod
    def generate_fuzz_report(output_report):
        attack_info = {}
        if os.path.exists(os.path.join(os.getcwd(), 'tests/data/attack_info.json')):
            with open(os.path.join(os.getcwd(), 'tests/data/attack_info.json'), encoding='utf-8') as file_:
                attack_info = json.load(file_).get("info")

        with open("report.json", encoding='utf-8') as fobj:
            report = json.load(fobj)

        consolidated_report = {}
        fuzz_metainfo = {}
        fuzz_types = {"critical": {}, "high": {}, "medium": {}, "low": {}, "info": {}, "bestpractice": {}}

        def get_metadata_for_fuzzinput(in_file):
            for type, subtype in attack_info.items():
                for name, info in subtype.items():
                    if str(in_file).lower() in [str(_).replace("\\", "/").split("/")[-1].lower()
                                                for _ in info.get("file_set", [])]:
                        return info
            return None

        for test in report["report"]["tests"]:
            test_name = test["name"].split("::", 1)[-1]
            api_method = test_name.split("test_")[-1].split("_")[0]
            api_name = test_name.split(api_method, 1)[-1].split("for")[0].replace("__", "_").replace("_", "/")
            stdout = test.get("call", {}).get("stdout")
            # fuzz_type = test_name.split("for_")[-1].split("[")[0] + "_fuzz"
            metadata = test.get("metadata")[0]
            try:
                response_length = metadata.split("::")[0]
            except Exception:
                response_length = 0
            try:
                response_time = metadata.split("::")[1]
            except Exception:
                response_time = 0
            try:
                response_code = metadata.split("::")[2]
            except Exception:
                response_code = 0
            try:
                fuzz_sub_type = metadata.split("::")[6]
            except Exception:
                fuzz_sub_type = "na"
            try:
                fuzz_file = metadata.split("::")[6].split("/")[-1]
            except Exception:
                fuzz_file = "na"
            try:
                fuzz_type = metadata.split("::")[3]
            except Exception:
                fuzz_type = "na"
            try:
                test_response = metadata.split("::")[4].split("<body>")[-1]
            except Exception:
                test_response = None
            try:
                if "CURL command to retry:" in stdout:
                    curl_command_to_try = (stdout.split("CURL command to retry:")[-1].replace("\n", "")
                                           .split("-------------------------------------------------------")[0])
                else:
                    curl_command_to_try = ""
            except Exception:
                curl_command_to_try = ""

            if str(fuzz_type).lower() in ["na", "all"]:
                continue

            if api_name not in consolidated_report:
                consolidated_report[api_name] = {}
            if api_method not in consolidated_report[api_name]:
                consolidated_report[api_name][api_method] = {}

            if fuzz_type not in consolidated_report[api_name][api_method]:
                consolidated_report[api_name][api_method][fuzz_type] = {"count": 1, "status": [test["outcome"]],
                                                                        "duration": [int(test["duration"])],
                                                                        "resp_duration": [response_time],
                                                                        "resp_length": [response_length],
                                                                        "resp_code": [response_code]}
            else:
                consolidated_report[api_name][api_method][fuzz_type]["count"] += 1
                consolidated_report[api_name][api_method][fuzz_type]["status"].append(test["outcome"])
                consolidated_report[api_name][api_method][fuzz_type]["duration"].append(int(test["duration"]))
                consolidated_report[api_name][api_method][fuzz_type]["resp_duration"].append(response_time)
                consolidated_report[api_name][api_method][fuzz_type]["resp_length"].append(response_length)
                consolidated_report[api_name][api_method][fuzz_type]["resp_code"].append(response_code)

            fuzz_metadata = get_metadata_for_fuzzinput(fuzz_file)

            if fuzz_metadata:
                fuzz_metainfo[fuzz_type] = {
                        "description": fuzz_metadata.get("description"),
                        "impact": fuzz_metadata.get("impact"),
                        "severity": fuzz_metadata.get("severity"),
                        "remedy": fuzz_metadata.get("remedy"),
                        "classification": fuzz_metadata.get("classification"),
                        "references": fuzz_metadata.get("references"),
                        "ease_of_exploitation": fuzz_metadata.get("ease_of_exploitation")
                    }

            if str(test["outcome"]).lower() in ["failed", "passed"]:
                if not fuzz_metadata:
                    continue
                fuzz_severity = str(fuzz_metadata.get("severity")).lower()
                fuzz_description = fuzz_metadata.get("description")
                fuzz_impact = fuzz_metadata.get("impact")
                fuzz_remedy = fuzz_metadata.get("remedy")
                fuzz_classification = fuzz_metadata.get("classification")
                fuzz_references = fuzz_metadata.get("references")
                fuzz_ease_of_exploitation = fuzz_metadata.get("ease_of_exploitation")

                if fuzz_type not in fuzz_types.get(fuzz_severity, {}):
                    if str(fuzz_type):
                        fuzz_types[fuzz_severity][fuzz_type] = {
                            "description": fuzz_description,
                            "severity": fuzz_severity,
                            "impact": fuzz_impact,
                            "remedy": fuzz_remedy,
                            "classification": fuzz_classification,
                            "references": fuzz_references,
                            "ease_of_exploitation": fuzz_ease_of_exploitation,
                            "executions": [{
                                                "api": api_name,
                                                "api_method": api_method,
                                                "api_response": test_response,
                                                "req_curl": curl_command_to_try,
                                                "status": str(test["outcome"]).lower()
                                          }]
                        }
                else:
                    fuzz_types[fuzz_severity][fuzz_type]["executions"].append({
                                                "api": api_name,
                                                "api_method": api_method,
                                                "api_response": test_response,
                                                "req_curl": curl_command_to_try,
                                                "status": str(test["outcome"]).lower()
                                          })

        api_data = []
        vulnerabilities_found = 0
        total_api_calls = 0
        for api, info in consolidated_report.items():
            for method, fuzz_info in info.items():
                total_tests = 0
                success_tests = 0
                failed_tests = 0
                resp_length = []
                resp_duration = []
                resp_code = []
                for type, info in fuzz_info.items():
                    total_tests += len(info["status"])
                    success_tests += info["status"].count("passed")
                    failed_tests += info["status"].count("failed")
                    resp_code += info["resp_code"]
                    resp_duration += info["resp_duration"]
                    resp_length += info["resp_length"]
                vulnerabilities_found += failed_tests
                record = {"name": api.replace("9i9", "-"), "method": method, "resp_duration": resp_duration,
                          "spec": "openapi_spec.json", "total_tests": total_tests,
                          "success_tests": success_tests, "resp_length": resp_length, "resp_code": resp_code,
                          "failed_tests": failed_tests, "host": os.environ.get("IMPACT_TEST_APP_HOST", ""), "app": "",
                          "skipped_tests": int(total_tests) - int(success_tests) - int(failed_tests),
                          "fuzz_type": type}
                if record["failed_tests"] > 0:
                    record["progress"] = 0
                    api_data.insert(0, record)
                else:
                    record["progress"] = 1
                    api_data.append(record)
                total_api_calls += record["total_tests"]

        fuzz_data = {}
        total_apis = 0
        apis_tested = []
        for api, info in consolidated_report.items():
            for method, fuzz_info in info.items():
                total_apis += 1
                apis_tested.append(api.split("[")[0])
                for type, info in fuzz_info.items():
                    total_tests = 0
                    success_tests = 0
                    failed_tests = 0
                    resp_length = []
                    resp_duration = []
                    resp_code = []
                    total_tests += len(info["status"])
                    success_tests += info["status"].count("passed")
                    failed_tests += info["status"].count("failed")
                    failed_apis = 0
                    resp_length += info["resp_length"]
                    resp_duration += info["resp_duration"]
                    resp_code += info["resp_code"]
                    if failed_tests > 0:
                        failed_apis += 1
                    if type not in fuzz_data:
                        fuzz_data[type] = {"apis_tested": total_apis, "apis_failed": failed_apis,
                                           "total_tests": total_tests, "success_tests": success_tests,
                                           "failed_tests": failed_tests, "resp_length": resp_length,
                                           "resp_duration": resp_duration, "resp_code": resp_code}
                    else:
                        fuzz_data[type]["apis_tested"] = total_apis
                        fuzz_data[type]["apis_failed"] += failed_apis
                        fuzz_data[type]["total_tests"] += total_tests
                        fuzz_data[type]["success_tests"] += success_tests
                        fuzz_data[type]["failed_tests"] += failed_tests
                        fuzz_data[type]["resp_length"] += resp_length
                        fuzz_data[type]["resp_duration"] += resp_duration
                        fuzz_data[type]["resp_code"] += resp_code

        fuzz_data_processed = []
        for k, v in fuzz_data.items():
            if len(k) == 0 or k == "na":
                continue
            if v["apis_failed"] > 0:
                progress = 0
                fuzz_data_processed.insert(0, {
                    "progress": progress, "fuzz_type": k, "total_apis": v["apis_tested"],
                    "host": os.environ.get("IMPACT_TEST_APP_HOST", ""),
                    "success_apis": v["apis_tested"] - v["apis_failed"], "failed_apis": v["apis_failed"], "app": "",
                    "total_tests": v["total_tests"], "success_tests": v["success_tests"],
                    "skipped_tests": int(v["total_tests"]) - int(v["success_tests"]) - int(v["failed_tests"]),
                    "failed_tests": v["failed_tests"], "resp_length": v["resp_length"],
                    "resp_duration": v["resp_duration"]})
            else:
                progress = 1
                fuzz_data_processed.append(
                    {"progress": progress, "fuzz_type": k, "total_apis": v["apis_tested"],
                     "success_apis": v["apis_tested"] - v["apis_failed"], "failed_apis": v["apis_failed"],
                     "total_tests": v["total_tests"], "success_tests": v["success_tests"], "app": "",
                     "failed_tests": v["failed_tests"], "host": os.environ.get("IMPACT_TEST_APP_HOST", ""),
                     "resp_length": v["resp_length"], "resp_duration": v["resp_duration"],
                     "skipped_tests": int(v["total_tests"]) - int(v["success_tests"] - v["failed_tests"])})

        with open(os.path.join(templates_dir, 'html/index.j2'), encoding='utf-8') as file_:
            template = Template(file_.read())

        vulns_stats = {
            "high": 0, "low": 0, "critical": 0, "medium": 0, "info": 0, "bestpractice": 0,
            "all": (len(fuzz_types.get("medium", [])) + len(fuzz_types.get("high", [])) +
                    len(fuzz_types.get("low", [])) + len(fuzz_types.get("critical", [])))
        }

        spaarc_findings = ImpactCore._parse_spaarc_report()
        if spaarc_findings:
            vulns_stats["info"] += sum([len(_) for _ in list(spaarc_findings.values())])

        for severity, types in fuzz_types.items():
            for k, v in types.items():
                vulns_stats[severity] += len([_ for _ in v.get("executions") if _.get("status") == "failed"])

        with open(output_report, "wb+", ) as file_:
            file_.write(template.render(
                api_data=api_data, fuzz_data=fuzz_data_processed, total_api_calls=total_api_calls,
                total_vulnerabilities=vulnerabilities_found, spaarc_findings=spaarc_findings,
                test_time=datetime.datetime.fromtimestamp(time.time()).isoformat(),
                total_apis_scanned=len(list(set(apis_tested))), fuzz_types=fuzz_types, vulns_stats=vulns_stats,
                fuzz_metadata=fuzz_metainfo, detailed_report=os.path.join(os.getcwd(), "CVIAST-detailed_report.html"),
                test_lapse_time=str(round(int(report["report"]["summary"]["duration"]) / 60)) + " min(s)")
                                .encode("utf-8", "ignore"))
        print("CVIAST report saved in " + os.path.join(os.getcwd(), output_report))


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r{prefix} |{bar}| {percent}% {suffix}'.format(prefix=prefix, bar=bar, percent=percent, suffix=suffix),
          end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    html_report_name = "CVIAST-report.html"
    quiet_mode = True
    is_timeoutpresent = False

    if sys.argv[1:]:
        for _ in sys.argv[1:]:
            if "report-out" in _:
                html_report_name = _.split("=")[-1]
                sys.argv.remove(_)
            if "--v" in _:
                quiet_mode = False
                sys.argv.remove(_)
            if "timeout" in _:
                is_timeoutpresent = True

        if not is_timeoutpresent:
            sys.argv.append("--timeout=300")
        if sys.argv[1:][0] == "--list-supported-fuzz-types":
            print("\n\t\t\t\t\t\t".join(supoorted_fuzz_types))
            return
        if sys.argv[1:][0] == "--generate-report":
            ImpactCore.generate_fuzz_report(html_report_name)
            return
        if sys.argv[1:][0] == "--generate-input-params":
            ImpactCore.generate_auto_input_params_file()
            return
        if sys.argv[1:][0] == "--execute":
            arguments = sys.argv[2:]
            print(arguments)
            if not quiet_mode:
                arguments += ["--json=report.json", "--html=CVIAST-detailed_report.html", "--self-contained-html",
                              "--log-cli-level=INFO", "-vv"]
            else:
                arguments += ["--json=report.json", "--html=CVIAST-detailed_report.html", "--self-contained-html",
                              "--log-cli-level=INFO", "-vv", ">> cviast_execution_log.txt"]
            try:
                print("Test Execution is in progress")
                if not quiet_mode:
                    pytest.main(arguments)
                else:
                    os.system("pytest " + " ".join(arguments))
                print("Test Execution completed!")
                ImpactCore.generate_fuzz_report(html_report_name)
            except Exception:
                raise
            return

    if os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml")) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    else:
        ce_details = {}

    print("\n\n" + "\t" * 4 + "*****" * 20)
    print("\t" * 8 + "Imperva - Dynamic Application Security Testing")
    print("\t" * 4 + "*****" * 20)
    # if ce_details:
    #     print("\nAPIShark details from my_cesetup.yaml:\n\t" + str(ce_details) + "\n")
    config = input("\n\nEnter the Imperva config file path: ")
    if os.path.exists(config):
        with open(config) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    print("APIShark details from my_cesetup.yaml:\n\t" + str(ce_details["ce_setup"]))
    ce_host = ce_details["ce_setup"]["ce_host"]
    ce_username = ce_details["ce_setup"]["ce_username"]
    ce_password = None
    if not config:
        if ce_details.get("ce_host"):
            ce_host = ce_details["ce_host"]
        else:
            ce_host = input("Enter APIShark host in format <host>:<port> : ")
        if ce_details.get("ce_username"):
            ce_username = ce_details["ce_username"]
        else:
            ce_username = input("Enter your APIShark username : ")
    if ce_host:
        ce_password = getpass.getpass(prompt="APIShark password:")
    option = input("what do you want to do? (1: Compare SPECs for diff or 2: Use new SPEC):")
    if int(option) == 1:
        input_spec_one = input("Enter absolute path to Old API SPEC(Version A): ")
        input_spec_two = input("Enter absolute path to New API SPEC(Version B) : ")
        cover_only_diff = input("Do you want to process only the missing parameters? (Y/N) : ")
    else:
        input_spec_one = ""
        input_spec_two = input("Enter absolute path to Open API SPEC: ")
        cover_only_diff = "n"
    input_params_file = input("Enter absolute path to input parameters file(press Enter for None):")
    if not os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml"), "w+") as fobj:
            yaml.dump({"ce_host": str(ce_host), "ce_username": str(ce_username)}, fobj)
    enable_fuzzing = False

    if sys.argv[1:]:
        if sys.argv[1:][0] == "--fuzz":
            print("Fuzzing enabled!")
            enable_fuzzing = True

    ImpactCore(str(input_spec_one).strip(), str(input_spec_two).strip(), ce_host, ce_username, ce_password, config,
               str(cover_only_diff).lower(), input_params_file, enable_fuzzing)
    if not enable_fuzzing:
        print("Generating test data(input_params.json) from the events captured in Cloudvector controller")
        ImpactCore.generate_auto_input_params_file()
        if os.path.exists(os.path.join("tests", "input_params.json")):
            override = input("input_params.json already present in tests folder, do you want to override (y/n): ")
            if str(override).lower() == "y":
                shutil.copy(os.path.join("tests", "input_params_auto-generated.json"),
                            os.path.join("tests", "input_params.json"))
            else:
                print("Note: you can also generate input_params.json using --generate-input-params "
                      "after test generation")
        else:
            shutil.copy(os.path.join("tests", "input_params_auto-generated.json"),
                        os.path.join("tests", "input_params.json"))
        print("done generating test data")
    print("Test generation complete! Making the pycode PEP complaint (https://www.python.org/dev/peps/pep-0008/)")
    printProgressBar(0, len(os.listdir("tests")), prefix='Progress:', suffix='Complete', length=50)
    i = 0
    for _ in os.listdir("tests"):
        if ".py" in _:
            os.system("autopep8 --in-place --aggressive --aggressive tests/" + str(_))
            printProgressBar(i + 1, len([_ for _ in os.listdir("tests") if ".py" in _]),
                             prefix='Progress:', suffix='Complete', length=50)
            i += 1
    print("done")


if __name__ == "__main__":
    main()
