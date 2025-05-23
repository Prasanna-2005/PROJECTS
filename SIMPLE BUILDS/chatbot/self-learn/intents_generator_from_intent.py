import pandas as pd
import json


def generate_intents(df):
    intents = [
        {
            "tag": "Products",
            "patterns": [
                "What products do you have?",
                "Can you show me your product list?",
                "What items are available?",
                "What are you selling?",
                "Tell me about your products",
                "What's in your inventory?",
                "Show me what you offer",
                "Could you display your current merchandise?",
                "Provide an overview of your product range",
                "I'm interested in browsing your catalog",
                "What merchandise are currently in stock?",
                "Give me a rundown of your product lineup",
                "What selection do you currently have?",
                "I'd like to see your full product inventory",
                "What collection are you offering right now?"
            ],
            "responses": [
                f"We have {len(df)} amazing products across various categories. Would you like to explore them?",
                f"Our extensive catalog features {len(df)} unique items spanning {df['Category'].nunique()} categories. Some standout products include {', '.join(df['Product Name'][:3])}.",
            ]
        },
        {
            "tag": "BestPrice",
            "patterns": [
                "Which product has the lowest price?",
                "What's the cheapest item?",
                "I want the most affordable product",
                "Show me the best-priced item",
                "What can I buy for the least money?",
                "Lowest price product",
                "Budget-friendly options",
                "What's your most economical offering?",
                "I'm looking for the most wallet-friendly product",
                "Which item provides the best value for money?",
                "Can you recommend something at the lowest price point?",
                "What's the most cost-effective item in your inventory?",
                "Show me the most budget-conscious option",
                "I need the most inexpensive product available",
                "What can I purchase without breaking the bank?"
            ],
            "responses": [
                f"Our 3 most affordable products are: {', '.join(df.nsmallest(3, 'Price')['Product Name'])}. Prices start at ${df['Price'].min():.2f}.",
                f"Looking to save? Check out {', '.join(df.nsmallest(3, 'Price')['Product Name'])}. These are our top budget-friendly options!"
            ]
        },
        {
            "tag": "MaxDiscount",
            "patterns": [
                "What has the biggest discount?",
                "Which product is most discounted?",
                "Highest discount available",
                "Show me the best deal",
                "Maximum discount item",
                "Where can I save the most?",
                "Best bargain",
                "Which product offers the most significant price reduction?",
                "I'm searching for the most massive markdown",
                "What item has the steepest discount?",
                "Show me the most dramatically reduced product",
                "Where can I find the most substantial savings?",
                "Which product provides the most impressive price cut?",
                "I want the deal with the maximum percentage off",
                "What's your most heavily discounted item?"
            ],
            "responses": [
                f"Our top 3 discounted products are: {', '.join(df.nlargest(3, 'Discount')['Product Name'])}. Discounts go up to {df['Discount'].max()}% !",
                f"The biggest savings are on {', '.join(df.nlargest(3, 'Discount')['Product Name'])}. Don't miss these great deals!"
            ]
        },
        {
            "tag": "Soon_ending",
            "patterns": [
                "Which deals are ending soon?",
                "What promotions are about to expire?",
                "Quick deals running out",
                "Urgent discounts",
                "Limited-time offers",
                "Ending soon sales",
                "Hurry before it's gone",
                "What time-sensitive deals do you have?",
                "Which promotions are about to close?",
                "I want to catch expiring offers",
                "Show me deals on the verge of ending",
                "What limited-time discounts are available?",
                "Which bargains are disappearing soon?",
                "I'm looking for last-chance deals",
                "What offers are about to vanish?"
            ],
            "responses": [
               f"Time is running out! The {df.loc[df['Ends In'].idxmin(), 'Product Name']} has just {df['Ends In'].min()} days remaining on its incredible discount.",
                f"Don't miss out! Our {df.loc[df['Ends In'].idxmin(), 'Product Name']} deal is about to expire in just {df['Ends In'].min()} days."
           ]
        },
        {
            "tag": "BestRated",
            "patterns": [
                "What are your top-rated products?",
                "Show me the highest-rated items",
                "Which products have the best reviews?",
                "Most recommended products",
                "Top-rated selections",
                "Highly recommended items",
                "Best customer favorites",
                "What products are receiving the most praise?",
                "Which items have the most impressive customer feedback?",
                "Show me the cream of the crop",
                "What are customers raving about?",
                "Which products have the most stellar reputation?",
                "Give me the most acclaimed items",
                "What products are consistently getting 5-star reviews?",
                "Show me the most celebrated merchandise"
            ],
            "responses": [
                f"Our top-rated products are: {', '.join(df.nlargest(3, 'Ratings')['Product Name'])}. The highest rating is {df['Ratings'].max()}!",
                f"Customers love {', '.join(df.nlargest(3, 'Ratings')['Product Name'])}. These products have outstanding feedback!"
            ]
        },
        {
            "tag": "Category",
            "patterns": [
                "What categories do you have?",
                "Show me product categories",
                "List of product types",
                "What kinds of products are available?",
                "Different product categories",
                "What types of items do you sell?",
                "Product category breakdown",
                "Items?",
                "Products?",
                "What merchandise classifications do you offer?",
                "Provide an overview of your product classifications",
                "What variety of product lines are in your inventory?",
                "Show me the different types of merchandise",
                "What product segments do you cover?",
                "Give me a breakdown of your product ecosystem",
                "What range of product categories can I explore?",
                "Describe the breadth of your product portfolio"
            ],
            "responses": [
                f"We offer products across {df['Category'].nunique()} categories. Something for everyone!",
                f"Our diverse product range spans {df['Category'].nunique()} unique categories, including {', '.join(df['Category'].unique()[:3])} and more."
            ]
        }
    ]
    return intents




df = pd.read_csv('items.csv')
new_intents = generate_intents(df)


with open('intent.json', 'r') as file:
    data = json.load(file)
    data['intents'].extend(new_intents)

with open('intents.json', 'w') as f:
    json.dump(data, f, indent=4)
    file.close()

