# Tokenize-Credit-Card-Number-With-Flask
Credit Card Tokonizer App.Restful api used to toknize credit card numbers using flask api.
1. [Program Structure](https://github.com/elaysason/Weather-Prediction-Project/blob/main/README.md#program-structure)  
2. [Installation](#Installation)
3. [Usage](#Usage)
3. [Footnote](#footnote)

## Program Structure

## Installation
1.Open the terminal

2.Clone the project by:
```
    $ git clone https://github.com/elaysason/Tokenize-Credit-Card-Number-With-Flask.git
```
3.Run the app.py file to start the api by:
```
    $ python3 app.py
```

## Usage
1. open a new terminal instance
2. Insert a new card by 
```
curl -X POST -H "Content-Type: application/json" http://localhost:8081/creditcard -d'{"credit-card":"1234-5678-9101- 1121"}'
```



