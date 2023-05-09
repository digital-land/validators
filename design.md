# Design Thoughts

Our inputs are
* A datafile 
* Its format (csv only for now)
* Its collection type eg Conserbvation Area

## Errors

1. If the file as a whole is not processable (Fatal)
    1. Zero length
    1. Unparseable as CSV eg quotes in fields etc
    1. Only header fields
1. If the file as a whole has errors that will prevent further processing (Fatal)
    1. Blank `reference` fields. Report the line number and bail.
1. `organisation` field makes sense. Lookup?
1. Mandatory field other than `reference` missing reported per line (Error).


## Possible warnings

1. Field length too short?
1. URL fields
    1. Invalid URL format?
    1.URL field does not give HTTP200? 
1. Date fields are wrong
    1. Entry data is in the future
    1. Start and End dates wrong way round? 
1. Geometry
    1. Outside expeted bounds (LPA, UK)
    1. Invalid, any format.

