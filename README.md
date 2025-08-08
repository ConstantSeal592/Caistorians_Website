# Caistorians_Website
The website project for the Caistorian's Association

For people new to GIT, GIT is type of software used to allow collaboration between people on a single project by keeping track of alterations and versions.
<br><br>
Terms:
<ul>
<li>Repo/Repository - A fancy folder that uses GIT to handle versioning and backups (A versions exists on both your device and GitHub)</li>
<li>Remote Repository - The repository that exists exclusivly on GitHub</li>
<li>Commit - Take the changes/edits you have made and save them on your computer</li>
<li>Branch - Create a copy of the current state of the project at a point</li>
<br>
<li>Fetch - Grab the current state of the project from elsewhere, in this case GitHub and store it on your device</li>
<li>Merge - Combine the commited state of the project on your computer (current) with the state of the project elsewhere, in this case GitHub (incoming)</li>
<li>Pull - The combination of Fetching the project from GitHub and merging it with what is on your local device.</li>
<br>
<li>Push - Take the commits on your computer and put them onto GitHub</li>
</ul>

<br><br>
Setup:
<ol>
<li>Create a GitHub account</li>
<li>Download the GitHub desktop application, and sign into it (You could technically do all of this through the terminal, but it is apain to set up and prone to user error)</li>
<li>Copy the URL to your account's homepage and send it to the group chat, unfortunatly you cannot continue with this handy-dandytutorial until someone has invited you as a collaborator to the repository (We at Yash&Friends Ltd aspire to do this within 5 workingdays)</li>
<li>To setup the repository in GitHub desktop do: File > Clone Repository (ctrl + shift + O)</li>
<li>Select this Repository ConstantSeal592/Caistorians_Website, or use the following URL "https://github.com/ConstantSeal592Caistorians_Website.git"</li>
<li>If you wish, you can change the directory on your device where the repository will be created, by default it is Documents (You canalways create a shortcut on your desktop if you desire)</li>
<li>Click Clone (blue button)</li>
<li>After it has loaded you should see, under the File button in the top left "Current Repository: Caistorians_Website"</li>
<img width="307" height="57" alt="image" src="https://github.com/user-attachments/assets/f32ef406-7f62-49a9-9b18-f47c6569d6dc" /><br>
<li>You can verify that this has worked by doing: Repository > Show in Explorer (ctrl + shift + F). The folder that opens should have(at the minimum) README.md (this file, so you can continue reading offline :D) (If you have "Show hidden files, folders and drives"enabled in file explorer, you should see the .git directory at the top of this folder, that designates that this folder behaves as a GITrepository, **DO NOT MUCK AROUND WITH THIS DIRECTORY**)</li>
</ol>

<br><br>
You have now successfully set up GitHub/GitHub desktop & the repository on your computer. VS code has alot of tools aimed at making GIT within VS code seemless. They are inbuilt, no extensions required. I dont believe that they activate if you have exclusively GitHub desktop installed. If you want, you may need to install GIT (see the following URL "https://git-scm.com/") and set it up (see the following URL "https://www.w3schools.com/git/default.asp")

<br><br>
Working (This is up for debate, feel free to make suggestions):
<ol>
<li>Create a branch of the project (and name accordingly). This branch is a copy of the project at the time you create it. Do this by clicking on the "Current Branch: main" drop down > New branch, or Branch > New branch (ctrl + shift + N)</li>
<img width="456" height="325" alt="image" src="https://github.com/user-attachments/assets/19981df2-7540-4aff-9281-195c7cd671e5" />
<li>Make your changes/edits to this branch, this can be whatever, just ensure whatever you change/create/delete remains in the repository</li>
<li>As you go along, be sure to commit your changes (preferably with appropriate summaries & descriptions), but especially when you are finished with this branch, commit everything and push to GitHub</li>
<li>You now need to merge your branch, back into the main branch.</li>
</ol>
