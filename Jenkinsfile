pipeline {
    agent {
        node {
            label 'jenkinsagent'
        }
    }

    environment {     
        DOCKERHUB_CREDENTIALS= credentials('dockerhub')
    }

    stages {
        stage('Build scanjson') {
            steps {
                echo "Build ID $BUILD_ID"
                git branch: 'master',
                    url: 'https://github.com/juvalen/mb-checker.git'
                script {
                    sh "ls -ltr"
                    sh "pwd"
                    sh "docker build -f Dockerfile.scan -t solarix/scanjson ."
                }
            }
        }
        stage('Push scanjson to hub.docker') {
            steps { 
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push solarix/scanjson:latest'
            }
        }
        stage('Build buildjson') {
            steps {
                echo "Build ID $BUILD_ID"
                script {
                    sh "pwd"
                    sh 'docker build -f Dockerfile.build -t solarix/buildjson .'
                }
            }
        }
        stage('Push buildjson to hub.docker') {
            steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push solarix/buildjson:latest'
            }
        }
    }

    post {
        always {  
	        sh 'docker logout'
        }      
    }  
}
