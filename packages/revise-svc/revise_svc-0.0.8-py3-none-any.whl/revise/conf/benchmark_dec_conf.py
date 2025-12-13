import os
from dataclasses import dataclass

from revise.conf.base_conf import BaseConf


@dataclass
class BenchmarkDecConf(BaseConf):
    mode = "benchmark"


    st_file: str
    real_st_file: str
    sc_ref_file: str
    spot_size: int

    # annotate parameters
    annotate_pot_reg: float = 0.01
    annotate_pot_reg_m: float = 0.0001
    annotate_pot_reg_type: str = "kl"

    # segmentation effect parameters
    dropout_total_counts: int = 60
    swapping_total_counts: int = 300
    lower_ts: float = 0.2
    upper_ts: float = 0.8

    # svc parameters
    svc_completeness: bool = True

    @property
    def result_dir(self):
        return os.path.join(self.result_root_path, self.sub_file_path, f"spot_{self.spot_size}")

    @property
    def st_file_path(self):
        return os.path.join(self.data_root_path, self.sub_file_path, f"spot_{self.spot_size}", self.st_file)

    @property
    def real_st_file_path(self):
        return os.path.join(self.data_root_path, self.sub_file_path, self.real_st_file)

    @property
    def sc_ref_file_path(self):
        return os.path.join(self.data_root_path, self.sub_file_path, self.sc_ref_file)

    @property
    def pm_on_cell_file(self):
        return os.path.join(os.path.dirname(os.path.join(self.data_root_path, self.sub_file_path)), "PM_on_cell.csv")
