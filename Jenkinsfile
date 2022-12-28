pipeline {
    agent any

    stages {
        stage('Build scanjson') {
            steps {
                echo "Build ID $BUILD_ID"
                app = docker.build("solarix/scanjson",  "Dockerfile.scan")
            }
        }
        stage('Build buildjson') {
            steps {
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.build -t solarix/buildjson ."
            }
        }
        stage('Deploy') {
            steps {
                echo "My name is $NODE_NAME"
            }
        }
    }
}
