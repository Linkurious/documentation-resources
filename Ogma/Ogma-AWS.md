# How to deploy Ogma on AWS Marketplace

Ogma can be purchased via AWS Marketplace, this documentation describes how to install Ogma bought via the marketplace via the container and Helm delivery methods.

For official documentation of the Ogma Product please visit: <https://doc.linkurious.com/ogma/latest/>

## The Basics

Subscribe to  on the AWS Marketplace and follow the Marketplace launch instructions to download the Ogma Helm charts and launch Ogma in Kubernetes.

### Required IAM role

The Ogma container must be run with the AWSLicenseManagerConsumptionPolicy IAM policy.

This policy allows the Ogma container to checkout license entitlements from the AWS License Manager.

### Launch Target

Once you have subscribed to Ogma on the AWS Marketplace click through to the 'Launch' page. You will be asked to choose a Launch Target.

Choose either AWS Managed Kubernetes (EKS) or Self-Managed Kubernetes (EKS Anywhere) to access the Ogma helm chart and instructions.

Launch Ogma on EKS
These instructions are taken from the Launch page of the Ogma product on AWS Marketplace.

### Step 1: Create an AWS IAM role and Kubernetes service account

Use the following command to create an AWS IAM role and Kubernetes service account.

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

Use the following commands to launch this software by installing a Helm chart on your Amazon EKS cluster. The Helm CLI version in your launch environment must be 3.7.1.

Retrieve helm chart:

```sh
export HELM_EXPERIMENTAL_OCI=1

aws ecr get-login-password \
    --region us-east-1 | helm registry login \
    --username AWS \
    --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com

mkdir ogma && cd ogma

helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/ogma --version 5.0.8

tar xf $(pwd)/* && find $(pwd) -maxdepth 1 -type f -delete
```

Install helm chart:

```sh
helm install ogma-5-0-8 \
    --namespace ogma ./* \
    --set serviceAccount.create=false \
    --set serviceAccount.name=ogma
```

Launch Ogma on EKS Anywhere
Running Ogma on self-managed Kubernetes via EKS Anywhere requires generating an access token and associating it to an IAM account.

These actions, and the following instructions to launch the product, can be found on the Launch page of the Ogma AWS Marketplace product.

## Accessing the UI

On a successful deployment, Ogma starts a web-server with a UI running on port 8080.

There are many different options to configure network egress allowing access to the Ogma pod on port 8080, one simple option to validate a deployment is to follow the notes provided by the output of the Helm install command:

1. Get the application URL by running these commands:

```sh
  export POD_NAME=$(kubectl get pods --namespace ogma -l "app.kubernetes.io/name=ogma,app.kubernetes.io/instance=ogma" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace ogma $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace ogma port-forward $POD_NAME 8080:$CONTAINER_PORT
```

This command temporarily port-forwards from localhost:8080 to your-pod:8080, meaning you can view the ogma UI at <http://localhost:8080> while that command runs.

Get help!
For assistance installing and configuring Ogma on the AWS Marketplace contact <mailto:support@linkurio.us>
