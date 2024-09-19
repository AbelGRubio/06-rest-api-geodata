

# Justifications:

The software structure has been proposed with the purpose
of allowing the addition or extension of new functionalities.
Therefore, some of the decisions taken are now justified

1. **Use of the .env file**: This file contains the
configuration of the program made. This allows us, in the future,
to modify the variables to our liking. In addition, it allows us to identify
which variables are relevant to include in the configMap and use them
in kubernetes.
2. **Include a logger**: The logger is included to collect everything that happens within the software.
In order to identify possible errors that may occur in the future.
3. **Module for the app ''api_module''**: This module includes everything necessary for the restAPI to work.
The following modules can be distinguished:
* functions: set of relevant functions
* global_variables: module that reads the variables from the .env and uses them in the program.
* schemas: models used to exchange information in the endpoints
* logger_api: the logger is defined to record what the software does.
* sql_commands: defines the connection to the database and useful functions to execute the commands.
It is also where all the sql commands are collected.
* routes: module where each of the routes that the API must have will be defined. There will be a file for each type of HTTP method that must be implemented. That is, a module for get and all the endpoints related to the get method are defined
another for patch, post...
4. **Module for tests**: In this module, different types of tests can be distinguished. Database-oriented and server-response-oriented.
5. **Database definition**: To avoid data redundancy and over time it takes up more space. We have a table called relations, which has a
cardinality of 1 to 1 with the **master** table (there is only one user related to a postal code)
and a cardinality of several users to 1 a postal code with the **details** table.
6. **Requirements.txt file**: This file is used to know what is necessary to run the software.
In this way we would only install what is necessary in the corresponding docker image when we want to run this software in
a kubernetes pod.

![Database diagram](assets/imgs/database.png)
> Diagram created on [dbdiagram.io](dbdiagram.io)


# Methodology

The TDD (Test Driven Development) methodology has been used to create this software
and the SOLID principles have been applied as far as possible.

# How to run it

The main software is run from the main.py file

```
python main.py
```


