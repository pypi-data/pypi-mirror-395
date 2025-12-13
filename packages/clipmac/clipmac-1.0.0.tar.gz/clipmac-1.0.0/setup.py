import os, sys, setuptools

descx = ''' clipmac is clipbard copy / paste tool '''

classx = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version number from the server support file:
fp = open("clipmacro.py", "rt")
vvv = fp.read(); fp.close()
loc_vers =  '1.0.0'     # Default
for aa in vvv.split("\n"):
    idx = aa.find("VERSION ")
    if idx == 0:        # At the beginning of line
        try:
            loc_vers = aa.split()[2].replace('"', "")
            break
        except:
            pass

#print("loc_vers:", loc_vers) ; sys.exit()

deplist = ["pyvguicom",] ,
includex = [ "*", "clipmac/", "icon.png"]

setuptools.setup(
    name="clipmac",
    version=loc_vers,
    author="Peter Glen",
    author_email="peterglen99@gmail.com",
    description=descx,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglen/clipmac",
    classifiers=classx,
    include_package_data=True,
    packages=setuptools.find_packages(include=includex),
    scripts = ['clipmacro.py'],
    package_dir = { "clipmac" : "clipmac",
                  },
    package_data= { "clipmac" : ("icon.png",),
                  },
    python_requires='>=3',
    install_requires=deplist,
    entry_points={
        'console_scripts': [
            "clipmacro=clipmacro:mainfunc",
            ],
        },
)

# EOF
