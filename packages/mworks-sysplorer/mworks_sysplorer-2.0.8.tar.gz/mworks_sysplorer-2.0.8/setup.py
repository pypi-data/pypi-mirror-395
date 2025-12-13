from setuptools import setup, find_packages
setup(
    name='mworks_sysplorer',
    version='2.0.8',
    packages=find_packages(),
    package_data={
        '':['*.ini'],
    },
    author='lipy@TongYuan',
    author_email='lipy@tongyuan.cc',
    description='This is a Sysplorer API by Tong Yuan.',
    install_requires=[
    'websocket-client',
    'jsonrpcclient',
    'colorama',
    'psutil'],
    python_requires='>=3.7,<3.12',
    entry_points={
        'console_scripts': [
            'StartSysplorer=mworks.sysplorer:StartSysplorer',
        ],
    },
)
