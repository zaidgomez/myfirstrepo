import ast
import operator
import tkinter as tk


def calculate(expression):
	"""Evaluate a basic arithmetic expression without using eval()."""
	operations = {
		ast.Add: operator.add,
		ast.Sub: operator.sub,
		ast.Mult: operator.mul,
		ast.Div: operator.truediv,
		ast.UAdd: operator.pos,
		ast.USub: operator.neg,
	}

	def visit(node):
		if isinstance(node, ast.Expression):
			return visit(node.body)
		if isinstance(node, ast.Constant) and type(node.value) in (int, float):
			return node.value
		if isinstance(node, ast.BinOp) and type(node.op) in operations:
			return operations[type(node.op)](visit(node.left), visit(node.right))
		if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
			return operations[type(node.op)](visit(node.operand))
		raise ValueError("Invalid expression")

	return visit(ast.parse(expression, mode="eval"))


class Calculator:
	def __init__(self, root):
		self.root = root
		self.root.title("Calculator")
		self.root.resizable(False, False)
		self.expression = tk.StringVar()
		self.just_calculated = False

		display = tk.Entry(
			root, textvariable=self.expression, font=("Arial", 24),
			justify="right", state="readonly", readonlybackground="white",
			width=16, bd=8,
		)
		display.grid(row=0, column=0, columnspan=4, padx=8, pady=8)

		buttons = [
			("C", "⌫", "÷", "×"),
			("7", "8", "9", "−"),
			("4", "5", "6", "+"),
			("1", "2", "3", "="),
			("0", ".", "(", ")"),
		]
		for row, labels in enumerate(buttons, start=1):
			for column, label in enumerate(labels):
				tk.Button(
					root, text=label, font=("Arial", 18), width=4, height=2,
					command=lambda value=label: self.press(value),
				).grid(row=row, column=column, padx=3, pady=3, sticky="nsew")

	def press(self, value):
		current = self.expression.get()
		if value == "C":
			self.expression.set("")
			self.just_calculated = False
		elif value == "⌫":
			self.expression.set(current[:-1])
			self.just_calculated = False
		elif value == "=":
			try:
				result = calculate(current.replace("×", "*").replace("÷", "/").replace("−", "-"))
				self.expression.set(str(result))
				self.just_calculated = True
			except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
				self.expression.set("Error")
				self.just_calculated = True
		else:
			if current == "Error" or (self.just_calculated and value not in "+−×÷"):
				current = ""
			self.expression.set(current + value)
			self.just_calculated = False


if __name__ == "__main__":
	window = tk.Tk()
	Calculator(window)
	window.mainloop()
