pipeline {
    agent any

    stages {
        stage('Build scanjson') {
            steps {
<<<<<<< HEAD
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.scan -t solarix/scanjson ."
=======
                echo "Building $BUILD_ID"
>>>>>>> 7b1508e (Id)
            }
        }
        stage('Build buildjson') {
            steps {
<<<<<<< HEAD
                echo "Build ID $BUILD_ID"
                sh "docker build -f Dockerfile.build -t solarix/buildjson ."
=======
                echo 'Testing...'
>>>>>>> 7b1508e (Id)
            }
        }
        stage('Deploy') {
            steps {
                echo "My nodename is $NODE_NAME"
            }
        }
    }
}
