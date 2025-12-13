import MDUS.Setting as Setting

def version_check_0_1_6():
    # chech setting json
    if "SPICE_KERNEL" not in Setting.setting:
        Setting.setting["SPICE_KERNEL"] = {
            "spk_path": "/data/messenger/spice_kernel"
        }
        print("Update setting json for version 0.1.6")
        print("Add SPICE_KERNEL setting")
