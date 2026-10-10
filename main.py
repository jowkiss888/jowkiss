# -*- coding: utf-8 -*-
import os
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.utils import platform

# ============================================================
# 改这两行就行
API_BASE = "http://10.90.1.11/api.asp"
API_TOKEN = "sample2024"
# ============================================================

# 字体（如果没有fonts文件夹，自动忽略，用默认字体，不报错）
BASE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(BASE, "fonts", "msyh.ttc")
FB = os.path.join(BASE, "fonts", "msyhbd.ttc")
if os.path.exists(FR):
    LabelBase.register(name="Roboto", fn_regular=FR,
                       fn_bold=FB if os.path.exists(FB) else FR)

if platform not in ("android", "ios"):
    Window.size = (480, 800)

CN = ["一", "二", "三", "四", "五", "六", "七", "八"]

BG = (0.96, 0.97, 0.98, 1)
CARD = (1, 1, 1, 1)
PRIMARY = (0.145, 0.388, 0.921, 1)
PRIMARY_DK = (0.102, 0.306, 0.780, 1)
SUCCESS = (0.063, 0.725, 0.506, 1)
SUCCESS_DK = (0.040, 0.560, 0.400, 1)
DANGER = (0.937, 0.267, 0.267, 1)
DANGER_DK = (0.780, 0.200, 0.200, 1)
OK_TXT = (0.06, 0.60, 0.42, 1)
ERR_TXT = (0.85, 0.20, 0.20, 1)
TEXT = (0.12, 0.16, 0.22, 1)
MUTED = (0.42, 0.45, 0.50, 1)

def _req(action, data=None):
    p = dict(data or {})
    p["action"] = action
    p["token"] = API_TOKEN
    r = requests.post(API_BASE, data=p, timeout=8)
    r.raise_for_status()
    return r.json()

def verify(batch, code, step, mode):
    return _req("verify", {"batch": batch, "code": code,
                           "step": step, "mode": mode})

def submit_record(machine, batch, uno, codes):
    return _req("submit", {"machine": machine, "batch": batch,
                           "uno": uno, "codes": "|".join(codes)})

def count_today():
    r = requests.get(API_BASE,
                     params={"action": "count", "token": API_TOKEN},
                     timeout=8)
    r.raise_for_status()
    return int(r.json().get("qty") or 0)

def run_async(func, ok_cb, err_cb=None):
    def w():
        try:
            res = func()
        except Exception as e:
            if err_cb:
                Clock.schedule_once(lambda dt, e=e: err_cb(e), 0)
            return
        Clock.schedule_once(lambda dt, r=res: ok_cb(r), 0)
    threading.Thread(target=w, daemon=True).start()

class Inp(TextInput):
    def __init__(self, **kw):
        kw.setdefault("multiline", False)
        kw.setdefault("write_tab", False)
        kw.setdefault("font_size", "16sp")
        kw.setdefault("size_hint_y", None)
        kw.setdefault("height", dp(42))
        super().__init__(**kw)
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = TEXT
        self.cursor_color = PRIMARY
        self.hint_text_color = (0.65, 0.67, 0.71, 1)
        self.padding = [dp(12), dp(10), dp(12), dp(10)]

