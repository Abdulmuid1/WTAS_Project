pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning WTAS project...'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t wtas-api:latest .'
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'This will push to AWS ECR (coming next)'
            }
        }

        stage('Deploy to ECS') {
            steps {
                echo 'This will update ECS Service (coming next)'
            }
        }
    }
}
