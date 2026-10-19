from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / "data" / "sales_data.csv", parse_dates=["Order_Date"])
df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]
df["Cost"] = df["Units_Sold"] * df["Unit_Cost"]
df["Profit"] = df["Revenue"] - df["Cost"]

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
metrics = pd.DataFrame({"Metric":["Total Gross Revenue","Total Profit","Profit Margin (%)",
                                  "Average Order Value (AOV)","Units Sold","Number of Orders"],
                        "Value":[round(total_revenue,2),round(total_profit,2),
                                 round(total_profit/total_revenue*100,2) if total_revenue else 0,
                                 round(df["Revenue"].mean(),2),int(df["Units_Sold"].sum()),len(df)]})
metrics.to_csv(OUT/"key_metrics.csv",index=False)
monthly = df.assign(Month=df["Order_Date"].dt.to_period("M").astype(str)).groupby("Month",as_index=False).agg(Revenue=("Revenue","sum"),Profit=("Profit","sum"),Units=("Units_Sold","sum"))
monthly.to_csv(OUT/"monthly_trends.csv",index=False)
category = df.groupby("Category",as_index=False).agg(Revenue=("Revenue","sum"),Profit=("Profit","sum"),Units=("Units_Sold","sum"))
category["Profit_Margin_Percent"] = (category["Profit"]/category["Revenue"]*100).round(2)
category.to_csv(OUT/"category_summary.csv",index=False)
region = df.groupby("Region",as_index=False).agg(Revenue=("Revenue","sum"),Profit=("Profit","sum"))
region.to_csv(OUT/"region_summary.csv",index=False)
for data, x, y, title, filename, kind in [
    (monthly,"Month","Revenue","Monthly Sales Revenue","monthly_revenue.png","line"),
    (category,"Category","Revenue","Revenue by Product Category","category_revenue.png","bar"),
    (region,"Region","Revenue","Revenue by Region","region_revenue.png","bar")]:
    plt.figure(figsize=(9,5))
    if kind == "line": plt.plot(data[x],data[y],marker="o")
    else: plt.bar(data[x],data[y])
    plt.title(title); plt.xlabel(x); plt.ylabel(y)
    plt.xticks(rotation=40,ha="right"); plt.tight_layout()
    plt.savefig(OUT/filename,dpi=200); plt.close()
print("Sales analysis completed. Outputs saved in:", OUT)
print(metrics.to_string(index=False))
