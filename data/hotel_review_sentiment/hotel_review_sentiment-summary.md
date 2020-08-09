# Dataset
## About the data
This dataset contains data from the Datafiniti's Business Database. The original dataset includes hotel location, name, rating, review data, title, username, and more. In this task we reduced the data only to the review message text and the review rating score.

## Preprocessing
1. All rows that didn't have the review message or the review rating were filtered out
2. All ratings value were mapped to the nominal cateogries (as described above).
3. For each category value a group of 400 rows were randomly selected.
4. All the result rows suffled.

## Schema
The schema of the dataset in available in JSON schema in the `hotel_review_sentiment-metadata.json` file.

## Source
This dataset was aquired from following link:
https://data.world/datafiniti/hotel-reviews/workspace/project-summary?agentid=datafiniti&datasetid=hotel-reviews

You can access the full dataset on the Datafiniti website:
https://datafiniti.co/products/business-data/

# Annotation task
## Description
The goal of this task was to assign a sentiment score based on a short Hotel review message.
In practice user selects one of following 5 nominal categories for the message:

Available categories:
```
[
    '1 - STRONGLY NEGATIVE',
    '2 - NEGATIVE',
    '3 - NEUTRAL',
    '4 - POSITIVE',
    '5 - STRONGLY POSITIVE'
]
```
Each category represents a different sentiment value adequate to the rating assigned in the review.

## Feedback
Annotators were randomly splited into two groups:
- The first group received a feedback information after each annotation. The feedback information showed if the correct annotation for this item.
- The second group did not received any sort of feedback after the annotation.


## Test conditions
This dataset was annotated in only one condition:
-`high quality feedback` - all feedback infromation was the same as the reference annotation

#  Licence
Dataset is a property of https://datafiniti.co/
