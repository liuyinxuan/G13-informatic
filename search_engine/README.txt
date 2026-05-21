Phuong Luong @pluong3
NetID: pluong3
Student ID:62887840

Yinxuan Liu @yinxual1
NetID: yinxual1
Student ID:70861360

Robin Stoebe @cstoebe
NetID: cstoebe
Student ID:63085315

Navid Sharmsar @nsharmsa
NetID: nsharmsa
Student ID:66353809

How to run the search engine

1. Make sure all the utils/modules listed in requirement.txt are installed.
if not, please using the following command:
"pip install -r <PATH-to-requirements.txt>

2. make sure you got "inverted_index.json" and "doc_id.json" ready in the "IR24W-A3-G15" folder. If not, please follow the guidiance below to generate it:
    (1)Place the developer.zip file into the "IR24W-A3-G15" folder. (or manually change line 169 in indexer.py to <PATH-to-developer.zip>)
    (2)On your terminal, Run the following scripts: "python indexer.py"
    (3)Try "Python3 indexer.py" if step2 does not working
    (4)In roughly 20-30 minute, "inverted_index.json" and "doc_id.json" would be generated and placed into "IR24W-A3-G15" folder
   
3. Running the GUI search engine using the following command: "python webGUI.py", a link will soon provided into the bash_prompt/terminal, click the link and you will be able to use the search engine. Press "ctrl-c" on terminal to exit the program

Optional step for text-based UI search engine:
The text based UI got more information and data, which is useful for debugging.
To access the test based UI, simply type "python search.py" and a text-based search engine would appear. use either 'ctrl-c" or type q to ends the program.

