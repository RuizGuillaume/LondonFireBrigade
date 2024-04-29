# Presentation and Installation

This repository contains the code for our project "London Fire Brigade", developed during our [Data Scientist training](https://datascientest.com/en/data-scientist-course) at [DataScientest](https://datascientest.com/).

The full report on this project is available in "London Fire Brigade - Report.pdf"

The aim of this project is to study London Fire Brigade activity data in order to create a model for predicting fire brigade response times.

This project was developed by the following team :

- Khassawneh Ammar ([GitHub](https://github.com/ammarkh90) / [LinkedIn](https://www.linkedin.com/in/ammar-khassawneh-02268695/))
- Ruiz Guillaume ([GitHub](https://github.com/RuizGuillaume) / [LinkedIn](https://www.linkedin.com/in/ruizguillaume/))

You will need to install the dependencies (in a dedicated environment) :

```
pip install -r requirements.txt
```


# Notebooks

To start, download datasets here : https://data.london.gov.uk/dataset/london-fire-brigade-incident-records and https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records.
Add them to folders 'Datasets\london-fire-brigade-incident-records' and 'Datasets\london-fire-brigade-mobilisation-records' respectivly
Run the data exploration notebook to generate the datasets needed for modeling notebook and the Streamlit application.

# Streamlit App

To run the app (be careful with the paths of the files in the app):

```shell
conda create --name LFB python=3.9
conda activate LFB
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

The app should then be available at [localhost:8501](http://localhost:8501).
