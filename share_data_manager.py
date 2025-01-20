import json
import os

SHARE_DATA_PATH = os.environ.get("SHARE_DATA_PATH", "./config/share_data.json")


class DataHandler:
    # 定义一个类属性，所有实例共享这个字典
    fid_to_object = {}
    data_item = {
        "fid": "",
        "title": "",
        "path": "",
        "share_url": "",
        "shareurl_ban": "",
        "share_text": ""
    }

    def __init__(self):
        self.load_from_file(SHARE_DATA_PATH)


    def load_data(self, json_data):
        """加载JSON数据并填充到类属性fid_to_object中"""
        data_list = json.loads(json_data)
        self.fid_to_object = {item['fid']: item for item in data_list}


    def get_object_by_fid(self, fid):
        """根据fid获取对应的对象"""
        return self.fid_to_object.get(fid)


    def get_shareurl_ban_by_fid(self, fid):
        """根据fid获取shareurl_ban值"""
        obj = self.get_object_by_fid(fid)
        return obj['shareurl_ban'] if obj else None


    def add_item(self, item, flush):
        """
        添加一个新的项目到fid_to_object字典。
        参数：
        - item: 包含'fid'键的字典，代表要添加的对象。
        """
        fid = str(item.get('fid'))
        if fid:
            self.fid_to_object[fid] = item
            print(f"已添加项，fid={fid}")
        else:
            print("无法添加项，缺少'fid'键")
        if flush:
            self.save_to_file()



    def remove_item(self, fid):
        """
        从fid_to_object字典中移除指定fid的项目。
        参数：
        - fid: 要移除的项目的fid。
        """
        fid_str = str(fid)  # 确保fid是字符串类型
        removed = self.fid_to_object.pop(fid_str, None)
        if removed:
            print(f"已移除项，fid={fid_str}")
        else:
            print(f"未找到fid为{fid_str}的项")

    def update_item(self, fid, name, value):
        """
        更新字典中的属性
        :param fid:
        :param name:
        :param value:
        :return:
        """
        fid_str = str(fid)
        obj = self.get_object_by_fid(fid_str)
        if obj:
            obj[name] = value
            self.fid_to_object[fid_str] = obj
            self.save_to_file()
        else:
            print(f"未找到fid为{fid_str}的项")


    def save_to_file(self, file_path=None):
        """
        将fid_to_object字典保存到指定的JSON文件中。
        参数：
        - file_path: JSON文件路径，默认使用实例初始化时设置的路径。
        """
        if file_path is None:
            file_path = getattr(self, 'file_path', SHARE_DATA_PATH)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.fid_to_object.values()), f, ensure_ascii=False, indent=4)
        print(f"数据已保存到文件: {file_path}")


    def load_from_file(self, file_path=None):
        """
        从指定的JSON文件加载数据到fid_to_object字典。
        参数：
        - file_path: JSON文件路径，默认使用实例初始化时设置的路径。
        """
        if file_path is None:
            file_path = getattr(self, 'file_path', SHARE_DATA_PATH)

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data_list = json.load(f)
                    # print("从文件加载的数据:", data_list)  # 调试信息

                    # 检查data_list是否是列表，并且每个元素都是字典
                    if isinstance(data_list, list) and all(isinstance(item, dict) for item in data_list):
                        self.fid_to_object = {item['fid']: item for item in data_list}
                    else:
                        print("警告: 文件中的数据格式不正确，不是包含字典的列表")
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
            except KeyError as e:
                print(f"键错误: {e}，某些项缺少'fid'键")
        else:
            print(f"文件不存在: {file_path}")


# 示例用法：
if __name__ == "__main__":
    # 初始化DataHandler类，并尝试加载现有数据
    handler = DataHandler()

    # 添加新项
    new_item = {
        "fid": "3aaa",
        "title": "3标题",
        "path": "3path",
        "share_url": "3链接",
        "shareurl_ban": "3错误信息",
        "share_text": "3文本"
    }
    handler.add_item(new_item, False)

    # 移除项
    handler.remove_item('2aa')

    # 保存当前状态到文件
    handler.save_to_file()

    # 打印当前状态
    print(handler.fid_to_object)

    # 模拟程序重启，重新加载数据
    print("\n模拟程序重启，重新加载数据")
    handler = DataHandler()
    print(handler.fid_to_object)
