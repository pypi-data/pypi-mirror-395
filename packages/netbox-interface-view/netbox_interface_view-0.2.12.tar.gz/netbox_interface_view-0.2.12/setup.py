from setuptools import find_packages, setup

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except (IOError, FileNotFoundError):
    long_description = 'NetBox Plugin for viewing interfaces in a grid layout with VLAN color-coding'

setup(
    name='netbox-interface-view',
    version='0.2.12',
    description='NetBox Plugin for viewing interfaces in a grid layout with VLAN color-coding',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ITW-Welding-AB/netbox-plugin-interface-view',
    author='Tolfx',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='netbox plugin interface grid visualization',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)
