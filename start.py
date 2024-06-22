import random
from claude_adapter import ClaudeAdapter
from llama_cpp_adapter import LlamaCppAdapter
from colorama import init, Fore, Style

# coloramaの初期化
init()

class ElementManager:
    def __init__(self) -> None:
        self.llm = LlamaCppAdapter()
        self.primitive_element = set(["木", "土", "金", "火", "水"])
        self.object_element:set[str] = set(self.primitive_element)
        self.primitive_recipe = {
            frozenset(["木", "土"]): "根",
            frozenset(["木", "火"]): "灰",
            frozenset(["木", "金"]): "樹液",
            frozenset(["木", "水"]): "流木",
            frozenset(["火", "土"]): "煙",
            frozenset(["火", "金"]): "熔岩",
            frozenset(["火", "水"]): "蒸気",
            frozenset(["土", "金"]): "粘土",
            frozenset(["土", "水"]): "泥",
            frozenset(["金", "水"]): "鏡",
            frozenset(["粘土", "木"]): "植物",
            frozenset(["植物", "水"]): "藻類",
            frozenset(["藻類", "火"]): "原始スープ",
            frozenset(["原始スープ", "金"]): "アミノ酸",
            frozenset(["アミノ酸", "火"]): "タンパク質",
            frozenset(["タンパク質", "水"]): "命",
            frozenset(["木", "命"]): "果実",
            frozenset(["火", "命"]): "精霊",
            frozenset(["土", "命"]): "種",
            frozenset(["金", "命"]): "道具",
            frozenset(["水", "命"]): "魚",
            frozenset(["魚", "種"]): "両生類",
            frozenset(["種", "精霊"]): "人間",
            frozenset(["精霊", "道具"]): "魔法使い"
        }
        # やったことの履歴の保持
        self.history = []
    def generate_element(self,element1:str, element2:str):
        # もし既存のレシピにあるが、まだobject_elementにないものであれば追加してそのまま返す
        recipe_key = frozenset([element1, element2])
        if recipe_key in self.primitive_recipe:
            recipe_check = self.primitive_recipe[recipe_key]
            if recipe_check not in self.object_element:
                print(Fore.GREEN + f"新しい要素が発見されました！-> {recipe_check}" + Style.RESET_ALL)
                self.object_element.add(recipe_check)
                self.history.append(f"{element1}+{element2}={recipe_check}")
                return recipe_check
        try:
            # レシピをテキストに変換する。
            recipe_text = "\n".join([f"A: {list(pair)[0]}, B: {list(pair)[1]}, C: {element}" for pair, element in self.primitive_recipe.items()])
            prompt = f"あなたはAの概念とBの概念を掛け合わせて新しい概念Cを出力します。事前に作ったレシピを参考に、もしこのパターンにないものであった場合は新しい概念を法則に基づいて出力する。[レシピ]{recipe_text}\n理由は書かず、出力結果のみを出力する。\n[input]\nA:木\nB:土\n[output]\nC:根\n[input]\nA:種\nB:精霊\n[output]\nC:人間\n[input]\nA:{element1}\nB:{element2}\n[output]\nC:"
            res = self.llm.generate(prompt)
            res_text:str = res
            recipe_check = self._add_recipe(element1, element2, res_text)
            if recipe_check is not True:
                print(f"このレシピは既に存在しています: {element1} -> {element2} -> {recipe_check}")
                return None
            self.object_element.add(res_text)
            self.history.append(f"{element1}+{element2}={res_text}")
            print(Fore.GREEN + f"新しい要素が発見されました！-> {res_text}" + Style.RESET_ALL)
            return res_text
        except Exception as e:
            print(Fore.RED + f"エラーが発生しました: {e}" + Style.RESET_ALL)


    def _add_recipe(self, element1:str, element2:str, element3:str)-> str|bool:
        key = frozenset([element1, element2])
        if key in self.primitive_recipe:
            # 既存のレシピがある場合は、そのレシピを返す。
            return self.primitive_recipe[key]
        self.primitive_recipe[key] = element3
        return True

    def remove_element(self,element:str) -> bool:
        # もしprimitive_elementにある場合は削除しない
        if element in self.primitive_element:
            return False
        self.object_element.remove(element)
        return True

