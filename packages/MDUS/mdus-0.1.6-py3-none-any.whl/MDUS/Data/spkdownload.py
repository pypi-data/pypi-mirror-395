# Warning: This file is old version of spkdownload.py.

import requests
import os
import spiceypy as sp

pckurl = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mess-e_v_h-spice-6-v1.0/messsp_1000/data/pck/pck00010_msgr_v23.tpc"
tlsurl = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls"
spkurl = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mess-e_v_h-spice-6-v1.0/messsp_1000/data/spk/msgr_040803_150430_150430_od431sc_2.bsp"
fkurl = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mess-e_v_h-spice-6-v1.0/messsp_1000/data/fk/msgr_dyn_v600.tf"

spkernel_files = [
    'msgr_040803_150430_150430_od431sc_2.bsp',
    'msgr_dyn_v600.tf',
    'naif0012.tls',
    'pck00010_msgr_v23.tpc'
]

library_dir = os.path.dirname(__file__)
def DownloadSPK():
    for file in spkernel_files:
        if not os.path.exists(os.path.join(library_dir,'spice_kernel', file)):
            print("Downloading: " + file)
            if file == 'msgr_040803_150430_150430_od431sc_2.bsp':
                url = spkurl
            elif file == 'msgr_dyn_v600.tf':
                url = fkurl
            elif file == 'naif0012.tls':
                url = tlsurl
            elif file == 'pck00010_msgr_v23.tpc':
                url = pckurl
            # download the file
            response = requests.get(url)
            # check if the request was successful
            if response.status_code == 200:
                # save the file
                with open(os.path.join(library_dir, 'spice_kernel', file), 'wb') as f:
                    f.write(response.content)
                print("Successfully downloaded: " + file)
                sp.furnsh(str(os.path.join(library_dir, 'spice_kernel', file)))
            else:
                print("Failed to download: " + file)
        else:
            print("Already exists: " + file)