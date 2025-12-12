from setuptools import setup, find_packages

setup(
    name="IM-COOL-BOOY-NGROK",
    version="1.1.1",
    author="𝐈𝐌 𝐂𝐎𝐎𝐋 𝐁𝐎𝐎𝐘 𝓢𝓱𝓪𝓭𝓸𝔀 𝓚𝓲𝓷𝓰",
    author_email="coolbooy@gmail.com",
    description="NGROK AUTO INSTALLER & MANAGER",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["IM_COOL_BOOY_NGROK"],
    install_requires=[],
    keywords=["NGROK"],
    entry_points={
        "console_scripts": [
            "IM-COOL-BOOY-NGROK=IM_COOL_BOOY_NGROK.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.png", "*.jpg", "*.jpeg", "*.gif"]},
)
