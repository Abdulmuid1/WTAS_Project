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
                      args '--user root'
                }
            }
            steps {
                 withCredentials([[$class: 'UsernamePasswordMultiBinding',
                          credentialsId: 'aws-credentials',
                          usernameVariable: 'AWS_ACCESS_KEY_ID',
                          passwordVariable: 'AWS_SECRET_ACCESS_KEY']]) {

                dir('terraform') {
                    sh '''
                        # Install required dependencies
                        yum install -y curl jq unzip --allowerasing

                        # Install AWS CLI
                        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                        unzip -o awscliv2.zip || exit 1   # Overwrite files 
                       ./aws/install
                        aws configure set region $AWS_REGION
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY


                        # Install Terraform on Amazon Linux
                        yum install -y yum-utils
                        yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
                        yum install -y terraform

                        # Verify Terraform installation
                        terraform --version

                        # Initialize and apply Terraform configuration
                        terraform init -upgrade
                        terraform apply -auto-approve
                    '''
                    }
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
                        if (!albDns) {
                            error("ALB DNS not found. Exiting.")
                        }
                        writeFile file: 'backend_url.txt', text: "http://${albDns}"
                        echo "Backend URL set to: http://${albDns}"
                    }
                }
            }
        }

        stage('Rebuild React with Updated Backend URL') {
            steps {
                dir('client') {
                    script {
                        def backendUrl = readFile('../backend_url.txt').trim()
                        sh '[ -f .env ] && rm .env'   // Check for the existence of .env before removing it
                        // Write the env file in Jenkins workspace before entering the container
                        writeFile file: '.env', text: "REACT_APP_BACKEND_URL=${backendUrl}\n"
                        docker.image('node:18-slim').inside('--user root -w /app') {
                            sh '''
                                mkdir -p /app
                                cp -r /var/jenkins_home/workspace/WTAS-Pipeline/client/. /app
                                cd /app
                                echo "REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}" > .env
                                npm install --no-audit
                                NODE_OPTIONS=--openssl-legacy-provider npm run build
                                cp -r /app/build /var/jenkins_home/workspace/WTAS-Pipeline/client/
                            '''
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