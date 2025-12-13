# deciml
### pip install deciml

## ***Abbrevations***

1. *variable -* **v**
2. *function -* **f**
3. *staticmethod -* **sm**
4. *classmethod -* **cm**
5. *class -* **s**
6. *object class -* **o**

## **Documentation**

**Note - The function arguments are explained in the "Docstring" (See in an editor).**

**Note - The default precision is used if precision is not given. Precison is the number of digits after decimal point,** ***different from total digits (As used in Decimal).***

<details>
   <summary>Precision</summary>
   <p>

   **Note - Explaination of [precision](./deciml_explained/precision.md)**
   
   1. (v) **__DecimalPrecision**: Variable used for precision, **default precision** used if precision is not specified.

   2. (f) **setpr(__p)**: Changes the precision
   
      ```python
      >>> from deciml.deciml import setpr
      >>> setpr(18)
      '''
         18 - The new precision
      '''
      ```

   3. (f) **getpr()**: Get the precision

      ```python
      >>> from deciml.deciml import getpr
      >>> precision = getpr()
      >>> precision
      18
      ```

   ***Note - Precision is integer***
   </p>
</details>

<details>
   <summary>Constant</summary>
   <p>

   **Note - Explaination of [constant](./deciml_explained/constant.md)**

   1. (v) **_Pi**: Variable that stores the value of pi

   2. (v) **_EulersNumber**: Variable that stores the value of e

   3. (c) **constant**: Get values of constants

      ```python
      >>> from deciml.deciml import constant
      ```

      i. (sm) **e(pr)**: Get value of e (in constant)

         ```python
         >>> value = constant.e(18)
         '''
            18 - The precision
         '''
         >>> value
         Decimal('2.718281828459045235')
         ```

      ii. (sm) **pi(pr)**: Get value of pi (in constant)

         ```python
         >>> value = constant.pi(18)
         '''
            18 - The precision
         '''
         >>> value
         Decimal('3.141592653589793238')
         ```
   </p>
</details>

<details>
   <summary>Random</summary>
   <p>

   **Note - Explaination of [random](./deciml_explained/random.md)**

   1. (f) **rint(__i, __j, __n, s)**: Generate random integers

      ```python
      >>> from deciml.deciml import rint
      >>> nums = rint(0, 100, 5, 2102)
      '''
         0 - Start integer
         100 - End integer
         5 - Number of integers to generate
         2102 - Seed
      '''
      >>> nums
      (38, 89, 64, 13, 59)
      ```

   2. (o) **rdeciml(__a, __b, __pr)**: Generate a rdeciml object

      ```python
      >>> from deciml.deciml import rdeciml
      >>> robj = rdeciml(0, 20, 18)
      '''
         0 - Start number
         20 - End number
         18 - The precision
      '''
      ```

      i. (f) **random(__n, __s)**: Generate random numbers (in rdeciml)

      ```python
      >>> nums = robj.random(4, 2025)
      '''
         4 - Number of random numbers to generate
         2025 - The seed
      '''
      >>> nums
      (Decimal('19.972330207834593468'), Decimal('9.763654124294660886'), Decimal('17.954068930830723688'), Decimal('4.279774972623744952'))
      ```

      ii. (f) **cgpr(__pr)**: Change precision for random numbers (in rdeciml) 

      ```python
      >>> robj.cgpr(2)
      New precision: 2
      '''
         2 - New precision to generate random numbers
      '''
      >>> robj.random(4, 2025)
      (Decimal('11.42'), Decimal('1.69'), Decimal('13.22'), Decimal('17.15'))
      ```

   ***Note - The seed returns different values after changing precision.***

   </p>
</details>


