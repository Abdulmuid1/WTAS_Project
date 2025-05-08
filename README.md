
# Winter Transit Alert System (WTAS)

A cloud-deployed, real-time transit delay alert application built with FastAPI, React, Terraform, AWS ECS, and GitLab CI/CD. It delivers timely bus/train delay notifications during harsh Edmonton winters via SMS-style alerts and speaker-style announcements. This project was primarily an opportunity for me to gain practical experience using modern DevOps tools like GitLab, Terraform, Docker, and ECS. I wanted to move beyond theory and actually apply them in a complete deployment pipeline

## Overview

WTAS helps transit users stay informed about delays during winter conditions by simulating live delay data and announcing them through two modes: speaker announcements and SMS-style logs.

- Built with **FastAPI** (Python) for real-time API endpoints
- Frontend in **React** for modern, responsive UI
- Deployed to **AWS ECS (Fargate)** using **Terraform**
- CI/CD via **GitLab Pipelines**
- API exposed through **AWS ALB**, DNS synced into React via GitLab Variable

## Technologies Used

- **FastAPI** for backend APIs
- **React** for frontend alerts interface
- **Terraform** for infrastructure as code (ECS, ALB, VPC, IAM, CloudWatch)
- **Docker** for containerization
- **GitLab CI/CD** for automated build, deploy, and variable updates
- **Amazon ECS + ALB + ECR** for container orchestration
- **Node.js**, **Axios**, and **CORS middleware**

## Features

- Live delay simulation using periodic updates
- Speaker announcements view
- SMS alerts view
- Manual refresh + toggle visibility
- Last updated timestamp on alerts
- Automatically syncs React backend URL via ALB DNS during pipeline deploy
- Health endpoint for ALB to validate app status


## Installation (Local Testing)

### Prerequisites

- Python 3.10+
- Node.js + npm
- Docker (for building images)
- Uvicorn (backend dev server)
- FastAPI, React, and dependencies listed in `requirements.txt` and `package.json`

### 1. Clone this repository

```bash
git clone https://github.com/Abdulmuid1/WTAS_Project.git
cd WTAS_Project
```

### 2. Set the local backend URL in React

Create a `.env` file inside the `client/` folder:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### 3. Run the FastAPI backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run the React frontend

```bash
cd client (navigate to the client folder)
npm install
npm start
```

### 5. Open the app

Visit: [http://localhost:3000] 


##  Production Deployment (AWS ECS)

The app is deployed to AWS via Terraform and GitLab CI/CD:

- `terraform/main.tf` provisions ECS, Load Balancer, IAM roles, and networking
- CI/CD pipeline stages:
  - deploy-backend – Terraform provisions all AWS infrastructure (ECS, ALB, etc.)
  - update-backend-url – GitLab syncs the new ALB DNS to REACT_APP_BACKEND_URL
  - rebuild-react – React rebuilds with the correct backend URL
  - dockerize-final – Docker image is rebuilt and pushed to ECR

### GitLab CI/CD Preview

```yaml
stages:
  - deploy-backend
  - update-backend-url
  - rebuild-react
  - dockerize-final
```

## Directory Structure

NOTE:
The __init__.py file in Python is used to indicate that the directory should be treated as a package/module. This allows you to import functions or classes from that folder using Python's module syntax.

```
WTAS_Project/
│
├── app/
│   ├── main.py  
│   ├── api/routes.py
|   ├── core/config.py 
│   ├── models/transit.py
│   ├── services/alerts.py
│   └── utilities/helper.py
│
├── client/
|    └──src/
│       ├── App.js
│       ├── Sms_alerts.js
│       ├── Speaker_announce.js
│       └── Delay_alerts.js
│
├── k8s/
├── terraform/
├── tests/
├── .gitlab-ci.yml
├── Dockerfile
├── Dockerfile.jenkins
├── Jenkinsfile
├── requirements.txt
├── README.md
└── .env
```

## Usage Instructions

- Launch the application locally or visit the deployed URL.
- To view the delay alerts:
   - Click the **Refresh SMS Alerts** or **Refresh Speaker Announcements** button first. This fetches the latest data from the backend.
   - Then click the **Show SMS Alerts** or **Show Speaker Announcements** button to reveal the alerts.
- You can hide the alerts by clicking the same button again.
- The "Last updated" timestamp appears below the title, indicating when the data was last refreshed.

## Troubleshooting

### 405 Method Not Allowed?

Fixed by:
- Mounting React static files under `/static`
- Prefixing all API routes with `/api`

### DNS Errors?

Ensure:
- Your Load Balancer DNS is updated into GitLab using the `update_backend_url` job
- Your final React build includes the synced `REACT_APP_BACKEND_URL`

### React shows old DNS?

React embeds env vars at build time. Be sure to:
- Rebuild after updating `.env`
- Use GitLab to trigger a second final rebuild with the new DNS


## Future Enhancements

- Audio announcement playback
- SMS integration using Twilio
- Map view for affected transit routes
- Mobile responsiveness
- Admin dashboard to control delay injection

## Suggestions for Transit Authorities
- Implement dedicated express bus routes between major commuter zones such as Southside and Downtown, operating without intermediate stops This approach would significantly reduce travel time, enhance efficiency, and improve reliability, particularly during high-demand winter periods.

- Increase bus frequency during severe weather conditions to accommodate higher passenger volumes and reduce wait times, helping to maintain consistent service levels despite disruptions.

- Integrate real-time delay information with public infrastructure, such as electronic signage at transit stops and mobile alert systems, to ensure that commuters are informed promptly and accurately.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS] (https://aws.amazon.com/containers/)
- [React](https://reactjs.org/)