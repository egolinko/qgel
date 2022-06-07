pipeline {
  agent {
    docker{
      image 'python:3.7.2'
      }
      }
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', credentialsId: 'ffe7b2a8-2432-4412-9fbf-ed83a415dcf3',url: 'git@github.com:egolinko/qgel.git'
      }
      }
    stage('test') {
      steps {
        sh 'python test.py'
      }
    }
  }
}
