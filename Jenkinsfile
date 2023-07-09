pipeline {
  agent any

  stages {
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
        script {
          // Execute commands inside the Docker container
          sh 'docker exec -e EC2_INSTANCE_IP=127.0.0.1 b622 /bin/bash -c "source /opt/myvenv/bin/activate && python /opt/myproject/manage.py runserver 0.0.0.0:8000"'
          
          // Check the return status of the Django application
          def returnStatus = sh returnStatus: true, script: 'echo \$?'
          print returnStatus

          // Stop the build if the Django application ran successfully
          if (returnStatus == 0) {
            error('Django application ran successfully. Stopping the build.')
            return
          }
        }
      }
    }
  }
}
