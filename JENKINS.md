# Bookmark cleansing R4.1

## Building with Jenkins pipelines

This declarative pipeline builds __scanjson__ and __buildjson__ images using Jenkins and pushes images to dockerhub. Image building is described in [DOCKER](DOCKER.md).

The agent is hosted in a VBox machine called __jenkinsagent__.

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

First time VM is started you must connect with ssh and run:

`sudo setfacl --modify user:jenkins:rw /var/run/docker.sock`

`sudo chmod o+rw /var/run/docker.sock`

## Operation

Jenkinsfile is kept in repo and is then run when executing a pipeline associated with that repo.

Add dockerhub credentials (used in Jenkinsfile)

* Manage Jenkins&gt;Credentials

## Result

After generation, images are pushed to dockerhub. Configure it for your own repository.
