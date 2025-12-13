import pandas as pd
import os

library_dir = os.path.dirname(__file__)

orbit = pd.read_pickle(os.path.join(library_dir, 'orbits.pkl'))