# Tokenize-Credit-Card-Number-With-Flask
Credit Card Tokonizer App.Restful api used to toknize credit card numbers using flask api.
1. [General](#General)
2. [Installation](#Installation)
3. [Usage](#Usage)
4. [Footnote](#footnote)
## General
This is an api that its main goal is to store credit cards and tokenize them after verifying that the card has a valid number.

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
   $ curl -X POST -H "Content-Type: application/json" http://localhost:8081/creditcard -d'{"credit-card":"4716-1923-6816-9803"}'
```
The response is a unique id that represents the credit card token:
```
{"token": "1e6e8ff7-4aec-4877-b52e-282e02c38919"}
```
3. To get the card:

```
   $ curl -X GET http://localhost:8081/creditcard/1e6e8ff7-4aec-4877-b52e-282e02c38919
```
or enter to http://localhost:8081/creditcard/1e6e8ff7-4aec-4877-b52e-282e02c38919 (the number after creidtcard is the specific token you got the one I entered is just an example) to your favorite browser.

4. To change the card:
```
   $ curl -X PUT http://localhost:8081/creditcard/1e6e8ff7-4aec-4877-b52e-282e02c38919 -d'{"credit-card":"4929-2059-4747-5013"}'
```
## Footnote
The credit card entred is checked if it is legal using luhn for the number itself and schema for the structure.
