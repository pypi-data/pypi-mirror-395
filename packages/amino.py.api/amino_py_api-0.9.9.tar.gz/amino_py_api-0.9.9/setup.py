from setuptools import setup, find_packages


info = {
	"name": "amino.py.api",
	"version": "0.9.9",
	"github_page": "https://github.com/alx0rr/amino.py",
	"download_link": "https://github.com/alx0rr/amino.py/archive/refs/heads/main.zip",
	"license": "MIT",
	"author": "alx0rr",
	"author_email": "anon.mail.al@proton.me",
	"description": "Library for creating amino bots and scripts.",
	"long_description": None,
	"long_description_file": "README.md",
	"long_description_content_type": "text/markdown",
	"keywords": [
		"aminoapps",
		"aminoxz",
		"amino",
		"amino-bot",
		"pymino",
		"python-amino",
		"amino.py",
		"amino.api",
		"narvii",
		"api",
		"python",
		"python3",
		"python3.x",
		"alx0rr",
		"official",
		"amino.py.api",
		"amino.fix",
		"amino.light",
		"amino.ligt.py",
		"AminoLightPy",
		"medialab",
		"aminolightpy",
		"dorksapi",
		"aminodorks",
	],

	"install_requires": [
		"requests",
		"aiohttp",
		"aiofiles",
		"websocket-client",
		"orjson",
		"json_minify"

	]

}


if info.get("long_description"):
	long_description=info.get("long_description")
else:
	with open(info.get("long_description_file"), "r") as file:
		long_description = file.read()

setup(
	name = info.get("name"),
	version = info.get("version"),
	url = info.get("github_page"),
	download_url = info.get("download_link"),
	license = info.get("license"),
	author = info.get("author"),
	author_email = info.get("author_email"),
	description = info.get("description"),
	long_description = long_description,
	long_description_content_type = info.get("long_description_content_type"),
	keywords = info.get("keywords"),
	install_requires = info.get("install_requires"),
	packages = find_packages(),
    	classifiers=[
	        "Intended Audience :: Developers",
	        "License :: OSI Approved :: MIT License",
	        "Programming Language :: Python :: 3.9",
	        "Programming Language :: Python :: 3.10",
	        "Programming Language :: Python :: 3.11",
	        "Programming Language :: Python :: 3.12",
    ],
)
