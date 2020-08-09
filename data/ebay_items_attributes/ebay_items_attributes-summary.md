# Dataset
## About the data
This dataset contains information about the attributes (item specifics) of the products available on online eCommerce platform eBay. It contains information about the title, categories and an example image of the product, one sentence extracted from the title or the description of the product, as well as information about item attributes that can be found in this sentence.
Item attributes are information that describe specific features of the product: such as product brand or the color.

## Reference annotations
The reference annotations in this dataset were based on the information aquired directly from the eBay API. However, the quality of the annotations is not perfect, because usually the sellers, who list the item do not put all the information about the product.

## Preprocessing
1. Filtered out all the rows that did not contain any named entity tags
2. A sample of 2000 sentences were selected from the main dataset
3. All rows were shuffled.

## Schema
The schema of the dataset in available in JSON schema in the `ebay_items_attributes-metadata.json` file.

## Source
Dataset was aquired from private database of the https://www.webinterpret.com/.
However all the items in the dataset can aquired using eBay API.

# Annotation task
## Description
The goal of this task was to find and annotated item attributes in the provided sentence. Each sentence always contains at least one named enitity, but may contain more. Also, each named enitity be represented but one or words. Moreover user sees information about the title of the product, path of categories (in which following produt is listed), an example image of the product.

In this we were using a following set of named entity categories:

```
[
    "Pattern",
    "Material",
    "Color",
    "Department",
    "Size",
    "Brand"
]
```

## Feedback
Annotators were randomly splited into groups. One group didn't recieved any sort of the feedback information.
Other, received feedback message after each annotation. The feedback information showed if the correct annotation for this item.

## Test conditions
This dataset was annotated in four conditions:
- `high quality feedback` - all feedback infromation was the same as the reference annotation
- `medium quality feedback` - a slighlty distorted feedback information after each annotation. The reference annotations were modified randomly to achieve value F1 = 0.75.
- `low quality feedback` - a heavily distorted feedback information after each annotation. The reference annotations were modified randomly to achieve value F1 = 0.55
- `control group` - no feedback message displayed

## Feedback distrotion
As described above, the second and the third group of the users received a distored feedback. It means, some of the feedback messages may have been incorrect and contain errors. In both cases we used the same alorigthm for modifing the data, with only difference in probability parameters.

Reference annotations were modified in the following way: 
For each token in each sentence we use two rules:
- if token is not is tagged as a named enitity there is a X percentage chance to remove the tag
    - 25% for the medium quality feedback
    - 40% for the low quality feedback
- there is a X percentage chance that any token (tagged or not) will be modified into a named a random named entity:
    - 5% for the medium quality feedback
    - 10% for the low quality feedback

#  Licence
Dataset is a property of https://www.webinterpret.com/
