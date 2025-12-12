from setuptools import setup, find_packages

setup(
    name='VKPyKit',
    version='0.1.2',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description='Packaged functions for Machine Learning and Data Science tasks.',
    author='Vishal Khapre',
    url='https://github.com/assignarc/VKPyKit',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'IPython.display',
        'plotly.express',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    # packages=find_packages(
    #     where='src',
    #     include=['VKPyKit'],
    # ),
)
