pipeline {
    agent any

    environment {     
        DOCKERHUB_CREDENTIALS= credentials('docker')
    }

    stages {
        stage('Build scanjson') {
            steps {
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.scan -t solarix/scanjson ."
            }
        }
        stage('Push to hub.docker') {
            steps {
                echo "Trying to log to dockerhub from $NODE_NAME"
               	sh 'echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
	            echo 'Login Completed'
                sh 'sudo docker push solarix/scanjson:latest'
                echo 'Push Image scanjson Completed' 
            }
        }
        stage('Build buildjson') {
            steps {
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.build -t solarix/buildjson ."
            }
        }
        stage('Push to hub.docker') {
            steps {
                echo "Trying to log to dockerhub from $NODE_NAME"
               	sh 'echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
	            echo 'Login Completed'
                sh 'sudo docker push solarix/buildjson:latest'
                echo 'Push Image buildjson Completed' 
            }
        }
    }
}
