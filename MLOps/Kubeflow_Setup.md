# Setting up Kubeflow on AWS EKS

**NOTE:** For this Demo I will be using `us-west-2` region for everything. Regiion is very important for this demo.

### Workspace Setup

We will be using AWS Cloud9 as our terminal workspace and SageMaker Jupyter Lab for Notebooks. 

To setup the Cloud9 environment:
- Login to your AWS account and Search for **Cloud9**
- Open Cloud9 service and Select Create environment
- Name it workspace, click Next.
- Choose `m5.large` for instance type, take all default values and click Create environment

When it comes up, you can open the evironment and start using the terminal.

To setup the SageMaker Jupyter Instance:
- Search for SageMaker and open its page
- On the left bar select **Notebook** and click on **Notebook Instances**
- Click on **Create Notebook Instance**
- Name your notebook instance
- Choose `ml.c5d.xlarge` for instance type
- Go down to "Git repositories" and from drop down select "Clone a public Git repository to this notebook instance only"
- Enter the following: `https://github.com/iam-abbas/Plaksha-DRL.git`
- Click on **Create Notebook**

We will use the Notebook workspace to code our pipelines (Because UI is much more neat and its easy to understand).

### Installing required tools

Now that your workspaces are setup, go back to Cloud0 environment and install following packages.

##### Kubectl
```bash
sudo curl --silent --location -o /usr/local/bin/kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
sudo chmod +x /usr/local/bin/kubectl
```

##### Update AWS CLI
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

##### YAML and JSON Dependencies 
```bash
sudo yum -y install jq gettext bash-completion moreutils
```
```bash
echo 'yq() {
  docker run --rm -i -v "${PWD}":/workdir mikefarah/yq "$@"
}' | tee -a ~/.bashrc && source ~/.bashrc
```
```bash
for command in kubectl jq envsubst aws
  do
    which $command &>/dev/null && echo "$command in path" || echo "$command NOT FOUND"
  done
```

##### Kustomize
```bash
curl --silent --location --remote-name \
"https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v3.2.3/kustomize_kustomize.v3.2.3_linux_amd64" && \
chmod a+x kustomize_kustomize.v3.2.3_linux_amd64 && \
sudo mv kustomize_kustomize.v3.2.3_linux_amd64 /usr/local/bin/kustomize
kustomize version
```

##### eksctl
```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv -v /tmp/eksctl /usr/local/bin
```

##### IAM Authenticator
```bash
curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.15.10/2020-02-22/bin/linux/amd64/aws-iam-authenticator
chmod +x aws-iam-authenticator
sudo mv aws-iam-authenticator /usr/local/bin
```

### Setting up permissions

You will need to create an IAM Role that has enough privileges to manage EKS Clusters

##### IAM Role
Create a new IAM Role by:
1. Go to IAM Console page
2. Go to **Roles** tab
3. Click on **Create Role**
4. Select "EC2" under usecase and click Next
5. Type "Administrator" in search box and select "AdministratorAccess"
6. Click **Next** and name the role as "Master"
7. Click **Create Role**

##### Attach your IAM Role to Cloud9
Now you need to attach the IAM Role to your Cloud9 environment

1. In your enviroment, click on your avatar
2. Click on "Manage EC2 Instance"
3. Select the instance and click on **actions** on top right.
4. Under "Security" click **Modify IAM Role**
5. Select the **Master** service role you created
  
##### Update IAM Settings for your workspace

Now you need to ensure that you are using right credentials in your terminal

Go back to your terminal and enter following commands
```bash
aws cloud9 update-environment  --environment-id $C9_PID --managed-credentials-action DISABLE
rm -vf ${HOME}/.aws/credentials
```

To check if the roles are successfully setup:
```bash
aws sts get-caller-identity --query Arn | grep Master -q && echo "IAM role valid" || echo "IAM role NOT valid"
```

### Creating EKS Cluster

Lets define our environment variables that we can re use later.
```bash
export CLUSTER_NAME=kflow-aws
export CLUSTER_REGION=us-west-2
```

Create EKS Cluster using eksctl
```bash
eksctl create cluster \
--name ${CLUSTER_NAME} \
--version 1.20 \
--region ${CLUSTER_REGION} \
--nodegroup-name linux-nodes \
--node-type m5.xlarge \
--nodes 2 \
--nodes-min 2 \
--nodes-max 5 \
--managed \
--with-oidc
```
**NOTE:** This step may take up to 20 Minutes!

Validate your cluster
```bash
eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} \
--region ${CLUSTER_REGION} --approve
```

### Installing Kubeflow

Download the Kubeflow packages
```bash
export KUBEFLOW_RELEASE_VERSION=v1.5-branch
git clone https://github.com/awslabs/kubeflow-manifests.git
cd kubeflow-manifests
git clone --branch ${KUBEFLOW_RELEASE_VERSION} https://github.com/kubeflow/manifests.git upstream
```

Install the manifests using Kustomize
```bash
while ! kustomize build deployment/vanilla | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```

Deploy Kubeflow locally
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

After running the command, you can access the Kubeflow Central Dashboard by doing the following:

- Go to **Tools**
- Click **Preview**
- Click **Preview Running Application**
- Login with the default user’s credential. The default email address is `user@example.com` and the default password is `12341234`.

### Extras

To connect to existing EKS use following command

```bash
export CLUSTER_NAME=kflow-aws
export CLUSTER_REGION=us-west-2
aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${CLUSTER_REGION}
```