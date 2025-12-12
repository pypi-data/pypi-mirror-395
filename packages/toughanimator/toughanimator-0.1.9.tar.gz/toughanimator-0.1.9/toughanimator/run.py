import os
import tough_classes as ta
import pandas as pd
import matplotlib.pyplot as plt

#dir_name = "unresolved" 
dir_name = "test_cases"
case_name = "PetraSim_2D_Conceptual"
test_case_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), dir_name) 

case_dir = os.path.join(test_case_dir, case_name)

case_dir = r"D:\Projects\202511\dip_left\TRv4"
#case_dir = r"D:\Projects\202504\polygonal\poly_test"
#case_dir = r"D:\Projects\202507\tough系列output\tough output format\TR_MINC_exe"
#case_dir = r"D:\Projects\202508\tough_cases\WW\7_TR_MINC_petrasim2025__5spot"
#case_dir = r"D:\Projects\202508\tough_cases\WW\6_TR_MINC_exe"
reader = ta.vis_reader(case_dir)
#reader.write_eleme_conne()
#reader.write_geometry()
#reader.write_incon()
#reader.write_result()
reader.write_all()


