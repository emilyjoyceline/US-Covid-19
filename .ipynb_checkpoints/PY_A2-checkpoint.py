{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "8d427735-c606-40a5-8fbd-27a8a53fd318",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "dca343ce-f9ac-47ce-a429-bbdc4dc93029",
   "metadata": {},
   "outputs": [],
   "source": [
    "covid_cnfrmd = pd.read_csv('covid_confirmed_usafacts.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "56df5c4b-b5d2-487d-8350-710fd31b1e0e",
   "metadata": {},
   "outputs": [],
   "source": [
    "county_pop = pd.read_csv('covid_county_population_usafacts.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "ff13ac47-7e50-4257-85b2-14b15eb1bc64",
   "metadata": {},
   "outputs": [],
   "source": [
    "covid_deaths = pd.read_csv('covid_deaths_usafacts.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6341c75e-30ea-4419-a972-56ddb9f7888f",
   "metadata": {},
   "outputs": [],
   "source": [
    "#pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "42916b94-04ad-4cfc-ae63-f9ed25bc59e9",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6ad938ac-67b9-4790-b318-89b86bb5d3c1",
   "metadata": {},
   "outputs": [],
   "source": [
    "st.title(\"covid 19 dashboard\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "be2b4cbd-db8b-42dc-9cd3-56c1c663045b",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e8c098dc-b385-436b-90f9-85669b49b6a3",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
