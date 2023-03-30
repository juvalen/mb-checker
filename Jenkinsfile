pipeline {
    agent any

    environment {     
        DOCKERHUB_CREDENTIALS= credentials('746b3360-da21-49eb-90c8-d5751fe24c45')
    }

    stages {
        stage('Build scanjson') {
            steps {
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.scan -t solarix/scanjson ."
            }
        }
        stage('Push scanjson to hub.docker') {
            steps {
                echo "Trying to log to dockerhub from $NODE_NAME"
               	sh "echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
	            echo 'Login Completed'
                sh 'sudo docker push solarix/scanjson:latest'
                echo 'Pushed Image scanjson' 
            }
        }
        stage('Build buildjson') {
            steps {
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.build -t solarix/buildjson ."
            }
        }
        stage('Push buildjson to hub.docker') {
            steps {
                echo "Trying to log to dockerhub from $NODE_NAME"
               	sh "echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
	            echo 'Login Completed'
                sh 'sudo docker push solarix/buildjson:latest'
                echo 'Pushed Image buildjson' 
            }
        }
    }
}
