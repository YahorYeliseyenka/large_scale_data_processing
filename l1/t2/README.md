# L1 - 2019

## Task 2
Proof that you can use Vim:
- find an expression
  ```text
  / or ? + <expression> .
  Press the n key to go directly to the next occurrence of the word.
  ```
- jump to line
  ```text
  42G
  42gg
  :42<CR>
  ```
- substitute a single character
  ```text
  A single character can be replaced with the r command for current cursor position.
  ```
- substitute a whole expression
  ```text
  :s/PATTERN/REPLACEMENT/ to substitute in a current line
  :%s/PATTERN/REPLACEMENT/ to substitute in a whole file
  ```
- save changes
  ```text
  :w 
  ```
- exit Vim (2 ways)
  ```text
  :q to quit
  :q! to quit without saving
  ZZ to save and quit
  ZQ to just quit
  ```

