# How to deploy linkurious-enterprise on the AWS Marketplace

linkurious-enterprise can be purchased via AWS Marketplace, this documentation describes how to install [linkurious-enterprise](https://doc.linkurio.us/linkurious-enterprise/latest/) 
bought via the AWS marketplace via the container and Helm delivery methods.
Please refer to the [official linkurious-enterprise documentation](https://doc.linkurious.com/linkurious-enterprise/latest/) for details about linkurious-enterprise itself.

## The Basics

Subscribe to linkurious-enterprise on the AWS Marketplace and follow the Marketplace launch instructions to download the linkurious-enterprise Helm charts and launch linkurious-enterprise in Kubernetes.

### Required IAM role

The linkurious-enterprise container must be run with the `AWSLicenseManagerConsumptionPolicy` IAM policy.
This policy allows the linkurious-enterprise container to checkout license entitlements from the AWS License Manager.

### Launch Target

Once you have subscribed to linkurious-enterprise on the AWS Marketplace click through to the `Launch` page. You will be asked to choose a Launch Target.
Choose either `AWS Managed Kubernetes (EKS)` or `Self-Managed Kubernetes (EKS Anywhere)` to access the linkurious-enterprise Helm chart and instructions.

## Launch linkurious-enterprise on "EKS"

These instructions are taken from the Launch page of the linkurious-enterprise product on AWS Marketplace.

### Step 1: Create an AWS IAM role and Kubernetes service account

Use the following commands to create an AWS IAM role and Kubernetes service account.

```sh
kubectl create namespace linkurious-enterprise
```

```sh
eksctl create iamserviceaccount \
    --name linkurious-enterprise \
    --namespace linkurious-enterprise \
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

mkdir linkurious-enterprise && cd linkurious-enterprise

helm pull oci://709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/lke-aws-hourly365 --version 0.2.7

```

Install the Helm chart:

```sh
helm upgrade --install linkurious-enterprise \
    --namespace linkurious-enterprise lke-aws-hourly365-0.2.7.tgz \
    --set serviceAccount.create=false \
    --set serviceAccount.name=linkurious-enterprise
```

## Launch linkurious-enterprise on "EKS Anywhere"

Running linkurious-enterprise on self-managed Kubernetes via `EKS Anywhere` requires generating an access token and associating it to an IAM account.
These actions, and the following instructions to launch the product, can be found on the Launch page of the linkurious-enterprise AWS Marketplace product.

## Accessing the user interface

Once a successfully deployed, linkurious-enterprise starts a web-server running on port `8080`.

There are many different options to configure network egress allowing access to the linkurious-enterprise pod on port `8080`, one simple option to validate a deployment is to follow the notes provided by the output of the Helm install command:

Example output of the Helm install command:

```sh
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace linkurious-enterprise -l "app.kubernetes.io/name=linkurious-enterprise,app.kubernetes.io/instance=linkurious-enterprise" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace linkurious-enterprise $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080/admin-manual/latest/ to use your application"
  kubectl --namespace linkurious-enterprise port-forward $POD_NAME 8080:$CONTAINER_PORT
2. Please log in using username: "lke" and password: "******".
```

These commands temporarily port-forwards from `localhost:8080` to `your-pod:8080`, meaning you can view the linkurious-enterprise user-interface at <http://localhost:8080/admin-manual/latest/> while these commands run.

## Launch standalone container

### Pull the image

Login to the ECR (Elastic Container Registry):

```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 709825985650.dkr.ecr.us-east-1.amazonaws.com
```

Pull the image:

```sh
docker pull 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/lke-aws-hourly365-container:4.1.6-rc2
```

### Run the container

You can now run the container, exposing port `8080` locally.

```sh
docker run --rm -p8080:8080 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/lke-aws-hourly365-container:4.1.6-rc2
```

You can now open <http://127.0.0.1:8080/admin-manual/latest/> to use the application.

### Run the container with password protection

Generate an `htpasswd` file locally, for a user named `linkurious-enterprise`:

```sh
htpasswd ./htpasswd linkurious-enterprise
```

Alternatively use on online generator such as <https://www.web2generators.com/apache-tools/htpasswd-generator>, and save the content to a file named htpasswd

You can now run the container, exposing port `8080` locally.

```sh
docker run --rm -p8080:8080 -v ./htpasswd:/etc/nginx/htpasswd-conf/htpasswd 709825985650.dkr.ecr.us-east-1.amazonaws.com/linkurious/linkurious-enterprise-hourly-container:5.0.8-rc4
```

You can now open <http://127.0.0.1:8080/linkurious-enterprise/latest/> to use the application, you will need to provide username and password used to generate the `htpasswd` file.

## Getting support

For assistance installing and configuring linkurious-enterprise on the AWS Marketplace [please get in touch](https://doc.linkurious.com/linkurious-enterprise/latest/contact.html)
