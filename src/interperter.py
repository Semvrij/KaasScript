from src.constants.constants import CURRENT_LANG, WHILELOOPLIMIT
from src.constants.errormessages import DivisionByZeroMessage
from src.errors import RTError
from src.constants.tokentypes import TT_KEYWORD, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_MODUL, TT_POW, TT_ROOT, TT_EE, TT_EEE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE
from src.lexer import Lexer
from src._parser import Parser

class RTResult:
	def __init__(self):
		self.reset()
	
	def reset(self):
		self.value = None
		self.error = None
		self.func_return_value = None
		self.loop_should_continue = False
		self.loop_should_break = False
	
	def register(self, res):
		self.error = res.error
		self.func_return_value = res.func_return_value
		self.loop_should_continue = res.loop_should_continue
		self.loop_should_break = res.loop_should_break
		return res.value
	
	def success(self, value):
		self.reset()
		self.value = value
		return self

	def success_return(self, value):
		self.reset()
		self.func_return_value = value
		return self
	
	def success_continue(self):
		self.reset()
		self.loop_should_continue = True
		return self

	def success_break(self):
		self.reset()
		self.loop_should_break = True
		return self

	def failure(self, error):
		self.reset()
		self.error = error
		return self

	def should_return(self):
		return (
			self.error or
			self.func_return_value or
			self.loop_should_continue or
			self.loop_should_break
		)

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)

	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)
	
	def modul_by(self, other):
		return None, self.illegal_operation(other)
	
	def root_of(self, other):
		return None, self.illegal_operation(other)

	def powed_by(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return None, self.illegal_operation(other)
	
	def get_comparison_eee(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_ne(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)

	def anded_by(self, other):
		return None, self.illegal_operation(other)

	def ored_by(self, other):
		return None, self.illegal_operation(other)

	def notted(self, other):
		return None, self.illegal_operation(other)

	def execute(self, args):
		return RTResult().failure(self.illegal_operation())

	def copy(self):
		raise Exception('No copy method defined')

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'Illegal operation',
			self.context
		)

class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					DivisionByZeroMessage[CURRENT_LANG],
					self.context
				)

			return Number(self.value / other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def modul_by(self, other):
		if isinstance(other, Number):
			return Number(self.value % other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def root_of(self, other):
		if isinstance(other, Number):
			return Number(other.value ** (1 / self.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, String):
			return Number(int(str(self.value) == other.value)).set_context(self.context), None
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eee(self, other):
		if isinstance(other, String):
			return Number(0).set_context(self.context), None
		elif isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def is_true(self):
		return self.value != 0

	def __repr__(self):
		return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == str(other.value))).set_context(self.context), None
		if isinstance(other, String):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)
	
	def get_comparison_eee(self, other):
		if isinstance(other, Number):
			return Number(0).set_context(self.context), None
		elif isinstance(other, String):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, String):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return self.value

	def __repr__(self):
		return f'"{self.value}"'

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):
		if isinstance(other, Number):
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Element at this index could not be removed from list because index is out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, List):
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Element at this index could not be retrieved from list because index is out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)
	
	def copy(self):
		copy = List(self.elements[:])
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return ", ".join([str(x) for x in self.elements])

	def __repr__(self):
		return f'[{", ".join([str(x) for x in self.elements])}]'

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RTResult()

		if len(args) > len(arg_names):
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				f"{len(args) - len(arg_names)} too many args passed into {self}",
				self.context
			))
		
		if len(args) < len(arg_names):
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				f"{len(arg_names) - len(args)} too few args passed into {self}",
				self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RTResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def execute(self, args):
		res = RTResult()
		interpreter = Interpreter()
		exec_ctx = self.generate_new_context()

		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, exec_ctx))
		if res.should_return() and res.func_return_value == None: return res
		
		ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
		return res.success(ret_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.should_return(): return res

		return_value = res.register(method(exec_ctx))
		if res.should_return(): return res
		return res.success(return_value)
	
	def no_visit_method(self, node, context):
		raise Exception(f'No execute_{self.name} method defined')

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<built-in function {self.name}>"

	def execute_print(self, exec_ctx):
		print(str(exec_ctx.symbol_table.get('value')))
		return RTResult().success(Number.null)
	execute_print.arg_names = ['value']

	def execute_input(self, exec_ctx):
		text = input()
		return RTResult().success(String(text))
	execute_input.arg_names = []

	def execute_run(self, exec_ctx):
		fn = exec_ctx.symbol_table.get("fn")

		if not isinstance(fn, String):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument must be string",
				exec_ctx
			))

		fn = fn.value

		try:
			with open(fn, "r") as f:
				script = f.read()
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Failed to load script \"{fn}\"\n" + str(e),
				exec_ctx
			))

		_, error = run(fn, script)
		
		if error:
			return RTResult().failure(error)

		return RTResult().success(Number.null)
	execute_run.arg_names = ["fn"]

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

class Interpreter:
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined')

	def visit_NumberNode(self, node, context):
		return RTResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_StringNode(self, node, context):
		return RTResult().success(
			String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is not defined",
				context
			))

		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.dived_by(right)
		elif node.op_tok.type == TT_MODUL:
			result, error = left.modul_by(right)
		elif node.op_tok.type == TT_POW:
			result, error = left.powed_by(right)
		elif node.op_tok.type == TT_ROOT:
			result, error = left.root_of(right)
		elif node.op_tok.type == TT_EE:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == TT_EEE:
			result, error = left.get_comparison_eee(right)
		elif node.op_tok.type == TT_NE:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == TT_LT:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == TT_GT:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == TT_LTE:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == TT_GTE:
			result, error = left.get_comparison_gte(right)
		elif node.op_tok.matches(TT_KEYWORD, 'and'):
			result, error = left.anded_by(right)
		elif node.op_tok.matches(TT_KEYWORD, 'or'):
			result, error = left.ored_by(right)
		
		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end))

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return(): return res

		error = None

		if node.op_tok.type == TT_MINUS:
			number, error = number.multed_by(Number(-1))
		elif node.op_tok.matches(TT_KEYWORD, 'not'):
			number, error = number.notted()
		
		if error:
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.pos_start, node.pos_end))
	
	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Number.null if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			else_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(Number.null if should_return_null else else_value)

		return res.success(Number.null)
	
	def visit_ForNode(self, node, context):
		res = RTResult()
		elements = []

		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Number(1)

		i = start_value.value

		if step_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value
		
		while condition():
			context.symbol_table.set(node.var_name_tok.value, Number(i))
			i += step_value.value

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue: continue
			if res.loop_should_break: break

			elements.append(value)

		return res.success(
			Number.null if node.should_return_null else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []
		i = 0

		while True:
			i += 1
			if i == WHILELOOPLIMIT:
				return res.failure(RTError(
					node.pos_start, node.pos_end,
					'Out of Memory (Infinite Loop)',
					context
				))

			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue: continue
			if res.loop_should_break: break

			elements.append(value)

		return res.success(
			Number.null if node.should_return_null else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_FuncDefNode(self, node, context):
		res = RTResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
		
		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RTResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.should_return(): return res

		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(return_value)

	def visit_ReturnNode(self, node, context):
		res = RTResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			value = Number.null
		
		return res.success_return(value)

	def visit_ContinueNode(self, node, context):
		return RTResult().success_continue()

	def visit_BreakNode(self, node, context):
		return RTResult().success_break()

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("print", BuiltInFunction("print"))
global_symbol_table.set("input", BuiltInFunction("input"))
global_symbol_table.set("run", BuiltInFunction("run"))

def run(fn, text):
	# Generate tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error

	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program

	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
