from setuptools import setup


def get_version():
    return '1.0.0'


setup(
    name='jira_timelog_lib',
    version=get_version(),
    description='',
    url='https://github.com/jluckett/jira-timelog-lib',
    author='Jamie Luckett',
    author_email='jamieluckett@gmail.com',
    license='MIT',
    install_requires=['jira'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['jira_timelog_lib'],
    include_package_data=True,
)
