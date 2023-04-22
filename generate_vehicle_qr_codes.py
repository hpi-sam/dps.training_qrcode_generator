import os
import shutil
import csv
import subprocess


# Define variables
CSV_INPUT_LIST = "input/vehicles.csv"
CSV_INPUT_IDS = "input/containers.csv"
IMG_VEHICLE = "components/img/image_vehicle.pdf"
IMG_APPICON = "components/img/icon_player.png"
TEX_BEGIN = "components/tex_base/begin_a4.tex"
TEX_CONTENT = "components/tex_content/template_vehicle.tex"
TEX_END = "components/tex_base/end.tex"
DIR_WORKING = "output/temp"
DIR_OUTPUT = "output"
OUTPUT_TEX_FILE = "vehicle_a4.tex"
OUTPUT_PDF_FILE = "vehicle_a4.pdf"

# Create output and working directory if not exists
if not os.path.exists(DIR_OUTPUT):
    os.makedirs(DIR_OUTPUT)
if not os.path.exists(DIR_WORKING):
    os.makedirs(DIR_WORKING)

# Copy image files to temp directory
shutil.copy(IMG_APPICON, DIR_WORKING)
shutil.copy(IMG_VEHICLE, DIR_WORKING)

# Create output files (delete previous files if exists)
output_tex_path = os.path.join(DIR_WORKING, OUTPUT_TEX_FILE)
if os.path.exists(output_tex_path):
    os.remove(output_tex_path)
output_file = open(output_tex_path, "w")

# Add latex header to ouput file
input_file = open(TEX_BEGIN)
input_text = input_file.read()
output_file.write(input_text)
input_file.close()

# Read IDs from CSV file
itemset_ids = {}
itemset_counter = {}
with open(CSV_INPUT_IDS) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        # Get data
        name = row[0]
        pk = row[1]
        # Put into dictioary
        itemset_ids[name] = pk
        itemset_counter[name] = 0

# Read CSV file entries
with open(CSV_INPUT_LIST) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        # Get patient data
        vehicle_type = row[0]
        vehicle_org = row[1]
        vehicle_name = row[2]

        # Open template
        input_file = open(TEX_CONTENT)
        input_text = input_file.read()
        input_file.close()

        # Write replace patient data
        itemset_counter[vehicle_type] += 1
        index = itemset_counter[vehicle_type]
        temp_text = input_text.replace("<<NAME>>", vehicle_org + " " + vehicle_name)
        temp_text = temp_text.replace("<<CTYPE>>", itemset_ids[vehicle_type])
        temp_text = temp_text.replace("<<CNUMBER>>", str(index))

        # Write to output file
        output_file.write(temp_text)


# Add latex header to ouput file
input_file = open(TEX_END)
input_text = input_file.read()
output_file.write(input_text)
input_file.close()

# Close output file (it's now finished)
output_file.close()

# RUN LATEX
subprocess.call(["pdflatex", OUTPUT_TEX_FILE], cwd=DIR_WORKING, shell=False)

# Copy result file
output_pdf_path = os.path.join(DIR_WORKING, OUTPUT_PDF_FILE)
shutil.copy(output_pdf_path, DIR_OUTPUT)

# Clean working directory
for working_file_name in os.listdir(DIR_WORKING):
    working_file_path = os.path.join(DIR_WORKING, working_file_name)
    if os.path.isfile(working_file_path):
        os.unlink(working_file_path)
