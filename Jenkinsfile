pipeline {
    agent any

    environment {
        AWS_REGION = 'ca-central-1'
        ECR_REPO = 'wtas-api'
        IMAGE_TAG = 'latest'
        AWS_ACCOUNT_ID = '643989280406'
    }

    stages {
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
                dir('terraform') {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }

    }
}
