# Masked Split
Split text with masked substrings where delimiters would not apply.

Input text: `"Hello, World!" {USER.NAME} Said. What a surprise! I was happy.`

Delimiters: `['!', '.']`

Masks: `[['"', '"'], ['{', '}']]`

Result: `['"Hello, World!" {USER.NAME} Said.', 'What a surprise!', 'I was happy.']`
