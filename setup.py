import setuptools

description = 'Dynamically generate spider subclasses. Run crawls sequentially with crochet. Do both.'
with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='scrapy_dynamic_spiders',
    version='1.0.0.a1',
    author='Derek Harootune Otis',
    author_email='dharootuneotis@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/harootune/scrapy_dynamic_spiders',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='scrapy spiders web-scraping',
    project_urls={
        'Source': 'https://github.com/harootune/scrapy_dynamic_spiders'
    },
    packages=setuptools.find_packages(),
    install_requires=['scrapy', 'crochet'],
    python_requires='~=3.6',
)
