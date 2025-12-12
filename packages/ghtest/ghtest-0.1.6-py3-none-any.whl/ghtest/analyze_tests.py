#!/usr/bin/env python
# coding: utf-8

# ## imports

# In[1]:


import os
import re
import glob
import yaml
from natsort import natsorted
from collections import defaultdict


# In[2]:


from .create_tests_workflow import create_tests


# ## constants

# In[3]:


EXCLUDE = ["__pycache__", "data"]


# In[ ]:


# ## analyze casssettes

# In[4]:


def _count_codes(codes):
    counts = defaultdict(lambda: 0)
    for code in codes:
        if isinstance(code, list):
            for code1 in code:
                counts[code1] += 1
        else:
            counts[code] += 1
    return dict(counts)


# In[5]:


def _analyze_codes(cassette_dir, modules):
    cassettes = natsorted([f for f in os.listdir(cassette_dir) if f.endswith(".yaml")])
    ret = []
    for cassette in cassettes:
        path = os.path.join(cassette_dir, cassette)
        with open(path) as f:
            t = yaml.safe_load(f)
            codes = [f["response"]["status"]["code"] for f in t["interactions"]]
            name = _get_function_name(path, cassette_dir, modules)
            ret.append((cassette, name, codes))
    return ret


# In[6]:


def _get_function_name(path, cassette_dir, modules, vb=0):
    # cp=os.path.join(cassette_dir, mod)
    # p=rf'^{cp}\.([\w+]+)\.case_\d+\.yaml$'
    # p1=rf'^{cp}\.(\w+)\.scenario\.step_\d+\.yaml$'
    # p1=rf'^{cp}\.(\w+)\.scenario\.step_\d+\.yaml$'
    # p1=rf'^{cp}\.(\w+)\.scenario\.(?:step_\d+|cleanup)\.yaml$'
    ps = [os.path.join(cassette_dir, m) for m in modules]
    ps1 = [rf"^{p}\.([\w+]+)\.case_\d+\.yaml$" for p in ps]
    ps2 = [rf"^{p}\.(\w+)\.scenario\.(?:step_\d+|cleanup)\.yaml$" for p in ps]
    ps1.extend(ps2)
    ps = ps1
    path1 = ""
    for p in ps:
        path1 = re.search(p, path)
        if path1:
            break
    try:
        path1 = path1.group(1).strip("__")
    except Exception as e:
        if vb:
            print(e)
            print("path", path)
            print("cd", cassette_dir)
            print("module", modules)
            print("path1", path1)
            print("p", p)
    p1 = r"__\d+"
    name = re.sub(rf"^(?:{p1})+|(?:{p1})+$", "", path1)
    return name


# In[7]:


def _compact_names(ret):
    ret1 = {}
    for p, n, c in ret:

        for p, n, c in ret:
            ret1[n] = [] if n not in ret1 else ret1[n]
            ret1[n].append(c)
    ret2 = {}
    for k, v in ret1.items():
        ret2[k] = _count_codes(v)

    return ret2


def _compact_names(ret):
    ret1 = {}
    for p, n, c in ret:
        ret1[n] = [] if n not in ret1 else ret1[n]
        ret1[n].append(c)
    ret2 = {}
    for k, v in ret1.items():
        ret2[k] = _count_codes(v)
    return ret2


# In[8]:


def _print_codes(ret):
    ret1 = {}
    for p, n, c in ret:
        ret1[n] = [] if n not in ret1 else ret1[n]
        ret1[n].append(c)
    for k, v in ret1.items():
        print(k)
        print(v)
        print()


# In[9]:


def _sum_codes(r):
    ret = {}
    for p, n, cs in r:
        if n in ret:
            ret[n].update(cs)
        else:
            ret[n] = set(cs)
    return ret


# In[10]:


def get_codes(cassette_dir, src_dir):
    """list requests return codes found in cassette_dir cassettes"""
    modules = modules = _get_modules(src_dir)
    ret = _analyze_codes(cassette_dir, modules)
    ret = _sum_codes(ret)
    # return _compact_names(ret)
    return ret


# In[ ]:


# ## analyze tests

# In[11]:


def _get_test_files(test_dir, exclude=None, vb=0):
    if not exclude:
        exclude = []  # noqa: E701
    if isinstance(exclude, str):
        exclude = [exclude]  # noqa: E701
    exclude.extend(EXCLUDE)
    test_modules = []
    for f in glob.glob(os.path.join(test_dir, "**", "*"), recursive=True):
        if any(e in f.split(os.sep) for e in exclude):
            continue
        if os.path.isdir(f):
            continue
        if vb:
            print(os.path.basename(f).split(".")[0])  # noqa: E701
        test_modules.append(f)
    return natsorted(test_modules)


# In[ ]:


# In[12]:


def _get_name(f):
    return os.path.basename(f).split(".")[0]


# In[13]:


def _get_base_test_name(f):
    return f.split(os.sep)[-1]


# In[14]:


def _get_tests(test_modules):
    ret = []
    for f in test_modules:
        with open(f) as h:
            t = h.read()
        funcs = [
            _l[9:].rstrip(":()") for _l in t.splitlines() if _l.startswith("def test")
        ]
        _n = _get_base_test_name(f)
        ret.append((f, _get_methods(funcs)))
    return ret


# In[15]:


