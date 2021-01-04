// rpm builder for check-solr Icinga plugin
properties([
    parameters([
        string(
            defaultValue: "gdchdpmn04drlx.geisinger.edu",
            description: "Hostname to build on",
            name: 'hostname'
        ),
        string(
                defaultValue: "master",
                description: 'Git target (such as a branch or tag)',
                name: 'git_target'
        ),
        choice(
            choices: ['branch','tag'].join("\n"),
            description: 'What the git target type is',
            name: 'git_target_type'
        ),
        string(
            defaultValue: "rpm-rhel7-dev",
            description: 'Artifactory repository to push to',
            name: 'repo'
        ),  
        choice(
            // At the moment choices is bugged, as it expects the choice
            // parameters as a newline delimited string instead of an array
            choices: [
                'test',
                'deploy',
                ].join("\n"),
            description: 'test or deploy utility',
            name: 'deploy'
        ),
    ])
])

node(params.hostname) {

    // PKG details
    // Make sure you update the RPM spec file versin alongside the tarball version below
    env.PKG_NAME = 'check-solr'
    env.PKG_VERSION = '1.0.0'
    env.RPM_ROOT = env.WORKSPACE + "/plugin-repo/RPMS"
    env.SRPM_ROOT = env.WORKSPACE + "/plugin-repo/SRPMS"

    echo "Connecting to Artifactory"
    //Define artifactory server
    //Definition by node-id does not seem to be working? 403, Jenkins system config is fine
    env.REPO_NAME = params.repo
    env.ARTIFACTORY_SERVER = 'https://ghsudarepo1rlxv.geisinger.edu/artifactory'
    env.rpm_upload_spec = ""
    env.srpm_upload_spec = ""

    if (params.git_target_type == 'branch') {
        env.GIT_TARGET = '*/' + params.git_target
    }
    else if (params.git_target_type == 'tag') {
        env.GIT_TARGET = 'refs/tags/' + params.git_target
    }
   
    // Define upload spec for RPM uploads
    // Does not currently notify you if 0 artifacts were found (BUG?)"
    // "props": "type=rpm"
    echo "Defining RPM upload spec"
    rpm_upload_spec = """{
      "files": [
        {
          "pattern": "${RPM_ROOT}/*/*.rpm",
          "target": "${REPO_NAME}/${PKG_NAME}/"
        }
     ]
    }"""
    echo rpm_upload_spec

    echo "Defining SRPM upload spec"
    srpm_upload_spec = """{
      "files": [
        {
          "pattern": "${SRPM_ROOT}/*.rpm",
          "target": "${REPO_NAME}/${PKG_NAME}/"
        } ]
    }"""
    echo srpm_upload_spec

    currentBuild.result = "SUCCESS"
    env.CREDENTIALS_STORE = 'udahadoopops'

    // Always start clean
    cleanWs()

    try {
        stage('Checkout') {
            dir('plugin-repo') {
                checkout([$class: 'GitSCM',
                    branches: [[name: env.GIT_TARGET]],
                    doGenerateSubmoduleConfigurations: false,
                    userRemoteConfigs: [[credentialsId: 'udahadoopops', 
                                        url: 'https://github.com/GeisingerHealthSystem/check-solr']]])
            }
        }
        stage('Prepare Source'){
                sh script: """
                    mkdir plugin-repo/SOURCES
                    cp -r plugin-repo  ${PKG_NAME}-${PKG_VERSION}
                    tar -czvf plugin-repo/SOURCES/${PKG_NAME}-${PKG_VERSION}.tar.gz ${PKG_NAME}-${PKG_VERSION}
                    rm -rf ${PKG_NAME}-${PKG_VERSION}
                """
        }
        stage('Build rpm') {
            dir('plugin-repo') {
                sh script: """
                    spectool -g -R check-solr.spec
                    rpmbuild --define "_topdir `pwd`" -ba check-solr.spec
                    find . -type f -name "*.rpm" -print -exec rpm -qlpv {} \\;
                """
            }
        }
        stage('Upload RPM(s) to Artifactory') {
            echo "Verifying existance of files"

            env.RPMPKG = sh(returnStdout: true, script: "find ${RPM_ROOT} -name *.rpm").trim()
            if(fileExists(env.RPMPKG)) {
                echo "Verified RPM: " + env.RPMPKG
            } else {
                error("RPM File not found! Aborting")
            }

            env.SRPMPKG = sh(returnStdout: true, script: "find ${SRPM_ROOT} -name *.rpm").trim()
            if(fileExists(env.RPMPKG)) {
                echo "Verified SRPM: " + env.SRPMPKG
            } else {
                error("SRPM File not found! Aborting")
            }

            if (params.deploy == 'deploy') {
                echo "Uploading RPM package to Artifactory"
                server = Artifactory.newServer url: env.ARTIFACTORY_SERVER, credentialsId: 'cdis_sys_prod'
                buildInfo = server.upload spec: rpm_upload_spec
                buildInfo = server.upload spec: srpm_upload_spec

                // Publish build info (doesn't work?)
                //artifactory_server.publishBuildInfo buildinfo
            }
        }
        stage('Cleanup') {
            //cleanWs()
        }
    }
    catch (err) {
        currentBuild.result = "FAILURE"
        throw err
    }
}
