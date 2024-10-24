# Cryptocurrencies API

### Data Ingestion

The objectif of this project was to test a free cryptocurrency api and see what we can do with the limited data.
The first step was to find a crypto API which we were able to find with cryptopaprika and we saw the limits :
    Only one year of data from today to pull from today
    Only 60 calls are allowed per hour and when this number is reached we are blocked

Those limitations gave me some trouble. The second one made me pull the first 50 cryptocoins since extract more could give me some trouble. In order to do so the package `requests` was used to connect to the API and we stored our generated csv in MySQL database. The code below shows the whole process.

###[code](https://github.com/WilliamBak6/WilliamBak6.github.io/blob/first_branch/biwillads/data-ingestion/cryptodata/crytocurrency.py)


### Little exploration

![bitcoin](https://github.com/user-attachments/assets/517957e9-c4c7-4b8c-bbe7-97a0e7112d0c)

We can see that the bitcoin has been pretty unstable the whole year which make it hard to predict. So i generated the stadard deviation of each cryptocurrencies and i made a pourcentage of how far each sd was to their mean.

![btc_distribution](https://github.com/user-attachments/assets/9ed451a7-a547-46b1-a481-d3be867e0b65)

Also the distribution of the bitcoin follow no obvious probability distribution. 
After i calculate the different standard deviation, i selected the coins with the less gap between the sd and the mean. And in those coins i had the trx-trixon and xml coins
![trx_xmr_coins](https://github.com/user-attachments/assets/09c652b5-1d5d-40c8-b262-077de8d7deea)

Trx had a ascending trend through the year and was the price was pretty stable so i tried to forecast with a one year data... Which was not ideal for this task. More details in 


[analyse_cryptocurrency.pdf](https://github.com/user-attachments/files/17509283/analyse_cryptocurrency.pdf)


