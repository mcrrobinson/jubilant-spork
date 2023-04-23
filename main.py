from __future__ import annotations
import os
from sys import argv
from datetime import datetime
from random import randbytes
import json

BYTE_QUOTA = 100

class Demultiplexer:
    def __init__(self, Writers: list[os.FileIO], WriterIndex: int = None, BytesWritten: int = None) -> None:
        self.Writers = Writers
        self.WriterIndex = WriterIndex
        self.BytesWritten = BytesWritten

    def nextWriter(self):
        self.WriterIndex += 1
        if self.writerIndex > len(self.Writers) - 1:
            self.WriterIndex = 0

        self.BytesWritten = 0

    def Write(self, p: bytearray) -> int:
        totalN = 0
        while totalN < len(p):
            remainingBytes = len(p) - totalN
            remainingBytesForWriter = BYTE_QUOTA - self.BytesWritten
            n = self.Writers[self.WriterIndex].write(
                p[totalN:totalN + min(remainingBytesForWriter, remainingBytes)])
            self.BytesWritten += n
            totalN += n

            if remainingBytesForWriter - n <= 0:
                self.nextWriter()

        return len(p)

    Writers: list[os.FileIO]
    WriterIndex: int
    BytesWritten: int


class HorcruxHeader:
    def __init__(self, OriginalFilename: str, Timestamp: datetime, Index: int, Total: int, Threshold: int, KeyFragment: bytearray) -> None:
        self.OriginalFilename = OriginalFilename
        self.Timestamp = Timestamp
        self.Index = Index
        self.Total = Total
        self.Threshold = Threshold
        self.KeyFragment = KeyFragment

    OriginalFilename: str
    Timestamp: datetime
    Index: int
    Total: int
    Threshold: int
    KeyFragment: bytearray


class Horcrux:
    path: str
    header: HorcruxHeader
    file: os.FileIO
    
class u8int(int):
    def __new__(cls, value: int) -> u8int:
        if value < 0 or value > 255:
            raise ValueError("u8int must be between 0 and 255")

        return super().__new__(cls, value)

    def __init__(self, value: int) -> None:
        super().__init__(value)


def header(index: int, total: int, headerBytes: bytearray) -> str:
    return ("""# THIS FILE IS A HORCRUX.
# IT IS ONE OF %d HORCRUXES THAT EACH CONTAIN PART OF AN ORIGINAL FILE.
# THIS IS HORCRUX NUMBER %d.
# IN ORDER TO RESURRECT THIS ORIGINAL FILE YOU MUST FIND THE OTHER %d HORCRUX(ES) AND THEN BIND THEM USING THE PROGRAM FOUND AT THE FOLLOWING URL
# https://github.com/jesseduffield/horcrux

-- HEADER --
%s
-- BODY --
""", total, index, total-1, headerBytes)


def getHorcruxes(paths: list[str]) -> list[Horcrux]:
    pass


def getHorcruxPathsInDir(dir: str) -> list[str]:
    # Read directory
    files = os.listdir(dir)
    if not files:
        return []

    paths = []
    for file in files:
        if file.endswith(".horcrux"):
            paths.append(os.path.join(dir, file))

    return paths


def bind(paths: list[str], dstPath: str, overwrite: bool):
    horcruxes = getHorcruxes(paths)
    if not horcruxes:
        raise Exception("No horcruxes found")

    validateHorcruxes(horcruxes)

    firstHorcrux = horcruxes[0]

    if dstPath == "":
        cwd = os.getcwd()
        dstPath = os.path.join(cwd, firstHorcrux.header.OriginalFilename)


def cryptoReader(file: os.FileIO, key: bytearray):
    pass


def generateKey() -> bytearray:
    """ Generates a list of size 8 of u8ints

    Returns:
        bytearray: list[u8int]
    """    
    return bytearray(randbytes(8))


def split(path: str, destination: str, total: int, threshold: int):
    key = generateKey()
    if not key:
        print("Failed to generate key")

    keyFragments = shamir.Split(key, total, threshold)
    if not keyFragments:
        print("Failed to split key")

    timestamp = datetime.now()
    file = open(path, "rb")
    if not file:
        print("Failed to open file")
        return

    originalFilename = os.path.basename(path)
    stat = os.stat(path)
    if not stat:
        print("Failed to get file stats")
        return

    if not os.path.isdir(path):
        print("Destination must be a directory")
        return

    horcruxFiles = []
    for i in range(total):
        index = i + 1
        headerBytes = json.dumps(HorcruxHeader(
            originalFilename,
            timestamp,
            index,
            total,
            keyFragments,
            threshold).__dict__)
        if not headerBytes:
            print("Failed to serialize header")
            return

        originalFilenameWithoutExt = os.path.splitext(originalFilename)[0]
        horcruxFilename = f"{originalFilenameWithoutExt}_{index}_of_{total}.horcrux"
        horcruxPath = os.path.join(destination, horcruxFilename)
        print(f"Creating horcrux {index} of {total} at {horcruxPath}")

        # Clearing file in case it already exists
        _ = os.truncate(horcruxPath, 0)

        with open(horcruxPath, "wb") as horcruxFile:
            horcruxFile.write(header(index, total, headerBytes))

        horcruxFiles[i] = horcruxFile

    fileReader = file

    # TODO: Needs to be completed...
    reader = cryptoReader(file, key)

    # var writer io.Writer
    if threshold == total:
        writer = Demultiplexer(horcruxFiles)
    else:
        writers = []
        for i in range(writers):
            writers[i] = horcruxFiles[i]

        writer = Multiwriter(writers)


def splitWithPrompt(path: str) -> str:
    total, threshold = obtainTotalAndThreshold()
    return split(path, os.path.dirname(path), total, threshold)


def main(kwargs: list):
    if len(kwargs) < 2:
        usage()
        return

    if kwargs[1] == "bind":
        if len(kwargs) == 2:
            dir = '.'
        else:
            dir = kwargs[2]

        paths = getHorcruxPathsInDir(dir)
        overwrite = False
        while True:
            try:
                bind(paths, "", overwrite)
            except Exception as err:
                print(err)
                overwrite_response = input("Overwrite existing files? (y/n): ")
                if overwrite_response.lower() == "y":
                    overwrite = True
                else:
                    print("Exiting...")
            else:
                break

        return

    elif kwargs[1] == "split":
        if len(kwargs) == 2:
            print("Please enter a valid file path")
            return

        path = kwargs[2]
        if err := splitWithPrompt(path):
            print(err)

        return

    usage()


def usage():
    print("usage: `horcrux bind [<directory>]` | `horcrux [-t] [-n] split <filename>`\n-n: number of horcruxes to make\n-t: number of horcruxes required to resurrect the original file\nexample: horcrux -t 3 -n 5 split diary.txt")


if __name__ == '__main__':
    main(argv)
