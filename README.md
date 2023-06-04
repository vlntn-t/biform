# BIForm

BIForm is a powerful tool designed for managing BI applications declaratively.

Currently, BIForm supports the following BI applications:

- [Qlik Sense](https://www.qlik.com/us/products/qlik-sense)

## Getting Started

Follow the instructions below to get a copy of the project running on your local machine for development and testing purposes.

### Prerequisites

- Qlik Sense Cloud
- Python 3.6 or higher

### Installing

To install and run the project, open your terminal and enter the following commands:

```bash
# To initialize the project
python3 biform.py init
```

Add all the required information to the **`config.json`** file.

```bash
# To pull the latest changes from the remote repository
python3 biform.py pull
```

```bash
# To compare the local and remote repositories
python3 biform.py plan
```

```bash
# To apply the changes to the remote repository
python3 biform.py apply
```