<details>
   <summary>Decimal Functions</summary>
   <p>

   1. (f) **deciml(__a, __pr)**: Get a Decimal object

      **Note - Explaination of [deciml](./deciml_explained/deciml_function.md)**

      ```python
      >>> from deciml.deciml import deciml
      >>> num = deciml('32.0722168131', 7)
      '''
         '32.0722168131' - The variable to convert to Decimal
         7 - The precision
      '''
      >>> num
      Decimal('32.0722168')
      ```

   2. (f) **abs(__a)**: Get the absolute value

      **Note - Explaination of [absolute](./deciml_explained/absolute.md)**

      ```python
      >>> from deciml.deciml import abs
      >>> abs_value = abs(-0.526842)
      '''
         -0.526842 - The variable to convert to it's absolute value
      '''
      >>> abs_value
      Decimal('0.526842')
      ```
   
   3. (f) **deciml_sort(__a, __pr)**: Get a new sorted list

      ```python
      >>> from deciml.deciml import deciml_sort
      >>> sorted_list = deciml_sort([12.525, 2.08, 9.2552, '-4.515117E1'], 4)
      '''
         [12.525, 2.08, 9.2552, '-4.515117E1'] - Variable to sort
         4 - The precision for sorted list
      '''
      >>> sorted_list
      [Decimal('-45.1512'), Decimal('2.08'), Decimal('9.2552'), Decimal('12.525')]
      ```

   </p>
</details>

<details>
   <summary>Arithmatic Operations</summary>
   <p>
<details>
   <summary>Primitive Operations</summary>
   <p>

   **(c) algbra**: primitive arithmatic operations

   ```python
   >>> from deciml.deciml import algbra
   ```

   i. (sm) **add(*__a, pr)**: add given numbers

   **Note - Explaination of [add](./deciml_explained/aithmatic_operations/add.md)**

   ```python
   >>> nums_sum = algbra.add(2.3221, 5.2425, 120.522, pr=3)
   '''
      2.3221, 5.2425, 120.522 - Numbers to add
      3 - The precision
   '''
   >>> nums_sum
   Decimal('128.087')
   ```

   ii. (sm) **sub(*__a, pr)**: subtract given numbers

   **Note - Explaination of [sub](./deciml_explained/aithmatic_operations/subtract.md)**

   ```python
   >>> nums_sub = algbra.sub(2.5562, 25.5521, 2.245, pr=3)
   '''
      25.5521, 2.245 - Numbers to subtract from 2.5562
      3 - The precision
   '''
   >>> nums_sub
   Decimal('-25.241')
   ```


   iii. (sm) **mul(*__a, pr)**: multiply given numbers

   **Note - Explaination of [mul](./deciml_explained/aithmatic_operations/multiply.md)**

   ```python
   >>> nums_mul = algbra.mul(2.9525, 3.755, 2.3524, pr=3)
   '''
      2.9525, 3.755, 2.3524 - Numbers to multiply
      3 - The precision
   '''
   >>> nums_mul
   Decimal('26.080')
   ```
   iv. (sm) **div(__a, __b, __pr)**: divide given numbers

   **Note - Explaination of [div](./deciml_explained/aithmatic_operations/divide.md)**

   ```python
   >>> num = algbra.div(2.02354, 3.2152, 4)
   '''
      2.02354 - Numerator
      3.2152 - Denominator
      4 - The precision
   '''
   >>> num
   Decimal('0.6294')
   ```

   v. (cm) **log(__a, __b, __pr)**: logarithmic given numbers

   **Note - Explaination of [log](./deciml_explained/aithmatic_operations/log.md)**

   ```python
   >>> num = algbra.log(2.23541, 3, 4)
   '''
      2.23541 - Number
      3 - Base
      4 - The precision
   '''
   >>> num
   Decimal('0.7322')
   ```

   vi. (cm) **pwr(__a, __b, __pr)**: exponent from given numbers

   **Note - Explaination of [pwr](./deciml_explained/aithmatic_operations/exponent.md)**

   ```python
   >>> num = algbra.pwr(2.3214, 2.213, 4)
   '''
      2.3214 - Number
      2.213 - Power
      4 - The precision
   '''
   >>> num
   Decimal('6.4477')
   ```

   </p>
