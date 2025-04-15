pipeline{
    agentany

    stages{
        stage('Cloning Github repo to Jenkin')
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/simR122/mlops1_hotel.git']])
                }
            }
    }
}