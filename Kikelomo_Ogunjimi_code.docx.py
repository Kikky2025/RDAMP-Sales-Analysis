#Perform data quality assessment (missing values, anomalies, duplicates)

import pandas as pd
#read ace_data.csv file and view it
ace_data = r"C:\Users\kikel\Desktop\RDAMP\Ace_dataset.csv"
acedata = pd.read_csv(ace_data, encoding = 'unicode_escape')
print(acedata)

#explore the ace_data info
print(acedata.info())

#find and sum the number of missing values in each column of acedata dataframe
print(acedata.isnull().sum())

#fill the missing values in the dataframe with zero
acedata_full = acedata.fillna(0)
print(acedata_full)

#perform summary statistics on acedata dataframe to see any outlier
print(acedata_full.describe())

#negative value in Sales and Cost Price column, confirm the minimum vaues in each column
print(acedata_full['Sales'].min())
print(acedata_full['Cost Price'].min())

#mask the negative values in the acedata dataframe
import numpy as np
acedata_full['Sales'] = acedata_full['Sales'].mask(acedata_full['Sales'] < 0, np.nan)
acedata_full['Cost Price'] = acedata_full['Cost Price'].mask(acedata_full['Cost Price'] < 0, np.nan)

#fill the masked negative valuesin the acedata dataframe with zero
acedata_full = acedata_full.fillna(0)

#confirm the min Sales and cost price to be replaced by zero
print(acedata_full['Sales'].min())
print(acedata_full['Cost Price'].min())                                                              
                                                                
#drop duplicates in acedata dataframe and view the dataframe, no duplicates found
acedata_full = acedata_full.drop_duplicates()
print(acedata_full)


#Summarize total sales, revenue, and discount rates by region and segment

#add the Revenue column to the acedata dataframe
acedata_full['Revenue'] = acedata_full['Sales'] * acedata_full['Quantity']
print(acedata_full)

#add discount rate column to the dataframe and view
acedata_full['Discount rates'] = (acedata_full['Discount'] / acedata_full['Cost Price']) * 100
print(acedata_full['Discount rates'])

#view the category column
print(acedata['Category'].head())

#split the category column into two columns
acedata_full[['Category', 'Segiments']] = acedata_full['Category'].str.split('-', expand =True, n=1)
print(acedata_full.head())

#view the new Category and Segiment column
print(acedata_full[['Category','Segiments']])

#replace none with empty string in the dataframe
acedata_full = acedata_full.replace([None], [''], regex=True)
print(acedata_full)

#Join Segiments and Sub category columns together to form a new column
acedata_full["Segiment"] = acedata_full["Segiments"] + " " + acedata_full["Sub-Category"]
print(acedata_full)

#view the new column,Segiment
acedata_full['Segiment'] = acedata_full['Segiment'].str.split(expand=True)[0]
print(acedata_full['Segiment'])

#Summary of total sales by region and segiment
print(acedata_full.pivot_table(values= 'Sales', index = 'Region', columns = 'Segiment', margins = True))

#summary of revenue by region and segiment
print(acedata_full.pivot_table(values= 'Revenue', index = 'Region', columns = 'Segiment', margins = True))

#summary of discount rates by region and segiment
print(acedata_full.pivot_table(values= 'Discount rates', index = 'Region', columns = 'Segiment', margins = True))


#Identify top 5 best-selling products and underperforming products by revenue

#top 5 best selling product
best_selling_products = acedata_full.sort_values('Revenue', ascending = False)
print(best_selling_products)
print(best_selling_products[['Segiment', 'Revenue']].head()) #bicycles and outdoor materials are the 5 top best selling products

revenue_by_segiment = acedata_full.pivot_table(values = 'Revenue', index= 'Segiment').reset_index()
print(revenue_by_segiment)

#product with maximum revenue
maxrev = revenue_by_segiment.max()
print(maxrev)

#product with minimum revenue
minrev = revenue_by_segiment.min()
print(minrev)



rev_comp = pd.concat([maxrev, minrev], axis=1)
print(rev_comp)




#5 underperforming products
underperforming_products = acedata_full.sort_values('Revenue', ascending = True)
print(underperforming_products[['Segiment', 'Revenue']].head()) #food produce including fresh food and cannned food are 5 underperforming products


#Provide insights into product categories with highest margins
acedata_full['Profit margin'] = (acedata_full['Revenue'] - acedata_full['Cost Price'])/ acedata_full['Revenue'] * 100

high_margin_products = acedata_full.sort_values('Profit margin', ascending = False)


print(high_margin_products[['Category', 'Profit margin']].head()) #food has highest profit margin at 100%, food is proitable.Increasing marketing on food products (except fresh and canned) will boast overall profit 


#Analyze sales distribution across Order Mode (Online vs In-Store)

# Group and sum sales
sales_by_mode = acedata_full.groupby('Order Mode')['Sales'].sum().reset_index()
print(sales_by_mode)

#plot the horizontal bar chart of sales against Order mode
import matplotlib.pyplot as plt

y = (sales_by_mode['Order Mode'])
x = (sales_by_mode['Sales'])
plt.barh(y, x)
plt.ylabel('Order Mode')
plt.xlabel("Sales") 
plt.title("sales by Order mode")
plt.show()

#view revenue by region
region_rev = acedata_full.pivot_table(values = 'Revenue', index= 'Region').reset_index()
print(region_rev)

#drop regions that contain zero
region_rev = region_rev.loc[region_rev['Region'] != 0]
print(region_rev)

#plot a horizontal bar chart of revenue by region
y = (region_rev['Region'])
x = (region_rev['Revenue'])
plt.barh(y, x)
plt.ylabel('Region')
plt.xlabel("Revenue") 
plt.title("Revenue by Region")
plt.show()

#view category and profit margin colums
print(high_margin_products[['Category', 'Profit margin']])

#drop nan in the dataset and view
print(high_margin_products[['Category', 'Profit margin']].dropna())

#group the mean of profit margin by category
Profit_Cat = high_margin_products.pivot_table(values = 'Profit margin', index= 'Category').reset_index()
print(Profit_Cat)

#drop the first row with missing value - zero
Category_P = Profit_Cat.drop(Profit_Cat.index[0])
print(Category_P)

#plot the horizontal bar chart of category against profit margin
y = (Category_P['Category'])
x = (Category_P['Profit margin'])
plt.barh(y, x)
plt.ylabel('Category')
plt.xlabel("Profit margin") 
plt.title("Profit margin by Category")
plt.show()


