# Setup
Create the environment

```
conda env create -f hmd-env.yml
```

If you want to use a GPU for training you can install GPU support

<!-- Although during development training with a GPU has been slower then training on CPU only, probably due to the little amount of data that make GPU contribution less important. -->

```
conda install cudatoolkit=11.2 cudnn=8.1.0
```

# Running the trained assistant

Startup the action server
```
rasa run actions
```

Run the assistant in the terminal

```
rasa shell
```

# Training the model from scratch

Startup the action server
```
rasa run actions
```

Train the model and run the assistant

```
rasa train && rasa shell
```
