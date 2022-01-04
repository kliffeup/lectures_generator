# lectures_generator
ImageToVideo &amp; TextToSpeech Lectures Generator

## Description
A script that gets a photo of a person and some text as an input and outputs a `.mp4` video of that person saying the text with a woman's voice.

## Google Colab demo
You can perform script work by running Google Colab Notebook, see `lectures_generator_demo.ipynb` or [demo in Google Colab](https://colab.research.google.com/drive/1xEje2h5xsLXGlxF78ZaaeznmxPeuXti3?usp=sharing).

## Requirements
- **CUDA supporting machine**;
- **Unix-like OS (Linux, Mac OS)**;
- **Python >= 3.6**;

[Google Colab](https://colab.research.google.com/) satisfies these requirements.

## Installation

- Clone repo:
```bash
git clone https://github.com/kliffeup/lectures_generator
```

- Go to the repository folder:
```bash
cd lectures_generator/
```

- Install python packages:
```bash
pip install -r requirements.txt
```

## Before using: input data preprocessing

### Add long pauses

If you want a long pause in the output video, for example between two paragraps, you need to simply preprocess your input text: just add `[paragraph]` between the two parts you wish to separate.

- Example: we have `input.txt` and we need a long pause between these sentences:

```
Hello, my name is Mona Lisa and I need a long pause after that sentence.
OK, let's start!
```

- insert `[paragraph]` and it's done!

```
Hello, my name is Mona Lisa and I need long pause after that sentence.
[paragraph]
OK, let's start!
```

Possible pause duration: 3 or 5 seconds.

You can specify it in the script parameters, [see below](#script-running).

### Replacements file

Sometimes the separate words pronunciation quality of the Text-To-Speech model that is used in this script leaves much to be desired.

You can use `.json` file with json-like dict that contains pairs of word replacements
```
<a word or a phrase which tends to sound bad, json-like string>: <replacement, json-like string>
```
to fix this trouble. This file should be specified in the script command-line parameters, [see below for more](#script-running).

- Example: we have `input.txt` as follows
```
'ML' is badly pronounced by our model.
```

and we know that the pronunciation of `'ML'` is not so good.

Just create a file `replacements.json`
```
{"ML": "EM EL"}
```

and pass it to the script command-line parameters.

### Custom image requirements:

img2vid part of the script requires to have a **`.jpg` format portrait image with a resolution `256x256`** as an input image.

**Be aware** of it if you want to pass a custom portrait to the script.

## Script running

The script can be run like this:
```bash
python ./script.py --text <relative path to text file> --image <relative path to portrait file> --replacements <relative path to replacements file> --output <relative path to output folder> --pause-duration <pause duration>
```
The command-line parameters description:

- `-t/--text <relative path to text file>` - **REQUIRED**. Pass an input text file to the script;
- `-i/--image <relative path to portrait file>` - **OPTIONAL**. Pass an input portrait image to the script. By default pass [this image](https://github.com/kliffeup/lectures_generator/blob/master/MakeItTalk/examples/monalisa2.jpg);
- `-r/--replacements <relative path to replacements file>` - **OPTIONAL**. Pass a replacements `.json` file described [above](#replacements-file) to the script. By default pass nothing;
- `-o/--output <relative path to output folder>` - **OPTIONAL**. Pass a specified folder to the script to save an output video in. By default pass a current directory of the script;
- `-p/--pause-duration <pause duration>` - **OPTIONAL**. Pass a pause duration (in seconds) between two paragraphs. Possible values: 3, 5. By default pass 3.
- `-h/--help` - Shows the **help** message.
