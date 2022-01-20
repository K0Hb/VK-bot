from machine import СonditionMachine
from request_db import get_all_name, get_category_photo, get_info_good


def test_machine():
    '''
    Небольшой тест, на работоспособность машины (проход от начала , до конца сценария).
    Так же частично проверяется работоспособность запросов в БД.
    '''
    rout_map = [('start', 1), ('categories_page', 2), ('category1', 3), ('good1', 4), ('Back', 3), ('Back', 2), ('Back', 1)]
    test_machine = СonditionMachine()
    for message, level_page in rout_map:
        test_machine.get_page_view(message)
        assert test_machine.level_page == level_page
        assert test_machine.page_photo != None


def test_db():
    '''
    Небольшой условный тест, проверяющий основные функции запросов бота в БД.
    Нобходимо, чтобы БД была минмально заполнена: одна категория(category1)
    и один товар(good1)
    '''
    assert len(get_all_name()) != 0
    assert type(get_category_photo('category1')) == str
    good_info = get_info_good('good1')
    assert good_info['id'] == 1
    assert type(good_info['discription']) == str
    assert good_info['discription'] != None
    assert type(good_info['discription']) == str
    assert good_info['discription'] != None
    assert good_info['category_id'] != None
    assert good_info['photo'] != None
