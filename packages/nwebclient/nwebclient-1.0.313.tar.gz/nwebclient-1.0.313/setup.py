import setuptools

version = "1.0.313"

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="nwebclient",
        version=version,
        author="Bjoern Salgert",
        author_email="bjoern.salgert@hs-duesseldorf.de",
        description="NWebClient via HTTP",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://bsnx.net/4.0/group/pynwebclient",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [
                'nx-sdb = nwebclient.sdb:main',
                'nx-sdb-count =  nwebclient.sdb:count',
                'nx-c =  nwebclient:main',
                'nx-gcode =  nwebclient.machine:main',
                'npy =  nwebclient.nx:main',
                'npy-ticker = nwebclient.ticker:main'
            ],
            'nweb_ticker': [ # https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/advanced_pylons/entry_points_and_plugins.html
                 'info-ticker = nwebclient.ticker:InfoTicker' 
            ],
            'nweb_runner': [
                'tokenize = nwebclient.runner:Tokenizer',
                'mqttsend = nwebclient.runner:MqttSend',
                'gcode = nwebclient.runner:GCodeExecutor',
                'llm = nwebclient.llm:LlmExecutor',
                'named = nwebclient.runner:NamedJobs',
                'if = nwebclient.runner:If',
                'echo = nwebclient.runner:Echo',
                'multi = nwebclient.runner:Multi',
                'failover = nwebclient.runner:FailoverRunner'
            ],
            'nweb_web': [    # Verarbeitung in nwebclient.web.NwFlaskRoutes
                'nwebclient-info = nwebclient.base:WebInfo'
            ],
            'nweb_page': [

            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            "usersettings>=1.0.7",
            "requests>=2.0.0",
            "pillow>=8.4.0",
            "seaborn",
            "pandas"
        ]
    )
