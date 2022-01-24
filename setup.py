import io
import os

from setuptools import setup, find_packages

dir = os.path.dirname(__file__)
github_token = os.environ['GITHUB_TOKEN']

with io.open(os.path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytrends-async',
    version='0.3.2',
    description='Pseudo API for Google Trends with asyncio support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #url='https://github.com/KyleKreutzer/pytrends-async',
    #download_url='https://github.com/KyleKreutzer/pytrends-async/archive/0.3.2.tar.gz',
    author='Kyle Kreutzer',
    author_email='kyleakreutzer@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['pandas>=0.25', 'lxml', 'httpx==0.9.5', 'tenacity==6.0.0'],
    keywords='google trends api search async asyncio',
    packages=['pytrendsasync'],
    install_requires='package',
    dependency_links = [
    'git+https://{github_token}@github.com/user/{package}.git/@{version}#egg={package}'
        .format(github_token=github_token, package='pytrends-async', version=master)
        ]
)
