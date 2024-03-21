#!/usr/bin/env python
from setuptools import setup, find_packages
from mediapipe_helper.__init__ import __version__

required=[]
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    for req in requirements:
        p = req.split('==')
        required.append(p[0])
        
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()     
setup(
    name='mediapipe_helper',
    version= __version__,
    description= 'A package to help you utilise landmarks in the face_landmark feature of google open source mediapipe.',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='learningnRunning',
    author_email='max_sungrok@naver.com',
    url='https://github.com/LearningnRunning/py_face_landmark_helper',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Education',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    install_requires=required,
)

    
def install():
    required = []
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
        for req in requirements:
            p = req.split('==')
            required.append(p[0])
            

        
    setup(
        name='mediapipe_helper',
        version= __version__,
        description= 'A package to help you utilise landmarks in the face_landmark feature of google open source mediapipe.',
        long_description = long_description,
        long_description_content_type='text/markdown',
        author='learningnRunning',
        author_email='max_sungrok@naver.com',
        url='https://github.com/LearningnRunning/py_face_landmark_helper',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Education',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Education',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        packages=find_packages(),
        install_requires=required,
    )


if __name__ == "__main__":
    install()
