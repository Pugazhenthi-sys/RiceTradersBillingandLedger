pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "${env.DOCKERHUB_REPO}"
        K8S_NAMESPACE = "rice-traders"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat 'git --version'
            }
        }

        stage('Validate Python source') {
            steps {
                bat '''
                    python --version
                    python -m compileall -q .
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    if (!env.DOCKERHUB_REPO?.trim()) {
                        error('Set Jenkins environment variable DOCKERHUB_REPO, e.g. yourdockerid/rice-traders-app')
                    }
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}"
                }
                bat 'docker build -t %DOCKERHUB_REPO%:%BUILD_NUMBER% -t %DOCKERHUB_REPO%:latest .'
            }
        }

        stage('Push image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    bat '''
                        echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin
                        docker push %DOCKERHUB_REPO%:%BUILD_NUMBER%
                        docker push %DOCKERHUB_REPO%:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl config current-context
                    powershell -NoProfile -Command "(Get-Content k8s/deployment.yaml) -replace 'DOCKERHUB_REPO_PLACEHOLDER', $env:DOCKERHUB_REPO | Set-Content k8s/deployment.rendered.yaml"
                    kubectl apply -f k8s/deployment.rendered.yaml
                    kubectl -n %K8S_NAMESPACE% set image deployment/rice-traders-app app=%DOCKERHUB_REPO%:%BUILD_NUMBER%
                    kubectl -n %K8S_NAMESPACE% rollout status deployment/rice-traders-app --timeout=180s
                    kubectl -n %K8S_NAMESPACE% get pods,svc -o wide
                '''
            }
        }
    }

    post {
        always {
            bat 'docker image prune -f'
        }
        success {
            echo 'Build, image push, and Kubernetes deployment completed.'
            echo 'Open the app using the instructions in k8s/README.md.'
        }
    }
}
