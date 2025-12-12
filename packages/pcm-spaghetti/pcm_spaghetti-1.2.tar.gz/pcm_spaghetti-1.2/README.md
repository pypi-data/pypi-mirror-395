# SPAGHETTI - Structural Phase Adaptation via Generative Histological Enhancement and Texture-preserving Translation Integration

[![PyPI version](https://badge.fury.io/py/pcm-spaghetti.svg)](https://badge.fury.io/py/pcm-spaghetti)

Implementation of the SPAGHETTI method for phase-contrast microscopy images pre-processing so that you can use your favourite H&E model on them through this domain adaptation method.

Read the documentation at [documentations.md](documentations.md)

## Installing SPAGHETTI

### Installing using PyPI

SPAGHETTI is available on the Python Package Index (PyPI) to be installed with `pip` directly. To install, run:

``pip install pcm-spaghetti``

### Installing Locally

Alternatively, you may also install SPAGHETTI from the GitHub repository directly. To do that, first create a virtual Python environment and install SPAHETTI locally.

```bash
virtualenv --no-download spaghetti
source spaghetti/bin/activate 
git clone https://github.com/schwartzlab-methods/spaghetti
cd spaghetti
python setup.py sdist bdist_wheel
pip install .
```

## Inferences using SPAGHETTI

An example workflow of how to use SPAGHETTI to convert your phase-contrast microscopy images into H&E-like images can be found at `./tutorials/inference_example.py`. Before running the example code, please ensure that you have cloned the default SPAGHETTI checkpoint file properly located at `./spaghetti_checkpoint.ckpt`. If not, please go to the repository and directly download this checkpoint file.

## Inferences with the CLI tool

Alternatively, you can also run inferences using the CLI interface to perform quick inferences. To do this, after you have installed SPAGHETTI, run:

```bash
python3 spaghetti --input path_to_directory_with_your_images \
--output path_to_directory_to_save_the_images --checkpoint path_to_the_checkpoint_file
```

The checkpoint file can either be the default checkpoint file (to be downloaded from `./spaghetti_checkpoint.ckpt`), or can be the checkpoint files from your own training (see below for more details on how to train your own SPAGHETTI model).

## Inferences with Docker

For a dependency-free and reproducible environment, the CLI inference tool of SPAGHETTI is available as a Docker image. To use it, ensure you have Docker installed, then run:

### Option 1: Use the Pre-built Image from Docker Hub

The official image is hosted on Docker Hub.

1.  **Pull the latest image:**
    ```bash
    docker pull yinnikun/spaghetti:latest
    ```

2.  **Run Inference:**

    To run inference, you need to mount a local directory into the container. This directory should contain your input images and the model checkpoint. The container will write the output images back to this same directory.

    Let's say your local data is organized as follows:
    ```
    /path/to/your/data/
    ├── inputs/
    │   ├── image1.tif
    │   └── image2.tif
    ├── spaghetti_checkpoint.ckpt
    └── outputs/  <-- This will be created
    ```

    Execute the following command:
    ```bash
    docker run --rm -v "/path/to/your/data:/data" yinnikun/spaghetti:latest \
      --input /data/inputs \
      --output /data/outputs \
      --checkpoint /data/spaghetti_checkpoint.ckpt
    ```
    -   `--rm`: Automatically removes the container when it exits.
    -   `-v "/path/to/your/data:/data"`: Mounts your local data directory into the `/data` directory inside the container. **Remember to use absolute paths.**

### Option 2: Build the Image Locally

You can also build the Docker image directly from the `dockerfile` in this repository.

1.  **Build the image:**
    ```bash
    docker build -t spaghetti:latest .
    ```

2.  **Run Inference:**
    The `docker run` command is the same as above, just replace the image name:
    ```bash
    docker run --rm -v "/path/to/your/data:/data" spaghetti:latest \
      --input /data/inputs \
      --output /data/outputs \
      --checkpoint /data/spaghetti_checkpoint.ckpt
    ```

## Training your own model
You can also train your own model to perform the inferences. See an example code at `./tutorials/train_example.py`






