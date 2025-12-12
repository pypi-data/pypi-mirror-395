from setuptools import setup, find_packages
setup(name='syutils',
      version='0.0.6',
      description='High frequency functions and class',
      long_description='High frequency functions and class for data processing, file operations, date handling, etc.',
      long_description_content_type="text/markdown",
      url='https://gitee.com/wdy0401/syutils',
      author='wangdeyang',
      author_email='wdy0401@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        # 依赖的库
        "trade_date",
        "py7zr",
    	],
      zip_safe=False)