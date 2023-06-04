# BIForm

BIForm is a powerful tool designed for managing Qlik Sense applications declaratively. The tool is built upon the [qlik-cli](https://github.com/qlik-oss/qliksense-k8s).

## Getting Started

Follow the instructions below to get a copy of the project running on your local machine for development and testing purposes.

### Prerequisites

First, you will need to access the following site:

- [QlikCloud Link](https://5llri6syh3zllpg.eu.qlikcloud.com/sense/app/4efdc0ca-fb74-4728-9ea4-6b38cc0ea3b6/sheet/41f524b1-b4e7-4641-968f-34e582229122/state/edit)

### Installing

To install and run the project, open your terminal and enter the following commands:

```bash
python3 biform.py init
python3 biform.py pull
python3 biform.py apply
```

**config.json** file should be created in the root directory of the project. It should contain the following information:

```
{
"TENANT": "wss://5llri6syh3zllpg.eu.qlikcloud.com/app/",
"API_KEY": "eyJhbGciOiJFUzM4NCIsImtpZCI6IjFiM2MzMWQ1LTUxYTktNGE5OS04MmU2LTJkMjllNDJiZTIzOCIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiTE5hd2ZBNkJlSFVmaUluRVFsekQwbFpzMEw2QUpBV2MiLCJqdGkiOiIxYjNjMzFkNS01MWE5LTRhOTktODJlNi0yZDI5ZTQyYmUyMzgiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjM5NWNmYWVhNDkyOGRlOTQxNWFjNzZjIn0.YO2EwY90ikS2EUY15-QWkiWQQTXcbAfrT4m1vOMLwGFU9a3lL8N5TD4-YgBx7kqs8v7QcfZtWlvtRDaAsFRz1iVBgNcheA7LnE4Bms_He197k\_\_uKQ1dJr_DIQ10nt4N",
"APP_IDS": ["4efdc0ca-fb74-4728-9ea4-6b38cc0ea3b6"]
}
```
