from request_db import get_category, get_goods,\
    get_info_good, get_category_photo


class СonditionMachine():

    def __init__(self):
        self.actual_page = None
        self.page_photo = None
        self.page_butt_name = None
        self.page_back_condition = None
        self.page_discription = None
        self.level_page = None
        self.user_id = None
        self.state_stack = []
        self.basket = []
        self.add_butt_basket = False

    def get_context(self):
        context = {
            'actual_page': self.actual_page,
            'page_photo': self.page_photo,
            'page_butt_name': self.page_butt_name,
            'page_back_condition': self.page_back_condition,
            'level_page':  self.level_page,
            'state_stack': self.state_stack,
            'discription': self.page_discription,
            'add_butt_back': self.add_butt_back,
            'add_butt_basket': self.add_butt_basket
        }
        return context

    def start_page(self):
        self.actual_page = 'start_page'
        self.page_photo = '457239027'
        self.page_butt_name = ['Выбор категорий']
        self.page_discription = None
        self.level_page = 1
        self.state_stack.append(self.actual_page)
        self.add_butt_basket = False
        self.add_butt_back = False

    def categories_page(self):
        self.page_butt_name = [category['name'] for category in get_category()]
        self.page_photo = '457239031'
        self.page_back_condition = self.actual_page
        self.page_discription = None
        self.actual_page = 'category_page'
        self.level_page = 2
        self.state_stack.append(self.actual_page)
        self.add_butt_basket = False
        self.add_butt_back = True

    def goods_page(self, category_name):
        self.page_butt_name =\
            [good['name'] for good in get_goods(category_name)]
        self.page_photo = get_category_photo(category_name)
        self.page_back_condition = self.actual_page
        self.page_discription = None
        self.actual_page = category_name
        self.level_page = 3
        self.state_stack.append(self.actual_page)
        self.add_butt_basket = False
        self.add_butt_back = True

    def good_page(self, good_name):
        self.page_butt_name = ['add in basket']
        good = get_info_good(good_name)
        self.page_photo = good['photo']
        self.page_back_condition = self.actual_page
        self.page_discription = f"Discription: {good['discription']}, price: {good['price']}"
        self.actual_page = good_name
        self.level_page = 4
        self.state_stack.append(self.actual_page)
        self.add_butt_back = True

    def go_back(self):
        self.state_stack.pop()
        page_back = self.state_stack.pop()
        self.get_page_view(page_back)

    def get_page_view(self, status):
        level_page = len(self.state_stack)
        if status == 'Back':
            self.go_back()
        elif status == 'add in basket':
            self.basket.append(self.state_stack[-1])
            print(self.state_stack)
            pass
        elif level_page == 0:
            print('start start_page')
            self.start_page()
        elif level_page == 1:
            print('start categories_page')
            self.categories_page()
        elif level_page == 2:
            print('start goods_page')
            self.goods_page(status)
        elif level_page == 3:
            print('start good_page')
            self.good_page(status)
        return self.get_context()
