# built-in imports
import csv
from datetime import datetime
# project imports
import oilprices
import config


def heat_fuel_usage(filename,
                    fiscal_year: int):
        
    fiscal_year = str(fiscal_year)
    with open(filename, newline='') as f:
        data = csv.DictReader(f)
        # data = json.load(f)

        total_spent = 0
        total_oil = 0
        diff = []
        dates = []
        for row in data:
            if row['WinterYear'] != fiscal_year:
                continue
            total_spent += float(row["Total"])
            total_oil += float(row["Gallons"])
            dates.append(datetime.strptime(row["Date"], "%Y-%m-%d").date())
    
    last_fill = dates[-1]
    if len(dates) == 1:
        print(f"\nWinter {fiscal_year} Heating Report")
        print("------------------------------------")    
        print()
        print(f"1 Fill-up: {total_oil} gallons, ${total_spent}")
        return

    dates_diff = [b - a for a, b in (zip(dates, dates[1:]))]
    days_diff = [x.days for x in dates_diff]
    tot_days = sum(days_diff)
    avg_days = tot_days / len(days_diff)
    days_since_datediff = datetime.today().date() - last_fill
    days_since = days_since_datediff.days
    spd = total_spent / tot_days
    opd = total_oil / tot_days


    print(f"\nWinter {fiscal_year} Heating Report")
    print("------------------------------------")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Total Oil Bought: {total_oil:.2f} gal")
    print()
    print(f"Total Span of Oil Purchases: {tot_days} days")
    print(f"Heating cost per day: ${spd:.2f}")
    print(f"Heating oil used per day: {opd:.2f} gal")
    print()
    if days_since > (avg_days - 5):
        print(f"May need to fill up soon.")
    print(f"It has been {days_since} days since last fill ({last_fill.strftime('%b %d %Y')})")
    print(f"Average time between fills is {avg_days:.1f} days")


if __name__ == "__main__":
    heat_fuel_usage(config.HEATFUELFILE, 2018)
    # oilprice = oilprices.curOilPrice()
    # print(f"Current price of oil: ${oilprice:.2f} (${(oilprice * 150):.2f} for 150 gal)")
