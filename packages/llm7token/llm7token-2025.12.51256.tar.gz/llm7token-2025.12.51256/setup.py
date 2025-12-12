from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='llm7token',
    version='2025.12.51256',
    author='Eugene Evstafev',
    author_email='support@llm7.io',
    description='Utilities for validating and reporting LLM7 API tokens.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/llm7token',
    packages=find_packages(),
    install_requires=[
        'requests==2.32.3',
        'cryptography==45.0.3',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
    tests_require=['unittest'],
    test_suite='test',
)
