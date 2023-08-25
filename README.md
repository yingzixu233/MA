# MA
Master_Thesis_2023_0825

Step 1: 
- Pull the project from **GitHub** repository to local repository
- Build a new environment through **Anaconda Navigator** and install all the relevant packages, including:
  - IfcOpenShell: **conda install -c ifcopenshell -c conda-forge ifcopenshell**
  - Neo4j Python Driver: **pip install neo4j**
- Open the project on **Pycharm Community**

Step 2:
- Download **docker desktop** https://www.docker.com/products/docker-desktop/ 
- Use "Control+Alt+S" to install Docker in Pycharm
- Edit configuration to add a new one under **docker-compose**, naming it as "docker-compose"
- Run the file "docker-compose.yml" to drive Neo4j,
  then you can ope the link under **Containers** on **docker desktop**
- Use username and password (find them from "main.py") to log in **Neo4j database** on the webpage

Step 3:
- Run "main.py" to build all the nodes and relationships 
- Check them in the neo4j database by using cypher language
- Compare it with **Revit** model