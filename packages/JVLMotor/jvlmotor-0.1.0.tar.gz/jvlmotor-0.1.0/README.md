## Installation

Follow these steps to install and set up the **JVLMotorLibrary** project.

### Prerequisites
- **Git**: Ensure that Git is installed on your machine. You can download it from [here](https://git-scm.com/downloads).
- **Python**: Make sure you have Python 3.x installed. You can download it from [here](https://www.python.org/downloads/).
- **Cifx Driver**: Install the **Cifx Driver** from the [Hilscher website](https://www.hilscher.com) as it's required for ethernet communication.
- **CIFX 50-RE PCI**: A CIFX 50-RE PCI card is required if the real-time Ethernet protocol are used.

### User installation
Ensure you have the Microsoft C++ Build Tools, since it is required by severeal libraries. You can get it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
## From pip
```bash
pip install JVLMotor
```
## From Gitea
```bash
git clone http://jvl_git:3000/jvl/JVLMotorLibrary.git
cd JVLMotorLibrary/dist
pip install JVLMotor-0.1.0-py3-none-any.whl
```
It is also possible to install it locally in a virtual environment:
```bash
py -m venv <DIR>
<DIR>\Scripts\activate
cd path\to\JVLMotor\package
pip install JVLMotor-0.0.2-py3-none-any.whl
```
### Developper installation
#### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone http://jvl_git:3000/jvl/JVLMotorLibrary.git
```

#### 2. Initialize Submodules
Navigate into the project directory and initialize submodules:
```bash
cd JVLMotorLibrary
git submodule update --init --recursive
```

#### 3. Install Dependencies
Install dependencies and the library:
```bash
pip install -r requirements.txt
pip install -e .
```
To install it in a virtual environment please refer to above.

#### 4. Verify Installation
Verify the installation by running the example script, remember to connect your motor on serial and change it accordingly in the example (this example makes the motor spinning at 1000RPM for 2 seconds):
```bash
python example.py
```
If you see no errors, the installation is complete.