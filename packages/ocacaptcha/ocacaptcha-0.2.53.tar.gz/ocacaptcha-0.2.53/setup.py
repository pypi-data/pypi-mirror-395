from setuptools import setup, find_packages

setup(
    name='ocacaptcha',
    version='0.2.53',
    author='OCA admin',
    author_email='oneclickactionsoft@gmail.com',
    description='This library for solving TikTok captcha via OCA captcha service',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OneClickAction/TikTok-Captcha-Solver',
    packages=find_packages(),
    install_requires=[
        'requests',
        'selenium',
        'playwright',
        'nodriver'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.13.1',
    keywords='tiktok, captcha, puzzle, slide, 3d, two the same shapes,2 objects, rotate, whirl, circle, automation, python, selenium, playwright, nodriver, tiktok captcha, icon, tiktok slide, tiktok whirl, tiktok 3d, tiktok icon, geetest, geetest icon, datadome, slider, audio', 
)
