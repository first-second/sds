pipeline {
  agent any
  
    stage('Execute Commands') {
      steps {
        // Execute commands inside the Docker container
        script {
          // Execute commands inside the Docker container
          def returnStatus = sh returnStdout: true, script: 'docker exec -e EC2_INSTANCE_IP=127.0.0.1 b622 /bin/bash -c "source /opt/myvenv/bin/activate && python /opt/myproject/manage.py runserver 0.0.0.0:8000 && echo \$?"'
          echo "Return Status: ${returnStatus}"

          // Stop the build if the Django application ran successfully
          if (returnStatus.trim() == '0') {
            error('Django application ran successfully. Stopping the build.')
            return
          }
        }
      }
    }
  }
}
