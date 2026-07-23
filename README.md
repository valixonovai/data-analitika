# FIFA World Cup 2026 — Player Performance tahlili

## Dataset tavsifi

**Manba**: "FIFA World Cup 2026 Player Performance Dataset" (Kaggle, sun'iy/simulyatsiya qilingan sport analitikasi ma'lumotlari).

- **54,600 qator, 75 ustun** — har bir qator bitta o'yinchining bitta o'yindagi statistikasi
- **1,248 noyob o'yinchi, 1,050 o'yin, 48 jamoa, 4 pozitsiya** (Goalkeeper, Defender, Midfielder, Forward)
- Asosiy ustun toifalari: o'yinchi ma'lumotlari (yosh, bo'y, vazn, bozor qiymati), o'yin ma'lumotlari (sana, stadion, bosqich), hujum/himoya statistikasi, jismoniy ko'rsatkichlar, reyting indekslari
- NULL qiymat va dublikat qatorlar yo'q (COUNTBLANK va player_id+match_id tekshiruvi bilan Excel'da tasdiqlangan)

## Fayllar

| Fayl | Tavsif |
|---|---|
| `fifa_analysis.xlsx` | Tozalangan ma'lumot (Excel Table), Tekshiruv varag'i, 6 ta pivot table, Xulosalar, Dashboard (4 KPI, 3 grafik, 2 slicer, conditional formatting) |
| `fifa_analysis.py` | pandas bilan barcha pivot-ekvivalent hisob-kitoblar, matplotlib grafiklar, Excel vs Python taqqoslash |
| `charts/` | `fifa_analysis.py` tomonidan yaratilgan 8 ta PNG grafik |

## Metodologiya

- Excelda: ma'lumot rasmiy Excel Table'ga aylantirildi, `match_date` — Date, `pass_accuracy`/`save_percentage` — Percentage formatida. `goal_conversion_rate = IFERROR(goals/shots, 0)` haqiqiy formula sifatida qo'shildi.
- 6 ta pivot table barcha bitta umumiy PivotCache'dan yaratilgan (shu sababli 2 ta slicer — team va tournament_stage — barcha 9 ta pivot table/chartga bir vaqtda ulangan).
- Python (pandas) bosqichida barcha 6 pivot natija mustaqil qayta hosil qilingan va Excel natijalari bilan solishtirilgan — **hech qanday sonli farq topilmadi**. Yagona nozik holat: Top-10 filtrlarida chegaraviy teng qiymatlar (tie) borligi sababli ba'zi pivotlarda 10 dan ortiq qator ko'rsatiladi (masalan Pivot5'da 15 qator, 13 golda 7 o'yinchi teng kelgani uchun) — bu Excel'ning standart "Top N bilan barcha teng qiymatlarni ko'rsatish" xatti-harakati, xato emas.
- Barcha hisob-kitoblar ikki bosqichli mustaqil tekshiruvdan (data-analyst dual-method + qa-reviewer) o'tgan.

## Asosiy 5 ta xulosa

1. **Qatar eng ko'p gol urgan jamoa** (95 gol), undan keyin Netherlands (94) va Panama (90) keladi.
2. **Forward pozitsiyasi eng yuqori o'rtacha reytingga ega** (3.88 ball) — Defenderdan (3.79) 0.09, Goalkeeperdan (2.07) 1.82 ballga yuqori. Ammo pas aniqligida Midfielder yetakchi (85.0%).
3. **Saudi Arabia — eng qimmat tarkibga ega jamoa** (o'rtacha ~33.8M EUR bozor qiymati), TOP10'dagi 10-o'rin Iran'dan (~23.9M EUR) sezilarli farq bilan.
4. **Memphis Zerrouki — turnirning eng samarali o'yinchisi** (24 gol + 9 gol uzatish, jami 33), ikkinchi o'rindagi Kasey Hectordan (16 gol) 8 golga ustun.
5. **England zarbani golga eng yaxshi aylantiruvchi jamoa** (o'rtacha 3.27% konversiya), garchi jami gollar bo'yicha TOP10'ga kirmasa ham — bu kamroq, lekin aniqroq zarba qilishni ko'rsatadi.

## Cheklovlar

- Dataset sun'iy/simulyatsiya qilingan bo'lib, ba'zi ustunlar (`total_*_tournament`) match-darajasidagi yig'indiga mos kelmaydi va ba'zi o'yinchilar bir kunda bir nechta o'yinda qatnashgan holatlar mavjud — ushbu tahlilning hech bir bandi bu ustunlardan foydalanmagan.
- `goal_conversion_rate` ustunida ba'zi qatorlarda 100%dan yuqori qiymat (max 3.0) uchraydi (`goals > shots` holatlarida) — bu dataset sun'iyligining yana bir belgisi.
