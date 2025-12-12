from setuptools import setup

setup(
    name='coremsft',
    version='0.1',
    packages=['coremsft'],
    author='Eran Paldi',
    description='This package is a test package to send information to a webhook',
    long_description='This package takes a specific file of your choosing and sends the content of it to a webhook of our choosing.',
    long_description_content_type='text/plain',  # Use plain text since there's no Markdown
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)