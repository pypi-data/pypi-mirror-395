from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easy-mcp',
    version='0.1.2',
    description='Seamlessly connect MCP tools to LangChain Agents.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Annyfly',
    author_email='2287551746@qq.com',
    url='https://github.com/Annyfee/easy-mcp',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'langchain-core',
        'langchain-openai',
        'langgraph'
        'pydantic',
        'mcp',
        'python-dotenv'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT'
)