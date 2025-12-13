import requests
import os
import spiceypy as sp
from MDUS.Setting.setting import setting
from pathlib import Path

library_dir = os.path.dirname(__file__)

spfiles_url_path = os.path.join(library_dir, 'SPICE_DOWNLOAD.txt')
spkfiles_path = setting["SPICE_KERNEL"]["spk_path"]

def chech_spkfile():
    with open(spfiles_url_path, 'r') as f:
        for url in f:
            url = url.strip()
            filename = url.split("/")[-1]
            for path in Path(spkfiles_path).rglob(filename):
                break
            else:
                print("Some SPICE kernel files are missing.")
                print("So you cannnot use GetPos()")
                print("Please run MDUS.DownloadSPK() to download the missing files.")
                return
    # load spice kernel
    sp.furnsh(str(os.path.join(spkfiles_path, 'msgr_2015_v02.tm')))
    return

def DownloadSPK(redownload=False):
    os.makedirs(os.path.join(spkfiles_path, 'data', "lsk"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "pck"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "sclk"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "fk"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "ik"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "spk"), exist_ok=True)
    os.makedirs(os.path.join(spkfiles_path, 'data', "ck"), exist_ok=True)
    # download
    with open(spfiles_url_path, 'r') as f:
        for url in f:
            url = url.strip()
            if not url:
                continue
            else:
                if url[-2:] == "tm":
                    filename = url.split("/")
                    filename = "/".join(filename[-1:])
                else:
                    filename = url.split("/")
                    filename = "/".join(filename[-2:])
                    filename = "data/" + filename
                if not os.path.exists(os.path.join(spkfiles_path, filename)) or redownload:
                    response = requests.get(url)
                    print("Download:" + filename)
                    with open(os.path.join(spkfiles_path, filename), 'wb') as file:
                        file.write(response.content)
                    print("Successfully downloaded: " + filename)
    # rewite MK kernekl file
    target_file = os.path.join(spkfiles_path, 'msgr_2015_v02.tm')
    with open(target_file, 'r') as file:
        text = file.read()
    old = "./data"
    new = os.path.join(spkfiles_path, "data")
    text = text.replace(f"      PATH_VALUES     = ( '{old}' )",
                        f"      PATH_VALUES     = ( '{new}' )")
    with open(target_file, 'w') as file:
        file.write(text)