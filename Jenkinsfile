// rpm builder for check-solr Icinga plugin
properties([
	parameters([
		string(
			defaultValue: "gdchdpmn04drlx.geisinger.edu",
			description: "Hostname to build on",
			name: 'hostname'
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

	echo "Connecting to Artifactory"
	//Define artifactory server
	//Definition by node-id does not seem to be working? 403, Jenkins system config is fine
    env.REPO_NAME = params.repo
	env.ARTIFACTORY_SERVER = 'https://ghsudarepo1rlxv.geisinger.edu/artifactory'
	env.RPM_ROOT = env.WORKSPACE + "/rpm-repo/check-solr/RPMS"
    env.upload_spec = ""

	// Define upload spec for RPM uploads
	// Does not currently notify you if 0 artifacts were found (BUG?)"
	// "props": "type=rpm"
	echo "Defining upload spec"
	upload_spec = """{
	  "files": [
		{
		  "pattern": "${RPM_ROOT}/*.rpm",
		  "target": "$REPO_NAME/check-solr/"
		}
	 ]
	}"""
    echo upload_spec

	currentBuild.result = "SUCCESS"
	env.CREDENTIALS_STORE = 'udahadoopops'
	try {
		stage('Checkout') {
			dir('rpm-repo') {
				git url: 'https://github.com/GeisingerHealthSystem/rpm', credentialsId: env.CREDENTIALS_STORE
			}
		}
		stage('Build rpm') {
			dir('rpm-repo/check-solr') {
				sh script: """
					rm -rf BUILD RPMS SOURCES SPECS SRPMS && mkdir BUILD RPMS SOURCES SPECS SRPMS
					spectool -g -R check-solr.spec -C SOURCES
					rpmbuild --define "_topdir `pwd`" -bb check-solr.spec
				"""
			}
		}
		stage('Upload RPM to Artifactory') {
			echo "Verifying existance of file"
			env.RPMPKG = sh(returnStdout: true, script: "find ${RPM_ROOT} -name check-solr*.rpm").trim()
			if(fileExists(env.RPMPKG)) {
				echo "Verified RPM: " + env.RPMPKG
			} else {
				error("RPM File not found! Aborting")
			}
            if (params.deploy == 'deploy') {
                echo "Uploading RPM package to Artifactory"
                server = Artifactory.newServer url: env.ARTIFACTORY_SERVER, credentialsId: 'cdis_sys_prod'
                buildInfo = server.upload spec: upload_spec

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