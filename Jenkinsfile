pipeline {
    agent any

    environment {
        AWS_REGION = 'ca-central-1'
        ECR_REPO = 'wtas-api'
        IMAGE_TAG = 'latest'
        AWS_ACCOUNT_ID = '643989280406'
    }

    stages {
        stage('Deploy to ECS with Terraform') {
            agent {
                docker {
                     image 'amazonlinux:latest'
                }
            }
            steps {
                dir('terraform') {
                    sh '''
                        yum install -y curl jq unzip
                        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                        unzip awscliv2.zip
                        ./aws/install
                        aws configure set region $AWS_REGION
                        terraform init -upgrade
                        terraform apply -auto-approve
                    '''
                }
            }
        }

        stage('Fetch ALB DNS from AWS') {
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'aws-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        def albDns = sh(
                            script: """
                                aws elbv2 describe-load-balancers \\
                                --names "wtas-lb" \\
                                --region $AWS_REGION \\
                                --query 'LoadBalancers[0].DNSName' \\
                                --output text
                            """,
                            returnStdout: true
                        ).trim()
                        env.REACT_APP_BACKEND_URL = "http://${albDns}"
                        echo "Backend URL set to: ${env.REACT_APP_BACKEND_URL}"
                    }
                }
            }
        }

        stage('Rebuild React with Updated Backend URL') {
            steps {
                dir('client') {
                    script {
                        docker.image('node:18-slim').inside('--user root -w /app') {
                            sh """
                                echo "REACT_APP_BACKEND_URL=${env.REACT_APP_BACKEND_URL}" > .env
                                cp -r . /app
                                cd /app
                                npm install --no-audit
                                NODE_OPTIONS=--openssl-legacy-provider npm run build
                                cp -r /app/build ./client/build
                            """
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