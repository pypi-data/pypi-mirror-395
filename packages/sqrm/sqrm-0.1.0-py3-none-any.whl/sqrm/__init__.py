"""
SQRM - Simple QR Warehouse Management System
"""

import os
import inspect

def get_caller_directory():
    """获取调用者文件所在的目录"""
    frame = inspect.stack()[2]
    caller_file = frame[0].f_code.co_filename
    return os.path.dirname(os.path.abspath(caller_file))

from .core import WarehouseQRManager

# API functions
def reg(weight=None):
    """Register a new item"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    return manager.register_item(weight)

def in_(operator, weight=None):
    """Check in an item"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    manager.scan_qr_code("入库", operator, weight)

def out(operator, weight=None):
    """Check out an item"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    manager.scan_qr_code("出库", operator, weight)

def all():
    """View all items"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    manager.view_inventory()

def log():
    """View operation logs"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    manager.view_logs()

def del_():
    """Delete last operation record"""
    base_dir = get_caller_directory()
    manager = WarehouseQRManager(base_dir)
    manager.delete_last_record()

# Version
__version__ = "0.1.0"
__all__ = ['reg', 'in_', 'out', 'all', 'log', 'del_', 'WarehouseQRManager']