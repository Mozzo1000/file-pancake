# file-pancake
File manager

## Building pancake
Building a installable package needs to be done from the same type of machine as the intended output, i.e if you want a `.exe` then build from a windows machine.

### Windows
**Prerequisites**:
* PyInstaller
* Inno Setup

Run the following from the root directory:
```
PyInstaller package-py.spec
```
Then compile `package-win.iss` with Inno Setup. The installer should be saved to a `Output` folder..