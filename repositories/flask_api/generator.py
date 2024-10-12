from datetime import datetime, timedelta
from faker import Faker
import random

class Generator:
    def __init__(self):
        self.fake = Faker("pt_BR")
        Faker.seed(42)

    def __get_all_dates_between(self, date_start, date_end):
        date_range = []
        current_date = date_start
        while current_date <= date_end:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        return date_range

    def __generate_campaign_dates(self):
        # for _ in range(num_active_campaigns):
        #     date_start, date_end = self.generate_campaign_dates()
        #     if date_end == datetime.today():
        #         active_campaigns.append((date_start, date_end))

        initial_date = datetime.fromisoformat("2022-01-01")
        today_date = datetime.today().date()
        
        # Generate the date_start
        date_start = self.fake.date_between(initial_date, today_date)
        
        # Calculate 3 months from date_start
        three_months_later = date_start + timedelta(days=90)
        
        # Set date_end based on the conditions
        if three_months_later <= today_date:
            date_end = self.fake.date_between(three_months_later, today_date)
        else:
            date_end = today_date
        
        return date_start, date_end

    def generate_campaign_data(self, num_campaigns=5, num_adsets=3, num_ads=2, start_date="2022-01-01"):
        data = []
        
        for campaign_num in range(1, num_campaigns + 1):
            date_start, date_end = self.__generate_campaign_dates()
            campaign_name = f"2024_Campaign_{date_start.strftime('%Y%m%d')}_{date_end.strftime('%Y%m%d')}_{campaign_num:02d}"
            campaign_id = self.fake.unique.random_int(min=70000000, max=79999999)
            
            for adset_num in range(1, num_adsets + 1):
                adset_name = f"AdSet_Target_{adset_num:02d}"
                adset_id = self.fake.unique.random_int(min=10000, max=99999)
                
                for ad_num in range(1, num_ads + 1):
                    ad_name = f"Ad_Creative_{ad_num:02d}_Platform"
                    ad_id = self.fake.unique.random_int(min=100000, max=999999)

                    dates = self.__get_all_dates_between(date_start, date_end)
                    for date in dates:
                        impressions = random.randint(1000, 10000)
                        clicks = random.randint(100, impressions)
                        spend = round(random.uniform(50, 500), 2)
                        cost_per_click = round(spend / clicks, 2) if clicks > 0 else 0
                        cost = spend  # spend and cost can be the same in this case

                        data.append({
                            "date": date.strftime("%Y-%m-%d"),
                            "campaign_name": campaign_name,
                            "campaign_id": campaign_id,
                            "adset_name": adset_name,
                            "adset_id": adset_id,
                            "ad_name": ad_name,
                            "ad_id": ad_id,
                            "clicks": clicks,
                            "cost": cost,
                            "spend": spend,
                            "impressions": impressions,
                            "cost_per_click": cost_per_click
                        })
        return data