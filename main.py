
import ast
import operator

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.035, 0.035, 0.045, 1)


class SafeMath(ast.NodeVisitor):
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid")

    def visit_BinOp(self, node):
        op = self.ops.get(type(node.op))
        if not op:
            raise ValueError("Invalid")
        return op(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
        raise ValueError("Invalid")

    def generic_visit(self, node):
        raise ValueError("Invalid")


class MyButton(Button):
    def __init__(self, bg, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (0.95, 0.95, 0.95, 1)
        self.font_size = "23sp"
        self.bold = True

        with self.canvas.before:
            Color(*bg)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[18]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MYCalculator(App):

    def build(self):
        self.expression = ""

        root = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=12
        )

        my_title = Label(
            text="[b][color=cccccc]MY[/color][/b]",
            markup=True,
            font_size="48sp",
            size_hint=(1, 0.23)
        )
        root.add_widget(my_title)

        title = Label(
            text="[b]PREMIUM CALCULATOR[/b]\n[color=cccccc]SPECIAL EDITION[/color]",
            markup=True,
            font_size="18sp",
            size_hint=(1, 0.12)
        )
        root.add_widget(title)

        self.display = Label(
            text="0",
            font_size="38sp",
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint=(1, 0.18)
        )
        self.display.bind(
            size=self.display.setter("text_size")
        )
        root.add_widget(self.display)

        grid = GridLayout(
            cols=4,
            spacing=9,
            size_hint=(1, 0.55)
        )

        buttons = [
            "AC", "⌫", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "−",
            "1", "2", "3", "+",
            "±", "0", ".", "="
        ]

        for value in buttons:
            if value == "=":
                bg = (0.75, 0.04, 0.09, 1)
            elif value in ["÷", "×", "−", "+", "%"]:
                bg = (0.32, 0.035, 0.06, 1)
            else:
                bg = (0.13, 0.13, 0.15, 1)

            btn = MyButton(bg=bg, text=value)
            btn.bind(
                on_press=lambda instance, v=value: self.press(v)
            )
            grid.add_widget(btn)

        root.add_widget(grid)
        return root

    def press(self, value):
        if value == "AC":
            self.expression = ""

        elif value == "⌫":
            self.expression = self.expression[:-1]

        elif value == "=":
            try:
                exp = (
                    self.expression
                    .replace("×", "*")
                    .replace("÷", "/")
                    .replace("−", "-")
                )
                tree = ast.parse(exp, mode="eval")
                result = SafeMath().visit(tree)
                self.expression = str(result)
            except Exception:
                self.expression = "Error"

        elif value == "±":
            if self.expression:
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression

        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += value

        self.display.text = self.expression or "0"


MYCalculator().run()
