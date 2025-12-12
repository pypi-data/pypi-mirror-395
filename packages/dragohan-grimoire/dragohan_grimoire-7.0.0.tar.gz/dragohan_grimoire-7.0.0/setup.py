"""
💀 DRAGOHAN GRIMOIRE - PRODUCTION SETUP.PY v2.1.0 💀
Fixed version with all monarch systems included
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dragohan-grimoire",
    version="7.0.0",  # 🆕 VERSION 7.0.0 - n-organ packaged
    py_modules=[
        "json_mage",
        "simple_file", 
        "loops",
        "duplicate_tools",
        "tool_fluency_v2",
        "tool_fluency",
        "brain",           # 🆕 Will use brain_fixed.py in production
        "experience",
    ],
    packages=find_packages(),  # 🆕 This will find monarchs/ package
    package_data={
        "": [
            "experience/*.json",
            "brain_config.json",
        ]
    },
    include_package_data=True,
    install_requires=[
        "jmespath>=1.0.0",
        "httpx>=0.27.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=5.0.0",
        "openai>=1.0.0",
        "anthropic>=0.25.0",
        "cryptography>=41.0.0",
        "python-dotenv>=1.0.0",
        # 🆕 Additional dependencies for monarch systems
        "aiofiles>=23.0.0",
        "asyncio-mqtt>=0.13.0",
    ],
    author="DragoHan",
    author_email="aafr0408@gmail.com",
    description="💀 AI Automation Grimoire v2.1.0 - PRODUCTION with Fixed Monarch System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farhanistopG1/my_grimoire",
    project_urls={
        "Bug Tracker": "https://github.com/farhanistopG1/my_grimoire/issues",
        "Source Code": "https://github.com/farhanistopG1/my_grimoire",
        "Documentation": "https://github.com/farhanistopG1/my_grimoire/wiki",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",  # 🆕 Changed to Production
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",  # 🆕 Updated minimum version
    keywords="json, files, automation, api, ai, agents, langchain, llm, deepseek, shadow-monarch, lead-enrichment, data-processing",
    entry_points={
        "console_scripts": [
            "dragohan-brain=brain:get_brain",
            "dragohan-monarch=monarchs:summon",
            "dragohan-datasystem=monarchs.systems:summon_system",
        ],
    },
)
