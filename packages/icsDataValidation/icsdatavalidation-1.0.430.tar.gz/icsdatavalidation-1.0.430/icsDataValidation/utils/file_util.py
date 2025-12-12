import errno
import os
from typing import Union
import json
import decimal
import numpy as np
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        try:
            super(CustomJSONEncoder, self).default(o)
        except:
            return str(o)

        return super(CustomJSONEncoder, self).default(o)

def load_file(file_path: str, encoding: str = "utf-8-sig") -> str:
    """
        Reads and returns the file content of given path.
        Encodings tried in following order:
                utf-8-sig - default
                utf-8
                utf-16-le
                utf-16
                cp1252
    Args:
        file_path: absolute file path to a file
        encoding: specific code page name
    Raises:
        EnvironmentError - if file could not been read with stated encodings
    Returns:
        File content as string representation
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    else:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except:
            try:
                encoding = "utf-8"
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except:
                try:
                    encoding = "utf-16-le"
                    with open(file_path, "r", encoding=encoding) as file:
                        return file.read()
                except:
                    try:
                        encoding = "utf-16"
                        with open(file_path, "r", encoding=encoding) as file:
                            return file.read()
                    except:
                        try:
                            encoding = "cp1252"
                            with open(file_path, "r", encoding=encoding) as file:
                                return file.read()
                        except:
                            raise EnvironmentError(
                                f"Can not read file {file_path}. Tried utf-8-sig (BOM), utf-8, utf-16, utf-16-le and cp1252."
                            )

def load_json(file_path: str, encoding: str = "utf-8-sig") -> Union[dict, None]:
    """
        Reads amd returns a given json file. Content must be in valid JSON Schema.
        Valid JSON Schema should not have any trailing commas.
        Encodings tried in following order:
                utf-8-sig - default
                utf-8
                utf-16-le
                utf-16
                cp1252
    Args:
        file_path: absolute file path to a file
        encoding: specific code page name
    Raises:
        EnvironmentError - if file could not been read with stated encodings
    Returns:
        File content as dictionary.
        If the file path does not exists None will be returned.
    """
    return json.loads(load_file(file_path, encoding))


def write_json_to_file(json_object: dict, file_path: str) -> None:
    with open(f"{file_path}", 'w') as f:
        json.dump(json_object, f, indent=4, cls=CustomJSONEncoder)