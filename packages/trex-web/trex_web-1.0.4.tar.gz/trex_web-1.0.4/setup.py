from setuptools import setup, find_packages

setup(
    name='trex-web',
    version="1.0.4",
    description="TRex web package",
    author="Jack Lok",
    packages=find_packages(include=["trexweb", "trexweb.*"]),
    include_package_data=False,   # don’t include non-Python files
    zip_safe=False,
    install_requires=[
      'flask',
      'Jinja2',
      'MarkupSafe',
      'phonenumbers',
      'requests',
      'testfixtures',
      'flask-babel',
      'Flask-CORS',
    ],
    entry_points={
        "console_scripts": [
            "trexweb=trexweb.__main__:main",   # optional
        ]
    },
)