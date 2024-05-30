# SPLIT THE ETAG DATA BASED ON 'GPW' OR 'DIG' SOURCE

def separate_data(input_file, output_gpw, output_dig):
    data_gpw = []
    data_dig = []

    with open(input_file, 'r') as f:
        for line in f:
            if "GPW" in line:
            # Keep the first ';' and replace the others with ','
                modified_line = line.strip().split(";", 1)[0] + ";" + line.strip().split(";", 1)[1].replace(";", ",")
                data_gpw.append(modified_line)
            elif "DIG" in line:
                data_dig.append(line.strip())

        with open(output_gpw, "w") as f:
            for row in data_gpw:
                f.write(row + "\n")

        with open(output_dig, "w") as f:
            for row in data_dig:
                f.write(row + "\n")

# Sources
import os
path = os.path.dirname(__file__)
os.chdir(path)

input_file = "2024-03-20_LTU22.log"
output_gpw = "2024-03-20_LTU22_GPW.log"
output_dig = "2024-03-20_LTU22_DIG.log"

separate_data(input_file, output_gpw, output_dig)

