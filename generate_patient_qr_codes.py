import os
import shutil
import csv
import subprocess


# Define variables
CSV_INPUT = "input/patients.csv"
IMG_PATIENT = "components/img/image_patient.pdf"
IMG_APPICON = "components/img/icon_player.png"
TEX_BEGIN = "components/tex_base/begin_a4.tex"
TEX_CONTENT = "components/tex_content/template_patient.tex"
TEX_CONTENT_EXTRA = "components/tex_content/block_patient_walking.tex"
TEX_END = "components/tex_base/end.tex"
DIR_WORKING = "output/temp"
DIR_OUTPUT = "output"
OUTPUT_TEX_FILE = "patient_a4.tex"
OUTPUT_PDF_FILE = "patient_a4.pdf"

# Create output and working directory if not exists
if not os.path.exists(DIR_OUTPUT):
    os.makedirs(DIR_OUTPUT)
if not os.path.exists(DIR_WORKING):
    os.makedirs(DIR_WORKING)

# Copy image files to temp directory
shutil.copy(IMG_APPICON, DIR_WORKING)
shutil.copy(IMG_PATIENT, DIR_WORKING)

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

# Read CSV file entries
with open(CSV_INPUT) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        # Get patient data
        patient_number = row[0]
        patient_set = row[1]
        state_intitial = row[2]
        state_progression = row[3]
        patient_can_walk = bool(row[4])

        # Open template
        input_file = open(TEX_CONTENT)
        input_text = input_file.read()
        input_file.close()

        # Write replace patient data
        temp_text = input_text.replace("<<NUMBER>>", patient_number)
        temp_text = temp_text.replace("<<SET>>", patient_set)
        temp_text = temp_text.replace("<<INITIAL>>", state_intitial)
        temp_text = temp_text.replace("<<PROGRESSION>>", state_progression)

        # Add "can walk" information to patient
        if patient_can_walk:
            extra_input_file = open(TEX_CONTENT_EXTRA)
            extra_input_text = extra_input_file.read()
            extra_input_file.close()
            temp_text = temp_text.replace("<<EXTRABLOCK>>", extra_input_text)
        else:
            temp_text = temp_text.replace("<<EXTRABLOCK>>", "")

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
