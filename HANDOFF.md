# HKUGAPS Exercise: handoff notes

This file tells a new AI agent (or a person) everything needed to keep this project going. Last updated 2026-11-11.

## 1. What this is

Practice exercises for Rex's daughter, age 6, in Primary 1 (2026-27 school year) at 港大同學會小學 (HKUGA Primary School), Hong Kong.

- Rex sends a school worksheet (a PDF exported from the school OneNote, or phone screenshots). There is no Microsoft/OneNote connector, so the worksheet always arrives as an upload.
- For each worksheet the agent builds one web page with a **practice set**, a **mock test**, **vocabulary flashcards** and **parent notes**, in Traditional Chinese, in the same style as the school worksheet.
- The page goes on a public website that Rex forwards on WhatsApp.

## 2. Who uses it, and the rules that follow from that

| Fact | Rule |
|---|---|
| She is weak at reading Chinese. | Every section heading and every question has a speaker button that reads it aloud in **Cantonese (廣東話)** or **Mandarin (普通話)**, with a switch at the top. |
| Rex rejected embedded audio. Generated MP3s made the page about 3.5 MB, and the Cantonese was wrong (技 read as 期). | Read-aloud uses the **device's own voices** through the browser Web Speech API (zh-HK for Cantonese, zh-CN/zh-TW for Mandarin). Do **not** embed audio unless Rex asks. |
| Links are shared on WhatsApp, and the recipient uses an **iPhone**. | Each page is a single small self-contained HTML file (about 30-40 KB). Only external resource: Google Fonts. Design for phone width first. |
| **claude.ai links do not open in Hong Kong** ("Claude is only available in certain regions"). | Never send claude.ai artifact links as the deliverable. Publish to GitHub Pages (below). |
| Rex works **only from his phone**, no computer. | The agent does all the publishing. Give Rex direct links. Any GitHub setting change Rex must do himself should come with a direct settings link and short tap-by-tap steps. |
| Rex labels worksheets by term, book and unit. | Show the label on each page and on its home-page card, e.g. **1下A · 單元 1 時間 · WS 1.2**. (1上B Unit 4 = 數數方法, 1下A Unit 1 = 時間, 1下A Unit 2 = 日期.) |

If there's no sound on the iPhone, the usual causes are, in order: the page was opened inside WhatsApp's preview instead of Safari; the phone is on silent mode; the Chinese (Hong Kong) voice isn't downloaded (Settings → Accessibility → Spoken Content → Voices → Chinese).

## 3. Hosting

- **Live site:** https://rexlearnai.github.io/HKUGAPS_Exercise/
- **Repo:** https://github.com/RexLearnAI/HKUGAPS_Exercise (public). GitHub Pages deploys from branch `main`, folder `/` (root). `.nojekyll` is there so files are served as they are.
- Pushing to `main` redeploys automatically in about a minute (workflow "pages build and deployment").
- If a Pages deploy run gets stuck queued or fails, re-running it may also hang. Pushing a new real commit triggers a fresh deploy that works.
- Agents in the Claude cloud sandbox could not open github.io (proxy blocked) or change Pages settings by API. Rex had to save the Pages settings himself.

## 4. Repository layout

```
index.html                 Home page "一年級溫習室": one card per set, grouped by subject
maths/counting-4-1c.html   1上B · WS 4.1c  數數方法: count in 2s, 5s, 10s
maths/ordering-4-2c.html   1上B · WS 4.2c  數數方法: 圈一圈，排一排, < and >
maths/time-1-2.html        1下A · 單元 1 時間 · WS 1.2  時正 and 時半 (drawn SVG clocks)
maths/dates-2-1.html       1下A · 單元 2 日期 · WS 2.1  星期, 昨天/今天/明天/後天
english/typing-pals.html   Typing Pals typing game, listed under "資通訊 ICT" on the home page
HANDOFF.md                 This file
backup/                    Sources and build scripts (copied from the old project's shared folder)
```

Newest set goes at the **top** of its section on the home page. The `code` badge on each card holds the unit label.

## 5. How a worksheet page works

All four maths pages share one design (copy the newest one, `dates-2-1`, as the starting point for a new set).

- **Tabs:** 練習卷 (practice, about 20 min) · 模擬測驗 (mock test, 20-30 min, with marks) · 生字卡 (flashcards) · 家長須知 (parent notes, tips and how to use).
- **Answering on screen:** number boxes, tap-to-cycle boxes (正/半, < / >), dropdowns, tap to circle. Buttons 對答案 / 交卷 grade and show a score, 顯示答案 fills in the answer key. The page also prints cleanly for pencil work.
- **Read-aloud:** `speak()`, `spk()`, `pickVoice()`, `loadVoices()` in the page script. Each `spk(textFn, boxFn)` call adds a speaker button. Bar at the top switches 廣東話/普通話 and slow/normal speed, saved in localStorage. Tables (e.g. the week table in 日期) have a speaker that reads the whole table.
- **Flashcards (生字卡):** a grid of flip cards. Tap to flip: the back shows an emoji, the word and an English gloss, and reads the word aloud in the chosen language. Words come from `backup/p1-maths/src/vocab/vocab.py`.
- **Gotcha:** the CSS must keep `[hidden]{display:none!important}`, or the tabs stop hiding the other sheets (this bug was hit and fixed once).

