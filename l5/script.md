# **Task 1. 2.**

`local`
## install kubectl
```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2 curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

## create master https://rancher.com/blog/2019/k3s-kubeconfig-in-seconds
```bash
sudo -i
curl -sLS https://raw.githubusercontent.com/alexellis/k3sup/master/get.sh | sh
cd /usr/local/bin
export SERVER_IP=184.73.55.119
export SLAVE0_IP=35.153.157.218
export SLAVE1_IP=54.81.241.219
./k3sup install --ip $SERVER_IP --user ubuntu
```

`server`
## set roles
```bash
kubectl label node ip-172-31-45-51 node-role.kubernetes.io/worker=worker
kubectl label node ip-172-31-40-90 node-role.kubernetes.io/worker=worker
```

`local`
## config
```bash
export KUBECONFIG=/usr/local/bin/kubeconfig
kubectl get node -o wide
```

# **Task 3.**
- *what is the difference between a Docker container and a Kubernetes Pod?*
    <br>
    https://enterprisersproject.com/article/2020/9/pod-cluster-container-what-is-difference#:~:text=%E2%80%9CA%20container%20runs%20logically%20in,tight%20logical%20borders%20called%20namespaces.%E2%80%9D

    A fundamental difference between Kubernetes and Docker is that Kubernetes is meant to run across a cluster while Docker runs on a single node. Kubernetes is more extensive than Docker Swarm and is meant to coordinate clusters of nodes at scale in production in an efficient manner. Kubernetes pods—scheduling units that can contain one or more containers in the Kubernetes ecosystem—are distributed among nodes to provide high availability.

    https://kubernetes.io/docs/concepts/workloads/pods/

    A Pod (as in a pod of whales or pea pod) is a group of one or more containers, with shared storage/network resources, and a specification for how to run the containers. A Pod's contents are always co-located and co-scheduled, and run in a shared context.
    </br>
- *what are the following Kubernetes objects and what are they used for?*
    - *deployment*
        <br>
        https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

        You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments. 
        </br>
    - *service*
        <br>
        https://kubernetes.io/docs/concepts/services-networking/service/

        Is an abstraction which defines a logical set of Pods and a policy by which to access them. 
        </br>
    - *daemonset*
        <br>
        https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/

        A DaemonSet ensures that all (or some) Nodes run a copy of a Pod. As nodes are added to the cluster, Pods are added to them. As nodes are removed from the cluster, those Pods are garbage collected. Deleting a DaemonSet will clean up the Pods it created.
        </br>
    - *statefulset*
        <br>
        https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

        StatefulSet is the workload API object used to manage stateful applications.
        </br>
    - *configmap*
        <br>
        https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/

        ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portableю
        </br>
    - *secret*
        <br>
        https://kubernetes.io/docs/concepts/configuration/secret/

        Kubernetes Secrets let you store and manage sensitive information, such as passwords, OAuth tokens, and ssh keys. Storing confidential information in a Secret is safer and more flexible than putting it verbatim in a Pod definition or in a container image.
        </br>
    - *persistentvolume(claim)*
        <br>
        https://kubernetes.io/docs/concepts/storage/persistent-volumes/

        A *PersistentVolume (PV)* is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes. It is a resource in the cluster just like a node is a cluster resource. PVs are volume plugins like Volumes, but have a lifecycle independent of any individual Pod that uses the PV. This API object captures the details of the implementation of the storage, be that NFS, iSCSI, or a cloud-provider-specific storage system.

        A *PersistentVolumeClaim (PVC)* is a request for storage by a user. It is similar to a Pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and Memory). Claims can request specific size and access modes (e.g., they can be mounted ReadWriteOnce, ReadOnlyMany or ReadWriteMany, see AccessModes).
        </br>
- *how to deploy these objects to your Kubernetes cluster?*
    ```bash
    sudo scp -i aws_key.pem -r $HOME/CODE/l5-tn17-NumGuy/examples ubuntu@$SERVER_IP:/home/ubuntu/examples

    kubectl create -f configmap.yaml
    kubectl create -f service.yaml
    kubectl create -f deployment.yaml
    ```
    ![1](imgs/1.png)
    ![2](imgs/2.png)
- deploy the provided sample manifests (`examples/plain_manifests`),
    check if they were correctly deployed (`kubectl get`),
    explain what these manifests do,
    eventually, delete them from your cluster
    ![3](imgs/3.png)

# **Task 4.**
https://github.com/deislabs/helm-workshop

`local`
## Install helm
```bash
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```
## Deploy the provided sample Helm chart
```bash
$ kubectl api-resources | grep deployment

# Changed /templates/deployment.yaml
# apiVersion: apps/v1beta2
# to
# apiVersion: apps/v1

helm install --dry-run --debug ./nginx-example --generate-name
helm install example ./nginx-example

kubectl get pods 
# example-nginx-example-54b7c7c954-x2477
kubectl describe pod example-nginx-example-54b7c7c954-x2477
kubectl logs example-nginx-example-54b7c7c954-x2477
```
![4](imgs/4.png)
## Remove from cluster
```bash
helm uninstall example
```
## How to use values defined in `values.yaml`?
```bash
path: {{ .Values.path }}
```
## how to use 3rd party Helm charts in your chart?
https://stackoverflow.com/questions/52552876/configuring-third-party-helm-charts-from-my-application-helm-chart
    by adding dependecies in `chart.yaml` and override some values in `values.yaml`
# **Task 5. 6. 7.**
## Push docker images as public images on your Docker Hub
```bash
$ sudo docker build -t lsdp5 .
$ docker tag lsdp5 numguy/lsdp5:latest
$ docker push numguy/lsdp5
```
## Create a Helm chart for application
```bash
$ helm create helm_chart

$ sudo snap install kompose
$ kompose convert
```
```bash
helm install l5 helm_chart
#redash
helm upgrade --install -f helm_chart/my-values.yaml myredash redash/redash
kubectl get pods -o wide
kubectl get services
kubectl port-forward myredash-redash-58dcf97f9d-5tkzr 5000
```
![5](imgs/5.png)
```bash
# rollbask changes
helm upgrade myredash redash/redash
helm history myredash
helm rollbask myredash 1
# uninstalling charts
helm uninstall l5
helm uninstall myredash
```
![6](imgs/6.png)
![7](imgs/7.png)
![8](imgs/8.png)