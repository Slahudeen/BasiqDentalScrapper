This is a python notebook.

## How to execute it
We can execute it by using 'https://research.google.com/colaboratory/'. Just a simple signup there and import this '.ipynb' file. At the top left, click on 'Runtime -> Run all' and it will start executing the notebook. All the files would be saved under the folder section at the left column. 

## Or
## We can execute it using Python jupyter notebook
First we have to install python notebook on one's computer.
On MAC, we can install jupyter by this command 
    `brew install jupyter`
Similarly we can find commands for windows and linux.
After installation, open it by
    `jupyter notebook`
            or
    `jupyter notebook BasiqDentalScrapper.ipynb`
This will directly open this notebook in jupyter and one can execute it by clicking 'Run all' at the top.
A complete guide can be found over [here](https://medium.com/@blessedmarcel1/how-to-install-jupyter-notebook-on-mac-using-homebrew-528c39fd530f).

## What is google colab?
Colaboratory, or “Colab” for short, is a product from Google Research. Colab allows anybody to write and execute arbitrary python code through the browser, and is especially well suited to machine learning, data analysis and education. More technically, Colab is a hosted Jupyter notebook service that requires no setup to use, while providing free access to computing resources including GPUs. It is free to use.

## Things that are handled 
1) Due to some reasons if something breaks then by executing the script again it will identify, if the file/files exist or not, previously.
2) If any subcategory has 1 page or more than that.
3) If manufacturuer is missing for some products or not.
4) All the URLs are utf-8 encoded.
