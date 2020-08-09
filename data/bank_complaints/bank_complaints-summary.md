# Dataset
## About the data
The Consumer Complaint Database is a collection of complaints about consumer financial products and services that we sent to companies for response. The original dataset contains a number of fields with information of the company serving the product as well as more detailed information about the financial product itself. In this dataset we reduced the data just to the complaint message and the product category value.

## Preprocessing
1. All rows with too short or to long complaint message was filtered out:
    - the minimal accepted length of the message was 30 characters
    - the maximal accepted length was 250 characters
2. To make the task more suitable for the crowdsourcing task, the we have selected data only for five, manually selected product:
```
[
    'Debt collection',
    'Mortgage',
    'Credit reporting',
    'Credit card',
    'Bank account or service'
]
```
3. Removed all rows where message contained blacklisted words, which would make annotation obvious (words that appears in the category name). Blacklist contained following words:
```
BLACKLIST_WORDS = [
    'mortgage', 'card', 'collect', 'account', 'report', 'debt', 'service'
]
```
4. For each category value a group of 400 rows were randomly selected.
5. All the result rows suffled.

## Schema
The schema of the dataset in available in JSON schema in the `bank_complaints-metadata.json` file.

## Source
This dataset was aquired from following link:
https://www.consumerfinance.gov/data-research/consumer-complaints/

# Annotation task
## Description
The goal of this task was to read the customer complaint message and decide to which of 5 financial products the message is related to.

## Feedback
Annotators were randomly splited into groups. One group didn't recieved any sort of the feedback information.
Other, received feedback message after each annotation. The feedback information showed if the correct annotation for this item.

## Test conditions
This dataset was annotated in two conditions:
- `high quality feedback` - all feedback infromation was the same as the reference annotation
- `control group` - no feedback message displayed

#  Licence
Public Domain
