# major-requirement-parser

## Components
- Command Line Interface
- Rust Library
- Python Library (FFI bindings)

### Command Line Usage

```
Usage: mql [OPTIONS] <INPUT>

Arguments:
  <INPUT>
          Path to the input file

Options:
  -o, --output <OUTPUT>
          Path to the output file [Default: output to `stdout`]

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

### Python Instalation

```bash
# minimum version 3.8
pip install pylibmql
```
Ready to use right away.
```py
import pylibmql
```
See walkthrough [here](./demo.ipynb).

## MQL Syntax

```ebnf
File              ::= SpecialStatement ";" { SpecialStatement ";" } ;

SpecialStatement  ::= Statement ":" String [ ":" QuantitySingle ] ;

Statement         ::= "SELECT" Quantity "FROM" Selector ;

Selector          ::= SelectorList | SelectorSingle ;
SelectorList      ::= "[" SelectorSingle { "," SelectorSingle } "]" ;
SelectorSingle    ::= Statement | XYZ ;

XYZ               ::= QueryName "(" QueryArgument { "," QueryArgument } ")" ;
QueryName         ::= "CLASS" | "class" | "PLACEMENT" | "placement"
                    | "TAG" | "tag" | "RANGE" | "range" ;
QueryArgument     ::= String | ClassArgument ;

ClassArgument     ::= DepartmentId ClassId ;
DepartmentId      ::= UppercaseLetter UppercaseLetter UppercaseLetter UppercaseLetter ;
ClassId           ::= Digit Digit Digit Digit ;

Quantity          ::= QuantityMany | QuantitySingle ;
QuantityMany      ::= QuantitySingle "-" QuantitySingle ;
QuantitySingle    ::= Digit { Digit } ;  (* one or more digits; non-empty *)

String            ::= "\"" { "\"\"" | (AnyCharExcept["\"", "\r", "\n"]) } "\"" ;

(* Lexical *)
UppercaseLetter   ::= "A" | ... | "Z" ;
Digit             ::= "0" | ... | "9" ;
```