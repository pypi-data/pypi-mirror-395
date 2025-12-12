from setuptools import setup, find_packages

VERSION = '0.1.15'
DESCRIPTION = 'Email manager'
LONG_DESCRIPTION = 'Email manager'

# Configurando
setup(
        name="email-manager", 
        version=VERSION,
        packages=find_packages(),
        author="Carlos Pacheco",
        license='MIT',
        author_email="carlos.pacheco@kemok.io",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url='https://github.com/Kemok-Repos/email-manager',
)