from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='PYW-WeavexPy',
    version='0.0.8',
    license='MIT License',
    author='João Victor',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='serveserviceaplication@gmail.com',
    keywords='PYW-WeavexPy',
    description=u'PYW-WeavexPy - 0.0.8 - beta',
    packages=['WeavexPy'],
    install_requires=['pywebview', 'flask'],)