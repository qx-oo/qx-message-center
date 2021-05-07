from setuptools import find_packages, setup


setup(
    name='qx-message-center',
    version='1.0.0',
    author='Shawn',
    author_email='q-x64@live.com',
    url='https://github.com/qx-oo/qx-message-center/',
    description='Django user message apps.',
    long_description=open("README.md").read(),
    packages=find_packages(exclude=["qx_test"]),
    install_requires=[
        'Django >= 3.0',
        'djangorestframework >= 3.10',
        'celery >= 4.3',
        'psycopg2 >= 2.8.3',
        'channels >= 3.0.3',
    ],
    python_requires='>=3.8',
    platforms='any',
)
