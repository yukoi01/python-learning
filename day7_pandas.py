import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "city": ["Kathmandu", "Pokhara", "Sarlahi", "Kathmandu"],
    "age": [25, 30, 22, 28],
    "salary": [50000, 60000, 45000, 70000]
}

df = pd.DataFrame(data)
# print(df["salary"])
# print(df[df["salary"] > 50000])
# print(df["salary"].mean())
# print(df["salary"].sum())
# print(df["salary"].max())
# print(df["salary"].describe())
df2 = pd.read_csv("my_expenses.csv")
print(df2)
print(df2["amount"].describe())
print(df2["category"].value_counts())
print(df2.groupby("category")["amount"].sum())
import pandas as pd

df = pd.read_csv("my_expenses.csv")

df["tax"] = (df["amount"] * 0.13).round(2)
df["total"] = df["amount"] + df["tax"]

print(df)
# df_sorted = df.sort_values("amount")
df_sorted = df.sort_values("amount", ascending=False)
print(df_sorted)
df.to_csv("expenses_with_tax.csv", index=False)
print("saved!")
import numpy as np

df = pd.read_csv("my_expenses.csv")
print(df["amount"].isnull())
# df = df.dropna()
# print(df)
df = df.fillna(0)
print(df)