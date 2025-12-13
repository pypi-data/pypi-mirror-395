# Masked Split
Split text with masked substrings where delimiters would not apply.

input text: "Hello, World!" {USER.NAME} Said. What a surprise! I was happy.
delimiters: ['!', '.']
masks: [['"', '"'], ['{', '}']]

Result:
['"Hello, World!" {USER.NAME} Said.', 'What a surprise!', 'I was happy.']
