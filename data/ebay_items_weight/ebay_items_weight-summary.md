# Dataset
## About the data
This dataset contains information about the weights of products available on online eCommerce platform eBay. It contains information about the title, categories and an example image of the product, as well as weight in grams of the item.

## Reference annotations
The reference weights used in the dataset were aquired from the shipping company. The provided weight includes the weight of the package (e.g. a cardboard box). In general the difference between the original weight and the shipping weight can have MAE (mean absolute error) around ~250 grams.

## Preprocessing
1. Filtered out all the rows that had weight larger than 10000 grams.

## Schema
The schema of the dataset in available in JSON schema in the `ebay_items_weight-metadata.json` file.

## Source
Dataset was aquired from private database of the https://www.webinterpret.com/.

# Annotation task
## Description
The goal of this task was to estimate the weight in grams of the displayed product. The product weight was is an integer value in a range from 50 grams to 10000 grams. Moreover, user sees information about the title of the product, path of categories (in which following produt is listed), an example image of the product.

## Feedback
Annotators were randomly splited into groups. One group didn't recieved any sort of the feedback information.
Other, received feedback message after each annotation. The feedback information showed if the correct annotation for this item.

## Test conditions
This dataset was annotated in four conditions:
- `high quality feedback` - all feedback infromation was the same as the reference annotation
- `medium quality feedback` - a slighlty distorted feedback information after each annotation. The reference annotations were modified randomly.
- `low quality feedback` - a heavily distorted feedback information after each annotation. The reference annotations were modified randomly.
- `control group` - no feedback message displayed

## Feedback distrotion
As described above, the second and the third group of the users received a distored feedback. It means, some of the feedback messages may have been incorrect and contain errors. In both cases we used the same alorigthm for modifing the data, with only difference in probability parameters.

The feedback annotations were distored by randomly adding or removing a value from the referene weight:
- for the low quality feedback, the noise was generated usign `normal(0, 1000)` function
- for the low medium feedback, the noise was generated usign `normal(0, 400)` function

#  Licence
Dataset is a property of https://www.webinterpret.com/