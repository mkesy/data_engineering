pipeline {
    
     agent any

     environment {

        DATA_ENGINEERING_DIR = '/var/jenkins_home/workspace/data_engineering'
        DATA_SCIENCE_PATH    = '/var/jenkins_home/workspace/data_science'
        DATA_ENGINEERING_GIT = 'https://github.com/mkesy/data_engineering.git'
        DATA_SCIENCE_GIT     = 'https://github.com/mkesy/data_science.git'
     }

     stages {

            stage('Kill running containers') {

                steps {
                    sh 'docker ps --filter "label=hackathon" -q | xargs --no-run-if-empty docker container stop'
                    sh 'docker container ls -a --filter "label=hackathon" -q | xargs -r docker container rm'
                    }
                }

            stage('Checkout repos') {

                steps {
                    script {
                        dataScienceCommitVars = checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${env.DATA_SCIENCE_PATH}"]], submoduleCfg: [], userRemoteConfigs: [[url: "${env.DATA_SCIENCE_GIT}"]]])
                    }
                    script {
                        dataEngineeringCommitVars = checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${env.DATA_ENGINEERING_DIR}"]], submoduleCfg: [], userRemoteConfigs: [[url: "${env.DATA_ENGINEERING_GIT}"]]])
                    }
                }
            }

            stage('Generate code') {

                agent {
                    docker { image 'python:2' }
                }

                steps {
                    dir("${env.DATA_ENGINEERING_DIR}") {
                        sh "cp ${env.DATA_SCIENCE_PATH}/* ."
                        sh "pip install --no-cache-dir -r ./requirements.txt"
                        sh "python ./code_generation.py ./data_science.ipynb False"
                    }
                }
            }

            stage('Build image') {

                 steps {

                    script {

                        dir("${env.DATA_ENGINEERING_DIR}") {
                            docker.withRegistry('https://localhost:5000') {
                                def engineeringImage = docker.build("hackathon/data_engineering_vectorization:${dataScienceCommitVars.GIT_COMMIT}")
                                engineeringImage.push()
                                engineeringImage.push('latest')
                            }
                            sh "nohup docker run -d --network=hackathoninfra_vn1  --name=decontainer -p 4000:80 hackathon/data_engineering_vectorization &"
                        }
                    }
                 }

            }

            stage('Test build correctness') {

                steps {

                    dir("${env.DATA_ENGINEERING_DIR}") {
                        sh "./build_test.sh"
                    }
                }

            }
     }

}

pipeline {
    
     agent any

     environment {

        DATA_ENGINEERING_DIR = '/var/jenkins_home/workspace/data_engineering'
        DATA_SCIENCE_PATH    = '/var/jenkins_home/workspace/data_science'
        DATA_ENGINEERING_GIT = 'https://github.com/mkesy/data_engineering.git'
        DATA_SCIENCE_GIT     = 'https://github.com/mkesy/data_science.git'
     }

     stages {

            stage('Kill running containers') {

                steps {
                    sh 'docker ps --filter "label=hackathon" -q | xargs --no-run-if-empty docker container stop'
                    sh 'docker container ls -a --filter "label=hackathon" -q | xargs -r docker container rm'
                    }
                }

            stage('Checkout repos') {

                steps {
                    script {
                        dataScienceCommitVars = checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${env.DATA_SCIENCE_PATH}"]], submoduleCfg: [], userRemoteConfigs: [[url: "${env.DATA_SCIENCE_GIT}"]]])
                    }
                    script {
                        dataEngineeringCommitVars = checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${env.DATA_ENGINEERING_DIR}"]], submoduleCfg: [], userRemoteConfigs: [[url: "${env.DATA_ENGINEERING_GIT}"]]])
                    }
                }
            }

            stage('Generate code') {

                agent {
                    docker { image 'python:2' }
                }

                steps {
                    dir("${env.DATA_ENGINEERING_DIR}") {
                        sh "cp ${env.DATA_SCIENCE_PATH}/* ."
                        sh "pip install --no-cache-dir -r ./requirements.txt"
                        sh "python ./code_generation.py ./data_science.ipynb True"
                    }
                }
            }

            stage('Build image') {

                 steps {

                    script {

                        dir("${env.DATA_ENGINEERING_DIR}") {
                            docker.withRegistry('https://localhost:5000') {
                                def engineeringImage = docker.build("hackathon/data_engineering_prediction:${dataScienceCommitVars.GIT_COMMIT}")
                                engineeringImage.push()
                                engineeringImage.push('latest')
                            }
                            sh "nohup docker run -d --network=hackathoninfra_vn1  --name=decontainer -p 4000:80 hackathon/data_engineering_prediction &"
                        }
                    }
                 }

            }

            stage('Test build correctness') {

                steps {

                    dir("${env.DATA_ENGINEERING_DIR}") {
                        sh "./build_test.sh"
                    }
                }

            }
     }

}

