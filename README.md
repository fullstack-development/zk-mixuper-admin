# Admin tools for tornadano

## Local development with IDE

### First time setup

1. Pin python version to Python 3.11.2:
If you don't have pyenv install it with this [guide](https://realpython.com/intro-to-pyenv/#installing-pyenv).
Then run:

```sh
pyenv install -v 3.11.2
pyenv local 3.11.2
```

2. Create virtual environment:

```sh
python -m venv ./venv
```

3. Activate virtual environment:

```sh
source venv/bin/activate
```

4. Install the project dependencies:

```sh
pip install -r requirements.txt
```

### Activation (after you've done first time setup only activation is necessary)

Do only 3. step from setup.

### Deactivation

```sh
deactivate
```
