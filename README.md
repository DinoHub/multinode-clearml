# Multinode-Mingle

## Problem statement
 More often than not, it suffices to train a model on multiple GPUs on a single node. As Large Language Models (LLM) become the norm, multi-machine multi-gpu training becomes neccessary due to the large data/model size despite its less than ideal training speeds due to network overheads. Most Machine Learning frameworks supports some form of multinode GPU training. The most widely adopted today is a Distributed Data-Parallel Training (DDP). 
 
 
## How DDP works underneath Pytorch
Using Pytorch (Currently most popular framework) as an example. A Distributed Data Parallel (DDP) application can be executed on multiple nodes where each node can consist of multiple GPU devices. Each node in turn can run multiple copies of the DDP application, each of which processes its models on multiple GPUs.

Let N be the number of nodes on which the application is running and G be the number of GPUs per node. The total number of application processes running across all the nodes at one time is called the World Size, W and the number of processes running on each node is referred to as the Local World Size, L.

Each application process is assigned two IDs: a local rank in [0, L-1] and a global rank in [0, W-1].

To illustrate the terminology defined above, consider the case where a DDP application is launched on two nodes, each of which has four GPUs. We would then like each process to span two GPUs each.

![DDP](/images/pytorchddp.png "DDP").
Reference: https://github.com/pytorch/examples/blob/main/distributed/ddp/README.md

## What are we solving here?
To perform the above training, we need to run 4 identical scripts, which we will identify them as **global** RANK 0, RANK 1, RANK 2 and RANK 3. For this to work, scripts that are identified as RANK 1, 2 and 3 needs to know the IP Address of the script that's running as RANK 0. In normal circumstances, this is not a problem. But in situations where you its not convenient to retrieve the IP address, this can be an issue. An example is when you are running DDP as  Kubernetes PODs.

## Convenience package
This is a convenience package that will allow all the scripts from RANK 1 to N to run and wait for the RANK 0 script to run. When RANK 0 script finally runs, the scripts from RANK 1 to N will receive an IP address to perform their DDP. To allow multiple DDPs of different training to run, we also include an ID that can be defined by the user. Only when the script reaches 'End', then will control be continued and the ML frameworks DDP will take in the Rank0 IP and its own interface IP for its operation.
![Architecture](/images/nodemingle.drawio.png "Architecture").