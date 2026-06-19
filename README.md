# Learn2Slither

## Getting started
```commandline
venv/bin/python3.10 main.py --help 
```

## Examples

- Runs one session in visual mode

```commandline
    venv/bin/python3.10 main.py -s 1 -v
```

-  Runs 10 sessions without visual mode, loading a model

```commandline
    venv/bin/python3.10 main.py -s 1 --load /path/to/file
```

- Runs 100 sessions without visual mode, the model will learn and its 
trained values will be saved in a file

```commandline
    venv/bin/python3.10 main.py -s 100 -l --save /path/to/file
```

Runs 3 sessions with visual mode, showing each step of the snake at a time 
(press enter to go to next step)
```commandline
    venv/bin/python3.10 main.py -s 3 -v -sbs 
```

### Requirements

- python3.10
- make
- pip