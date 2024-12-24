# Mazeofchemistry : A python chemical-like game

Mazeofchemistry is a python game which let user to have a brief knowledge about chemistry. Although some of the explainations are not clear and rigourous enough, it is friendly for person who has the curiousity on chemistry tho has no foundation of chemistry.

## (1) 程式的功能 Features

Mazeofcheimstry provides the following functionalities:

- **pygame template** : using pygame to make the program more interesting and having more interaction instead using the command box

# stage1

- **inserting answer** : user is in order to insert the respective answer when there is a blank or gap for user to enter something
# stage2

- **online database access** : instead of inserting the molar mass of each element and tolerate the molecular weight of each compound, visiting the online database and take those desired information

- **3d-like molecule structure** : when user answered correctly, the 3d model of the compound will be displayed

# stage3

- **reaction leveling-local database access** : for complicated program and having a huge amount of database, by inserting the information into a local database will create a more stable program-running-environment,such as this stage the program will provide a chemical reaction without coefficient which letting user to level it

# stage4

- **changing on concentration-dynamic display** : when user answer correctly the chemical reaction equilibrium constant, then there will display a dynamic concentration changing against time graph, which let user has a more deep understanding about chemical equilibrium

## (2) 使用方式 

Follow these steps to use Mazeofchemistry

### 1. Set up Your Environment

To use Mazeofchemistry, follow these steps:

```bash
# download attachment
chemical_equations.json
# install dependencies
pip install requests
pip install pygame
pip install json
pip install numpy
pip install matplotlib
pip install rdkit
```

### 2. Step 1 (insert the compound which you are curious on)

At first, there is a blank for the user to guide them to enter a correct compound name, which will activate the game tool

### 3. Step 2 (test on molecular weight and 3d-compound structure)

Based on the compound inserted by user, there is another blank for them to inserted the correct molecular weight, which allowed the error within +-2

While user answered the correct answer, there is a 3d-molecular structure been displayed for user to know about this compound

### 4. Step 3 (test on chemical reaction leveling)

After that, pygame will flip to another interface, which will provide a chemical reaction without the coefficient(chemical stoichiometry),then aspect user to level it with the correct coefficient

*Note that: while finish typing every compound and symbol, dont forget to space one column so pygame could detect the correct answer

### 5. Step 4 (test on chemical reaction equlibrium constant and dynamic display)

Lastly, pygame will provide a rough chemical reaction and also provide concentration for each reactants and products, which we assumed it is the concentration when the reaction reached equilibrium state

User is in order to calculate the chemical reaction equilibrium constant and this program allowed an error between 0.5

After user answered the correct answer, there is a concentration changes against time graph dislay dynamically

Finally, this game is ended and there is a string " Congratulations! You won!" will be displayed

## (3) 程式的架構 Program Architecture

The project is organized as follows:

```
Mazeofchemistry/
|——mazeofchemsitry/
|  |——pygame.init
|  |——interface setting
definition to simplify the block
|  |——common function
make each game as a stage and define as a block
|  |——stage1
|  |——stage2
|  |——stage3
|  |——stage4
by defining main to merge those block in order
|  |——main.py
adding ending word
|  |——setting(for the last interface)
if __name__="__main__":
  main()
```
## (4) 開發過程 Development Process

The development of Mazeofchemistry followed these steps:

1. **Ideation and Planning** : Since I has a more deep knowledge about chemistry comparing with physics, I decided to make a program which is about chemistry. Then, after choosing the categories and the small planning, I decided to merge all of my idea into a big program, then I asked ChatGPT for help and it suggested me by using pygame
2. **implementation** : Bulit those common functions and also define the stage game, but due to the pygame template which I am not so familiar with, I seeked for help from ChatGPT to contribute the program to make it logically run well
3. **Testing** : Just like what I have mentioned, I setted every stage game as a block and run through individually,if there is any problem,then debug, if not, then merge into the final program. What I need to do is just define the main block and arrange the ordering of the block
4. **Enhancements** : The original pygame interface is very simple and boring, so I had added some colour and some elements such as block, big font and etc by asking ChatGPT

## (5) 參考資料來源 References

1. ChatGPT- Assisted with ducumentation and architectural structuring of the project
   - conservation with chatgpt: https://chatgpt.com/share/676aca3d-771c-800b-be0c-8bbbbdc8808c

## (6) 程式修改或增强的内容 Enhancements and Contributions

The following modifications and enhancements were added to the project

### Unique Contributions:
1. Instead just letting user to insert the answer and jump to the next question, I created several "feedback" so that user could have the interaction with the project and also could know more about chemical knowledge
2. Setting the answer so that it could have a bigger range of answer to let the user to insert it since pygame only accept the specific answer at first 
