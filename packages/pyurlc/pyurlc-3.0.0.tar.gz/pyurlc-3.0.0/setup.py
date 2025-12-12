from setuptools import setup, Extension
import sys
import platform

compile_args = ['-O3', '-Wall', '-Wextra', '-std=c11']

system = platform.system()
machine = platform.machine()

if system == 'Darwin':
    if machine == 'arm64':
        compile_args += ['-march=armv8-a', '-DUSE_NEON=1']
    else:
        compile_args += ['-march=native', '-msse2', '-DUSE_SSE=1']
elif system == 'Linux':
    if 'arm' in machine or 'aarch64' in machine:
        compile_args += ['-march=armv8-a', '-DUSE_NEON=1']
    elif 'x86' in machine or 'amd64' in machine:
        compile_args += ['-march=native', '-msse2', '-DUSE_SSE=1']
    else:
        compile_args += ['-O3']
elif system == 'Windows':
    compile_args = ['/O2', '/arch:AVX2', '/fp:fast', '/DUSE_SSE=1']
else:
    compile_args += ['-O3']

pyurlc_module = Extension(
    'pyurlc',
    sources=['pyurlc.c'],
    extra_compile_args=compile_args,
    language='c'
)

setup(
    name='pyurlc',
    version='2.0.1',
    description='Ultra-fast URL encoding/decoding in C with SIMD',
    author='pyurlc developer',
    ext_modules=[pyurlc_module],
    python_requires='>=3.6',
    zip_safe=False,
)