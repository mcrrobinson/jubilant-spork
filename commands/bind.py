from io import TextIOWrapper
import os
import json
from shamir import Shamir


class HorcruxHeader:
    def __init__(self, originalFilename, timestamp, index, total, threshold, keyFragment) -> None:
        self.originalFilename = originalFilename
        self.timestamp = timestamp
        self.index = index
        self.total = total
        self.threshold = threshold
        self.keyFragment = keyFragment
    originalFilename: str
    timestamp: int
    index: int
    total: int
    threshold: int
    keyFragment: str  # Bytes?


class Horcrux:
    def __init__(self, path: str, header: HorcruxHeader, file: TextIOWrapper) -> None:
        self.path = path
        self.header = header
        self.file = file
    path: str
    header: HorcruxHeader
    file: TextIOWrapper


def get_horcrux_paths_in_dir(dir: str) -> list[str]:
    """Returns a list of paths to horcrux files in a directory."""
    return [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith(".horcrux")]


def get_header_from_horcrux_file(file: TextIOWrapper) -> HorcruxHeader:
    scan_line = False
    for line in file.readlines():
        if scan_line:
            return HorcruxHeader(**json.loads(line.decode().strip()))
        if line == b"-- HEADER --\n":
            scan_line = True


def new_horcrux(path: str) -> Horcrux:
    """Creates a new horcrux file."""
    with open(path, 'rb') as file:
        return Horcrux(path, get_header_from_horcrux_file(file), file)


def validate_horcruxes(horcruxes: list[Horcrux]) -> bool:
    """Validates a horcrux file."""
    if len(horcruxes) == 0:
        print("No horcruxes found.")
        return False

    if len(horcruxes) < horcruxes[0].header.threshold:
        print("Not enough horcruxes to recover.")
        return False

    for horcrux in horcruxes:
        if not horcrux.path.endswith(".horcrux"):
            print("Invalid horcrux file.")
            return False

        if horcrux.header.originalFilename != horcruxes[0].header.originalFilename or horcrux.header.timestamp != horcruxes[0].header.timestamp:
            print(
                "All horcruxes in the given directory must have the same original filename and timestamp.")
            return False

    return True


def file_exists(path: str) -> bool:
    return os.path.exists(path)


def bind(paths: list[str], dest_path: str, overwrite: bool):
    horcruxes = get_horcruxes(paths)
    if not validate_horcruxes(horcruxes):
        print("Invalid horcruxes.")
        return

    first_horcrux = horcruxes[0]

    if dest_path == "":
        cwd = os.getcwd()
        dest_path = os.path.join(cwd, first_horcrux.header.originalFilename)

    if file_exists(dest_path) and not overwrite:
        print("File already exists.")
        return

    key_fragments = [horcrux.header.keyFragment for horcrux in horcruxes]
    key = Shamir.combine(key_fragments)


def get_horcruxes(paths: list[str]) -> list[Horcrux]:
    for path in paths:
        pass


print(new_horcrux("test.horcrux"))
