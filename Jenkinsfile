pipeline {
    agent any

    environment{
        venv_DIR = 'venv'
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/simR122/mlops1_hotel.git']])
                }
            }
        }

        stage('Setting up our virtual env and installing dependencies') {
            steps {
                script {
                    echo 'Setting up our virtual env and installing dependencies.........'
                    sh '''
                    python -m venv $venv_DIR    
                    . ${VENV_DIR}/Scripts/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''          
                }
            }
        }
    }
}