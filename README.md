# What is this
This is a conversational agent built with the Rasa framework, designed to help the user follow a recipe step by step and manage a shopping list.

# Setup
Create the environment

```
conda env create -f hmd-env.yml
conda activate hmd
```

If you want to use a GPU for training you can install GPU support

<!-- Although during development training with a GPU has been slower then training on CPU only, probably due to the little amount of data that make GPU contribution less important. -->

```
conda install cudatoolkit=11.2 cudnn=8.1.0
```

## If you don't have conda
Assuming you already have python 3.8 (required) installed:


Create the environment and activate it
```
python3.8 -m venv env
source env/bin/activate
```

Install the dependencies
```
python -m pip install -r requirements.txt
```

# Running the trained assistant

Startup the action server
```
rasa run actions
```

Run the assistant in the terminal (in a separate terminal)

```
rasa shell
```

# Training the model from scratch

Startup the action server
```
rasa run actions
```

Train the model and run the assistant (in a separate terminal)

```
rasa train && rasa shell
```
