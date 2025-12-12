"""
AutoRiskML - A Fully Automated Risk & Trading Intelligence Engine
The most comprehensive, production-ready risk ML automation package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Core requirements (minimal for basic functionality)
install_requires = []

# Optional extras for different use cases
extras_require = {
    # Performance acceleration
    'perf': [
        'numpy>=1.20.0',
        'numba>=0.55.0',
        'pyarrow>=10.0.0',
    ],
    
    # Machine learning models
    'ml': [
        'scikit-learn>=1.0.0',
        'xgboost>=1.7.0',
        'lightgbm>=3.3.0',
    ],
    
    # Explainability
    'explain': [
        'shap>=0.41.0',
        'lime>=0.2.0',
    ],
    
    # Distributed processing
    'distributed': [
        'dask[complete]>=2023.1.0',
        'ray>=2.0.0',
    ],
    
    # Data connectors
    'connectors': [
        'sqlalchemy>=2.0.0',
        'boto3>=1.26.0',
        'azure-storage-blob>=12.0.0',
        'confluent-kafka>=2.0.0',
        'psycopg2-binary>=2.9.0',
        'pymongo>=4.0.0',
    ],
    
    # Azure deployment
    'azure': [
        'azureml-sdk>=1.50.0',
        'azure-identity>=1.12.0',
        'azure-mgmt-containerinstance>=10.0.0',
    ],
    
    # Monitoring & alerting
    'monitoring': [
        'prometheus-client>=0.16.0',
        'grafana-api>=1.0.0',
    ],
    
    # Reporting
    'reporting': [
        'matplotlib>=3.5.0',
        'seaborn>=0.12.0',
        'plotly>=5.10.0',
        'jinja2>=3.1.0',
        'weasyprint>=57.0',
    ],
    
    # Development tools
    'dev': [
        'pytest>=7.2.0',
        'pytest-cov>=4.0.0',
        'black>=23.0.0',
        'isort>=5.12.0',
        'mypy>=1.0.0',
        'flake8>=6.0.0',
    ],
}

# Full installation (all extras)
extras_require['all'] = sum(extras_require.values(), [])

setup(
    name="autoriskml",
    version="0.1.0",
    author="Idriss Bado",
    author_email="idrissbadoolivier@gmail.com",
    description="A Fully Automated Risk & Trading Intelligence Engine - Production-ready ML pipeline for risk scoring, monitoring, and deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/AutoRiskML",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'autorisk=autoriskml.cli:main',
        ],
    },
    keywords=[
        'risk-management', 'machine-learning', 'credit-scoring', 'trading',
        'fintech', 'psi', 'woe', 'iv', 'scorecard', 'drift-detection',
        'mlops', 'automl', 'explainability', 'monitoring', 'azure',
        'fraud-detection', 'financial-engineering', 'quantitative-finance'
    ],
    project_urls={
        "Bug Reports": "https://github.com/idrissbado/AutoRiskML/issues",
        "Source": "https://github.com/idrissbado/AutoRiskML",
        "Documentation": "https://github.com/idrissbado/AutoRiskML#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
