from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_mysql',
    version='3.0.4',
    description='MySQL wrapper from Bryn',
    long_description='MySQL wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'pandas>=1,<3',
        'pymysql>=1,<=2',
        'requests>=2,<=3',
        'cryptography>=38,<=38',
    ],
    zip_safe=False,
)