def _print_tests(test_dir, exclude=None, vb=0):
    nc, nt = 0, 0
    fns = {}
    tm = _get_test_files(test_dir, exclude=exclude, vb=vb)
    r = _get_tests(tm)
    cps, tps = [], []

    for a, b in r:
        if "cassette" in a:
            cps.append(a)
            nc += 1
        else:
            tps.append(a)
            nt += 1
        if vb:
            print(a)
        for c in b:
            nm, nr = c
            if nm in fns:
                fns[nm] += nr
            else:
                fns[nm] = nr
            if vb:
                print(c)
        if vb:
            print()
    ntsts = sum([v for k, v in fns.items()])
    print(f"{nc} cassettes, {nt} test modules, {ntsts} tests")
    print(fns)


# In[16]:


def _get_methods(ls):
    ret = {}
    for el in ls:
        i = el.find("case")
        if i:
            el = el[:i].rstrip("_")
            if el not in ret:
                ret[el] = 1
            else:
                ret[el] += 1
    return [(k, v) for k, v in ret.items()]


# In[17]:


def _get_modules(src_dir):
    fs = glob.glob(os.path.join(src_dir, "**", "*.py"), recursive=True)
    modules = [os.path.basename(f).rstrip(".py") for f in fs]
    return modules


# In[18]:


def _print_line(t="", ll=80):
    ln = len(t)
    s = (ll - ln) // 2
    s1 = (ll - ln) / 2
    e = "" if s1 == s else "#"
    print()
    print("#" * s, t, "#" * s + e)


# In[27]:


def _load_test_data(test_objects_dir="testdata_test_objects", vb=0):
    import dill
    import os

    objs = ["scs", "sps", "gts", "trs"]
    ret = []
    for p in objs:
        path = os.path.join(test_objects_dir, p)
        if not os.path.isfile(path):
            if vb:
                print(f"{path} not found")  # noqa: E701
            continue
        with open(path, "rb") as f:
            ret.append(dill.load(f))  # nosec: B301
    if not ret:
        return None, None, None, None
    scs, sps, gts, trs = ret
    return scs, sps, gts, trs


# ## api

# In[28]:


# scanner
def print_scan(scs):
    for sc in scs:
        _m, n, ps = sc.module, sc.qualname, sc.parameters

        ls = {p.name: p.default for p in ps}
        print(n)
        print(ls)


# In[29]:


def print_suggestion(sps):
    for sc in sps:
        _m, n, ps = sc.module, sc.qualname, sc.param_sets
        print()
        print(n)
        for p in ps:
            print(p)
        sn = sc.scenario
        if sn:
            print()
            print("scenario")
            for s in sn.steps:
                print(s.qualname)
                print(s.params)


# In[30]:


def print_tests(trs):
    for tr in trs:
        if not tr:
            continue

        cn = os.path.basename(tr.cassette_path).split(".")
        mn = cn[1]
        print(mn)

        for c in tr.cases:

            ct = c.target
            if mn != ct:
                pass
                # print('user warning: ',mn,ct)
            cp = c.cassette_path
            cscn = "no path"
            if cp is not None:
                cscn = os.path.basename(c.cassette_path).split(".")[2]

            ctt = ct if ct != mn else ""
            print(cscn, ctt, c.params)

            # break
        print()


# In[ ]:


# In[33]:


def print_test_summary(
    cassette_dir="testdata_tests/cassettes",
    test_dir="testdata_tests",
    src_dir="testdata",
    data_dir="data",
    test_objects_dir="testdata_test_objects",
    refresh=False,
    vb=0,
):
    """
    Print tests statistics like tested functions, request return codes etc.

    Args:
        cassette_dir (str): folder with vcr cassettes
        test_dir (str): folder with tests
        src_dir (str): folder with source under test
        data_dir (str): data folder within tests to ignore
        test_objects_dir (str): folder with test objects
        refresh (bool): create tests before showing detailed stats, else try to load from disk
        vb (int): detail level

    Returns:
        None

    Side Effects:
        prints to stdout
    """

    _print_line("test summary")
    r = _print_tests(test_dir)
    print(r)
    _print_line("return codes summary")
    r = get_codes(cassette_dir, src_dir)
    print(r)
    # create tests

    if not vb > 1:
        return
    if refresh:
        try:
            scs, sps, gts, trs = create_tests(cassette_dir, test_dir, src_dir)
        except Exception:
            print("test objects not found, abandoning detailed statistics printout")
            return
    else:
        try:
            scs, sps, gts, trs = _load_test_data(test_objects_dir=test_objects_dir)
        except Exception:
            print("error reading test objects, abandoning detailed statistics printout")
            return
    if scs:
        _print_line("scans")
        print_scan(scs)
    if sps:
        _print_line("suggestions")
        print_suggestion(sps)
    if trs:
        _print_line("tests")
        print_tests(trs)


# In[ ]:


# In[ ]:


# In[36]:


if __name__ == "__main__":
    cassette_dir = "testdata_tests/cassettes"
    test_dir = "testdata_tests"
    src_dir = "testdata"
    data_dir = "data"
    vb = 2
    print_test_summary(
        cassette_dir="testdata_tests/cassettes",
        test_dir="testdata_tests",
        src_dir="testdata",
        data_dir="data",
        vb=vb,
    )


# In[ ]:


# In[ ]:


# In[ ]:
