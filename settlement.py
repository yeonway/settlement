import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date
import json
import os

root = tk.Tk()
root.title("알바 정산 프로그램")

# 창 크기
w = 1200
h = 700

# 화면 크기
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# 중앙 좌표 계산
x = (screen_w // 2) - (w // 2)
y = (screen_h // 2) - (h // 2)

root.geometry(f"{w}x{h}+{x}+{y}")

# 이름 드롭다운 메뉴
names = ["허연우", "허윤아"]

name_cb = ttk.Combobox(root, width=10, height=5, values=names, state="readonly")
name_cb.place(x=25, y=20)
name_cb.set("허윤아")

# 월
month = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]

month_cb = ttk.Combobox(root, width=10, height=5, values=month, state="readonly")
month_cb.place(x=440, y=80)
month_cb.set("1월")

def reset_range():
    global range_start, range_end
    range_start = None
    range_end = None
    clear_range_highlight()

def on_name_change(event):
    m = month.index(month_cb.get()) + 1
    update_calendar(current_year, m)
    reset_range()
    
name_cb.bind("<<ComboboxSelected>>", on_name_change)

def on_month_change(event):
    m = month.index(month_cb.get()) + 1
    update_calendar(current_year, m)
    reset_range()
month_cb.bind("<<ComboboxSelected>>", on_month_change)

def make_date_key(year, month, day):
    name = name_cb.get()
    return f"{name}-{year}-{month:02d}-{int(day):02d}"

calendar_data: dict[str, dict] = {}
DATA_FILE = "calendar_data.json"

def load_data():
    global calendar_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            calendar_data = json.load(f)
    else:
        calendar_data = {}


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {str(k): v for k, v in calendar_data.items()},
            f,
            ensure_ascii=False,
            indent=2
        )

load_data()

""" 
button1 = tk.Button(root) 
button2 = tk.Button(root) 
button3 = tk.Button(root) 
button4 = tk.Button(root) 
button5 = tk.Button(root) 
button6 = tk.Button(root) 
button7 = tk.Button(root) 

button1.place(x=200, y=80, width=80, height=50) 
button2.place(x=280, y=80, width=60, height=50)
button3.place(x=360, y=80, width=60, height=50) 
button4.place(x=440, y=80, width=60, height=50) 
button5.place(x=520, y=80, width=60, height=50) 
button6.place(x=600, y=80, width=60, height=50) 
button7.place(x=680, y=80, width=60, height=50) 
"""

buttons = []
num = 1

for i in range(7):
    text = str(num) if num <= 31 else ""
    btn = tk.Button(root, text=text, anchor="nw")
    btn.place(x=130 + i*110, y=120, width=110, height=80)
    buttons.append(btn)
    num += 1

for i in range(7):
    text = str(num) if num <= 31 else ""
    btn = tk.Button(root, text=text, anchor="nw")
    btn.place(x=130 + i*110, y=200, width=110, height=80)
    buttons.append(btn)
    num += 1

for i in range(7):
    text = str(num) if num <= 31 else ""
    btn = tk.Button(root, text=text, anchor="nw")
    btn.place(x=130 + i*110, y=280, width=110, height=80)
    buttons.append(btn)
    num += 1

for i in range(7):
    text = str(num) if num <= 31 else ""
    btn = tk.Button(root, text=text, anchor="nw")
    btn.place(x=130 + i*110, y=360, width=110, height=80)
    buttons.append(btn)
    num += 1

for i in range(7):
    text = str(num) if num <= 31 else ""
    btn = tk.Button(root, text=text, anchor="nw")
    btn.place(x=130 + i*110, y=440, width=110, height=80)
    buttons.append(btn)
    num += 1

range_start = None
range_end = None

def clear_range_highlight():
    for b in buttons:
        b.config(bg="SystemButtonFace")

def apply_range_highlight(year, month_num, s, e):
    clear_range_highlight()
    for b in buttons:
        t = b.cget("text").split("\n")[0].strip()
        if t.isdigit():
            d = int(t)
            if s <= d <= e:
                b.config(bg="#d9eaff")  # 연한 파란색(원하면 변경)

# ====== 우측 정산표(표시용) ======
panel_x = 950
panel_y = 120
panel_w = 230
panel_h = 260

panel = tk.Frame(root, bd=1, relief="solid")
panel.place(x=panel_x, y=panel_y, width=panel_w, height=panel_h)

# 항목/단가
items = [
    ("설거지", 5000),
    ("분리수거", 1500),
    ("글 쓰기", 750),
    ("타자 연습", 1500),
]

qty_labels = {}     # 항목별 횟수 Label
money_labels = {}   # 항목별 금액 Label

# 헤더
tk.Label(panel, text="", bd=1, relief="solid").place(x=0,   y=0,  width=90, height=30)
tk.Label(panel, text="횟수", bd=1, relief="solid").place(x=90,  y=0,  width=50, height=30)
tk.Label(panel, text="금액", bd=1, relief="solid").place(x=140, y=0,  width=90, height=30)

row_h = 35
start_y = 30

for r, (name, unit) in enumerate(items):
    y = start_y + r * row_h

    tk.Label(panel, text=name, anchor="w", padx=6, bd=1, relief="solid").place(
        x=0, y=y, width=90, height=row_h
    )

    qlbl = tk.Label(panel, text="0", anchor="e", padx=6, bd=1, relief="solid")
    qlbl.place(x=90, y=y, width=50, height=row_h)
    qty_labels[name] = qlbl

    mlbl = tk.Label(panel, text="0원", anchor="e", padx=6, bd=1, relief="solid")
    mlbl.place(x=140, y=y, width=90, height=row_h)
    money_labels[name] = mlbl

