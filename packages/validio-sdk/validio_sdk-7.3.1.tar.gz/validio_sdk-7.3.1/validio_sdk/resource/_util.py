from dataclasses import dataclass
from typing import Any

from gql.transport.exceptions import TransportServerError


@dataclass
class SourceSchemaReinference:
    source_names: set[str] | None

    def should_reinfer_schema_for_source(self, source_name: str) -> bool:
        if self.source_names is None:
            return False
        if len(self.source_names) == 0:  # ReInfer for all
            return True
        return source_name in self.source_names


def _sanitized_error_str(e: Exception, show_secrets: bool) -> str:
    """Sanitize error and return string.

    This method **does not** raise any exception but returns a string
    representation of either the original error or the sanitized version to be
    re-raised.

    :param e: The exception.
    :param show_secrets: If secrets should be shown or not.
    """
    if show_secrets:
        return str(e)

    code = ""
    if isinstance(e, TransportServerError):
        code = f" ({e.code})"

    return (
        f"API error{code}: The error message has been "
        "suppressed because it potentially contains sensitive information; "
        "If you would like to view the error message, run again with --show-secrets"
    )


def _rename_dict_key(d: dict[str, Any], from_key: str, to_key: str) -> None:
    if from_key not in d:
        return

    d[to_key] = d[from_key]
    del d[from_key]
