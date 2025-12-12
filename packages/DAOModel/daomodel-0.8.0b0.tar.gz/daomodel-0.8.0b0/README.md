# DAOModel
An instant CRUD layer for your Python models.

DAOModel is a powerful yet beginner-friendly database toolkit built on top of industry-standard libraries
([SQLModel](https://sqlmodel.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/latest/), and [SQLAlchemy](https://www.sqlalchemy.org/)).
It provides everything you need to get your database-backed project up and running quickly.

* Eliminate repetitive work by auto-creating your DAOs
* Make your code more straightforward and readable
* Write less code, which means:
    * having a usable product sooner
    * reduced testing burden
    * minimal potential bugs

## Purpose
Assembled from a collection of duplicated logic found across several projects,
this library serves as a starting point for your Python project.
Though great for complex apps, it's also a great starting point for simple projects.
DAOModel will benefit new developers the most by providing a straight forward start to writing code.

A goal of my libraries is to remove upfront hurdles to facilitate learning along the way.
Following the [Guides](https://daomodel.readthedocs.io/en/latest/docs/getting_started/),
anyone can get started without knowledge of relational databases or SQLAlchemy.
If any documentation or design is unclear,
please [submit a ticket](https://github.com/BassMastaCod/DAOModel/issues/new)
so that I can be sure that even beginners are able to benefit from this project.

## Features
* Expands upon SQLModel; works seamlessly with existing models
* SQLAlchemy under the hood; keep existing logic while using DAOModel functions for new code
* A proven, reliable data layer
* Advanced search capabilities without raw SQL
* Quality-of-life additions

Looking for more? Check out my other projects on [GitHub](https://github.com/BassMastaCod)

## Installation
Python 3.10+ is required.

SQLModel, SQLAlchemy, and all other dependencies will be installed with the pip cmd:
```
pip install DAOModel
```
or, given that this project is a development tool, you will likely add _DAOModel_ to `requirements.txt` or `pyproject.toml`.

Next, move on to the [Getting Started](https://daomodel.readthedocs.io/en/latest/docs/getting_started/) page to begin developing your DAOModels.

## Caveats

### Database Support
Most testing has been completed using SQLite, though since SQLModel/SQLAlchemy
support other database solutions, DAOModel is expected to as well.

Speaking of SQLite, this library configures Foreign Key constraints to be enforced by default in SQLite.

### Table Names
Table names are configured to be snake_case which differs from SQLModel.
See [Table Naming](docs/usage/model.md#table-naming) for more information.

### Unsupported Functionality
Not all functionality will work as intended through DAOModel.
If something isn't supported, [submit a ticket](https://github.com/BassMastaCod/DAOModel/issues/new) or pull request.
And remember that you may always use what you can and then
override the code or use the query method in DAO to do the rest.
It should still save you a lot of lines of code.
