# Virtual Environments

Ensure you have pulled the git repo before starting this to ensure you have requirements.txt

To create the virtual environment (in VS code):
<ol>
<li>Click on the central search box at the top of VS code (ctrl + shift + P)</li>
<li>Start to type "Python: Create Environment" and click it</li>
<li>Click on the top option, "Venv"</li>
<li>Select the python interpreter (preferable python 3.13.2)</li>
<li>Select Use requirements.txt, which should automattically install the libraries we will be using (Notably Django)</li>
</ol>

<br><br>
To enter the virtual environment:
<ol>
<li>Run the command, "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"</li>
<li>Run the command, ".venv/Scripts/Activate.ps1", this should work from the local path, but you may need to specify the global path if this fails</li>
</ol>

<br><br>
To check this is working, run Django/test.py and it should print "5.2.5"

--Written with love, Reuben & Yash