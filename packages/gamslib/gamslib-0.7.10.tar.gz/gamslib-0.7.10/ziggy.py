import os
import sys 
import pprint

from pygfried import identify

data_dir = sys.argv[1]
result = []
for filename in os.listdir(data_dir):
    filepath = os.path.join(data_dir, filename)
    if os.path.isfile(filepath) and not filename.startswith('.'):
        try:
            data = identify(filepath, detailed=True)
            fileinfo = data["files"][0]["matches"][0] 
            if fileinfo:
                mime_type = fileinfo.get("mime", "application/undefined")
                pronom_id = fileinfo.get("id", "N/A")

            result.append(f"{filename},{mime_type},{pronom_id},")
        except Exception as e:
            print(f"====> {filename},ERROR,{str(e)}")

result.sort()
for line in result:
    print(line)