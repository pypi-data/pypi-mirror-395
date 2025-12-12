import qrcode
import cv2
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

class WarehouseQRManager:
    def __init__(self, base_dir=None):
        # 使用调用者文件所在的目录作为基础目录
        self.base_dir = base_dir
        self.items_file = os.path.join(base_dir, "warehouse_items.csv")
        self.log_file = os.path.join(base_dir, "inventory_log.csv")
        self.qr_code_dir = os.path.join(base_dir, "qr_codes")
        
        # 创建必要的目录
        if not os.path.exists(self.qr_code_dir):
            os.makedirs(self.qr_code_dir)
            
        self.initialize_files()
    
    def initialize_files(self):
        """初始化数据文件"""
        # 物品信息文件
        if not os.path.exists(self.items_file):
            df_items = pd.DataFrame(columns=[
                '物品ID', '物品重量(kg)', '注册日期', '二维码路径'
            ])
            df_items.to_csv(self.items_file, index=False, encoding='utf-8-sig')
        
        # 出入库记录文件
        if not os.path.exists(self.log_file):
            df_log = pd.DataFrame(columns=[
                '时间戳', '物品ID', '操作类型', '操作人员', '物品重量(kg)', '备注'
            ])
            df_log.to_csv(self.log_file, index=False, encoding='utf-8-sig')
    
    def register_item(self, weight=None):
        """物品注册功能"""
        print("\n=== 物品注册 ===")
        
        # 生成唯一物品ID
        item_id = f"ITEM_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        register_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 创建物品信息字典
        item_info = {
            '物品ID': item_id,
            '物品重量(kg)': weight,
            '注册日期': register_date
        }
        
        # 生成二维码
        qr_filename = self.generate_qr_code(item_info, item_id)
        item_info['二维码路径'] = qr_filename
        
        # 保存到CSV文件
        self.save_item_to_csv(item_info)
        
        print(f"\n物品注册成功!")
        print(f"物品ID: {item_id}")
        if weight is not None:
            print(f"物品重量: {weight}kg")
        print(f"二维码已保存: {qr_filename}")
        print(f"数据文件位置: {self.base_dir}")
        
        return item_id
    
    def generate_qr_code(self, item_info, item_id):
        """生成包含物品信息的二维码"""
        # 将物品信息转换为JSON格式
        qr_data = json.dumps(item_info, ensure_ascii=False)
        
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # 生成二维码图片
        filename = os.path.join(self.qr_code_dir, f"{item_id}.png")
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
        return filename
    
    def save_item_to_csv(self, item_info):
        """保存物品信息到CSV文件"""
        df = pd.read_csv(self.items_file, encoding='utf-8-sig')
        new_row = pd.DataFrame([item_info])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.items_file, index=False, encoding='utf-8-sig')
    
    def scan_qr_code(self, operation_type, operator, weight=None):
        """扫描二维码进行出入库操作"""
        print(f"\n=== {operation_type}操作 ===")
        print(f"操作人员: {operator}")
        if weight is not None:
            print(f"物品重量: {weight}kg")
        
        notes = input("请输入备注信息(可选): ")
        
        print(f"\n正在启动摄像头扫描二维码...")
        print("请将二维码对准摄像头，按 'q' 键退出扫描")
        
        # 初始化摄像头
        cap = cv2.VideoCapture(0)
        qr_detector = cv2.QRCodeDetector()
        
        scanned = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法访问摄像头")
                break
            
            # 检测并解码二维码
            data, bbox, _ = qr_detector.detectAndDecode(frame)
            
            if data and not scanned:
                try:
                    # 解析二维码数据
                    item_info = json.loads(data)
                    item_id = item_info.get('物品ID')
                    
                    print(f"\n扫描到物品 ID: {item_id}")
                    
                    # 记录出入库操作
                    self.log_operation(item_id, operation_type, operator, weight, notes)
                    scanned = True
                    
                    # 在图像上显示识别结果
                    cv2.putText(frame, f"识别成功: {item_id}", 
                               (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    cv2.imshow('QR Code Scanner', frame)
                    cv2.waitKey(2000)  # 显示2秒
                    break
                    
                except json.JSONDecodeError:
                    print("二维码数据解析失败")
                    break
            
            # 显示摄像头画面
            cv2.imshow('QR Code Scanner', frame)
            
            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if not scanned:
            print("未扫描到二维码")
    
    def log_operation(self, item_id, operation_type, operator, weight, notes):
        """记录出入库操作"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            '时间戳': timestamp,
            '物品ID': item_id,
            '操作类型': operation_type,
            '操作人员': operator,
            '物品重量(kg)': weight,
            '备注': notes
        }
        
        # 保存到日志文件
        df = pd.read_csv(self.log_file, encoding='utf-8-sig')
        new_row = pd.DataFrame([log_entry])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.log_file, index=False, encoding='utf-8-sig')
        
        print(f"{operation_type}操作已记录!")
        print(f"时间: {timestamp}")
        print(f"物品ID: {item_id}")
        print(f"操作人: {operator}")
        if weight is not None:
            print(f"物品重量: {weight}kg")
    
    def delete_last_record(self):
        """删除最后一条记录"""
        try:
            df = pd.read_csv(self.log_file, encoding='utf-8-sig')
            if df.empty:
                print("没有记录可删除")
                return
            
            # 获取最后一条记录
            last_record = df.iloc[-1]
            print("将要删除的记录:")
            print(f"时间: {last_record['时间戳']}")
            print(f"物品ID: {last_record['物品ID']}")
            print(f"操作类型: {last_record['操作类型']}")
            print(f"操作人员: {last_record['操作人员']}")
            
            confirm = input("确认删除这条记录? (y/n): ")
            if confirm.lower() == 'y':
                # 删除最后一行
                df = df[:-1]
                df.to_csv(self.log_file, index=False, encoding='utf-8-sig')
                print("记录已删除")
            else:
                print("取消删除")
                
        except FileNotFoundError:
            print("日志文件不存在")
        except Exception as e:
            print(f"删除记录时出错: {e}")
    
    def view_inventory(self):
        """查看当前库存"""
        print("\n=== 当前库存 ===")
        try:
            df = pd.read_csv(self.items_file, encoding='utf-8-sig')
            if df.empty:
                print("暂无物品注册")
            else:
                print(df.to_string(index=False))
        except FileNotFoundError:
            print("物品文件不存在")
    
    def view_logs(self):
        """查看出入库记录"""
        print("\n=== 出入库记录 ===")
        try:
            df = pd.read_csv(self.log_file, encoding='utf-8-sig')
            if df.empty:
                print("暂无出入库记录")
            else:
                print(df.to_string(index=False))
        except FileNotFoundError:
            print("日志文件不存在")
    
    def show_storage_info(self):
        """显示存储位置信息"""
        print(f"\n=== 存储位置信息 ===")
        print(f"数据存储目录: {self.base_dir}")
        print(f"物品信息文件: {self.items_file}")
        print(f"出入库记录文件: {self.log_file}")
        print(f"二维码图片目录: {self.qr_code_dir}")
        
        # 显示文件大小信息
        if os.path.exists(self.items_file):
            items_count = len(pd.read_csv(self.items_file))
            print(f"已注册物品数量: {items_count}")
        
        if os.path.exists(self.log_file):
            logs_count = len(pd.read_csv(self.log_file))
            print(f"出入库记录数量: {logs_count}")
        
        if os.path.exists(self.qr_code_dir):
            qr_count = len([f for f in os.listdir(self.qr_code_dir) if f.endswith('.png')])
            print(f"二维码图片数量: {qr_count}")

def main():
    """主函数 - 命令行交互界面"""
    import inspect
    # 获取调用者文件所在的目录
    frame = inspect.stack()[1]
    caller_file = frame[0].f_code.co_filename
    base_dir = os.path.dirname(os.path.abspath(caller_file))
    
    manager = WarehouseQRManager(base_dir)
    
    # 显示存储位置信息
    manager.show_storage_info()
    
    while True:
        print("\n=== 仓库二维码管理系统 ===")
        print("1. 物品注册")
        print("2. 入库扫描")
        print("3. 出库扫描")
        print("4. 查看库存")
        print("5. 查看出入库记录")
        print("6. 删除最后一条记录")
        print("7. 显示存储信息")
        print("8. 退出")
        
        choice = input("请选择操作(1-8): ")
        
        if choice == '1':
            weight_input = input("请输入物品重量(kg)(可选，直接回车跳过): ").strip()
            weight = float(weight_input) if weight_input else None
            manager.register_item(weight)
        elif choice == '2':
            operator = input("请输入操作人员姓名: ")
            weight_input = input("请输入物品重量(kg)(可选，直接回车跳过): ").strip()
            weight = float(weight_input) if weight_input else None
            manager.scan_qr_code("入库", operator, weight)
        elif choice == '3':
            operator = input("请输入操作人员姓名: ")
            weight_input = input("请输入物品重量(kg)(可选，直接回车跳过): ").strip()
            weight = float(weight_input) if weight_input else None
            manager.scan_qr_code("出库", operator, weight)
        elif choice == '4':
            manager.view_inventory()
        elif choice == '5':
            manager.view_logs()
        elif choice == '6':
            manager.delete_last_record()
        elif choice == '7':
            manager.show_storage_info()
        elif choice == '8':
            print("感谢使用仓库二维码管理系统!")
            break
        else:
            print("无效选择，请重新输入!")

if __name__ == "__main__":
    main()