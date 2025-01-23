import pandas as pd
from geopy.distance import geodesic
from datetime import datetime

# 获取当前时间
current_time = datetime.now()
print(current_time)

DISTANCE_THRESHOLD = 500

# 只保留一种单位的数据
df_mp = pd.read_csv("USA/MicroPlastic.csv")
df_mp = df_mp[df_mp["Unit"] == "pieces/m3"]
df_mp.drop(columns=["Unit"], inplace=True)
df_mp["Date"] = pd.to_datetime(df_mp["Date"])
df_mp['Year'] = df_mp['Date'].dt.year
df_mp['Month'] = df_mp['Date'].dt.month
df_mp.drop(columns=["Date"], inplace=True)
df_mp = df_mp.rename(columns={
	"Latitude": "latitude",
	"Longitude": "longitude",
	"Year": "mp_year",
	"Month": "mp_month"
})
df_mp


def is_within_period(row1, row2, period):
	# row1 是出生数据, row2是微塑料数据
	# period的取值为 0 ~ 4. 0对应怀孕前三月，4对应怀孕后三月
	year_diff = row1["birth_year"] - row2["mp_year"]
	month_diff = row1["birth_month"] - row2["mp_month"]
	diff = year_diff * 12 + month_diff
	left = 9 - 3 * period
	right = 11 - 3 * period
	return left <= diff <= right


def is_within_distance(row1, row2, max_distance):
	point1 = (row1["latitude"], row1["longitude"])
	point2 = (row2["latitude"], row2["longitude"])
	return geodesic(point1, point2).km <= max_distance


df1 = pd.read_csv("USA_LBW.csv")
df2 = df_mp


def myCondition(row, row_in_df1, period):
	if is_within_period(row_in_df1, row, period):
		if is_within_distance(row_in_df1, row, DISTANCE_THRESHOLD):
			return True
	return False


global_count = 0

# 计算函数


def myJoin(row, df2, period):
	global global_count
	row_in_df1 = row
	filtered_df2 = df2[df2.apply(myCondition, axis=1, args=(row_in_df1, period))]
	# print(filtered_df2)
	result = filtered_df2["Measurement"].mean()

	global_count += 1
	if global_count % 10 == 0:
		global_count = 0
		print("-", end="")
	return result


# 在 df1 中添加新列，通过 apply 来应用计算函数
for i in range(5):
	print(f">\n开始计算第{i + 1}期数据")
	df1[f'mp{i + 1}'] = df1.apply(lambda row: myJoin(row, df2, i), axis=1)

df1.to_csv("final1_test.csv")

# 获取当前时间
current_time = datetime.now()
print(current_time)