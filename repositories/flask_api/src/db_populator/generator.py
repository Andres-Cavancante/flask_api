import json
from secrets import choice
from uuid import uuid4
from datetime import datetime, timedelta
from faker import Faker
import random

class Generator:
    def __init__(self):
        self.fake = Faker("pt_BR")
        Faker.seed(42)
        self.taxonomy = {
            "campaign": "{campaign_name}_{free_text}_{product_category}_{objective}_{country}",
            "ad_set": "{audience}_{free_text}_{journey_stage}_{placement}_{device}",
            "ad": "{creative_name}_{free_text}_{creative_type}_{creative_dimension}"
        }
        self.client_ids = self.__generate_client_ids()
        with open("src/db_populator/taxonomy.json", 'r') as file:
            self.taxonomy_fields = json.load(file)

    def __generate_client_ids(self):
        client_ids = {}

        for _ in range(2):
            client_id = f"5{self.fake.unique.random_int(min=10000, max=99999)}40"
            client_secret = str(uuid4())+str(uuid4())
            client_ids[client_id] = {
                "client_secret": client_secret,
                "refresh_token": str(uuid4()),
                "user_id": ":".join([client_id, client_secret])
            }
        return client_ids

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

        date_start = self.fake.date_between(initial_date, today_date)

        three_months_later = date_start + timedelta(days=90)

        if three_months_later <= today_date:
            date_end = self.fake.date_between(three_months_later, today_date)
        else:
            date_end = today_date

        return date_start, date_end

    def chose_taxonomy(self, key: str=None):
        random_info = {}
        for item, value_list in self.taxonomy_fields.items():
            random_info[item] = choice(value_list)
        return random_info[key] if key else random_info

    def format_infos(self, taxonomy, free_text, date_start="", date_end=""):
        rand_infos = self.chose_taxonomy()
        return taxonomy.format(
            campaign_name=f"campaign-number-{self.fake.unique.random_int(min=1000, max=9999)}",
            product_category=rand_infos["product_category"],
            free_text=free_text,
            creative_name="-".join(self.fake.words(random.randint(3,7))),
            journey_stage=rand_infos["journey_stage"],
            objective=rand_infos["objective"],
            country=rand_infos["country"],
            audience=rand_infos["audience"],
            placement=rand_infos["placement"],
            device=rand_infos["device"],
            channel=rand_infos["channel"],
            platform=rand_infos["platform"],
            creative_type=rand_infos["creative_type"],
            creative_dimension=rand_infos["creative_dimension"],
            date_start=date_start if not date_start else date_start.strftime("%Y%m%d"),
            date_end=date_end if not date_end else date_end.strftime("%Y%m%d")
        )

    def generate_auth_data(self):
        return [
            (
            client_id,
            infos["client_secret"],
            infos["refresh_token"]
            )
            for client_id, infos in self.client_ids.items()
        ]

    def generate_campaign_data(self, num_campaigns=5, num_adsets=3, num_ads=2, start_date="2022-01-01"):
        data = []

        for client in self.client_ids.values():
            for account in range(4):
                account_id = str(self.fake.unique.random_int(min=80000000, max=89999999))
                account_name = "-".join(self.fake.words(2))

                for campaign_num in range(1, num_campaigns + 1):
                    date_start, date_end = self.__generate_campaign_dates()
                    free_text = "-".join(self.fake.words(random.randint(3,7)))
                    campaign_name = self.format_infos(self.taxonomy["campaign"], free_text, date_start, date_end)
                    campaign_id = str(self.fake.unique.random_int(min=70000000, max=79999999))

                    for adset_num in range(1, num_adsets + 1):
                        adset_name = self.format_infos(self.taxonomy["ad_set"], free_text)
                        adset_id = str(self.fake.unique.random_int(min=10000, max=99999))

                        for ad_num in range(1, num_ads + 1):
                            ad_name = self.format_infos(self.taxonomy["ad"], free_text)
                            ad_id = str(self.fake.unique.random_int(min=100000, max=999999))

                            for date in self.__get_all_dates_between(date_start, date_end):
                                impressions = random.randint(1000, 10000)
                                clicks = random.randint(100, impressions)
                                cost = round(random.uniform(50, 500), 2)
                                revenue = round(random.uniform(100, 500), 2)

                                data.append((
                                    client["user_id"],
                                    date.strftime("%Y-%m-%d"),
                                    account_id,
                                    account_name,
                                    campaign_name,
                                    campaign_id,
                                    adset_name,
                                    adset_id,
                                    ad_name,
                                    ad_id,
                                    clicks,
                                    cost,
                                    impressions,
                                    revenue
                                ))
        return data
