# BIForm

BIForm is a powerful CLI tool designed for managing BI applications and their configurations. It allows you to easily manage your BI applications and their configurations declaratively in a version control system (VCS) such as Git.

Currently, BIForm supports the following BI applications:

- [x] [Qlik Sense](https://www.qlik.com/us/products/qlik-sense)
- [ ] [Microsoft Power BI](https://powerbi.microsoft.com/)
- [ ] [Tableau](https://www.tableau.com/)

## Getting Started

Follow the instructions below to get a copy of the project running on your local machine for development and testing purposes.

### Prerequisites

- A Qlik Sense Cloud tenant: You can get a free trail [here](https://www.qlik.com/us/products/qlik-cloud)
- Qlik Sense Cloud API key
  - Profile Settings > API keys
- Version Control such as GitHub or GitLab _(optional)_
- Python 3.6 or higher installed on your local machine

#### Windows

- Install the Qlik CLI manually: https://github.com/qlik-oss/qlik-cli/releases

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

### Scaffolding

```bash
└── /
  ├── biform.py # Contains the main logic of the application
  ├── README.md # Contains the documentation of the application
  └── biforms/
          ├── state.json # Contains the state of the application
          ├── config.json # Contains the configuration of the application (e.g. Qlik Sense Cloud API key and tenant)
          ├── README.md # Contains the documentation of the application
          └── app-id-1/
              ├── frontend/
              │   ├── objects.json
              │   ├── measures.json
              │   ├── dimensions.json
              │   └── ...
              └── backend/
                  ├── scripts.json
                  ├── connections.json
                  └── ...
```

## Built With

- [Python](https://www.python.org/) - The programming language used
- [Qlik CLI](https://qlik.dev/toolkits/qlik-cli/) - The CLI tool used to manage Qlik Sense applications