</details>
<details>
   <summary>Grouped Operations</summary>
   <p>

   **(c) galgbra**: Arithmatic operations using lists

   ```python
   >>> from deciml.deciml import galgbra
   ```

   i. (sm) **add(*__a, pr)**: Addition with lists of numbers

   ```python
   >>> nums = galgbra.add([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894], pr=4)
   '''
      [2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894] - Lists to add
      4 - The precision
   '''
   >>> nums
   (Decimal('30.8847'), Decimal('88.1372'), Decimal('50.1749'))
   ```

   ii. (sm) **sub(*__a, pr)**: Subtraction with list of numbers

   ```python
   >>> nums = galgbra.sub([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894], pr=4)
   '''
      [2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894] - Lists to subtract
      4 - The precision
   '''
   >>> nums
   (Decimal('-26.4217'), Decimal('-83.4067'), Decimal('-37.5235'))
   ```

   iii. (sm) **mul(*__a, pr)**: Multiplication with list of numbers

   ```python
   >>> nums = galgbra.mul([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894], pr=4)
   '''
      [2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], [21.3265, 0.23654, 20.3256894] - Lists to multiply
      4 - The precision
   '''
   >>> nums
   (Decimal('348.6825'), Decimal('47.8556'), Decimal('3024.5107'))
   ```

   iv. (sm) **div(__a, __b, __pr)**: Division with lists of numbers

   ```python
   >>> nums = galgbra.div([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], 4)
   '''
      [2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235] - Lists to divide
      4 - The precision
   '''
   >>> nums
   (Decimal('0.3046'), Decimal('0.027653'), Decimal('0.2689'))
   ```

   v. (sm) **log(__a, __b, __pr)**: Logarithm with lists of numbers

   ```python
   >>> nums = galgbra.log([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], 4)
   '''
      [2.23153, 2.36528, 6.32569] - List of numbers
      [7.32669, 85.5354, 23.5235] - List of base
      4 - The precision
   '''
   >>> nums
   (Decimal('0.4031'), Decimal('0.1935'), Decimal('0.5841'))
   ```

   vi. (sm) **pwr(__a, __b, __pr)**: Exponentiation with lists of numbers

   ```python
   >>> nums = galgbra.pwr([2.23153, 2.36528, 6.32569], [7.32669, 85.5354, 23.5235], 4)
   '''
      [2.23153, 2.36528, 6.32569] - Lists of numbers
      [7.32669, 85.5354, 23.5235] - Lists of exponents
      4 - The precision
   '''
   >>> nums
   (Decimal('358.1823'), Decimal('95541990468229107013623363686972.6621'), Decimal('6996193289690917769.8999'))
   ```

   vii. (sm) **addsg(__a, __b, __pr)**: Addition of a list of numbers with a number

   ```python
   >>> nums = galgbra.addsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Number to add
      [7.32669, 85.5354, 23.5235] - List of numbers to add
      4 - 
   '''
   >>> nums
   (Decimal('9.3522'), Decimal('87.5609'), Decimal('25.5490'))
   ```

   viii. (sm) **subsg(__a, __b, __pr)**: Subtraction of a list of numbers from a number

   ```python
   >>> nums = galgbra.subsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Number
      [7.32669, 85.5354, 23.5235] - Numbers to subtract
      4 - The precision
   '''
   >>> nums
   (Decimal('-5.3012'), Decimal('-83.5099'), Decimal('-21.49710'))
   ```

   ix. (sm) **subgs(__a, __b, __pr)**: Subtraction of number from a list of numbers

   ```python
   >>> nums = galgbra.subgs([7.32669, 85.5354, 23.5235], 2.02552, 4)
   '''
      [7.32669, 85.5354, 23.5235] - Numbers
      2.02552 - Number to subtract
      4 - The precision
   '''
   >>> nums
   (Decimal('5.3012'), Decimal('83.5099'), Decimal('21.49710'))
   ```

   x. (sm) **mulsg(__a, __b, __pr)**: Multiplication of number with a list of numbers

   ```python
   >>> nums = galgbra.mulsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Number
      [7.32669, 85.5354, 23.5235] - Numbers to multiply
      4 - The precision
   '''
   >>> nums
   (Decimal('14.8404'), Decimal('173.2537'), Decimal('47.6473'))
   ```

   xi. (sm) **divsg(__a, __b, __pr)**: Division of number by a list of numbers 

   ```python
   >>> nums = galgbra.divsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Numerator
      [7.32669, 85.5354, 23.5235] - Denominators
      4 - The precision
   '''
   >>> nums
   (Decimal('0.2765'), Decimal('0.023681'), Decimal('0.086106'))
   ```

   xii. (sm) **divgs(__a, __b, __pr)**: Division of a list of numbers by number  

   ```python
   >>> nums = galgbra.divgs([7.32669, 85.5354, 23.5235], 2.02552, 4)
   '''
      [7.32669, 85.5354, 23.5235] - Numerators
      2.02552 - Denominator
      4 - The precision
   '''
   >>> nums
   (Decimal('3.6172'), Decimal('42.2289'), Decimal('11.6136'))
   ```

   xiii. (sm) **logsg(__a, __b, __pr)**: Logarithm of numbers with a list of bases

   ```python
   >>> nums = galgbra.logsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Number
      [7.32669, 85.5354, 23.5235] - Bases of logarithm
      4 - The precision
   '''
   >>> nums
   (Decimal('0.3544'), Decimal('0.1587'), Decimal('0.2235'))
   ```

   xvi. (sm) **loggs(__a, __b, __pr)**: Logarithm of a list of numbers with base

   ```python
   >>> nums = galgbra.loggs([7.32669, 85.5354, 23.5235], 2.02552, 4)
   '''
      [7.32669, 85.5354, 23.5235] - Numbers
      2.02552 - Base of logarithm
      4 - The precision
   '''
   >>> nums
   (Decimal('2.8215'), Decimal('6.3031'), Decimal('4.4742'))
   ```

   xvii. (sm) **pwrsg(__a, __b, __pr)**: Exponentiate a number by a list of numbers

   ```python
   >>> nums = galgbra.pwrsg(2.02552, [7.32669, 85.5354, 23.5235], 4)
   '''
      2.02552 - Number
      [7.32669, 85.5354, 23.5235] - Exponents
      4 - The precision
   '''
   >>> nums
   (Decimal('176.1563'), Decimal('165853714112712692593865989.2344'), Decimal('16248459.7577'))
   ```

   xviii. (sm) **pwrgs(__a, __b, __pr)**: Exponentiate a list of numbers by number

   ```python
   >>> nums = galgbra.pwrgs([7.32669, 85.5354, 23.5235], 2.02552 , 4)
   '''
      [7.32669, 85.5354, 23.5235] - Numbers
      2.02552 - Exponent
      4 - The precision
   '''
   >>> nums
   (Decimal('56.4791'), Decimal('8195.9659'), Decimal('599.7974'))
   ```

   </p>
