from PIL import Image
from pydicom.dataset import FileDataset
import datetime
import numpy as np
import pydicom


class DicomService(object):

    def __init__(self, patient_id: str, patient_name: str, modality: str = "OT"):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.modality = modality

    def convert_to_dicom(self, input_path: str, output_path: str):
        # Load the JPEG image
        image = Image.open(input_path)
        image = image.convert('L')  # Convert to grayscale
        pixel_array = np.asarray(image)
        rows, cols = pixel_array.shape

        # File meta information
        file_meta = pydicom.dataset.FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
        file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID
        file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

        # Create the FileDataset instance (initially no data elements, but has file meta)
        ds = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

        # Add the necessary DICOM data elements
        ds.PatientID = self.patient_id
        ds.PatientName = self.patient_name
        ds.Modality = self.modality
        ds.SeriesInstanceUID = pydicom.uid.generate_uid()
        ds.StudyInstanceUID = pydicom.uid.generate_uid()
        ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
        ds.ContentDate = datetime.date.today().strftime('%Y%m%d')
        ds.ContentTime = datetime.datetime.now().strftime('%H%M%S.%f')

        # Image pixel data
        ds.Rows = rows
        ds.Columns = cols
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.PixelData = pixel_array

        # Set additional metadata if necessary
        ds.is_little_endian = True
        ds.is_implicit_VR = True

        # Save the DICOM file
        ds.save_as(output_path)
