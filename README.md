# text-diff-app/text-diff-app/README.md

# Text Diff App

This is a simple PyQt5 application that allows users to input two pieces of text and compare their differences using the `difflib` library. The application provides a user-friendly interface to visualize the differences between the two texts.

## Features

- Input two pieces of text for comparison.
- View differences highlighted in a web view.
- Easy-to-use interface.

## Requirements

- Python 3.x
- PyQt5
- difflib (included in Python standard library)

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd text-diff-app
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute the following command:

```
python src/main.py
```

## Usage

1. Enter the first piece of text in the first text area.
2. Enter the second piece of text in the second text area.
3. Click the "Compare" button to view the differences.
4. The differences will be displayed in a web view below the input areas.

## License

This project is licensed under the MIT License.