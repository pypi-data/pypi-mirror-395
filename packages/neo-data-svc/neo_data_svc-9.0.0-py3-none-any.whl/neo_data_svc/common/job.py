import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from . import system as NDP_sys

_logger = logging.getLogger(__name__)

_bs = BackgroundScheduler(timezone=NDP_sys.tz)
atexit.register(lambda: stop())


def add(job, now=False, trigger='cron', **a):
    if not _bs.running:
        try:
            _bs.start()
            _logger.info("✅ 已启动")
        except Exception as e:
            _logger.error(f"❌ 启动失败: {e}")

    if now:
        _bs.add_job(job, 'date', run_date=NDP_sys.get_now(), max_instances=1)
    return _bs.add_job(job, trigger, max_instances=1, **a)


def stop(wait=True):
    if _bs.running:
        _logger.debug(f"🛑 正在关闭...")
        _bs.shutdown(wait=wait)
        _logger.debug("✅ 已关闭")


def pause():
    _bs.pause()
    _logger.debug("⏸️ 已暂停")


def resume():
    _bs.resume()
    _logger.debug("▶️ 已恢复")