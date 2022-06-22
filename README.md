# Setup
Create the environment

```
conda env create -f hmd-env.yml
```

If you want to use a GPU to train the models you can install GPU support

<!-- Although during development training with a GPU has been slower then training on CPU only, probably due to the little amount of data that make GPU contribution less important. -->

```
conda install cudatoolkit=11.2 cudnn=8.1.0
```

# Training and running the assistant

Startup the action server
```
rasa run actions
```

Train the models and run the assistant

```
rasa train && rasa shell
```