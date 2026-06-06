# 🚗 Vehicle Insurance Prediction - End-to-End MLOps Project

Welcome to this MLOps project, designed to demonstrate a complete machine learning pipeline for predicting customer interest in vehicle insurance. This project showcases data ingestion, validation, transformation, model training, prediction serving, Docker containerization, AWS deployment, and CI/CD automation using GitHub Actions.

Follow along to understand how the project was built from scratch and deployed to production.

---

## 📁 Project Setup and Structure

### Step 1: Project Overview
- The objective of this project is to predict whether a customer is interested in purchasing vehicle insurance based on demographic and vehicle-related information, helping insurance companies identify potential customers and improve marketing efficiency.
- This project was developed as an end-to-end MLOps solution covering the complete machine learning lifecycle, including data ingestion from MongoDB Atlas, data validation, data transformation, model training, and prediction serving through FastAPI.
- The application is containerized using Docker and deployed on AWS EC2 with CI/CD automation using GitHub Actions, enabling automatic deployment whenever new code is pushed to the GitHub repository.
  

### Project Structure

```text
vehicle_insurance_project/

├── notebook/
│   └── research.ipynb
│
├── src/
│   └── vehicle_insurance/
│       ├── constants/
│       ├── configuration/
│       ├── data_access/
│       ├── entity/
│       ├── exception/
│       ├── logger/
│       ├── components/
│       ├── pipeline/
│       ├── utils/
│       └── cloud/
│
├── templates/
├── static/
├── app.py
├── Dockerfile
├── requirements.txt
├── setup.py
└── README.md
```

---

### Step 2: Package Management

Configured:

```text
setup.py
requirements.txt
```

Purpose:

* Install project dependencies
* Import local packages
* Manage project structure

---

### Step 3: Virtual Environment and Dependencies

Create virtual environment:

```bash
conda create -n vehicle python=3.11 -y
conda activate vehicle
```

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## 📊 MongoDB Setup and Data Management

### Step 4: MongoDB Atlas Configuration

1. Create a MongoDB Atlas account and set up a new project for the Vehicle Insurance dataset.
2. Configure a free cluster, create database credentials, and allow network access for application connectivity.
3. Generate the MongoDB connection string and use it to establish communication between the application and the database.

Example:

```bash
mongodb+srv://<username>:<password>@cluster.mongodb.net
```

---

### Step 5: Upload Dataset to MongoDB

1. Load the Vehicle Insurance dataset and connect to MongoDB Atlas using the generated connection string.
2. Insert the dataset into a MongoDB collection for centralized cloud-based storage.
3. Verify the uploaded records in MongoDB Atlas before using them in the data ingestion pipeline.

---

## 📝 Logging, Exception Handling and EDA

### Step 6: Logging and Exception Handling

Created:

```text
logger/
└── logger.py

exception/
└── exception.py
```

Purpose:

* Track pipeline execution
* Capture errors
* Improve debugging

---

### Step 7: Exploratory Data Analysis (EDA) and Feature Engineering

Performed:

* Data Understanding
* Missing Value Analysis
* Feature Analysis
* Target Variable Analysis
* Correlation Analysis
* Feature Engineering

Notebook Used:

```text
notebook/research.ipynb
```

---

## 📥 Data Ingestion Pipeline

### Step 8: MongoDB Connection Configuration

Created:

```text
configuration/
└── mongo_db_connection.py
```

Responsibilities:

* Connect to MongoDB Atlas
* Retrieve dataset
* Handle database operations

---

### Step 9: Data Ingestion Component

Created:

```text
components/
└── data_ingestion.py
```

Tasks:

* Read data from MongoDB
* Export raw dataset
* Train-Test Split
* Generate ingestion artifacts

---

## 🔍 Data Validation, Transformation & Model Training

### Step 10: Data Validation

- Define schema in config/schema.yaml and implement validation logic in components/data_validation.py.

### Step 11: Data Transformation
- Implement data transformation logic in components/data_transformation.py for feature scaling, encoding, and preprocessing.

### Step 12: Model Training
- Train and evaluate multiple machine learning models in components/model_trainer.py, select the best-performing model, and save it as trained_model.pkl.

