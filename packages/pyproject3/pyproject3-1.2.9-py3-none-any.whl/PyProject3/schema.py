from dataclasses import dataclass, field
from typing import List
from PyProject3.utils import create_file, create_dir
import os
from typing import Protocol


class ContentMiddlewareProtocol(Protocol):
    def process(self, content: str) -> str:
        pass


class ContentMiddleware(ContentMiddlewareProtocol):
    def __init__(self, old: str, new: str):
        self.old = old
        self.new = new

    def process(self, content: str) -> str:
        new_content = content.replace(self.old, self.new)
        return new_content


@dataclass
class Dir:
    name: str
    dirs: List['Dir'] = field(default_factory=list)
    files: List['File'] = field(default_factory=list)

    def create(self, base_dir: str = '.', override: bool = False):
        p = os.path.join(base_dir, self.name)
        if os.path.exists(p) and not override:
            raise FileExistsError(f"Directory {p} already exists")
            return
        create_dir(p)
        for dir in self.dirs:
            dir.create(p, override=override)
        for file in self.files:
            file.create(base_dir=p, override=override)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "dirs": [dir.to_dict() for dir in self.dirs],
            "files": [file.to_dict() for file in self.files]
        }
    
    @property
    def dir_count(self) -> int:
        return sum(dir.dir_count for dir in self.dirs) + len(self.dirs)
    
    @property
    def file_count(self) -> int:
        return sum(dir.file_count for dir in self.dirs) + len(self.files)

    @classmethod
    def from_directory(cls, directory: str, override: bool = False, middlewares: List['ContentMiddlewareProtocol'] = []) -> 'Dir':
        root_dir = cls(name=os.path.basename(directory))
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                root_dir.files.append(File.from_file(file_path, override=override, middlewares=middlewares))
            elif os.path.isdir(file_path):
                root_dir.dirs.append(cls.from_directory(file_path, override=override, middlewares=middlewares))
        return root_dir


@dataclass
class File:
    name: str
    content: str
    override: bool = False
    middlewares: List['ContentMiddlewareProtocol'] = field(
        default_factory=list)

    @property
    def processed_content(self):
        content = self.content
        for middleware in self.middlewares:
            content = middleware.process(content)
        return content

    @classmethod
    def from_file(cls, file_path: str, override: bool = False, middlewares: List['ContentMiddlewareProtocol'] = []):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            content = ""
        return cls(name=os.path.basename(file_path),
                   content=content,
                   override=override,
                   middlewares=middlewares if isinstance(content, str) else [])

    def create(self, base_dir: str = '.', override=False):
        content = self.processed_content
        create_file(abs_filename=os.path.join(base_dir, self.name),
                    content=content,
                    override=self.override)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            # "content": self.processed_content,
            "override": self.override,
            #"middlewares": [middleware.to_dict() for middleware in self.middlewares]
        }


@dataclass
class Project:

    # 项目基本信息
    name: str
    # 项目目录结构
    base_dir: str
    root_dir: Dir
    context: dict
    override: bool = True

    # 创建项目
    def create(self):
        self.root_dir.create(self.base_dir, self.override)
