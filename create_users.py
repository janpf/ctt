import sys

sys.path.insert(1, "../diagnosis-keys/")

from lib.diagnosis_keys import *
from lib.diagnosis_key import DiagnosisKey
from lib.count_users import count_users
import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description="Exposure Notification Diagnosis Key Parser.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--diagnosiskeys", type=str, default="testExport-2-records-1-of-1.zip", help="file name of the Diagnosis Keys .zip file")
parser.add_argument("-a", "--auto_multiplier_detect", action="store_true", help="detect the multiplier automatically")
parser.add_argument("-n", "--new-android-apps-only", action="store_true", help="assume that no 'old' Android apps uploaded keys")
parser.add_argument("-m", "--multiplier", type=int, default=10, help="padding multiplier (RANDOM_KEY_PADDING_MULTIPLIER as set on cwa-server)")
args = parser.parse_args()

dk_file_name = args.diagnosiskeys
dk = DiagnosisKeys(dk_file_name)


dk_list = [DiagnosisKey(tek.key_data, tek.rolling_start_interval_number, tek.rolling_period, tek.transmission_risk_level) for tek in dk.get_keys()]

print("approximated user count according to https://github.com/corona-warn-app/cwa-documentation/issues/258#issuecomment-650700745")
print(f"called with: multiplier={args.multiplier}, auto_multiplier_detect={args.auto_multiplier_detect}, new_android_apps_only={args.new_android_apps_only}")
count_users(dk_list, auto_multiplier_detect=args.auto_multiplier_detect, multiplier=args.multiplier, new_android_apps_only=args.new_android_apps_only)
