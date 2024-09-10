pipeline {
  agent {
      label 'kaniko'
  }

  environment {
    ECR_REPO = '108174090253.dkr.ecr.us-east-1.amazonaws.com/production-support-course'
  }

  stages {
    
    stage('Build Trading Front End') {
      steps {
        container(name: 'kaniko') {
          sh '''
            echo \'{ "credsStore": "ecr-login" }\' > /kaniko/.docker/config.json
            /kaniko/executor -f `pwd`/Dockerfiles/Dockerfile_nginx -c `pwd` --insecure --skip-tls-verify --cache=false --cleanup --destination=${ECR_REPO}:${JOB_NAME}fe-dev-${BUILD_NUMBER}
          '''
        }
      }
    }
    
    stage('Build and Publish DB') {
      steps {
        container(name: 'kaniko') {
          sh '''
            echo \'{ "credsStore": "ecr-login" }\' > /kaniko/.docker/config.json
            /kaniko/executor -f `pwd`/Dockerfiles/Dockerfile_mysql -c `pwd` --insecure --skip-tls-verify --cache=false --cleanup --destination=${ECR_REPO}:${JOB_NAME}replica-dev-${BUILD_NUMBER}
          '''
        }
      }
    }

    stage('Build and Publish DB-replica') {
      steps {
        container(name: 'kaniko') {
          sh '''
            echo \'{ "credsStore": "ecr-login" }\' > /kaniko/.docker/config.json
            /kaniko/executor -f `pwd`/Dockerfiles/Dockerfile_replica -c `pwd` --insecure --skip-tls-verify --cache=false --cleanup --destination=${ECR_REPO}:${JOB_NAME}db-dev-${BUILD_NUMBER}
          '''
        }
      }
    }
    
    
    stage('Build and Publish API') {
      steps {
        container(name: 'kaniko') {
          sh '''
            echo \'{ "credsStore": "ecr-login" }\' > /kaniko/.docker/config.json
            /kaniko/executor -f `pwd`/Dockerfiles/Dockerfile_fastapi -c `pwd` --insecure --skip-tls-verify --cache=false --cleanup --destination=${ECR_REPO}:${JOB_NAME}api-dev-${BUILD_NUMBER}
          '''
        }
      }
    }
  }

  triggers {
    pollSCM('*/10 * * * 1-5')
  }
}