class GameManager:
    selected_elements = [None, None]
    difficult_goals = ["恒星間航行の実現","時空の操作","多次元宇宙の探索","集合意識の作成","物質創造エンジンの作成"]
    easy_goals = ["蒸気期間の発明","飛行機の発明","チョコレートの作成","車の発明","空を飛ぶ","LLMの発明"]

    def __init__(self) -> None:
        try:
            self.claude = ClaudeAdapter()
        except ValueError as e:
            print(Fore.RED + f"エラーが発生しました: {e}" + Style.RESET_ALL)
            self.claude = LlamaCppAdapter()
        print(Fore.CYAN,"起動中…")
        self.element_manager = ElementManager()
        print(Fore.GREEN + "--- Primitive God ---" + Style.RESET_ALL)
        print("--- ルール ---")
        print("あなたは神に任命されました。今からあなたは世界に新しいものを創造していきます。")
        print("二つの要素を掛け合わせて、色々なものを創造しましょう。")
            # 二分の一でeasyかdifficult
        self.goals = self.easy_goals if random.randint(0, 1) == 0 else self.difficult_goals
        self.goal = random.choice(self.goals)
    def start(self):
        game_turn = 0
        while(True):
            game_turn += 1
            print(f"今回のゴール：{self.goal}")
            print(f"---ゲームターン：{game_turn}---")
            # 過去3回分の履歴を表示
            print("---履歴---")
            for i, history in enumerate(self.element_manager.history[-3:]):
                print(f"{i}: {history}")
            print("---")
            self._add_element()
            if game_turn % 5 == 0:
                print(Fore.CYAN,"---試験時間がやってきました---" + Style.RESET_ALL)
                print(Fore.CYAN + f"要素を梱包し、Claudeくんに{self.goal}が可能かを判断してもらいます…" + Style.RESET_ALL)
                self._evaluate_goal()


    def _add_element(self):
        for i, element in enumerate(self.element_manager.object_element):
            print(f"{i}: {element}")
        try:
            print("---")
            print("要素を二つ選択してください。")
            self.selected_elements[0] = list(self.element_manager.object_element)[int(input("最初の要素の番号を入力してください: "))]
            self.selected_elements[1] = list(self.element_manager.object_element)[int(input("二番目の要素の番号を入力してください: "))]
        except (ValueError, IndexError):
            print("無効な入力です。")
            return
        print(Fore.CYAN + f"選択された要素: {self.selected_elements[0]}と{self.selected_elements[1]}" + Style.RESET_ALL)
        print("新しい要素を生成中...")
        self.element_manager.generate_element(self.selected_elements[0], self.selected_elements[1])

    def _evaluate_goal(self):
        # もしゴールがたっせいできなかったら削除
        prompt = f"あなたは判定員です。列挙する要素しかない世界で{self.goal}を現実的に実現できるかを判断する必要があります。例えば発電機と人がいれば、発電が可能になります。発電機と人だけがいても、集合意識の作成や時空の操作はできません。まずどの要素（例えば人や新しい種族）がそれを作り、具体的に技術を利用して作れるか（つまり植物があっても薪がなければ利用できることになりません。なるべく要素は具体的である必要があります）を判断してください。達成するには主語と述語が必要になります。（木材があっても人がいなければ意味がないし、人や魔法使いがいなければ車の発明はできない）その上でこれをTrue、Falseで判断を出力したあとに理由を100文字程度で出力してください。TrueかFalseかは必ず表示すること。\n要素:{self.element_manager.object_element}"
        res = self.claude.generate(prompt,max_new_tokens=300)
        print(res)
        # resの中にTrueがあるかを確認
        if "True" in res:
            print(Fore.GREEN + "成功！" + Style.RESET_ALL)
            is_valid = True 
        else:
            print(Fore.RED + "失敗！" + Style.RESET_ALL)
            is_valid = False
        if is_valid == False:
            # 削除対象はobject_elementで、かつprimitive_elementでないもの
            removable_elements = self.element_manager.object_element - self.element_manager.primitive_element
            print(removable_elements)
            remove_element = random.choice(list(removable_elements))
            self.element_manager.remove_element(remove_element)
            print(Fore.RED + f"失敗！挑戦中に{remove_element}を失ってしまいました。" + Style.RESET_ALL)
        pass
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start()

