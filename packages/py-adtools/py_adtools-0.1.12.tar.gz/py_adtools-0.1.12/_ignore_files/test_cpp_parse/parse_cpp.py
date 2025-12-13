from tree_sitter import Language, Parser
import tree_sitter_cpp
import os


class SimpleCppParser:
    def __init__(self):
        """初始化C++解析器"""
        self.cpp_language = Language(tree_sitter_cpp.language())
        self.parser = Parser(self.cpp_language)
        # self.parser.set_language(self.cpp_language)

    def read_cpp(self, filename):
        """读取C++文件"""
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_file(self, filename):
        """解析C++文件并提取组件"""
        code = self.read_cpp(filename)
        tree = self.parser.parse(bytes(code, "utf-8"))
        root_node = tree.root_node

        # 按行分割代码
        code_lines = code.split("\n")

        functions = []
        classes = []
        structs = []
        scripts = []

        # 遍历所有子节点
        for child_node in root_node.children:
            node_type = child_node.type

            # 跳过空的或无关紧要的节点
            if self.should_skip_node(child_node, code_lines):
                continue

            # 提取函数定义
            if node_type == "function_definition":
                self.extract_function(child_node, code_lines, code, functions)

            # 提取模板函数定义
            elif node_type == "template_declaration":
                function_node = self.find_function_in_template(child_node)
                if function_node:
                    self.extract_function(function_node, code_lines, code, functions, is_template=True)
                else:
                    self.extract_script(child_node, code_lines, scripts)

            # 提取类定义
            elif node_type == "class_specifier":
                self.extract_class(child_node, code_lines, code, classes, "class")

            # 提取结构体定义
            elif node_type == "struct_specifier":
                self.extract_class(child_node, code_lines, code, structs, "struct")

            # 其他节点类型（脚本部分）
            else:
                self.extract_script(child_node, code_lines, scripts)

        return {
            'functions': functions,
            'classes': classes,
            'structs': structs,
            'scripts': scripts
        }

    def should_skip_node(self, node, code_lines):
        """判断是否应该跳过这个节点"""
        start_line = node.start_point[0]
        end_line = node.end_point[0]

        # 获取节点文本
        if start_line == end_line:
            node_text = code_lines[start_line].strip()
        else:
            node_text = code_lines[start_line].strip()

        # 跳过只有分号或大括号的节点
        skip_patterns = ['};', ';', '}', '{']
        if node_text in skip_patterns:
            return True

        # 跳过空的注释节点
        if node.type == "comment" and not node_text:
            return True

        return False

    def find_function_in_template(self, template_node):
        """在模板声明中查找函数定义"""
        for child in template_node.children:
            if child.type == "function_definition":
                return child
        return None

    def extract_function(self, function_node, code_lines, source_code, functions_list, is_template=False):
        """提取函数定义"""
        start_line = function_node.start_point[0]
        end_line = function_node.end_point[0]

        # 获取函数代码
        if start_line != end_line:
            function_code = "\n".join(code_lines[start_line:end_line + 1])
        else:
            function_code = code_lines[start_line]

        # 提取函数名
        function_name = self.extract_function_name(function_node, source_code)

        function_type = 'template_function' if is_template else 'function'

        functions_list.append({
            'name': function_name,
            'type': function_type,
            'code': function_code,
            'start_line': start_line + 1,
            'end_line': end_line + 1
        })

    def extract_class(self, class_node, code_lines, source_code, classes_list, class_type):
        """提取类/结构体定义"""
        start_line = class_node.start_point[0]
        end_line = class_node.end_point[0]

        # 获取类代码
        if start_line != end_line:
            class_code = "\n".join(code_lines[start_line:end_line + 1])
        else:
            class_code = code_lines[start_line]

        # 提取类名
        class_name = self.extract_class_name(class_node, source_code)

        classes_list.append({
            'name': class_name,
            'type': class_type,
            'code': class_code,
            'start_line': start_line + 1,
            'end_line': end_line + 1
        })

    def extract_script(self, script_node, code_lines, scripts_list):
        """提取脚本部分"""
        start_line = script_node.start_point[0]
        end_line = script_node.end_point[0]

        # 获取脚本代码
        if start_line != end_line:
            script_code = "\n".join(code_lines[start_line:end_line + 1])
        else:
            script_code = code_lines[start_line]

        # 跳过空的或只有标点符号的脚本
        script_text = script_code.strip()
        if not script_text or script_text in ['};', ';', '}', '{']:
            return

        scripts_list.append({
            'name': f"script_{len(scripts_list) + 1}",
            'type': 'script',
            'code': script_code,
            'start_line': start_line + 1,
            'end_line': end_line + 1
        })

    def extract_function_name(self, function_node, source_code):
        """提取函数名"""
        # 查找函数声明器
        for child in function_node.children:
            if child.type == "function_declarator":
                # 在函数声明器中查找标识符
                for grandchild in child.children:
                    if grandchild.type == "identifier":
                        start_byte = grandchild.start_byte
                        end_byte = grandchild.end_byte
                        return source_code[start_byte:end_byte]
        return "unknown"

    def extract_class_name(self, class_node, source_code):
        """提取类/结构体名"""
        # 查找名称字段
        for child in class_node.children:
            if child.type == "type_identifier":
                start_byte = child.start_byte
                end_byte = child.end_byte
                return source_code[start_byte:end_byte]
        return "unknown"

    def print_results(self, analysis_result):
        """打印分析结果"""
        print(f"找到 {len(analysis_result['functions'])} 个函数:")
        for func in analysis_result['functions']:
            print(f"  {func['type']}: {func['name']} (行 {func['start_line']}-{func['end_line']})")

        print(f"\n找到 {len(analysis_result['classes'])} 个类:")
        for cls in analysis_result['classes']:
            print(f"  {cls['type']}: {cls['name']} (行 {cls['start_line']}-{cls['end_line']})")

        print(f"\n找到 {len(analysis_result['structs'])} 个结构体:")
        for struct in analysis_result['structs']:
            print(f"  {struct['type']}: {struct['name']} (行 {struct['start_line']}-{struct['end_line']})")

        print(f"\n找到 {len(analysis_result['scripts'])} 个脚本块:")
        for script in analysis_result['scripts']:
            print(f"  脚本: {script['name']} (行 {script['start_line']}-{script['end_line']})")

    def save_components(self, analysis_result, output_dir="cpp_components"):
        """将提取的组件保存到单独的文件"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存函数
        for i, func in enumerate(analysis_result['functions']):
            safe_name = "".join(c for c in func['name'] if c.isalnum() or c in ('_', '-')).rstrip()
            if not safe_name:
                safe_name = f"unnamed_{i + 1}"

            filename = f"{output_dir}/{func['type']}_{safe_name}_{i + 1}.cpp"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"// {func['type']}: {func['name']}\n")
                f.write(f"// 位置: 行 {func['start_line']}-{func['end_line']}\n")
                f.write("//" + "=" * 40 + "\n")
                f.write(func['code'])
            print(f"保存{func['type']}到: {filename}")

        # 保存类
        for i, cls in enumerate(analysis_result['classes']):
            safe_name = "".join(c for c in cls['name'] if c.isalnum() or c in ('_', '-')).rstrip()
            if not safe_name:
                safe_name = f"unnamed_{i + 1}"

            filename = f"{output_dir}/{cls['type']}_{safe_name}_{i + 1}.cpp"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"// {cls['type']}: {cls['name']}\n")
                f.write(f"// 位置: 行 {cls['start_line']}-{cls['end_line']}\n")
                f.write("//" + "=" * 40 + "\n")
                f.write(cls['code'])
            print(f"保存{cls['type']}到: {filename}")

        # 保存结构体
        for i, struct in enumerate(analysis_result['structs']):
            safe_name = "".join(c for c in struct['name'] if c.isalnum() or c in ('_', '-')).rstrip()
            if not safe_name:
                safe_name = f"unnamed_{i + 1}"

            filename = f"{output_dir}/{struct['type']}_{safe_name}_{i + 1}.cpp"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"// {struct['type']}: {struct['name']}\n")
                f.write(f"// 位置: 行 {struct['start_line']}-{struct['end_line']}\n")
                f.write("//" + "=" * 40 + "\n")
                f.write(struct['code'])
            print(f"保存{struct['type']}到: {filename}")

        # 保存脚本
        for i, script in enumerate(analysis_result['scripts']):
            filename = f"{output_dir}/script_{script['name']}_{i + 1}.cpp"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"// 脚本: {script['name']}\n")
                f.write(f"// 位置: 行 {script['start_line']}-{script['end_line']}\n")
                f.write("//" + "=" * 40 + "\n")
                f.write(script['code'])
            print(f"保存脚本到: {filename}")


def main():
    """主函数"""
    parser = SimpleCppParser()

    # 要解析的C++文件路径
    cpp_file = "example.cpp"

    if not os.path.exists(cpp_file):
        # 如果文件不存在，创建一个示例文件
        with open(cpp_file, 'w', encoding='utf-8') as f:
            f.write("""#include <iostream>
#include <string>

using namespace std;

// 全局变量
int global_var = 42;

// 函数声明
void print_message(const string& message);

// 类定义
class Calculator {
private:
    double result;

public:
    Calculator() : result(0) {}

    double add(double a, double b) {
        return a + b;
    }

    double multiply(double a, double b) {
        return a * b;
    }

    double get_result() const {
        return result;
    }
};

// 结构体定义
struct Point {
    int x;
    int y;

    Point(int x, int y) : x(x), y(y) {}
};

// 函数定义
void print_message(const string& message) {
    cout << "Message: " << message << endl;
}

template<typename T>
T max_value(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    Calculator calc;
    Point p(10, 20);

    cout << "Addition: " << calc.add(5, 3) << endl;
    print_message("Hello, World!");

    return 0;
}
""")
        print(f"已创建示例文件: {cpp_file}")

    # 分析代码
    try:
        print(f"正在分析文件: {cpp_file}")
        print("=" * 50)

        result = parser.parse_file(cpp_file)
        parser.print_results(result)

        print("\n保存提取的组件...")
        parser.save_components(result)

    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()