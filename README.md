# 🚀 Wazuh Deployment with CI/CD on AWS

This repository contains an automated **CI/CD pipeline** for deploying **Wazuh in a multi-node Docker Swarm cluster** using **GitHub Actions, AWS CodeBuild (self-hosted runners).  

The pipeline builds, tests, and deploys Wazuh components inside an AWS environment while enforcing security best practices (secrets, TLS, scanning, etc.).

---

## 📌 Architecture Overview

The deployment environment is built entirely on **AWS Cloud** to ensure scalability, isolation, and automation of the CI/CD process. The main components are:

![Architecture](./docs/aws-architecture.png)  
<!-- Replace with the correct relative path to your first diagram -->

### 🔹 GitHub Actions
- Acts as the central CI/CD orchestrator.
- On every **push/PR to main**, workflows are triggered automatically.
- Jobs are dispatched to **self-hosted runners** (in AWS CodeBuild) instead of using GitHub’s hosted runners, which gives more control over the environment and avoids runner limitations.

### 🔹 AWS CodeBuild (Self-Hosted Runner)
- CodeBuild is configured as a **GitHub self-hosted runner**.
- Provides an **isolated container environment** for running jobs securely.
- Responsible for executing tasks such as:
  - Building container images.
  - Running vulnerability scans (e.g., with Trivy).
  - Executing Selenium tests.
  - Deploying to the target EC2 instance.

This approach ensures that the build environment is **ephemeral** (destroyed after each job), reducing persistence risks.

### 🔹 Virtual Private Cloud (VPC)
- The EC2 instance is deployed inside a **private subnet** of an AWS VPC.
- Security Groups restrict access (e.g., only allowing SSH from CodeBuild, and exposing only necessary Wazuh dashboard ports).
- Ensures isolation from the public internet except where strictly needed.

### 🔹 EC2 Instance (Docker Swarm Manager)
- Acts as the **control plane** of the Docker Swarm cluster.
- Hosts the **Wazuh multi-node stack** (manager, indexer, dashboard).
- Deployment flow:
  1. CodeBuild establishes an **SSH connection** to the EC2 instance.
  2. Stack files and configuration are securely transferred.
  3. Docker Swarm orchestrates the deployment of Wazuh services.
  4. Certificates are generated dynamically to secure Wazuh communications.

### 🔹 Docker Swarm & Wazuh
- **Docker Swarm** is used for container orchestration because it’s simple to set up on a single EC2 instance (and can be extended for multi-node clusters).
- **Wazuh Components** deployed:
  - Wazuh Manager
  - Wazuh Indexer
  - Wazuh Dashboard
- Services are containerized, ensuring **reproducibility** and **scalability**.

---

✅ This architecture ensures:  
- **Automation**: Full CI/CD with no manual intervention.  
- **Security**: Ephemeral build runners, VPC isolation, secrets in GitHub.  
- **Scalability**: Can extend the Docker Swarm cluster with additional EC2 nodes.  
- **Resilience**: Rollback possible by re-deploying a previous stack version.  

---

## ⚙️ Workflow Jobs

The CI/CD pipeline defines **two main jobs**:

![Workflow Jobs](./docs/workflow.png)  
<!-- Replace with the correct relative path to your second diagram -->

### 1. **Deploy Wazuh to Docker Swarm**
Steps:
1. Checkout repository  
2. Configure SSH (private key & known hosts)  
3. Fetch Wazuh multi-node bundle  
4. Upload bundle + stack files to EC2 instance  
5. Run Docker stack to generate certificates & deploy Wazuh components  

---

### 2. **Run Selenium Tests**
Steps:
1. Checkout repository  
2. Install dependencies (Python, pip, etc.)  
3. Install **Chrome** & **Chromedriver**  
4. Run **Selenium tests** against the Wazuh dashboard  

Tests include:  
- ✅ Dashboard reachable & title check  
- ✅ Login form presence  
- ✅ Successful login  

---

## 🛠️ Prerequisites
Before running the pipeline, ensure you have:  
- AWS account with **VPC, EC2, and CodeBuild** configured  
- Docker & Docker Swarm installed on target EC2 instance  
- GitHub repository with:  
  - Workflows under `.github/workflows/*.yml`  
  - Docker stack definition for Wazuh deployment  
  - Ansible configuration items  
- GitHub Secrets:  
  - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`  
  - `SSH_PRIVATE_KEY` (for EC2 connection)  
  - Any other required secrets (TLS, Wazuh credentials, etc.)  

---

