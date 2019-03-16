import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

#required_package = ['numpy', 'pandas', 'seaborn', 'matplotlib',
#'scipy', 'plotly', 'researchpy', 'statsmodels', 'squarify']

required_package = ['pandas', 'oauth2client', 'httplib2',
 'google-api-python-client', 'google-api-core', 'google-cloud-storage',
 'google-cloud-bigquery']

setuptools.setup(
     name='GoogleDrivePy',
     version='1.0',
     #scripts=['data_analysis_econometrics'] ,
     author="Thomas Pernet",
     author_email="t.pernetcoudrier@gmail.com",
     description="A simple package to connect to the drive from Colab",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/thomaspernet/GoogleDrive-python",
     packages=setuptools.find_packages(),
     install_requires= required_package,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
