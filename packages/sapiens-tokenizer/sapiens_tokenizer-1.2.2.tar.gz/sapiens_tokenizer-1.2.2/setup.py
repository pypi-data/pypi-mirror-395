# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
from setuptools import setup, find_packages
package_name = 'sapiens_tokenizer'
version = '1.2.2'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['tiktoken', 'certifi'],
    url='https://github.com/sapiens-technology/SapiensTokenizer',
    license='Proprietary Software',
    package_data={package_name: ['vocabulary.json']},
    include_package_data=True
)
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
