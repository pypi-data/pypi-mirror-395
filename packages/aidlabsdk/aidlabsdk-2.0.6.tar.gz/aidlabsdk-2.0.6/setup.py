from setuptools import setup, find_packages

def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

setup_args = dict(
    name='aidlabsdk',
    version='2.0.6',
    description="Comprehensive SDK for integrating Aidlab's and Aidmed One's biofeedback and biosignal processing functionalities into your applications.",
    long_description_content_type="text/markdown",
    long_description=read_file("README.md"),
    license=read_file("LICENSE.md"),
    packages=find_packages(),
    install_requires=['bleak==0.21.1', 'packaging'],
    author='Aidlab',
    author_email='contact@aidlab.com',
    keywords=['biofeedback', 'aidlab', 'aidmed', 'wearable technology', 'fitness', 'data analysis', 'healthcare', 'biomedical', 'chest strap', 'sdk', 'signals', 'biosignals', 'heart rate', 'ecg'],
    url='https://www.aidlab.com',
    include_package_data=True,
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
    
