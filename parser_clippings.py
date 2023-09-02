# 定义分隔符
import re
from hashlib import md5

DELIMITER = u"==========\n"

# 按照分隔符对所有标注进行分割，并存放在该数组中
all_marks = []

# 按照书籍来对标注进行分组存放
all_books = []


# 定义一个函数用于获取当前书籍在 all_books 列表中的索引
def get_book_index(book_name):
    """get book's index"""
    for i in range(len(all_books)):
        if all_books[i]["name"] == book_name:
            return i
    # 如果书籍并不存在，说明还没有插入该元素，就将该元素插入到最后一个元素
    return -1


# 定义渲染处理标注文本的函数
def render_clippings(file_name):
    global all_marks
    global all_books

    # 以 utf-8 格式打开标注文件并并将内容读取到 content 变量中
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()

    # 对读入的内容去除空行，即将 '\n\n' 替换为 '\n'，方便后续处理
    content = content.replace("\n\n", "\n")
    # 对去除空行的内容以分隔符进行分隔，得到的是一个列表，每个元素就是一个标注
    all_marks = content.split(DELIMITER)
    for i in range(len(all_marks)):
        # 以换行符进行分隔，将每个标注拆分成四个元素
        mark = all_marks[i].split("\n")
        # 如果该标注中元素的数量为 4 说明就是一个正确的标注，否则就是无效的
        if len(mark) == 4:

            if not len(mark[2].strip()):
                continue

            # 对标注的第一个元素，即书名部分进行 md5 计算，用于将它设置为后续的 url 路径，以及 html 文件名
            book_url = md5(mark[0].encode("utf-8")).hexdigest()
            # 去除掉书名中一些特殊的字符，用来拆分出简短的书名
            book_info = re.split(r"[()<>|\[\]（）《》【】｜]\s*", mark[0])
            # 获取书名，一般为第一个元素，目的是为了去除 kinlde 中文商店下载的又长又臭的书名
            book_name = book_info[0].strip() if str(book_info[0]) != "" else (mark[0])

            # 获取该书的作者
            book_author = book_info[-2] if len(book_info) > 1 else ""

            mark_info = mark[1].split("|")
            # 获取该书的标记时间和标注位置
            mark_time = mark_info[1]
            mark_address = mark_info[0].strip("- ")

            # 获取该标注的正文内容
            mark_content = mark[2]

            # 查询该书的列表索引，将该标记插入到该书的 marks 列表中
            book_index = get_book_index(book_name)
            if book_index == -1:
                all_books.append(
                    {
                        "name": book_name,
                        "author": book_author,
                        "url": book_url,
                        "nums": 0,
                        "marks": [],
                    }
                )
            all_books[book_index]["marks"].append(
                {"time": mark_time, "address": mark_address, "content": mark_content}
            )
            # 更新该书的标记数量
            all_books[book_index]["nums"] += 1
        # 使用 lambda 函数以标注数量为 key 对所有书籍进行倒序排序
    all_books.sort(key=lambda x: x["nums"], reverse=True)


clippings_file = 'My Clippings.txt'
render_clippings(clippings_file)

for book in all_books:
    file_path = book['name'] + '.md'

    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write('# ')
        f.write(book['name'])
        f.write('\n')
        f.write('author:: ')
        f.write(book['author'])
        f.write('\n')

        for mark in book['marks']:
            f.write('- ')
            f.write(mark['content'])
            f.write('\n')

