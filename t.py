import os
import json


mapping_file_path = "/home/djlee/deep/github/vision_project/bacekend/model/label.txt"

with open(mapping_file_path) as f:
    txt = f.readlines()

dic = {}
for idx, t in enumerate(txt):
    dic[idx] = t.strip()

# JSON 파일 저장
with open("data.json", "w") as f:
    json.dump(dic, f, indent=4)

print("JSON 파일 저장 완료!")
