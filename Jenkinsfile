def remote = [:]
pipeline {
    agent any
    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest')
    }
    environment {
        REPO = 'anestesia01/http-server'
        DOCKER_TOKEN = credentials('docker-token')
        HOST = '130.49.149.237'
        GIT_URL = 'git@github.com:AnastasiyaGapochkina01/http-py.git'
        PRJ_DIR = '/opt/www/http-server'
        DOCKER_USER = 'anestesia01'
    }

    stages {
        stage('Configure credentials') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'jenkins-key', keyFileVariable: 'private_key', usernameVariable: 'username')]) {
                    script {
                        remote.name = "${env.HOST}"
                        remote.host = "${env.HOST}"
                        remote.user = "$username"
                        remote.identity = readFile "$private_key"
                        remote.allowAnyHosts = true
                    }
                }
            }
        }

        stage('Checkout repo') {
            steps {
                git branch: 'main', url: "${env.GIT_URL}", credentialsId: 'jenkins-key'
            }
        }

        stage('Build and push image') {
            steps {
                script {
                    env.FULL_IMAGE = "${env.REPO}:${params.IMAGE_TAG}"
                    sh """
                        docker build -t ${env.FULL_IMAGE} ./
                        docker login -u ${env.DOCKER_USER} -p ${env.DOCKER_TOKEN}
                        docker push ${env.FULL_IMAGE}
                        docker logout
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        docker pull ${env.FULL_IMAGE}
                        if [ -d ${env.PRJ_DIR} ]; then
                          cd ${env.PRJ_DIR}
                          sed -i "s|image: anestesia01.*|image: ${env.FULL_IMAGE}|" compose.yaml
                          docker compose up -d --force-recreate
                        else
                          git clone ${env.GIT_URL} ${env.PRJ_DIR}
                          sed -i "s|image: anestesia01.*|image: ${env.FULL_IMAGE}|" compose.yaml
                          docker compose up -d --force-recreate
                        fi
                    """
                }
            }
        }
    }
}