class Btn(Button):
    def __init__(self, bg=PRIMARY, bgd=PRIMARY_DK, **kw):
        kw.setdefault("font_size", "16sp")
        kw.setdefault("bold", True)
        kw.setdefault("color", (1, 1, 1, 1))
        super().__init__(**kw)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self._n, self._p = bg, bgd
        with self.canvas.before:
            self._c = Color(*bg)
            self._r = RoundedRectangle(pos=self.pos, size=self.size,
                                       radius=[dp(12)])
        self.bind(pos=self._sync, size=self._sync, state=self._st)

    def _sync(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size

    def _st(self, i, v):
        self._c.rgba = self._p if v == "down" else self._n

class ModeBtn(ButtonBehavior, Label):
    def __init__(self, **kw):
        kw.setdefault("color", (1, 1, 1, 1))
        kw.setdefault("bold", True)
        kw.setdefault("font_size", "12sp")
        kw.setdefault("halign", "center")
        kw.setdefault("valign", "middle")
        kw.setdefault("size_hint", (None, None))
        kw.setdefault("size", (dp(104), dp(32)))
        super().__init__(**kw)
        self.bind(size=lambda i, v: setattr(i, "text_size", v))
        with self.canvas.before:
            self._c = Color(1, 1, 1, 0.18)
            self._r = RoundedRectangle(pos=self.pos, size=self.size,
                                       radius=[dp(8)])
        self.bind(pos=self._s, size=self._s, state=self._st)

    def _s(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size

    def _st(self, i, v):
        self._c.rgba = (1, 1, 1, 0.42) if v == "down" else (1, 1, 1, 0.18)

class Card(BoxLayout):
    def __init__(self, **kw):
        kw.setdefault("orientation", "vertical")
        kw.setdefault("size_hint_y", None)
        kw.setdefault("padding", [dp(14), dp(12), dp(14), dp(12)])
        kw.setdefault("spacing", dp(6))
        super().__init__(**kw)
        with self.canvas.before:
            Color(*CARD)
            self._r = RoundedRectangle(pos=self.pos, size=self.size,
                                       radius=[dp(12)])
        self.bind(pos=self._s, size=self._s)
        self.bind(minimum_height=self.setter("height"))

    def _s(self, *a):
        self._r.pos = self.pos
        self._r.size = self.size

class Dots(Widget):
    def __init__(self, **kw):
        super().__init__(size_hint=(None, None), size=(dp(180), dp(22)), **kw)
        self.total = 8
        self.done = 0
        self.cur = 0
        self.bind(pos=self._draw, size=self._draw)

    def set_progress(self, d, c):
        self.done, self.cur = d, c
        self._draw()

    def _draw(self, *a):
        self.canvas.clear()
        r, gap = dp(5), dp(9)
        step = r * 2 + gap
        tw = self.total * r * 2 + (self.total - 1) * gap
        x = self.center_x - tw / 2 + r
        y = self.center_y
        with self.canvas:
            for i in range(self.total):
                if i < self.done:
                    Color(*SUCCESS)
                elif i == self.cur:
                    Color(*PRIMARY)
                else:
                    Color(0.86, 0.88, 0.91, 1)
                Ellipse(pos=(x - r, y - r), size=(r * 2, r * 2))
                x += step

class Main(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", **kw)
        self.codes = [""] * 8
        self.busy = False
        self.mode = 0

        with self.canvas.before:
            Color(*BG)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: (setattr(self._bg, "pos", self.pos),),
                  size=lambda *a: (setattr(self._bg, "size", self.size),))

        bar = BoxLayout(size_hint_y=None, height=dp(52),
                        padding=[dp(18), 0, dp(18), 0], spacing=dp(8))
        with bar.canvas.before:
            Color(*PRIMARY)
            br = Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(pos=lambda i, v: setattr(br, "pos", v),
                 size=lambda i, v: setattr(br, "size", v))
        t = Label(text="扫码采集", color=(1, 1, 1, 1), bold=True,
                  font_size="20sp", halign="left", valign="middle")
        t.bind(size=lambda i, v: setattr(i, "text_size", v))
        bar.add_widget(t)
        self.mode_btn = ModeBtn(text="订单号模式")
        self.mode_btn.bind(on_release=lambda *_: self._toggle())
        bar.add_widget(self.mode_btn)
        self.add_widget(bar)

        sw = BoxLayout(size_hint_y=None, height=dp(38),
                       padding=[dp(18), 0, dp(18), 0])
        with sw.canvas.before:
            Color(1, 1, 1, 0.6)
            sr = Rectangle(pos=sw.pos, size=sw.size)
        sw.bind(pos=lambda i, v: setattr(sr, "pos", v),
                size=lambda i, v: setattr(sr, "size", v))
        self.status = Label(text="请先输入机器号", color=MUTED,
                            font_size="14sp", halign="left", valign="middle")
        self.status.bind(size=lambda i, v: setattr(i, "text_size", v))
        sw.add_widget(self.status)
        self.add_widget(sw)

        sv = ScrollView(do_scroll_x=False, bar_width=0)
        root = BoxLayout(orientation="vertical", spacing=dp(10),
                         size_hint_y=None,
                         padding=[dp(14), dp(10), dp(14), dp(16)])
        root.bind(minimum_height=root.setter("height"))

        c1 = Card()
        self.f_machine = self._add_inp(c1, "机器号", "请输入机台编号",
                                       lambda: setattr(self.f_batch, "focus", True))
        self.f_batch = self._add_inp(c1, "批次号", "请输入或扫描批次号",
                                     lambda: setattr(self.f_uno, "focus", True))
        self.f_uno = self._add_inp(c1, "Uno", "请输入 Uno（可选）", self._on_uno)
        root.add_widget(c1)

        c2 = Card()
        hdr = BoxLayout(size_hint_y=None, height=dp(24), spacing=dp(8))
        ht = Label(text="加捻股线扫码", color=TEXT, bold=True,
                   font_size="15sp", halign="left", valign="middle")
        ht.bind(size=lambda i, v: setattr(i, "text_size", v))
        hdr.add_widget(ht)
        self.dots = Dots()
        hdr.add_widget(self.dots)
        c2.add_widget(hdr)

        self.scans = []
        for i in range(8):
            row = BoxLayout(orientation="horizontal", size_hint_y=None,
                            height=dp(46), spacing=dp(8))
            lbl = Label(text="加捻第%s股线：" % CN[i], color=MUTED, bold=True,
                        font_size="14sp", size_hint_x=None, width=dp(112),
                        halign="left", valign="middle")
            lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
            row.add_widget(lbl)
            inp = Inp(hint_text="等待扫码")
            inp.bind(on_text_validate=lambda inst, k=i:
                     self._on_scan(k, inst.text.strip()))
            inp.disabled = (i != 0)
            row.add_widget(inp)
            c2.add_widget(row)
            self.scans.append(inp)
        root.add_widget(c2)

        sv.add_widget(root)
        self.add_widget(sv)

        bw = BoxLayout(orientation="vertical", size_hint_y=None,
                       height=dp(94),
                       padding=[dp(14), dp(8), dp(14), dp(12)],
                       spacing=dp(6))
        with bw.canvas.before:
            Color(*CARD)
            br2 = Rectangle(pos=bw.pos, size=bw.size)
        bw.bind(pos=lambda i, v: setattr(br2, "pos", v),
                size=lambda i, v: setattr(br2, "size", v))
        self.counter = Label(text="今日：-", color=MUTED, font_size="13sp",
                             size_hint_y=None, height=dp(16),
                             halign="center", valign="middle")
        self.counter.bind(size=lambda i, v: setattr(i, "text_size", v))
        bw.add_widget(self.counter)
        row = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        b1 = Btn(text="提 交", bg=SUCCESS, bgd=SUCCESS_DK)
        b1.bind(on_release=lambda *_: self._submit())
        b2 = Btn(text="清 空", bg=DANGER, bgd=DANGER_DK)
        b2.bind(on_release=lambda *_: self._clear())
        row.add_widget(b1)
        row.add_widget(b2)
        bw.add_widget(row)
        self.add_widget(bw)

        Clock.schedule_interval(self._tick, 10)
        Clock.schedule_once(lambda dt: setattr(self.f_machine, "focus", True), 0.3)

    def _add_inp(self, card, cap, hint, on_enter):
        lbl = Label(text=cap, color=MUTED, bold=True, font_size="13sp",
                    size_hint_y=None, height=dp(18),
                    halign="left", valign="middle")
        lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
        card.add_widget(lbl)
        inp = Inp(hint_text=hint)
        inp.bind(on_text_validate=lambda *_: on_enter())
        card.add_widget(inp)
        return inp

    def _toggle(self):
        self.mode = 1 - self.mode
        self.mode_btn.text = "订单号模式" if self.mode == 0 else "批次号模式"
        self._set_status("已切换到 " + self.mode_btn.text, ok=True)

    def _on_uno(self):
        self.scans[0].disabled = False
        self.scans[0].focus = True
        self.dots.set_progress(0, 0)
        self._set_status("批次已录入，请扫 加捻第一股线")

    def _on_scan(self, idx, text):
        if not text or self.busy:
            return
        batch = self.f_batch.text.strip()
        if not batch:
            self._set_status("请先输入批次号", ok=False)
            return
        self.busy = True
        self._set_status("校验中...")
        run_async(lambda: verify(batch, text, idx + 1, self.mode),
                  lambda r: self._v_ok(idx, r),
                  lambda e: self._v_err(idx, e))

    def _v_ok(self, idx, res):
        self.busy = False
        if not res.get("ok"):
            self._set_status("不通过  期望[%s]  实际[%s]" %
                             (res.get("expect", ""), res.get("short", "")),
                             ok=False)
            self.codes[idx] = ""
            self.scans[idx].text = ""
            self.scans[idx].focus = True
            return
        self._set_status("通过  %s" % res.get("code", ""), ok=True)
        self.codes[idx] = res.get("code", "")
        nxt = idx + 1
        if res.get("next") and nxt < 8:
            self.scans[nxt].disabled = False
            self.scans[nxt].focus = True
            self.dots.set_progress(nxt, nxt)
        else:
            self.dots.set_progress(8, -1)
            self._set_status("全部扫码完成，请点击 [提交]", ok=True)

    def _v_err(self, idx, err):
        self.busy = False
        self._set_status("请求失败：%s" % err, ok=False)
        self.codes[idx] = ""
        self.scans[idx].text = ""
        self.scans[idx].focus = True

    def _submit(self):
        if self.busy:
            return
        m = self.f_machine.text.strip()
        b = self.f_batch.text.strip()
        u = self.f_uno.text.strip()
        if not (m and b and self.codes[0]):
            self._set_status("机器号/批次号/加捻第一股线 不能为空", ok=False)
            return
        self.busy = True
        self._set_status("提交中...")
        codes = list(self.codes)
        run_async(lambda: submit_record(m, b, u, codes),
                  lambda _: self._after_submit(),
                  lambda e: self._submit_err(e))

    def _after_submit(self):
        self.busy = False
        self._set_status("已保存", ok=True)
        self._clear()

    def _submit_err(self, err):
        self.busy = False
        self._set_status("提交失败：%s" % err, ok=False)

    def _clear(self):
        self.codes = [""] * 8
        self.f_machine.text = ""
        self.f_batch.text = ""
        self.f_uno.text = ""
        for i, inp in enumerate(self.scans):
            inp.text = ""
            inp.disabled = (i != 0)
        self.dots.set_progress(0, 0)
        self.f_machine.focus = True

    def _set_status(self, msg, ok=True):
        self.status.text = msg
        self.status.color = OK_TXT if ok else ERR_TXT

    def _tick(self, *_):
        run_async(count_today,
                  lambda n: setattr(self.counter, "text", "今日：%d" % n),
                  lambda e: setattr(self.counter, "text", "今日：-"))

class SampleApp(App):
    def build(self):
        self.title = "扫码采集"
        return Main()

if __name__ == "__main__":
    SampleApp().run()