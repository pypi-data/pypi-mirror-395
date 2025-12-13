from os import getcwd
from gitlab_ps_utils.logger import myLogger
from gitlab_evaluate.lib.log_utils import get_log_level

log = myLogger(__name__, app_path=getcwd(), log_dir='.', log_name='evaluate')
log.setLevel(get_log_level())