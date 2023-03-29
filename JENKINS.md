# Bookmark cleansing R4.0

## Building with Jenkins pipelines

This declarative pipeline builds __scanjson__ and __buildjson__ images using Jenkins and pushes images to dockerhub.

The agent is hosted in a VBox machine.

## Usage

Create a VBox machine (CentOS) for a Jenkins worker, in which:

* Set an IP address
* Create jenkins user
* Associate jenkins user to former key
* Install JDK 11
* Install git
* Install docker daemon

Change Jenkins port in host by `sudo systemctl edit jenkins`:

    [Service]
    Environment="JENKINS_PORT=8088"

Create a rsa key in host:

`ssh-keygen -f ~/.ssh/jenkins_agent_key`

Then copy it to the worker using `ssh-copy-id`

Install following packages in VBOX

First time VM is started it has to be run:

`sudo setfacl --modify user:jenkins:rw /var/run/docker.sock`

`sudo chmod o+rw /var/run/docker.sock`

## Operation

Jenkinsfile is kept in repo and is then run when executing a pipeline associated with that repo.

Add git & dockerhub credentials (used in Jenkinsfile)

* Manage Jenkins￼> Credentials

## Result

After being generated images are pushed to dockerhub.
