#!/usr/bin/env python3
import sys

sys.path.insert(1, "../diagnosis-keys/")

from lib.diagnosis_keys import *
from lib.conversions import *
import argparse
import struct
from lib.count_users import count_users

parser = argparse.ArgumentParser(description="Exposure Notification Diagnosis Key Parser.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--diagnosiskeys", type=str, default="testExport-2-records-1-of-1.zip", help="file name of the Diagnosis Keys .zip file")
parser.add_argument("-l", "--localtime", action="store_true", help="display timestamps in local time (otherwise the default is UTC)")
parser.add_argument("-u", "--usercount", action="store_true", help="count the number of users who submitted Diagnosis Keys")
args = parser.parse_args()

dk_file_name = args.diagnosiskeys
dk = DiagnosisKeys(dk_file_name)

print("{")

start_timestamp = dk.get_upload_start_timestamp()
end_timestamp = dk.get_upload_end_timestamp()
if args.localtime:
    start_timestamp = get_local_datetime(start_timestamp)
    end_timestamp = get_local_datetime(end_timestamp)

print(f'"timeWindowStart":"{get_string_from_datetime(start_timestamp)}",')
print(f'"timeWindowEnd":"{get_string_from_datetime(end_timestamp)}",')
print(f'"region":"{dk.get_region()}",')
print(f'"batchNum":{dk.get_batch_num()},')
print(f'"batchCount":{dk.get_batch_size()},')

print('"signatureInfos":{')
for signature_info in dk.get_signature_infos():
    for line in str(signature_info).split("\n"):
        line = line.strip()
        if line:
            print(f'"{line.split(":")[0]}":{line.split(":")[1]},')
        else:
            print("{}")
print("},")
print('"diagnosisKeys":[{')
i = 0
for tek in dk.get_keys():
    i += 1
    start_timestamp = get_datetime_from_utc_timestamp(get_timestamp_from_interval(tek.rolling_start_interval_number))
    end_timestamp = get_datetime_from_utc_timestamp(get_timestamp_from_interval(tek.rolling_start_interval_number + tek.rolling_period))
    if args.localtime:
        start_timestamp = get_local_datetime(start_timestamp)
        end_timestamp = get_local_datetime(end_timestamp)
    print(f'"num":{i},')
    print(f'"TemporaryExposureKey":"{tek.key_data.hex()}",')
    print(f'"transmissionRiskLevel":{tek.transmission_risk_level},')
    print('"validity":{')
    print(f'"start":"{get_string_from_datetime(start_timestamp)}",')
    print(f'"end":"{get_string_from_datetime(end_timestamp)}",')
    print(f'"rollingStartIntervalNumber":{tek.rolling_start_interval_number},')
    print(f'"rollingPeriod":{tek.rolling_period}')
    print("}},{")
print("}]")
print("}")
