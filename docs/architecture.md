// Jenkinsfile aggiornato
pipeline {
    agent any

    environment {
        CONTAINER_NAME = "sentiment-api-prod"
        IMAGE_NAME = "sentiment-api:latest"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo "Fase 0: Preparazione ambiente e creazione della rete Docker"
                script {
                    sh "docker network create monitor-network || true"
                }
            }
        }

        stage('Download Model') {
            steps {
                echo "Fase 0.1: Download del modello di sentiment analysis"
                script {
                    sh "mkdir -p src"
                    // Usa curl invece di wget
                    sh "curl -L -o src/sentiment_analysis_model.pkl 'https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentimentanalysismodel.pkl'"
                }
            }
        }

        stage('Build') {
    steps {
        echo "Fase 1: Costruzione dell'immagine Docker"
        script {
            // Pulisci la cache e builda senza cache
            sh "docker builder prune -f"
            sh "docker build --no-cache -t ${IMAGE_NAME} ."
        }
    }
}
        stage('Test') {
            steps {
                echo "Fase 2: Esecuzione dei test"
                script {
                    sh "docker stop test-api-container || true"
                    sh "docker rm test-api-container || true"
                    sh "docker run -d --name test-api-container --network=monitor-network ${IMAGE_NAME}"
                    
                    sh """
                        for i in \$(seq 1 10); do
                            docker exec test-api-container curl -s http://localhost:8000/ > /dev/null && break
                            sleep 2
                        done
                    """
                    
                    sh "docker run --rm --network=monitor-network -v \"${env.WORKSPACE}/tests:/app/tests\" python:3.9-slim-buster /bin/bash -c \"pip install requests && python -m unittest tests/test_api.py tests/test_model.py\""
                }
            }
            post {
                always {
                    echo "Pulizia del container di test"
                    sh "docker stop test-api-container || true"
                    sh "docker rm test-api-container || true"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Fase 3: Deploy del container in produzione"
                script {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8081:8000 --network=monitor-network --restart always ${IMAGE_NAME}"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completata con successo!"
        }
        failure {
            echo "❌ Pipeline fallita. Controllare i log per i dettagli."
        }
    }
} # funzionante 