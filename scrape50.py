from scrapers import LookFantastic, HouseOfFraser, CultBeauty, BeautyBay

# create instances of each class and run methods to scrape products
# lf = LookFantastic()
# lf.get_all_brands()
# lf.loop_through_categories()
# lf.clean_all_products()
#lf.write_to_csv(lf.brand_data)
# lf.write_brands_to_sql()

# hof = HouseOfFraser()
# hof.loop_through_categories()
# hof.clean_all_products()
# hof.write_to_csv()

bb = BeautyBay()
bb.get_all_brands()