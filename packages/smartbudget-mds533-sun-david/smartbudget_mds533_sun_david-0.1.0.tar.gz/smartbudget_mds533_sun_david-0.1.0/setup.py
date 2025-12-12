from setuptools import setup, find_packages


setup(
    name="smartbudget-mds533-sun-david",  # 必须唯一，不能和别人相同
    version="0.1.0",
    description="SmartBudget: A simple budgeting tool for MDS 533 Step 3 project",
    author="Chongwen Sun, Yifu Zhao,Chuying Chen",
    author_email="chongwen.sun1992@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)