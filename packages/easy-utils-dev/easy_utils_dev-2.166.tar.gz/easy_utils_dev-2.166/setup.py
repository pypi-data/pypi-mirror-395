from setuptools import setup, find_packages

VERSION = '2.166'

# Setting up
setup(
    name="easy_utils_dev",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            'psutil' ,
            'ping3' , 
            'snakebite-py3',
            'flask' , 
            'flask_cors' , 
            'xmltodict' , 
            'paramiko' ,
            'oracledb' ,
            'requests',
            'flask_socketio',
            'python-dotenv',
            'gevent',
            'pyzipper',
            'pyjwt',
            'authlib',
            'kafka-python'
        ],
    keywords=['python3'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)