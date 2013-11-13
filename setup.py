from setuptools import setup, find_packages

setup(
    name = "django-content-edit",
    version = "1.3",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("A very simple way to let users edit content on the front end of a website."),
    license = "BSD",
    keywords = "django cms content ajax",
    url = "https://github.com/burke-software/django-content-edit",
    packages=find_packages(),
    include_package_data=True,
    test_suite='setuptest.setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest',
        'south',
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=['django', 'django-ckeditor', 'django-reversion']
)
