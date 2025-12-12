import setuptools

with open("README.rst", "r", encoding="utf-8") as f:
  long_description = f.read()

setuptools.setup(name='neo4j_litellm',  # package name
      version='0.0.2',  # version
      description='A LiteLLM LLM component for Neo4j graph RAG. ',
      long_description=long_description,
      author='1Vewton.zh-n',
      author_email='zhanyunze0601@gmail.com',
      install_requires=[
          'litellm>=1.77.5',
          'neo4j_graphrag>=1.9.0'
      ],
      license='MIT License',
      packages=setuptools.find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13'
      ],
      )