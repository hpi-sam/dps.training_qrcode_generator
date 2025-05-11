import os
import shutil
import csv
import copy
import subprocess


# Define variables
CSV_INPUT_LIST = "input/vehicles_generic.csv"
CSV_INPUT_MAPPING = "input/containers_per_vehicle_type.csv"
CSV_INPUT_IDS = "input/containers.csv"
IMG_CONTAINER = "components/img/image_container.pdf"
IMG_APPICON = "components/img/icon_player.png"
TEX_BEGIN = "components/tex_base/begin_a5.tex"
TEX_CONTENT = "components/tex_content/template_container.tex"
TEX_END = "components/tex_base/end.tex"
DIR_WORKING = "output/temp"
DIR_OUTPUT = "output"
OUTPUT_TEX_FILE = "container_a5.tex"
OUTPUT_PDF_FILE = "container_a5.pdf"

# Create output and working directory if not exists
if not os.path.exists(DIR_OUTPUT):
    os.makedirs(DIR_OUTPUT)
if not os.path.exists(DIR_WORKING):
    os.makedirs(DIR_WORKING)

# Copy image files to temp directory
shutil.copy(IMG_APPICON, DIR_WORKING)
shutil.copy(IMG_CONTAINER, DIR_WORKING)

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
        itemset_counter[pk] = 0

# Read MAPPING from CSV file
itemset_demand = {}
with open(CSV_INPUT_MAPPING) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        # Get name and remove from dictionary
        name = row["container"]
        row.pop("container", None)
        # Put data into dictioary (at key name)
        itemset_demand[name] = copy.deepcopy(row)

# Read CSV file entries
with open(CSV_INPUT_LIST) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')

    # Iterate vehicles
    for row in csv_reader:
        # Get vehicle data
        vehicle_type = row[0]
        vehicle_org = row[1]
        vehicle_name = row[2]

        # Iterate over container demand for vehicle
        for container_name in itemset_demand:
            demand = itemset_demand[container_name]
            if not vehicle_type in demand:
                continue
            amount = int(demand[vehicle_type])
            if amount <= 0:
                continue

            # Open template
            input_file = open(TEX_CONTENT)
            input_text = input_file.read()
            input_file.close()

            # Write replace patient data
            pk = itemset_ids[container_name]
            itemset_counter[pk] += 1
            index = itemset_counter[pk]
            temp_text = input_text.replace("<<CONTAINERNAME>>", container_name)
            temp_text = temp_text.replace(
                "<<VEHICLENAME>>", vehicle_org + " " + vehicle_name
            )
            temp_text = temp_text.replace("<<CTYPE>>", pk)
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
