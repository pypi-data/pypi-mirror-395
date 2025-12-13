from setuptools import setup
from setuptools.command.install import install
# from setuptools.command.develop import develop
# from setuptools.command.egg_info import egg_info
import platform

import os
import glob


def custom_command():
    CUR_OS = platform.system()
    assert CUR_OS == 'Linux', f"What is '{CUR_OS}'? Only Linux is currently supported 🤗"

    SHAREDOBJ_TEMPLATE = {
        'Windows': "ringo_base.cp{py_ver}-win_amd64.pyd",
        'Linux': "ringo_base.cpython-{py_ver}*-x86_64-linux-gnu.so",
    }
    # Python version specifics
    python_version_tuple = platform.python_version_tuple()
    py_ver = int(f"{python_version_tuple[0]}{python_version_tuple[1]}")

    ringo_so_list = glob.glob(
        os.path.join('./ringo',
                     SHAREDOBJ_TEMPLATE[CUR_OS].format(py_ver=py_ver)))
    assert len(ringo_so_list) == 1, (
        f"Unable to run on Python version {python_version_tuple}. Please, report this."
    )
    ringo_object_name = os.path.basename(ringo_so_list[0])

    for file in glob.glob('./ringo/*.pyd') + glob.glob('./ringo/*.so'):
        if os.path.basename(file) != ringo_object_name:
            os.remove(file)


class InstallCommand(install):

    def run(self):
        custom_command()
        install.run(self)


# class DevelopCommand(develop):
#
#     def run(self):
#         custom_command()
#         develop.run(self)
#
#
# class EggInfoCommand(egg_info):
#
#     def run(self):
#         custom_command()
#         egg_info.run(self)

setup(
    cmdclass={
        'install': InstallCommand,
        # 'develop': DevelopCommand,
        # 'egg_info': EggInfoCommand,
    }, )
