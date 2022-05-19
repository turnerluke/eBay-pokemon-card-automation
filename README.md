# eBay_Pokemon_Card_Automation
A Python program to automate the listing of Pokemon cards to eBay. Utilizes the ebaysdk-python eBay API from timotheus, linked here: https://github.com/timotheus/ebaysdk-python
Download this repository and place in the directory to use.

Listing Pokemon cards to eBay is a repetitve, time consuming, and mindless task. The workflow for doing so is as follows:

(Approximately 15 minutes)
1. Select a card
2. Search the cards name and identifier number on eBay, view previously sold listings
3. Note the successful listing's title and price
4. Take high-quality images of the front and back of the card
5. Load these images onto your computer
6. Orient the images properly
7. Crop the images
8. List the images manually
- Paste the title
- Paste the previously successful price
- Paste a disclaimer about quality (since I am not professionally minting these cards)
- Battle with eBay's UI to properly denote these listings as Pokemon cards

Using this program, the automated workflow is as follows:
(Approximately 3 minutes)
1. Select a card
2. Search the cards name and identifier number on eBay, view previously sold listings
3. Note the successful listing's title and price, paste them in a local excel file
4. Take high-quality images of the front and back of the card
5. Load these images onto your computer, place them in a designated folder
6. Run the local Python program


This use of this program to list hundreds of cards has the potential to save 10s of hours for the user.

![Flowchart](https://github.com/turnerluke/eBay-pokemon-card-automation/blob/main/eBay%20Automation%20Flowchart.png)
