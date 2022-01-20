from word_db import get_category, get_goods, get_price_good, get_category_photo


class СonditionMachine():

    def __init__(self):
        self.actual_page = None
        self.page_photo = None
        self.page_butt_name = None
        self.page_back_condition = None
        self.page_discription = None
        self.level_page = None
        self.user_id = None

    def get_context(self):
        context = {
            'actual_page': self.actual_page,
            'page_photo': self.page_photo,
            'page_butt_name': self.page_butt_name,
            'page_back_condition': self.page_back_condition,
            'level_page':  self.level_page,
        }
        return context

    def start_page(self):
        self.actual_page = 'start_page'
        self.page_photo = '457239027'
        self.page_butt_name = ['Выбор категорий',]
        self.level_page = 1

    def categories_page(self):
        self.page_butt_name = [category['name'] for category in get_category()]
        self.page_photo = '457239031'
        self.page_back_condition = self.actual_page
        self.actual_page = 'category_page' #fix me
        self.level_page = 2

    def goods_page(self, category_name):
        self.page_butt_name = [good['name'] for good in get_goods(category_name)]
        self.page_photo = get_category_photo(category_name)
        self.page_back_condition = self.actual_page
        self.actual_page = category_name
        self.level_page = 3

    def good_page(self, good_name):
        good = get_price_good(good_name)[0]
        self.page_photo = good['photo']
        self.page_back_condition = self.actual_page
        self.page_discription = good['discription']
        self.actual_page = good_name
        self.level_page = 4

    def go_back(self):
        self.level_page = self.level_page - 2

    def get_page_view(self, status):
        if status == 'Back':
            self.go_back()
            self.get_page_view(self.page_back_condition)
        elif self.level_page == None:
            self.start_page()
        elif self.level_page == 1:
            self.categories_page()
        elif self.level_page == 2:
            self.goods_page(status)
        elif self.level_page == 3:
            self.good_page(status)
        return self.get_context()

# lol = СonditionMachine()
# lol.get_page_view('start')
# print(lol.get_context())
# print('-'*50)
# lol.get_page_view('categories_page')
# print(lol.get_context())
# print('-'*50)
# lol.get_page_view('category1')
# print(lol.get_context())
# print('-'*50)
# lol.get_page_view('good1')
# print(lol.get_context())
# print('-'*50)
# lol.get_page_view('Back')
# print(lol.get_context())
# print('-'*50)
# lol.get_page_view('Back')
# print(lol.get_context())
# print('-'*50)

scanery = ({'start_page': ({'category_page': ({'category1':
                                                   ({'good1': None}, {'good2': None}, {'good3': None})},
                                              {'category2':
                                                   ({'good4': None}, {'good5': None}, {'good6': None})},
                                              {'category3':
                                                   ({'good7': None}, {'good8': None}, {'good9': None})})
                            })
            })
