
AOA Diagram and Analysis Software for Windows
=============================================

Overview
--------
This project introduces the first Windows software for creating Activity on Arrow (AOA) network diagrams, 
a tool essential for project scheduling and critical path analysis. Developed using Python and the PyQt 
framework, this software serves as a zero-cost alternative to premium tools like Microsoft Project, which 
generates Activity on Node (AON) diagrams and requires a subscription.

The software is tailored for civil engineering applications and enables efficient project planning, scheduling, 
and analysis, offering significant cost savings and usability advantages.

Features
--------
- AOA Network Diagram Generation:
  - Create clear and accurate AOA diagrams.
  - User-friendly drag-and-drop interface for defining activities and dependencies.

- Critical Path Analysis:
  - Automatically calculates the critical path of a project.
  - Provides detailed project scheduling metrics, including earliest start, latest start, earliest finish, 
    and latest finish times.

- Efficient Algorithms:
  - Optimized for fast processing of large networks.
  - Utilizes advanced data structures for efficient analysis.

- Cost-Effective:
  - Zero-cost software developed as a free alternative to Microsoft Project, saving users a subscription cost of INR 830/month.

Problem Solved
--------------
Traditional tools for project planning, like Microsoft Project, rely on Activity on Node (AON) diagrams and 
often require expensive licenses. This software fills the gap by:
1. Offering a free and open-source alternative for AOA diagrams.
2. Providing project scheduling tools tailored to civil engineering and construction applications.
3. Eliminating the need for manual calculations of the critical path and project metrics.

Tools and Technologies
-----------------------
- Programming Language: Python
- Framework: PyQt for GUI development
- Libraries: 
  - matplotlib for diagram visualization.
  - Custom algorithms for project scheduling and critical path analysis.

How to Use
----------
1. Download the Software:
   - Clone the repository:
     ```
     git clone <repository-url>
     cd AOA-Diagram-Software
     ```

2. Install Dependencies:
   - Install required Python libraries:
     ```
     pip install -r requirements.txt
     ```

3. Run the Software:
   - Start the application:
     ```
     python main.py
     ```

4. Features:
   - Add activities with start and end points, durations, and dependencies.
   - View and export AOA network diagrams.
   - Analyze project schedules, including:
     - Total project duration.
     - Critical path and slack times.
    
    
Or if you want to runthe software without changing anything:
To use the AOA Network Diagram project, you have two options:

Download the executable file from the following link: [Hosted Exe File](https://github.com/makhanjaiswalonair/AOA-Network-making-Windows-Software/blob/main/AOA_Project_Manager.exe).
This option is recommended if you just want to run the project without modifying the source code.
OR

Download the source code by cloning the repository or downloading as zip from here and then running the main.py file. Make sure you have Python installed, preferably version 3.10. This option is recommended if you want to customize or contribute to the project.
Please note that you need to have Graphviz installed, the environment variables properly set, and the Graphviz bin folder path added to the PATH environment variable for the project to work correctly.

For more instructions of app usage, please refer to the App Manual.

Architecture and Algorithms
---------------------------
- Architecture:
  - Modular design for UI, diagram generation, and analysis.
  - Designed for scalability and maintainability.

- Key Algorithms:
  - Critical Path Method (CPM):
    - Efficiently calculates the critical path.
    - Identifies slack for non-critical activities.
  - Data Structures:
    - Directed graphs to represent project dependencies.
    - Optimized adjacency list for analyzing large networks.

Team and Contributions
----------------------
- Team Members:
  - Led a team of 4 developers to design, develop, and test the software.

- Key Contributions:
  - Designed the software architecture and developed core algorithms.
  - Implemented GUI using the PyQt framework.
  - Optimized data structures for efficient project analysis.

Achievements
------------
- Recognition:
  - Received a Letter of Recommendation (LOR) from Prof. K.N. Jha for contributions to this project.

- Impact:
  - Created a cost-effective tool for civil engineers and project managers.
  - Enhanced accessibility to project scheduling software without a subscription fee.

Future Enhancements
-------------------
1. Add support for Activity on Node (AON) diagram generation.
2. Enhance visualization options, such as color-coded critical paths.
3. Include export functionality for diagrams in popular formats like PDF or PNG.
4. Optimize algorithms for handling even larger projects.



Contributors
------------
- Makhan Jaiswal  
  Lead Developer and Architect
- Shashank Kosta
  UI Designer and Developer
- Shreyansh Jain
  UI Designing and Add on
- Aditya Kumar
  Helper

