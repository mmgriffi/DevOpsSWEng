# DevOps Software Engineering Assignment

## Introduction
This application is a basic Django website with a basic table and functions to view a members table. I've used Django/Python framework as it has extensive libraries and testing facilities.
(_and, I'm trying to learn Python_). I've used PyCharm as the IDE which allows me run/basic test applications in a virtual python enviroment locally before transfer to a docker desktop on the laptop, or to a container environment. 

## Build/Deployment Environment 
I have a homelab server that I've used for development and testing in the past. 
This is configred as a Promox Virtual host and runs the virtual machines used in my environment. 
The relevant items for this assigment are : 

| Item                      |Description| Notes                                                                                                                                                                   |
|---------------------------|----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Container Orchestration   |Kubernetes(rke2)| I have confgured a 2 node rke2 cluster. This is managed from command line and using the "Headlamp" GUI utility.                                                         |
| GitHub Runner             |Ubuntu 22.04 node VM| This is configured as a "self hosted" github runner with docker, python testing tools (playwright, pytest, chromium) and keys required to connect to github, sonarqube. | 
| Code Analysis (SonarQube) |LXC Ubuntu 22.04 container| This LXC container has docker and the SonarCube images (website/db) installed , running on http://192.168.1.92 locally.                                                 | 
|Monitoring||                                                                                                                                                                         |

## CI/CD Tool Integration ###

**GitHub Actions**
I've used GitHub Actions as I had expierence of this from previous work. 


**Clickup**

ClickUp is linked with my repos ![image](images/ClickUpApps-GitHub.jpg)
From that, ClickUp can create Issues/Pull Requests/Create Branches on the repo.  From GitHub you can close the issue and the status is reflected 
on the ClickUp task if you use some keywords in the comment such as Fixes CU-1amhxucrzgq
(CU-1amhxucrzgq is the task-ID, not it's name).
If you're commiting or doing a pull merge this keywork will move the task status.
CU-1amhxucrzgq[<state name>]  (to do, in progress, complete )  are the only states I've used. 

**Slack**

GitHub integrations allow communictation with Slack. In this case I selected this repo only.

**Testing tools**
 - **Unit Test:** I'm using **pytest* to execute unit/internal tests defined in DevOpsSWEng\my_tennis_club\members\tests.py. These validate the python functions that add a user, and the views to display member listings.
 - **Build/Integration test:** For validation of the build, I start the container on the runner system and use pytest-playwright to execute selenium tests (http://127.0.0.1:8000) . These verify the container has started correctly and functions like displaying a list of users work.
 - **Smoke Tests:** Once deployed on the Kubernetes cluster I execute smoke tests using the actual URL (http://devops-dev.cluen.com or http://devops-prod.cluen.com). This is the final validation that the Kubernetes pods/services/ingress is working.
 - 
**Application Repository**
Once build and tests complete the application is pushed to the GitHub Container Registry (GHCR). 


**New version Deployment**
 - When you are ready to push a new version and include a tag do the following :
```` 
     git tag v1.1 
     git push --tags
     
     _verify_
     git describe --tags
````
- Commit and push changes to the branch.
- Run GitHub Actions "CI_PipeLine" CI_workflow.yaml. This 

**Application Revision History**
After I got the initial website/ app running .  I have used tagged some of the commits (not every workflow correction was included) to mark the main changes 

|Version|Notes|
|----|----|
|v1.0|1st version, website and basic deployment workflows working|
| v1.1| Added version + build info to footer page.  added SonarCube Scans|
