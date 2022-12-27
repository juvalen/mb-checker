# Jenkins pipelines

This pipeline builds __scanjson__ and __buildjson__ images using Jenkins.

The agent is hosted in a VBox machine.

## Usage

Create a rsa key in host:

`ssh-keygen -f ~/.ssh/jenkins_agent_key`

Then copy to the worker using `ssh-copy-id`

Install following packages in VBOX

* Create user jenkins, asociated to former key
* Install JDK 11
* Install git
* Install docker daemon (change socket permissions there with `chmod o+rw /var/run/docker.sock`)

## Result

Generated images remain in agent docker. They should be pushed to the apropriate registry.
