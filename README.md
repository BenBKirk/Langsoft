# Langsoft

Language learning software that makes looking up words,
making flashcards and highlighting grammar easy.

## Development

Here are the steps to set up your development environment.

Requirements:
* **python 3.8.5** or something close to it.
* **virtualenv** - you can install it like `pip install virtualenv`.

Clone and enter the project:
```shell
git clone https://github.com/BenBKirk/Langsoft.git Langsoft
cd Langsoft
```

Create and activate a virtual environment. This will add a `venv` folder
to which sandboxed dependencies will be installed.
> The virtual environment will remain active for the rest of the shell session
or until disabled. You must activate it again when starting a new shell 
> session.
```shell
python3 -m venv venv
source venv/bin/activate
```

Install the requirements. This will download all the dependencies into
the directory `venv/`.

> If the installation fails with a warning about your version of `pip`
> being outdated, follow the directions in the console and try again.
```shell
python3 -m pip install -r requirements.txt
```

Run the application.
```shell
python3 src/main.py
```
