pipeline {
  agent any

  stages {
    stage('Start Container') {
      steps {
        // Start the Docker container
        sh 'docker start b622'
      }
    }
    stage('Check SCM Configuration') {
      steps {
        script {
          // Checkout the repository to access SCM configuration
          checkout scm

          // Access SCM configuration parameters
          def scmConfig = scm
          def scmType = scmConfig.getClass().getSimpleName()
          def repositoryUrl = scmConfig.getUserRemoteConfigs()[0].getUrl()
          def branchName = scmConfig.getBranches()[0].getName()

          // Print SCM configuration details
          echo "SCM Type: ${scmType}"
          echo "Repository URL: ${repositoryUrl}"
          echo "Branch Name: ${branchName}"
        }
      }
    }

    stage('Execute Commands') {
      steps {
        // Execute commands inside the Docker container
        sh 'docker exec -e EC2_INSTANCE_IP=127.0.0.1 b622 /bin/bash -c "source /opt/myvenv/bin/activate && python /opt/myproject/manage.py runserver 0.0.0.0:8000"'
      }
    }
    
  }
}

