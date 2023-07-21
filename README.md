# Uwuscator - Python Obfuscator (alfa WIP)

## Description

Uwuscator is a powerful obfuscation tool written in Python, designed specifically to seamlessly integrate with PyInstaller. This tool enables developers to protect their Python code by obscuring sensitive information and making it more challenging for reverse engineering attempts.


Before
```python
import datetime
import csv
# Test
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
class Inventory:
    def __init__(self):
        self.products = []
    def add_product(self, product):
        self.products.append(product)
    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)
    def calculate_total_value(self):
        total_value = 0
        for product in self.products:
            total_value += product.price * product.quantity
        return total_value
    def print_inventory(self):
        if len(self.products) == 0:
            print("Inventory is empty.")
        else:
            print("Inventory:")
            for product in self.products:
                print(f"Product: {product.name}\tPrice: ${product.price}\tQuantity: {product.quantity}")
inventory = Inventory()
product1 = Product("Apple", 0.5, 10)
product2 = Product("Banana", 0.3, 15)
product3 = Product("Orange", 0.4, 12)
inventory.add_product(product1)
inventory.add_product(product2)
inventory.add_product(product3)
inventory.print_inventory()
inventory.remove_product(product2)
inventory.print_inventory()
total_value = inventory.calculate_total_value()
print(f"Total value of the inventory: ${total_value}")
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"inventory_{timestamp}.csv"
print(f"Inventory exported to {filename}.")
```
After
![Test 1](https://github.com/OxynDev/uwuscator/blob/720aa235a0c6df475c33bbdd9996afeda1cd078d/temp/1.png)



## Change log
```diff
v1.0.0 ⋮ 21/07/2023
+ released
```

## Todo

- [] Add class rename
- [] Add nuitka support
- [] Add trash code gen


## Features

### String Obfuscation and Encryption

Uwuscator excels at obfuscating strings by subjecting them to encryption and encoding techniques. This process ensures that critical string data remains well-hidden and resistant to straightforward extraction.

### Built-in Function Name Obfuscation

The obfuscator ingeniously changes the names of built-in functions, making it significantly harder for potential attackers to identify and analyze the underlying functionality.

### Custom Function Name Obfuscation

With Uwuscator, developers can rename their functions, thereby thwarting code comprehension efforts and preventing unauthorized access to the original function logic.

### Import Name Obfuscation

Uwuscator goes the extra mile by altering import names, obscuring the relationships between different modules and making the code structure more obscure.

### Variable Name Obfuscation

To enhance protection, Uwuscator skillfully changes the names of variables within the code, hindering the comprehension of data flow and usage.

### Function Compilation

By compiling functions, Uwuscator transforms the source code into bytecode, adding an extra layer of complexity for potential attackers to decipher.

### Code Hiding within Compiled Artifacts

Uwuscator cleverly conceals portions of the original code within the compiled artifacts, making it challenging to retrieve the full source even if the attacker manages to decompile the binary.

## How it Works

Uwuscator leverages Python's abstract syntax tree (AST) module to parse, analyze, and modify the source code. It identifies various code elements, such as strings, functions, imports, and variables, and then applies a combination of encryption, renaming, and compilation techniques to obfuscate the code effectively.

## Getting Started

To get started with Uwuscator, follow these steps:

1. Put your code in input.txt
2. Run obfuscator by `python uwuscator.py` command

## Disclaimer

Please be aware that obfuscation is not an infallible security measure. While Uwuscator significantly increases the complexity of reverse engineering attempts, determined attackers may still find ways to deobfuscate the code. Therefore, consider combining multiple security techniques and best practices for robust code protection.

## Contributions

We welcome contributions to Uwuscator! If you find any issues or have suggestions for improvements, please feel free to create a pull request or submit an issue on the GitHub repository.

## License

Uwuscator is open-source software licensed under the [MIT License](link-to-license).

## Contact

For any inquiries or further information, please contact us at https://discord.gg/8W6BweksGY.

Protect your Python code with Uwuscator today! Happy obfuscating!
