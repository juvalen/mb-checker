# Bookmark cleansing R4.0

## Building with Jenkins pipelines

This declarative pipeline builds __scanjson__ and __buildjson__ images using Jenkins and pushes images to dockerhub.

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

Each time VM is started:

`sudo setfacl --modify user:jenkins:rw /var/run/docker.sock`

`sudo chmod o+rw /var/run/docker.sock`

**warning** To be included in the VM boot process

## Operation

Jenkinsfile is kept in repo and is then run when executing a pipeline associated with that repo.

Add git & dockerhub ceredentials

## Result

After being generated images are pushed to dockerhub.
