pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Building $BUILD_ID"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo "My name is $NODE_NAME"
            }
        }
    }
}
