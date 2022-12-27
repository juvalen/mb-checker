# Jenkins pipelines

This pipeline builds __scanjson__ and __buildjson__ images using Jenkins.

The agent is hosted in a VBox machine.

## Usage

Create a VBox machine (CentOS), in which:

* Set an IP address
* Create jenkins user
* Create a rsa key in host, and copy key to worker
* Associate jenkins user to former key
* Install JDK 11
* Install git
* Install docker daemon and enable it

ach time VM is started:

`sudo setfacl --modify user:jenkins:rw /var/run/docker.sock`
`sudo chmod o+rw /var/run/docker.sock`

:exclamation: To be included in the VM boot process

## Operation

Jenkinsfile is kept in repo and is then run when executing a pipeline assiciated with that repo.

## Result

Generated images remain in agent docker. They should be pushed to the apropriate registry in a following stage.
