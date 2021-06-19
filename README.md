# KaasScript

A programming language made in Python.

<details>
  <summary>Arithmetic Operators</summary>

| Operator | Meaning                      | Example                                  |
| -------- | ---------------------------- | ---------------------------------------- |
| +        | Addition                     | <code>5 + 10; // 15</code>               |
| -        | Subtraction                  | <code>10 - 5; // 2<br>- 5; // -5 </code> |
| \*       | Multiplication               | <code>5 \* 10; // 50</code>              |
| /        | Division                     | <code>10 / 5; // 2</code>                |
| %        | Modulus (Division Remainder) | <code>10 % 4; // 2</code>                |
| ^        | Exponentiation               | <code>2 ^ 4; // 16</code>                |
| #        | Root of                      | <code>3 # 27; // 3<br># 4; // 2</code>   |

</details>
<details>
  <summary>Assignment Operators</summary>

| Operator | Meaning                      | Example                                   |
| -------- | ---------------------------- | ----------------------------------------- |
| =        | Set value to                 | <code>var x = 10;</code>                  |
| +=       | Addition                     | <code>var a = 5;<br>a += 10; // 15</code> |
| -=       | Subtraction                  | <code>var a = 10;<br>a -= 5; // 5</code>  |
| \*=      | Multiplication               | <code>var a = 5;<br>a \* 10; // 50</code> |
| /=       | Division                     | <code>var a = 10;<br>a /= 5; // 2</code>  |
| %=       | Modulus (Division Remainder) | <code>var a = 10;<br>a %= 4; // 2</code>  |
| ^=       | Exponentiation               | <code>var a = 2;<br>a ^= 4; // 16</code>  |
| #=       | Root of                      | <code>var a = 3;<br>a #= 27; // 3</code>  |

</details>
<details>
  <summary>Increment / Decrement Operators</summary>

| Operator | Meaning                                              | Example                    |
| -------- | ---------------------------------------------------- | -------------------------- |
| ++x      | Pre-increment (Increments x by one, then returns x)  | <code>++x; // x + 1</code> |
| x++      | Post-increment (Returns x, then increments x by one) | <code>x++; // x</code>     |
| --x      | Pre-decrement (Decrements x by one, then returns x)  | <code>--x; // x - 1</code> |
| x--      | Post-decrement (Returns x, then decrements x by one) | <code>x--; // x</code>     |

</details>
<details>
  <summary>Comparison Operators</summary>

| Operator | Meaning                    | Example                            |
| -------- | -------------------------- | ---------------------------------- |
| ==       | Equal to                   | <code>10 == '10'; // true</code>   |
| ===      | Egual value and equal type | <code>10 === '10'; // false</code> |
| !=       | Not equal                  | <code>5 != 10; // true</code>      |
| >        | Greater than               | <code>5 > 10; // false</code>      |
| <        | Less than                  | <code>5 < 10; // true</code>       |
| >=       | Greater than or equal to   | <code>5 >= 5; // true</code>       |
| <=       | Less than or equal to      | <code>5 <= 10; // true</code>      |

</details>
<details>
  <summary>Logical Operators</summary>

| Operator | Meaning | Example                                      |
| -------- | ------- | -------------------------------------------- |
| &&       | And     | <code>true && true // true</code>            |
| \|\|     | Or      | <code>true &#124;&#124; false // true</code> |
| !        | Not     | <code>!false // true</code>                  |

</details>
<details>
  <summary>Conditional Assignment Operators</summary>

| Operator | Meaning                        | Example                                    |
| -------- | ------------------------------ | ------------------------------------------ |
| ? :      | Conditional (ternary) operator | <code>var x = y == z ? 'yes' : 'no'</code> |

</details>
<details>
  <summary>Data Types</summary>

| Type    | Example                                          |
| ------- | ------------------------------------------------ |
| Number  | <code>1</code> or <code>2.71</code>              |
| String  | <code>'Example'</code> or <code>"Example"</code> |
| Boolean | <code>true</code> or <code>false</code>          |
| List    | <code>\[1, 12.56, 'Example', true]</code>        |
| Null    | <code>null</code>                                |

</details>
<details>
  <summary>Variables</summary>

| Type     | Meaning                               | Example                           |
| -------- | ------------------------------------- | --------------------------------- |
| Normal   | A reassignable variable               | <code>var str = 'example';</code> |
| Constant | A variable that can not be reassigned | <code>const pi = 3.14;</code>     |

</details>
<details>
  <summary>Conditional Statements</summary>

| Type           | Example                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------- |
| If             | <code>if (age >= 18) {<br>&nbsp;&nbsp;return 'You are allowed to vote!'<br>};</code>                     |
| Elif (else if) | <code>elif (age < 18 && age >= 0) {<br>&nbsp;&nbsp;return 'You are not old enough to vote!'<br>};</code> |
| Else           | <code>else {<br>&nbsp;&nbsp;return 'Age is less than zero!'<br>};</code>                                 |

</details>
<details>
  <summary>Loops</summary>

Loops can use the <code>break</code> statement to jump out of a loop.
The <code>continue</code> statement will jump over one iteration in the loop.

| Type  | Example                                                                                                                                                                                 | Info                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| For   | <code>const array = ['pizza', 'cheese', 'ice cream'];<br>for i = 0 to len(array) step 1 {<br>&nbsp;&nbsp;print(array / i);<br>&nbsp;&nbsp;if (array / i == 'cheese') break;<br>}</code> | <code>step</code> is optional.<br>default is 1 |
| While | <code>var number = 0;<br>while (number < 10) {<br>&nbsp;&nbsp;number++;<br>&nbsp;&nbsp;print(number);<br>&nbsp;&nbsp;if (number == 8) continue;<br>}</code>                             |                                                |

</details>
<details>
  <summary>Functions</summary>

| Type     | Example                                                                                     |
| -------- | ------------------------------------------------------------------------------------------- |
| Brackets | <code>function funnyFunction(value) {<br>&nbsp;&nbsp;return value + ' is fun!'<br>};</code> |
| Arrow    | <code>function funnyFunction(value) -> value + ' is fun!';</code>                           |

</details>
<details>
  <summary>Built-in Functions</summary>

| Type        | Info                                                              |
| ----------- | ----------------------------------------------------------------- |
| len(data)   | Returns the length of a <code>list</code> or <code>string</code>. |
| print(data) | Prints a string representation of an object to the console.       |
| input       | Reads and returns a string from the console.                      |
| run(file)   | Runs a <code>.kss</code> file                                     |

</details>
