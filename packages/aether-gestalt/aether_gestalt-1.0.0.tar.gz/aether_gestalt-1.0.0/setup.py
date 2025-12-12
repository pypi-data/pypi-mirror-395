from setuptools import setup, find_packages

setup(
    name='aether-gestalt',
    version='1.0.0',
    author='Norman Brandt, DeepSeek AI, Claude Sonnet 4.5',
    author_email='tanzdebil85@gmail.com',
    description='φ-modulated GestaltAttention mechanism',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/normanbrandt/aether',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'torch>=2.0.0',
        'numpy>=1.24.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
