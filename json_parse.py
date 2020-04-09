import json


class RegisterJson:
    def __init__(self, jsonPath):
        print("RegisterJson __init__")
        self.register_cfg_file_path = './register_cfg.json'
        self.register_value_file_path = './register_value.json'
        self.json_reg_cfg_data = self.read_json(self.register_cfg_file_path)
        self.json_reg_value_data = self.read_json(self.register_value_file_path)
        self.addr_byte_len = int(self.json_reg_cfg_data["total_cfg"]["addr_byte_len"])
        self.data_byte_len = int(self.json_reg_cfg_data["total_cfg"]["data_byte_len"])
        #self.addr_count    = len(self.json_reg_cfg_data)
        self.cfg_addr_list     = []
        self.get_all_cfg_addr_list()
        self.value_addr_list     = []
        self.get_all_value_addr_list()

        self.update_addr_value()
        self.save_all_data()

    def update_addr_value(self):# 更新 cfg文件中 addr地址上的值
        for k,v in self.json_reg_value_data.items():
            if k in self.cfg_addr_list:#更新cfg文件已经有的地址
                self.json_reg_cfg_data[k]["value"] = v
            else:#向cfg文件中新增配置项
                self.json_reg_cfg_data[k] = {}
                self.json_reg_cfg_data[k]["value"] = v
                self.json_reg_cfg_data[k]["bit_len"] = "32"
                self.json_reg_cfg_data[k]["region"] = []
                print(k,self.json_reg_cfg_data[k])


        self.get_all_value_addr_list()

    def get_all_value_addr_list(self):#获取value文件中的所有地址
        for k,v in self.json_reg_value_data.items():
            self.value_addr_list.append(k)

    def read_json(self,path):
        with open(path, 'r') as f:
            data = json.load(f)
            f.close()
            return data

    def write_json(self,data,path):
        with open(path, 'w') as f:
            #print("&"*20)
            #print(type(self.json_reg_cfg_data))
            string = str(data).replace("'",'"')#str(self.json_reg_cfg_data).replace("'",'"')#单引号替换为双引号
            #print(string)
            data = json.loads(string)
            #print("*"*20)
            json.dump(data,f,indent=4)
            f.close()
    def save_all_data(self):
        self.write_json(self.json_reg_cfg_data,self.register_cfg_file_path)
        self.write_json(self.json_reg_value_data,self.register_value_file_path)       

    def trans_addr_to_json(self,addr_str):# addr 格式0x00...0a的16进制格式
        if not addr_str.startswith(("0x","0X")):
            print("trans_addr_to_json addr not startswith 0x")
            return "0x00000000"
        length =len(addr_str)
        valid_len = self.addr_byte_len*2 + len("0x")
        if length > valid_len:#检查长度是否超标
            print("addr len error:%s" % (length,))
            return "0x00000000"

        #转换为大写
        addr_str = "0x" + addr_str[2:].upper()

        #当地址长度不够json配置文件中指定的 valid_len长度时，调整下以字符串方式表示的地址长度
        zero_pad_len = valid_len - length
        addr_str = addr_str[0:2] + "0"*zero_pad_len + addr_str[2:]#长度不够，补 0
        return addr_str

    def trans_value_to_json(self,value_str):
        return self.trans_addr_to_json(value_str)

    def get_addr_value(self, addr_str):#addr 是字符串格式，获取json中addr对应的value值
        addr_str = self.trans_addr_to_json(addr_str)
        if addr_str in self.cfg_addr_list:
            value = self.json_reg_cfg_data[addr_str]["value"]
        elif addr_str in self.value_addr_list:
            value = self.json_reg_value_data[addr_str]
        else:
            #print("need_to_do: pop not found addr Message ",reply)
            #value =  "0x00000000"
            return None

        value = self.trans_addr_to_json(value)
        return value #返回值为字符串格式
        
    def get_reset_value(self, addr_str):
        addr_str = self.trans_addr_to_json(addr_str)
        if addr_str in self.cfg_addr_list:
            value = self.json_reg_cfg_data[addr_str]["reset_value"]
        else:
            #print("need_to_do: pop not found addr Message ",reply)
            #value =  "0x00000000"
            return None

        value = self.trans_addr_to_json(value)
        return value #返回值为字符串格式

    def set_addr_value(self, addr_str, value_str):
        addr_str = self.trans_addr_to_json(addr_str)
        self.json_reg_cfg_data[addr_str]["value"] = self.trans_value_to_json(value_str)

    def get_all_cfg_addr_list(self):
        for k,v in self.json_reg_cfg_data.items():
            #print(k,type(k))
            if "total_cfg" == k:
                continue
            self.cfg_addr_list.append(k)

if __name__ == "__main__":
    reg = RegisterJson("./register.json")
    
    ret = reg.get_addr_value("0x00000004")
    print(ret)
    reg.set_addr_value("0x00000004","0xcc0FF")
    ret = reg.get_addr_value("0x00000004")
    print(ret)
    
    reg.write_json(reg.json_reg_cfg_data,reg.register_cfg_file_path)
    
