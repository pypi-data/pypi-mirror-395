# init file for setting module

import json
import inspect
import os

datapath = {
    "MAG": {
        "pfile_path": "/data/messenger/mag/pfile",
        "ofile_path": "/data/messenger/mag/ofile"
    },
    "FIPS_CDR_SCAN": {
        "pfile_path": "/data/messenger/scan/pfile",
        "ofile_path": "/data/messenger/scan/pfile"
    },
    "SPICE_KERNEL": {
        "spk_path": "/data/messenger/spice_kernel"
    }
}

# importしたファイルのパスを取得
caller_dir = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))
library_dir = os.path.dirname(__file__)

def check_datapath_json():
    if not os.path.exists(os.path.join(caller_dir, 'datapath.json')):
        print("datapath.json file is missing")
        print("create a new datapath.json file")
        with open(os.path.join(caller_dir, 'datapath.json'), 'w') as f:
            json.dump(datapath, f, indent=4)
check_datapath_json()