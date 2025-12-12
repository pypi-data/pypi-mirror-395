from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()


setup(name='dgredis',
      version='0.1.1',
      description='Ver.0.1.0',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   #'Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent",
                   ],
      keywords='',
      url='https://gitlab.com/gng-group/dgredis.git',
      author='Malanris',
      author_email='admin@roro.su',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          "redis"
      ],
      include_package_data=True,
      zip_safe=False)
