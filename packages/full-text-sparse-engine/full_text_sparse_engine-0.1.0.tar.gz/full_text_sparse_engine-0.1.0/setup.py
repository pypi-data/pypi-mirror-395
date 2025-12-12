from setuptools import setup

setup(
    name='full-text-sparse-engine',
    version='0.1.0',
    author='Carlo Moro',
    author_email='cnmoro@gmail.com',
    description="A fast search engine using LMDB, BM25 and Rust-based components.",
    py_modules=["engine", "sparse_matrix", "storage", "vectorizer"],
    install_requires=[
        "lmdb",
        "numpy",
        "scipy",
        "unidecode",
        "scikit-learn",
        "lenlp",
        "xxhash",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
