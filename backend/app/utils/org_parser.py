import re
from typing import List, Dict, Any

class OrgNode:
    def __init__(self, type: str, content: str, level: int = 0):
        self.type = type
        self.content = content
        self.level = level
        self.children: List[OrgNode] = []
        self.properties: Dict[str, Any] = {}

class OrgParser:
    def __init__(self):
        self.content = ""
        self.root = OrgNode("root", "")
        
    def parse(self, content: str) -> OrgNode:
        self.content = content
        lines = content.split('\n')
        current_node = self.root
        stack = [self.root]
        
        for line in lines:
            if not line.strip():
                continue
                
            # 헤딩 파싱
            if line.startswith('*'):
                level = len(re.match(r'\*+', line).group())
                title = line.strip('* ').strip()
                node = OrgNode("heading", title, level)
                
                while stack and stack[-1].level >= level:
                    stack.pop()
                
                if stack:
                    stack[-1].children.append(node)
                stack.append(node)
                current_node = node
                
            # TODO 항목 파싱
            elif line.strip().startswith('- [ ]') or line.strip().startswith('- [X]'):
                done = line.strip().startswith('- [X]')
                content = line.strip()[5:].strip()
                node = OrgNode("todo", content)
                node.properties["done"] = done
                current_node.children.append(node)
                
            # 리스트 항목 파싱
            elif line.strip().startswith('-'):
                content = line.strip()[1:].strip()
                node = OrgNode("list_item", content)
                current_node.children.append(node)
                
            # 일반 텍스트
            else:
                node = OrgNode("text", line.strip())
                current_node.children.append(node)
                
        return self.root

    def to_html(self, node: OrgNode = None) -> str:
        if node is None:
            node = self.root
            
        html = []
        
        for child in node.children:
            if child.type == "heading":
                h_level = min(child.level + 1, 6)  # h1 ~ h6
                html.append(f"<h{h_level}>{child.content}</h{h_level}>")
                html.append(self.to_html(child))
                
            elif child.type == "todo":
                checked = ' checked' if child.properties.get("done") else ''
                html.append(
                    f'<div class="todo-item">'
                    f'<input type="checkbox"{checked}>'
                    f'<span>{child.content}</span>'
                    f'</div>'
                )
                
            elif child.type == "list_item":
                html.append(f"<li>{child.content}</li>")
                
            elif child.type == "text":
                # 인라인 마크업 처리
                content = self._process_inline_markup(child.content)
                html.append(f"<p>{content}</p>")
                
        return '\n'.join(html)
    
    def _process_inline_markup(self, text: str) -> str:
        # 볼드 처리
        text = re.sub(r'\*([^*]+)\*', r'<strong>\1</strong>', text)
        # 이탤릭 처리
        text = re.sub(r'/([^/]+)/', r'<em>\1</em>', text)
        # 코드 처리
        text = re.sub(r'~([^~]+)~', r'<code>\1</code>', text)
        return text 