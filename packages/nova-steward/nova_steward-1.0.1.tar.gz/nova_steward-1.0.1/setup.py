from setuptools import setup, find_packages

setup(
    name="nova-steward",
    version="1.0.1",
    author="Gourav Kumar Dhaka",
    author_email="gauravkr7114@gmail.com",
    description="Autonomous AI Agent for Self-Healing Code Security",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gourav-kd/nova-steward",
    
    # --- CRITICAL UPDATE: INCLUDES SOUL.JSON ---
    include_package_data=True,
    # -------------------------------------------
    
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'nova-steward=nova_steward.core:main_loop',
        ],
    },
)

