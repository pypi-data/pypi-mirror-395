from setuptools import setup

setup(
    name='notears-pytorch',
    version='0.2.0',
    description='A PyTorch implementation of the NOTEARS algorithm for causal discovery.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',  # Update this
    author_email='rafat.joy99@gmail.com',  # Update this
    url='https://github.com/rajoy99/notears-pytorch',  # Update this
    py_modules=['notears_pytorch'],
    install_requires=[
        'numpy',
        'torch>=1.0.0',
    ],
    # Add keywords for searchability
    keywords=['causal-discovery', 'structure-learning', 'dag', 'pytorch', 'notears','notears-linear','linear causal discovery'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
)