import sys

sys.path.insert(1, "../diagnosis-keys/")

from lib.diagnosis_keys import *
from lib.diagnosis_key import DiagnosisKey
from lib.count_users import count_users
import argparse


parser = argparse.ArgumentParser(description="Exposure Notification Diagnosis Key Parser.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--diagnosiskeys", type=str, default="testExport-2-records-1-of-1.zip", help="file name of the Diagnosis Keys .zip file")
args = parser.parse_args()

dk_file_name = args.diagnosiskeys
dk = DiagnosisKeys(dk_file_name)


dk_list = [DiagnosisKey(tek.key_data, tek.rolling_start_interval_number, tek.rolling_period, tek.transmission_risk_level) for tek in dk.get_keys()]

print("approximated user count:")
count_users(dk_list)
