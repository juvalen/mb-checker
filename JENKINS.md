# Jenkins pipelines

This pipeline builds __scanjson__ and __buildjson__ images using Jenkins.

The agent is hosted in a VBox machine.

## Usage

Create a VBox machine (CentOS), in which:

* Set an IP address
* Create jenkins user
* Associate jenkins user to former key
* Install JDK 11
* Install git
* Install docker daemon (change socket permissions there with `chmod o+rw /var/run/docker.sock`)

Create a rsa key in host:

`ssh-keygen -f ~/.ssh/jenkins_agent_key`

Then copy it to the worker using `ssh-copy-id`

Install following packages in VBOX

## Operation

Jenkinsfile is kept in repo and is then run when executing a pipeline assiciated with that repo.

## Result

Generated images remain in agent docker. They should be pushed to the apropriate registry in a following stage.
