"""pylibmql.pyi

Transform MQL input to structured JSON output. 

```
import pylibmql
    
output = pylibmql.parse('SELECT 1 FROM CLASS(MATH 2250): "Must take MATH 2250";')

print(output.version())
'''
0.1.3
'''

print(output.json())
'''
{"version":"0.1.3","requirements":[{"query":{"quantity":{"Single":1},"selector":[{"Class":{"department_id":"MATH","course_number":2250}}]},"description":"Must take MATH 2250","priority":1}]}
'''

print(output.json_pretty()) 
'''
{
  "version": "0.1.3",
  "requirements": [
    {
      "query": {
        "quantity": {
          "Single": 1
        },
        "selector": [
          {
            "Class": {
              "department_id": "MATH",
              "course_number": 2250
            }
          }
        ]
      },
      "description": "Must take MATH 2250",
      "priority": 1
    }
  ]
}
'''
```
"""


class MQL:
    """
    Structured output from an MQL parse
    """

    def version(self) -> str: 
        """Return the version of the parser used to create the structured output."""
        ...
    def json(self) -> str: 
        """Return the structured output as JSON."""
        ...
    def json_pretty(self) -> str: 
        """Return the structured output as pretty-printed JSON."""
        ...


def parse(mql: str) -> MQL:
    """
    Parse MQL input to a structured output.

    This can be formatted as JSON, pretty-printed JSON, or the internal Rust struct with `str`
    """
    ...

