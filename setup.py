from setuptools import setup

setup(name='reportTelegram',
      version='0.2.3',
      description='A telegram bot that helps you to keep the group clean by a report system with kicks and ban times.',
      url='https://github.com/jossalgon/reportTelegram',
      author='Jose Luis Salazar Gonzalez',
      author_email='joseluis25sg@gmail.com',
      packages=['reportTelegram'],
      package_data={'reportTelegram': ['data/stickers/*']},
      install_requires=[
          "python-telegram-bot",
          "pymysql"
      ],
      zip_safe=False)
