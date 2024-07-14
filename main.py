from pathlib import Path
from service.dicom_service import DicomService
from service.utils import *
from tqdm import tqdm


input_dir = "./input"
output_dir = "./output"
output_extension = ".dcm"
[input_files, input_dirs] = get_all_files_in_dir(input_dir)
output_dirs = convert_to_output_path(input_dirs, input_dir, output_dir)
create_output_dirs(output_dirs)

dicom_service = DicomService("123456", "Patient Name")
for input_file in tqdm(input_files):
    extension = Path(input_file).suffix
    output_file = input_file.replace(input_dir, output_dir).replace(extension, output_extension)
    dicom_service.convert_to_dicom(input_file, output_file)
