pipeline {
    agent any

    environment {
        AWS_REGION = 'ca-central-1'
        ECR_REPO = 'wtas-api'
        IMAGE_TAG = 'latest'
        AWS_ACCOUNT_ID = '643989280406'
    }

    stages {
        stage('Build React Frontend using Node container') {
            steps {
                dir('client') {
                    script {
                        docker.image('node:18-alpine').inside('--user root -w /app') { // Run as root
                            sh 'mkdir -p /app && chmod -R 777 /app' // Ensure permissions
                            sh 'cp -r . /app'
                            sh 'cd /app && npm install'
                            sh 'cd /app && npm run build'
                        }
                    }
                }
            }
        }


        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'aws-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY']]) {

                    echo "Logging into AWS ECR..."
                    sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION

                        aws ecr get-login-password | docker login --username AWS --password-stdin https://$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag & Push Docker Image') {
            steps {
                echo "Tagging and pushing Docker image to ECR..."
                script {
                    def repoUrl = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
                    sh """
                        docker tag $ECR_REPO:$IMAGE_TAG $repoUrl:$IMAGE_TAG
                        docker push $repoUrl:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Deploy to ECS with Terraform') {
            steps {
                echo "Deploying to ECS using Terraform..."
                dir('terraform') {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment to ECS was successful!'
        }
        failure {
            echo 'Deployment failed. Please check the logs.'
        }
    }
}
