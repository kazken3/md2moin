import re
import sys
import os

def markdown_to_moinmoin(markdown_text):
    # 見出し変換
    moinmoin_text = re.sub(r'^(#)\s(.+)$', r'= \2 =', markdown_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(##)\s(.+)$', r'== \2 ==', moinmoin_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(###)\s(.+)$', r'=== \2 ===', moinmoin_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(####)\s(.+)$', r'==== \2 ====', moinmoin_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(#####)\s(.+)$', r'===== \2 =====', moinmoin_text, flags=re.MULTILINE)



    # 強調変換
    moinmoin_text = re.sub(r'(\*\*|__)(.+?)\1', r"'''\2'''", moinmoin_text)
    # アンダースコアはダメ
  　　　　# moinmoin_text = re.sub(r'(\*|_)(.+?)\1', r"''\2''", moinmoin_text)

    # リンク変換
    moinmoin_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[[\2 | \1]]', moinmoin_text)

    # 水平線変換
    moinmoin_text = re.sub(r'^-+$', r'----', moinmoin_text, flags=re.MULTILINE)

    # 順序なしリスト変換
    moinmoin_text = re.sub(r'^(\s*\*)\s(.+)$', r'\1 \2', moinmoin_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(\*)\s(.+)$', r' \1 \2', moinmoin_text, flags=re.MULTILINE)
    moinmoin_text = re.sub(r'^(\s*\-)\s(.+)$', r' * \2', moinmoin_text, flags=re.MULTILINE)

    # 順序付きリスト変換
    moinmoin_text = re.sub(r'^(\s*\d+\.\s+)(.+)$', r'\1\2', moinmoin_text, flags=re.MULTILINE)

    # コードブロック変換
    moinmoin_text = re.sub(r'^```(\w+)?\n(.+?)\n```$', r'{{{\1\n\2\n}}}', moinmoin_text, flags=re.MULTILINE | re.DOTALL)

    return moinmoin_text

if __name__ == "__main__":
    # 入力ファイルが指定されていない場合はエラーメッセージを表示して終了
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <markdown_file>")
        sys.exit(1)

    # 入力ファイル名
    input_file = sys.argv[1]

    # 入力ファイルが存在しない場合もエラーメッセージを表示して終了
    if not os.path.isfile(input_file):
        print(f"Error: File {input_file} does not exist")
        sys.exit(1)

    # 出力ファイル名を作成 (入力ファイル名 + .moin拡張子)
    output_file = os.path.splitext(input_file)[0] + ".moin"

    # 入力ファイルを読み込んで変換
    with open(input_file, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    moinmoin_text = markdown_to_moinmoin(markdown_text)

    # 変換結果を出力ファイルに書き込む
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(moinmoin_text)

    print(f"Conversion completed. Output saved to {output_file}")
