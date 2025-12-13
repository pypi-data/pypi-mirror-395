import sys
from IPython.display import Video, Image

# import dill
import PIL.Image

# import skrf as rf
from pprint import pprint
import os
import subprocess
import json
import numpy as np
import requests
from .sparams import *
from .utils import *
from .layers import *
from .constants import *
from PIL import Image as PILImage

from subprocess import Popen, PIPE

URL = "http://127.0.0.1:8975"


def start_fdtd_server(url=URL):
    try:
        r = requests.get(url)
    except:
        print("starting julia fdtd server on localhost...")
        cmd = ["julia", "-e", "using Luminescent; start_fdtd_server()"]
        proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with proc:
            for line in proc.stdout:
                print(str(line.decode().strip()), flush=True)
            err_message = proc.stderr.read().decode()
            print(err_message)


def solve(path, RUN=None, nthreads=None, **kwargs):
    os.environ["JULIA_CUDA_USE_COMPAT"] = "0"
    os.environ["JULIA_NUM_THREADS"] = str(nthreads or os.cpu_count())
    if sys.platform.startswith("linux"):
        os.environ["PATH"] += ":/usr/local/Luminescent/bin"
    if nthreads is None:
        nthreads = os.cpu_count()
    path = os.path.abspath(path)
    prob = load_prob(path)
    prob = {**prob, **kwargs}
    with open(os.path.join(path, "problem.json"), "w") as f:
        json.dump(prob, f)

    # prob["action"] = "solve"
    # r = requests.post(f"{url}/local", json=prob)
    1
    # print(f"""
    #       using simulation folder {path}
    #       starting julia process...
    #       """)
    # start_time = time.time()

    # if dev:
    #     env = r'using Pkg;Pkg.activate(raw"c:\Users\pxshe\OneDrive\Desktop\beans\Luminescent.jl\luminescent");'
    # else:
    #     env = '0;'
    # cmd = ["lumi", path]
    # try:
    if not RUN:
        try:
            c = run(
                [
                    "luminescent",
                    path,
                    prob["gpu_backend"],
                    # f" --julia-args -t{nthreads}",
                    f"--julia-args --threads={nthreads}",
                ]
            )
            if c != 0:
                print("can't find fdtd binary ")
                # exit(1)
        except:
            print("failed")
    else:
        run(
            [
                "julia",
                f"-t{nthreads}",
                RUN,
                path,
            ]
        )

    # except:
    # run(["julia", "-e", f'println(Base.active_project())'])
    # print("no binaries found - starting julia session to compile - will alternate between execution and JIT compilation - will take 3 mins before simulation starts.\nYou can take a break and come back :) ...")

    # prob = json.loads(open(os.path.join(path, "problem.json"), "rb").read())
    # a = ['julia', '-e', ]
    # gpu_backend = prob["gpu_backend"]
    # _class = prob["class"]
    # if gpu_backend == "CUDA":
    #     array = "cu"
    #     pkgs = ",CUDA"
    # else:
    #     array = "Array"
    #     pkgs = ""

    # run([f'using Luminescent;picrun(raw"{path}")'])
    # b = [f'using Luminescent{pkgs};{_class}run(raw"{path}",{array})']
    # run(a+b)

    # with Popen(cmd,  stdout=PIPE, stderr=PIPE) as p:
    #     if p.stderr is not None:
    #         for line in p.stderr:
    #             print(line, flush=True)
    # exit_code = p.poll()
    # subprocess.run()
    # print(f"julia simulation took {time.time()-start_time} seconds")
    # print(f"images and results saved in {path}")
    # sol = load(path=path)
    # return sol


def load_sparams(sparams):
    if "re" in list(sparams.values())[0]:
        return {k: v["re"] + 1j * v["im"] for k, v in sparams.items()}
    return {
        wavelength: {k: (v["re"] + 1j * v["im"]) for k, v in d.items()}
        for wavelength, d in sparams.items()
    }


def load(path, show=True):
    path = os.path.abspath(path)
    print(f"loading solution from {path}")
    return readjsonnp(os.path.join(path, "solution.json"))


def design_from_gds(path, i=1):
    # make_design_gds(path)
    c = gf.import_gds(os.path.join(path, f"design{i}.gds"))
    d = json.load(open(os.path.join(path, "info.json")))
    for p in d[f"designs"][i - 1]["ports"]:
        c.add_port(**p, layer=WG)
    c.info = d
    return c
