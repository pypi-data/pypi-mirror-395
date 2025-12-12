#!/usr/bin/env python
# coding=utf-8
import os
import argparse

from .project import BaseProject, PyQtProject, CythonProject, PackageProject, DockerProject, CommonProject
from .schema import ContentMiddleware
from PyProject3 import __version__

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

all_commands = "py-project, pyqt-project, cython-project, package-project, docker-project, common-project"

def create_dir(abs_filename):
    """
    创建目录，如果目录不存在。
    :param abs_filename: 绝对路径。
    :return:
    """
    created = False
    if not os.path.exists(abs_filename):
        print(f'created: {abs_filename}')
        os.makedirs(abs_filename)
        created = True
    return created


def create_file(abs_filename, content):
    path, filename = os.path.split(abs_filename)
    create_dir(path)
    if filename and not os.path.exists(abs_filename):
        print(f'created: {abs_filename}')
        with open(abs_filename, 'w+', encoding='utf-8') as fid:
            fid.write(content)


def get_args(_type, type_list=[], example_msg=""):
    parser = argparse.ArgumentParser(description=f'创建{_type}项目模板，版本:{__version__}。\n{example_msg}')
    parser.add_argument('-n', '--name', type=str, help='项目名称')
    parser.add_argument('-r', '--root', default='.', type=str, help='项目路径')
    if len(type_list) > 0:
        type_list_str = ",".join(type_list)
        default_type = type_list[0]
        parser.add_argument('-t', '--type', default=default_type, type=str, help=f"可选{type_list_str}")
    args = parser.parse_args()
    print(args)
    return args


def create_base_project():
    args = get_args('Python Package',
                    example_msg=f"""
    示例:
    # 创建一个Python Package项目
    py-project -n pypackage_demo

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    p = BaseProject(name=name, root_dir=root)
    p.create()
    return p

def create_package_project():
    args = get_args('Python Package',
                    example_msg="""
    示例:
    package-project -n package_demo

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    p = PackageProject(name=name, root_dir=root)
    p.create()
    return p

def create_pyqt_project():
    args = get_args('PyQt Package',
                    example_msg="""
    示例:
    pyqt-project -n pyqt_demo

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    p = PyQtProject(name=name, root_dir=root)
    p.create()
    return p


def create_cython_project():
    args = get_args('Cython Package',
                    example_msg="""
    示例:
    cython-project -n cython_demo

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    p = CythonProject(name=name, root_dir=root)
    p.create()
    return p

def create_docker_project():
    args = get_args('Docker Project', 
                    type_list=DockerProject.get_all_project_types(),
                    example_msg="""
    示例:
    # 使用模板创建支持docker的项目，可选django、streamlit、mkdocs、supervisor
    docker-project -n django_demo -t django

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    project_type = args.type
    root_dir = os.path.abspath(root)
    p = DockerProject(name=name, root_dir=root_dir, project_type=project_type)
    p.create()
    return p

def create_common_project():
    args = get_args('Common Project', 
                    type_list=CommonProject.get_all_project_types(),
                    example_msg="""
    示例:
    common-project -n rustpy -t rustpy

    其他可用命令: 
    {all_commands}
                    """)
    name = args.name
    root = args.root
    project_type = args.type
    root_dir = os.path.abspath(root)
    p = CommonProject(
        name=name, 
        root_dir=root_dir, 
        project_type=project_type,
        middlewares=[ContentMiddleware(old='__NAME__', new=name)]
    )
    p.create()
    return p

def test():
    p = BaseProject(name='PyProject', root_dir=r'D:\xmov\projects\git.xmov\py-project')
    p.create()


if __name__ == "__main__":
    test()
