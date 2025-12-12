#!/usr/bin/env python
# coding: utf-8


import os
import shutil
import dill

# import sys
# import glob
# import ast
# from pathlib import Path


# Add src to path if needed
# sys.path.insert(0, os.path.abspath("src"))

from ghtest import scan, suggest, make_test, write_module
from ghtest.tests_writer import TestArtifact


def _run_tests(gts, interactive=True, vb=0):
    trs = []
    for gt in gts:
        try:
            tr = gt.test_callable(interactive=interactive)
            trs.append(tr)
        except Exception as e:
            if vb:
                print(str(e))
            # if tests fail, we append None so the number of items remains in sync with eg result or suggest lists
            trs.append(None)
    return trs


def create_tests(
    cassette_dir, test_dir, src_dir, clean_up=True, unsafe=True, history=False, vb=1
):
    """
    Run test suite, return values from component functions.

    Args:
        cassette_dir (str): folder with vcr cassettes
        test_dir (str): folder with test modules
        src_dir (str): folder with src under test
        clean_up (bool): remove existing cassettes and tests
        unsafe (bool): run potentially destructive functions without requesting permission
        history (bool): disregard parameter suggestions from history
        vb (int): verbosity

    Returns:
        tuple: (scs, sps, gts, trs) (scans, suggested params, generated tests, test results)

    Side Effects:
        deletes cassette_dir, test_dir
        writes cassette_dir, test_dir
        executes functions in src, potentially including destructive functions
    """
    if clean_up:
        if os.path.exists(cassette_dir):
            shutil.rmtree(cassette_dir)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        os.makedirs(cassette_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

    # Set unsafe mode
    if unsafe:
        os.environ["GHTEST_ASSUME_SAFE"] = "1"
    if not history:
        os.environ["GHTEST_PARAM_HISTORY"] = ""  # Disable history for reproducibility

    if vb > 1:
        print(f"Scanning {src_dir}...")  # noqa: E701
    scs = scan(src_dir)
    scs = [
        f
        for f in scs
        if not f.qualname.startswith("_") and not f.qualname.startswith("test_")
    ]
    if vb > 1:
        print(f"Found {len(scs)} functions.")  # noqa: E701

    for f in scs:
        if vb > 1:
            print(
                f"  {f.qualname}: role={f.crud_role}, resource={f.crud_resource}"
            )  # noqa: E701

    if vb > 1:
        print("Suggesting params...")  # noqa: E701
    sps = []
    total_params = 0
    for func in scs:
        sp = suggest(func, literal_only=False)
        sps.append(sp)
        total_params += len(sp.param_sets)
        if vb > 1:
            print(f"  {func.qualname}: {len(sp.param_sets)} param sets")  # noqa: E701
        if func.qualname == "list_repos":
            if vb > 1:
                print(f"    list_repos params: {sp.param_sets}")  # noqa: E701
        if func.qualname == "create_repo" and sp.scenario:
            if vb > 1:
                print(
                    f"    create_repo scenario steps: {[s.params for s in sp.scenario.steps]}"
                )  # noqa: E701

    if vb:
        print(f"Total param sets: {total_params}")  # noqa: E701

    if vb > 1:
        print("Generating tests and recording cassettes...")  # noqa: E701
    gts = []
    for sp in sps:
        if vb > 1:
            print(f"  Processing {sp.qualname}...")  # noqa: E701
        try:
            gt = make_test(suggestion=sp, cassette_dir=cassette_dir)
            gts.append(gt)
        except Exception as e:
            if vb:
                print(f"  ERROR creating test for {sp.qualname}: {e}")  # noqa: E701

    # Coverage Feedback Loop
    try:
        import coverage
        import tempfile

        if vb:
            print("Running tests with coverage for feedback...")  # noqa: E701

        with tempfile.TemporaryDirectory() as tmp_cassette_dir:
            # Regenerate tests for coverage run using temp cassette dir
            gts_cov = []
            for sp in sps:
                try:
                    gt = make_test(suggestion=sp, cassette_dir=tmp_cassette_dir)
                    gts_cov.append(gt)
                except Exception:
                    pass

            cov = coverage.Coverage(source=[src_dir])
            cov.start()

            _run_tests(gts_cov, interactive=False, vb=vb)

            cov.stop()
            cov.save()

            if vb:
                print("Analyzing coverage for targeted suggestions...")  # noqa: E701
            sps_targeted = []
            for func in scs:
                # Pass coverage data to suggest
                sp = suggest(func, literal_only=False, coverage_data=cov)
                sps_targeted.append(sp)

            # Regenerate tests with targeted suggestions (using real cassette_dir)
            gts = []
            for sp in sps_targeted:
                try:
                    gt = make_test(suggestion=sp, cassette_dir=cassette_dir)
                    gts.append(gt)
                except Exception as e:
                    if vb:
                        print(
                            f"  ERROR creating targeted test for {sp.qualname}: {e}"
                        )  # noqa: E701

    except ImportError:
        if vb:
            print("Coverage library not found, skipping feedback loop.")  # noqa: E701
    except Exception as e:
        if vb:
            print(f"Error during coverage feedback: {e}")  # noqa: E701

    if vb:
        print(f"Generated {len(gts)} test objects.")  # noqa: E701

    if vb > 1:
        print("Running tests to record cassettes (final pass)...")  # noqa: E701
    trs = _run_tests(gts, interactive=not unsafe, vb=vb)

    if vb > 1:
        print("Writing test modules...")  # noqa: E701
    artifacts = []
    for sp, tr in zip(sps_targeted if "sps_targeted" in locals() else sps, trs):
        if tr is not None:
            artifacts.append(TestArtifact(suggestion=sp, run=tr))

    write_module(
        artifacts=artifacts,
        output_dir=test_dir,
        exception_assertion="type",
        include_return_summary=True,
    )

    return scs, sps, gts, trs


def workflow(
    src_dir,
    test_dir,
    cassette_dir,
):

    scs, sps, gts, trs = create_tests(cassette_dir, test_dir, src_dir)

    data_dir = "testdata_test_objects"
    os.makedirs(data_dir, exist_ok=True)
    objs = [("scs", scs), ("sps", sps), ("gts", gts), ("trs", trs)]
    for p, o in objs:
        path = os.path.join(data_dir, p)
        with open(path, "wb") as f:
            dill.dump(o, f)
