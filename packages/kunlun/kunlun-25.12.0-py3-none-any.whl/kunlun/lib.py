from kunlun.job import util, vars

cn = vars.CONN_DICT
#
VERSION = vars.VERSION
USERNAME = vars.USERNAME
HOSTNAME = vars.HOSTNAME
HOME_PATH = vars.HOME_PATH
DATA_PATH = vars.DATA_PATH
TMP_PATH = vars.TMP_PATH
SCRIPT_PATH = vars.SCRIPT_PATH
TEST_PATH = vars.TEST_PATH
PROJECT_NAME = vars.PROJECT_NAME

CTRL_A = '\001'
CTRL_B = '\002'
CTRL_C = '\003'
CTRL_D = '\004'
CTRL_E = '\005'
CTRL_F = '\006'
CTRL_G = '\007'
#
CTRL_H = '\010'
CTRL_I = '\011'
CTRL_J = '\012'
CTRL_K = '\013'
CTRL_L = '\014'
CTRL_M = '\015'
CTRL_N = '\016'
CTRL_O = '\017'
#
CTRL_P = '\020'
CTRL_Q = '\021'
CTRL_R = '\022'
CTRL_S = '\023'
CTRL_T = '\024'
CTRL_U = '\025'
CTRL_V = '\026'
CTRL_W = '\027'
#
CTRL_X = '\030'
CTRL_Y = '\031'
CTRL_Z = '\032'
#
ESC = '\033'
BREAK_TELNET = '\035'
UP = '\x1b[A'
DOWN = '\x1b[B'
RIGHT = '\x1b[C'
LEFT = '\x1b[D'


def get_event_logger():
    return util.get_event_logger()


def get_container_name():
    return util.get_container_info('name')


def get_mode():
    return util.get_container_info('mode')


def set_display1(value):
    return util.set_container_info('display1', value)


def set_display2(value):
    return util.set_container_info('display2', value)


def set_display3(value):
    return util.set_container_info('display3', value)


def set_display4(value):
    return util.set_container_info('display4', value)


def set_display5(value):
    return util.set_container_info('display5', value)


def set_display6(value):
    return util.set_container_info('display6', value)


def set_step_name(name):
    return util.set_step_name(name)


def ask_question(question, **kwargs):
    return util.ask_question(question, **kwargs)


def ask_questions(questions, **kwargs):
    return util.ask_questions(questions, **kwargs)


def acquire_locking(name, wait_timeout=3600, privilege=False):
    util.acquire_queue(name, wait_timeout=wait_timeout, privilege=privilege)


def release_locking(name):
    util.release_queue(name)


class FIFOLocking(util.FIFOQueue):
    def __init__(self, name, wait_timeout=3600, privilege=False):
        super(FIFOLocking, self).__init__(name, wait_timeout=wait_timeout, privilege=privilege)


def fifo_locking(name, wait_timeout=3600, privilege=False):
    return util.fifo_queue(name, wait_timeout=wait_timeout, privilege=privilege)


def sync_up(group_name, wait_timeout=3600):
    return util.sync_up(group_name, wait_timeout=wait_timeout)


def set_cache(name, value):
    return util.set_cache(name, value)


def get_cache(name):
    return util.get_cache(name)


def get_sync_group(name):
    return util.get_sync_group(name)


def add_test_data(**kwargs):
    return util.add_test_data(**kwargs)


def get_sequence_definition(name='SEQUENCE', **kwargs):
    return util.get_sequence_definition(name=name, **kwargs)


def add_measure(name, value, **kwargs):
    return util.add_measure(name, value, **kwargs)
