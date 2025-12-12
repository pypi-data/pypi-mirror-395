#!/usr/bin/env python3

import subprocess


def _run(cmd):
    print(cmd)
    ret = subprocess.call(cmd, cwd="example", shell=True)
    assert ret == 0


def test_zeo():
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")
    _run("canYouDigIt --verbose init --yes")
    _run("canYouDigIt --verbose jobs create  --yes")
    _run("canYouDigIt --verbose runs create --run_name test ")
    _run("canYouDigIt --verbose runs info ")
    _run("canYouDigIt --verbose runs launch ")
    _run("canYouDigIt --verbose full-update --run_name test ")
    _run("canYouDigIt --verbose runs plot --list_quantities")
    _run("canYouDigIt --verbose runs info --run_id 1")
    _run("canYouDigIt --verbose runs exec --run_id 1 ls")
    _run("canYouDigIt --verbose info")
    _run("canYouDigIt --verbose runs update  nproc = 2")
    _run("canYouDigIt --verbose runs plot --quantity ekin --fileout tmp.pdf")
    _run("python post_treatment.py --no_show")
    _run("canYouDigIt server stop")
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")


def test_server():
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")
    _run("canYouDigIt init  --yes")
    _run("canYouDigIt --verbose server start")
    _run("canYouDigIt server status")
    _run("canYouDigIt server stop")
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")


def test_tcp_server():
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")
    _run("canYouDigIt init  --yes")
    _run("canYouDigIt server stop")
    _run("canYouDigIt --verbose server start --host zeo://localhost:6666")
    _run("canYouDigIt server status")
    _run("canYouDigIt server status --host zeo://localhost:6666")
    _run("canYouDigIt server stop")
    _run("rm -rf .bd bd.log BD-bd_study-runs test.pdf tmp.pdf")
