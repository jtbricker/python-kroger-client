from setuptools import setup

setup(name='python_kroger_client',
      version='0.1',
      description="Wrapper around Kroger's api",
      url='http://github.com/jtbricker/python-kroger-client',
      author='Justin Bricker',
      author_email='jt.bricker@gmail.com',
      license='MIT',
      packages=['python_kroger_client'],
      install_requires=[
          'simple_cache',
          'selenium',
      ],
      zip_safe=False)