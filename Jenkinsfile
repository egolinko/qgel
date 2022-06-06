pipeline {
  agent { docker { image 'python:3.9-bullseye' } }
  stage('Checkout') {
       git branch: 'main',
       credentialsId: '1889a3a3-80f8-4bb4-b656-f67f52fe11d8',
       url: 'git@github.com:egolinko/qgel.git'
   }
  stages {
    stage('test') {
      steps {
        sh 'python test.py'
      }
    }
  }
}
