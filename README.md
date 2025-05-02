# Hotel Reservation Prediction

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0.3-green?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?logo=jenkins&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-Model-green?logo=lightgbm&logoColor=white)

## Live Application
**Try before I am out of AWS credits**: [Hotel Reservation Prediction](http://a4d76dacd85884eaaa2c0f1b1e173b67-1601615365.us-east-1.elb.amazonaws.com)

## Overview
This project demonstrates an end-to-end MLOps pipeline for predicting hotel reservations. It includes data ingestion, preprocessing, model training, and deployment. The application is deployed on AWS using EKS and Load Balancer, and it features a Flask-based web interface for user interaction.

## Features
- **MLOps Pipeline**: Automates machine learning workflows.
- **Flask Web Application**: User-friendly interface for predictions.
- **AWS Deployment**: Hosted on AWS using EKS and Load Balancer.
- **Dockerized Application**: Fully containerized for portability.
- **CI/CD Pipeline**: Seamless integration and deployment with Jenkins and GitHub Actions.
- **LightGBM Model**: Efficient and accurate predictions.

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework for the application.
- **Docker**: Containerization for consistent environments.
- **AWS**: Cloud platform for deployment.
- **Jenkins**: CI/CD pipeline for automation.
- **GitHub Actions**: For continuous integration and deployment.
- **LightGBM**: Machine learning model for predictions.

## Getting Started

### Prerequisites
- Python 3.9+
- Docker
- AWS CLI
- kubectl
- Jenkins (optional for CI/CD)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/hotel-reservation-prediction.git
   cd hotel-reservation-prediction
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the Docker image:
   ```bash
   docker build -t flask-app .
   ```

4. Run the Docker container:
   ```bash
   docker run -p 5000:5000 flask-app
   ```

5. Access the application:
   Open your browser and navigate to `http://localhost:5000`.

### Deployment on AWS
1. Push the Docker image to Amazon ECR.
2. Deploy the application to an EKS cluster.
3. Access the application via the Load Balancer URL.

## Deployment Process
- **DinD Deployment**: Used Docker-in-Docker for building and testing the application.
- **GitHub Actions**: Automated CI/CD pipeline for testing and deployment.
- **EKS AWS Deployment**: Deployed the Docker image to an AWS EKS cluster for scalability and reliability.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Open a pull request.



## License
This project is licensed under the MIT License.
