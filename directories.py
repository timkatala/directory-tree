from __future__ import annotations

from collections import deque
from enum import Enum


class DirectoryNotExist(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Directory:
    def __init__(self, name: str = "", parent: Directory | None = None):
        self.name = name
        self.parent = parent
        self.subdirectories = {}

    def create(self, path_dirs: deque[str]) -> None:
        if (dir_ := path_dirs.popleft()) not in self.subdirectories:
            self.subdirectories[dir_] = Directory(name=dir_, parent=self)
        if path_dirs:
            self.subdirectories[dir_].create(path_dirs)

    def move(self, moving_path_dirs, target_path_dirs: deque[str]) -> None:
        moving_dir = self.get_directory(moving_path_dirs)
        target_dir = self.get_directory(target_path_dirs)

        target_dir.subdirectories[moving_dir.name] = moving_dir
        moving_dir.parent.subdirectories.pop(moving_dir.name)

    def delete(self, path_dirs) -> None:
        dir_ = self.get_directory(path_dirs)
        dir_.parent.subdirectories.pop(dir_.name)

    def list_all(self, level: int = -1) -> list[str]:
        result = [] if level == -1 else [" " * level + self.name]
        for _, dir_ in sorted(self.subdirectories.items()):
            result += dir_.list_all(level + 1)
        return result

    def get_directory(self, path: deque[str]) -> Directory:
        if not path:
            return self
        if (dir_ := path.popleft()) not in self.subdirectories:
            raise DirectoryNotExist(value=dir_)
        return self.subdirectories[dir_].get_directory(path)

    @staticmethod
    def parse_path(path) -> deque[str]:
        return deque(path.split("/"))


class Command(str, Enum):
    CREATE = "CREATE"
    MOVE = "MOVE"
    DELETE = "DELETE"
    LIST = "LIST"


def execute(command: Command, directory: Directory, path: str | None = None, target_path: str | None = None) -> None:
    path_dirs = Directory.parse_path(path)
    target_path_dirs = Directory.parse_path(target_path)

    if command == Command.CREATE:
        directory.create(path_dirs)

    if command == Command.MOVE:
        try:
            directory.move(path_dirs, target_path_dirs)
        except DirectoryNotExist as e:
            print(f"Cannot move {path} - {e.value} does not exist")

    if command == Command.DELETE:
        try:
            directory.delete(path_dirs)
        except DirectoryNotExist as e:
            print(f"Cannot delete {path} - {e.value} does not exist")

    if command == Command.LIST:
        print("\n".join(directory.list_all()))


if __name__ == "__main__":
    ROOT = Directory()

    with open("input.txt", "r") as file:
        lines = filter(None, (line.rstrip() for line in file))
        for line in lines:
            print(line)
            command, path, target_path, *_ = line.split() + 2 * [""]
            execute(Command[command], ROOT, path, target_path)
