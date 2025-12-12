"""
DICOM data models for handling DICOM files and series.
"""
import os
from typing import List, Dict, Any, Optional, Generator
import pydicom
from pydicom.dataset import FileDataset


class DICOMInstance:
    """
    Represents a single DICOM file instance.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._dataset: Optional[FileDataset] = None

    @property
    def dataset(self) -> FileDataset:
        """
        Lazy-load the DICOM dataset.
        
        Returns:
            FileDataset: The pydicom dataset object
        """
        if self._dataset is None:
            try:
                self._dataset = pydicom.dcmread(self.filepath)
            except Exception as e:
                print(f"Error reading DICOM file {self.filepath}: {e}")
                raise
        return self._dataset

    def get_tag(self, tag: str) -> Any:
        """
        Get a DICOM tag value from the dataset.
        
        Args:
            tag: DICOM tag name
            
        Returns:
            Tag value or None if not found
        """
        try:
            return getattr(self.dataset, tag, None)
        except Exception as e:
            print(f"Error getting tag {tag} from {self.filepath}: {e}")
            return None


class Series:
    """
    Represents a DICOM series containing multiple instances.
    """
    def __init__(self, series_uid: str, folder_name: str = None):
        self.series_uid = series_uid
        self.folder_name = folder_name
        self.instances: List[DICOMInstance] = []

    def add_instance(self, instance: DICOMInstance) -> None:
        """
        Add a DICOM instance to this series.
        
        Args:
            instance: DICOMInstance to add
        """
        self.instances.append(instance)

    def get_dicom_tag(self, tag: str) -> Any:
        """
        Get a DICOM tag value from the first instance in the series.
        
        Args:
            tag: DICOM tag name
            
        Returns:
            Tag value or None if series is empty
        """
        if not self.instances:
            return None
        return self.instances[0].get_tag(tag)


class DICOMDirectory:
    """
    DICOMDirectory traverses a given directory to find DICOM files, and
    groups them into Series based on SeriesInstanceUID per folder.
    """

    def __init__(self, directory: str):
        """
        :param directory: Path to the directory where DICOM files are stored.
        """
        self.directory = directory
      # or however you obtain your logger

    def get_dicom_series(self) -> Generator["Series", None, None]:
        """
        Traverse each folder in the directory, gather files into series, and yield 
        the series for that folder. This ensures we do not load the entire directory's 
        DICOM files into memory at once.
        """
        for root, _, files in os.walk(self.directory):
            # For each folder, gather Series objects from all DICOM files in it
            series_dict = self._gather_series_from_files(root, files)

            # Yield the series for this folder before moving on
            yield from series_dict.values()

    def _gather_series_from_files(
        self, root: str, files: List[str]
    ) -> Dict[str, "Series"]:
        """
        Given a folder path (root) and a list of files, this function:
          1. Attempts to read each file as a DICOM instance.
          2. Organizes them by SeriesInstanceUID in a dictionary.

        :param root: Path to the current folder being scanned.
        :param files: List of filenames in the current folder.
        :return: A dictionary {series_uid: Series} for all files in this folder.
        """
        series_dict: Dict[str, Series] = {}
        
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                instance = DICOMInstance(filepath)
                series_uid = instance.get_tag('SeriesInstanceUID')
                if series_uid:
                    if series_uid not in series_dict:
                        series_dict[series_uid] = Series(series_uid)
                    series_dict[series_uid].add_instance(instance)
            except Exception as exc:
                self.logger.warning(f"Skipping file {filepath}: {exc}")

        return series_dict