# Netbox Nbservice
[Netbox](https://github.com/netbox-community/netbox) Plugin for ITSM service mapping.

## Compatibility

This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 2.10 and later.
Tested in versions: 2.10.6; 2.11.12; 3.1.11; 3.2.1

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```
pip install nb-service
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['nb_service']
```
The Plugin contains static files for topology visualization. They should be served directly by the HTTP frontend. In order to collect them from the package to the Netbox static root directory use the following command:
```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py collectstatic
```
The Plugin was built for multiple Netbox Versions, so in order to setup the database objects run make migrations, and aply the database models
```
(venv) $ python3 manage.py makemigrations nb_service
(venv) $ python3 manage.py migrate nb_service
```

# Screenshots

## Versions 2.X

### Service List

![](docs/2_x_SvList.png)

### Service View

![](docs/2_x_SvView.png)

### Service Relations

![](docs/2_x_SvRelation.png)

### Service Diagram

![](docs/2_x_SvDiagram.png)

### Application List

![](docs/2_x_AppList.png)

### Application View

![](docs/2_x_AppView.png)

### Application Devices

![](docs/2_x_AppDevices.png)

## Versions 3.X

### Service List

![](docs/3_x_SvList.png)

### Service View

![](docs/3_x_SvView.png)

### Service Relations

![](docs/3_x_SvRelation.png)

### Service Diagram

![](docs/3_x_SvDiagram.png)

### Application List

![](docs/3_x_AppList.png)

### Application View

![](docs/3_x_AppView.png)

### Application Devices

![](docs/3_x_AppDevices.png)
