# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
from setuptools import setup, find_packages
package_name = 'sapiens_tokenizer'
version = '1.2.1'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['tiktoken==0.4.0', 'certifi==2024.2.2'],
    url='https://github.com/sapiens-technology/SapiensTokenizer',
    license='Proprietary Software',
    package_data={package_name: ['vocabulary.json']},
    include_package_data=True
)
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
