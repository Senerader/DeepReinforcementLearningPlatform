from setuptools import setup, find_packages


setup(
    name='drl_platform',
    version='0.1',
    license='MIT',
    author="Mark Sisin",
    author_email='markas050@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Senerader/DeepReinforcementLearningPlatform',
    keywords='Deep Reinforcement Learning',
    install_requires=[
          'gym==0.19.0',
      ],

)