# o-o

**o&#8209;o** is a command line interface for running jobs on ephemeral
cloud instances with tracked inputs and outputs. Building data or MLOps
pipelines is as simple as stringing together multiple commands, as easily as
running locally, but with the power of cloud compute and storage.

## Highlights

* Easily run any command in any language in cloud compute environments
* Flexible. Define your own run environments with docker images and machine types
* Traceable. Trace all inputs to the commands that produced them
* You control your data. Data and source code is stored in your managed buckets
* Support for Scaleway and Google Cloud (more to come...)

## Getting Started

Follow the [installation instructions](https://o-o.tools/) to configure
**o-o**. Once setup, define environments and datastores in an `.ooconfig` file:

```yaml
project: test-project
environments:
  - name: scaleway
    provider: scaleway
    image: docker.io/debian:stable-slim
    machinetype: STARDUST1-S
    region: fr-par-1
  - name: gcp
    provider: gcp
    image: docker.io/debian:stable-slim
    machinetype: e2-highcpu-2
    region: northamerica-northeast1-b
  - name: scaleway-l4
    provider: scaleway
    image: docker.io/nvidia/cuda:11.0.3-base-ubuntu20.04
    machinetype: L4-1-24G
    region: fr-par-1
datastores:
  - name: my-datastore
    provider: scaleway
    bucket: o-o-data
    region: fr-par
```

Lets start with a simple example that creates a `data.txt` file containing
"Hello World" (under the hood, **o-o** will start and configure our `scaleway`
environment, execute our command, copy output files to our datastore, and
finally, delete the Scaleway instance).

```console
$ o-o run --environment scaleway --message "create data.txt" -- \
    'echo "Hello World" > o://output/data.txt'
```

We completed our first run! `o-o run --list` displays the run's id (in this
case `ntus965ryy`) and message:

```console
$ o-o run --list
ntus965ryy create data.txt
```

You are free to run commands in any configured environment. Let's run a second
command in our `gcp` environment that uses the output of `ntus965ryy`
as input, and simply prints the contents of `data.txt`:

```console
$ o-o run --environment gcp --message "print data.txt" -- \
    cat o://ntus965ryy/data.txt
Hello World

$ o-o run --list
ntus965ryy create data.txt
cxdbx8am38 print data.txt
```

GPUs are also available with properly configured environments. The
`scaleway-l4` environment we configured above supports GPU workloads:

```console
$ o-o run --environment scaleway-l4 --message "try gpu environment" -- nvidia-smi
Sat Feb 1 10:00:00 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.195.03             Driver Version: 570.195.03     CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA L4                      Off |   00000000:01:00.0 Off |                    0 |
| N/A   36C    P0             27W /   72W |       0MiB /  23034MiB |      2%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

And that's the basics. Find out more in the [documentation](https://o-o.tools/)
and with `o-o --help`.
