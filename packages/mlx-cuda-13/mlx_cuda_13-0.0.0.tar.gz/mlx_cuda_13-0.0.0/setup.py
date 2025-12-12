import sys
from pathlib import Path

from setuptools import setup

setup(
    name="mlx-cuda-13",
    version="0.0.0",
    description="MLX CUDA 13",
    author_email="mlx@group.apple.com",
    author="MLX Contributors",
    packages=["mlx_cuda"],
    url="https://github.com/ml-explore/mlx",
    license="MIT",
    python_requires=">=3.10",
)