## 6. Source files and build (backup/)

```
backup/p1-maths/src/*.template.html   Page bodies without the html/head/body skeleton (the real sources)
backup/p1-maths/src/wrap.py           Template -> published page (adds doctype, charset, viewport, head/body)
backup/p1-maths/src/vocab/vocab.py    Flashcard words per set: (word, emoji, English)
backup/p1-maths/src/vocab/add_cards.py Injects the 生字卡 tab + its CSS/JS into a template that lacks it
backup/p1-maths/src/unused-audio/     The rejected offline-TTS (sherpa-onnx MP3) scripts. Kept only for history. Do not use.
backup/p1-maths/early-versions/       Earliest drafts from 2026-11-05 (claude.ai artifact era). History only.
```

`wrap.py` reproduces the four published maths pages byte for byte from their templates (checked 2026-11-11). Editing the published file in `maths/` directly is also fine for small fixes. If you do, apply the same change to the template, or just regenerate the template by deleting the five skeleton lines at the top and the `</head><body>` / `</body></html>` lines.

The original school worksheets Rex uploaded (PDFs and screenshots) are **not** in this public repo, because they are school material. They're in the private backup zip Rex was given with this handoff.

## 7. How to add a new set (checklist)

1. Read the uploaded worksheet: topic, question types, and the unit label (ask Rex for the term/book/unit if it isn't on the sheet).
2. Copy the newest template, e.g. `cp dates-2-1.template.html <topic>-<unit>.template.html`, and rewrite the questions: a practice set in the worksheet's style, and a mock test with the same question types but new numbers/names (the school uses names like 大文, 小喬, 明明). Traditional Chinese.
3. Give every heading and question a speaker (`spk(...)`) with text that reads naturally aloud.
4. Add 15-25 key words from the questions to `vocab/vocab.py` under the new key. If the template doesn't have a 生字卡 tab yet, run `python3 -I vocab/add_cards.py <name>.template.html <name>` from `src/`.
5. Build: `python3 -I wrap.py <name>.template.html ../../../maths/<name>.html`.
6. Test in a phone-width browser (e.g. Playwright at 390 px): every tab switches, grading and 顯示答案 work, no page errors, no sideways scrolling.
7. Add a card at the top of the 數學 section in `index.html` with the unit label badge, title, and "練習卷（約 20 分鐘）＋ 模擬測驗（N 分鐘）＋ 生字卡".
8. Commit and push to `main`. Check the Pages deploy finished, then send Rex the direct page link.

For another subject, create a new folder (e.g. `chinese/`) and a new `<h2>` section on the home page.

## 8. Typing Pals (english/typing-pals.html)

An original creature-collecting typing game (she loves Pokémon, but **no Pokémon names or art are used**, and none should be added). She types letters or short words to fill a pal's hearts and catch it. 10 original pals, each levels up at 3 and 6 catches (star, then wings and crown).

- Levels: 1 = home row (a s d f…), 2 = all letters, 3 = 3-letter words, 4 = longer words. 8 catches per round, then a celebration screen.
- A big on-screen QWERTY keyboard lights up the next key, so the iPhone keyboard never opens. A real keyboard works too.
- The device's English voice reads each letter/word. Wrong keys cost nothing.
- Progress is saved in that phone's browser (localStorage keys `typingPals.v1`, `typingPals.sound`).
- On 2026-11-11 Rex renamed its home-page section from "英文 English" to "資通訊 ICT". The file still lives in `english/`.

## 9. History (from the project's two work threads)

**Create P1 exercises and mock tests** (2026-11-05 to 2026-11-10)
- 11-05: WS 4.1c built as a claude.ai artifact. Read-aloud added with device voices. Rex reported silence (opened in WhatsApp, phone on silent). Embedded MP3s were tried and rejected (too big, wrong Cantonese), so device voices came back.
- 11-05: claude.ai links failed in Hong Kong and the Claude app shows .html as code, so the site moved to GitHub Pages. Rex created the repo (first private, then public) and set Pages to main / root. Fixed a tab bug (sheets not hiding).
- 11-05: WS 4.2c added.
- 11-10: WS 1.2 時間 added, relabelled 1下A · 單元 1 時間 at Rex's request. WS 2.1 日期 added (first Pages deploy hung, a new commit fixed it). 生字卡 flashcards added to all four sets.

**Build English typing game** (2026-11-05, 2026-11-10)
- Typing Pals built and merged (PR #1). Home section renamed to 資通訊 ICT (PR #2).

## 10. Ideas Rex hasn't asked for yet

Chinese, English and General Studies worksheets; a progress record of mock-test scores; more Typing Pals word lists. Ask before building any of these.