# 합계
y_sum = start_y + len(items) * row_h
tk.Label(panel, text="합계", anchor="center", bd=1, relief="solid").place(
    x=0, y=y_sum, width=140, height=row_h
)
total_label = tk.Label(panel, text="0원", anchor="e", padx=6, bd=1, relief="solid")
total_label.place(x=140, y=y_sum, width=90, height=row_h)


items = [("설거지", 5000), ("분리수거", 1500), ("글 쓰기", 750), ("타자 연습", 1500)]

qty_vars = {}       # 항목별 IntVar
money_labels = {}   # 항목별 금액 Label
total_label = None  # 합계 Label


def range_summary(year, month_num, s, e):
    # items는 네가 만든 정산표 항목 리스트 그대로 사용한다고 가정
    # items = [("설거지",5000), ("분리수거",1500), ("글 쓰기",750), ("타자 연습",1500)]
    sums = {name: 0 for name, _ in names}

    for day in range(s, e + 1):
        key = make_date_key(year, month_num, day)   # (이미 이름까지 포함하도록 바꿔둔 상태 기준)
        info = calendar_data.get(key)
        if not info:
            continue
        for name, _ in names:
            sums[name] += int(info.get(name, 0))

    return sums

def on_day_click(day, btn):
    global range_start, range_end

    day = int(day)
    m = month.index(month_cb.get()) + 1

    if range_start is None or (range_start is not None and range_end is not None):
        # 새 범위 시작
        range_start = day
        range_end = None
        apply_range_highlight(current_year, m, range_start, range_start)
        return

    # 범위 종료
    range_end = day
    if range_end < range_start:
        range_start, range_end = range_end, range_start

    apply_range_highlight(current_year, m, range_start, range_end)

    # ✅ 선택 범위 합계 -> 우측 표에 반영
    sums = range_summary(current_year, m, range_start, range_end)

    # qty_vars / money_labels / total_label는 네가 만든 우측 정산표 코드 그대로 사용
    for name, unit in names:
        qty_vars[name].set(sums[name])
        money_labels[name].config(text=f"{sums[name] * unit}원")

    total = sum(sums[name] * unit for name, unit in items)
    total_label.config(text=f"{total}원")





calendar.setfirstweekday(calendar.SUNDAY)  # 월요일 시작

# 날짜 연동
current_year = date.today().year

# 팝업
popup = None  # 팝업 중복 방지

def open_popup(day, btn):
    global popup

    if popup is not None and popup.winfo_exists():
        return

    # 버튼의 화면 좌표 (버튼 오른쪽에 약간 띄워서)
    bx = btn.winfo_rootx()
    by = btn.winfo_rooty()
    bw = btn.winfo_width()

    popup = tk.Toplevel(root)
    popup.title(f"{day}일")
    popup.geometry(f"300x200+{bx + bw + 10}+{by}")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    # 날짜별 데이터 불러오기
    current_month = month.index(month_cb.get()) + 1
    date_key = make_date_key(current_year, current_month, day)

    data = calendar_data.get(date_key, {
        "설거지": 0,
        "분리수거": 0,
        "글 쓰기": 0,
        "타자 연습": 0
    })

    vars = {}
    font = ("맑은 고딕", 11)

    def make_row(text, y):
        tk.Label(popup, text=text, font=font).place(x=10, y=y)
        var = tk.IntVar(value=data[text])
        vars[text] = var
        tk.Spinbox(
            popup,
            from_=0, to=100,
            textvariable=var,
            font=font
        ).place(x=90, y=y-3, width=130, height=28)

    make_row("설거지", 20)
    make_row("분리수거", 50)
    make_row("글 쓰기", 80)
    make_row("타자 연습", 110)


# 팝업 닫을 때 JSON 저장    
    def on_close():
        global popup
        current_month = month.index(month_cb.get()) + 1
        date_key = make_date_key(current_year, current_month, day)

        calendar_data[date_key] = {k: v.get() for k, v in vars.items()}
        save_data()

        if popup is not None and popup.winfo_exists():
            popup.destroy()
        popup = None
        
        update_calendar(current_year, month.index(month_cb.get()) + 1)


    # ✅ popup 생성 이후에만 호출 가능
    popup.protocol("WM_DELETE_WINDOW", on_close)

def update_calendar(year, month):
    month_data = calendar.monthcalendar(year, month)
    days = [d for week in month_data for d in week]
    days += [0] * (len(buttons) - len(days))

    for btn, d in zip(buttons, days):
        if d == 0:
            btn.config(text="", command=lambda: None)
        else:
            date_key = make_date_key(year, month, d)
            info = calendar_data.get(date_key)

            lines = [str(d)]  # 첫 줄: 날짜

            if info:
                if info.get("설거지", 0) > 0:
                    lines.append(f"설거지 {info['설거지']}")
                if info.get("분리수거", 0) > 0:
                    lines.append(f"분리수거 {info['분리수거']}")
                if info.get("글 쓰기", 0) > 0:
                    lines.append(f"글 쓰기 {info['글 쓰기']}")
                if info.get("타자 연습", 0) > 0:
                    lines.append(f"타자 연습 {info['타자 연습']}")

            btn.config(
                text="\n".join(lines),
                anchor="nw",
                justify="left",
                command=lambda day=d, b=btn: on_day_click(day, b)
            )




# 열렸을 때 1월 업데이트
update_calendar(current_year, 1)

root.mainloop()