### Step 13: Prediction Pipeline
- Create pipeline/prediction.py to load the trained model, process user input, and generate insurance purchase predictions.

## 🚀 Model Evaluation, Model Pusher, and Web Application

### Step 14: Model Evaluation & Model Pusher

- Implement model evaluation and model deployment components.
- Compare the trained model with the production model and push the best model for deployment.

### Step 15: Prediction Pipeline and FastAPI Application

- Create the Prediction Pipeline and integrate it with the FastAPI application.
- Develop templates and static files for the web interface.

```bash
uvicorn app:app --reload
```

---
## 🐳 Dockerization

### Step 16: Docker Setup

1. Create a Dockerfile to containerize the Vehicle Insurance Prediction application.
2. Build the Docker image and verify successful image creation.
3. Run the application inside a Docker container and test local deployment.

```bash
docker build -t vehicle-insurance .

docker images

docker run -d -p 8000:8000 vehicle-insurance
```

---

## ☁️ AWS Setup

### Step 17: IAM User Setup

1. Create an IAM user in AWS and generate an Access Key ID and Secret Access Key for programmatic access.
2. Configure the AWS CLI locally and verify the credentials using AWS Security Token Service (STS).
3. Store the AWS credentials securely in GitHub Secrets for CI/CD automation.

```bash
aws sts get-caller-identity
```

---

### Step 18: Amazon ECR & EC2 Setup

1. Create an Amazon ECR repository to store Docker images and authenticate Docker with ECR.
2. Launch an Ubuntu EC2 instance, configure security groups, and install Docker for deployment.
3. Push the Docker image to ECR and pull it on the EC2 instance for application deployment.

```bash
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-north-1.amazonaws.com

docker tag vehicle-insurance:latest <ACCOUNT_ID>.dkr.ecr.eu-north-1.amazonaws.com/vehicle-insurance:latest

docker push <ACCOUNT_ID>.dkr.ecr.eu-north-1.amazonaws.com/vehicle-insurance:latest

sudo apt update

sudo apt install docker.io -y

sudo docker pull <ACCOUNT_ID>.dkr.ecr.eu-north-1.amazonaws.com/vehicle-insurance:latest
```

---

## 🔄 Deployment and CI/CD Automation

### Step 19: Application Deployment

1. Push the Docker image to Amazon ECR and verify successful upload.
2. Pull the latest Docker image on the EC2 instance.
3. Run the application container and access the application through the EC2 Public IP.

```bash
docker push <ECR_URI>

docker pull <ECR_URI>

docker run -d -p 8000:8000 --name vehicle-app <ECR_URI>
```

---

### Step 20: GitHub Secrets Configuration

1. Configure GitHub Secrets for AWS authentication and deployment automation.
2. Store ECR and EC2 configuration values securely.
3. Enable secure communication between GitHub Actions and AWS services.

GitHub Secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION

ECR_REGISTRY
ECR_REPOSITORY

EC2_HOST
EC2_USERNAME
EC2_SSH_KEY
```

---

### Step 21: GitHub Actions CI/CD Pipeline

1. Configure GitHub Actions to build Docker images automatically.
2. Push the latest image to Amazon ECR whenever code is pushed to GitHub.
3. Deploy the updated application automatically to the EC2 instance.

Workflow:

```text
Git Push
    ↓
GitHub Actions
    ↓
Build Docker Image
    ↓
Push to ECR
    ↓
Deploy to EC2
    ↓
Application Updated
```

---

## 🎯 Project Workflow Summary

1. MongoDB Atlas ➜ Data Ingestion
2. Data Validation ➜ Data Transformation
3. Model Training ➜ Prediction Pipeline
4. FastAPI Application ➜ User Predictions
5. Docker ➜ Containerization
6. Amazon ECR ➜ Image Registry
7. Amazon EC2 ➜ Application Hosting
8. GitHub Actions ➜ Automated Deployment

---

This README provides a structured walkthrough of the MLOps project, showcasing the end-to-end pipeline, cloud integration, CI/CD setup, and robust data handling capabilities.
