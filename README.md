# Workouts Tracking
A small python GUI to track the progress of individual workouts. 

## Main Features
TBA

## Quick Start
### Installation
1. Clone this repository to your preferred location, using:
```bash
git clone https://github.com/rekaiser/workouts-tracking.git
```
2. Change into the repository and create a virtual environment:
```bash
cd workouts-tracking
python3 -m venv venv
```
3. Activate the virtual environment:
```bash
source venv/bin/activate
```
4. Install Workouts Tracking and its dependencies in editable mode:
```bash
pip install -e .
```
5. The GUI requires the `libOpenGL` library. So in case you need it, install it with:
```bash
sudo apt install libopengl0
```
6. Now Workouts Tracking is ready to be run within the virtual environment with
either
```bash
WT
```
or 
```bash
workouts_tracking
```
### Running the Program
Following the steps for the installation above, the program can only be run from within the virtual 
environment. So be sure to always source the script to activate the virtual environment before.
To explore the latest stage of the development process checkout the develop branch via:
```bash
git checkout develop
```
Then it is possible to start using the program by creating a new database by clicking the button
`New Database`. After having loaded a database into the program, the various actions you can perform
in the GUI are quite self-explanatory.

## Authors
Reinhold Kaiser

## License
[GPLv3](LICENSE)
