#%%
import shutil
from setuptools import setup
from setuptools import find_packages
import os

#%% Remove old build directory
build_folder = 'build'
if os.path.exists(build_folder):
    shutil.rmtree(build_folder)

#%% Input section
package_name = 'yafem'
description  = 'Yet Another Finite Element Method (YAFEM) Package'
version      = '1.1.2'
requirements = False 

#%% Load requirements
if requirements == True:
    with open('requirements.txt') as f:
        required = f.read().splitlines()
else:
    required = ('numpy',
                'scipy',
                'jax',
                'jaxlib',
                'matplotlib',
                )

# # Generating license file of the "required"
# generate_license(required)

#%% Exclude redundant files

# all files in the package_name path
yafem_files = os.listdir(package_name + '\\elem')

# dev files
yafem_dev_files = [s for s in yafem_files if "_dev" in s]

# file to generate lamdified functions
yafem_functions = [s for s in yafem_files if "fun_" in s]

# concatinated files to be ignored when packing
exclude_files = yafem_dev_files + yafem_functions + ["testing", "testing.*"]

#%% Setup

setup(
    # setup_requires=['wheel'],
    name = package_name,
    version = version,
    description = description,
    long_description= open('readme_package_description.md').read(),
                    #   + ' \n# Change log of version ' + version + ': \n\n' + \
                    #   open('readme_change_log\\readme_changes_' + version + '.md').read(),             
    install_requires = required,
    packages = find_packages(exclude = exclude_files),
    # package_data={'': ['LICENSE.md','NOTICE.md']},
    package_dir={"yafem": "yafem"},
    license="MIT",            
    license_files=["LICENSE", "NOTICE"],
    )


# #%% Creating a requirements file

# dist_files = os.listdir('dist')
# yafem_wheel = [s for s in dist_files if ".whl" in s and version in s]

# with open('dist\\requirements.txt', 'w') as f:
#     f.write(yafem_wheel[0] + '\n')

# with open('dist\\requirements.txt', 'a') as f:
#     f.write('sympy' + '\n'
#             'numpy' + '\n'
#             'scipy' + '\n'
#             'pandas' + '\n'
#             'jax' + '\n'
#             'jaxlib' + '\n'
#             'matplotlib' + '\n'
#             'ipykernel' + '\n'
#             'mkdocs-material' + '\n'
#             'pipdeptree' + '\n'
#             'gmsh' + '\n'
#             'raschii' + '\n'
#             )