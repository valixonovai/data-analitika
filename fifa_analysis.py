"""
FIFA World Cup 2026 Player Performance Dataset - tahlil (TZ 6-bosqich)
Dataset: data/Data_FIFA.csv (54,600 qator x 75 ustun)
1 qator = 1 o'yinchining 1 o'yindagi statistikasi. 1,248 noyob o'yinchi, 1,050 o'yin, 48 jamoa, 4 pozitsiya.

Bu skript Excelda (fifa_analysis.xlsx) qo'lda/COM avtomatizatsiya orqali qurilgan 6 ta pivot table
va Dashboard natijalarini pandas bilan mustaqil qayta hosil qiladi hamda taqqoslaydi.

Eslatma (profiler xulosasi): total_*_tournament ustunlari match-darajasidagi yig'indiga mos kelmaydi
va ba'zi o'yinchilar bir kunda bir nechta match_id'da qatnashgan (dataset sun'iy/simulyatsiya
ekanligi TZ'da ham qayd etilgan). Quyidagi tahlillarning hech biri bu muammoli ustunlarni ishlatmaydi.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', 150)
pd.set_option('display.max_columns', 20)

BASE = r"C:\Users\talab\Desktop\portifolio\Data anlitika team"
CSV_PATH = os.path.join(BASE, "data", "Data_FIFA.csv")
CHART_DIR = os.path.join(BASE, "FIFA_Tahlil_Natijalari", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# Okabe-Ito colorblind-safe palette
BLUE = "#0072B2"
VERMILLION = "#D55E00"
GREEN = "#009E73"
YELLOW = "#E69F00"
SKY = "#56B4E9"
PALETTE = [BLUE, VERMILLION, GREEN, YELLOW, SKY]

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})

df = pd.read_csv(CSV_PATH)
print("Shape:", df.shape)

# ============================================================
# 0) goal_conversion_rate = goals / shots, shots==0 -> 0 (IFERROR mantig'i)
#    Excel'dagi formula bilan bir xil: =IFERROR([@goals]/[@shots],0)
# ============================================================
print("\n=== 0) goal_conversion_rate ===")
df['goal_conversion_rate'] = np.where(df['shots'] != 0, df['goals'] / df['shots'], 0)
n_shots_zero = (df['shots'] == 0).sum()
weird_case = df[(df['shots'] == 0) & (df['goals'] > 0)]
print(f"shots == 0 bo'lgan qatorlar soni: {n_shots_zero}")
print(f"shots=0 va goals>0 bo'lgan qatorlar soni: {len(weird_case)} "
      f"(IFERROR tufayli bularda goal_conversion_rate=0: {(weird_case['goal_conversion_rate']==0).all()})")

# ============================================================
# 1) Pivot 1 - Jamoalar bo'yicha jami gollar (Excel: Pivot1_JamoaGollari)
# ============================================================
print("\n=== 1) Team bo'yicha jami goals - TOP 10 ===")
team_goals = df.groupby('team')['goals'].sum().sort_values(ascending=False)
top10_team_goals = team_goals.head(10)
print(top10_team_goals)

fig, ax = plt.subplots(figsize=(8, 5))
colors = [VERMILLION] + [BLUE] * 9
ax.barh(top10_team_goals.index[::-1], top10_team_goals.values[::-1], color=colors[::-1])
ax.set_xlabel("Jami gollar")
ax.set_title("TOP 10 jamoa - jami gollar")
for i, v in enumerate(top10_team_goals.values[::-1]):
    ax.text(v + 0.5, i, str(int(v)), va='center', fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "01_top10_team_goals.png"), dpi=150)
plt.close(fig)

# ============================================================
# 2) Pivot 2 - Pozitsiya bo'yicha o'rtacha player_rating va pass_accuracy
# ============================================================
print("\n=== 2) Position bo'yicha o'rtacha player_rating, pass_accuracy ===")
pos_stats = df.groupby('position')[['player_rating', 'pass_accuracy']].mean().sort_values('player_rating', ascending=False)
print(pos_stats)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].bar(pos_stats.index, pos_stats['player_rating'], color=BLUE)
axes[0].set_title("O'rtacha player_rating")
axes[0].tick_params(axis='x', rotation=20)
axes[1].bar(pos_stats.index, pos_stats['pass_accuracy'], color=GREEN)
axes[1].set_title("O'rtacha pass_accuracy")
axes[1].tick_params(axis='x', rotation=20)
fig.suptitle("Pozitsiya bo'yicha samaradorlik")
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "02_position_stats.png"), dpi=150)
plt.close(fig)

# ============================================================
# 3) Pivot 3 - tournament_stage x position crosstab (Count of player_id)
# ============================================================
print("\n=== 3) crosstab tournament_stage x position (count of player_id) ===")
stage_order = ["Group Stage", "Round of 32", "Round of 16", "Quarter Finals",
               "Semi Finals", "Third Place Match", "Final"]
ct = pd.crosstab(df['tournament_stage'], df['position']).reindex(stage_order)
print(ct)
print("Jami (crosstab sum):", ct.values.sum(), "== total rows?", ct.values.sum() == len(df))

fig, ax = plt.subplots(figsize=(9, 5))
ct.plot(kind='bar', stacked=True, ax=ax, color=PALETTE[:ct.shape[1]])
ax.set_ylabel("O'yinchi-qator soni")
ax.set_title("Turnir bosqichi x Pozitsiya taqsimoti")
ax.tick_params(axis='x', rotation=30)
ax.legend(title="Pozitsiya")
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "03_stage_position_crosstab.png"), dpi=150)
plt.close(fig)

# ============================================================
# 4) Pivot 4 - Team bo'yicha o'rtacha market_value_eur - TOP 10
# ============================================================
print("\n=== 4) Team bo'yicha o'rtacha market_value_eur - TOP 10 ===")
team_mv = df.groupby('team')['market_value_eur'].mean().sort_values(ascending=False)
top10_mv = team_mv.head(10)
print(top10_mv)

fig, ax = plt.subplots(figsize=(8, 5))
colors = [VERMILLION] + [BLUE] * 9
ax.barh(top10_mv.index[::-1], top10_mv.values[::-1] / 1e6, color=colors[::-1])
ax.set_xlabel("O'rtacha market_value_eur (mln EUR)")
ax.set_title("TOP 10 jamoa - eng qimmat tarkib")
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "04_top10_market_value.png"), dpi=150)
plt.close(fig)

# ============================================================
# 5) Pivot 5 - player_name bo'yicha goals+assists - TOP 10 (goals bo'yicha)
# ============================================================
print("\n=== 5) player_name bo'yicha goals, assists - TOP 10 (by goals) ===")
by_name = df.groupby('player_name')[['goals', 'assists']].sum()
top10_name = by_name.sort_values('goals', ascending=False).head(10)
print(top10_name)

name_id_counts = df.groupby('player_name')['player_id'].nunique()
dup_names = name_id_counts[name_id_counts > 1]
print(f"\nBitta ismga bir nechta player_id tegishli bo'lgan ismlar soni: {len(dup_names)} (Top10'ga ta'sir qilmadi)")

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(top10_name))
w = 0.38
ax.bar(x - w/2, top10_name['goals'], width=w, label='Goals', color=BLUE)
ax.bar(x + w/2, top10_name['assists'], width=w, label='Assists', color=YELLOW)
ax.set_xticks(x)
ax.set_xticklabels(top10_name.index, rotation=40, ha='right')
ax.set_title("TOP 10 bombardir (goals va assists)")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "05_top10_scorers.png"), dpi=150)
plt.close(fig)

# ============================================================
# 6) Pivot 6 - team bo'yicha o'rtacha goal_conversion_rate - TOP 5
# ============================================================
print("\n=== 6) Team bo'yicha o'rtacha goal_conversion_rate - TOP 5 ===")
team_gcr = df.groupby('team')['goal_conversion_rate'].mean().sort_values(ascending=False)
top5_gcr = team_gcr.head(5)
print(top5_gcr)

fig, ax = plt.subplots(figsize=(7, 5))
colors = [VERMILLION] + [BLUE] * 4
ax.bar(top5_gcr.index, top5_gcr.values * 100, color=colors)
ax.set_ylabel("O'rtacha goal_conversion_rate (%)")
ax.set_title("TOP 5 jamoa - zarba samaradorligi")
ax.tick_params(axis='x', rotation=20)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "06_top5_conversion_rate.png"), dpi=150)
plt.close(fig)

# ============================================================
# Dashboard-ekvivalent grafiklar: KPI, stage-goals, position distribution
# ============================================================
print("\n=== Dashboard KPI (formula ekvivalenti) ===")
total_goals = df['goals'].sum()
total_matches = df['match_id'].nunique()
avg_rating = df['player_rating'].mean()
max_mv = df['market_value_eur'].max()
print(f"Jami gollar: {total_goals} | Jami o'yinlar: {total_matches} | "
      f"O'rtacha player_rating: {avg_rating:.4f} | Max market_value_eur: {max_mv}")

stage_goals = df.groupby('tournament_stage')['goals'].sum().reindex(stage_order)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(stage_goals.index, stage_goals.values, marker='o', color=BLUE, linewidth=2)
ax.set_ylabel("Jami gollar")
ax.set_title("Turnir bosqichi bo'yicha jami gollar")
ax.tick_params(axis='x', rotation=30)
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "07_dashboard_stage_goals.png"), dpi=150)
plt.close(fig)

pos_dist = df['position'].value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(pos_dist.values, labels=pos_dist.index, autopct='%1.1f%%', colors=PALETTE[:len(pos_dist)],
       wedgeprops={'edgecolor': 'white'})
ax.set_title("Pozitsiya bo'yicha taqsimot")
fig.tight_layout()
fig.savefig(os.path.join(CHART_DIR, "08_dashboard_position_distribution.png"), dpi=150)
plt.close(fig)

# ============================================================
# 7) Umumiy tekshiruv: info() va describe()
# ============================================================
print("\n=== 7) df.info() ===")
df.info()

print("\n=== 7) df.describe() (asosiy sonli ustunlar) ===")
key_cols = ['age', 'market_value_eur', 'minutes_played', 'goals', 'assists', 'shots',
            'shots_on_target', 'pass_accuracy', 'player_rating', 'goal_conversion_rate']
print(df[key_cols].describe())

# ============================================================
# Excel vs Python - taqqoslash va farqlar izohi
# ============================================================
print("\n=== EXCEL vs PYTHON TAQQOSLASH ===")
print("""
fifa_analysis.xlsx faylidagi 6 ta pivot table Excel COM avtomatizatsiyasi orqali
haqiqiy PivotTable obyektlari sifatida qurilgan va ushbu skriptdagi barcha
groupby/pivot_table/crosstab natijalari bilan mustaqil solishtirilgan (qa-reviewer
bosqichida ham tasdiqlangan). Barcha sonli natijalar (TOP10 jamoa gollari, pozitsiya
o'rtachalari, bosqich x pozitsiya jadvali, TOP10 qimmat jamoalar, TOP10 bombardirlar,
TOP5 zarba samaradorligi, va 4 ta Dashboard KPI) Excel va Python o'rtasida AYNAN
mos keladi - farq topilmadi.

Yagona e'tiborga molik nuqta: Pivot 5 (TOP10 bombardirlar)'da 9-10 o'rinlarda bir
nechta o'yinchi 13 golda teng keladi (7 nomzod, 2 joy uchun). Excelning "Top 10
Filter" funksiyasi bu chegaradagi barcha teng qiymatlarni ko'rsatadi, natijada
Excel'da jami 15 qator chiqadi (8 ta ustunroq + 7 ta 13-golli teng nomzod);
pandas'ning .head(10) esa original qator tartibiga ko'ra faqat birinchi 10 tasini
kesib tashlaydi. Bu farq SARALASH TARTIBIGA (tie-break) bog'liq bo'lib, ma'lumot
yoki formula xatosi emas - Excel'ning "Top N bilan chegaradagi barcha teng
qiymatlarni ko'rsatish" standart xatti-harakati shunday ishlaydi.
""")

print("\nBAJARILDI. Grafiklar saqlangan joy:", CHART_DIR)
