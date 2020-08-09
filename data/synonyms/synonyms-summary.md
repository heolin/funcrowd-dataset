# Dataset
## About the data
The goal of this dataset was to check if users are able to determine if two selected words are synonyms or not. This dataset contains pairs of sentences with one word marked in each of them. Half of the pairs contains words that are synonyms, the other half contains words that are not.

## Preprocessing
1. Randomly select a pair of words that are synonys. Synonyms are selected using Wordnet.
2. Randomly select a pair of words that are not synonyms.
3. For each word find a sentence which contains that words. Sentences were selected from the Gutenberg dataset.
4. Mark the word in each sentence using XML-like tag
5. Randomly select only one sentence for each word.
6. Shuffle all rows

## Schema
The schema of the dataset in available in JSON schema in the `synonyms-metadata.json` file.

## Source
https://web.eecs.umich.edu/~lahiri/gutenberg_dataset.html

# Annotation task
## Description
The goal of this task was to determine if two marked words are synonyms or not. User sees two sentences with one highlighted word in each of them.

## Feedback
Annotators were randomly splited into groups. One group didn't recieved any sort of the feedback information.
Other, received feedback message after each annotation. The feedback information showed if the correct annotation for this item.

## Test conditions
This dataset was annotated in two conditions:
- `high quality feedback` - all feedback infromation was the same as the reference annotation
- `control group` - no feedback message displayed

#  Licence
Public Domain
