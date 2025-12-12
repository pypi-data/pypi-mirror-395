#!python3
#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2012-2025                                       ###
###                                                                          ###
### University of California at San Francisco (UCSF), USA                    ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland         ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import datetime
import json
import sys
import urllib
import urllib.error
import urllib.request

################################################################################

def get_pypi_versions(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return list(data.get("releases", {}).keys())
    except urllib.error.HTTPError as e:
        if (e.code == 404):
            return [] # Package doesn't exist yet
        raise

def get_next_pypi_version(package_name):
    now = datetime.datetime.now()
    print(f"now: {now}")
    current_date = f"{now.year}.{now.month}.{now.day}"
    print(f"current_date: {current_date}")

    all_versions = get_pypi_versions(package_name)
    print(f"all_versions: {all_versions}")

    today_versions = [v for v in all_versions if (v == current_date) or (v.startswith(current_date + "."))]
    print(f"today_versions: {today_versions}")

    if (current_date not in today_versions):
        return current_date
    
    max_post = 0
    for v in today_versions:
        if (".post" in v):
            try:
                suffix = int(v.split(".post")[-1])
                max_post = max(max_post, suffix)
            except ValueError:
                continue
    return f"{current_date}.post{max_post+1}"

if (__name__ == "__main__"):
    import fire
    fire.Fire(get_next_pypi_version)
