# **📦 \PBL1**

**MVP Status:** \[e.g., v1.0-Production]

**Group Members:** Adrien, Axelle B, Nour R, Gabrièle P


## **🎯 Project Overview**

**Provide a concise (2-3 sentence) description of what your application does and the specific problem it solves. Why did you build this?**

Our application allows to play Tic Tac Toe using 3 different modes: player vs player, player vs AI and AI vs AI. We also allow the player to chose the level of the AI he wants to compete against. We made this game to be able to play Tic Tac Toe alone or in pair and for all levels !

## **🚀 Quick Start (Architect Level: < 60s Setup)**

**Instructions on how to get this project running on a fresh machine.**

   Open git bash and type in : 
   
1. **Clone the repo:**\
   git clone \[your-repo-link]\
   cd \[project-folder]

3. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. **Install Dependencies:**\
   pip install -r requirements.txt

5. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.

- **main.py**: Entry point of the application. Everything was put on one file as we were working on mac and Os and any other option resulted in bugs from one side or another.

  **minimax**
  implementing the method
  **tkinter**
  creating a game window. 
  **game functions**
  implementing the base game functions, like checking for victory, creating a grid or simply playing 
  ** controls**
  creating the buttons and their functionalities with tkinter 
  
  


## **🧪 Testing & Validation**

How can a user verify the code works?

- List any test scripts included (e.g., pytest tests/).

- **Describe the "Happy Path" inputs for the demo.**
- In this scenario, our happy path would be for the player to actively try to win at the game. In human vs human, every victory should be detected by the algoritm. in human Vs AI, as the level gets harder it should be harder to win, and matches should end up in losses or ties in the hardest level. For AI vs AI, each Ai should be making logical choices and mimicking an actual gameplay. 
  


## **📦 Dependencies**

**List the main third-party libraries used and _why_ they were chosen:**

- Tkinter : in order to create a game window with functionning buttons
- Tkinter.messagebox() module : provides a template base class for popup win windows 
- Minimax methode: recursive minimax algorythm to collect and save pathways for the AI player 


## **🔮 Future Roadmap (v2.0)**

**What features would you add if you had more time or a larger budget?**

If given more time, we would have added some options for the AI vs AI game to have mutiple difficulty levels, in order to see different levels of AI competing against one another. 
Another option discussed was to turn it into another known game, connect 4, but we ultimately decided to focus on other parts of the project first. 


_Generated as part of the Algorithmique avancée Production Deliverables._

__
