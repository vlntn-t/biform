# BIForm

BIForm is a powerful CLI tool designed for managing BI applications and their configurations. It allows you to easily manage your BI applications and their configurations declaratively in a version control system (VCS) such as Git.

Currently, BIForm supports the following BI applications:

- [x] [Qlik Sense](https://www.qlik.com/us/products/qlik-sense)
- [ ] [Microsoft Power BI](https://powerbi.microsoft.com/)
- [ ] [Tableau](https://www.tableau.com/)

## Getting Started

Follow the instructions below to get a copy of the project running on your local machine for development and testing purposes.

### Prerequisites

- A Qlik Sense Cloud tenant [Try for free](https://www.qlik.com/us/products/qlik-cloud)
- Qlik Sense Cloud API key
- Version Control such as GitHub or GitLab _(optional)_
- Python 3.6 or higher installed on your local machine

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

## Built With

- [Python](https://www.python.org/) - The programming language used
- [Qlik CLI](https://qlik.dev/toolkits/qlik-cli/) - The CLI tool used to manage Qlik Sense applications
