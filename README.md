# beaker-docker

Testing using Docker file at https://github.com/beaker/docs/blob/main/docs/start/run.md, which is copied here as `Dockerfile`.

Two symptoms, not positive about underlying issues:

1. I think that `--gpus all`, or (`--runtime=nvidia`?) is now required for Docker to have access to GPUs. This has now been [fixed](https://github.com/beaker/docs/commit/ef01f95816423459e02b100baf1d2e82decf30ed) in the documentation.

2. `nvidia-smi` will not be found by Beaker when running a container. This manifests as exactly the same error mesasge as symptom (1).

Both issues persisted when I instead started from an `nvidia/cuda` image (`nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu20.04`) and then installed python.

## steps to reproduce

After installing Docker, clone this repository and run

```bash
# This demonstrates the issue with Docker.
docker --version
docker build -t my-experiment .
docker run --rm -it my-experiment nvidia-smi  # fails
docker run --rm -it --gpus all my-experiment nvidia-smi  # succeeds
docker run --rm -it --runtime=nvidia my-experiment nvidia-smi  # succeeds

beaker image create --name my-experiment my-experiment
# NOTE: Edit `beaker-conf-failing.yaml` and `beaker-conf.yaml` to set your username.

# This demonstrates nvidia-smi failing on Beaker.
beaker experiment create beaker-conf-failing.yaml

# This demonstrates python successfully finding CUDA and devices on Beaker.
beaker experiment create beaker-conf.yaml
```

## my output

### Docker

```bash
$ docker --version
Docker version 20.10.8, build 3967b7d

$ docker build -t my-experiment .
# ...

# no --gpus flag, no GPUs seen
$ docker run --rm -it my-experiment python main.py
torch: CUDA available: False
torch: CUDA device count: 0

# with --gpus flag
$ docker run --rm -it --gpus all my-experiment python main.py
torch: CUDA available: True
torch: CUDA device count: 1

# ... or with --runtime=nvidia
$ docker run --rm -it --runtime=nvidia my-experiment python main.py
torch: CUDA available: True
torch: CUDA device count: 1

# same thing for nvidia-smi: by itself, it fails
$ docker run --rm -it my-experiment nvidia-smi
docker: Error response from daemon: OCI runtime create failed:
container_linux.go:380: starting container process caused: exec:
"nvidia-smi": executable file not found in $PATH: unknown.

# succeeds with --gpus all
$ docker run --rm -it --gpus all my-experiment nvidia-smi
Mon Aug 23 17:35:13 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.42.01    Driver Version: 470.42.01    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A100-SXM...  Off  | 00000000:00:04.0 Off |                    0 |
| N/A   37C    P0    51W / 400W |      0MiB / 40536MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+

# also succeeds with --runtime=nvidia
$ docker run --rm -it --runtime=nvidia my-experiment nvidia-smi
Tue Aug 24 21:30:45 2021
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.42.01    Driver Version: 470.42.01    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A100-SXM...  Off  | 00000000:00:04.0 Off |                    0 |
| N/A   37C    P0    51W / 400W |      0MiB / 40536MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

### Beaker

```bash
beaker image create --name my-experiment my-experiment
# OK

# Running nvidia-smi
beaker experiment create beaker-conf-failing.yaml
# Experiment runs and fails with:
# StartError: failed to create containerd task: OCI runtime create failed:
# container_linux.go:380: starting container process caused: exec:
# "nvidia-smi": executable file not found in $PATH: unknown

# Running python main.py
beaker experiment create beaker-conf.yaml
# Experiment runs and does find GPUs:
# 2021-08-24T21:30:45.182527592Z	torch: CUDA available: True
# 2021-08-24T21:30:45.182566577Z	torch: CUDA device count: 1
```