</details>
   </p>
</details>

<details>
   <summary>Trignometric Operations</summary>
   <p>
<details>
   <summary>Primitive Operations</summary>
   <p>

   **(c) trig**: Primitive trignometric operations

   ```python
   >>> from deciml.deciml import trig
   ```

   i. (sm) **sin(__a, __pr)**: To get the sine of a number

   **Note - Explaination of [sin](./deciml_explained/trignometric_operations/sine.md)**

   ```python
   >>> num = trig.sin(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('0.90406')
   ```

   ii. (sm) **cos(__a, __pr)**: To get the cosine of a number

   **Note - Explaination of [cos](./deciml_explained/trignometric_operations/cosine.md)**

   ```python
   >>> num = trig.cos(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('-0.42740')
   ```

   iii. (cm) **tan(__a, __pr)**: To get the tan of a number

   ```python
   >>> num = trig.tan(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('-2.11525')
   ```

   iv. (cm) **cosec(__a, __pr)**: To get the cosec of a number

   ```python
   >>> num = trig.cosec(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('1.10612')
   ```

   v. (cm) **sec(__a, __pr)**: To get the sec of a number

   ```python
   >>> num = trig.sec(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('-2.33971')
   ```

   vi. (cm) **cot(__a, __pr)**: To get the cot of a number

   ```python
   >>> num = trig.cot(2.012414, 5)
   '''
      2.012414 - Number
      5 - The precision
   '''
   >>> num
   Decimal('-0.47276')
   ```

   vii. (cm) **asin(__a, __pr)**: To get the sine<sup>-1</sup> of a number
   
   **Note - Return upper bound is pi/2 and lower bound is -pi/2.**

   ```python
   >>> num = trig.asin(0.241445, 5)
   '''
      1.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('0.24385')
   ```

   viii. (cm) **acos(__a, __pr)**: To get the cosine<sup>-1</sup> of a number
   
   **Note - Return upper bound is pi and lower bound is 0.**

   ```python
   >>> num = trig.acos(0.241445, 5)
   '''
      0.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('1.32694')
   ```

   ix. (cm) **atan(__a, __pr)**: To get the tan<sup>-1</sup> of a number

   ```python
   >>> num = trig.atan(7.241445, 5)
   '''
      7.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('1.43357')
   ```

   x. (cm) **acosec(__a, __pr)**: To get the cosec<sup>-1</sup> of a number

   ```python
   >>> num = trig.acosec(1.241445, 5)
   '''
      0.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('0.93654')
   ```

   xi. (cm) **asec(__a, __pr)**: To get the sec<sup>-1</sup> of a number

   ```python
   >>> num = trig.asec(1.241445, 5)
   '''
      1.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('0.63426')
   ```

   xii. (cm) **acot(__a, __pr)**: To get the cot<sup>-1</sup> of a number

   ```python
   >>> num = trig.acot(7.241445, 5)
   '''
      7.241445 - Number
      5 - The precision
   '''
   >>> num
   Decimal('0.13723')
   ```
   </p>
