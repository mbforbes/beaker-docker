# beaker-docker

Testing using Docker file at https://github.com/beaker/docs/blob/main/docs/start/run.md, which is copied here as `Dockerfile`.

I think that `--gpus all` is now required for Docker to have access to GPUs. This is causing failures when I try to run images with beaker.

The issue below persists when I instead start from an `nvidia/cuda` image (`nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu20.04`) and then install python. I still need to pass `--gpus all` when running.

## steps to reproduce

After installing Docker, clone this repository and run

```bash
docker --version
docker build -t my-experiment .
docker run --rm -it my-experiment nvidia-smi
docker run --rm -it --gpus all my-experiment nvidia-smi
```

## my output

```bash
$ docker --version
Docker version 20.10.8, build 3967b7d

$ docker build -t my-experiment .
# ...

$ docker run --rm -it my-experiment nvidia-smi
docker: Error response from daemon: OCI runtime create failed:
container_linux.go:380: starting container process caused: exec:
"nvidia-smi": executable file not found in $PATH: unknown.

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
```
