pipeline {
    agent any

    stages {
        stage('Build scanjson') {
            steps {
                echo "Build ID $BUILD_ID"
                docker build -f Dockerfile.scan -t solarix/scanjson .
            }
        }
        stage('Build buildjson') {
            steps {
                echo "Build ID $BUILD_ID"
                docker build -f Dockerfile.build -t solarix/buildjson .
            }
        }
        stage('Deploy') {
            steps {
                echo "My name is $NODE_NAME"
            }
        }
    }
}
