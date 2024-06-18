# How to deploy Ogma on the AWS Marketplace

Ogma can be purchased via AWS Marketplace, this documentation describes how to install [Ogma](https://doc.linkurio.us/ogma/latest/) 
bought via the AWS marketplace via the container and Helm delivery methods.
Please refer to the [official Ogma documentation](https://doc.linkurious.com/ogma/latest/) for details about Ogma itself.

## The Basics

Subscribe to Ogma on the AWS Marketplace and follow the Marketplace launch instructions to download the Ogma Helm charts and launch Ogma in Kubernetes.

### Required IAM role

The Ogma container must be run with the `AWSLicenseManagerConsumptionPolicy` IAM policy.
This policy allows the Ogma container to checkout license entitlements from the AWS License Manager.

### Launch Target

Once you have subscribed to Ogma on the AWS Marketplace click through to the `Launch` page. You will be asked to choose a Launch Target.
Choose either `AWS Managed Kubernetes (EKS)` or `Self-Managed Kubernetes (EKS Anywhere)` to access the Ogma Helm chart and instructions.

## Launch Ogma on "EKS"

These instructions are taken from the Launch page of the Ogma product on AWS Marketplace.

### Step 1: Create an AWS IAM role and Kubernetes service account

Use the following commands to create an AWS IAM role and Kubernetes service account.

```sh
kubectl create namespace ogma
```

```sh
eksctl create iamserviceaccount \
    --name ogma \
    --namespace ogma \
    --cluster <ENTER_YOUR_CLUSTER_NAME_HERE> \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringFullAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringRegisterUsage \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy \
    --approve \
    --override-existing-serviceaccounts
```

### Step 2: Launch the software

Use the following commands to launch this software by installing a Helm chart on your Amazon EKS cluster.
The Helm CLI version in your launch environment must be 3.7.1.

Retrieve the Helm chart:

```sh
export HELM_EXPERIMENTAL_OCI=1

aws ecr get-login-password \
    --region us-east-1 | helm registry login \
    --username AWS \
    --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

mkdir ogma && cd ogma

helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/ogma --version 0.2.4

tar xf $(pwd)/* && find $(pwd) -maxdepth 1 -type f -delete
```

Install the Helm chart:

```sh
helm install ogma \
    --namespace ogma ./* \
    --set serviceAccount.create=false \
    --set serviceAccount.name=ogma
```

## Launch Ogma on "EKS Anywhere"

Running Ogma on self-managed Kubernetes via `EKS Anywhere` requires generating an access token and associating it to an IAM account.
These actions, and the following instructions to launch the product, can be found on the Launch page of the Ogma AWS Marketplace product.

## Accessing the user interface

Once a successfully deployed, Ogma starts a web-server running on port `8080`.

There are many different options to configure network egress allowing access to the Ogma pod on port `8080`, one simple option to validate a deployment is to follow the notes provided by the output of the Helm install command:

Example output of the Helm install command:

```sh
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace ogma -l "app.kubernetes.io/name=ogma,app.kubernetes.io/instance=ogma" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace ogma $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080/ogma/latest/ to use your application"
  kubectl --namespace ogma port-forward $POD_NAME 8080:$CONTAINER_PORT
2. Please log in using username: "ogma" and password: "******".
```

These commands temporarily port-forwards from `localhost:8080` to `your-pod:8080`, meaning you can view the Ogma user-interface at <http://localhost:8080/ogma/latest/> while these commands run.

## Launch standalone container

### Pull the image

Login to the ECR (Elastic Container Registry):

```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com
```

Pull the image:

```sh
docker pull 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/ogma-container:5.0.8-rc3
```

### Run the container

You can now run the container, exposing port `8080` locally.

```sh
docker run --rm -p8080:8080 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/ogma-container:5.0.8-rc3
```

You can now open <http://127.0.0.1:8080/ogma/latest/> to use the application.

### Run the container with password protection

Generate an `htpasswd` file locally, for a user named `ogma`:

```sh
htpasswd ./htpasswd ogma
```

Alternatively use on online generator such as <https://www.web2generators.com/apache-tools/htpasswd-generator>, and save the content to a file named htpasswd

You can now run the container, exposing port `8080` locally.

```sh
docker run --rm -p8080:8080 -v ./htpasswd:/etc/nginx/htpasswd-conf/htpasswd 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/ogma-container:5.0.8-rc3
```

You can now open <http://127.0.0.1:8080/ogma/latest/> to use the application, you will need to provide username and password used to generate the `htpasswd` file.

## Getting support

For assistance installing and configuring Ogma on the AWS Marketplace [please get in touch](https://doc.linkurious.com/ogma/latest/contact.html)
