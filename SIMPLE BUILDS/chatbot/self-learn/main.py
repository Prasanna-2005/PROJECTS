from chatbot import get_response, bot_name
import pandas as pd
from intents_generator_from_intent import df as product_df
cats = ['lightning','electronics', 'clothing','household','footwear','watches', 'computer accessories','pet supplies', 'grocery']
def main():
    # Sample dataframe for product information
   

    print(f"{bot_name}: Hi! I'm here to chat with you. Type 'exit' to end the chat.")

    while True:
        user_input = input("You     : ").strip()
        if user_input.lower() == 'exit':
            print(f"{bot_name}: Goodbye! Have a great day!")
            break

        if not user_input:
            print(f"{bot_name}      : Please enter a message.")
            continue

        words = user_input.lower().split()
        matched = None
      

        for word in words:
            if(len(word) >= 4):
                match = product_df[product_df['Product Name'].str.contains(word, case=False, na=False)]
                if not match.empty:
                    matched = match.iloc[0]
               
                    break


        if matched is not None:
            product_name = matched['Product Name']
            price = matched['Price']
            discount = matched['Discount']
            ends_in = matched['Ends In']
            rate = matched['Ratings']
            print(f"{bot_name}   : {product_name} is available at {discount}% with {price} until {ends_in} days with rating of {rate}.")
      
        
        else:
            response = get_response(user_input)
            print(f"{bot_name}: {response}")

main()
