from setuptools import setup, find_packages
setup(
    name='irradpy2',     # pip install irradpy2
    version='0.2.2',
    author='Peiyu Lin,Xixi Sun',
    author_email='15958007542@163.com',
    description='A unified multi-source solar radiation and ground meteorological data downloader with forecasting tools.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/raabitt/irradpy2',
    packages=find_packages(),
    license='Apache-2.0',
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.18',
        'requests>=2.25',
        'pytz>=2020.1',
        'torch>=1.9.0',
        'scikit-learn>=1.0',
    ],
    python_requires='>=3.8',
)

