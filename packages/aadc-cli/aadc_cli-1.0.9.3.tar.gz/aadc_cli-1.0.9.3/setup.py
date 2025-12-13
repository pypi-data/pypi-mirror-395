from setuptools import setup
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8") if (this_directory / "README.md").exists() else ""

setup(
    name="aadc-cli",
    version="1.0.0",
    description="AADC - Agentic AI Developer Console. Build anything with AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AADC Team",
    author_email="team@aadc.dev",
    url="https://github.com/yourusername/aadc",
    packages=[],  # Explicitly no packages to avoid auto-discovery
    py_modules=[
        "main",
        "agent",
        "config",
        "auth",
        "utils",
        "memory",
        "prompts",
        "tools",
        "terminal_manager",
        "project_init",
        "firebase_client",
        "input_handler",
        "background_task",
        "proxy_agent",
        "github_integration",
    ],
    install_requires=[
        "google-generativeai>=0.8.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic[vertex]>=0.40.0",
        "httpx>=0.25.0",
        "google-auth>=2.0.0",
        "firebase-admin>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "aadc=main:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    keywords="ai developer agent cli code generation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/aadc/issues",
        "Source": "https://github.com/yourusername/aadc",
        "Documentation": "https://github.com/yourusername/aadc#readme",
    },
)
