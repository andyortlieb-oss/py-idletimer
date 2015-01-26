from distutils.core import setup

files = ['idletimer/*']
scripts = []

setup(
    name = "idletimer",
    version = "0.1",
    author = "Andy Ortlieb",
    author_email = "andyortlieb@gmail.com",
    description = ("A simple class to manage timeout conditions"),
    license = "MPL",
    packages = ['idletimer'],
    package_data = {'idletimer': files},
    scripts = scripts
)
