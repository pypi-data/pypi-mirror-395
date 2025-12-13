from setuptools import setup, find_packages

setup(
    name='biontfy',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'biontfy': ['resources/*'],
    },
    include_package_data=True,
    install_requires=[
        'PyQt6',
        'pydub',
        # Note: simpleaudio failed to install, so we rely on mpg123 and subprocess.
        # The user must install mpg123 separately for sound to work.
    ],
    author='Bitro dev',
    description='A customizable PyQt6 notification library based on a Telegram-like design.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pyqt-custom-notify', # Placeholder
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
