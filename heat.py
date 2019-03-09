# built-in imports
import csv
from datetime import datetime
# project imports
import oilprices
import config


def heat_fuel_usage(filename,
                    fiscal_year: str = None,
                    fiscal_year_start = None,
                    fiscal_year_end = None):
    
    if fiscal_year == None:
        temp = datetime.today()
        fyear = temp.year
        if temp > datetime.strptime(f"01-01-{fyear}", "%m-%d-%Y"):
            # after new years, so fiscal year = current_year - 1
            fyear = fyear - 1
        fiscal_year = str(fyear)

    with open(filename, newline='') as f:
        data = csv.DictReader(f)
        # data = json.load(f)

        total_spent = 0
        diff = []
        dates = []
        for row in data:
            if row['WinterYear'] != fiscal_year:
                continue
            total_spent += float(row["Total"])
            dates.append(datetime.strptime(row["Date"], "%Y-%m-%d").date())
    
    last_fill = dates[-1]

    dates_diff = [b - a for a, b in (zip(dates, dates[1:]))]
    days_diff = [x.days for x in dates_diff]

    tot_days = sum(days_diff)
    avg_days = tot_days / len(days_diff)
    days_since_datediff = datetime.today().date() - last_fill
    days_since = days_since_datediff.days
    spd = total_spent / tot_days

    print(f"\nWinter {fiscal_year} Heating Report")
    print("------------------------------------")
    print(f"Total Spent in Fiscal {fiscal_year}: ${total_spent:.2f}")
    print(f"Total Days Between Oil Purchases: {tot_days}")
    print(f"Spending per day: ${spd:.2f}")
    print()
    if days_since > (avg_days - 5):
        print(f"May need to fill up soon.")
    print(f"It has been {days_since} days since last fill ({last_fill.strftime('%b %d %Y')})")
    print(f"Average time between fills is {avg_days:.1f} days")


if __name__ == "__main__":
    heat_fuel_usage(config.HEATFUELFILE)
    oilprice = oilprices.curOilPrice()
    print(f"Current price of oil: ${oilprice:.2f} (${(oilprice * 150):.2f} to fill up)")
