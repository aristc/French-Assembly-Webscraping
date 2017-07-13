# Webscraping - Deputies of the National Assembly of France

This Python script extracts information on the current French deputies from the official National Assembly website (www2.assemblee-nationale.fr)

## List of fields

* Title as "Civilite"
* First Name as "Prénom"
* Last Name as "Nom"
* Group as "Groupe"
* Constituency (Region) as "Département d'élection"
* Constituency (District) as "Circ."
* Standing Committee as "Commission permanente"
* Age Range as "Age"
* Deputy ID Number as "Dep_ID"
* Seat Number in Assembly as "Siege"
* Occupational Category as "Cat SocioPro"

## Output format

* The output file is a UTF-8 encoded csv file named deputes-info.csv".
* The output language is French.

## Datasources

The scripts joins data collected from different web pages.

* Most fields: http://www2.assemblee-nationale.fr/deputes/liste/ages/(vue)/tableau
* Occupation category: http://www2.assemblee-nationale.fr/deputes/liste/cat-sociopro
* Seat number: http://www2.assemblee-nationale.fr/deputes/hemicycle

## Notes

* Python 2.7
* Packages: urllib2, pandas, BeautifulSoup
* Encoding: UTF-8 (French characters)
