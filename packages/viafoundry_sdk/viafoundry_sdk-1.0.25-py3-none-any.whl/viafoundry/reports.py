import pandas as pd
import os
import requests
import logging
import io
import mimetypes
from datetime import datetime
from IPython import get_ipython
from typing import Union, Optional, List
from viafoundry.models.domain.reports import (
    ReportData,
    MultiReportData,
    FileUploadRequest,
    FileUploadResponse,
    ReportDirectory,
    ReportPathsResponse
)


class Reports:
    """
    A class for managing reports in the ViaFoundry API.

    Attributes:
        client (ViaFoundryClient): The client instance to interact with the API.
        enable_session_history (bool): Whether session history is enabled for reports.
    """

    def __init__(self, client, enable_session_history: bool = False) -> None:
        """
        Initializes the Reports class.

        Args:
            client (ViaFoundryClient): The client instance to interact with.
            enable_session_history (bool): Whether to enable session history for reports. Defaults to False.
        """
        self.client = client
        self.enable_session_history = enable_session_history

    def fetch_report_data(self, report_id: str) -> MultiReportData:
        """
        Fetches JSON data for a report and injects `file_dir` into all entries.

        Args:
            report_id (str): The ID of the report to fetch data for.

        Returns:
            MultiReportData: The fetched report data with injected file paths as a Pydantic model.

        Raises:
            RuntimeError: If fetching report data fails.
        """
        try:
            endpoint = f"/api/run/v1/{report_id}/reports/"
            report_data = self.client.call("GET", endpoint)

            # Recursively add `file_dir` to all entries
            def add_file_path(data):
                for entry in data:
                    # Inject `file_dir` into the current entry
                    entry["file_path"] = (
                        entry["routePath"].split("pubweb/")[-1]
                        if "pubweb/" in entry["routePath"]
                        else None
                    )
                    # Recursively process children if they exist
                    if "children" in entry and isinstance(entry["children"], list):
                        add_file_path(entry["children"])

            add_file_path(report_data.get("data", []))
            return MultiReportData.model_validate(report_data)
        except Exception as e:
            self._raise_error(
                601, f"Failed to fetch report data for report ID '{report_id}': {e}"
            )

    def get_process_names(self, report_data: Union[dict, MultiReportData]) -> list:
        """
        Gets unique process names from report data.

        Args:
            report_data (Union[dict, MultiReportData]): The report data containing process entries.

        Returns:
            list: A list of unique process names.

        Raises:
            RuntimeError: If extracting process names fails.
        """
        try:
            if isinstance(report_data, MultiReportData):
                data_entries = [entry.model_dump()
                                for entry in report_data.data]
            else:
                data_entries = report_data["data"]

            return list({entry.get("processName") for entry in data_entries})
        except Exception as e:
            self._raise_error(602, f"Failed to extract process names: {e}")

    def get_file_names(self, report_data: Union[dict, MultiReportData], process_name: str) -> pd.DataFrame:
        """
        Gets file names for a specific process, including files in nested directories.

        Args:
            report_data (Union[dict, MultiReportData]): The report data containing file entries.
            process_name (str): The name of the process to get file names for.

        Returns:
            pd.DataFrame: A DataFrame containing file names and metadata for the specified process.

        Raises:
            RuntimeError: If extracting file names fails.
        """
        try:
            if isinstance(report_data, MultiReportData):
                data_entries = [entry.model_dump()
                                for entry in report_data.data]
            else:
                data_entries = report_data["data"]

            # Find all entries for the given process
            processes = [
                entry
                for entry in data_entries
                if entry.get("processName") == process_name
            ]
            if not processes:
                self._raise_error(603, f"Process '{process_name}' not found.")

            # Recursively collect all files from children
            def collect_files(children):
                files = []
                for child in children:
                    if child.get("extension") == "dir" and "children" in child:
                        files.extend(collect_files(child["children"]))
                    else:
                        files.append(child)
                return files

            all_files = collect_files(processes[0].get("children", []))

            if not all_files:
                self._raise_error(
                    604, f"No files found for process '{process_name}'.")

            return pd.DataFrame(all_files)[
                [
                    "id",
                    "processName",
                    "name",
                    "extension",
                    "file_path",
                    "fileSize",
                    "routePath",
                ]
            ]
        except Exception as e:
            self._raise_error(
                604, f"Failed to get file names for process '{process_name}': {e}"
            )

    def load_file(
        self, json_data: Union[dict, MultiReportData], file_path: str, sep: str = "\t"
    ) -> Union[pd.DataFrame, str]:
        """
        Loads or downloads a file from a process.

        Args:
            json_data (Union[dict, MultiReportData]): JSON data containing the report.
            file_path (str): The path of the file to load or download.
            sep (str): Separator for tabular files. Defaults to tab character.

        Returns:
            Union[pd.DataFrame, str]: DataFrame if the file is tabular, or raw content for non-tabular files.

        Raises:
            RuntimeError: If loading the file fails.
        """
        try:
            files = self.get_all_files(json_data)
            print(file_path)
            file_details = files[files["file_path"] == file_path]
            file_name = os.path.basename(file_path)

            if file_details.empty:
                self._raise_error(
                    605, f"File '{file_name}' not found in the files of this report."
                )

            file_url = self.client.auth.hostname + \
                file_details["routePath"].iloc[0]
            file_extension = file_details["extension"].iloc[0].lower()

            headers = self.client.auth.get_headers()
            response = requests.get(file_url, headers=headers)

            if response.status_code != 200:
                self._raise_error(
                    606, f"Failed to fetch file: HTTP {response.status_code}"
                )

            # Load as a DataFrame
            content = response.text
            if file_extension in ["csv", "tsv", "txt"]:
                return pd.read_csv(io.StringIO(content), sep=sep)

            return content  # Return raw content for non-tabular files

        except Exception as e:
            self._raise_error(607, f"Failed to load file '{file_name}': {e}")

    def download_file(
        self, report_data: Union[dict, MultiReportData], file_path: str, download_dir: str = os.getcwd()
    ) -> str:
        """
        Downloads a file from the API.

        Args:
            report_data (Union[dict, MultiReportData]): The report data containing file entries.
            file_path (str): The path of the file to download.
            download_dir (str): The directory to save the downloaded file. Defaults to current working directory.

        Returns:
            str: The path to the downloaded file.

        Raises:
            RuntimeError: If downloading the file fails.
        """
        try:
            files = self.get_all_files(report_data)
            file_details = files[files["file_path"] == file_path]
            file_name = os.path.basename(file_path)

            if file_details.empty:
                self._raise_error(
                    608, f"File '{file_name}' not found in the files of this report."
                )

            file_url = self.client.auth.hostname + \
                file_details["routePath"].iloc[0]
            output_path = os.path.join(download_dir, file_name)

            response = requests.get(
                file_url, headers=self.client.auth.get_headers())
            if response.status_code != 200:
                self._raise_error(
                    609, f"Failed to download file: HTTP {response.status_code}"
                )

            with open(output_path, "wb") as file:
                file.write(response.content)

            return output_path
        except Exception as e:
            self._raise_error(
                610, f"Failed to download file '{file_name}': {e}")

    def get_all_files(self, report_data: Union[dict, MultiReportData]) -> pd.DataFrame:
        """
        Extracts all files across all processes for a specific report, including files in nested directories.

        Args:
            report_data (Union[dict, MultiReportData]): JSON data containing the report.

        Returns:
            pd.DataFrame: A DataFrame containing all files with metadata.

        Raises:
            RuntimeError: If extracting files fails.
        """
        try:
            all_files = []

            def collect_files(children, process_name):
                files = []
                for child in children:
                    child["processName"] = process_name
                    if child.get("extension") == "dir" and "children" in child:
                        files.extend(collect_files(
                            child["children"], process_name))
                    else:
                        files.append(child)
                return files

            if isinstance(report_data, MultiReportData):
                data_entries = [entry.model_dump()
                                for entry in report_data.data]
            else:
                data_entries = report_data["data"]

            for entry in data_entries:
                process_name = entry.get("processName")
                if "children" in entry and isinstance(entry["children"], list):
                    all_files.extend(collect_files(
                        entry["children"], process_name))

            if not all_files:
                self._raise_error(611, "No files found in the report.")
            else:
                logging.info(f"Found {len(all_files)} files in the report.")
            return pd.DataFrame(all_files)[
                [
                    "id",
                    "processName",
                    "file_path",
                    "name",
                    "extension",
                    "fileSize",
                    "routePath",
                ]
            ]
        except Exception as e:
            self._raise_error(
                612, f"Failed to extract all files from report: {e}")

    def _raise_error(self, code: int, message: str) -> None:
        """
        Raises a categorized error with a specific code and message.

        Args:
            code (int): The error code.
            message (str): The error message.

        Raises:
            RuntimeError: Always raises a RuntimeError.
        """
        logging.error(f"Error {code}: {message}")  # Log the error
        raise RuntimeError(f"Error {code}: {message}")

    def upload_report_file(
        self, report_id: str, local_file_path: str, dir: Optional[str] = None
    ) -> FileUploadResponse:
        """
        Uploads a file to a specific report.

        Args:
            report_id (str): The ID of the report.
            local_file_path (str): The path to the local file to upload.
            dir (Optional[str]): The directory to upload the file to. Defaults to None.

        Returns:
            FileUploadResponse: Information about the uploaded file.

        Raises:
            RuntimeError: If uploading the file fails.
        """
        try:

            upload_request = FileUploadRequest(
                local_file_path=local_file_path,
                report_id=report_id,
                target_dir=dir
            )

            # Fetch the latest attempt_id if not provided
            report_paths_response = self.get_all_report_paths(report_id)
            attempt_id = (
                report_paths_response.paths[0].split(
                    "/report-resources/")[1].split("/pubweb")[0]
            )

            # Construct the upload endpoint
            upload_endpoint = f"/api/run/v1/{report_id}/reports/upload/{attempt_id}"

            # Guess the MIME type of the file
            mime_type, _ = mimetypes.guess_type(upload_request.local_file_path)
            if not mime_type:
                mime_type = "application/octet-stream"  # Default to binary stream

            # Open the file in binary mode
            filename = upload_request.local_file_path.split("/")[-1]
            with open(upload_request.local_file_path, "rb") as file:
                files = {"file": (filename, file, mime_type)}
                data = {
                    "dir": upload_request.target_dir} if upload_request.target_dir else {}

                # Perform the upload
                response = self.client.call(
                    "POST", upload_endpoint, files=files, data=data
                )

            return FileUploadResponse(
                success=True,
                message=f"File '{filename}' uploaded successfully",
                file_id=response.get("file_id")
            )
        except Exception as e:
            return FileUploadResponse(
                success=False,
                message=f"Failed to upload file to report: {e}",
                file_id=None
            )

    def get_all_report_paths(self, report_id: str) -> ReportPathsResponse:
        """
        Gets unique report directories and attempt IDs for a specific report.

        Args:
            report_id (str): The ID of the report.

        Returns:
            ReportPathsResponse: A structured response containing unique report paths.

        Raises:
            Exception: If the API call fails or no reports are found.
        """
        try:
            # Define the API endpoint
            endpoint = f"/api/run/v1/{report_id}/reports"

            # Call the API to fetch report data
            response = self.client.call("GET", endpoint)
            reports = response.get("data", [])

            if not reports:
                raise ValueError("No reports found.")

            # Extract unique `routePath` entries
            unique_paths = {
                entry.get("routePath") for entry in reports if "routePath" in entry
            }

            return ReportPathsResponse(
                paths=list(unique_paths),
                total_count=len(unique_paths)
            )
        except Exception as e:
            self._raise_error(602, f"Failed to fetch report directories: {e}")

    def get_report_dirs(self, report_id: str) -> list:
        """
        Gets possible directories following 'pubweb' in the routePath.

        Args:
            report_id (str): The ID of the report.

        Returns:
            list: A list of unique directories found after 'pubweb'.

        Raises:
            Exception: If the API call fails or no directories are found.
        """
        try:
            # Get all routePaths for the report
            all_paths_response = self.get_all_report_paths(report_id)

            if not all_paths_response.paths:
                raise ValueError("No reports found.")

            # Extract directories after 'pubweb'
            report_dirs = set()
            for route_path in all_paths_response.paths:
                if "pubweb/" in route_path:
                    dir_after_pubweb = route_path.split("pubweb/")[-1]
                    report_dirs.add(dir_after_pubweb)

            if not report_dirs:
                raise ValueError("No directories found after 'pubweb'.")

            return list(report_dirs)

        except Exception as e:
            self._raise_error(
                603, f"Failed to fetch possible directories: {e}")

    def upload_session_history(self, report_id: str, dir: Optional[str] = None) -> dict:
        """
        Uploads the session history as a standalone file.

        Args:
            report_id (str): The ID of the report.
            dir (Optional[str]): The directory to upload the session history to. Defaults to None.

        Returns:
            dict: Information about the uploaded session history.

        Raises:
            RuntimeError: If uploading the session history fails.
        """
        try:
            if not self.enable_session_history:
                raise RuntimeError(
                    "Session history functionality is disabled.")

            # Prepare session history file
            history_file_path = self.prepare_session_history()
            # Upload session history only if the flag is enabled
            if self.enable_session_history:
                self.upload_report_file(report_id, history_file_path, dir)

            # Clean up the temporary history file
            os.remove(history_file_path)

        except Exception as e:
            raise Exception(f"Failed to upload session history: {e}")

    def prepare_session_history(self) -> str:
        """
        Prepares session history from the current Jupyter or IPython session.

        Returns:
            str: Path to the saved history file.

        Raises:
            Exception: If preparing the session history fails.
        """
        try:
            ipython = get_ipython()
            if ipython is None:
                raise EnvironmentError(
                    "Session history can only be prepared in IPython or Jupyter environments."
                )

            # Generate a filename with the current date and time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            history_file_path = f"session_history_{timestamp}.txt"

            # Save the session history to the file using run_line_magic (recommended)
            ipython.run_line_magic("history", f"-f {history_file_path}")

            return history_file_path
        except Exception as e:
            raise Exception(f"Failed to prepare session history: {e}")
