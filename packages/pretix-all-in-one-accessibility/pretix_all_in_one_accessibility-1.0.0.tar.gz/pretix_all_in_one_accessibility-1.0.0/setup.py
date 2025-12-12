import io
from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

setup(
    name="pretix_all_in_one_accessibility",
    version="1.0.0",
    description="Website accessibility widget for improving WCAG 2.0, 2.1, 2.2 and ADA compliance!",
    author="Skynet Technologies USA LLC",
    author_email='developer3@skynettechnologies.com',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    # url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests"  
    ],
    entry_points={
        'pretix.plugins': [
            'pretix_all_in_one_accessibility = pretix_all_in_one_accessibility.apps:AccessibilityPluginApp',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.9',
)




