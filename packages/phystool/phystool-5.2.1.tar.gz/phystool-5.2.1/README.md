# Phystool

This package is there to help managing physics lecture notes, exercises,
tests... It is based on four complementary elements:

1. **phystool**: Manages a database of LaTeX documents with additional metadata
2. **physnoob**: Provides some the of **phystool**'s functionalities in a GUI
3. _optional_ **[physvim](https://bitbucket.org/jdufour/physvim/src/master/)** or **[phystool.nvim](https://bitbucket.org/jdufour/phystool.nvim/src/master/)**: Implements vim commands to interact with **phystool**
5. _optional_ **[phystex](https://bitbucket.org/jdufour/phystex/src/main/)**: LaTeX classes and packages that are compatible with **phystool**

Among other things, this package provides:

+ a clean way to compile LaTeX documents without cluttering your directories
+ a neat and user-friendly log LaTeX compilation messages
+ an automatic LaTeX recompilation when/if required


# Development tools

The following tools are used during development:

+ [uv](https://docs.astral.sh/uv/): manages the python dependencies, build and publish new releases
+ [just](https://just.systems/): provides a set of commands
+ [direnv](https://direnv.net/): automatically loads the `.envrc`  when the directory is entered so that
    + the envrironment variables are set
    + the virtual envrironment is synchronized and activated