</details>
<details>
   <summary>Grouped Operations</summary>
   <p>

   **(c) gtrig**: Grouped trignometric operations
   
   ```python
   >>> from deciml.deciml import gtrig
   ```

   i. (sm) **sine(__a, __pr)**: To get the sine for a list of numbers

   ```python
   >>> nums = gtrig.sine([0.256745, 0.754455, 0.454845, 0.3874258], 4)
   '''
      [0.256745, 0.754455, 0.454845, 0.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.2539'), Decimal('0.6849'), Decimal('0.4393'), Decimal('0.3778'))
   ```

   ii. (sm) **cosine(__a, __pr)**: To get the cosine for a list of numbers

   ```python
   >>> nums = gtrig.cosine([0.256745, 0.754455, 0.454845, 0.3874258], 4)
   '''
      [0.256745, 0.754455, 0.454845, 0.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.9672'), Decimal('0.7286'), Decimal('0.8983'), Decimal('0.9259'))
   ```

   iii. (sm) **tan(__a, __pr)**: To get the tan for a list of numbers

   ```python
   >>> nums = gtrig.tan([6.256745, 8.754455, 9.454845, 13.3874258], 4)
   '''
      [6.256745, 8.754455, 9.454845, 13.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('-0.026446'), Decimal('-0.7928'), Decimal('0.030077'), Decimal('1.07310'))
   ```

   iv. (sm) **cosec(__a, __pr)**: To get the cosec for a list of numbers

   ```python
   >>> nums = gtrig.cosec([6.256745, 8.754455, 9.454845, 13.3874258], 4)
   '''
      [6.256745, 8.754455, 9.454845, 13.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('-37.8254'), Decimal('1.6097'), Decimal('-33.2640'), Decimal('1.3664'))
   ```

   v. (sm) **sec(__a, __pr)**: To get the sec for a list of numbers

   ```python
   >>> nums = gtrig.sec([6.256745, 8.754455, 9.454845, 13.3874258], 4)
   '''
      [6.256745, 8.754455, 9.454845, 13.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('1.0003'), Decimal('-1.2761'), Decimal('-1.0005'), Decimal('1.4675'))
   ```

   vi. (sm) **cot(__a, __pr)**: To get the cot for a list of numbers

   ```python
   >>> nums = gtrig.cot([6.256745, 8.754455, 9.454845, 13.3874258], 4)
   '''
      [6.256745, 8.754455, 9.454845, 13.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('-37.8122'), Decimal('-1.2614'), Decimal('33.24810'), Decimal('0.9311'))
   ```

   vii. (sm) **asine(__a, __pr)**: To get the sine<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.asine([0.256745, 0.754455, 0.454845, 0.3874258], 4)
   '''
      [0.256745, 0.754455, 0.454845, 0.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.2596'), Decimal('0.8548'), Decimal('0.4722'), Decimal('0.3978'))
   ```

   viii. (sm) **acosine(__a, __pr)**: To  get the cosine<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.acosine([0.256745, 0.754455, 0.454845, 0.3874258], 4)
   '''
      [0.256745, 0.754455, 0.454845, 0.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('1.3111'), Decimal('0.71510'), Decimal('1.0986'), Decimal('1.17210'))
   ```

   ix. (sm) **atan(__a, __pr)**: To get the tan<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.atan([1.256745, 2.754455, 3.454845, 4.3874258], 4)
   '''
      [1.256745, 2.754455, 3.454845, 4.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('3.0788'), Decimal('-0.4077'), Decimal('0.3239'), Decimal('2.9682'))
   ```

   x. (sm) **acosec(__a, __pr)**: To get the cosec<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.acosec([1.256745, 2.754455, 3.454845, 4.3874258], 4)
   '''
      [1.256745, 2.754455, 3.454845, 4.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.9202'), Decimal('0.3715'), Decimal('0.2937'), Decimal('0.2299'))
   ```

   xi. (sm) **asec(__a, __pr)**: To get the sec<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.asec([1.256745, 2.754455, 3.454845, 4.3874258], 4)
   '''
      [1.256745, 2.754455, 3.454845, 4.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.6506'), Decimal('1.1993'), Decimal('1.2771'), Decimal('1.3409'))
   ```

   xii. (sm) **acot(__a, __pr)**: To get the cot<sup>-1</sup> for a list of numbers

   ```python
   >>> nums = gtrig.acot([1.256745, 2.754455, 3.454845, 4.3874258], 4)
   '''
      [1.256745, 2.754455, 3.454845, 4.3874258] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.6721'), Decimal('0.3483'), Decimal('0.2817'), Decimal('0.2241'))
   ```

   </p>
</details>
   </p>
</details>

<details>
   <summary>Hyperbolic Operations</summary>
   <p>
<details>
   <summary>Primitive Operations</summary>
   <p>

   **(c) htrig**: Primitive hyperbolic trignometry operations
   
   ```python
   >>> from deciml.deciml import htrig
   ```

   i. (sm) **sinh(__a, __pr)**: To get the sinh for a number

   ```python
   >>> num = htrig.sinh(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('6.3551')
   ```
   ii. (sm) **cosh(__a, __pr)**: To get the cosh for a number

   ```python
   >>> num = htrig.cosh(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('6.4333')
   ```

   iii. (cm) **tanh(__a, __pr)**: To get the tanh for a number

   ```python
   >>> num = htrig.tanh(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('0.9878')
   ```

   iv. (cm) **cosech(__a, __pr)**: To get the cosech for a number

   ```python
   >>> num = htrig.cosech(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('0.1574')
   ```

   v. (cm) **sech(__a, __pr)**: To get the sech for a number

   ```python
   >>> num = htrig.sech(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('0.1554')
   ```

   vi. (cm) **coth(__a, __pr)**: To get the coth for a number

   ```python
   >>> num = htrig.coth(2.5485421, 4)
   '''
      2.5485421 - Number
      4 - The precision
   '''
   >>> num
   Decimal('1.0123')
   ```

   </p>
</details>
<details>
   <summary>Grouped Operations</summary>
   <p>

   **(c) ghtrig**: Grouped hyperbolic trignometry opeerations
   
   ```python
   >>> from deciml.deciml import ghtrig
   ```

   i. (sm) **sinh(__a, __pr)**: To get the sinh for a list of numbers

   ```python
   >>> nums = ghtrig.sinh([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('1.2144'), Decimal('18.0050'), Decimal('177.8979'), Decimal('225.5253'))
   ```

   ii. (sm) **cosh(__a, __pr)**: To get the cosh for a list of numbers

   ```python
   >>> nums = ghtrig.cosh([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('1.5731'), Decimal('18.0328'), Decimal('177.9007'), Decimal('225.5275'))
   ```

   iii. (sm) **tanh(__a, __pr)**: To get the tanh for a list of numbers

   ```python
   >>> nums = ghtrig.tanh([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.77110'), Decimal('0.9985'), Decimal('0.99910'), Decimal('0.99910'))
   ```

   iv. (sm) **cosech(__a, __pr)**: To get the cosech for a list of numbers

   ```python
   >>> nums = ghtrig.cosech([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.8235'), Decimal('0.055540'), Decimal('0.0056212'), Decimal('0.0044341'))
   ```

   v. (sm) **sech(__a, __pr)**: To get the sech for a list of numbers

   ```python
   >>> nums = ghtrig.sech([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('0.6357'), Decimal('0.055455'), Decimal('0.0056211'), Decimal('0.0044340'))
   ```

   vi. (sm) **coth(__a, __pr)**: To get the coth for a list of numbers

   ```python
   >>> nums = ghtrig.coth([1.0251547, 3.5845677, 5.8743648, 6.1115845], 4)
   '''
      [1.0251547, 3.5845677, 5.8743648, 6.1115845] - List of numbers
      4 - The precision
   '''
   >>> nums
   (Decimal('1.2954'), Decimal('1.0015'), Decimal('1.0000'), Decimal('1.0000'))
   ```

   </p>
</details>
   </p>
</details>

<details>
   <summary>Statistics</summary>
   <p>

   **(c) stat**: For statistical calculations
   
   ```python
   >>> from deciml.deciml import stat
   ```

   i. (sm) **amean(__a, __pr)**: To get the arithmatic mean of a list of numbers

   ```python
   >>> num = stat.amean([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('3.3578')
   ```

   ii. (sm) **gmean(__a, __pr)**: To get the geometric mean of a list of numbers

   ```python
   >>> num = stat.gmean([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('2.8756')
   ```

   iii. (sm) **hmean(__a, __pr)**: To get the harmonic mean of a list of numbers

   ```python
   >>> num = stat.hmean([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('0.4697')
   ```
   
   iv. (sm) **qmean(__a, __pr)**:To get the quadratic mean of a list of numbers
   
   ```python
   >>> num = stat.qmean([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('3.7256')
   ```

   v. (cm) **pvar(__a, __pr)**: To get the population variance of numbers

   ```python
   >>> num = stat.pvar([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('2.6057')
   ```

   vi. (cm) **svar(__a, __pr)**: To get the sample variance of numbers

   ```python
   >>> num = stat.svar([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('3.2572')
   ```

   vii. (cm) **pstd_dev(__a, __pr)**: To get the population standard deviation of numbers

   ```python
   >>> num = stat.pstd_dev([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('1.6142')
   ```

   viii. (cm) **sstd_dev(__a, __pr)**: To get the sample standard deviation of numbers

   ```python
   >>> num = stat.sstd_dev([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('1.8048')
   ```

   ix. (sm) **median(__a, __pr)**: To get the median of a list of numbers

   ```python
   >>> num = stat.median([1, 2.352, 3.242814, 4.65247541, 5.5415], 4)
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   Decimal('2.7974')
   ```

   x. (sm) **mode(__a, __pr)**: To get the mode of a list of numbers

   ```python
   >>> num = stat.mode([1, 2.352, 3.242814, 5.5415, 5.5415, 1, 1, 4.65247541, 5.5415])
   '''
      [1, 2.352, 3.242814, 4.65247541, 5.5415] - List of numbers
      4 - The precision
   '''
   >>> num
   {'values': (1, 5.5415), 'mode': 3}
   ```

   </p>
</details>


