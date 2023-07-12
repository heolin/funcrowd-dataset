# Funcrowd's Datasets
## About the project
Funcrowd's Dataset is collection of 6 datasets that were created during the research conducted on verifing the influence of feedback information on the quality of the annotations created in the crowdsourcing annotation process.

The collection consists of 6 datasets, each of those contains data of a different kind. Datasets were prepared based on previously annotated data, so they contain both user annotations as well as reference annotations from the original dataset.

Because during this research, we tested how different type of feedback information can affect the quality of gathared data: the dataset also contains information about what feedback was showed to a certain user during the annotation.

## The research
The goal of the research was to verify if providing feedback information during a crowdsourcing annotation task can positively influence the quality of aquired data. In this research we tested a different types of annotations task, to see if the results are task-dependent.

During the research we checked:
- if providing feedback will positively affect the quality of the data
- if feedback with lower quality will still positively affect the quality

All the tests were done using:
- Funcrowd engine - a custom crowdsourcing service built for this task
    - https://github.com/heolin123/funcrowd
    - https://github.com/heolin123/funcrowd-frontend
- Amazon Mechanical Turk - a crowdsourcing marketplace, which provides an interface to distribute a custom task over crowdsourcing workers. 
    - https://www.mturk.com/

# Datasets
## bank_complaints
This database contains data from The Consumer Complaint Database, which is a collection of complaints about consumer financial products and services that we sent to companies for response.

[Read more...](data/bank_complaints/bank_complaints-summary.md)

[See test results...](notebooks/bank_complaints/Analyse%20dataset.ipynb)

## ebay_items_attributes
This dataset contains information about the attributes (item specifics) of the products available on online eCommerce platform eBay.

[Read more...](data/ebay_items_attributes/ebay_items_attributes-summary.md)

[See test results...](notebooks/ebay_items_attributes/Analyse%20dataset.ipynb)

## ebay_items_weight
This dataset contains information about the weights of products available on online eCommerce platform eBay. 

[Read more...](data/ebay_items_weight/ebay_items_weight-summary.md)

[See test results...](notebooks/ebay_items_weight/Analyse%20dataset.ipynb)

## hotel_review_sentiment
This dataset contains Hotel's review message together with ratings values assigned to those messages. The data used in the dataset was extracted from the Datafiniti's Business Database.

[Read more...](data/hotel_review_sentiment/hotel_review_sentiment-summary.md)

[See test results...](notebooks/hotel_review_sentiment/Analyse%20dataset.ipynb)

## ner
This dataset contains annotated sentences with marked named entities. Data used in this dataset comes from the GMB (Groningen Meaning Bank). 

[Read more...](data/ner/ner-summary.md)

[See test results...](notebooks/ner/Analyse%20dataset.ipynb)

## synonyms
The goal of this dataset was to check if users are able to determine if two selected words are synonyms or not. This dataset contains pairs of sentences with one word marked in each of them.

[Read more...](data/synonyms/synonyms-summary.md)

[See test results...](notebooks/synonyms/Analyse%20dataset.ipynb)

## Dataset structure
Within each dataset you will find three files:
- `<name>-dataset.csv` - a file with the data
- `<name>-metadata.json` - a JSON schema of the dataset together with some additional metadata information
- `<name>-summary.md` - a longer information about the dataset, annotation task, feedback information and the licence

# Analysis
This repository contains a set of python notebooks with a basic analysis for verifing the analysis of the influence of the feedback information on the quality of annotated data. In each notebook you will find information about the basic statistics of the dataset as well as the confidence intervals for the influence.

## Installation
To open analysis provided in the notebooks:
1. Install required packages:
```
pip install -r requirements.txt`
```
2. Open jupyter notebook service
```
jupyter notebook
```

3. Open selected notebook and run all the cells
