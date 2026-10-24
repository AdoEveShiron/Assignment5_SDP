# Route Planner (Strategy Pattern)

Assignment 5 for ShP-2216 Software Design Patterns.

A small console program that plans a route between two points using three
interchangeable ways of travel: by car, on foot, or by bicycle. The program
asks for the distance and prints the result for all three strategies, so it
is easy to see that the same `Navigator` object works with different
strategies at runtime.

## Project structure

```
src/strategy
├── RouteStrategy.java   Strategy interface
├── CarStrategy.java     concrete strategy
├── WalkStrategy.java    concrete strategy
├── CycleStrategy.java   concrete strategy
├── Navigator.java       Context: holds a strategy and delegates to it
└── Main.java            client: creates strategies and switches them
docs/uml                 UML class diagram (png, svg) and the script that draws it
```

## Build

```
javac --release 17 -d out $(find src -name "*.java")
```

## Run

With the distance as an argument:

```
java -cp out strategy.Main 12
```

Or without arguments, the program asks for it:

```
java -cp out strategy.Main
```

Sample output:

```
Car: 12.0 km, about 0.20 h at 60 km/h
Walk: 12.0 km, about 2.40 h at 5 km/h
Cycle: 12.0 km, about 0.80 h at 15 km/h
```

## How to add a new strategy

1. Create a new class that implements `RouteStrategy` and its `planRoute` method.
2. Use it in `Navigator`, for example `navigator.setStrategy(new BusStrategy())`.

`Navigator` and `RouteStrategy` do not need to change.
