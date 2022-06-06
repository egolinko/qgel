pipeline {
  agent { docker { image 'python:3.9.7' } }
  stages {
    stage('test') {
      steps {
        sh 'python test.py'
      }
    }
  }
}
