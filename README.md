# Designer-ai-1

Our project is dedicated to the development of a module aimed at supporting students in both the creation and comprehension of **Entity-Relationship (ER) models**.
</br>
The primary function of this tool is to transform textual instructions outlining logical concepts into tangible ER models. By bridging the gap between textual representation and visual understanding, our module strives to provide an extended resource for students to enhance their proficiency in ER model creation and interpretation.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.x (download and installation instructions: [Python Downloads](https://www.python.org/downloads/))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/masoud-khalilian/designer-ai-1.git
   ```

2. Navigate to the project directory:

   ```bash
   cd designer-ai-1
   ```

3. set the environment variables in .env file

### Running the Program

berfore running the code you must create a .env file and define the api keys we will provide you the keys to the file upon asking

Run the following command from the project's root directory:
you have option between 3 different main file

for using finetuned gpt-3.5 use

```bash
python main_gpt_3.py
```

for using using variety of operouter models use

```bash
python main_openrouter.py
```

for using getting json to be created by llm use the following but be careful that it will not produce good result in many of instances

```bash
python main_with_json.py
```

after running the command the system will ask you about the description of your ER-model

write or paste the description in the command line and then ctrl+z and press enter (because you can input multi line).

the output file will be close the the mains with name given in main.

you can change some settings in config file and and above each main file there is little more config setting too.

## Evaluating the Outcome

After executing the program and entering your prompt, the generated output will be stored in a file. Visit [designER](https://designerdb.io/) and upload the generated file. Compare the given prompt with the visual representation, and kindly provide constructive feedback to assist us in further refinement. Please be aware that this feature is currently under development, and your input is invaluable in enhancing the overall quality of the results.
