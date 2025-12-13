# Injecty

A simple IOC / Dependency injection micro framework for Python.

## What Problem does this try and solve?

Suppose you are tasked with implementing a library which does some task, the specification for which is...

* Long and complicated,
* Possibly unknown.
* May even have contradictory methods depending on the context

For the purpose of your library, you only need to implement part of the specification, but you want to leave it open ended so other libraries / programs can extend what you have done to fit their needs. 

This is what injecty is for!

## Installation

`pip install injecty`

## Example

Take the task of processing lists containing hashes representing 2D shapes and calculate the area of each:

```
[
  {"type": "Circle", radius: 2.0},
  {"type": "Square", length: 3},
  ...
]
```

You create a python library for this task - let's call it shape_area_calculator.

You may start by defining [an abstract base class with a method for calculating area](/example/models/shape_abc.py)

Your [main method for parsing the shapes may look like this](example/main.py)

Next, you might define implementations for [circle](/example/models/circle.py) and [square](example/models/square.py)

With injecty, your code for [a parser may look like this](example/shape_parser.py).
 * Get all implementations of shape
 * Find the one where the name matches the type from the input
 * Initialize the implementation

Injecty finds implementations using config modules. These are any top level module with a name matching
`injecty_config_*` (e.g.: [injecty_config_shapes.py](injecty_config_shapes.py)). Each config module must have:
* A configure method, which is used to register / deregister impls with a context.
* A priority - this determines the order of processing, with higher numbers processed after lower ones, so they can
* override / deregister impls if required

So in this example, the author of a program could add a dependency on this library and define their own processors 
for any other shape (e.g.: [Rectangle](example/models/rectangle.py)) by defining their class and creating a config
module for it (e.g.: [injecty_config_rectangle.py](injecty_config_rectangle.py))

## Ordering of Implementations

Often - the ordering of implementations is important.  Taking the shape example above - suppose the input data did not
contain an explicit `type` attribute. In that case, the program would have to examine the other attributes to determine
if a type is suitable. It is considered to be a circle if the input has a `radius`. If the input has a `length`, it is
a square. If the input has both a `length` and a `height`, it is a rectangle.

In order to make sure that we don't confuse a rectangle for a square, we would need to make sure the rectangle check is
done BEFORE the square check. Remember, the original program has no knowledge of rectangles. So we accomplish this
using implementation ordering. 

You can pass a `sort_key` into any of the injecty `get_impl` methods. If no explicit
sort_key is given, Injecty examines the base class to see if there is an integer priority attribute, and sorts
implementations in descending order. So in this case, simply by giving Rectangle a higher priority than Square, we
would ensure that processing occurs correctly.

## Release Procedure

![status](https://github.com/tofarr/injecty/actions/workflows/quality.yml/badge.svg?branch=main)

The typical process here is:
* Create a PR with changes. Merge these to main (The `Quality` workflows make sure that your PR
  meets the styling, linting, and code coverage standards).
* New releases created in github are automatically uploaded to pypi
