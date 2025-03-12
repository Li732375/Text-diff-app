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

<<<<<<< HEAD
因 PyQt5 採用 GPL (GNU，General Public License) v3 或 商業許可證。表示：

- 免費使用（GPLv3）
你可以免費使用 PyQt5 進行開發，但你的應用程式也 必須 採用 GPLv3（即開源）。
如果你的應用程式不是開源的，那就 不能免費使用 PyQt5。
- 商業授權
如果你要開發 封閉源碼（商業）應用程式，你需要購買 Riverbank Computing 提供的商業許可證。
- PyQt5 與 Qt 的區別
  - Qt 本身 提供 LGPL 授權（允許封閉源碼使用）。
  - PyQt5 只提供 GPL 或商業許可證，因此 無法免費用於封閉源碼專案。

因此本專案採用 GNU GPL 授權條款。
=======
2. Install the required dependencies:
>>>>>>> parent of 707e21c (釋出該軟體首個版本)

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

This project is licensed under the GNU GPL License.