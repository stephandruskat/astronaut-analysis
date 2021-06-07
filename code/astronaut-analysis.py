import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def is_alive(date_of_death):
    if pd.isnull(date_of_death):
        return True
    return False


def died_with_age(row):
    if pd.isnull(row["date_of_death"]):
        return None
    born = row["birthdate"]
    today = row["date_of_death"]
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


plt.style.use("ggplot")
df = pd.read_json("../data/astronauts.json")
df = df.rename(
    index=str,
    columns={
        "astronaut": "astronaut_id",
        "astronautLabel": "name",
        "birthplaceLabel": "birthplace",
        "sex_or_genderLabel": "sex_or_gender"
    }
)

df = df.set_index("astronaut_id")
df = df.dropna(subset=["time_in_space"])
df["time_in_space"] = df["time_in_space"].astype(int)
df["time_in_space"] = pd.to_timedelta(df["time_in_space"], unit="m")
df["time_in_space_D"] = df["time_in_space"].astype("timedelta64[D]")
df["birthdate"] = pd.to_datetime(df["birthdate"])
df["date_of_death"] = pd.to_datetime(df["date_of_death"])
df.sort_values("birthdate", inplace=True)
df["alive"] = df["date_of_death"].apply(is_alive)
df["age"] = df["birthdate"].apply(calculate_age)
df["died_with_age"] = df.apply(died_with_age, axis=1)

# Male humans in space
df_male = df.loc[df["sex_or_gender"] == "male", ["birthdate", "time_in_space", "time_in_space_D"]].copy()
reduced_df = df_male[["birthdate", "time_in_space", "time_in_space_D"]].copy()
reduced_df["accumulated_time_in_minutes"] = reduced_df["time_in_space"].cumsum()
reduced_df["accumulated_time_in_days"] = reduced_df["time_in_space_D"].cumsum()
reduced_df.plot(x="birthdate", y="accumulated_time_in_days")
plt.title("Total time male humans have spend in space")
plt.xlabel("Years")
plt.ylabel("t in days")
fig = plt.gcf()
fig.savefig("male_humans_in_space.png")

# Female humans in space
df_female = df.loc[df["sex_or_gender"] == "female", ["birthdate", "time_in_space", "time_in_space_D"]].copy()
reduced_df = df_female[["birthdate", "time_in_space", "time_in_space_D"]].copy()
reduced_df["accumulated_time_in_minutes"] = reduced_df["time_in_space"].cumsum()
reduced_df["accumulated_time_in_days"] = reduced_df["time_in_space_D"].cumsum()
reduced_df.plot(x="birthdate", y="accumulated_time_in_days")
plt.title("Total time female humans have spend in space")
plt.xlabel("Years")
plt.ylabel("t in days")
fig = plt.gcf()
fig.savefig("female_humans_in_space.png")

# Humans in space
reduced_df = df[["birthdate", "time_in_space", "time_in_space_D"]].copy()
reduced_df["accumulated_time_in_minutes"] = reduced_df["time_in_space"].cumsum()
reduced_df["accumulated_time_in_days"] = reduced_df["time_in_space_D"].cumsum()
reduced_df.plot(x="birthdate", y="accumulated_time_in_days")
plt.title("Total time humans have spend in space")
plt.xlabel("Years")
plt.ylabel("t in days")
fig = plt.gcf()
fig.savefig("humans_in_space.png")

died_df = df.loc[df["alive"] == 0, ["died_with_age"]].copy()
age_df = df.loc[df["alive"] == 1, ["age"]].copy()

# Combined Histogram of dead and alive astronauts
fig, axs = plt.subplots(1, 1)
axs.hist([died_df["died_with_age"], age_df["age"]], bins=70, range=(31, 100), stacked=True)
axs.set_xlabel("Age")
axs.set_ylabel("Number of astronauts")
axs.set_title("Dead vs. Alive astronauts")
fig.savefig("combined_histogram.png")

# Box plots of dead vs alive astronauts
fig, axs = plt.subplots(1, 1)
axs.boxplot([died_df["died_with_age"], age_df["age"]])
axs.set_title("Age distribution; Dead vs. Alive astronauts")
axs.set_xlabel("Category")
plt.setp(axs, xticks=[1, 2], xticklabels=["Dead", "Alive"])
axs.set_ylabel("Age")
fig.savefig("boxplot.png")
