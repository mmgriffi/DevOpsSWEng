# DevOps Software Engineering Assignment

## Introduction
This application is a basic Django website with a basic table and functions to add/update or delete enties to a members table.

## CI/CD Tool Integration ###

**Clickup**
ClickUp can create Issues on GitHub within a task.  From GitHub you can close the issue and the status is reflected 
on the ClickUp task if you use some keywords in the comment such as "Fixes CU-1amhxucrzgq"
(CU-1amhxucrzgq is the task-ID, not it's name).
If you're commiting or doing a pull merge this keywork will move the task status.
````
CU-1amhxucrzgq[<state name>]  
````
(to do, in progress or complete , all in lower cases  )  

**Slack**
GitHub integrations allow communictation with Slack. In this case I selected this repo only.

**CI / Testing tools**
 - I'm using **pytest* to execute unit/internal tests defined in DevOpsSWEng\my_tennis_club\members\tests.py. These validate the python functions that add a user, and the views to display member listings.
 - For validation of the website, I start the container on the runner system and use pytest-playwright to execute selenium test. These verify the container has started correctly and functions like displaying a list of users work.

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
- Run GitHub Actions "CI_PipeLine" CI_workflow.yaml

**Application Revision History**

|Version|Notes|
|----|----|
|v1.0|1st version, website and basic deployment workflows working|
| v1.1| Added version + build info to footer page.  added SonarCube Scans|
