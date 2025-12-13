# msunpv library

![PyPI](https://img.shields.io/pypi/v/msunpv) ![TestPyPI](https://img.shields.io/badge/dynamic/json?label=TestPyPI&url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fmsunpv%2Fjson&query=$.info.version) ![License](https://img.shields.io/pypi/l/msunpv) 

[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://thanatos-vf-2000.github.io/msunpv/) [![Workflow Status](https://github.com/thanatos-vf-2000/msunpv/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/thanatos-vf-2000/msunpv/actions)

![Python Versions](https://img.shields.io/pypi/pyversions/msunpv)
![Downloads](https://img.shields.io/pypi/dm/msunpv)

msunpv library for Python 3. The library was created to call api from your msunpv.

See <https://ard-tek.com/> for more information on the MSunPV MD Router Solar.

## Document

[Document](https://thanatos-vf-2000.github.io/msunpv/)

## Example usage

See [example.py](./example.py) for a basic usage and tests

```code
PYTHONPATH=./src/ python3 example.py <IP>
```

## https://ard-tek.com/ - MSunPV

This library can read information from MSunPV 2*2 or 4*4 simply by using the IP or hostname. The project is independent of ard-tek.

## Help

- If you pass an IP to the project as a parameter, verify that it is fixed, or if it is dynamic, ensure that your project manages it.


## Issues

You can create issues in this repository to plan, discuss, and track work. Issues can track bug reports, new features and ideas, and anything else you need to write down or discuss. [➡️ Go to issues ⬅️](https://github.com/thanatos-vf-2000/msunpv/issues)

## Contributing

We welcome contributions of all kinds to this repository. For instructions on how to get started and
descriptions of our development workflows, please see our [contributing guide][contrib].

[contrib]: https://github.com/thanatos-vf-2000/esp32-c6-lcd-1.47/blob/main/CONTRIBUTING.md

## License

Copyright 2025 @Franck VANHOUCKE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


For the full license text see [`LICENSE`](LICENSE).