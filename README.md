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

### Prepare environment

Copy template:

```sh
cp template.env .env
```

And modify variables there

## Pycardano off-chain mixer

There are two main entry points to main functionality of this lib:

1. A [class](mixer/start.py) for starting new mixer.
2. A [class](mixer/user.py) for using already created mixer.

Other functionality includes a [helper](mixer/nft_minter.py) to mint NFTs; and also a [owner script](mixer/owner_script.py) implementation. `OwnerScript` exists just to query owner wallet for a UTxO to reference during mixer NFT (protocol token) mint.

## Mixer script compilation & other preparations

First mixer owner should create an mixer, so he needs to generate a pair of keys for his wallet.
Also he needs to compile mixer script, therefore he first needs to prepare script parameters. It is done with this runner:

```sh
python print_mixer_start_params.py
```

It will generate and print important parameters which should be saved for later use. First, they are used as a mixer script parameter `MixerConfig`.

After that owner needs to copy printed parameters and consult on-chain deposit [readme](https://github.com/fullstack-development/tornadano-on-chain-deposit/tree/master#usage) and withdraw [readme](https://github.com/fullstack-development/tornadano-on-chain/tree/master#usage).

## Mixer related transactions

### Starting mixer

Owner wallet needs to run:

```sh
python run_start.py
```
