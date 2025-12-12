from ts_cli.errors.critical_error import CriticalError
from ts_cli.util.emit import emit_error
import os

from .validator import Validator

data_app_size_override_envvar = "OVERRIDE_DATA_APP_SIZE_BYTES"


def bytes_as_human_readable_string(num_bytes: float, decimals: int = 1) -> str:
    """Return the file size as a human-readable string."""
    for unit in ["", "Ki", "Mi", "Gi", "Ti"]:
        if abs(num_bytes) < 1024.0:
            return f"{round(num_bytes, ndigits=decimals):.{decimals}f} {unit}B"
        num_bytes /= 1024.0
    return f"{round(num_bytes, ndigits=decimals):.{decimals}f} YiB"


class UploadValidator(Validator):
    """
    Check whether given file(s) or other data may be uploaded to Tetra Data Platform.
    """

    def __init__(
        self,
        *,
        artifact_type: str,
        upload_content: bytes = None,
        exiting: bool = False,
    ) -> None:
        self.artifact_type = artifact_type
        self.upload_content = upload_content
        super().__init__(exiting=exiting)

    def max_upload_size(self) -> int:
        default_data_app_size = 2000 * 1024 * 1024

        if self.artifact_type == "data-app":
            if data_app_size_override_envvar in os.environ:
                try:
                    file_size = int(os.environ[data_app_size_override_envvar])
                    if file_size > 10000:
                        emit_error(
                            f"{data_app_size_override_envvar} value is too large. Override cannot be larger than 10 GB"
                        )
                        return default_data_app_size

                    return file_size * 1024 * 1024
                except:
                    emit_error(
                        f"{data_app_size_override_envvar} is not a valid integer."
                    )
                    return default_data_app_size
            else:
                return default_data_app_size

        if self.artifact_type == "connector":
            return default_data_app_size

        return 50 * 1024 * 1024

    def validate(self) -> bool:
        max_upload_size = self.max_upload_size()
        file_size = len(self.upload_content)
        if file_size > max_upload_size:
            friendly_file_size = bytes_as_human_readable_string(file_size)
            friendly_max_file_size = bytes_as_human_readable_string(max_upload_size)
            friendly_excess = bytes_as_human_readable_string(
                file_size - max_upload_size
            )

            emit_error(
                f"File exceeded upload limit of ~{friendly_max_file_size} "
                + f"by ~{friendly_excess}. Actual file size: {friendly_file_size}"
            )

            if self._exiting:
                raise CriticalError("Exiting")
            return False
        return True
